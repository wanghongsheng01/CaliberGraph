"""Human validation of the AI attribution (ICDE revision). Two modes:

  build: draw a simple random sample of the headline attribution items (first-stage samples at A_1f/A_0
         and second-stage samples at A_R), shuffle them, and write a blind annotation sheet without tool,
         tier or AI verdicts, plus a private key.
         python human_validation.py build --n1 30 --n2 30 --seed 20261016 --out ../results/audit/human_validation
  score: parse one or two filled sheets and report human-AI agreement (overall, by stage, Cohen's kappa)
         and, with two sheets, human-human agreement.
         python human_validation.py score --dir ../results/audit/human_validation SHEET_A.md [SHEET_B.md]
"""
import argparse
import json
import os
import random
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from score import qcols, load_pairs  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
LABELS = ['pred_wrong', 'gold_wrong', 'both_wrong', 'ambiguous', 'implausible_data']


def P(*a):
    return os.path.join(ROOT, *a)


def final(prefix):
    key = json.load(open(P('results/audit', prefix + '_key.json')))
    A = {x['idx']: x['verdict'] for x in json.load(open(P('results/audit', prefix + '_ann_a.json')))}
    B = {x['idx']: x['verdict'] for x in json.load(open(P('results/audit', prefix + '_ann_b.json')))}
    C = {x['idx']: x['verdict'] for x in json.load(open(P('results/audit', prefix + '_ann_c.json')))}
    blind = {b['idx']: b for b in json.load(open(P('results/audit', prefix + '_blind.json')))}
    out = []
    for k in key:
        if k['source'].startswith('calib:'):
            continue
        i = k['idx']
        v = A[i] if A[i] == B[i] else C[i]
        out.append(dict(source=k['source'], ai=v, item=blind[i]))
    return out


def fmt_table(name, t, cols):
    keep = [j for j, c in enumerate(t['columns']) if (name.lower(), c.lower()) in cols]
    if not keep:
        keep = list(range(min(4, len(t['columns']))))
    head = [t['columns'][j] for j in keep]
    lines = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    for r in t['rows']:
        lines.append('| ' + ' | '.join('NULL' if r[j] is None else str(r[j]).replace('|', '\\|').replace('\n', ' ')[:60]
                                       for j in keep) + ' |')
    omitted = len(t['columns']) - len(keep)
    return f'*{name}*' + (f' ({omitted} unreferenced columns omitted)' if omitted else '') + '\n\n' + '\n'.join(lines)


def build(a):
    rng = random.Random(a.seed)
    s1 = final('test_v4')
    s2 = final('test_r')
    pick = rng.sample(s1, a.n1) + rng.sample(s2, a.n2)
    rng.shuffle(pick)
    pairs = {p['pair_id']: p for p in load_pairs('test')}
    os.makedirs(a.out, exist_ok=True)
    key, md = [], ['# Human attribution sheet (blind)\n',
                   'For each item, read the question, evidence, both queries, the witness database and the two results, '
                   'then replace `____` after **Verdict:** with exactly one of: '
                   '`pred_wrong`, `gold_wrong`, `both_wrong`, `ambiguous`, `implausible_data`. See INSTRUCTIONS.md. '
                   'Do not consult any other file of the repository while annotating.\n']
    for n, x in enumerate(pick, 1):
        it = x['item']
        key.append(dict(no=n, pair_id=it['pair_id'], source=x['source'], ai=x['ai']))
        cols = qcols(pairs[it['pair_id']])
        md.append(f"\n---\n\n## Item {n} ({it['db_id']})\n")
        md.append(f"**Question:** {it['question']}\n\n**Evidence:** {it.get('evidence') or '-'}\n")
        md.append(f"**Gold SQL:**\n```sql\n{it['gold']}\n```\n**Predicted SQL:**\n```sql\n{it['pred']}\n```\n")
        md.append('**Witness database:**\n')
        for t, tv in it['witness'].items():
            md.append(fmt_table(t, tv, cols) + '\n')
        md.append(f"**Gold result on the witness:** `{it['gold_rows']}`  \n**Predicted result on the witness:** `{it['pred_rows']}`\n")
        md.append('**Verdict:** ____  \n**Reason (one sentence):** \n')
    open(os.path.join(a.out, 'sheet_blind.md'), 'w').write('\n'.join(md))
    json.dump(key, open(os.path.join(a.out, 'key_DO_NOT_OPEN_BEFORE_ANNOTATING.json'), 'w'), indent=1)
    print('wrote', len(pick), 'items to', a.out, Counter(k['source'] for k in key))


def parse(path):
    txt = open(path).read()
    out = {}
    for m in re.finditer(r'## Item (\d+).*?\*\*Verdict:\*\*\s*`?([a-z_]+)`?', txt, re.S):
        if m.group(2) in LABELS:
            out[int(m.group(1))] = m.group(2)
    return out


def kappa(x, y):
    n = len(x)
    po = sum(a == b for a, b in zip(x, y)) / n
    cx, cy = Counter(x), Counter(y)
    pe = sum(cx[l] * cy[l] for l in LABELS) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def score(a):
    key = {k['no']: k for k in json.load(open(os.path.join(a.dir, 'key_DO_NOT_OPEN_BEFORE_ANNOTATING.json')))}
    res = {}
    sheets = [parse(s) for s in a.sheets]
    for h, (name, sh) in enumerate(zip(a.sheets, sheets)):
        common = sorted(set(sh) & set(key))
        hx = [sh[i] for i in common]
        ax = [key[i]['ai'] for i in common]
        r = dict(n=len(common), agree=sum(p == q for p, q in zip(hx, ax)), kappa=kappa(hx, ax),
                 agree_implausible_vs_not=sum((p == 'implausible_data') == (q == 'implausible_data') for p, q in zip(hx, ax)))
        for stage, pref in (('first_stage', ('CaliberGraph@', 'Fuzz@', 'ParSEval', 'SpotIt')), ('second_stage', ('CaliberGraph-R@', 'Fuzz-R@'))):
            cs = [i for i in common if key[i]['source'].startswith(pref) and not (stage == 'first_stage' and '-R@' in key[i]['source'])]
            r[stage] = dict(n=len(cs), agree=sum(sh[i] == key[i]['ai'] for i in cs),
                            human_implausible=sum(sh[i] == 'implausible_data' for i in cs),
                            ai_implausible=sum(key[i]['ai'] == 'implausible_data' for i in cs))
        res[f'annotator_{h + 1}_vs_ai'] = r
    if len(sheets) == 2:
        common = sorted(set(sheets[0]) & set(sheets[1]))
        x = [sheets[0][i] for i in common]
        y = [sheets[1][i] for i in common]
        res['annotator_1_vs_2'] = dict(n=len(common), agree=sum(p == q for p, q in zip(x, y)), kappa=kappa(x, y))
    out = os.path.join(a.dir, 'human_validation_summary.json')
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps(res, indent=1))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    b = sp.add_parser('build')
    b.add_argument('--n1', type=int, default=30)
    b.add_argument('--n2', type=int, default=30)
    b.add_argument('--seed', type=int, default=20261016)
    b.add_argument('--out', required=True)
    s = sp.add_parser('score')
    s.add_argument('--dir', required=True)
    s.add_argument('sheets', nargs='+')
    a = ap.parse_args()
    build(a) if a.cmd == 'build' else score(a)


if __name__ == '__main__':
    main()
