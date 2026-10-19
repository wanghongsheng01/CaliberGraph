"""Mine data-profile constraints (admissibility tier R) from the official BIRD databases.

For every database and every table/column of the DDL, with standard data-profiling queries:
  * column domains: NULL allowed?, numeric range and integrality, observed distinct values
    (stored when <= MAX_DOMAIN distinct), lexical shapes, letter-case styles and surrounding
    whitespace of text values, lexicographic range of temporal text;
  * unique column combinations (UCC) of size 1 (any column) and 2 (key-like / discrete columns);
  * inclusion dependencies: undeclared foreign keys (same-named columns into a unique column),
    total participation of a parent in a (declared or undeclared) foreign key, symmetric and
    irreflexive self-relations (two foreign keys to the same column);
  * lookup tables (<= 200 rows, <= 3 columns, referenced by a foreign key): content is fixed;
  * year/date agreement (an integer 'year' column equal to the year of a date column).
Output: data/official/profile_R.json

Usage: python mine_profile.py ../data/official/dev_databases
"""
import json
import os
import re
import sqlite3
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from cgx.certify import SchemaInfo, shape, TEMPORAL_NAME  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
MAX_DOMAIN = 5000      # store the full distinct-value set up to this size
MAX_SHAPES = 50        # more distinct shapes than this = free text (no shape constraint)
MIN_ROWS_UCC = 20
LOOKUP_ROWS, LOOKUP_COLS = 200, 3
GENERIC_NAMES = {'id', 'name', 'type', 'code', 'date', 'value', 'text', 'title', 'number', 'description', 'year'}


def q(x):
    return '"' + x.replace('"', '""') + '"'


def case_style(v):
    letters = re.sub(r'[^A-Za-zÀ-ɏ]', '', v)
    if not letters:
        return 'none'
    if letters.islower():
        return 'lower'
    if letters.isupper():
        return 'upper'
    return 'mixed'


def norm(n):
    return re.sub(r'[^a-z0-9]', '', n.lower())


def is_int(v):
    return isinstance(v, int) or (isinstance(v, float) and v.is_integer())


def mine_db(path, schema: SchemaInfo):
    con = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    P = dict(tables={}, ucc=[], ind_fk=[], ind_total=[], symmetric=[], irreflexive=[], lookup={}, year_date=[])
    nrows = {}
    dvals = {}
    for t, tinfo in schema.tables.items():
        n = con.execute(f'SELECT COUNT(*) FROM {q(t)}').fetchone()[0]
        nrows[t] = n
        cols = {}
        for c in tinfo['columns']:
            cn = c['name']
            vals = Counter()
            nnull = 0
            for (v,) in con.execute(f'SELECT {q(cn)} FROM {q(t)}'):
                if v is None:
                    nnull += 1
                else:
                    vals[v] += 1
            info = dict(n=n, n_null=nnull, n_distinct=len(vals))
            nums = [v for v in vals if isinstance(v, (int, float)) and not isinstance(v, bool)]
            texts = [v for v in vals if isinstance(v, str)]
            if nums:
                info['num_min'], info['num_max'] = min(nums), max(nums)
                info['num_int'] = all(is_int(v) for v in nums)
            info['num_share'] = sum(vals[v] for v in nums) / max(1, sum(vals.values()))
            if texts:
                shp = Counter()
                cs = Counter()
                ws = 0
                for v in texts:
                    shp[shape(v)] += vals[v]
                    cs[case_style(v)] += vals[v]
                    if v != v.strip():
                        ws += vals[v]
                tot = sum(vals[v] for v in texts)
                info['shapes'] = [s for s, _ in shp.most_common(MAX_SHAPES)] if len(shp) <= MAX_SHAPES else None
                info['case_styles'] = sorted(k for k, v in cs.items() if v / tot >= 0.001)
                info['ws_ok'] = ws / tot >= 0.001
                if c['temporal'] is not None or TEMPORAL_NAME.search(cn):
                    info['text_min'], info['text_max'] = min(texts), max(texts)
            if len(vals) <= MAX_DOMAIN:
                info['domain'] = sorted(vals, key=lambda v: (-vals[v], str(v)))
            else:
                info['top'] = [v for v, _ in vals.most_common(200)]
            cols[cn] = info
            if not texts or sum(len(v) for v in texts[:2000]) / min(len(texts), 2000) <= 64:
                dvals[(t, cn)] = set(vals)
        P['tables'][t] = dict(n=n, columns=cols)
    print('  domains done', flush=True)
    # ---- unary UCC and key-like columns
    unique1 = {}
    for t, tinfo in schema.tables.items():
        for c in tinfo['columns']:
            i = P['tables'][t]['columns'][c['name']]
            nn = i['n'] - i['n_null']
            unique1[(t, c['name'])] = nn >= MIN_ROWS_UCC and i['n_distinct'] == nn
            if unique1[(t, c['name'])] and not (c['pk'] and sum(x['pk'] > 0 for x in tinfo['columns']) == 1):
                P['ucc'].append([t, [c['name']]])
    # ---- declared and undeclared foreign keys
    fks = []
    for t, tinfo in schema.tables.items():
        for fk in tinfo['fks']:
            p = fk['ref_table_resolved']
            if p and len(fk['from_cols']) == 1 and fk['to_cols'] and fk['to_cols'][0]:
                fks.append((t, fk['from_cols'][0], p, fk['to_cols'][0], True))
    declared = {(a, b, c, d) for a, b, c, d, _ in fks}
    for t, tinfo in schema.tables.items():
        for c in tinfo['columns']:
            for p, pinfo in schema.tables.items():
                if p == t:
                    continue
                for pc in pinfo['columns']:
                    if norm(c['name']) in GENERIC_NAMES:
                        continue
                    if norm(pc['name']) != norm(c['name']) or not (unique1[(p, pc['name'])] or
                                                                     (pc['pk'] and sum(x['pk'] > 0 for x in pinfo['columns']) == 1)):
                        continue
                    if (t, c['name'], p, pc['name']) in declared:
                        continue
                    if (t, c['name']) not in dvals or (p, pc['name']) not in dvals:
                        continue
                    bad = len(dvals[(t, c['name'])] - dvals[(p, pc['name'])])
                    nn = nrows[t] - P['tables'][t]['columns'][c['name']]['n_null']
                    if bad == 0 and nn > 0:
                        fks.append((t, c['name'], p, pc['name'], False))
                        P['ind_fk'].append([t, c['name'], p, pc['name']])
    # ---- lookup tables
    referenced = {p for _, _, p, _, _ in fks}
    for t, tinfo in schema.tables.items():
        if nrows[t] <= LOOKUP_ROWS and len(tinfo['columns']) <= LOOKUP_COLS and t in referenced:
            P['lookup'][t] = [list(r) for r in con.execute(f'SELECT {", ".join(q(c["name"]) for c in tinfo["columns"])} FROM {q(t)}')]
    # ---- total participation (every parent row has a child), not for lookup parents
    for t, c, p, pc, decl in fks:
        if p in P['lookup'] or nrows[p] < MIN_ROWS_UCC:
            continue
        if (p, pc) not in dvals or (t, c) not in dvals:
            continue
        missing = len(dvals[(p, pc)] - dvals[(t, c)])
        if missing == 0:
            P['ind_total'].append([p, pc, t, c])
    # ---- symmetric / irreflexive self-relations
    by_t = {}
    for t, c, p, pc, _ in fks:
        by_t.setdefault((t, p, pc), []).append(c)
    for (t, p, pc), cs in by_t.items():
        cs = sorted(set(cs))
        for i in range(len(cs)):
            for j in range(i + 1, len(cs)):
                a, b = cs[i], cs[j]
                pairs = {(x, y) for x, y in con.execute(f'SELECT {q(a)}, {q(b)} FROM {q(t)}') if x is not None and y is not None}
                if pairs and all((y, x) in pairs for x, y in pairs):
                    P['symmetric'].append([t, a, b])
                if pairs and all(x != y for x, y in pairs):
                    P['irreflexive'].append([t, a, b])
    print('  inds done', flush=True)
    # ---- binary UCC over key-like / discrete columns
    for t, tinfo in schema.tables.items():
        if nrows[t] < MIN_ROWS_UCC or t in P['lookup']:
            continue
        fkcols = {c for tt, c, _, _, _ in fks if tt == t}
        pkc = [c['name'] for c in tinfo['columns'] if c['pk'] > 0]
        cand = []
        for c in tinfo['columns']:
            cn = c['name']
            i = P['tables'][t]['columns'][cn]
            if unique1[(t, cn)] or (len(pkc) == 1 and cn in pkc):
                continue
            if cn in fkcols or cn in pkc or i['n_distinct'] <= 0.5 * nrows[t]:
                cand.append(cn)
        cand = cand[:40]
        for i in range(len(cand)):
            for j in range(i + 1, len(cand)):
                a, b = cand[i], cand[j]
                if sorted([a, b]) == sorted(pkc):
                    continue
                d = con.execute(f'SELECT 1 FROM {q(t)} WHERE {q(a)} IS NOT NULL AND {q(b)} IS NOT NULL '
                                f'GROUP BY {q(a)}, {q(b)} HAVING COUNT(*) > 1 LIMIT 1').fetchone()
                if d is None:
                    P['ucc'].append([t, [a, b]])
    # ---- year agrees with a date column
    for t, tinfo in schema.tables.items():
        for yc in tinfo['columns']:
            if not re.fullmatch(r'(?i)year', yc['name']):
                continue
            for dc in tinfo['columns']:
                if dc is yc or not (dc['temporal'] is not None or TEMPORAL_NAME.search(dc['name'])):
                    continue
                bad = con.execute(f'SELECT COUNT(*) FROM {q(t)} WHERE {q(dc["name"])} IS NOT NULL AND {q(yc["name"])} IS NOT NULL '
                                  f'AND CAST(substr({q(dc["name"])}, 1, 4) AS INTEGER) <> {q(yc["name"])}').fetchone()[0]
                nn = con.execute(f'SELECT COUNT(*) FROM {q(t)} WHERE {q(dc["name"])} IS NOT NULL').fetchone()[0]
                if bad == 0 and nn > 0:
                    P['year_date'].append([t, yc['name'], dc['name']])
    con.close()
    return P


def main(root):
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    out = {}
    for db in sorted(ddl):
        p = os.path.join(root, db, f'{db}.sqlite')
        if not os.path.exists(p):
            continue
        t0 = time.time()
        out[db] = mine_db(p, SchemaInfo(ddl[db]))
        P = out[db]
        print(db, f'{time.time() - t0:.0f}s', 'ucc', len(P['ucc']), 'fk+', len(P['ind_fk']), 'total', len(P['ind_total']),
              'sym', len(P['symmetric']), 'irr', len(P['irreflexive']), 'lookup', list(P['lookup']), 'yd', P['year_date'], flush=True)
    json.dump(out, open(os.path.join(ROOT, 'data', 'official', 'profile_R.json'), 'w'), default=str)


if __name__ == '__main__':
    main(sys.argv[1])
