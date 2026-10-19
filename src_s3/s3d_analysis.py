"""S3-D confirmatory and descriptive analysis (docs/en/17, S3-D), Spider dev.

Inputs: results/stage3/s3d/analyze_r.json (frozen src_r/analyze_r.py run in the Spider data root; counts, McNemar,
question-clustered bootstrap), the attribution key and annotation passes in results/stage3/s3d/.
Final attribution label = pass A if A == B, else the adjudication pass C (as on BIRD).
Usage: python src_s3/s3d_analysis.py [adj]   ('adj' writes the adjudication batch for items where A != B)
"""
import glob
import json
import math
import os
import random
import sys
from collections import Counter

from scipy.stats import fisher_exact, binomtest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
D = os.path.join(ROOT, 'results', 'stage3', 's3d')
MEANINGFUL = ('pred_wrong', 'gold_wrong', 'both_wrong', 'ambiguous')
key = {k['idx']: k for k in json.load(open(os.path.join(D, 'spider_attr_key.json')))}
blind = {b['idx']: b for b in json.load(open(os.path.join(D, 'spider_attr_blind.json')))}


def load(pass_):
    out = {}
    for f in sorted(glob.glob(os.path.join(D, f'spider_b*_ann_{pass_}.json'))) + \
            ([os.path.join(D, 'spider_adj_ann_c.json')] if pass_ == 'c' and os.path.exists(os.path.join(D, 'spider_adj_ann_c.json')) else []):
        for x in json.load(open(f)):
            out[x['idx']] = x['verdict']
    return out


A, B = load('a'), load('b')
if len(sys.argv) > 1 and sys.argv[1] == 'adj':
    dis = [blind[i] for i in sorted(key) if A.get(i) != B.get(i)]
    json.dump(dis, open(os.path.join(D, 'spider_adj_blind.json'), 'w'), indent=1, default=str, ensure_ascii=False)
    print(len(A), len(B), 'disagreements:', len(dis))
    sys.exit()
C = load('c')
final = {i: (A[i] if A[i] == B[i] else C[i]) for i in key}
S = json.load(open(os.path.join(D, 'analyze_r.json')))
res = dict(n_exc=S['n_exc'], n_exi=S['n_exi'], counts=S['main'], recall=S['known_positive_recall'])
# H-S1: CG-R vs Fuzz-R at A_R, one-sided exact McNemar; question-clustered bootstrap CI from analyze_r
t = next(x for x in S['tests'] if x['a'] == 'cgr' and x['b'] == 'fuzzr' and x['tier'] == 'R')
res['H_S1'] = dict(cgr=t['count_a'], fuzzr=t['count_b'], cgr_only=t['a_only'], fuzzr_only=t['b_only'], diff=t['diff'],
                   ci95_cluster=t['ci95'],
                   p_one_sided=binomtest(t['a_only'], t['a_only'] + t['b_only'], 0.5, alternative='greater').pvalue
                   if t['a_only'] + t['b_only'] else 1.0)
# attribution
agree = sum(A[i] == B[i] for i in key)
ca, cb = Counter(A[i] for i in key), Counter(B[i] for i in key)
pe = sum(ca[k] * cb[k] for k in ca) / len(key) ** 2
res['attribution_agreement'] = dict(n=len(key), agree=agree, kappa=(agree / len(key) - pe) / (1 - pe), adjudicated=len(key) - agree)
by = {}
for i, k in key.items():
    by.setdefault(k['source'], Counter())[final[i]] += 1
res['attribution'] = {s: dict(n=sum(c.values()), counts=dict(c), implausible=c['implausible_data'],
                              meaningful=sum(c[v] for v in MEANINGFUL), errors=c['pred_wrong'] + c['both_wrong'])
                      for s, c in by.items()}
cg, cgr, fzr = res['attribution']['CaliberGraph'], res['attribution']['CaliberGraph-R'], res['attribution']['Fuzz-R']
# H-S2: implausible share CG-R@A_R < CG@A_1f, one-sided Fisher
res['H_S2'] = dict(cg_impl=f"{cg['implausible']}/{cg['n']}", cgr_impl=f"{cgr['implausible']}/{cgr['n']}",
                   p_one_sided=fisher_exact([[cg['implausible'], cg['n'] - cg['implausible']],
                                             [cgr['implausible'], cgr['n'] - cgr['implausible']]], alternative='greater')[1])
# H-S3: estimated meaningful A_R witnesses CG-R vs Fuzz-R, parametric bootstrap (as H6)
Na, Nb = S['main']['cgr']['R'], S['main']['fuzzr']['R']
pa, pb = cgr['meaningful'] / cgr['n'], fzr['meaningful'] / fzr['n']
rng = random.Random(7)
da = []
for _ in range(10000):
    xa = Na * sum(rng.random() < pa for _ in range(cgr['n'])) / cgr['n']
    xb = Nb * sum(rng.random() < pb for _ in range(fzr['n'])) / fzr['n']
    da.append(xa - xb)
da.sort()
res['H_S3'] = dict(est_cgr=Na * pa, est_fuzzr=Nb * pb, diff=Na * pa - Nb * pb, ci95=[da[250], da[9749]],
                   p_one_sided=sum(1 for x in da if x <= 0) / len(da))
res['profile_compare'] = json.load(open(os.path.join(D, 'profile_compare.json')))
json.dump(res, open(os.path.join(D, 's3d_summary.json'), 'w'), indent=1, default=float)
print(json.dumps({k: v for k, v in res.items() if k != 'profile_compare'}, indent=1, default=float))
