"""Post hoc analyses requested by the pre-submission review for Information Systems (amendment E20).
Not pre-registered; every output is labelled post hoc in the paper.
  1. rerun variance of CaliberGraph (A_1f) and CaliberGraph-R (A_R) on 500 subsample pairs;
  2. SpotIt with a 60 s budget vs 5 s on 150 subsample pairs;
  3. entity-missing (empty vs. one all-NULL/zero row) A_R witnesses counted as not meaningful: H6, error estimates;
  4. leave-one-class-out and cumulative profile ablation on the first-stage witnesses (A_1f, distinct pairs);
  5. duplication-weighted estimates of meaningful witnesses;
  6. Wilson intervals for the attribution shares (BIRD samples) and the Spider attribution shares;
  7. round-3 outcomes without annotator A.
Usage: python src_s3/rev_posthoc.py   -> results/posthoc_rev/rev_posthoc.json and numbers_rev.tex in each paper dir
"""
import json
import math
import os
import random
import sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src_r'))
from score import load_pairs, expand, is_cert, qcols  # noqa: E402
from icde_posthoc import final_verdicts, shares, cluster_boot, ci, MEANINGFUL, ERR  # noqa: E402

P = lambda *a: os.path.join(ROOT, *a)  # noqa: E731
OUT = P('results', 'posthoc_rev')
B = 10000


def jl(p):
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else None


def wilson(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [max(0.0, c - h), min(1.0, c + h)]


def empty_vs_null(b):
    g, q = b.get('gold_rows'), b.get('pred_rows')

    def nullish(x):
        return isinstance(x, list) and len(x) == 1 and all(v is None or v == 0 for v in x[0])
    return (g == [] and nullish(q)) or (q == [] and nullish(g))


def main():
    R, M = {}, {}
    rng = random.Random(20261020)
    allp = [p for p in load_pairs('test') if p['source'] != 'parseval_model']
    exc = [p for p in allp if p['ex'] == 'correct']
    pm = {p['pair_id']: p for p in allp}
    v4 = final_verdicts(P('results/audit/test_v4_key.json'), P('results/audit/test_v4_ann_a.json'),
                        P('results/audit/test_v4_ann_b.json'), P('results/audit/test_v4_ann_c.json'))
    vr = final_verdicts(P('results/audit/test_r_key.json'), P('results/audit/test_r_ann_a.json'),
                        P('results/audit/test_r_ann_b.json'), P('results/audit/test_r_ann_c.json'))
    samples = {k: v for k, v in list(v4.items()) + list(vr.items()) if not k.startswith('calib:')}
    R['sample_keys'] = {k: len(v) for k, v in samples.items()}
    files = {'CaliberGraph-R': P('results/test_r/cgx_r_exc.jsonl'), 'Fuzz-R': P('results/test_r/fuzz_r_exc.jsonl'),
             'CaliberGraph': P('results/test/cgx_exc.jsonl'), 'Fuzz': P('results/test/fuzz_exc_corrected.jsonl'),
             'ParSEval-L1': P('results/test/parseval_l1_exc.jsonl')}
    raw = {k: jl(f) for k, f in files.items()}
    exp = {k: expand(v, exc) for k, v in raw.items()}
    cnt = {'CaliberGraph-R@R': sum(1 for p in exc if is_cert(exp['CaliberGraph-R'].get(p['pair_id']), 'R', 'C_set', p)),
           'Fuzz-R@R': sum(1 for p in exc if is_cert(exp['Fuzz-R'].get(p['pair_id']), 'R', 'C_set', p))}

    # ---- 3. entity-missing witnesses counted as not meaningful
    blind = {b['idx']: b for b in json.load(open(P('results/audit/test_r_blind.json')))}

    def strict(items):
        return [(pid, 'entity_missing' if empty_vs_null(blind[i]) else v, i) for pid, v, i in items]
    st = {k: strict(samples[k]) for k in ('CaliberGraph-R@R', 'Fuzz-R@R')}
    em = {}
    boots = {}
    for k in st:
        sh = shares(st[k])
        bt, _ = cluster_boot(st[k], B, rng)
        boots[k] = bt
        em[k] = dict(n_entity_missing=sum(1 for _, v, _ in st[k] if v == 'entity_missing'),
                     meaningful=sh['meaningful'], meaningful_ci=ci(bt['meaningful']), error=sh['error'],
                     est_meaningful=cnt[k] * sh['meaningful'], est_error=cnt[k] * sh['error'])
    d6 = [cnt['CaliberGraph-R@R'] * x - cnt['Fuzz-R@R'] * y for x, y in
          zip(boots['CaliberGraph-R@R']['meaningful'], boots['Fuzz-R@R']['meaningful'])]
    obs = em['CaliberGraph-R@R']['est_meaningful'] - em['Fuzz-R@R']['est_meaningful']
    em['H6_strict'] = dict(diff=obs, ci=ci(d6), p_one_sided=sum(1 for x in d6 if x <= 0) / len(d6))
    R['entity_missing'] = em
    M['emCGRMean'] = f"{100 * em['CaliberGraph-R@R']['meaningful']:.0f}"
    M['emFZRMean'] = f"{100 * em['Fuzz-R@R']['meaningful']:.0f}"
    M['emCGREst'] = f"{em['CaliberGraph-R@R']['est_meaningful']:.0f}"
    M['emFZREst'] = f"{em['Fuzz-R@R']['est_meaningful']:.0f}"
    M['emHSixDiff'] = f"{obs:.0f}".replace('-', '\\ensuremath{-}')
    M['emHSixCI'] = ('[%.0f, %.0f]' % tuple(em['H6_strict']['ci'])).replace('-', '\\ensuremath{-}')
    M['emHSixP'] = f"{em['H6_strict']['p_one_sided']:.2f}"
    M['emCGRErrEst'] = f"{em['CaliberGraph-R@R']['est_error']:.0f}"
    M['emFZRErrEst'] = f"{em['Fuzz-R@R']['est_error']:.0f}"

    # ---- 4. leave-one-class-out / cumulative profile ablation on first-stage witnesses (distinct pairs)
    sys.path.insert(0, P('src_r'))
    from cgx.certify import SchemaInfo  # noqa: E402
    from run_method import load_profile_r  # noqa: E402
    from profile_stats import vclass, CLASSES  # noqa: E402
    ddl = json.load(open(P('data', 'raw', 'bird_schema_ddl.json')))
    schemas = {db: SchemaInfo(s) for db, s in ddl.items()}
    prof, _ = load_profile_r(schemas)
    abl = {}
    for name in ('CaliberGraph', 'Fuzz', 'ParSEval-L1'):
        sets = []
        for r in raw[name]:
            c = r.get('cert') or {}
            if not (r.get('found') and r.get('witness') and c.get('L1f') and c.get('differ', {}).get('C_set')):
                continue
            p = pm.get(r['pair_id'])
            if p is None:
                continue
            s = schemas[p['db_id']]
            w = {}
            for t, rows in r['witness'].items():
                tt = s.table(t)
                if tt is not None:
                    w[tt['name']] = rows
            try:
                sets.append({vclass(v) for v in prof[p['db_id']].violations(w)})
            except Exception:  # noqa: BLE001
                continue
        n = len(sets)
        loo = {c: sum(1 for x in sets if x <= {c}) for c in CLASSES}
        loo['other_classes_seen'] = sorted({c for x in sets for c in x} - set(CLASSES))
        cum, active = [], []
        for c in CLASSES:
            active.append(c)
            cum.append([c, sum(1 for x in sets if not (x & set(active)))])
        abl[name] = dict(n=n, pass_all=sum(1 for x in sets if not x), leave_one_out=loo, cumulative=cum)
        print('ablation', name, abl[name], flush=True)
    R['profile_ablation'] = abl
    a = abl['CaliberGraph']
    M['ablN'] = f"{a['n']:,}"
    M['ablLooNull'], M['ablLooDomain'], M['ablLooValuedep'] = (str(a['leave_one_out'][c]) for c in ('null', 'domain', 'valuedep'))
    M['ablLooMax'] = str(max(v for k, v in a['leave_one_out'].items() if k in CLASSES))
    M['ablCumDomain'] = f"{dict(a['cumulative'])['domain']:,}"
    M['ablCumNull'] = f"{dict(a['cumulative'])['null']:,}"

    # ---- 5. duplication-weighted estimates of meaningful witnesses
    rep = defaultdict(int)
    for p in exc:
        rep[(p['qid'], p['gold'].strip(), p['pred'].strip())] += 1
    mult = lambda pid: rep[(pm[pid]['qid'], pm[pid]['gold'].strip(), pm[pid]['pred'].strip())]  # noqa: E731
    dw = {}
    for k, items in samples.items():
        w = [mult(pid) for pid, _, _ in items]
        mean_w = sum(wi for wi, (_, v, _) in zip(w, items) if v in MEANINGFUL) / sum(w)
        err_w = sum(wi for wi, (_, v, _) in zip(w, items) if v in ERR) / sum(w)
        dw[k] = dict(meaningful=shares(items)['meaningful'], meaningful_w=mean_w, error=shares(items)['error'], error_w=err_w,
                     mean_multiplicity=sum(w) / len(w))
    for k in cnt:
        dw[k]['est_meaningful'] = cnt[k] * dw[k]['meaningful']
        dw[k]['est_meaningful_w'] = cnt[k] * dw[k]['meaningful_w']
    R['dup_weighted'] = dw
    M['dwCGREst'] = f"{dw['CaliberGraph-R@R']['est_meaningful_w']:.0f}"
    M['dwFZREst'] = f"{dw['Fuzz-R@R']['est_meaningful_w']:.0f}"
    M['dwMaxShift'] = f"{max(abs(v['meaningful_w'] - v['meaningful']) for v in dw.values()) * 100:.0f}"

    # ---- 6. Wilson intervals
    wl = {}
    for k, items in samples.items():
        n = len(items)
        ki = sum(1 for _, v, _ in items if v == 'implausible_data')
        wl[k] = dict(n=n, implausible=ki, ci=wilson(ki, n))
    R['wilson_bird'] = wl
    sd = json.load(open(P('results/stage3/s3d/s3d_summary.json')))
    R['spider_attribution_raw'] = sd.get('attribution')
    sp = {}
    att = sd['attribution']
    for nm, key in (('CG', 'CaliberGraph'), ('CGR', 'CaliberGraph-R'), ('FZR', 'Fuzz-R')):
        k, n = att[key]['implausible'], att[key]['n']
        sp[nm] = dict(k=k, n=n, ci=wilson(k, n))
        lo, hi = sp[nm]['ci']
        M[f'spImp{nm}CI'] = f'[{100 * lo:.0f}, {100 * hi:.0f}]'
    R['wilson_spider'] = sp

    # ---- 7. round 3 without annotator A
    h3 = json.load(open(P('results/stage3/s3a_human_r3.json')))
    s = h3['sensitivity_without_A']
    R['round3_without_A'] = s
    M['rtBCkappaFive'] = f"{s['kappa5_B_C']:.2f}"
    M['rtBCcons'] = str(s['n_consensus'])
    M['rtBCkappaAI'] = f"{s['kappa2_consensus_vs_ai']:.2f}"
    M['rtBCImpOne'], M['rtBCConsOne'] = s['implausible_stage1']
    M['rtBCImpTwo'], M['rtBCConsTwo'] = s['implausible_stage2']
    M['rtBCErrTwo'], M['rtBCNTwo'] = s['pred_error_stage2_consensus']
    M['rtBCErrAITwo'] = s['pred_error_stage2_ai_same_items'][0]

    # ---- 1. rerun variance
    ids = set(json.load(open(P(OUT, 'ids_rerun500.json')))['pair_ids'])
    rv = {}
    for name, f_old, f_new, tier in (('CaliberGraph', 'results/test/cgx_exc.jsonl', 'cgx_rerun.jsonl', 'L1f'),
                                     ('CaliberGraph-R', 'results/test_r/cgx_r_exc.jsonl', 'cgx_r_rerun.jsonl', 'R')):
        new = jl(P(OUT, f_new))
        if not new:
            continue
        old = {r['pair_id']: r for r in jl(P(f_old)) if r['pair_id'] in ids}
        newd = {r['pair_id']: r for r in new}
        common = sorted(set(old) & set(newd))
        a_ = {i: is_cert(old[i], tier, 'C_set', pm[i]) for i in common}
        b_ = {i: is_cert(newd[i], tier, 'C_set', pm[i]) for i in common}
        rv[name] = dict(n=len(common), tier=tier, stored=sum(a_.values()), rerun=sum(b_.values()),
                        lost=sum(1 for i in common if a_[i] and not b_[i]), gained=sum(1 for i in common if b_[i] and not a_[i]))
    R['rerun_variance'] = rv
    if 'CaliberGraph' in rv:
        M['rvN'] = str(rv['CaliberGraph']['n'])
        for nm, k in (('CG', 'CaliberGraph'), ('CGR', 'CaliberGraph-R')):
            if k in rv:
                M[f'rv{nm}Stored'], M[f'rv{nm}Rerun'] = str(rv[k]['stored']), str(rv[k]['rerun'])
                M[f'rv{nm}Lost'], M[f'rv{nm}Gained'] = str(rv[k]['lost']), str(rv[k]['gained'])

    # ---- 2. SpotIt 60 s vs 5 s
    s60 = jl(P(OUT, 'spotit60.jsonl'))
    if s60:
        s5 = {r['pair_id']: r for r in jl(P('results/stage3/spotit/spotit_test_exc.jsonl'))}
        d60 = {r['pair_id']: r for r in s60}
        common = sorted(set(d60) & set(s5))
        out = dict(n=len(common))
        for lab, d in (('5s', s5), ('60s', d60)):
            out[lab] = dict(claims=sum(1 for i in common if d[i].get('spotit_verdict') == 'incorrect'),
                            L0=sum(1 for i in common if is_cert(d[i], 'L0', 'C_set', pm[i])),
                            L1f=sum(1 for i in common if is_cert(d[i], 'L1f', 'C_set', pm[i])),
                            killed=sum(1 for i in common if d[i].get('killed')))
        cg = {r['pair_id']: r for r in raw['CaliberGraph']}
        out['CaliberGraph'] = dict(L0=sum(1 for i in common if is_cert(cg.get(i), 'L0', 'C_set', pm[i])),
                                   L1f=sum(1 for i in common if is_cert(cg.get(i), 'L1f', 'C_set', pm[i])))
        R['spotit_budget'] = out
        M['sbN'] = str(out['n'])
        for lab, nm in (('5s', 'Five'), ('60s', 'Sixty')):
            M[f'sb{nm}Claims'], M[f'sb{nm}Lzero'], M[f'sb{nm}Lonef'] = (str(out[lab][x]) for x in ('claims', 'L0', 'L1f'))
            M[f'sb{nm}Killed'] = str(out[lab]['killed'])
        M['sbCGLzero'], M['sbCGLonef'] = str(out['CaliberGraph']['L0']), str(out['CaliberGraph']['L1f'])

    os.makedirs(OUT, exist_ok=True)
    json.dump(R, open(P(OUT, 'rev_posthoc.json'), 'w'), indent=1, default=str)
    lines = ['% generated by src_s3/rev_posthoc.py -- post hoc analyses (amendment E20)']
    lines += [f'\\newcommand{{\\{k}}}{{{v}\\xspace}}' for k, v in M.items()]
    for d in ('paper_is', 'paper_pvldb'):
        if os.path.isdir(P(d)):
            open(P(d, 'numbers_rev.tex'), 'w').write('\n'.join(lines) + '\n')
    print(json.dumps({k: R[k] for k in R if k not in ('spider_attribution_raw',)}, indent=1, default=str)[:4000])


if __name__ == '__main__':
    main()
