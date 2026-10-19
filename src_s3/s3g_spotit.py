"""Analysis of the local SpotIt re-run (pre-registration docs/en/17d).

Primary (test, EX-correct, (system, question) pairs, expanded from distinct triples with score.expand):
  H-SP1  CaliberGraph (first freeze, results/test/cgx_exc.jsonl) vs re-run SpotIt at A_1f, exact McNemar one-sided
  H-SP2  the same at A_0. Holm over {H-SP1, H-SP2}; 95% CI from the question-clustered bootstrap (10,000, seed 0).
Descriptive: re-run counts at L0, L1, L1f, Rq, R next to released claims and recertified released witnesses;
CG-R (results/test_r/cgx_r_exc.jsonl) at Rq/R; agreement of re-run vs released verdict on dev and test;
time to counterexample, errors, budget exhaustion; diagnostic re-cased certification.
Usage: python src_s3/s3g_spotit.py --out results/stage3/spotit/s3g_spotit.json
"""
import argparse
import json
import math
import os
import statistics
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src_r'))
from score import load_pairs, expand, is_cert  # noqa: E402
from stats_eval import cluster_bootstrap, mcnemar_exact  # noqa: E402

SP = os.path.join(ROOT, 'results', 'stage3', 'spotit')
TIERS = ('L0', 'L1', 'L1f', 'Rq', 'R')


def load(p):
    return [json.loads(l) for l in open(p)]


def mcnemar_one_sided(b, c):
    """P(X >= b), X ~ Binom(b + c, 1/2): evidence that A-only discordances exceed B-only ones."""
    n = b + c
    if n == 0:
        return 1.0
    lp = [math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) - n * math.log(2) for i in range(b, n + 1)]
    m = max(lp)
    return min(1.0, math.exp(m) * sum(math.exp(x - m) for x in lp))


def log10_p_one_sided(b, c):
    """log10 of mcnemar_one_sided, for p-values below double precision."""
    n = b + c
    if n == 0:
        return 0.0
    lp = [math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) - n * math.log(2) for i in range(b, n + 1)]
    m = max(lp)
    return min(0.0, (m + math.log(sum(math.exp(x - m) for x in lp))) / math.log(10))


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, prev = [0.0] * len(ps), 0.0
    for rank, i in enumerate(order):
        prev = max(prev, min(1.0, (len(ps) - rank) * ps[i]))
        adj[i] = prev
    return adj


def recased(r):
    if not r or not r.get('cert_recased'):
        return None
    r2 = dict(r)
    r2['cert'] = r['cert_recased']
    return r2


def describe(rows):
    v = Counter(r.get('spotit_verdict') for r in rows)
    t_ce = [r['search_s'] for r in rows if r.get('spotit_verdict') == 'incorrect' and r.get('search_s') is not None]
    return dict(n=len(rows), verdicts=dict(v), killed=sum(1 for r in rows if r.get('killed')),
                ce_bound=dict(Counter(r.get('ce_bound') for r in rows if r.get('ce_bound'))),
                time_to_ce=dict(n=len(t_ce), median=statistics.median(t_ce) if t_ce else None,
                                p95=sorted(t_ce)[int(0.95 * (len(t_ce) - 1))] if t_ce else None),
                wall_median=statistics.median([r['wall_s'] for r in rows if r.get('wall_s') is not None]))


def agreement(rows, split):
    pairs = {p['pair_id']: p for p in load_pairs(split)}
    c = Counter((pairs[r['pair_id']].get('spotit'), r.get('spotit_verdict')) for r in rows)
    both = sum(n for (a, b), n in c.items() if a in ('incorrect', 'unknown') and b in ('incorrect', 'unknown'))
    agree = sum(n for (a, b), n in c.items() if a == b and a in ('incorrect', 'unknown'))
    rel_ce = sum(n for (a, b), n in c.items() if a == 'incorrect')
    both_ce = c.get(('incorrect', 'incorrect'), 0)
    return dict(table={f'{a}->{b}': n for (a, b), n in sorted(c.items(), key=lambda x: -x[1])},
                agree_over_decided=[agree, both], released_ce_found_again=[both_ce, rel_ce],
                new_ce=sum(n for (a, b), n in c.items() if b == 'incorrect' and a != 'incorrect'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--boot', type=int, default=10000)
    a = ap.parse_args()
    S = {}
    dev = load(os.path.join(SP, 'spotit_dev_exc.jsonl'))
    test = load(os.path.join(SP, 'spotit_test_exc.jsonl'))
    exc = [p for p in load_pairs('test') if p['source'] != 'parseval_model' and p['ex'] == 'correct']
    S['n_pairs'] = len(exc)
    S['n_distinct'] = len({(p['qid'], p['gold'].strip(), p['pred'].strip()) for p in exc})
    S['n_rerun_records'] = len(test)
    files = {'CaliberGraph': os.path.join(ROOT, 'results', 'test', 'cgx_exc.jsonl'),
             'CaliberGraph-R': os.path.join(ROOT, 'results', 'test_r', 'cgx_r_exc.jsonl'),
             'SpotIt (released, recertified)': os.path.join(ROOT, 'results', 'test_spotit_vanilla_null.jsonl')}
    M = {k: expand(load(f), exc) for k, f in files.items()}
    M['SpotIt (re-run)'] = expand(test, exc)
    S['coverage_rerun'] = sum(1 for p in exc if p['pair_id'] in M['SpotIt (re-run)'])

    def ind(name, tier):
        m = M[name]
        return {p['pair_id']: is_cert(m.get(p['pair_id']), tier, 'C_set', p) for p in exc}

    S['counts'] = {k: {t: sum(ind(k, t).values()) for t in TIERS} for k in M}
    S['counts']['SpotIt (released claims)'] = sum(1 for p in exc if p.get('spotit') == 'incorrect')
    S['counts']['SpotIt (re-run claims)'] = sum(1 for p in exc
                                                if (M['SpotIt (re-run)'].get(p['pair_id']) or {}).get('spotit_verdict') == 'incorrect')
    rc = {p['pair_id']: recased(M['SpotIt (re-run)'].get(p['pair_id'])) for p in exc}
    S['counts']['SpotIt (re-run, re-cased, diagnostic)'] = {
        t: sum(1 for p in exc if is_cert(rc[p['pair_id']], t, 'C_set', p)) for t in ('L0', 'L1', 'L1f')}
    tests = []
    for lab, t in (('H-SP1', 'L1f'), ('H-SP2', 'L0')):
        A, B = ind('CaliberGraph', t), ind('SpotIt (re-run)', t)
        b = sum(1 for k in A if A[k] and not B[k])
        c = sum(1 for k in A if B[k] and not A[k])
        lo, hi = cluster_bootstrap(exc, A, B, a.boot)
        tests.append(dict(label=lab, tier=t, cg=sum(A.values()), spotit=sum(B.values()), cg_only=b, spotit_only=c,
                          diff=sum(A.values()) - sum(B.values()), ci95=[lo, hi], p_one_sided=mcnemar_one_sided(b, c), log10_p_one_sided=log10_p_one_sided(b, c),
                          p_two_sided=mcnemar_exact(b, c)))
    for t, pa in zip(tests, holm([t['p_one_sided'] for t in tests])):
        t['p_holm'] = pa
        t['log10_p_holm_bound'] = t['log10_p_one_sided'] + math.log10(len(tests))  # Holm adj. p <= m * p
        t['met'] = pa < 0.05 and t['diff'] > 0
    S['tests'] = tests
    S['describe'] = {'dev': describe(dev), 'test': describe(test)}
    S['agreement'] = {'dev': agreement(dev, 'dev'), 'test': agreement(test, 'test')}
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(S, open(a.out, 'w'), indent=1)
    print(json.dumps({k: S[k] for k in ('n_pairs', 'n_distinct', 'n_rerun_records', 'coverage_rerun', 'counts', 'tests')}, indent=1))


if __name__ == '__main__':
    main()
