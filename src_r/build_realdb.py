"""Indexed read-only copies of the official BIRD databases for fast row retrieval by CaliberGraph-R
and the real-row baselines. Indexes: key columns (primary/foreign keys, mined undeclared foreign
keys) and every column referenced by any benchmark query. Indexes change speed only, never results.
Output: data/official/indexed/<db>.sqlite

Usage: python build_realdb.py ../data/official/dev_databases
"""
import json
import os
import sqlite3
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from cgx.certify import SchemaInfo  # noqa: E402
from cgx.sqlinfo import Analyzer  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')


def q(x):
    return '"' + x.replace('"', '""') + '"'


def main(root):
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    P = json.load(open(os.path.join(ROOT, 'data', 'official', 'profile_R.json')))
    pairs = [json.loads(l) for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl'))]
    out_dir = os.path.join(ROOT, 'data', 'official', 'indexed')
    os.makedirs(out_dir, exist_ok=True)
    for db in sorted(ddl):
        src = os.path.join(root, db, f'{db}.sqlite')
        if not os.path.exists(src):
            continue
        t0 = time.time()
        s = SchemaInfo(ddl[db])
        an = Analyzer(s)
        cols = set()
        for t, ti in s.tables.items():
            for c in ti['columns']:
                if c['pk'] > 0:
                    cols.add((t, c['name']))
            for fk in ti['fks']:
                for a, b in zip(fk['from_cols'], fk['to_cols']):
                    cols.add((t, a))
                    if fk['ref_table_resolved'] and b:
                        cols.add((fk['ref_table_resolved'], b))
        for a, b, c, d in P[db]['ind_fk'] + P[db]['ind_total']:
            cols.add((s.table(a)['name'], b))
            cols.add((s.table(c)['name'], d))
        for p in pairs:
            if p['db_id'] != db:
                continue
            for sql in (p['gold'], p['pred']):
                try:
                    cols |= set(an.analyze(sql).columns)
                except Exception:  # noqa: BLE001
                    pass
        dst = os.path.join(out_dir, f'{db}.sqlite')
        if os.path.exists(dst):
            os.remove(dst)
        sc = sqlite3.connect(f'file:{src}?mode=ro', uri=True)
        dc = sqlite3.connect(dst)
        sc.backup(dc)
        sc.close()
        n = 0
        for t, c in sorted(cols):
            if s.table(t) is None:
                continue
            try:
                dc.execute(f'CREATE INDEX IF NOT EXISTS {q("cgx_" + t + "_" + c)} ON {q(t)} ({q(c)})')
                n += 1
            except sqlite3.Error as e:
                print('  skip', t, c, e)
        dc.execute('ANALYZE')
        dc.commit()
        dc.close()
        print(db, n, 'indexes', f'{time.time() - t0:.0f}s', flush=True)


if __name__ == '__main__':
    main(sys.argv[1])
