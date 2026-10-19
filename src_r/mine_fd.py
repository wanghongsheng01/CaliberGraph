"""Mine value dependencies for tier R from the official BIRD databases:
  * intra-table functional dependencies x -> y between categorical / identifier columns that hold
    exactly on the official data and are not trivial (x not unique), plus one-to-one mappings
    between two unique identifier-like text columns (e.g. a set's name and its code);
  * cross-table agreements: when a child row joins its parent through a (declared or mined)
    foreign key, a child column equals a parent column on >= 99.5% of joined rows (denormalised
    attributes such as a school's county name stored in two tables).
Mappings are stored for x values (<= MAX_MAP distinct). Output: data/official/profile_FD.json

Usage: python mine_fd.py ../data/official/dev_databases
"""
import json
import os
import sqlite3
import sys
import time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from cgx.certify import SchemaInfo, TEMPORAL_NAME  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
MAX_MAP = 5000
MAX_CAND = 30
MAX_ROWS = 200000


def q(x):
    return '"' + x.replace('"', '""') + '"'


def main(root):
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    PR = json.load(open(os.path.join(ROOT, 'data', 'official', 'profile_R.json')))
    out = {}
    for db in sorted(ddl):
        path = os.path.join(root, db, f'{db}.sqlite')
        if not os.path.exists(path):
            continue
        t0 = time.time()
        s = SchemaInfo(ddl[db])
        con = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
        prof = PR[db]['tables']
        fds, maps11, cross = [], [], []
        for t, ti in s.tables.items():
            info = prof[t]['columns']
            n = prof[t]['n']
            if n < 20:
                continue
            cand = []
            for c in ti['columns']:
                i = info[c['name']]
                nd = i['n_distinct']
                if c['temporal'] is not None or TEMPORAL_NAME.search(c['name']) or c['affinity'] == 'REAL':
                    continue
                if 2 <= nd <= MAX_MAP:
                    cand.append(c['name'])
            cand = cand[:MAX_CAND]
            if len(cand) < 2:
                continue
            idx = {c['name']: j for j, c in enumerate(ti['columns'])}
            rows = con.execute(f'SELECT {", ".join(q(c) for c in cand)} FROM {q(t)} LIMIT {MAX_ROWS}').fetchall()
            col = {c: [r[k] for r in rows] for k, c in enumerate(cand)}
            del idx
            for x in cand:
                nd_x = info[x]['n_distinct']
                nn_x = n - info[x]['n_null']
                unique_x = nd_x == nn_x
                for y in cand:
                    if y == x:
                        continue
                    unique_y = info[y]['n_distinct'] == n - info[y]['n_null']
                    if unique_x and not (unique_y and ti['columns'][[c['name'] for c in ti['columns']].index(y)]['affinity'] == 'TEXT'):
                        continue
                    m = {}
                    ok = True
                    for a, b in zip(col[x], col[y]):
                        if a is None:
                            continue
                        if a in m:
                            if m[a] != b:
                                ok = False
                                break
                        else:
                            m[a] = b
                    if ok and len(m) >= 2:
                        if unique_x:
                            maps11.append([t, x, y, [[k, v] for k, v in m.items()]])
                        else:
                            fds.append([t, x, y, [[k, v] for k, v in m.items()]])
        # cross-table agreements along foreign keys
        links = []
        for t, ti in s.tables.items():
            for fk in ti['fks']:
                p = fk['ref_table_resolved']
                if p and len(fk['from_cols']) == 1 and fk['to_cols'] and fk['to_cols'][0]:
                    links.append((t, fk['from_cols'][0], p, fk['to_cols'][0]))
        for a, b, c, d in PR[db]['ind_fk']:
            links.append((s.table(a)['name'], b, s.table(c)['name'], d))
        for t, b, p, d in links:
            tcols = [c['name'] for c in s.tables[t]['columns'] if c['name'] != b and c['affinity'] != 'REAL']
            pcols = [c['name'] for c in s.tables[p]['columns'] if c['name'] != d and c['affinity'] != 'REAL']
            if not tcols or not pcols or t == p:
                continue
            sel = ', '.join([f'x.{q(c)}' for c in tcols] + [f'y.{q(c)}' for c in pcols])
            try:
                rows = con.execute(f'SELECT {sel} FROM {q(t)} x JOIN {q(p)} y ON x.{q(b)} = y.{q(d)} LIMIT 20000').fetchall()
            except sqlite3.Error:
                continue
            if len(rows) < 20:
                continue
            k = len(tcols)
            for i, x in enumerate(tcols):
                for j, y in enumerate(pcols):
                    both = [(r[i], r[k + j]) for r in rows if r[i] is not None and r[k + j] is not None]
                    if len(both) < 20:
                        continue
                    eq = sum(1 for u, v in both if u == v)
                    if eq >= 0.995 * len(both) and len({u for u, _ in both}) >= 2:
                        cross.append([t, x, b, p, y, d])
        con.close()
        out[db] = dict(fd=fds, map11=maps11, cross=cross)
        print(db, f'{time.time() - t0:.0f}s', 'fd', len(fds), 'map11', len(maps11), 'cross', len(cross),
              [(c[0], c[1], c[3], c[4]) for c in cross][:6], flush=True)
    json.dump(out, open(os.path.join(ROOT, 'data', 'official', 'profile_FD.json'), 'w'), default=str)


if __name__ == '__main__':
    main(sys.argv[1])
