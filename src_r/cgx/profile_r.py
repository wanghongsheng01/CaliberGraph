"""Admissibility tier R: data-profile constraints mined from the official database
(see mine_profile.py). Standard library only, so the certifier and every baseline can use it.

A witness is R-admissible if every value lies in its column's observed domain (NULL only where the
official column has NULLs; numbers within the observed range and integrality; text in the observed
value set, or with an observed lexical shape, letter case and no unobserved surrounding
whitespace; temporal text within the observed range), lookup tables hold only official rows, and
the mined unique column combinations, inclusion dependencies (undeclared foreign keys, total
participation), symmetric / irreflexive self-relations and year/date agreements hold.
Key columns (primary-key or foreign-key columns) may hold new identifiers of the observed type.
"""
import re
import sqlite3

from .certify import shape, _col_resolve, TEMPORAL_NAME
from .certify import SchemaInfo  # noqa: F401  (type reference)


def case_style(v):
    letters = re.sub(r'[^A-Za-zÀ-ɏ]', '', v)
    if not letters:
        return 'none'
    if letters.islower():
        return 'lower'
    if letters.isupper():
        return 'upper'
    return 'mixed'


_CON = sqlite3.connect(':memory:')


def _k(v):
    """Mapping key: numbers and their text forms compare equal (JSON keeps both as values)."""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return repr(v) if not isinstance(v, str) else v


def as_affinity(v, aff):
    """Value as SQLite stores it in a column of the given affinity."""
    if v is None or isinstance(v, bytes):
        return v
    if aff == 'TEXT':
        return v if isinstance(v, str) else _CON.execute('SELECT CAST(? AS TEXT)', (v,)).fetchone()[0]
    if aff in ('INTEGER', 'NUMERIC', 'REAL') and isinstance(v, str):
        _CON.execute('CREATE TABLE IF NOT EXISTS _a (i INTEGER, n NUMERIC, r REAL)')
        _CON.execute('DELETE FROM _a')
        col = {'INTEGER': 'i', 'NUMERIC': 'n', 'REAL': 'r'}[aff]
        _CON.execute(f'INSERT INTO _a ({col}) VALUES (?)', (v,))
        return _CON.execute(f'SELECT {col} FROM _a').fetchone()[0]
    if aff == 'REAL' and isinstance(v, int) and not isinstance(v, bool):
        return float(v)
    return v


class ProfileR:
    def __init__(self, P, schema):
        self.s = schema
        self.P = P
        self.col = {}
        self.dom = {}
        for t, ti in P['tables'].items():
            tt = schema.table(t)
            if tt is None:
                continue
            for cn, info in ti['columns'].items():
                i = _col_resolve(tt['columns'], cn)
                if i is None:
                    continue
                key = (tt['name'], tt['columns'][i]['name'])
                self.col[key] = info
                if info.get('domain') is not None:
                    self.dom[key] = set(info['domain'])

        def T(t):
            x = schema.table(t)
            return x['name'] if x else None

        def C(t, c):
            x = schema.table(t)
            if x is None:
                return None
            i = _col_resolve(x['columns'], c)
            return x['columns'][i]['name'] if i is not None else None
        self.T, self.C = T, C
        # unique column combinations: only over identifier-like columns; a measure (real number,
        # date/time, or a many-valued integer that is not a code) is unique only by accident
        def measure(t, c):
            tt = schema.table(t)
            if tt is None or c is None:
                return True
            ci = next((x for x in tt['columns'] if x['name'] == c), None)
            info = self.col.get((tt['name'], c)) or {}
            if ci is None:
                return True
            if ci['temporal'] is not None or TEMPORAL_NAME.search(c):
                return True
            if ci['affinity'] in ('REAL', 'NUMERIC'):
                return True
            if ci['affinity'] == 'INTEGER' and info.get('n_distinct', 0) > 50 and \
                    not re.search(r'(?i)(id|code|year|num|number|round|no|rank|position|season|stage|type)$', c):
                return True
            return False
        ucc = [(T(t), [C(t, c) for c in cs]) for t, cs in P['ucc'] if T(t)]
        self.ucc = [(t, cs) for t, cs in ucc if None not in cs and not any(measure(t, c) for c in cs)]
        # categorical columns: values must be observed ones (few distinct values, or heavily repeated)
        self.categorical = set()
        for key, info in self.col.items():
            nd = info.get('n_distinct', 0)
            nn = info.get('n', 0) - info.get('n_null', 0)
            if key not in self.dom:
                continue
            numeric = info.get('num_share', 0) > 0.5
            if (numeric and nd <= 20) or (not numeric and (nd <= 100 or nd <= 0.01 * nn)):
                self.categorical.add(key)
        self.ind_fk = [(T(a), C(a, b), T(c), C(c, d)) for a, b, c, d in P['ind_fk'] if T(a) and T(c)]
        self.ind_total = [(T(a), C(a, b), T(c), C(c, d)) for a, b, c, d in P['ind_total'] if T(a) and T(c)]
        self.symmetric = [(T(t), C(t, a), C(t, b)) for t, a, b in P['symmetric'] if T(t)]
        self.irreflexive = [(T(t), C(t, a), C(t, b)) for t, a, b in P['irreflexive'] if T(t)]
        self.year_date = [(T(t), C(t, y), C(t, d)) for t, y, d in P['year_date'] if T(t)]
        # value dependencies (profile_FD.json): x -> y mappings within a table, and child.x = parent.y
        self.fd = []
        for kind in ('fd', 'map11'):
            for t, x, y, pairs in P.get(kind, []):
                if T(t) and C(t, x) and C(t, y):
                    self.fd.append((T(t), C(t, x), C(t, y), {_k(a): b for a, b in pairs}))
        self.cross = [(T(t), C(t, x), C(t, b), T(p), C(p, y), C(p, d)) for t, x, b, p, y, d in P.get('cross', [])
                      if T(t) and T(p) and C(t, x) and C(p, y)]
        self.lookup = {}
        for t, rows in P['lookup'].items():
            if T(t):
                self.lookup[T(t)] = {tuple(r) for r in rows}
        self.lookup_rows = {T(t): [list(r) for r in rows] for t, rows in P['lookup'].items() if T(t)}
        self.keycols = set()
        for t, tinfo in schema.tables.items():
            for c in tinfo['columns']:
                if c['pk'] > 0:
                    self.keycols.add((t, c['name']))
            for fk in tinfo['fks']:
                for a, b in zip(fk['from_cols'], fk['to_cols']):
                    self.keycols.add((t, a))
                    if fk['ref_table_resolved'] and b:
                        self.keycols.add((fk['ref_table_resolved'], b))
        for a, b, c, d in self.ind_fk:
            self.keycols.add((a, b))
            self.keycols.add((c, d))

    # ------------------------------------------------------------------ single values
    def value_ok(self, t, c, v):
        info = self.col.get((t, c))
        if info is None:
            return True
        if v is None:
            return info['n_null'] > 0
        tt = self.s.tables[t]
        cinfo = next(x for x in tt['columns'] if x['name'] == c)
        v = as_affinity(v, cinfo['affinity'])
        if (t, c) in self.keycols:
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                if info.get('num_int') and not float(v).is_integer():
                    return False
                lo = info.get('num_min')
                return lo is None or v >= min(lo, 1)
            if isinstance(v, str):
                shp = info.get('shapes')
                if (t, c) in self.dom and v in self.dom[(t, c)]:
                    return True
                return shp is None or shape(v) in shp
            return True
        if (t, c) in self.categorical:
            return v in self.dom[(t, c)]
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if 'num_min' not in info:
                return False
            if info.get('num_int') and not float(v).is_integer():
                return False
            return info['num_min'] <= v <= info['num_max']
        if isinstance(v, str):
            shp = info.get('shapes')
            if shp is not None and shape(v) not in shp:
                return False
            cs = info.get('case_styles')
            if cs is not None and case_style(v) not in cs:
                return False
            if not info.get('ws_ok', True) and v != v.strip():
                return False
            if 'text_min' in info and not (info['text_min'][:len(v)] <= v <= info['text_max'] + '￿'):
                return False
            return True
        return True

    # ------------------------------------------------------------------ whole witness
    def violations(self, w, only=None):
        """w: table -> list of rows (column order of the DDL). Returns a list of violation strings.
        only: optional set of lower-cased (table, column) pairs; then only constraints involving these
        columns are checked (tier Rq: the columns referenced by either query)."""
        out = []
        cols = {t: [c['name'] for c in self.s.tables[t]['columns']] for t in w}

        def inq(t, *cs):
            return only is None or any((t.lower(), c.lower()) in only for c in cs)
        for t, rows in w.items():
            for r in rows:
                for c, v in zip(cols[t], r):
                    if inq(t, c) and not self.value_ok(t, c, v):
                        out.append(f'value {t}.{c}={v!r}')
            if t in self.lookup and inq(t, *cols[t]):
                for r in rows:
                    if tuple(r) not in self.lookup[t]:
                        out.append(f'lookup {t} row {r!r}')

        def vals(t, c):
            if t not in w:
                return None
            i = cols[t].index(c)
            return [r[i] for r in w[t]]
        for t, cs in self.ucc:
            if t not in w or None in cs or not inq(t, *cs):
                continue
            idx = [cols[t].index(c) for c in cs]
            seen = set()
            for r in w[t]:
                k = tuple(r[i] for i in idx)
                if any(x is None for x in k):
                    continue
                if k in seen:
                    out.append(f'ucc {t}{tuple(cs)}={k!r}')
                    break
                seen.add(k)
        for a, b, c, d in self.ind_fk:
            if not (inq(a, b) or inq(c, d)):
                continue
            ch = vals(a, b)
            if not ch:
                continue
            par = set(vals(c, d) or [])
            for x in ch:
                if x is not None and x not in par:
                    out.append(f'fk {a}.{b}={x!r} not in {c}.{d}')
                    break
        for a, b, c, d in self.ind_total:  # every parent a.b has a child c.d
            if not (inq(a, b) or inq(c, d)):
                continue
            par = vals(a, b)
            if not par:
                continue
            ch = set(vals(c, d) or [])
            for x in par:
                if x is not None and x not in ch:
                    out.append(f'total {a}.{b}={x!r} has no {c}.{d}')
                    break
        for t, a, b in self.symmetric:
            if t not in w or not inq(t, a, b):
                continue
            ia, ib = cols[t].index(a), cols[t].index(b)
            pairs = {(r[ia], r[ib]) for r in w[t]}
            for x, y in pairs:
                if x is not None and y is not None and (y, x) not in pairs:
                    out.append(f'symmetric {t}({a},{b})=({x!r},{y!r})')
                    break
        for t, a, b in self.irreflexive:
            if t not in w or not inq(t, a, b):
                continue
            ia, ib = cols[t].index(a), cols[t].index(b)
            for r in w[t]:
                if r[ia] is not None and r[ia] == r[ib]:
                    out.append(f'irreflexive {t}({a},{b})={r[ia]!r}')
                    break
        for t, x, y, m in self.fd:
            if t not in w or not inq(t, x, y):
                continue
            ix, iy = cols[t].index(x), cols[t].index(y)
            for r in w[t]:
                k = _k(r[ix])
                if r[ix] is not None and k in m and m[k] != r[iy] and not (m[k] is not None and r[iy] is not None
                                                                            and str(m[k]) == str(r[iy])):
                    out.append(f'fd {t}.{x}={r[ix]!r} -> {y}={r[iy]!r} (official {m[k]!r})')
                    break
        for t, x, b, p, y, d in self.cross:
            if t not in w or p not in w or not (inq(t, x) or inq(p, y)):
                continue
            ix, ib = cols[t].index(x), cols[t].index(b)
            iy, idd = cols[p].index(y), cols[p].index(d)
            par = {}
            for r in w[p]:
                par.setdefault(r[idd], []).append(r[iy])
            for r in w[t]:
                ys = par.get(r[ib])
                if ys and r[ix] is not None and any(v is not None and v != r[ix] for v in ys):
                    out.append(f'cross {t}.{x}={r[ix]!r} vs {p}.{y}={ys[0]!r}')
                    break
        for t, y, d in self.year_date:
            if t not in w or not inq(t, y, d):
                continue
            iy, idd = cols[t].index(y), cols[t].index(d)
            for r in w[t]:
                if r[iy] is None or r[idd] is None:
                    continue
                try:
                    if int(str(r[idd])[:4]) != int(r[iy]):
                        out.append(f'year_date {t}.{y}={r[iy]!r} vs {d}={r[idd]!r}')
                        break
                except ValueError:
                    out.append(f'year_date {t}.{d}={r[idd]!r}')
                    break
        return out

    def ok(self, w, only=None):
        return not self.violations(w, only)
