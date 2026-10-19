"""S3-F (docs/en/17): Holm correction over the pre-registered Stage-3 test family, plus threshold hypotheses.
Usage: python src_s3/s3f_family.py -> results/stage3/s3f_family.json"""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
R = os.path.join(ROOT, 'results', 'stage3')
L = lambda p: json.load(open(os.path.join(R, p)))  # noqa: E731
a, b, c, d, e = L('s3a_human.json'), L('s3b_crossmodel.json'), L('s3c_arcwise.json'), L('s3d/s3d_summary.json'), L('s3e/s3e_summary.json')
P = {'H-A3': a['H_A3_p_unadjusted'], 'H-B2': b['H_B2_p_unadjusted'],
     'H-C1': c['confirmatory_unadjusted']['H-C1']['p_one_sided'], 'H-C2': c['confirmatory_unadjusted']['H-C2']['p_one_sided'],
     'H-S1': d['H_S1']['p_one_sided'], 'H-S2': d['H_S2']['p_one_sided'], 'H-S3': d['H_S3']['p_one_sided'],
     'H-E1': e['H_E1']['p_one_sided']}
order = sorted(P, key=P.get)
m, adj, run, stop = len(P), {}, 0.0, False
for i, h in enumerate(order):
    run = max(run, min(1.0, (m - i) * P[h]))
    adj[h] = run
res = dict(p=P, holm_adjusted=adj, significant={h: adj[h] < 0.05 for h in P},
           thresholds={'H-A1': a['H_A1_binary_kappa_h1_h2_ge_0.60'], 'H-A2': a['H_A2_binary_kappa_each_human_vs_ai_ge_0.60'],
                       'H-B1': b['H_B1_binary_kappa_ge_0.60']})
r2 = L('s3a_human_r2.json')
res['round2_17b'] = {'H-R2-1': r2['H_A1_binary_kappa_h1_h2_ge_0.60'], 'H-R2-2': r2['H_A2_binary_kappa_each_human_vs_ai_ge_0.60'],
                     'H-R2-3_p': r2['H_A3_p_unadjusted']}
json.dump(res, open(os.path.join(R, 's3f_family.json'), 'w'), indent=1, default=float)
print(json.dumps(res, indent=1, default=float))
