"""Regenerate results/audit/test_v4_attribution_summary.json: attribution of the first-freeze witness
samples (5 sources x 100 witnesses) from the key and the AI annotation passes.

Inputs: results/audit/test_v4_key.json (idx -> source 'Method@Tier', pair_id), test_v4_ann_a.json and
test_v4_ann_b.json (two blind passes, 500 items each), test_v4_ann_c.json (third pass on the 42
disagreements only).
Definitions (same rules as the attribution routine of analyze_r.py):
  * final verdict = pass A if A == B, else pass C (adjudication);
  * agreement: n = items in both passes, agree = A == B, Cohen's kappa of A vs B, adjudicated = |pass C|;
  * per source (in key order): counts of final verdicts (in key order of first occurrence),
    implausible_share = implausible_data / n with Wilson 95% CI,
    meaningful = n - implausible_data (pred_wrong + gold_wrong + both_wrong + ambiguous) with Wilson 95% CI,
    errors = pred_wrong + both_wrong with Wilson 95% CI;
  * certified = number of EX-correct (system, question) pairs certified at the sampled tier (L1f or L0),
    computed as in recert_r_counts.py (Fuzz = corrected fuzzing baseline, amendment P2);
  * est_meaningful = certified * meaningful / n, est_errors = certified * errors / n, and their CIs are the
    share CIs scaled by certified.

Usage (from src_r/):
    python attribution_v4_summary.py --out ../results/audit/test_v4_attribution_summary.json
"""
import argparse
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_r import wilson  # noqa: E402
from recert_r_counts import counts  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
A = os.path.join(ROOT, 'results', 'audit')


def load(name):
    return json.load(open(os.path.join(A, name)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--prefix', default='test_v4')
    a = ap.parse_args()
    key = load(f'{a.prefix}_key.json')
    ann_a = {x['idx']: x['verdict'] for x in load(f'{a.prefix}_ann_a.json')}
    ann_b = {x['idx']: x['verdict'] for x in load(f'{a.prefix}_ann_b.json')}
    ann_c = {x['idx']: x['verdict'] for x in load(f'{a.prefix}_ann_c.json')}
    both = [x['idx'] for x in key if x['idx'] in ann_a and x['idx'] in ann_b]
    agree = sum(ann_a[i] == ann_b[i] for i in both)
    ca, cb = Counter(ann_a[i] for i in both), Counter(ann_b[i] for i in both)
    pe = sum(ca[k] * cb[k] for k in ca) / len(both) ** 2
    po = agree / len(both)
    S = dict(agreement=dict(n=len(both), agree=agree, kappa=(po - pe) / (1 - pe), adjudicated=len(ann_c)))
    final = {i: (ann_a[i] if ann_a[i] == ann_b[i] else ann_c[i]) for i in both}
    sources = list(dict.fromkeys(x['source'] for x in key))
    cert = counts()
    methods = {}
    for src in sources:
        c = Counter(final[x['idx']] for x in key if x['source'] == src)
        n = sum(c.values())
        imp = c['implausible_data']
        ici = wilson(imp, n)
        err = c['pred_wrong'] + c['both_wrong']
        eci = wilson(err, n)
        name, _, tier = src.partition('@')
        N = cert[name][tier]
        mci = wilson(n - imp, n)
        d = dict(n=n, counts=dict(c), implausible_share=imp / n, implausible_ci=ici,
                 meaningful=n - imp, meaningful_ci=mci, errors=err, errors_ci=eci, certified=N,
                 est_meaningful=N * (n - imp) / n, est_meaningful_ci=[N * x for x in mci],
                 est_errors=N * err / n, est_errors_ci=[N * x for x in eci])
        if name == 'Fuzz':
            d['certified_note'] = 'corrected fuzzing baseline (P2)'
        methods[src] = d
    S['methods'] = methods
    json.dump(S, open(a.out, 'w'), indent=1)
    print(json.dumps(S['agreement']), {k: v['counts'] for k, v in methods.items()})


if __name__ == '__main__':
    main()
