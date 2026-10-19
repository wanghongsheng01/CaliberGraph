"""Random real rows per table from the official BIRD databases (seeded), used as row templates by
the R-tier generators so that columns the queries do not touch hold real, mutually consistent
values. Output: data/official/sample_rows.json {db: {table: [rows in DDL column order]}}

Usage: python sample_rows.py ../data/official/dev_databases
"""
import json
import os
import random
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(__file__))
from cgx.certify import SchemaInfo  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
N = 60


def q(x):
    return '"' + x.replace('"', '""') + '"'


def main(root):
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    out = {}
    for db in sorted(ddl):
        p = os.path.join(root, db, f'{db}.sqlite')
        if not os.path.exists(p):
            continue
        s = SchemaInfo(ddl[db])
        con = sqlite3.connect(f'file:{p}?mode=ro', uri=True)
        rng = random.Random(f'cgx-rows-{db}')
        out[db] = {}
        for t, ti in s.tables.items():
            cols = ', '.join(q(c['name']) for c in ti['columns'])
            mx = con.execute(f'SELECT MAX(rowid) FROM {q(t)}').fetchone()[0] or 0
            ids = sorted(rng.sample(range(1, mx + 1), min(mx, 4 * N))) if mx else []
            rows = []
            for i in range(0, len(ids), 500):
                chunk = ids[i:i + 500]
                rows += [list(r) for r in con.execute(f'SELECT {cols} FROM {q(t)} WHERE rowid IN ({",".join(map(str, chunk))})')]
            if len(rows) < N:  # sparse or non-integer rowids: seeded offsets instead
                n = con.execute(f'SELECT COUNT(*) FROM {q(t)}').fetchone()[0]
                offs = sorted(rng.sample(range(n), min(n, N)))
                rows = [list(con.execute(f'SELECT {cols} FROM {q(t)} LIMIT 1 OFFSET {o}').fetchone()) for o in offs]
            rng.shuffle(rows)
            out[db][t] = rows[:N]
        con.close()
        print(db, {t: len(v) for t, v in out[db].items()}, flush=True)
    json.dump(out, open(os.path.join(ROOT, 'data', 'official', 'sample_rows.json'), 'w'), default=str)


if __name__ == '__main__':
    main(sys.argv[1])
