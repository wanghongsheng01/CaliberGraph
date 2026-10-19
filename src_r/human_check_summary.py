"""Regenerate the summaries of the first author's filled human-check sheets, comparing the author's
verdicts with the AI annotation passes.

Two sheets (30 items each, numbered 1..30 in the order of the corresponding *_idx.json file):

  v4  (first freeze, pilot attribution sample)
      sheet   results/test/audit/human_check_filled.md
      index   results/test/audit/human_check_idx.json        (idx into the annotation passes)
      passes  results/test/audit/attribution_a.json, attribution_b.json
      output  results/test/audit/human_check_summary.json
      n, agree_a / agree_b (human == pass A / B), n_ai_agree (A == B), agree_on_ai_agree (human == A on
      the items with A == B), agree_any (human in {A, B}); items: idx, pair_id, human, ai_a, ai_b.

  R   (second freeze, tier-R witness sample)
      sheet   results/audit/human_check_R_filled.md
      index   results/audit/human_check_R_idx.json
      key     results/audit/test_r_key.json (source 'Method@Tier')
      passes  results/audit/test_r_ann_a.json, test_r_ann_b.json, test_r_ann_c.json (adjudication)
      output  results/audit/human_check_R_summary.json
      final = A if A == B else C (as in analyze_r.py); n, agree_final, agree_a, agree_b,
      agree_any (human in {A, B}), agree_implausible_binary ((human == implausible_data) ==
      (final == implausible_data)); items: n (sheet number), idx, pair_id, source, human, final, a, b.

The author's verdict is the bold cell (**verdict**) of column 6 ("我的判定") of the table rows
"| <number> | <pair_id>（<db>） | ...". The AI verdicts are taken from the annotation files; the AI
columns printed on the sheet are only cross-checked (a mismatch is reported on stderr).

Usage (from src_r/):
    python human_check_summary.py v4 --out ../results/test/audit/human_check_summary.json
    python human_check_summary.py R  --out ../results/audit/human_check_R_summary.json
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


def P(*a):
    return os.path.join(ROOT, 'results', *a)


def parse_sheet(path):
    """Rows of the verdict table: list of (number, pair_id, human verdict, cells)."""
    rows = []
    for line in open(path, encoding='utf-8'):
        if not re.match(r'^\| \d+ \|', line):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        m = re.fullmatch(r'\*\*(\w+)\*\*', cells[5])
        if not m:
            raise ValueError(f'no bold verdict in row: {line[:80]}')
        rows.append((int(cells[0]), cells[1].split('（')[0].strip(), m.group(1), cells))
    return rows


def warn(msg):
    print('WARNING:', msg, file=sys.stderr)


def summary_v4():
    idx = json.load(open(P('test', 'audit', 'human_check_idx.json')))
    A = {x['idx']: x for x in json.load(open(P('test', 'audit', 'attribution_a.json')))}
    B = {x['idx']: x for x in json.load(open(P('test', 'audit', 'attribution_b.json')))}
    rows = parse_sheet(P('test', 'audit', 'human_check_filled.md'))
    assert len(rows) == len(idx) and [r[0] for r in rows] == list(range(1, len(idx) + 1))
    items = []
    for (num, pid, human, cells), i in zip(rows, idx):
        a, b = A[i]['verdict'], B[i]['verdict']
        if A[i]['pair_id'] != pid:
            warn(f'#{num}: sheet pair {pid} != annotation pair {A[i]["pair_id"]}')
        if (cells[-2], cells[-1]) != (a, b):
            warn(f'#{num}: sheet AI columns {cells[-2:]} != annotation files {(a, b)}')
        items.append(dict(idx=i, pair_id=pid, human=human, ai_a=a, ai_b=b))
    ai_agree = [x for x in items if x['ai_a'] == x['ai_b']]
    return dict(n=len(items),
                agree_a=sum(x['human'] == x['ai_a'] for x in items),
                agree_b=sum(x['human'] == x['ai_b'] for x in items),
                n_ai_agree=len(ai_agree),
                agree_on_ai_agree=sum(x['human'] == x['ai_a'] for x in ai_agree),
                agree_any=sum(x['human'] in (x['ai_a'], x['ai_b']) for x in items),
                items=items)


def summary_r():
    idx = json.load(open(P('audit', 'human_check_R_idx.json')))
    key = {x['idx']: x for x in json.load(open(P('audit', 'test_r_key.json')))}
    A, B, C = ({x['idx']: x['verdict'] for x in json.load(open(P('audit', f'test_r_ann_{s}.json')))} for s in 'abc')
    rows = parse_sheet(P('audit', 'human_check_R_filled.md'))
    assert len(rows) == len(idx) and [r[0] for r in rows] == list(range(1, len(idx) + 1))
    items = []
    for (num, pid, human, cells), i in zip(rows, idx):
        a, b = A[i], B[i]
        final = a if a == b else C[i]
        if key[i]['pair_id'] != pid:
            warn(f'#{num}: sheet pair {pid} != key pair {key[i]["pair_id"]}')
        if len(cells) >= 9 and cells[7] != final:
            warn(f'#{num}: sheet final {cells[7]} != recomputed final {final}')
        items.append(dict(n=num, idx=i, pair_id=pid, source=key[i]['source'], human=human, final=final, a=a, b=b))
    imp = 'implausible_data'
    return dict(n=len(items),
                agree_final=sum(x['human'] == x['final'] for x in items),
                agree_a=sum(x['human'] == x['a'] for x in items),
                agree_b=sum(x['human'] == x['b'] for x in items),
                agree_any=sum(x['human'] in (x['a'], x['b']) for x in items),
                agree_implausible_binary=sum((x['human'] == imp) == (x['final'] == imp) for x in items),
                items=items)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('sheet', choices=['v4', 'R'])
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    S = summary_v4() if a.sheet == 'v4' else summary_r()
    json.dump(S, open(a.out, 'w'), indent=1)
    print(json.dumps({k: v for k, v in S.items() if k != 'items'}))


if __name__ == '__main__':
    main()
