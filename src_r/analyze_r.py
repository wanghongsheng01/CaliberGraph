"""Second-freeze analysis (tier R): counts per method and tier, paired tests, known-positive recall,
per-system effect, and attribution summaries. Results on distinct triples are expanded to systems.

Usage: python analyze_r.py --split test --out ../results/test_r/summary_r.json \
          --exc CaliberGraph-R=../results/test_r/cgx_r_exc.jsonl --exc Fuzz-R=... \
          --exi CaliberGraph-R=../results/test_r/cgx_r_exi.jsonl ... \
          [--attr ../results/audit/test_r_key.json:../results/audit/test_r_ann_a.json[:...ann_b.json]]
"""
import argparse
import json
import math
import os
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from score import load_pairs, expand, is_cert  # noqa: E402
from stats_eval import mcnemar_exact, cluster_bootstrap  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
TIERS = ['L0', 'L1f', 'L2', 'Rq', 'R', 'R2']
MEANINGFUL = ('pred_wrong', 'gold_wrong', 'both_wrong', 'ambiguous')


def wilson(k, n, z=1.96):
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [(c - h) / d, (c + h) / d]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--split', default='test')
    ap.add_argument('--out', required=True)
    ap.add_argument('--exc', action='append', default=[])
    ap.add_argument('--exi', action='append', default=[])
    ap.add_argument('--attr', action='append', default=[])
    ap.add_argument('--boot', type=int, default=10000)
    ap.add_argument('--h7-ref', dest='h7_ref', default='', help='k/n implausible witnesses of the reference sample')
    ap.add_argument('--abl', action='append', default=[], help='name=path evaluated on the --abl-ids subsample')
    ap.add_argument('--abl-ids', dest='abl_ids', default='')
    ap.add_argument('--ids', default='', help='restrict EX-correct population to these distinct pair_ids (dev subsamples)')
    a = ap.parse_args()
    allp = [p for p in load_pairs(a.split) if p['source'] != 'parseval_model']
    exc = [p for p in allp if p['ex'] == 'correct']
    ok = json.load(open(os.path.join(ROOT, 'data', 'exec_check.json')))
    exi = [p for p in allp if p['ex'] == 'incorrect' and ok[p['pair_id']]['pred'] is True]
    if a.ids:
        keep = set(json.load(open(a.ids))['pair_ids'])
        rep = {}
        for p in allp:
            k = (p['qid'], p['gold'].strip(), p['pred'].strip())
            if p['pair_id'] in keep:
                rep[k] = True
        exc = [p for p in exc if rep.get((p['qid'], p['gold'].strip(), p['pred'].strip()))]
        exi = [p for p in exi if rep.get((p['qid'], p['gold'].strip(), p['pred'].strip()))]
    S = dict(split=a.split, n_exc=len(exc), n_exi=len(exi))
    M = {}
    for spec in a.exc:
        name, path = spec.split('=', 1)
        if os.path.exists(path):
            M[name] = expand([json.loads(l) for l in open(path)], exc)

    def ind(name, tier):
        return {p['pair_id']: is_cert(M[name].get(p['pair_id']), tier, 'C_set', p) for p in exc}
    S['main'] = {name: {t: sum(ind(name, t).values()) for t in TIERS} for name in M}
    tt = {}
    for spec in a.exc:
        name, path = spec.split('=', 1)
        if os.path.exists(path):
            ts = sorted(r.get('search_s', 0.0) for r in map(json.loads, open(path)) if (r.get('cert_R') or {}).get('ok') and r.get('found'))
            if ts:
                tt[name] = dict(n=len(ts), median=ts[len(ts) // 2], p95=ts[int(0.95 * (len(ts) - 1))], within1=sum(1 for x in ts if x <= 1) / len(ts))
    S['time_to_witness_R'] = tt
    tests = []
    names = list(M)
    if names:
        ref = names[0]
        for other in names[1:]:
            for tier in ('R', 'Rq'):
                A, B = ind(ref, tier), ind(other, tier)
                b = sum(1 for k in A if A[k] and not B[k])
                c = sum(1 for k in A if B[k] and not A[k])
                lo, hi = cluster_bootstrap(exc, A, B, a.boot)
                tests.append(dict(a=ref, b=other, tier=tier, count_a=sum(A.values()), count_b=sum(B.values()),
                                  a_only=b, b_only=c, diff=sum(A.values()) - sum(B.values()), ci95=[lo, hi],
                                  p=mcnemar_exact(b, c)))
    S['tests'] = tests
    # per-system effect at the data-profile tier (first method = reference) and at the schema tier
    if names:
        ref = names[0]
        sysn = {'alpha': 'Alpha-SQL', 'chess': 'CHESS', 'csc-32b': 'CSC-SQL-32B', 'csc-7b': 'CSC-SQL-7B',
                'gena_submission_1': 'GenaSQL-1', 'gena_submission_2': 'GenaSQL-2', 'gsr': 'GSR',
                'omni-32-majority': 'OmniSQL-32B', 'rsl': 'RSL-SQL', 'slm': 'SLM-SQL'}
        R = ind(ref, 'R')
        per = {}
        for src in sorted({p['source'] for p in allp}):
            n_all = sum(1 for p in allp if p['source'] == src)
            n_ex = sum(1 for p in exc if p['source'] == src)
            w = sum(1 for p in exc if p['source'] == src and R[p['pair_id']])
            per[src] = dict(name=sysn.get(src, src), n=n_all, ex=n_ex / n_all, r_witnesses=w, r_share=w / n_ex if n_ex else 0)
        S['per_system_R'] = per
    rec = {}
    for spec in a.exi:
        name, path = spec.split('=', 1)
        if not os.path.exists(path):
            continue
        m = expand([json.loads(l) for l in open(path)], exi)
        rec[name] = {t: sum(1 for p in exi if is_cert(m.get(p['pair_id']), t, 'C_set', p)) / max(1, len(exi)) for t in TIERS}
    S['known_positive_recall'] = rec
    # attribution: key file + one or two annotation files (second pass: agreement)
    att = {}
    for spec in a.attr:
        parts = spec.split(':')
        key = {x['idx']: x for x in json.load(open(parts[0]))}
        anns = [{x['idx']: x for x in json.load(open(f))} for f in parts[1:] if os.path.exists(f)]
        if not anns:
            continue
        final = {}
        for i in key:
            vs = [an[i]['verdict'] for an in anns if i in an]
            if not vs:
                continue
            if len(vs) == 1 or vs[0] == vs[1]:
                final[i] = vs[0]
            else:
                final[i] = vs[2] if len(vs) > 2 else vs[0]  # a third pass adjudicates disagreements
        by = defaultdict(Counter)
        for i, v in final.items():
            by[key[i]['source']][v] += 1
        for src, c in by.items():
            n = sum(c.values())
            m = sum(c[v] for v in MEANINGFUL)
            att[src] = dict(n=n, counts=dict(c), meaningful=m, meaningful_share=m / n, meaningful_ci=wilson(m, n),
                            implausible_share=c['implausible_data'] / n, implausible_ci=wilson(c['implausible_data'], n),
                            errors=c['pred_wrong'] + c['both_wrong'], benchmark_issues=c['gold_wrong'] + c['ambiguous'])
        if len(anns) >= 2:
            both = [i for i in key if i in anns[0] and i in anns[1]]
            agree = sum(anns[0][i]['verdict'] == anns[1][i]['verdict'] for i in both)
            ca, cb = Counter(anns[0][i]['verdict'] for i in both), Counter(anns[1][i]['verdict'] for i in both)
            pe = sum(ca[k] * cb[k] for k in ca) / max(1, len(both)) ** 2
            po = agree / max(1, len(both))
            att['_agreement'] = dict(n=len(both), agree=agree, kappa=(po - pe) / (1 - pe) if pe < 1 else 1.0)
    S['attribution'] = att
    # estimated meaningful witnesses = certified count at the sampled tier x meaningful share (parametric bootstrap)
    est = {}
    rng = random.Random(7)
    for src, v in att.items():
        if src.startswith('_'):
            continue
        name, _, tier = src.partition('@')
        if name in S['main'] and tier in TIERS:
            N = S['main'][name][tier]
            draws = sorted(N * sum(rng.random() < v['meaningful_share'] for _ in range(v['n'])) / v['n'] for _ in range(2000))
            est[src] = dict(count=N, estimate=N * v['meaningful_share'], ci95=[draws[50], draws[1949]])
    for src, v in att.items():
        if src.startswith('_') or src not in est:
            continue
        N = est[src]['count']
        e = v['errors'] / v['n']
        est[src]['errors_estimate'] = N * e
        est[src]['errors_ci95'] = [N * x for x in wilson(v['errors'], v['n'])]
    S['estimated_meaningful'] = est
    # H6: difference of estimated meaningful witnesses (parametric bootstrap over both samples)
    srcs = sorted(est, key=lambda k: (not k.startswith('CaliberGraph-R'), k))
    if len(srcs) >= 2:
        a1, b1 = srcs[0], srcs[1]
        da = []
        for _ in range(10000):
            xa = est[a1]['count'] * sum(rng.random() < att[a1]['meaningful_share'] for _ in range(att[a1]['n'])) / att[a1]['n']
            xb = est[b1]['count'] * sum(rng.random() < att[b1]['meaningful_share'] for _ in range(att[b1]['n'])) / att[b1]['n']
            da.append(xa - xb)
        da.sort()
        S['h6'] = dict(a=a1, b=b1, diff=est[a1]['estimate'] - est[b1]['estimate'], ci95=[da[250], da[9749]],
                       p_one_sided=sum(1 for x in da if x <= 0) / len(da))
    # H7: implausible share of the first source vs. a reference share (first-freeze CaliberGraph)
    if a.h7_ref and srcs:
        k_ref, n_ref = map(int, a.h7_ref.split('/'))
        v = att[srcs[0]]
        k1, n1 = v['counts'].get('implausible_data', 0), v['n']
        p = (k1 + k_ref) / (n1 + n_ref)
        z = (k_ref / n_ref - k1 / n1) / math.sqrt(p * (1 - p) * (1 / n1 + 1 / n_ref)) if 0 < p < 1 else 0.0
        S['h7'] = dict(share=k1 / n1, ref_share=k_ref / n_ref, z=z, p_one_sided=0.5 * math.erfc(z / math.sqrt(2)))
    if a.abl and a.abl_ids:
        sub = set(json.load(open(a.abl_ids))['pair_ids'])
        Pm = {p['pair_id']: p for p in allp}
        abl = {}
        for spec in a.abl:
            name, path = spec.split('=', 1)
            if not os.path.exists(path):
                continue
            byid = {json.loads(l)['pair_id']: json.loads(l) for l in open(path)}
            abl[name] = {t: sum(1 for k in sub if k in Pm and is_cert(byid.get(k), t, 'C_set', Pm[k])) for t in ('L1f', 'R')}
        S['ablation_R'] = dict(n=len(sub), counts=abl)
    json.dump(S, open(a.out, 'w'), indent=1)
    print(json.dumps({k: v for k, v in S.items() if k != 'attribution'}, indent=1)[:4000])
    print(json.dumps(att, indent=1)[:3000])


if __name__ == '__main__':
    main()
