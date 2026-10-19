"""Scoring of the third human validation round (pre-registration docs/en/17c).

M-R3-1  Fleiss' kappa of the three annotators (five labels; binary implausible vs other); pairwise Cohen's kappa.
M-R3-2  Human majority label (>= 2 of 3 annotators); items without one are "no majority".
M-R3-3  Cohen's kappa human majority vs AI final label (five labels, binary), over items with a majority.
M-R3-4  Label shares by stage, human majority and AI, 95% bootstrap intervals over items (10,000, seed 20261022).
H-R3-1  Fleiss binary kappa >= 0.60.            H-R3-2  binary kappa majority vs AI >= 0.60.
H-R3-3  majority implausible share stage 1 > stage 2, one-sided Fisher, alpha 0.05.
H-R3-4  stage-2 prediction-error share (pred_wrong + both_wrong), majority vs AI, exact two-sided McNemar.
Sensitivity (post hoc, labelled as such in the output): the same measures without annotator A (two annotators,
consensus = both agree), because the process check (src_s3/hv3_check.py) found A's reasons templated.
Usage: python src_s3/s3a_human_r3.py [OUT]   (default results/stage3/s3a_human_r3.json)
"""
import json
import math
import os
import random
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src_r'))
sys.path.insert(0, os.path.dirname(__file__))
from human_validation import kappa, LABELS  # noqa: E402
from stats_eval import mcnemar_exact  # noqa: E402
from hv3_check import split_items, verdict  # noqa: E402
from scipy.stats import fisher_exact  # noqa: E402

D = os.path.join(ROOT, 'results', 'audit', 'human_validation_r3')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'results', 'stage3', 's3a_human_r3.json')
SEED, NB = 20261022, 10000
PRED_ERR = ('pred_wrong', 'both_wrong')


def B(v):
    return 'imp' if v == 'implausible_data' else 'other'


def bkappa(x, y):
    n = len(x)
    po = sum(a == b for a, b in zip(x, y)) / n
    cx, cy = Counter(x), Counter(y)
    pe = sum(cx[l] * cy[l] for l in set(x) | set(y)) / n / n
    return (po - pe) / (1 - pe) if pe < 1 else float('nan')


def fleiss(rows, cats):
    """rows: list of label tuples (one label per rater)."""
    n, k = len(rows), len(rows[0])
    P, tot = [], Counter()
    for r in rows:
        c = Counter(r)
        tot.update(c)
        P.append((sum(v * v for v in c.values()) - k) / (k * (k - 1)))
    pbar = sum(P) / n
    pe = sum((tot[c] / (n * k)) ** 2 for c in cats)
    return (pbar - pe) / (1 - pe) if pe < 1 else float('nan')


def boot_ci(fn, idx, seed=SEED, nb=NB):
    r = random.Random(seed)
    out = []
    for _ in range(nb):
        s = [idx[r.randrange(len(idx))] for _ in idx]
        v = fn(s)
        if v is not None and not (isinstance(v, float) and math.isnan(v)):
            out.append(v)
    out.sort()
    return [out[int(0.025 * len(out))], out[int(0.975 * len(out)) - 1]] if out else [None, None]


def majority(labels):
    v, n = Counter(labels).most_common(1)[0]
    return v if n >= 2 else None


def main():
    key = {k['code']: k for k in json.load(open(os.path.join(D, 'key_DO_NOT_OPEN_BEFORE_ANNOTATING.json')))}
    H = {}
    for w in 'ABC':
        _, items = split_items(open(os.path.join(D, f'sheet_r3_annotator{w}.md')).read())
        H[w] = {c: verdict(b)[0] for c, b in items.items()}
    ids = sorted(c for c in key if all(H[w].get(c) in LABELS for w in 'ABC'))
    stage = {c: key[c]['stage'] for c in ids}
    ai = {c: key[c]['ai'] for c in ids}
    maj = {c: majority([H[w][c] for w in 'ABC']) for c in ids}
    withmaj = [c for c in ids if maj[c]]
    R = dict(n_items=len(ids), n_stage={s: sum(1 for c in ids if stage[c] == s) for s in (1, 2)},
             labels={w: dict(Counter(H[w][c] for c in ids)) for w in 'ABC'})
    R['labels']['ai'] = dict(Counter(ai[c] for c in ids))
    R['labels']['majority'] = dict(Counter(maj[c] or 'no_majority' for c in ids))
    # M-R3-1
    f5 = lambda s: fleiss([tuple(H[w][c] for w in 'ABC') for c in s], LABELS)
    f2 = lambda s: fleiss([tuple(B(H[w][c]) for w in 'ABC') for c in s], ('imp', 'other'))
    R['M_R3_1'] = dict(fleiss5=f5(ids), fleiss5_ci=boot_ci(f5, ids), fleiss2=f2(ids), fleiss2_ci=boot_ci(f2, ids),
                       pairwise={})
    for a, b in (('A', 'B'), ('A', 'C'), ('B', 'C')):
        x, y = [H[a][c] for c in ids], [H[b][c] for c in ids]
        R['M_R3_1']['pairwise'][a + b] = dict(agree5=sum(p == q for p, q in zip(x, y)), kappa5=kappa(x, y),
                                              agree2=sum(B(p) == B(q) for p, q in zip(x, y)),
                                              kappa2=bkappa([B(v) for v in x], [B(v) for v in y]))
    # M-R3-2 / M-R3-3
    R['M_R3_2'] = dict(with_majority=len(withmaj), no_majority=len(ids) - len(withmaj),
                       unanimous=sum(1 for c in ids if len({H[w][c] for w in 'ABC'}) == 1))
    k5 = lambda s: kappa([maj[c] for c in s], [ai[c] for c in s])
    k2 = lambda s: bkappa([B(maj[c]) for c in s], [B(ai[c]) for c in s])
    R['M_R3_3'] = dict(n=len(withmaj), agree5=sum(maj[c] == ai[c] for c in withmaj), kappa5=k5(withmaj),
                       kappa5_ci=boot_ci(k5, withmaj), agree2=sum(B(maj[c]) == B(ai[c]) for c in withmaj),
                       kappa2=k2(withmaj), kappa2_ci=boot_ci(k2, withmaj),
                       confusion={f'{l}->{m}': sum(1 for c in withmaj if maj[c] == l and ai[c] == m)
                                  for l in LABELS for m in LABELS if any(maj[c] == l and ai[c] == m for c in withmaj)})
    # binary majority of the three binary judgements (always defined), reported alongside
    bmaj = {c: Counter(B(H[w][c]) for w in 'ABC').most_common(1)[0][0] for c in ids}
    kb = lambda s: bkappa([bmaj[c] for c in s], [B(ai[c]) for c in s])
    R['M_R3_3']['binary_majority_of_binary'] = dict(n=len(ids), kappa2=kb(ids), kappa2_ci=boot_ci(kb, ids))
    # M-R3-4 shares by stage
    shares = {}
    for st in (1, 2):
        it = [c for c in ids if stage[c] == st]
        itm = [c for c in it if maj[c]]
        row = {'n': len(it), 'n_with_majority': len(itm), 'majority': {}, 'ai': {}, 'ai_same_items': {}}
        for lab in LABELS + ['pred_error']:
            hit = (lambda v: v in PRED_ERR) if lab == 'pred_error' else (lambda v, l=lab: v == l)
            fm = lambda s, h=hit: sum(h(maj[c]) for c in s) / len(s)
            fa = lambda s, h=hit: sum(h(ai[c]) for c in s) / len(s)
            row['majority'][lab] = dict(k=sum(hit(maj[c]) for c in itm), share=fm(itm), ci=boot_ci(fm, itm))
            row['ai'][lab] = dict(k=sum(hit(ai[c]) for c in it), share=fa(it), ci=boot_ci(fa, it))
            row['ai_same_items'][lab] = dict(k=sum(hit(ai[c]) for c in itm), share=fa(itm))
        shares[f'stage{st}'] = row
    R['M_R3_4'] = shares
    # hypotheses
    s1 = [c for c in withmaj if stage[c] == 1]
    s2 = [c for c in withmaj if stage[c] == 2]
    i1 = sum(maj[c] == 'implausible_data' for c in s1)
    i2 = sum(maj[c] == 'implausible_data' for c in s2)
    p3 = fisher_exact([[i1, len(s1) - i1], [i2, len(s2) - i2]], alternative='greater')[1]
    b = sum(1 for c in s2 if maj[c] in PRED_ERR and ai[c] not in PRED_ERR)
    cc = sum(1 for c in s2 if ai[c] in PRED_ERR and maj[c] not in PRED_ERR)
    p4 = mcnemar_exact(b, cc)
    R['hypotheses'] = {
        'H-R3-1': dict(value=R['M_R3_1']['fleiss2'], threshold=0.60, met=R['M_R3_1']['fleiss2'] >= 0.60),
        'H-R3-2': dict(value=R['M_R3_3']['kappa2'], threshold=0.60, met=R['M_R3_3']['kappa2'] >= 0.60),
        'H-R3-3': dict(stage1=[i1, len(s1)], stage2=[i2, len(s2)], p_one_sided=float(p3), met=bool(p3 < 0.05)),
        'H-R3-4': dict(n=len(s2), majority_pred_error=sum(maj[c] in PRED_ERR for c in s2),
                       ai_pred_error=sum(ai[c] in PRED_ERR for c in s2), majority_only=b, ai_only=cc, p_two_sided=p4,
                       met=bool(p4 < 0.05))}
    # post-hoc sensitivity without annotator A
    cons = [c for c in ids if H['B'][c] == H['C'][c]]
    x, y = [H['B'][c] for c in ids], [H['C'][c] for c in ids]
    kc2 = lambda s: bkappa([B(H['B'][c]) for c in s], [B(ai[c]) for c in s])
    sens = dict(note='post hoc, not pre-registered: annotators B and C only; consensus = B and C agree',
                kappa2_B_C=bkappa([B(v) for v in x], [B(v) for v in y]), kappa5_B_C=kappa(x, y),
                n_consensus=len(cons),
                kappa2_consensus_vs_ai=bkappa([B(H['B'][c]) for c in cons], [B(ai[c]) for c in cons]),
                kappa2_consensus_vs_ai_ci=boot_ci(kc2, cons))
    c1 = [c for c in cons if stage[c] == 1]
    c2 = [c for c in cons if stage[c] == 2]
    sens['implausible_stage1'] = [sum(H['B'][c] == 'implausible_data' for c in c1), len(c1)]
    sens['implausible_stage2'] = [sum(H['B'][c] == 'implausible_data' for c in c2), len(c2)]
    sens['pred_error_stage2_consensus'] = [sum(H['B'][c] in PRED_ERR for c in c2), len(c2)]
    sens['pred_error_stage2_ai_same_items'] = [sum(ai[c] in PRED_ERR for c in c2), len(c2)]
    R['sensitivity_without_A'] = sens
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(R, open(OUT, 'w'), indent=1)
    print(json.dumps({k: R[k] for k in ('n_items', 'labels', 'M_R3_2', 'hypotheses', 'sensitivity_without_A')}, indent=1))
    print('fleiss', R['M_R3_1']['fleiss5'], R['M_R3_1']['fleiss2'], 'maj-ai', R['M_R3_3']['kappa5'], R['M_R3_3']['kappa2'])


if __name__ == '__main__':
    main()
