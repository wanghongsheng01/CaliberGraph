"""Produce every number, table and figure input used in the paper from saved result files.

Usage: python analyze.py --split test --dir ../results/test --out ../results/test/summary.json
All counts are over (system, question) pairs unless stated otherwise; results computed on distinct
(question, gold, prediction) triples are expanded to every system that produced that prediction.
"""
import argparse
import json
import os
import re
import statistics
from collections import Counter, defaultdict

from score import load_pairs, expand, is_cert
from stats_eval import mcnemar_exact, cluster_bootstrap

ROOT = os.path.join(os.path.dirname(__file__), '..')
HOLDOUT = {'formula_1', 'superhero', 'toxicology'}
SYSTEM_NAMES = {'alpha': 'Alpha-SQL', 'chess': 'CHESS', 'csc-32b': 'CSC-SQL-32B', 'csc-7b': 'CSC-SQL-7B',
                'gena_submission_1': 'GenaSQL-1', 'gena_submission_2': 'GenaSQL-2', 'gsr': 'GSR',
                'omni-32-majority': 'OmniSQL-32B', 'rsl': 'RSL-SQL', 'slm': 'SLM-SQL'}


def load(path):
    return [json.loads(l) for l in open(path)] if os.path.exists(path) else None


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, m, prev = [0] * len(ps), len(ps), 0
    for rank, i in enumerate(order):
        v = min(1.0, (m - rank) * ps[i])
        prev = max(prev, v)
        adj[i] = prev
    return adj


def kendall_tau(a, b):
    """Kendall's tau-b (ties in either ranking handled)."""
    keys = list(a)
    conc = disc = ta = tb = 0
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            da, db = a[keys[i]] - a[keys[j]], b[keys[i]] - b[keys[j]]
            if da == 0 and db == 0:
                continue
            if da == 0:
                ta += 1
            elif db == 0:
                tb += 1
            elif da * db > 0:
                conc += 1
            else:
                disc += 1
    den = ((conc + disc + ta) * (conc + disc + tb)) ** 0.5
    return (conc - disc) / den if den else 1.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--split', default='test')
    ap.add_argument('--dir', default='../results/test')
    ap.add_argument('--out', required=True)
    ap.add_argument('--boot', type=int, default=10000)
    ap.add_argument('--fuzz-exc', dest='fuzz_exc', default='')
    ap.add_argument('--fuzz-exi', dest='fuzz_exi', default='')
    a = ap.parse_args()
    D = a.dir
    all_pairs = [p for p in load_pairs(a.split) if p['source'] != 'parseval_model']
    ok = json.load(open(os.path.join(ROOT, 'data', 'exec_check.json')))
    exc = [p for p in all_pairs if p['ex'] == 'correct']
    exi = [p for p in all_pairs if p['ex'] == 'incorrect' and ok[p['pair_id']]['pred'] is True]
    pre = 'dev_' if a.split == 'dev' else ''
    files_exc = {
        'CaliberGraph': f'{D}/cgx_exc.jsonl', 'CaliberGraph+SC': f'{D}/cgx_sc_exc.jsonl',
        'ParSEval-L1': f'{D}/parseval_l1_exc.jsonl', 'ParSEval (official)': f'{D}/parseval_official_exc.jsonl',
        'Random fuzzing': a.fuzz_exc or f'{D}/fuzz_exc.jsonl',
        'SpotIt': os.path.join(ROOT, 'results', f'{a.split}_spotit_vanilla_null.jsonl'),
        'SpotIt+': os.path.join(ROOT, 'results', f'{a.split}_spotit_llm.jsonl'),
    }
    S = dict(split=a.split, n_exc=len(exc), n_exi=len(exi), n_questions_exc=len({p['qid'] for p in exc}),
             n_distinct_exc=len({(p['qid'], p['gold'].strip(), p['pred'].strip()) for p in exc}))
    M = {}
    for name, f in files_exc.items():
        r = load(f)
        if r is not None:
            M[name] = expand(r, exc)
    tiers = ['L0', 'L1', 'L1f', 'L1n', 'O1f', 'O1n', 'L2']
    contracts = ['C_set', 'C_bag', 'C_lenient']

    def ind(name, tier='L1f', contract='C_set', claims=False):
        m = M[name]
        if claims:
            return {p['pair_id']: bool(m.get(p['pair_id'], {}).get('author_claim')) for p in exc}
        return {p['pair_id']: is_cert(m.get(p['pair_id']), tier, contract, p) for p in exc}

    # ---- main table
    main = {}
    for name in M:
        row = {t: sum(ind(name, t).values()) for t in tiers}
        row['contracts_L1f'] = {c: sum(ind(name, 'L1f', c).values()) for c in contracts}
        if name.startswith('SpotIt'):
            row['author_claims'] = sum(ind(name, claims=True).values())
        main[name] = row
    S['main'] = main
    # ---- paired tests (primary: L1f vs SpotIt claims; L2 SC vs SpotIt+ claims; vs ParSEval-L1 / fuzz)
    tests = []

    def paired(n1, n2, t1='L1f', t2='L1f', claims2=False, label=''):
        if n1 not in M or n2 not in M:
            return
        A, B = ind(n1, t1), ind(n2, t2, claims=claims2)
        b = sum(1 for k in A if A[k] and not B[k])
        c = sum(1 for k in A if B[k] and not A[k])
        lo, hi = cluster_bootstrap(exc, A, B, a.boot)
        tests.append(dict(label=label, a=n1, b=n2, tier_a=t1, tier_b=t2 if not claims2 else 'author-claims',
                          count_a=sum(A.values()), count_b=sum(B.values()), a_only=b, b_only=c,
                          diff=sum(A.values()) - sum(B.values()), ci95=[lo, hi], p=mcnemar_exact(b, c)))
    paired('CaliberGraph', 'SpotIt', claims2=True, label='H1')
    paired('CaliberGraph+SC', 'SpotIt+', t1='L2', claims2=True, label='H2')
    paired('CaliberGraph', 'ParSEval-L1', label='vs ParSEval-L1')
    paired('CaliberGraph', 'Random fuzzing', label='vs fuzzing')
    paired('CaliberGraph', 'SpotIt+', claims2=True, label='vs SpotIt+ claims (L1f)')
    S['tests'] = tests
    # ---- known positives
    files_exi = {'CaliberGraph': f'{D}/cgx_exi.jsonl', 'ParSEval-L1': f'{D}/parseval_l1_exi.jsonl',
                 'Random fuzzing': a.fuzz_exi or f'{D}/fuzz_exi.jsonl',
                 'SpotIt (claims)': os.path.join(ROOT, 'results', f'{a.split}_spotit_null_raw.jsonl')}
    rec = {}
    for name, f in files_exi.items():
        r = load(f)
        if r is None:
            continue
        m = expand(r, exi)
        if 'claims' in name:
            n = sum(1 for p in exi if m.get(p['pair_id'], {}).get('author_claim'))
            rec[name] = dict(found=n, recall=n / len(exi))
        else:
            rec[name] = {t: sum(1 for p in exi if is_cert(m.get(p['pair_id']), t, 'C_set', p)) / len(exi) for t in ('L0', 'L1', 'L1f', 'L1n', 'L2')}
            rec[name]['found_L1f'] = sum(1 for p in exi if is_cert(m.get(p['pair_id']), 'L1f', 'C_set', p))
    S['known_positive_recall'] = rec
    # H3: recall of CaliberGraph > ParSEval-L1 and > SpotIt (claims) on known positives; paired McNemar on
    # the same pairs; H3 holds if both comparisons hold (intersection-union test: p = max of the two)
    exi_m = {}
    for name, f in files_exi.items():
        r = load(f)
        if r is not None:
            exi_m[name] = expand(r, exi)
    h3 = []
    if 'CaliberGraph' in exi_m:
        A = {p['pair_id']: is_cert(exi_m['CaliberGraph'].get(p['pair_id']), 'L1f', 'C_set', p) for p in exi}
        for nb in ('ParSEval-L1', 'SpotIt (claims)', 'Random fuzzing'):
            if nb not in exi_m:
                continue
            if 'claims' in nb:
                B = {p['pair_id']: bool(exi_m[nb].get(p['pair_id'], {}).get('author_claim')) for p in exi}
            else:
                B = {p['pair_id']: is_cert(exi_m[nb].get(p['pair_id']), 'L1f', 'C_set', p) for p in exi}
            b = sum(1 for k in A if A[k] and not B[k])
            c = sum(1 for k in A if B[k] and not A[k])
            h3.append(dict(b=nb, a_only=b, b_only=c, p=mcnemar_exact(b, c), count_a=sum(A.values()), count_b=sum(B.values())))
    S['h3_tests'] = h3
    fam = [t for t in tests if t['label'] in ('H1', 'H2')]
    ps = [t['p'] for t in fam]
    comp = [t for t in h3 if t['b'] in ('ParSEval-L1', 'SpotIt (claims)')]
    if len(comp) == 2:
        ps.append(max(t['p'] for t in comp))
    adj = holm(ps)
    for t, pa in zip(fam, adj):
        t['p_holm'] = pa
    if len(comp) == 2:
        S['h3'] = dict(p=max(t['p'] for t in comp), p_holm=adj[-1])
    # ---- per-system accuracy correction and ranking
    if 'CaliberGraph' in M:
        allm = [n for n in M if not n.startswith('SpotIt')]
        union = {p['pair_id']: any(is_cert(M[n].get(p['pair_id']), 'L1f', 'C_set', p) for n in allm) for p in exc}
        cg = ind('CaliberGraph')
        per = {}
        for src in sorted({p['source'] for p in all_pairs}):
            n_all = sum(1 for p in all_pairs if p['source'] == src)
            n_ex = sum(1 for p in exc if p['source'] == src)
            fp = sum(1 for p in exc if p['source'] == src and cg[p['pair_id']])
            fpu = sum(1 for p in exc if p['source'] == src and union[p['pair_id']])
            spot = sum(1 for p in exc if p['source'] == src and p['spotit'] == 'incorrect')
            per[src] = dict(name=SYSTEM_NAMES.get(src, src), n=n_all, ex=n_ex / n_all, cg_fp=fp, union_fp=fpu,
                            spotit_fp=spot, corrected=(n_ex - fp) / n_all, corrected_union=(n_ex - fpu) / n_all,
                            fp_share=fp / n_ex if n_ex else 0)
        ex_rank = {k: v['ex'] for k, v in per.items()}
        cor = {k: v['corrected'] for k, v in per.items()}
        S['per_system'] = per
        S['kendall_tau_ex_vs_corrected'] = kendall_tau(ex_rank, cor)
        S['kendall_tau_ex_vs_spotit_corrected'] = kendall_tau(ex_rank, {k: (v['ex'] * v['n'] - v['spotit_fp']) / v['n'] for k, v in per.items()})
        rk = lambda d: {k: i + 1 for i, k in enumerate(sorted(d, key=lambda x: -d[x]))}  # noqa: E731
        S['rank_ex'], S['rank_corrected'] = rk(ex_rank), rk(cor)
        # holdout vs seen schemas
        hs = defaultdict(lambda: [0, 0])
        for p in exc:
            g = 'held-out schemas' if p['db_id'] in HOLDOUT else 'other schemas'
            hs[g][0] += 1
            hs[g][1] += cg[p['pair_id']]
        S['schema_groups'] = {k: dict(n=v[0], found=v[1], rate=v[1] / v[0]) for k, v in hs.items()}
        # difficulty
        dd = defaultdict(lambda: [0, 0])
        for p in exc:
            dd[p['difficulty']][0] += 1
            dd[p['difficulty']][1] += cg[p['pair_id']]
        S['difficulty'] = {k: dict(n=v[0], found=v[1], rate=v[1] / v[0]) for k, v in dd.items()}
        # time to witness (distinct runs)
        tt = {}
        for name, f in files_exc.items():
            r = load(f)
            if r is None or name.startswith('SpotIt'):
                continue
            ts = [x.get('search_s', 0.0) for x in r
                  if x.get('cert') and x['cert'].get('L1f') and x['cert']['differ'].get('C_set')]
            if ts:
                ts.sort()
                tt[name] = dict(n=len(ts), median=statistics.median(ts), p95=ts[int(0.95 * (len(ts) - 1))], max=ts[-1],
                                curve=[sum(1 for x in ts if x <= b) for b in (0.01, 0.03, 0.1, 0.3, 1, 2, 3, 4, 5)])
        S['time_to_witness'] = tt
        sp = [x.get('released_time_s') for x in load(files_exc['SpotIt']) or [] if x.get('released_time_s') is not None]
        if sp:
            sp.sort()
            S['spotit_released_time'] = dict(n=len(sp), median=statistics.median(sp), p95=sp[int(0.95 * (len(sp) - 1))],
                                             total_h=sum(sp) / 3600)
    # ---- ablations and budget (subsample)
    sub_path = os.path.join(ROOT, 'data', 'test_subsample.json')
    if a.split == 'test' and os.path.exists(sub_path):
        sub_ids = set(json.load(open(sub_path))['pair_ids'])
        subp = [p for p in exc if p['pair_id'] in sub_ids]
        abl = {}
        for name, f in [('full', f'{D}/cgx_exc.jsonl'), ('-anchoring', f'{D}/abl_cgx_noanchor.jsonl'),
                        ('-isolation', f'{D}/abl_cgx_noiso.jsonl'), ('-join graph', f'{D}/abl_cgx_nojoin.jsonl'),
                        ('-SQLite domain', f'{D}/abl_cgx_nodomain.jsonl'), ('full, 10 s', f'{D}/budget10_cgx.jsonl'),
                        ('ParSEval-L1, 5 s', f'{D}/parseval_l1_exc.jsonl'), ('ParSEval-L1, 10 s', f'{D}/budget10_parseval_l1.jsonl')]:
            r = load(f)
            if r is None:
                continue
            byid = {x['pair_id']: x for x in r}
            abl[name] = sum(1 for p in subp if is_cert(byid.get(p['pair_id']), 'L1f', 'C_set', p))
        S['subsample'] = dict(n=len(subp), counts=abl)
    json.dump(S, open(a.out, 'w'), indent=1)
    print(json.dumps({k: v for k, v in S.items() if k not in ('per_system',)}, indent=1)[:6000])


if __name__ == '__main__':
    main()
