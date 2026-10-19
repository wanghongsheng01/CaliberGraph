"""Second human validation round (option B, docs/en/17a E3; to be pre-registered in docs/en/17b before it starts).

Differences from round 1 (src_r/human_validation.py build):
  * a new random sample: 30 first-stage and 30 second-stage attributed items not used in round 1, seed 20261021;
  * every item carries a neutral, mechanically generated section "Facts from the real (official) database":
    for each column that either query references and that appears in the witness: rows, NULLs, distinct
    values and uniqueness in the official table, and how often each witness value of that column occurs
    there; tables of at most 15 real rows that a query references are shown in full (referenced columns).
    The facts are the same kind for every item and are not selected by any annotator's verdict or by the
    data profile.
Usage: python src_s3/hv2_build.py --out results/audit/human_validation_r2
"""
import argparse
import json
import os
import random
import sqlite3
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src_r'))
from human_validation import final, fmt_table  # noqa: E402
from score import load_pairs, qcols  # noqa: E402

_CON = {}
_CACHE = {}


def con(db):
    if db not in _CON:
        p = os.path.join(ROOT, 'data', 'official', 'dev_databases', db, f'{db}.sqlite')
        _CON[db] = sqlite3.connect(f'file:{p}?mode=ro', uri=True)
    return _CON[db]


def q(x):
    return '"' + x.replace('"', '""') + '"'


def col_stats(db, t, c):
    k = (db, t, c)
    if k not in _CACHE:
        cur = con(db)
        n, nn, nd = cur.execute(f'SELECT COUNT(*), COUNT({q(c)}), COUNT(DISTINCT {q(c)}) FROM {q(t)}').fetchone()
        _CACHE[k] = (n, n - nn, nd, nd == nn and nn > 0)
    return _CACHE[k]


def occ(db, t, c, v):
    cur = con(db)
    if v is None:
        return cur.execute(f'SELECT COUNT(*) FROM {q(t)} WHERE {q(c)} IS NULL').fetchone()[0]
    return cur.execute(f'SELECT COUNT(*) FROM {q(t)} WHERE {q(c)} = ?', (v,)).fetchone()[0]


def show(v):
    return 'NULL' if v is None else repr(v)[:50]


def facts(db, it, cols):
    out = ['**Facts from the real (official) database** (generated mechanically; the same kinds of facts for every item):\n']
    for t, tv in it['witness'].items():
        ref = [(j, c) for j, c in enumerate(tv['columns']) if (t.lower(), c.lower()) in cols]
        if not ref:
            continue
        n_real = con(db).execute(f'SELECT COUNT(*) FROM {q(t)}').fetchone()[0]
        for j, c in ref:
            n, nnull, nd, uniq = col_stats(db, t, c)
            vals = Counter(r[j] for r in tv['rows'])
            vs = '; '.join(f'{show(v)} occurs {occ(db, t, c, v):,}x' for v in list(vals)[:6])
            more = f' (+{len(vals) - 6} more)' if len(vals) > 6 else ''
            out.append(f'- `{t}.{c}`: {n:,} rows, {nnull:,} NULL, {nd:,} distinct values'
                       f"{', all non-NULL values unique' if uniq else ''}. Witness values: {vs}{more}.")
        if 0 < n_real <= 15:
            names = [c for _, c in ref]
            rows = con(db).execute(f"SELECT {', '.join(q(c) for c in names)} FROM {q(t)}").fetchall()
            out.append(f'- Real content of `{t}` ({n_real} rows; referenced columns): '
                       + '; '.join('(' + ', '.join(show(v) for v in r) + ')' for r in rows) + '.')
    return '\n'.join(out) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--seed', type=int, default=20261021)
    a = ap.parse_args()
    used = {(k['pair_id'], k['source']) for k in json.load(open(os.path.join(
        ROOT, 'results', 'audit', 'human_validation', 'key_DO_NOT_OPEN_BEFORE_ANNOTATING.json')))}
    rng = random.Random(a.seed)
    s1 = [x for x in final('test_v4') if (x['item']['pair_id'], x['source']) not in used]
    s2 = [x for x in final('test_r') if (x['item']['pair_id'], x['source']) not in used]
    pick = rng.sample(s1, 30) + rng.sample(s2, 30)
    rng.shuffle(pick)
    pairs = {p['pair_id']: p for p in load_pairs('test')}
    os.makedirs(a.out, exist_ok=True)
    key, md = [], ['# Human attribution sheet, round 2 (blind)\n',
                   'For each item, read the question, evidence, both queries, the witness database, the two results and the '
                   'facts from the real database, then replace `____` after **Verdict:** with exactly one of: '
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
        md.append(facts(it['db_id'], it, cols))
        md.append('**Verdict:** ____  \n**Reason (one sentence):** \n')
    open(os.path.join(a.out, 'sheet_blind.md'), 'w').write('\n'.join(md))
    json.dump(key, open(os.path.join(a.out, 'key_DO_NOT_OPEN_BEFORE_ANNOTATING.json'), 'w'), indent=1)
    print('wrote', len(pick), 'items', Counter(k['source'].split('@')[0] for k in key))


if __name__ == '__main__':
    main()
