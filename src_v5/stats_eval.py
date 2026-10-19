"""Statistics for the protocol: per-method certified counts, paired McNemar exact tests, and
question-clustered bootstrap confidence intervals of count differences.

Usage: python stats_eval.py --split test --subset exc --tier L1f --contract C_set \
          --method CGX=results/test_cgx.jsonl --method ParSEval-L1=results/test_parseval_l1.jsonl ...
Methods named SpotIt* that come from spotit_import can use author claims with ":claims".
"""
import argparse
import json
import math
import os
import random
from collections import defaultdict

from score import load_pairs, expand, is_cert

ROOT = os.path.join(os.path.dirname(__file__), '..')


def mcnemar_exact(b, c):
    """Two-sided exact McNemar p-value for discordant counts b (A only) and c (B only)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    # P(X <= k) for X ~ Binom(n, 0.5), doubled
    logp = [math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) - n * math.log(2) for i in range(k + 1)]
    m = max(logp)
    p = math.exp(m) * sum(math.exp(x - m) for x in logp)
    return min(1.0, 2 * p)


def indicator(spec, pairs, tier, contract):
    name, path = spec.split('=', 1)
    claims = path.endswith(':claims')
    path = path[:-7] if claims else path
    res = [json.loads(l) for l in open(path)]
    m = expand(res, pairs)
    ind = {}
    for p in pairs:
        r = m.get(p['pair_id'])
        if claims:
            ind[p['pair_id']] = bool(r and r.get('author_claim'))
        else:
            ind[p['pair_id']] = is_cert(r, tier, contract, p)
    return name, ind


def cluster_bootstrap(pairs, a, b, n_boot=10000, seed=0):
    by_q = defaultdict(list)
    for p in pairs:
        by_q[p['qid']].append(p['pair_id'])
    qs = sorted(by_q)
    diffs_q = {q: sum(a[i] for i in by_q[q]) - sum(b[i] for i in by_q[q]) for q in qs}
    rng = random.Random(seed)
    stats = []
    for _ in range(n_boot):
        s = 0
        for _ in range(len(qs)):
            s += diffs_q[qs[rng.randrange(len(qs))]]
        stats.append(s)
    stats.sort()
    return stats[int(0.025 * n_boot)], stats[int(0.975 * n_boot) - 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--split', default='test')
    ap.add_argument('--subset', default='exc')
    ap.add_argument('--tier', default='L1f')
    ap.add_argument('--contract', default='C_set')
    ap.add_argument('--method', action='append', required=True)
    ap.add_argument('--ref', default=None, help='reference method name for paired tests (default: first)')
    ap.add_argument('--boot', type=int, default=10000)
    ap.add_argument('--json', default=None)
    a = ap.parse_args()
    pairs = [p for p in load_pairs(a.split) if p['source'] != 'parseval_model']
    pairs = [p for p in pairs if p['ex'] == ('correct' if a.subset == 'exc' else 'incorrect')]
    if a.subset == 'exi':  # known positives: only predictions that execute can have a witness
        ok = json.load(open(os.path.join(ROOT, 'data', 'exec_check.json')))
        pairs = [p for p in pairs if ok[p['pair_id']]['pred'] is True]
    inds = [indicator(s, pairs, a.tier, a.contract) for s in a.method]
    ref = a.ref or inds[0][0]
    R = dict(inds)[ref]
    out = dict(split=a.split, subset=a.subset, tier=a.tier, contract=a.contract, n_pairs=len(pairs),
               n_questions=len({p['qid'] for p in pairs}), methods={})
    print(f'{a.split}/{a.subset} tier={a.tier} contract={a.contract}: {len(pairs)} pairs, {out["n_questions"]} questions')
    for name, ind in inds:
        n = sum(ind.values())
        row = dict(count=n, rate=n / len(pairs))
        if name != ref:
            b = sum(1 for k in ind if R[k] and not ind[k])
            c = sum(1 for k in ind if ind[k] and not R[k])
            lo, hi = cluster_bootstrap(pairs, R, ind, a.boot)
            row.update(ref_only=b, method_only=c, mcnemar_p=mcnemar_exact(b, c), diff=sum(R.values()) - n,
                       diff_ci95=[lo, hi])
        out['methods'][name] = row
        extra = '' if name == ref else f"  {ref}-only={row['ref_only']} {name}-only={row['method_only']} " \
            f"diff={row['diff']} CI95=[{row['diff_ci95'][0]},{row['diff_ci95'][1]}] p={row['mcnemar_p']:.2e}"
        print(f'  {name:22s} {n:6d} ({100 * n / len(pairs):5.1f}%){extra}')
    if a.json:
        json.dump(out, open(a.json, 'w'), indent=1)


if __name__ == '__main__':
    main()
