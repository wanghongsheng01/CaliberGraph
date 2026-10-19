"""Stage-3 S3-A: pre-registered measures for the human validation (docs/en/17, S3-A).
Usage: python src_s3/s3a_human.py  -> results/stage3/s3a_human.json"""
import json, os, re, sys, math, random
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src_r'))
from human_validation import parse, kappa, LABELS  # noqa
from scipy.stats import fisher_exact
ROOT = os.path.join(os.path.dirname(__file__), '..')
# optional arguments (round 2, docs/en/17b): DIR SHEET1 SHEET2 OUT
D = os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else 'results/audit/human_validation')
S1, S2 = (sys.argv[2], sys.argv[3]) if len(sys.argv) > 3 else ('sheet_annotator1.md', 'sheet_annotator2.md')
OUT = sys.argv[4] if len(sys.argv) > 4 else 'results/stage3/s3a_human.json'
key = {k['no']: k for k in json.load(open(os.path.join(D, 'key_DO_NOT_OPEN_BEFORE_ANNOTATING.json')))}
h1 = parse(os.path.join(D, S1)); h2 = parse(os.path.join(D, S2))
ids = sorted(set(h1) & set(h2) & set(key))
stage = {i: (2 if re.match(r'(CaliberGraph-R|Fuzz-R)@', key[i]['source']) else 1) for i in ids}
ai = {i: key[i]['ai'] for i in ids}
B = lambda v: 'imp' if v == 'implausible_data' else 'other'

def bkappa(x, y):
    n = len(x); po = sum(a == b for a, b in zip(x, y)) / n
    cx, cy = Counter(x), Counter(y); pe = sum(cx[l] * cy[l] for l in set(x) | set(y)) / n / n
    return (po - pe) / (1 - pe) if pe < 1 else float('nan')

def boot(fn, x, y, n=10000, seed=20261018):
    r = random.Random(seed); m = len(x); out = []
    for _ in range(n):
        idx = [r.randrange(m) for _ in range(m)]
        v = fn([x[i] for i in idx], [y[i] for i in idx])
        if not math.isnan(v): out.append(v)
    out.sort(); return [out[int(0.025 * len(out))], out[int(0.975 * len(out)) - 1]]

def wilson(k, n, z=1.96):
    if n == 0: return [None, None]
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [c - h, c + h]

def pair(a, b):
    x = [a[i] for i in ids]; y = [b[i] for i in ids]
    xb = [B(v) for v in x]; yb = [B(v) for v in y]
    return dict(n=len(ids), agree5=sum(p == q for p, q in zip(x, y)), kappa5=kappa(x, y), kappa5_ci=boot(kappa, x, y),
                agree2=sum(p == q for p, q in zip(xb, yb)), kappa2=bkappa(xb, yb), kappa2_ci=boot(bkappa, xb, yb),
                confusion={f'{l}->{m}': sum(1 for p, q in zip(x, y) if p == l and q == m) for l in LABELS for m in LABELS if any(p == l and q == m for p, q in zip(x, y))})

res = {'n_items': len(ids), 'labels': {'h1': Counter(h1[i] for i in ids), 'h2': Counter(h2[i] for i in ids), 'ai': Counter(ai[i] for i in ids)},
       'M_A1_h1_vs_h2': pair(h1, h2), 'M_A2_h1_vs_ai': pair(h1, ai), 'M_A2_h2_vs_ai': pair(h2, ai)}
cons = [i for i in ids if h1[i] == h2[i]]
shares = {}
for name, lab, pool in (('h1', h1, ids), ('h2', h2, ids), ('ai', ai, ids), ('consensus', h1, cons)):
    s = {}
    for st in (1, 2):
        it = [i for i in pool if stage[i] == st]; k = sum(lab[i] == 'implausible_data' for i in it)
        s[f'stage{st}'] = dict(n=len(it), implausible=k, share=k / len(it) if it else None, wilson=wilson(k, len(it)))
    a, b = s['stage1'], s['stage2']
    s['fisher_one_sided_stage1_gt_stage2'] = fisher_exact([[a['implausible'], a['n'] - a['implausible']], [b['implausible'], b['n'] - b['implausible']]], alternative='greater')[1]
    shares[name] = s
res['M_A3_implausible_by_stage'] = shares
res['H_A1_binary_kappa_h1_h2_ge_0.60'] = res['M_A1_h1_vs_h2']['kappa2'] >= 0.60
res['H_A2_binary_kappa_each_human_vs_ai_ge_0.60'] = all(res[k]['kappa2'] >= 0.60 for k in ('M_A2_h1_vs_ai', 'M_A2_h2_vs_ai'))
res['H_A3_p_unadjusted'] = shares['consensus']['fisher_one_sided_stage1_gt_stage2']
# by source: what the humans said where the AI said implausible
res['ai_implausible_items'] = [dict(no=i, stage=stage[i], source=key[i]['source'], h1=h1[i], h2=h2[i]) for i in ids if ai[i] == 'implausible_data']
res['by_source'] = {}
for i in ids:
    s = key[i]['source'].split('@')[0]
    d = res['by_source'].setdefault(s, Counter())
    d['n'] += 1; d['ai_imp'] += ai[i] == 'implausible_data'; d['h1_imp'] += h1[i] == 'implausible_data'; d['h2_imp'] += h2[i] == 'implausible_data'
    d['h1_eq_ai'] += h1[i] == ai[i]; d['h2_eq_ai'] += h2[i] == ai[i]
json.dump(res, open(os.path.join(ROOT, OUT), 'w'), indent=1, default=float)
print(json.dumps(res, indent=1, default=float))
