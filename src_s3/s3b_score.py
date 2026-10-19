"""S3-B (docs/en/17): score the cross-model annotation (claude-sonnet-5-5, one blind pass, frozen prompt) against the
Opus final labels, and, on the 60 human-validation items, against each human annotator.
Usage: python src_s3/s3b_score.py -> results/stage3/s3b_crossmodel.json"""
import glob, json, math, os, random, sys
from collections import Counter
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src_r'))
from human_validation import final, parse, kappa  # noqa: E402
from scipy.stats import fisher_exact  # noqa: E402
O = os.path.join(ROOT, 'results', 'stage3', 's3b')
key = {k['idx']: k for k in json.load(open(os.path.join(O, 'key.json')))}
son = {}
for f in sorted(glob.glob(os.path.join(O, 'batch*_ann_sonnet.json'))):
    for x in json.load(open(f)):
        son[x['idx']] = x['verdict']
opus = {}
for prefix in ('test_v4', 'test_r'):
    for x in final(prefix):
        opus[(x['item']['pair_id'], x['source'])] = x['ai']
D = os.path.join(ROOT, 'results', 'audit', 'human_validation')
hk = {(k['pair_id'], k['source']): k['no'] for k in json.load(open(os.path.join(D, 'key_DO_NOT_OPEN_BEFORE_ANNOTATING.json')))}
h1, h2 = parse(os.path.join(D, 'sheet_annotator1.md')), parse(os.path.join(D, 'sheet_annotator2.md'))
B = lambda v: 'imp' if v == 'implausible_data' else 'other'  # noqa: E731


def bk(x, y):
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


def comp(ids, a, b):
    x = [a[i] for i in ids]; y = [b[i] for i in ids]
    xb, yb = [B(v) for v in x], [B(v) for v in y]
    return dict(n=len(ids), agree5=sum(p == q for p, q in zip(x, y)), kappa5=kappa(x, y), kappa5_ci=boot(kappa, x, y),
                agree2=sum(p == q for p, q in zip(xb, yb)), kappa2=bk(xb, yb), kappa2_ci=boot(bk, xb, yb))


ids = sorted(i for i in key if i in son)
op = {i: opus[(key[i]['pair_id'], key[i]['source'])] for i in ids}
res = dict(n_annotated=len(ids), missing=sorted(set(key) - set(son)),
           labels_sonnet=Counter(son[i] for i in ids), labels_opus=Counter(op[i] for i in ids),
           M_B1_sonnet_vs_opus=comp(ids, son, op))
st = {}
for s in (1, 2):
    it = [i for i in ids if key[i]['stage'] == s]
    st[f'stage{s}'] = dict(n=len(it), sonnet_imp=sum(son[i] == 'implausible_data' for i in it),
                           opus_imp=sum(op[i] == 'implausible_data' for i in it))
a, b = st['stage1'], st['stage2']
st['H_B2_fisher_one_sided'] = fisher_exact([[a['sonnet_imp'], a['n'] - a['sonnet_imp']], [b['sonnet_imp'], b['n'] - b['sonnet_imp']]], alternative='greater')[1]
res['M_B2_by_stage'] = st
hv = [i for i in ids if key[i]['hv']]
H1 = {i: h1[hk[(key[i]['pair_id'], key[i]['source'])]] for i in hv}
H2 = {i: h2[hk[(key[i]['pair_id'], key[i]['source'])]] for i in hv}
res['M_B3_on_60'] = dict(sonnet_vs_h1=comp(hv, son, H1), sonnet_vs_h2=comp(hv, son, H2), sonnet_vs_opus=comp(hv, son, op))
res['H_B1_binary_kappa_ge_0.60'] = res['M_B1_sonnet_vs_opus']['kappa2'] >= 0.60
res['H_B2_p_unadjusted'] = st['H_B2_fisher_one_sided']
json.dump(res, open(os.path.join(ROOT, 'results', 'stage3', 's3b_crossmodel.json'), 'w'), indent=1, default=float)
print(json.dumps(res, indent=1, default=float))
