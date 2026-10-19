"""Paper macros for Stage 3 (docs/en/17, 17a, 17b) -> paper_pvldb/numbers_s3.tex.
Every number in the Stage-3 text of the paper comes from this file.
Usage: python src_s3/make_numbers_s3.py"""
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
R = os.path.join(ROOT, 'results', 'stage3')
M = {}


def f2(x):
    t = f'{x:.2f}'
    return '0.00' if t == '-0.00' else t.replace('-', '\\ensuremath{-}')


def pct(a, b):
    return f'{100 * a / b:.0f}'


a = json.load(open(os.path.join(R, 's3a_human.json')))
M['hvN'] = a['n_items']
M['hvAgreeHH'] = a['M_A1_h1_vs_h2']['agree5']
M['hvKappaHH'] = f2(a['M_A1_h1_vs_h2']['kappa5'])
M['hvKappaHHlo'], M['hvKappaHHhi'] = (f2(x) for x in a['M_A1_h1_vs_h2']['kappa5_ci'])
M['hvKappaHHbin'] = f2(a['M_A1_h1_vs_h2']['kappa2'])
k = sorted([a['M_A2_h1_vs_ai']['kappa5'], a['M_A2_h2_vs_ai']['kappa5']])
M['hvKappaHAmin'], M['hvKappaHAmax'] = f2(k[0]), f2(k[1])
k = sorted([a['M_A2_h1_vs_ai']['kappa2'], a['M_A2_h2_vs_ai']['kappa2']])
M['hvKappaHAbinMin'], M['hvKappaHAbinMax'] = f2(k[0]), f2(k[1])
s = a['M_A3_implausible_by_stage']
M['hvImpConsOne'], M['hvConsOne'] = s['consensus']['stage1']['implausible'], s['consensus']['stage1']['n']
M['hvImpConsTwo'], M['hvConsTwo'] = s['consensus']['stage2']['implausible'], s['consensus']['stage2']['n']
M['hvImpAIOne'], M['hvImpAITwo'] = s['ai']['stage1']['implausible'], s['ai']['stage2']['implausible']
M['hvImpHOne'] = s['h1']['stage1']['implausible']
M['hvImpHTwo'] = s['h2']['stage1']['implausible']
lab = a['labels']
M['hvHImpOne'], M['hvHImpTwo'] = lab['h1'].get('implausible_data', 0), lab['h2'].get('implausible_data', 0)

a2 = json.load(open(os.path.join(R, 's3a_human_r2.json')))
M['hvTwoKappaBin'] = f2(a2['M_A1_h1_vs_h2']['kappa2'])
M['hvTwoKappaBinLo'], M['hvTwoKappaBinHi'] = (f2(x) for x in a2['M_A1_h1_vs_h2']['kappa2_ci'])
M['hvTwoKappa'] = f2(a2['M_A1_h1_vs_h2']['kappa5'])
M['hvTwoAgree'] = a2['M_A1_h1_vs_h2']['agree5']
k = sorted([a2['M_A2_h1_vs_ai']['kappa2'], a2['M_A2_h2_vs_ai']['kappa2']])
M['hvTwoKappaAIbinMin'], M['hvTwoKappaAIbinMax'] = f2(k[0]), f2(k[1])
k5 = sorted([a2['M_A2_h1_vs_ai']['kappa5'], a2['M_A2_h2_vs_ai']['kappa5']])
M['hvTwoKappaHAfiveMin'], M['hvTwoKappaHAfiveMax'] = f2(k5[0]), f2(k5[1])
s2 = a2['M_A3_implausible_by_stage']
M['hvTwoImpConsOne'], M['hvTwoConsOne'] = s2['consensus']['stage1']['implausible'], s2['consensus']['stage1']['n']
M['hvTwoImpConsTwo'], M['hvTwoConsTwo'] = s2['consensus']['stage2']['implausible'], s2['consensus']['stage2']['n']
M['hvTwoP'] = f'{s2["consensus"]["fisher_one_sided_stage1_gt_stage2"]:.4f}'
M['hvTwoImpHOne'], M['hvTwoImpHTwo'] = a2['labels']['h1'].get('implausible_data', 0), a2['labels']['h2'].get('implausible_data', 0)
M['hvTwoImpAI'] = a2['labels']['ai'].get('implausible_data', 0)

b = json.load(open(os.path.join(R, 's3b_crossmodel.json')))
M['cmN'] = b['n_annotated']
M['cmKappa'] = f2(b['M_B1_sonnet_vs_opus']['kappa5'])
M['cmKappaBin'] = f2(b['M_B1_sonnet_vs_opus']['kappa2'])
M['cmKappaBinLo'], M['cmKappaBinHi'] = (f2(x) for x in b['M_B1_sonnet_vs_opus']['kappa2_ci'])
M['cmImpOne'], M['cmImpTwo'] = b['M_B2_by_stage']['stage1']['sonnet_imp'], b['M_B2_by_stage']['stage2']['sonnet_imp']
M['cmNOne'], M['cmNTwo'] = b['M_B2_by_stage']['stage1']['n'], b['M_B2_by_stage']['stage2']['n']
k = sorted([b['M_B3_on_60']['sonnet_vs_h1']['kappa2'], b['M_B3_on_60']['sonnet_vs_h2']['kappa2']])
M['cmKappaHbinMin'], M['cmKappaHbinMax'] = f2(k[0]), f2(k[1])

c = json.load(open(os.path.join(R, 's3c_arcwise.json')))
z = c['sizes']
M['arcN'], M['arcO'], M['arcIss'] = z['arcwise_questions'], z['O'], z['issues_in_O']
M['arcG'], M['arcA'], M['arcNN'] = z['G'], z['A'], z['N']
h1, h2 = c['confirmatory_unadjusted']['H-C1'], c['confirmatory_unadjusted']['H-C2']
M['arcGk'], M['arcNk'] = h1['G']['k'], h1['N']['k']
M['arcGpct'], M['arcNpct'] = pct(h1['G']['k'], h1['G']['n']), pct(h1['N']['k'], h1['N']['n'])
M['arcPone'] = f2(h1['p_one_sided'])
M['arcAk'], M['arcANk'] = h2['A']['k'], h2['N']['k']
M['arcApct'], M['arcANpct'] = pct(h2['A']['k'], h2['A']['n']), pct(h2['N']['k'], h2['N']['n'])
M['arcPtwo'] = f2(h2['p_one_sided'])
d = c['descriptive']['concordance']
M['arcGneither'], M['arcAneither'] = d['G']['neither'], d['A']['neither']
sec = c['secondary_descriptive_sql_text_diff_only']['concordance']
M['arcGtext'], M['arcGtextPct'] = sec['G']['sql_corrected'], pct(sec['G']['sql_corrected'], sec['G']['n'])
M['arcNtextPct'] = pct(sec['N']['sql_corrected'], sec['N']['n'])
M['arcGuntouched'], M['arcAuntouched'] = sec['G']['neither'], sec['A']['neither']  # no text change at all

x = json.load(open(os.path.join(R, 'x1_repair.json')))
o1 = x['outcome_by_stage']['1']
n1 = sum(o1.values())
M['xN'] = n1
M['xVan'], M['xSurv'], M['xUnrep'] = o1.get('vanishes', 0), o1.get('survives', 0), o1.get('unrepairable', 0)
M['xVanPct'] = pct(M['xVan'], n1)
imp = x['outcome_by_stage_ai']['1|implausible_data']
M['xImpN'] = sum(imp.values())
M['xImpVan'] = imp.get('vanishes', 0)
M['xImpVanPct'] = pct(imp.get('vanishes', 0), M['xImpN'])
oth = {}
for kk, v in x['outcome_by_stage_ai'].items():
    if kk.startswith('1|') and kk != '1|implausible_data':
        for o, n in v.items():
            oth[o] = oth.get(o, 0) + n
M['xOthN'] = sum(oth.values())
M['xOthSurv'] = oth.get('survives', 0)
M['xOthSurvPct'] = pct(oth.get('survives', 0), M['xOthN'])
M['xOthVanPct'] = pct(oth.get('vanishes', 0), M['xOthN'])
pa = x['pairAR_by_stage']['1']
M['xPairAR'] = pa.get('True', 0)
_van = [r for r in map(json.loads, open(os.path.join(R, 'x1_repair_items.jsonl'))) if r['stage'] == 1 and r['outcome'] == 'vanishes']
M['xVanPairAR'], M['xVanPairARpct'] = sum(bool(r['pair_AR_any']) for r in _van), pct(sum(bool(r['pair_AR_any']) for r in _van), len(_van))
M['xPairARpct'] = pct(pa.get('True', 0), sum(pa.values()))

# round-2 consensus-implausible first-stage witnesses vs. repair outcome
import sys
sys.path.insert(0, os.path.join(ROOT, 'src_r'))
from human_validation import parse  # noqa: E402
D2 = os.path.join(ROOT, 'results', 'audit', 'human_validation_r2')
k2 = {k['no']: k for k in json.load(open(os.path.join(D2, 'key_DO_NOT_OPEN_BEFORE_ANNOTATING.json')))}
r1, r2 = parse(os.path.join(D2, 'sheet_r2_annotator1.md')), parse(os.path.join(D2, 'sheet_r2_annotator2.md'))
xi = {(r['pair_id'], r['source']): r for r in map(json.loads, open(os.path.join(R, 'x1_repair_items.jsonl')))}
rep = van = 0
for i, kk in k2.items():
    r = xi[(kk['pair_id'], kk['source'])]
    if r['stage'] == 1 and r1[i] == r2[i] == 'implausible_data' and r['outcome'] in ('vanishes', 'survives'):
        rep += 1
        van += r['outcome'] == 'vanishes'
M['xHumRep'], M['xHumVan'] = rep, van

d = json.load(open(os.path.join(R, 's3d', 's3d_summary.json')))
M['spN'], M['spNexi'] = f"{d['n_exc']:,}", f"{d['n_exi']:,}"
M['spCG'], M['spCGR'] = d['counts']['cg']['L1f'], d['counts']['cg']['R']
M['spFZ'], M['spFZR'] = d['counts']['fuzz']['L1f'], d['counts']['fuzz']['R']
M['spCGRq'], M['spFZRq'] = d['counts']['cg']['Rq'], d['counts']['fuzz']['Rq']
M['spRCG'], M['spRFZ'] = d['counts']['cgr']['R'], d['counts']['fuzzr']['R']
h = d['H_S1']
M['spSOneA'], M['spSOneB'] = h['cgr_only'], h['fuzzr_only']
M['spSOneLo'], M['spSOneHi'] = (str(x).replace('-', '\\textminus') for x in h['ci95_cluster'])
M['spSOneP'] = f2(h['p_one_sided'])
M['spRecCGR'], M['spRecFZR'] = f"{100 * d['recall']['cgr']['R']:.1f}", f"{100 * d['recall']['fuzzr']['R']:.1f}"
at = d['attribution']
M['spImpCG'], M['spImpCGR'], M['spImpFZR'] = at['CaliberGraph']['implausible'], at['CaliberGraph-R']['implausible'], at['Fuzz-R']['implausible']
M['spNCG'], M['spNCGR'], M['spNFZR'] = at['CaliberGraph']['n'], at['CaliberGraph-R']['n'], at['Fuzz-R']['n']
M['spSTwoP'] = f2(d['H_S2']['p_one_sided'])
M['spEstCGR'], M['spEstFZR'] = f"{d['H_S3']['est_cgr']:.0f}", f"{d['H_S3']['est_fuzzr']:.0f}"
M['spSThreeLo'], M['spSThreeHi'] = (f"{x:.0f}".replace('-', '\\textminus') for x in d['H_S3']['ci95'])
M['spKappa'] = f2(d['attribution_agreement']['kappa'])
pc = d['profile_compare']
M['spCatShare'], M['bdCatShare'] = pct(pc['Spider']['categorical_cols'], pc['Spider']['columns']), pct(pc['BIRD']['categorical_cols'], pc['BIRD']['columns'])
M['spUcc'], M['bdUcc'] = pc['Spider']['ucc'], pc['BIRD']['ucc']
M['spTables'], M['spRows'] = pc['Spider']['tables'], f"{pc['Spider']['rows'] / 1000:.0f}"

e = json.load(open(os.path.join(R, 's3e', 's3e_summary.json')))
M['mdN'] = f"{e['n_exc']:,}"
M['mdCGR'], M['mdFZR'] = e['H_E1']['cgr'], e['H_E1']['fuzzr']
M['mdA'], M['mdB'] = e['H_E1']['cgr_only'], e['H_E1']['fuzzr_only']
M['mdDiff'] = e['H_E1']['cgr'] - e['H_E1']['fuzzr']
M['mdLo'], M['mdHi'] = e['H_E1']['ci95_cluster']
M['mdImp'], M['mdAttrN'] = e['attribution']['implausible'], e['attribution']['n']
M['mdErr'] = e['attribution']['counts'].get('pred_wrong', 0) + e['attribution']['counts'].get('both_wrong', 0)
# post hoc: error-weighted effect on EX with the human annotators' error rates (pooled rounds, consensus items)
ht = json.load(open(os.path.join(R, 's3a_humanai_table.json')))
import re as _re
_icde = open(os.path.join(ROOT, 'paper_pvldb', 'numbers_icde.tex')).read()
_v = lambda n: float(_re.search(r'\\newcommand\{\\%s\}\{([0-9.]+)' % n, _icde).group(1))  # noqa: E731
for st, tier in ((1, 'Onef'), (2, 'R')):
    err = agreed = 0
    for rnd in ('1', '2'):
        h = ht[f'r{rnd}s{st}']['human']
        err += h.get('pred_wrong', 0) + h.get('both_wrong', 0)
        agreed += sum(v for k, v in h.items() if k != 'disagree')
    M[f'humErrPct{tier}'] = pct(err, agreed)
    M[f'ptsHum{tier}Min'] = f"{_v(f'ptsCount{tier}Min') * err / agreed:.1f}"
    M[f'ptsHum{tier}Max'] = f"{_v(f'ptsCount{tier}Max') * err / agreed:.1f}"
# round 3 (docs/en/17c): three annotators, human majority
h3 = json.load(open(os.path.join(R, 's3a_human_r3.json')))
M['hvThreeN'] = h3['n_items']
M['hvThreeFleissFive'], M['hvThreeFleissBin'] = f2(h3['M_R3_1']['fleiss5']), f2(h3['M_R3_1']['fleiss2'])
M['hvThreeFleissBinLo'], M['hvThreeFleissBinHi'] = (f2(x) for x in h3['M_R3_1']['fleiss2_ci'])
M['hvThreeMaj'], M['hvThreeNoMaj'], M['hvThreeUnan'] = h3['M_R3_2']['with_majority'], h3['M_R3_2']['no_majority'], h3['M_R3_2']['unanimous']
M['hvThreeKappaAIfive'], M['hvThreeKappaAIbin'] = f2(h3['M_R3_3']['kappa5']), f2(h3['M_R3_3']['kappa2'])
M['hvThreeKappaAIbinLo'], M['hvThreeKappaAIbinHi'] = (f2(x) for x in h3['M_R3_3']['kappa2_ci'])
hy = h3['hypotheses']
M['hvThreeImpOne'], M['hvThreeMajOne'] = hy['H-R3-3']['stage1']
M['hvThreeImpTwo'], M['hvThreeMajTwo'] = hy['H-R3-3']['stage2']
M['hvThreePThree'] = f"{hy['H-R3-3']['p_one_sided']:.4f}"
M['hvThreeErrHumTwo'], M['hvThreeErrAITwo'] = hy['H-R3-4']['majority_pred_error'], hy['H-R3-4']['ai_pred_error']
M['hvThreePFour'] = f"{hy['H-R3-4']['p_two_sided']:.4f}"
M['hvThreeKappaBCbin'] = f2(h3['sensitivity_without_A']['kappa2_B_C'])
M['hvThreeImpAI'] = h3['labels']['ai'].get('implausible_data', 0)
M['hvThreeImpA'], M['hvThreeImpB'], M['hvThreeImpC'] = (h3['labels'][w].get('implausible_data', 0) for w in 'ABC')
for st, tier in ((1, 'Onef'), (2, 'R')):
    sh = h3['M_R3_4'][f'stage{st}']
    hm, am = sh['majority']['pred_error'], sh['ai']['pred_error']
    M[f'humThreeErrPct{tier}'] = f"{100 * hm['share']:.0f}"
    M[f'humThreeErrPct{tier}Lo'], M[f'humThreeErrPct{tier}Hi'] = (f"{100 * x:.0f}" for x in hm['ci'])
    M[f'aiThreeErrPct{tier}'] = f"{100 * am['share']:.0f}"
    M[f'aiThreeErrPct{tier}Lo'], M[f'aiThreeErrPct{tier}Hi'] = (f"{100 * x:.0f}" for x in am['ci'])
    for nm, share in (('ptsHumThree', hm['share']), ('ptsAIThree', am['share'])):
        M[f'{nm}{tier}Min'] = f"{_v(f'ptsCount{tier}Min') * share:.1f}"
        M[f'{nm}{tier}Max'] = f"{_v(f'ptsCount{tier}Max') * share:.1f}"
    M[f'ptsHumThree{tier}MinLo'] = f"{_v(f'ptsCount{tier}Min') * hm['ci'][0]:.1f}"
    M[f'ptsHumThree{tier}MaxHi'] = f"{_v(f'ptsCount{tier}Max') * hm['ci'][1]:.1f}"
# SpotIt re-run (docs/en/17d)
sg = json.load(open(os.path.join(R, 'spotit', 's3g_spotit.json')))
rr = sg['counts']['SpotIt (re-run)']
M['srClaims'] = f"{sg['counts']['SpotIt (re-run claims)']:,}"
M['srLzero'], M['srLonef'], M['srRq'], M['srR'] = rr['L0'], rr['L1f'], rr['Rq'], rr['R']
for t in sg['tests']:
    nm = 'srOne' if t['label'] == 'H-SP1' else 'srTwo'
    M[nm + 'Diff'] = f"{t['diff']:+,}"
    M[nm + 'CI'] = f"[{t['ci95'][0]:+,}, {t['ci95'][1]:+,}]"
    M[nm + 'CGonly'], M[nm + 'SIonly'] = f"{t['cg_only']:,}", t['spotit_only']
ag = sg['agreement']
M['srAgreeDev'] = pct(*ag['dev']['agree_over_decided'])
M['srAgreeTest'] = pct(*ag['test']['agree_over_decided'])
M['srRefoundTest'], M['srRelCETest'] = f"{ag['test']['released_ce_found_again'][0]:,}", f"{ag['test']['released_ce_found_again'][1]:,}"
M['srRefoundPct'] = pct(*ag['test']['released_ce_found_again'])
dt = sg['describe']['test']
M['srKilledPct'] = pct(dt['killed'], dt['n'])
M['srErr'] = dt['verdicts'].get('error', 0)
M['srMedCE'] = f"{dt['time_to_ce']['median']:.1f}"
fam = json.load(open(os.path.join(R, 's3f_family.json')))


def pfmt(x):
    return '$<10^{-10}$' if x < 1e-10 else ('$<10^{-4}$' if x < 1e-4 else f'{x:.2f}')


for h, v in fam['holm_adjusted'].items():
    M['holm' + h.replace('H-', '').replace('1', 'One').replace('2', 'Two').replace('3', 'Three')] = pfmt(v)

lines = ['% generated by src_s3/make_numbers_s3.py -- do not edit']
for kk, v in M.items():
    if kk.startswith('_'):
        continue
    lines.append(f'\\newcommand{{\\{kk}}}{{{v}\\xspace}}' if not isinstance(v, str) or not v.startswith('\\') else
                 f'\\newcommand{{\\{kk}}}{{{v}\\xspace}}')
open(os.path.join(ROOT, 'paper_pvldb', 'numbers_s3.tex'), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
