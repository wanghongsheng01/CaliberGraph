"""Independently recompute BIRD execution accuracy (EX) on the official development databases.

Follows the official BIRD evaluator: execute predicted and gold SQL on the database, the
prediction is correct iff set(pred_rows) == set(gold_rows); errors and time-outs are incorrect.
Writes data/ex_recomputed.json {pair_id: 'correct'|'incorrect'|'timeout'|'error'} and prints the
agreement with the EX labels released by the SpotIt+ authors.

Usage: python recompute_ex.py /path/to/dev_databases [--timeout 30] [--procs 2]
"""
import argparse
import json
import multiprocessing as mp
import os
import sqlite3
import time
from collections import Counter

ROOT = os.path.join(os.path.dirname(__file__), '..')
_DB = {}


def run(sql, con, timeout):
    dl = time.monotonic() + timeout
    con.set_progress_handler(lambda: 1 if time.monotonic() > dl else 0, 10000)
    try:
        return 'ok', con.execute(sql).fetchall()
    except sqlite3.OperationalError as e:
        return ('timeout' if 'interrupted' in str(e) else 'error'), str(e)
    except Exception as e:  # noqa: BLE001
        return 'error', str(e)
    finally:
        con.set_progress_handler(None, 0)


def work(args):
    row, root, timeout = args
    db = row['db_id']
    if db not in _DB:
        _DB[db] = sqlite3.connect(f'file:{os.path.join(root, db, db + ".sqlite")}?mode=ro', uri=True)
    con = _DB[db]
    sg, rg = run(row['gold'], con, timeout)
    sp, rp = run(row['pred'], con, timeout)
    if sg != 'ok':
        return row['pair_id'], f'gold_{sg}'
    if sp != 'ok':
        return row['pair_id'], sp
    return row['pair_id'], 'correct' if set(rp) == set(rg) else 'incorrect'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--timeout', type=float, default=30.0)
    ap.add_argument('--procs', type=int, default=2)
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl'))]
    rows = [r for r in rows if r['source'] != 'parseval_model'
            and os.path.exists(os.path.join(a.root, r['db_id'], r['db_id'] + '.sqlite'))]
    out = {}
    with mp.Pool(a.procs) as pool:
        for i, (k, v) in enumerate(pool.imap_unordered(work, [(r, a.root, a.timeout) for r in rows], chunksize=20)):
            out[k] = v
            if (i + 1) % 1000 == 0:
                print(i + 1, flush=True)
    os.makedirs(os.path.join(ROOT, 'data', 'official'), exist_ok=True)
    prev = os.path.join(ROOT, 'data', 'official', 'ex_recomputed.json')
    if os.path.exists(prev):
        old = json.load(open(prev))
        old.update(out)
        out_all = old
    else:
        out_all = out
    json.dump(out_all, open(prev, 'w'))
    agree = Counter()
    for r in rows:
        mine = 'correct' if out[r['pair_id']] == 'correct' else 'incorrect'
        agree[(r['ex'], mine)] += 1
    print('released x recomputed:', dict(agree))
    print('agreement', sum(v for (x, y), v in agree.items() if x == y) / len(rows))


if __name__ == '__main__':
    main()
