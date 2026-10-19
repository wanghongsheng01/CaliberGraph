"""Post-hoc re-analyses for the ICDE version, computed from stored outputs only (no method is re-run).
They answer an independent review and are reported as post hoc in the paper.

  1. error-weighted over-statement of EX per system at A_1f and A_R (certified share x attributed
     prediction-error rate), count-based corrections, and Kendall tau_b against EX;
  2. second-freeze counts under the lenient contract C_len (empty result == one all-NULL row);
  3. cluster-bootstrap (by question) intervals for the attribution shares, H6 and H7;
  4. sampled A_R witnesses whose difference is an empty result against one all-NULL row;
  5. results by schema group (held-out vs other schemas);
  6. audit cost of one system audited alone (no de-duplication across systems);
  7. sensitivity of A_R to the categorical-column thresholds (re-certification of stored witnesses).

Usage: python icde_posthoc.py --out ../results/test_r/icde_posthoc.json --tex ../paper_icde/numbers_icde.tex
"""
import argparse
import json
import os
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from score import load_pairs, expand, is_cert  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
HELD_OUT = {'formula_1', 'superhero', 'toxicology'}
MEANINGFUL = ('pred_wrong', 'gold_wrong', 'both_wrong', 'ambiguous')
ERR = ('pred_wrong', 'both_wrong')


def P(*a):
    return os.path.join(ROOT, *a)


def jl(path):
    return [json.loads(l) for l in open(path)]


def kendall_tau_b(x, y):
    from scipy.stats import kendalltau
    return float(kendalltau(x, y).statistic)


def final_verdicts(key, a, b, c):
    A = {x['idx']: x['verdict'] for x in json.load(open(a))}
    B = {x['idx']: x['verdict'] for x in json.load(open(b))}
    C = {x['idx']: x['verdict'] for x in json.load(open(c))}
    out = defaultdict(list)
    for k in json.load(open(key)):
        i = k['idx']
        v = A[i] if A.get(i) == B.get(i) else C.get(i, A.get(i))
        out[k['source']].append((k['pair_id'], v, i))
    return out


def shares(items):
    n = len(items)
    return dict(n=n, meaningful=sum(v in MEANINGFUL for _, v, _ in items) / n,
                implausible=sum(v == 'implausible_data' for _, v, _ in items) / n,
                error=sum(v in ERR for _, v, _ in items) / n)


def cluster_boot(items, B, rng):
    """Resample questions (clusters) with replacement; returns lists of meaningful/implausible/error shares."""
    by_q = defaultdict(list)
    for it in items:
        by_q[it[0].split(':', 1)[1]].append(it)
    qs = list(by_q)
    out = defaultdict(list)
    for _ in range(B):
        s = [it for q in (rng.choice(qs) for _ in qs) for it in by_q[q]]
        sh = shares(s)
        for k in ('meaningful', 'implausible', 'error'):
            out[k].append(sh[k])
    return out, len(qs)


def ci(xs):
    xs = sorted(xs)
    return [xs[int(0.025 * len(xs))], xs[int(0.975 * len(xs)) - 1]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--tex', required=True)
    ap.add_argument('--boot', type=int, default=10000)
    a = ap.parse_args()
    rng = random.Random(20261016)
    S1 = json.load(open(P('results/test/summary.json')))
    S2 = json.load(open(P('results/test_r/summary_r.json')))
    A1 = json.load(open(P('results/audit/test_v4_attribution_summary.json')))
    R = {}
    M = {}  # LaTeX macros

    # ---- attribution verdicts
    v4 = final_verdicts(P('results/audit/test_v4_key.json'), P('results/audit/test_v4_ann_a.json'),
                        P('results/audit/test_v4_ann_b.json'), P('results/audit/test_v4_ann_c.json'))
    vr = final_verdicts(P('results/audit/test_r_key.json'), P('results/audit/test_r_ann_a.json'),
                        P('results/audit/test_r_ann_b.json'), P('results/audit/test_r_ann_c.json'))
    samples = {k: v for k, v in list(v4.items()) + list(vr.items()) if not k.startswith('calib:')}
    e_cg = shares(samples['CaliberGraph@L1f'])['error']
    e_cgr = shares(samples['CaliberGraph-R@R'])['error']

    # ---- 1. per-system corrections
    rows = []
    for k, v in S1['per_system'].items():
        r = S2['per_system_R'][k]
        n = v['n']
        rows.append(dict(system=v['name'], ex=100 * v['ex'],
                         count_1f=100 * v['cg_fp'] / n, count_spotit=100 * v['spotit_fp'] / n,
                         err_1f=100 * v['cg_fp'] * e_cg / n, count_R=100 * r['r_witnesses'] / n,
                         err_R=100 * r['r_witnesses'] * e_cgr / n))
    ex = [x['ex'] for x in rows]
    R['per_system'] = rows
    R['tau'] = {k: kendall_tau_b(ex, [x['ex'] - x[k] for x in rows]) for k in ('count_1f', 'err_1f', 'err_R')}
    for k, name in (('count_1f', 'CountOnef'), ('count_spotit', 'CountSpotIt'), ('err_1f', 'ErrOnef'),
                    ('count_R', 'CountR'), ('err_R', 'ErrR')):
        M['pts%sMin' % name] = f"{min(x[k] for x in rows):.1f}"
        M['pts%sMax' % name] = f"{max(x[k] for x in rows):.1f}"
    M['tauErrOnef'] = f"{R['tau']['err_1f']:.2f}"
    M['tauErrR'] = f"{R['tau']['err_R']:.2f}"
    M['errShareCG'] = f"{100 * e_cg:.0f}"
    M['errShareCGR'] = f"{100 * e_cgr:.0f}"

    # ---- pairs and second-freeze outputs
    allp = [p for p in load_pairs('test') if p['source'] != 'parseval_model']
    exc = [p for p in allp if p['ex'] == 'correct']
    files = {'CaliberGraph-R': P('results/test_r/cgx_r_exc.jsonl'), 'Fuzz-R': P('results/test_r/fuzz_r_exc.jsonl'),
             'CaliberGraph': P('results/test/cgx_exc.jsonl')}
    res = {k: jl(f) for k, f in files.items()}
    exp = {k: expand(v, exc) for k, v in res.items()}

    # ---- 2. C_len at A_R
    R['clen_R'] = {}
    for k in ('CaliberGraph-R', 'Fuzz-R'):
        e = exp[k]
        cset = sum(1 for p in exc if is_cert(e.get(p['pair_id']), 'R', 'C_set', p))
        clen = sum(1 for p in exc if is_cert(e.get(p['pair_id']), 'R', 'C_lenient', p))
        R['clen_R'][k] = dict(C_set=cset, C_len=clen)
    M['nCGRAtRClen'] = f"{R['clen_R']['CaliberGraph-R']['C_len']:,}".replace(',', '{,}')
    M['nFZRAtRClen'] = f"{R['clen_R']['Fuzz-R']['C_len']:,}".replace(',', '{,}')

    # ---- 3. cluster bootstrap of attribution shares; H6, H7
    R['attribution_cluster'] = {}
    boots = {}
    for k, items in samples.items():
        bt, nq = cluster_boot(items, a.boot, rng)
        boots[k] = bt
        sh = shares(items)
        R['attribution_cluster'][k] = dict(n=sh['n'], questions=nq, **{x: [sh[x], ci(bt[x])] for x in ('meaningful', 'implausible', 'error')})
    nq = [v['questions'] for v in R['attribution_cluster'].values()]
    M['attrQMin'], M['attrQMax'] = str(min(nq)), str(max(nq))
    # certified counts at A_R (system pairs), recomputed from the outputs; treated as fixed in the bootstrap
    cnt = {'CaliberGraph-R@R': sum(1 for p in exc if is_cert(exp['CaliberGraph-R'].get(p['pair_id']), 'R', 'C_set', p)),
           'Fuzz-R@R': sum(1 for p in exc if is_cert(exp['Fuzz-R'].get(p['pair_id']), 'R', 'C_set', p))}
    R['certified_R'] = cnt
    d6 = [cnt['CaliberGraph-R@R'] * x - cnt['Fuzz-R@R'] * y for x, y in
          zip(boots['CaliberGraph-R@R']['meaningful'], boots['Fuzz-R@R']['meaningful'])]
    obs6 = cnt['CaliberGraph-R@R'] * shares(samples['CaliberGraph-R@R'])['meaningful'] - \
        cnt['Fuzz-R@R'] * shares(samples['Fuzz-R@R'])['meaningful']
    R['h6_cluster'] = dict(diff=obs6, ci=ci(d6), p_one_sided=sum(1 for x in d6 if x <= 0) / len(d6))
    d7 = [x - y for x, y in zip(boots['CaliberGraph@L1f']['implausible'], boots['CaliberGraph-R@R']['implausible'])]
    R['h7_cluster'] = dict(ci=ci(d7), p_one_sided=sum(1 for x in d7 if x <= 0) / len(d7))
    M['hSixClusterCI'] = ('[%.0f, %.0f]' % tuple(R['h6_cluster']['ci'])).replace('-', '$-$')
    M['hSixClusterP'] = '%.3f' % R['h6_cluster']['p_one_sided']
    M['hSevenClusterP'] = ('< 10^{-4}' if R['h7_cluster']['p_one_sided'] == 0 else '%.4f' % R['h7_cluster']['p_one_sided'])
    for k, nm in (('CaliberGraph-R@R', 'CGR'), ('Fuzz-R@R', 'FZR'), ('CaliberGraph@L1f', 'CG')):
        lo, hi = R['attribution_cluster'][k]['meaningful'][1]
        M[f'p{nm}MeaningfulClusterCI'] = f'[{100 * lo:.0f}, {100 * hi:.0f}]'
        lo, hi = R['attribution_cluster'][k]['implausible'][1]
        M[f'p{nm}ImplClusterCI'] = f'[{100 * lo:.0f}, {100 * hi:.0f}]'

    # ---- 4. empty result vs one all-NULL row in the sampled A_R witnesses
    blind = {b['idx']: b for b in json.load(open(P('results/audit/test_r_blind.json')))}

    def empty_vs_null(b):
        g, q = b.get('gold_rows'), b.get('pred_rows')

        def nullish(x):  # one row whose values are all NULL or zero (aggregates over an empty input)
            return isinstance(x, list) and len(x) == 1 and all(v is None or v == 0 for v in x[0])
        return (g == [] and nullish(q)) or (q == [] and nullish(g))
    R['empty_vs_null'] = {}
    for k in ('CaliberGraph-R@R', 'Fuzz-R@R'):
        its = [(pid, v) for pid, v, i in vr[k] if empty_vs_null(blind[i])]
        R['empty_vs_null'][k] = dict(n=len(its), verdicts=dict(Counter(v for _, v in its)))
    M['nEmptyNullCGR'] = str(R['empty_vs_null']['CaliberGraph-R@R']['n'])
    M['nEmptyNullFZR'] = str(R['empty_vs_null']['Fuzz-R@R']['n'])

    # ---- 5. by schema group
    R['by_group'] = {}
    for grp, sel in (('held_out', lambda p: p['db_id'] in HELD_OUT), ('other', lambda p: p['db_id'] not in HELD_OUT)):
        ps = [p for p in exc if sel(p)]
        d = dict(n_exc=len(ps))
        d['CaliberGraph_L1f'] = sum(1 for p in ps if is_cert(exp['CaliberGraph'].get(p['pair_id']), 'L1f', 'C_set', p))
        for k in ('CaliberGraph-R', 'Fuzz-R'):
            d[k + '_R'] = sum(1 for p in ps if is_cert(exp[k].get(p['pair_id']), 'R', 'C_set', p))
        pm = {p['pair_id']: p for p in allp}
        for k, items in samples.items():
            its = [it for it in items if sel(pm[it[0]])]
            if its:
                d['impl_' + k] = [sum(v == 'implausible_data' for _, v, _ in its), len(its)]
        R['by_group'][grp] = d
    g = R['by_group']
    for grp, nm in (('held_out', 'Held'), ('other', 'Other')):
        M[f'rateCGR{nm}'] = f"{100 * g[grp]['CaliberGraph-R_R'] / g[grp]['n_exc']:.1f}"
        M[f'rateFZR{nm}'] = f"{100 * g[grp]['Fuzz-R_R'] / g[grp]['n_exc']:.1f}"
        k, n = g[grp]['impl_CaliberGraph-R@R']
        M[f'implCGR{nm}'] = f'{k} of {n}'
        k, n = g[grp]['impl_CaliberGraph@L1f']
        M[f'implCG{nm}'] = f'{k} of {n}'

    # ---- 6. stand-alone audit cost per system (CaliberGraph-R, EX-correct test pairs)
    byid = {r['pair_id']: r for r in res['CaliberGraph-R']}
    rep = {}
    for p in exc:
        if p['pair_id'] in byid:
            rep[(p['qid'], p['gold'].strip(), p['pred'].strip())] = byid[p['pair_id']]
    cost = defaultdict(float)
    seen = defaultdict(set)
    for p in exc:
        sysname = p['pair_id'].split(':', 1)[0]
        kk = (p['qid'], p['gold'].strip(), p['pred'].strip())
        if kk in rep and kk not in seen[sysname]:
            seen[sysname].add(kk)
            cost[sysname] += rep[kk].get('wall_s') or 0.0
    hours = sorted(v / 3600 for v in cost.values())
    R['standalone_cost_hours'] = dict(per_system={k: v / 3600 for k, v in cost.items()},
                                      mean=sum(hours) / len(hours), min=hours[0], max=hours[-1])
    M['costSysMean'] = f"{R['standalone_cost_hours']['mean']:.2f}"
    M['costSysMin'] = f"{hours[0]:.2f}"
    M['costSysMax'] = f"{hours[-1]:.2f}"

    # ---- 7. sensitivity of A_R to the categorical thresholds
    from cgx.certify import SchemaInfo
    from run_method import load_profile_r
    ddl = json.load(open(P('data', 'raw', 'bird_schema_ddl.json')))
    schemas = {db: SchemaInfo(s) for db, s in ddl.items()}
    prof, _ = load_profile_r(schemas)
    pairs_by = {p['pair_id']: p for p in allp}

    def recat(text_n, text_frac, num_n):
        for pr in prof.values():
            pr.categorical = set()
            for key, info in pr.col.items():
                if key not in pr.dom:
                    continue
                nd = info.get('n_distinct', 0)
                nn = info.get('n', 0) - info.get('n_null', 0)
                numeric = info.get('num_share', 0) > 0.5
                if (numeric and nd <= num_n) or (not numeric and (nd <= text_n or nd <= text_frac * nn)):
                    pr.categorical.add(key)

    def admissible(k):
        n = 0
        for r in res[k]:
            p = pairs_by.get(r['pair_id'])
            if p is None or not is_cert(r, 'L1f', 'C_set', p):
                continue
            s = schemas[p['db_id']]
            w = {}
            for t, rr in (r.get('witness') or {}).items():
                tt = s.table(t)
                if tt is not None:
                    w[tt['name']] = rr
            try:
                n += not prof[p['db_id']].violations(w)
            except Exception:  # noqa: BLE001
                errors[k] = errors.get(k, 0) + 1
        return n
    errors = {}
    R['threshold_sensitivity'] = {}
    for name, th in (('frozen', (100, 0.01, 20)), ('stricter', (200, 0.02, 40)), ('looser', (50, 0.005, 10))):
        recat(*th)
        R['threshold_sensitivity'][name] = dict(thresholds=th, **{k: admissible(k) for k in res})
        R['threshold_sensitivity'][name]['check_errors'] = dict(errors)
        errors.clear()
        print(name, R['threshold_sensitivity'][name], flush=True)
    ts = R['threshold_sensitivity']
    for nm, k in (('CGR', 'CaliberGraph-R'), ('FZR', 'Fuzz-R'), ('CG', 'CaliberGraph')):
        for v in ('frozen', 'stricter', 'looser'):
            M[f'thr{nm}{v.capitalize()}'] = f"{ts[v][k]:,}".replace(',', '{,}')

    # ---- 8. flags on the released benchmark-issue list: witnesses without the named entity, and
    #         differences that vanish under rounding or letter case (both disappear under C_len or case folding)
    blinds = {}
    for f in ('test_v4_blind.json', 'test_r_blind.json'):
        for b in json.load(open(P('results/audit', f))):
            blinds.setdefault(b['pair_id'], b)

    def norm_rows(rows, case=False):
        out = []
        for r in rows or []:
            out.append(tuple((float('%.9g' % v) if isinstance(v, float) else (v.lower() if case and isinstance(v, str) else v))
                             for v in r))
        return sorted(out, key=repr)
    issues = json.load(open(P('results/audit/benchmark_issues.json')))
    flags = []
    for x in issues:
        b = blinds.get(x['example_pair'])
        f = dict(question_id=x['question_id'], kind=x['kind'], entity_missing=False, rounding_or_case_only=False)
        if b:
            f['entity_missing'] = empty_vs_null(b)
            f['rounding_or_case_only'] = (norm_rows(b['gold_rows']) == norm_rows(b['pred_rows'])) or \
                (norm_rows(b['gold_rows'], True) == norm_rows(b['pred_rows'], True))
        flags.append(f)
    json.dump(flags, open(P('results/audit/benchmark_issues_flags.json'), 'w'), indent=1)
    fl = Counter((f['kind'], f['entity_missing'], f['rounding_or_case_only']) for f in flags)
    R['issue_flags'] = {str(k): v for k, v in fl.items()}
    robust = [f for f in flags if not f['entity_missing'] and not f['rounding_or_case_only']]
    M['nIssuesRobust'] = str(len(robust))
    M['nIssuesRobustGold'] = str(sum(f['kind'] == 'gold_wrong' for f in robust))
    M['nIssuesRobustAmb'] = str(sum(f['kind'] == 'ambiguous' for f in robust))
    M['nIssuesFragile'] = str(len(flags) - len(robust))

    json.dump(R, open(a.out, 'w'), indent=1, default=str)
    with open(a.tex, 'w') as f:
        f.write('% generated by src_r/icde_posthoc.py -- do not edit by hand\n')
        for k, v in sorted(M.items()):
            f.write('\\newcommand{\\%s}{%s}\n' % (k, v))
    print(json.dumps({k: v for k, v in R.items() if k not in ('per_system',)}, indent=1, default=str)[:6000])


if __name__ == '__main__':
    main()
