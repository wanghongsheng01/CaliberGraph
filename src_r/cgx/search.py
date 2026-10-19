"""CGX: diff-anchored, masking-isolating witness synthesis over the query join graph.

Given a schema and a (gold, predicted) SQL pair, search for a small database, valid under the
declared DDL and type-faithful (protocol tier L1), on which the two queries return different
results under the BIRD set contract. Every candidate is executed by the real SQLite engine, so
any reported witness is a concrete counterexample (it is re-certified independently afterwards).

Components (each can be disabled for ablation):
  * join-graph completion  (cfg.join_graph): columns equated by either query, plus FK edges,
    form union-find classes that share one value per probe tuple, so probes reach the output;
  * isolation              (cfg.isolation): start from single-probe databases and grow only by
    targeted operators (duplicate, tie, decoy), instead of multi-row random databases;
  * diff anchoring         (cfg.anchoring): columns/atoms that differ between the two queries
    receive boundary values and most of the mutation budget;
  * SQLite value domain    (cfg.sqlite_domain): boundary/case/fraction/date-format variants
    derived from literals and declared types.
"""
from __future__ import annotations

import random
import re
import sqlite3
import time
from dataclasses import dataclass, field

from .certify import SchemaInfo, qi, shape, TEMPORAL_NAME, TEMPORAL_TEXT
from .sqlinfo import Analyzer, analyze_pair


@dataclass
class Config:
    budget_s: float = 10.0
    query_timeout_s: float = 0.3
    join_graph: bool = True
    isolation: bool = True
    anchoring: bool = True
    sqlite_domain: bool = True
    realism: object = None        # optional RealismConstraints used as generation constraints (CGX+SC)
    formats: object = None        # FormatProfile: value shapes of the official DB (protocol tier L1f)
    never_null: object = None     # v5 (post-freeze, exploratory): columns never NULL in the official DB
    profile_r: object = None      # R (second freeze): ProfileR data-profile constraints of the official DB
    templates: object = None      # R: real rows per table (dict table -> rows) used as row templates
    real_src: object = None       # R: RealSource on the official database (real sub-database phase)
    real_phase: bool = True       # R ablation switch: real sub-database phase on/off
    synthetic: bool = True        # R ablation switch: synthetic probe phases (v4 machinery) on/off
    seed: int = 0
    max_rows_per_table: int = 6
    max_group_rows: int = 16


# ----------------------------------------------------------------------------- kinds & values
def col_kind(c):
    if c['temporal'] == 'date':
        return 'date'
    if c['temporal'] == 'datetime':
        return 'datetime'
    if c['temporal'] == 'time':
        return 'time'
    return {'INTEGER': 'int', 'REAL': 'real', 'NUMERIC': 'num', 'TEXT': 'text', 'BLOB': 'text'}[c['affinity']]


def coerce(v, kind):
    """Convert a literal to a type-faithful value for the column kind, or return _BAD."""
    if v is None:
        return None
    if kind == 'int':
        if isinstance(v, bool):
            return int(v)
        if isinstance(v, int):
            return v
        if isinstance(v, float):
            return int(v) if v == int(v) else _BAD
        if isinstance(v, str) and re.fullmatch(r'\s*-?\d+\s*', v):
            return int(v)
        return _BAD
    if kind in ('real', 'num'):
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return float(v) if kind == 'real' else v
        if isinstance(v, str):
            try:
                f = float(v)
                return f if kind == 'real' else (int(f) if f == int(f) and re.fullmatch(r'\s*-?\d+\s*', v) else f)
            except ValueError:
                return _BAD
        return _BAD
    if kind == 'date':
        if isinstance(v, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', v) and _valid_date(v):
            return v
        return _BAD
    if kind == 'datetime':
        if isinstance(v, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})?', v) and _valid_date(v[:10]):
            return v
        return _BAD
    if kind == 'time':
        if isinstance(v, str) and re.fullmatch(r'\d{2}:\d{2}(:\d{2})?', v):
            return v
        return _BAD
    if kind == 'tdate':  # temporal-named TEXT column without an observed format: ISO-like text
        if isinstance(v, str):
            x = v.strip()
            if re.fullmatch(r'\d{4}', x):
                x = f'{x}-01-01'
            elif re.fullmatch(r'\d{4}-\d{2}', x):
                x = f'{x}-01'
            if TEMPORAL_TEXT.match(x) and (not re.match(r'\d{4}-', x) or _valid_date(x[:10])):
                return x
        return _BAD
    # text
    if isinstance(v, float) and v == int(v):
        return str(v)
    return str(v)


_BAD = object()


def _valid_date(s):
    try:
        y, m, d = int(s[:4]), int(s[5:7]), int(s[8:10])
    except ValueError:
        return False
    if not (1 <= m <= 12 and 1 <= d <= 31 and y >= 1):
        return False
    mdays = [31, 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return d <= mdays[m - 1]


GENERIC = {
    'int': [1, 2, 3, 0, 5, 10, -1, 100],
    'real': [1.0, 2.0, 1.5, 0.0, 3.25, 10.0, -1.5, 100.0],
    'num': [1, 2, 1.5, 0, 10, 2.5],
    'text': ['a', 'b', 'c', 'A', 'x1', 'y2'],
    'date': ['2000-01-01', '2010-06-15', '2015-03-20', '1995-12-31', '2020-02-29'],
    'datetime': ['2000-01-01 00:00:00', '2010-06-15 12:30:00', '2015-03-20 08:00:00', '2020-02-29 23:59:59'],
    'time': ['00:00:00', '12:30:00', '08:15:00'],
    'tdate': ['2000-01-01', '2010-06-15 00:00:00', '2015-03-20', '2012-02-22 00:00:00'],
}


def variants(v, kind, wrapper, op, sqlite_domain=True):
    """Values for a column that make an atom on it true/false and probe its boundaries."""
    out = []
    w = wrapper or ''
    if w.startswith('strftime:') and isinstance(v, str):
        fmt = w.split(':', 1)[1] or ''
        out += _strftime_preimages(fmt, v, kind)
    elif w.startswith('substr:') and isinstance(v, str):
        try:
            st = int(w.split(':')[1])
        except ValueError:
            st = 1
        if kind in ('date', 'datetime') and st == 1 and re.fullmatch(r'\d{4}', v):
            out += [f'{v}-01-01', f'{v}-12-31', f'{v}-06-15 10:00:00']
        elif kind in ('date', 'datetime') and st == 6 and re.fullmatch(r'\d{2}', v):
            out += [f'2010-{v}-01', f'2010-{v}-15 10:00:00']
        else:
            pad = 'x' * max(0, st - 1)
            out += [pad + v, pad + v + 'z']
    elif w.startswith(('add:', 'sub:', 'mul:', 'div:')) and isinstance(v, (int, float)):
        k = float(w.split(':')[1])
        base = {'add': v - k, 'sub': v + k, 'mul': (v / k if k else v), 'div': v * k}[w.split(':')[0]]
        out += [base, base + 1, base - 1]
        if sqlite_domain:
            out += [base + 0.5, base - 0.5]
    elif w in ('lower', 'upper', 'trim') and isinstance(v, str):
        out += [v, v.lower(), v.upper(), v.title(), ' ' + v if w == 'trim' else v]
    elif w == 'date' and isinstance(v, str):
        out += [v, v + ' 10:00:00'] if re.fullmatch(r'\d{4}-\d{2}-\d{2}', v) else [v]
    if op == 'like' and isinstance(v, str):
        base = v.replace('%', '').replace('_', 'a')
        out += [base, v.replace('%', 'x').replace('_', 'b'), base.lower(), base.upper(), 'zz' + base[:-1]]
        if kind in ('date', 'datetime') and re.fullmatch(r'\d{4}%?', v):
            out += [f'{v[:4]}-01-01', f'{v[:4]}-07-07 09:00:00']
        if kind in ('date', 'datetime') and re.fullmatch(r'\d{4}-\d{2}%?', v):
            out += [f'{v[:7]}-01', f'{v[:7]}-15 09:00:00']
    if not out:
        out.append(v)
        if isinstance(v, bool):
            pass
        elif isinstance(v, int):
            out += [v + 1, v - 1]
            if sqlite_domain:
                out += [v + 0.5, v - 0.5, float(v)]
        elif isinstance(v, float):
            out += [v + 1, v - 1]
            if sqlite_domain:
                out += [v + 0.01, v - 0.01, int(v) if v == int(v) else v]
        elif isinstance(v, str):
            if sqlite_domain:
                out += [v.lower(), v.upper(), v + ' ', v.title()]
                if re.fullmatch(r'\d{4}-\d{2}-\d{2}', v) and kind in ('datetime', 'text'):
                    out += [v + ' 00:00:00', v + ' 12:00:00']
                if re.fullmatch(r'-?\d+(\.\d+)?', v):
                    out += [str(float(v)), v + '.0']
            else:
                out += [v + 'z']
    res = []
    for x in out:
        c = coerce(x, kind)
        if c is not _BAD and c not in res:
            res.append(c)
    return res


def _strftime_preimages(fmt, v, kind):
    out = []
    if fmt == '%Y' and re.fullmatch(r'\d{4}', v):
        out = [f'{v}-01-01', f'{v}-12-31', f'{v}-06-15 10:00:00', f'{int(v) + 1}-01-01', f'{int(v) - 1}-12-31']
    elif fmt == '%m' and re.fullmatch(r'\d{2}', v):
        out = [f'2010-{v}-01', f'2011-{v}-28 10:00:00']
    elif fmt == '%d' and re.fullmatch(r'\d{2}', v):
        out = [f'2010-01-{v}', f'2010-02-{v} 10:00:00']
    elif fmt in ('%Y-%m',) and re.fullmatch(r'\d{4}-\d{2}', v):
        out = [f'{v}-01', f'{v}-28 10:00:00']
    elif fmt in ('%Y-%m-%d',) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', v):
        out = [v, v + ' 10:00:00']
    elif fmt in ('%H',) and re.fullmatch(r'\d{2}', v):
        out = [f'2010-01-01 {v}:00:00']
    elif fmt in ('%J', '%s'):
        out = []
    return out


# ----------------------------------------------------------------------------- union-find
class UF:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


# ----------------------------------------------------------------------------- evaluator
class Evaluator:
    """Fast candidate evaluation on one persistent connection (savepoint per candidate)."""

    def __init__(self, schema: SchemaInfo, gold, pred, timeout_s):
        self.schema = schema
        self.gold, self.pred = gold, pred
        self.timeout_s = timeout_s
        self.con = sqlite3.connect(':memory:', isolation_level=None)
        for s in schema.ddl:
            self.con.executescript(s)
        self.ins = {}
        for t in schema.tables.values():
            self.ins[t['name']] = f'INSERT INTO {qi(t["name"])} VALUES ({",".join("?" * len(t["columns"]))})'
        self.n_eval = 0

    def _q(self, sql):
        deadline = time.monotonic() + self.timeout_s
        self.con.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 2000)
        try:
            return True, self.con.execute(sql).fetchall()
        except Exception as e:  # noqa: BLE001
            return False, str(e)
        finally:
            self.con.set_progress_handler(None, 0)

    def eval(self, db, extra=None):
        self.n_eval += 1
        self.extra_result = None
        self.con.execute('SAVEPOINT c')
        try:
            for t, rows in db.items():
                if rows:
                    self.con.executemany(self.ins[t], rows)
        except Exception as e:  # noqa: BLE001
            self.con.execute('ROLLBACK TO c')
            self.con.execute('RELEASE c')
            return 'insert_fail', str(e), None
        okg, rg = self._q(self.gold)
        okp, rp = self._q(self.pred)
        if extra is not None and okg and okp and set(rg) != set(rp):
            try:
                self.extra_result = extra(self.con)
            except Exception as e:  # noqa: BLE001
                self.extra_result = [('extra_error', str(e))]
        self.con.execute('ROLLBACK TO c')
        self.con.execute('RELEASE c')
        if not okg:
            return 'gold_err', rg, rp
        if not okp:
            return 'pred_err', rg, rp
        return 'ok', rg, rp

    def close(self):
        self.con.close()


# ----------------------------------------------------------------------------- generator
class Generator:
    def __init__(self, schema: SchemaInfo, pair, cfg: Config, rng: random.Random):
        self.s, self.pair, self.cfg, self.rng = schema, pair, cfg, rng
        self.qtables = sorted(pair.tables)
        # relevant tables = query tables + FK-parent closure
        rel, stack = set(self.qtables), list(self.qtables)
        while stack:
            t = stack.pop()
            for fk in self.s.tables[t]['fks']:
                p = fk['ref_table_resolved']
                if p and p not in rel:
                    rel.add(p)
                    stack.append(p)
        pr = cfg.profile_r
        if pr is not None:
            # undeclared foreign keys (child -> parent) and total participation (parent -> child)
            for _ in range(3):
                new = {c for a, b, c, d in pr.ind_fk if a in rel} | {c for a, b, c, d in pr.ind_total if a in rel}
                new -= rel
                if not new:
                    break
                rel |= new
                stack = list(new)
                while stack:
                    t = stack.pop()
                    for fk in self.s.tables[t]['fks']:
                        p = fk['ref_table_resolved']
                        if p and p not in rel:
                            rel.add(p)
                            stack.append(p)
        self.rtables = sorted(rel)
        self.cols = {t: self.s.tables[t]['columns'] for t in self.rtables}
        self.colnames = {t: [c['name'] for c in self.cols[t]] for t in self.rtables}
        self.qcols = set(pair.gold.columns | pair.pred.columns)
        self._used_real = {}
        self._sat_cache = {}
        self.kind = {(t, c['name']): col_kind(c) for t in self.rtables for c in self.cols[t]}
        fp = cfg.formats
        self.col_shapes = {}
        self.col_samples = {}
        for t in self.rtables:
            for c in self.cols[t]:
                k = (t, c['name'])
                if c['affinity'] != 'TEXT':
                    continue
                if fp is not None and k in fp.shapes:
                    self.col_shapes[k] = fp.shapes[k]
                    self.col_samples[k] = fp.samples.get(k, [])
                elif c['temporal'] is None and TEMPORAL_NAME.search(c['name']):
                    self.kind[k] = 'tdate'
        nn = cfg.never_null or set()
        self.nullable = {(t, c['name']): (not c['notnull'] and c['pk'] == 0 and (t.lower(), c['name'].lower()) not in nn
                                          and (pr is None or pr.value_ok(t, c['name'], None)))
                         for t in self.rtables for c in self.cols[t]}
        self.pkcols = {t: [c['name'] for c in self.cols[t] if c['pk'] > 0] for t in self.rtables}
        # union-find classes
        self.uf = UF()
        for t in self.rtables:
            for c in self.cols[t]:
                self.uf.find((t, c['name']))
        if cfg.join_graph:
            for a, b in pair.gold.equalities + pair.pred.equalities:
                if a in self.kind and b in self.kind:
                    self.uf.union(a, b)
        # FK edges are always honoured (DDL validity); they also link join paths
        for t in self.rtables:
            for fk in self.s.tables[t]['fks']:
                p = fk['ref_table_resolved']
                if p in self.cols:
                    for a, b in zip(fk['from_cols'], fk['to_cols']):
                        if b is not None:
                            self.uf.union((t, a), (p, b))
        if pr is not None:
            for a, b, c, d in pr.ind_fk:
                if a in self.cols and c in self.cols:
                    self.uf.union((a, b), (c, d))
        self.qlinked = {x for e in pair.gold.equalities + pair.pred.equalities for x in e}
        self.classes = {}
        for k in self.kind:
            self.classes.setdefault(self.uf.find(k), []).append(k)
        self.cls_kind = {r: self._class_kind(m) for r, m in self.classes.items()}
        self.key_class = {r: any(t_c[1] in self.pkcols[t_c[0]] for t_c in m) for r, m in self.classes.items()}
        self.cls_nullable = {r: all(self.nullable[x] for x in m) for r, m in self.classes.items()}
        # atoms per class
        self.atoms = {'gold': {}, 'pred': {}}
        for side, q in (('gold', pair.gold), ('pred', pair.pred)):
            for a in q.atoms:
                if a.col in self.kind:
                    self.atoms[side].setdefault(self.uf.find(a.col), []).append(a)
        self.anchor_cls = {self.uf.find(c) for c in pair.anchor_columns if c in self.kind} if cfg.anchoring else set()
        self.lookup_keys = {}
        if pr is not None:
            for t, rows in pr.lookup_rows.items():
                if t not in self.cols:
                    continue
                pki = [i for i, c in enumerate(self.cols[t]) if c['pk'] > 0]
                if len(pki) == 1:
                    r = self.uf.find((t, self.cols[t][pki[0]]['name']))
                    self.lookup_keys[r] = [row[pki[0]] for row in rows]
        self.pools = {r: self._pool(r) for r in self.classes}
        lits = pair.gold.literals + pair.pred.literals
        self.global_lits = lits
        self._fresh = 1000
        self._rkeys = {}

    def _class_kind(self, members):
        ks = [self.kind[m] for m in members]
        for pref in ('int', 'date', 'datetime', 'time', 'tdate', 'real', 'num', 'text'):
            if pref in ks and all(k == pref or (pref in ('real', 'num') and k in ('real', 'num', 'int')) for k in ks):
                return pref
        # mixed kinds (e.g. INTEGER joined to TEXT): prefer int-like strings that satisfy both
        return 'mixed'

    def _pool(self, r):
        kind = self.cls_kind[r]
        vals = []
        atoms = self.atoms['gold'].get(r, []) + self.atoms['pred'].get(r, [])
        for a in atoms:
            for v in a.values:
                for k in ([kind] if kind != 'mixed' else ['int', 'text']):
                    for x in variants(v, k, a.wrapper, a.op, self.cfg.sqlite_domain):
                        if x not in vals:
                            vals.append(x)
        if self.cfg.realism is not None:
            vals += [x for x in self._realism_values(r) if x not in vals]
        # interpolation: a value strictly between two comparable literals of the class (e.g. a
        # birthday between '1985-01-01' and '1995-01-01'), exposing differing comparison bounds
        lits = sorted({v for a in atoms for v in a.values if isinstance(v, (int, float)) and not isinstance(v, bool)})
        for lo, hi in zip(lits, lits[1:]):
            mid = (lo + hi) / 2
            for x in (int(mid) if kind == 'int' else mid,):
                c = coerce(x, kind if kind != 'mixed' else 'int')
                if c is not _BAD and c not in vals:
                    vals.append(c)
        dts = sorted({v[:10] for a in atoms for v in a.values if isinstance(v, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}.*', v) and _valid_date(v[:10])})
        for lo, hi in zip(dts, dts[1:]):
            y = (int(lo[:4]) + int(hi[:4])) // 2
            cand = f'{y:04d}-06-15' if lo[:4] != hi[:4] else lo[:8] + '15'
            for x in (cand, cand + ' 00:00:00'):
                c = coerce(x, kind if kind != 'mixed' else 'text')
                if c is not _BAD and c not in vals and lo < x[:10] < hi:
                    vals.append(c)
        for m in self.classes[r]:
            if m in self.col_shapes:
                shp = self.col_shapes[m]
                vals = [x for x in vals if not isinstance(x, str) or shape(x) in shp]
                vals += [x for x in self.col_samples[m][:8] if x not in vals]
        if self.cfg.profile_r is not None:
            vals = [x for x in vals if self.realism_allowed(r, x)]
            if not self.key_class[r]:
                vals += [x for x in self.real_values(r, 24) if x not in vals]
        return vals

    def real_values(self, r, n):
        """Observed values of the class's columns (most frequent first) allowed for every member."""
        pr = self.cfg.profile_r
        out = []
        for t, c in self.classes[r]:
            info = pr.col.get((t, c)) or {}
            for v in (info.get('domain') or info.get('top') or [])[:400]:
                if v not in out and self.realism_allowed(r, v):
                    out.append(v)
                    if len(out) >= n:
                        return out
        return out

    def new_key(self, t, c):
        k = self.kind[(t, c)]
        return self.real_unused(t, c, k) if self.cfg.profile_r is not None else self.fresh(k)

    def real_unused(self, t, c, kind):
        """A new value for a key column: a fresh integer, or an observed text value not used yet."""
        if kind in ('int', 'num', 'real', 'mixed'):
            return self.fresh(kind)
        info = self.cfg.profile_r.col.get((t, c)) or {}
        used = self._used_real.setdefault((t, c), set())
        vals = info.get('domain') or info.get('top') or []
        for v in vals:
            if v not in used and isinstance(v, str):
                used.add(v)
                return v
        base = [v for v in vals if isinstance(v, str)]
        if base:  # a new identifier with the lexical shape of a real one (letters/digits re-drawn)
            for _ in range(20):
                v = ''.join(self.rng.choice('abcdefghijklmnopqrstuvwxyz' if ch.islower() else 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                            if ch.isalpha() else self.rng.choice('0123456789') if ch.isdigit() else ch
                            for ch in self.rng.choice(base))
                if v not in used:
                    used.add(v)
                    return v
        return self.fresh(kind)

    def fresh_class(self, r):
        kind = self.cls_kind[r]
        if self.cfg.profile_r is None or kind in ('int', 'num', 'real', 'mixed'):
            return self.fresh(kind if kind != 'mixed' else 'int')
        if r in self.lookup_keys:
            ks = self.lookup_keys[r]
            used = self._used_real.setdefault(r, set())
            for k in ks:
                if k not in used:
                    used.add(k)
                    return k
            return self.rng.choice(ks)
        t, c = sorted(self.classes[r])[0]
        for _ in range(50):
            v = self.real_unused(t, c, kind)
            if self.realism_allowed(r, v):
                return v
        return self.fresh(kind)

    def _realism_values(self, r):
        out = []
        for kind_, (t, c), arg in self.cfg.realism.items:
            if (t, c) in self.classes[r]:
                if kind_ == 'in':
                    out += [coerce(x, self.cls_kind[r] if self.cls_kind[r] != 'mixed' else 'text') for x in arg]
                elif kind_ == 'between' and isinstance(arg[0], (int, float)):
                    lo, hi = arg
                    if hi > 1e12:
                        hi = lo + 100
                    mid = (lo + hi) / 2
                    k = self.cls_kind[r]
                    out += [coerce(lo, k), coerce(hi, k), coerce(int(mid) if k == 'int' else mid, k)]
        return [x for x in out if x is not _BAD]

    def realism_keys(self, r):
        """Up to 12 key values allowed by every in/between constraint on the class."""
        if r in self._rkeys:
            return self._rkeys[r]
        kind = self.cls_kind[r]
        cands = []
        for kind_, tc, arg in self.cfg.realism.items:
            if tc in self.classes[r]:
                if kind_ == 'in':
                    cands += list(arg)
                elif kind_ == 'between' and isinstance(arg[0], (int, float)):
                    lo = int(arg[0]) if arg[0] == int(arg[0]) else arg[0]
                    cands += [lo + i for i in range(12)]
        out = []
        for v in cands:
            c = coerce(v, kind if kind != 'mixed' else 'int')
            if c is not _BAD and c is not None and c not in out and self.realism_allowed(r, c):
                out.append(c)
        self._rkeys[r] = out[:12]
        return self._rkeys[r]

    def realism_allowed(self, r, v):
        pr = self.cfg.profile_r
        if pr is not None and not all(pr.value_ok(t, c, v) for t, c in self.classes[r]):
            return False
        if self.cfg.realism is None:
            return True
        for kind_, tc, arg in self.cfg.realism.items:
            if tc not in self.classes[r]:
                continue
            if kind_ == 'not_null' and v is None:
                return False
            if v is None:
                continue
            if kind_ == 'in' and v not in arg and str(v) not in [str(a) for a in arg]:
                return False
            if kind_ == 'between':
                try:
                    if not (arg[0] <= v <= arg[1]):
                        return False
                except TypeError:
                    return False
        return True

    # ---------------------------------------------------------------- value choice
    def fresh(self, kind, i=0):
        self._fresh += 1
        n = self._fresh
        if kind in ('int', 'num', 'mixed'):
            return n
        if kind == 'real':
            return float(n)
        if kind == 'date':
            return f'{1990 + n % 30:04d}-{1 + n % 12:02d}-{1 + n % 28:02d}'
        if kind == 'datetime':
            return f'{1990 + n % 30:04d}-{1 + n % 12:02d}-{1 + n % 28:02d} 0{n % 10}:00:00'
        if kind == 'time':
            return f'{n % 24:02d}:{n % 60:02d}:00'
        if kind == 'tdate':
            return f'{1990 + n % 30:04d}-{1 + n % 12:02d}-{1 + n % 28:02d}'
        return f'v{n}'

    def satisfying(self, r, side):
        """A value making most atoms of `side` ('gold'/'pred'/'both') on class r true."""
        kind = self.cls_kind[r]
        atoms = []
        if side in ('gold', 'both'):
            atoms += self.atoms['gold'].get(r, [])
        if side in ('pred', 'both'):
            atoms += self.atoms['pred'].get(r, [])
        if not atoms:
            return _BAD
        if (r, side) in self._sat_cache:
            return self._sat_cache[(r, side)]
        cands = []
        for a in atoms:
            cands += canonical_true(a, kind if kind != 'mixed' else 'text', self.cfg.sqlite_domain)
        if self.cfg.profile_r is not None and not self.key_class[r]:
            cands += self.real_values(r, 400)
        best, bests = _BAD, -1
        for c in cands:
            if not self.realism_allowed(r, c):
                continue
            sc = sum(1 for a in atoms if approx_eval(a, c) is True)
            if sc > bests:
                best, bests = c, sc
        if self.cfg.profile_r is not None:
            self._sat_cache[(r, side)] = best
        return best

    def pick(self, r, mode, probe_idx):
        kind = self.cls_kind[r]
        if self.key_class[r]:
            # keys: distinct per probe; a filtered key (WHERE id = 5) takes its literal for probe 0
            has_atoms = bool(self.atoms['gold'].get(r) or self.atoms['pred'].get(r))
            pool = [v for v in self.pools[r] if v is not None]
            if has_atoms and pool:
                if probe_idx == 0 and mode in ('gold', 'pred', 'both'):
                    v = self.satisfying(r, mode)
                    if v is not _BAD and v is not None:
                        return v
                if mode != 'random' and probe_idx < len(pool):
                    return pool[probe_idx]
                if self.rng.random() < 0.5:
                    return self.rng.choice(pool)
            if r in self.lookup_keys:
                ks = self.lookup_keys[r]
                return ks[probe_idx % len(ks)] if mode != 'random' else self.rng.choice(ks)
            if self.cfg.realism is not None:
                ks = self.realism_keys(r)
                if ks:
                    return ks[probe_idx % len(ks)] if mode != 'random' else self.rng.choice(ks)
            if self.cfg.profile_r is not None:
                return self.fresh_class(r)
            return self.fresh(kind if kind != 'mixed' else 'int', probe_idx)
        if mode in ('gold', 'pred', 'both'):
            v = self.satisfying(r, mode)
            if v is not _BAD:
                return v
        pool = self.pools[r]
        rnd = self.rng.random()
        if pool and rnd < 0.7:
            v = self.rng.choice(pool)
        elif self.cls_nullable[r] and rnd < 0.8 and self.realism_allowed(r, None):
            v = None
        else:
            gk = kind if kind != 'mixed' else 'int'
            v = self.rng.choice(GENERIC[gk]) if self.cfg.sqlite_domain or gk != 'real' else float(self.rng.randint(0, 9))
        if not self.realism_allowed(r, v):
            alt = [x for x in pool if self.realism_allowed(r, x)]
            v = self.rng.choice(alt) if alt else v
        return v

    # ---------------------------------------------------------------- database construction
    def build(self, probes):
        """probes: list of dict class_root -> value. Returns db dict (table -> rows)."""
        db = {t: [] for t in self.rtables}
        for k, pv in enumerate(probes):
            for t in self.qtables:
                row = []
                tmpl = self.template(t, k)
                for j, c in enumerate(self.cols[t]):
                    r = self.uf.find((t, c['name']))
                    v = pv.get(r, _BAD)
                    if tmpl is not None and not self.key_class[r] and (t, c['name']) not in self.qcols \
                            and len(self.classes[r]) == 1:
                        v = tmpl[j]  # a column no query touches: real value of a real row
                    if v is _BAD:
                        v = self.pick(r, 'random', 0)
                    v = self._fit(t, c, v)
                    row.append(v)
                db[t].append(row)
        self.repair(db)
        return db

    def template(self, t, k=None):
        rows = (self.cfg.templates or {}).get(t) if self.cfg.profile_r is not None else None
        if not rows:
            return None
        return rows[k % len(rows)] if k is not None else self.rng.choice(rows)

    def _fit(self, t, c, v):
        k = self.kind[(t, c['name'])]
        if v is None and (c['notnull'] or c['pk'] or not self.nullable.get((t, c['name']), True)):
            smp = self.col_samples.get((t, c['name']))
            v = self.rng.choice(smp) if smp else self.fresh(k)
        if v is not None:
            cv = coerce(v, k)
            if cv is _BAD:
                cv = self.fresh(k)
            v = cv
        shp = self.col_shapes.get((t, c['name']))
        if shp and v is not None and shape(v) not in shp:
            smp = self.col_samples.get((t, c['name']))
            v = self.rng.choice(smp) if smp else v
        if self.cfg.realism is not None:
            r = self.uf.find((t, c['name']))
            if not self.realism_allowed(r, v):
                alt = [x for x in self.realism_keys(r) if coerce(x, k) is not _BAD]
                if alt:
                    v = coerce(self.rng.choice(alt), k)
        pr = self.cfg.profile_r
        if pr is not None and not pr.value_ok(t, c['name'], v):
            v = self.real_fix(t, c, v)
        return v

    def real_fix(self, t, c, v):
        """Closest admissible value for column (t, c): clamp numbers into the observed range, else an
        observed value."""
        pr = self.cfg.profile_r
        info = pr.col.get((t, c['name'])) or {}
        k = self.kind[(t, c['name'])]
        if (t, c['name']) in pr.keycols:
            return self.real_unused(t, c['name'], k)
        if isinstance(v, (int, float)) and not isinstance(v, bool) and 'num_min' in info:
            x = min(max(v, info['num_min']), info['num_max'])
            if info.get('num_int'):
                x = int(round(x))
            if pr.value_ok(t, c['name'], x):
                return x
        vals = info.get('domain') or info.get('top') or []
        if vals:
            return self.rng.choice(vals[:50])
        tm = self.template(t)
        if tm is not None:
            return tm[self.colnames[t].index(c['name'])]
        return v

    def repair(self, db):
        """Make the database DDL-valid: unique PKs, NOT NULL, FK parents exist (added rows),
        and every query table non-empty."""
        for t in self.rtables:
            pk = self.pkcols[t]
            if pk:
                idx = [i for i, c in enumerate(self.cols[t]) if c['name'] in pk]
                seen = set()
                keep = []
                for row in db[t]:
                    key = tuple(row[i] for i in idx)
                    if key in seen:
                        continue  # duplicate PK: drop the later row (keeps the first probe intact)
                    seen.add(key)
                    keep.append(row)
                db[t] = keep
        for _ in range(4):
            changed = False
            for t in self.rtables:
                for fk in self.s.tables[t]['fks']:
                    p = fk['ref_table_resolved']
                    if p not in db:
                        continue
                    pcols = [c['name'] for c in self.cols[p]]
                    tcols = [c['name'] for c in self.cols[t]]
                    try:
                        fi = [tcols.index(a) for a in fk['from_cols']]
                        ti = [pcols.index(b) for b in fk['to_cols']]
                    except (ValueError, TypeError):
                        continue
                    have = {tuple(r[i] for i in ti) for r in db[p]}
                    for row in db[t]:
                        key = tuple(row[i] for i in fi)
                        if any(v is None for v in key) or key in have:
                            continue
                        newrow = []
                        tmpl = self.template(p)
                        for j, c in enumerate(self.cols[p]):
                            if j in ti:
                                newrow.append(key[ti.index(j)])
                            else:
                                r = self.uf.find((p, c['name']))
                                if tmpl is not None and not self.key_class[r] and (p, c['name']) not in self.qcols:
                                    newrow.append(tmpl[j])
                                else:
                                    newrow.append(self._fit(p, c, self.pick(r, 'random', 0)))
                        # parent PK uniqueness
                        pki = [j for j, c in enumerate(self.cols[p]) if c['pk'] > 0]
                        pkeys = {tuple(r[j] for j in pki) for r in db[p]}
                        tries = 0
                        while pki and tuple(newrow[j] for j in pki) in pkeys and tries < 5:
                            for j in pki:
                                if j not in ti:
                                    newrow[j] = self.new_key(p, self.cols[p][j]['name'])
                            tries += 1
                        db[p].append(newrow)
                        have.add(key)
                        changed = True
            if not changed:
                break
        for t in self.qtables:
            if not db[t]:
                row = [self._fit(t, c, self.pick(self.uf.find((t, c['name'])), 'random', 0)) for c in self.cols[t]]
                db[t].append(row)
        if self.cfg.profile_r is not None and not getattr(self, '_in_r', False):
            self._in_r = True
            try:
                for _ in range(3):
                    if not self.repair_r(db):
                        break
                    self.repair(db)
            finally:
                self._in_r = False
        return db

    # ---------------------------------------------------------------- R-tier repair
    def _new_row(self, t, fixed):
        """A row of table t from a real template row, with fixed {col: value}; keys refreshed."""
        tm = self.template(t)
        row = []
        for j, c in enumerate(self.cols[t]):
            cn = c['name']
            if cn in fixed:
                row.append(fixed[cn])
            elif c['pk'] > 0:
                row.append(self.new_key(t, cn))
            elif tm is not None:
                row.append(tm[j])
            else:
                row.append(self._fit(t, c, self.pick(self.uf.find((t, cn)), 'random', 0)))
        return row

    def _parents_for(self, t, db):
        """For the FK columns of a new row of t: reuse an existing parent key when there is one, unless
        the column is unique in t (then a new parent key; the FK repair adds the parent row)."""
        pr = self.cfg.profile_r
        uniq = {cs[0] for tt, cs in pr.ucc if tt == t and len(cs) == 1}
        pk = [c['name'] for c in self.cols[t] if c['pk'] > 0]
        if len(pk) == 1:
            uniq.add(pk[0])
        links = []
        for fk in self.s.tables[t]['fks']:
            p = fk['ref_table_resolved']
            if p in db and len(fk['from_cols']) == 1 and fk['to_cols'] and fk['to_cols'][0] in self.colnames.get(p, []):
                links.append((fk['from_cols'][0], p, fk['to_cols'][0]))
        for a, b, c, d in pr.ind_fk:
            if a == t and c in db:
                links.append((b, c, d))
        fixed = {}
        for b, p, d in links:
            if b in fixed:
                continue
            pi = self.colnames[p].index(d)
            if b in uniq:
                usedv = {r[self.colnames[t].index(b)] for r in db.get(t, [])}
                free = [r[pi] for r in db[p] if r[pi] not in usedv]
                fixed[b] = free[0] if free else self.new_key(p, d)
            elif db[p]:
                fixed[b] = db[p][0][pi]
        return fixed

    def repair_r(self, db):
        pr = self.cfg.profile_r
        changed = False
        # lookup tables hold official rows only (same key if it exists, else remap the key)
        for t, rows in pr.lookup_rows.items():
            if t not in db or not db[t]:
                continue
            pki = [i for i, c in enumerate(self.cols[t]) if c['pk'] > 0]
            if len(pki) != 1:
                continue
            pk = pki[0]
            by_key = {r[pk]: r for r in rows}
            used = {r[pk] for r in db[t] if tuple(r) in pr.lookup[t]}
            new = []
            for r in db[t]:
                if tuple(r) in pr.lookup[t]:
                    new.append(r)
                    continue
                changed = True
                if r[pk] in by_key:
                    if r[pk] not in {x[pk] for x in new}:
                        new.append(list(by_key[r[pk]]))
                    continue
                free = [k for k in by_key if k not in used]
                if not free:
                    continue
                nk = free[0]
                used.add(nk)
                old = r[pk]
                cls = self.classes[self.uf.find((t, self.cols[t][pk]['name']))]
                for t2, c2 in cls:
                    if t2 in db and (t2, c2) != (t, self.cols[t][pk]['name']):
                        j = self.colnames[t2].index(c2)
                        for r2 in db[t2]:
                            if r2[j] == old:
                                r2[j] = nk
                new.append(list(by_key[nk]))
            db[t] = new
        # unique column combinations: change a free column of the later duplicate, else drop it
        for t, cs in pr.ucc:
            if t not in db or len(db[t]) < 2:
                continue
            idx = [self.colnames[t].index(c) for c in cs]
            seen, keep = set(), []
            for r in db[t]:
                k = tuple(r[i] for i in idx)
                if any(x is None for x in k) or k not in seen:
                    seen.add(k)
                    keep.append(r)
                    continue
                changed = True
                fixed = False
                for i in idx:
                    c = self.cols[t][i]
                    rc = self.uf.find((t, c['name']))
                    if self.key_class[rc] or rc in self.anchor_cls or (t, c['name']) in self.qlinked or len(self.classes[rc]) > 1:
                        continue
                    for v in self.real_values(rc, 60):
                        r2 = list(r)
                        r2[i] = v
                        if tuple(r2[j] for j in idx) not in seen and pr.value_ok(t, c['name'], v):
                            r[i] = v
                            fixed = True
                            break
                    if fixed:
                        break
                if fixed:
                    seen.add(tuple(r[i] for i in idx))
                    keep.append(r)
            if len(keep) != len(db[t]):
                db[t] = keep if keep else db[t][:1]
        # undeclared foreign keys: add the parent row
        for a, b, c, d in pr.ind_fk:
            if a not in db or c not in db:
                continue
            ib, idd = self.colnames[a].index(b), self.colnames[c].index(d)
            have = {r[idd] for r in db[c]}
            for r in db[a]:
                if r[ib] is not None and r[ib] not in have:
                    fixed = self._parents_for(c, db)
                    fixed[d] = r[ib]
                    db[c].append(self._new_row(c, fixed))
                    have.add(r[ib])
                    changed = True
        # total participation: every parent key has a child row
        for a, b, c, d in pr.ind_total:
            if a not in db or c not in db:
                continue
            ib, idd = self.colnames[a].index(b), self.colnames[c].index(d)
            have = {r[idd] for r in db[c]}
            for r in list(db[a]):
                if r[ib] is not None and r[ib] not in have and len(db[c]) < 4 * self.cfg.max_group_rows:
                    fixed = self._parents_for(c, db)
                    fixed[d] = r[ib]
                    db[c].append(self._new_row(c, fixed))
                    have.add(r[ib])
                    changed = True
        # symmetric and irreflexive self-relations
        for t, a, b in pr.symmetric:
            if t not in db:
                continue
            ia, ib = self.colnames[t].index(a), self.colnames[t].index(b)
            pairs = {(r[ia], r[ib]) for r in db[t]}
            for r in list(db[t]):
                if r[ia] is not None and r[ib] is not None and (r[ib], r[ia]) not in pairs:
                    r2 = list(r)
                    r2[ia], r2[ib] = r[ib], r[ia]
                    for j, c in enumerate(self.cols[t]):
                        if c['pk'] > 0 and j not in (ia, ib):
                            r2[j] = self.new_key(t, c['name'])
                    db[t].append(r2)
                    pairs.add((r2[ia], r2[ib]))
                    changed = True
        for t, a, b in pr.irreflexive:
            if t not in db:
                continue
            ia, ib = self.colnames[t].index(a), self.colnames[t].index(b)
            bad = [r for r in db[t] if r[ia] is not None and r[ia] == r[ib]]
            if bad:
                db[t] = [r for r in db[t] if r not in bad] or db[t][:1]
                changed = True
        # value dependencies: x -> y inside a table (official mapping), child.x = parent.y across a key
        from .profile_r import _k
        for t, x, y, m in pr.fd:
            if t not in db or not db[t]:
                continue
            ix, iy = self.colnames[t].index(x), self.colnames[t].index(y)
            inv = None
            for r in db[t]:
                k = _k(r[ix])
                if r[ix] is None or k not in m or m[k] == r[iy] or (m[k] is not None and str(m[k]) == str(r[iy])):
                    continue
                changed = True
                if (t, y) in self.qcols and (t, x) not in self.qcols:
                    if inv is None:
                        inv = {}
                        for a_, b_ in m.items():
                            inv.setdefault(repr(b_), []).append(a_)
                    alts = inv.get(repr(r[iy]))
                    if alts:
                        a_ = alts[0]
                        info = pr.col.get((t, x)) or {}
                        cand = [v for v in (info.get('domain') or []) if _k(v) == a_]
                        if cand:
                            r[ix] = cand[0]
                            continue
                r[iy] = m[k]
        for t, x, b, p, y, d in pr.cross:
            if t not in db or p not in db or not db[t] or not db[p]:
                continue
            ix, ib = self.colnames[t].index(x), self.colnames[t].index(b)
            iy, idd = self.colnames[p].index(y), self.colnames[p].index(d)
            par = {r[idd]: r for r in db[p]}
            for r in db[t]:
                pr_ = par.get(r[ib])
                if pr_ is None or r[ix] is None or pr_[iy] is None or r[ix] == pr_[iy]:
                    continue
                changed = True
                if (t, x) in self.qcols and (p, y) not in self.qcols:
                    pr_[iy] = r[ix]
                else:
                    r[ix] = pr_[iy]
        # year agrees with the date
        for t, y, d in pr.year_date:
            if t not in db:
                continue
            iy, idd = self.colnames[t].index(y), self.colnames[t].index(d)
            for r in db[t]:
                if r[iy] is None or r[idd] is None:
                    continue
                try:
                    if int(str(r[idd])[:4]) == int(r[iy]):
                        continue
                except ValueError:
                    pass
                changed = True
                if (t, d) in self.qcols and (t, y) not in self.qcols:
                    try:
                        r[iy] = int(str(r[idd])[:4])
                    except ValueError:
                        r[idd] = f'{int(r[iy]):04d}' + str(r[idd])[4:]
                else:
                    r[idd] = f'{int(r[iy]):04d}' + str(r[idd])[4:]
        return changed

    def fanout_rows(self, db, t, n):
        """Append n copies of the first row of table t that keep every join-linked column (so the
        copies join exactly like the original) and refresh only primary-key columns that are not
        join-linked. Returns False when the key cannot be refreshed without breaking the join."""
        if not db.get(t):
            return False
        cols = self.cols[t]
        base = db[t][0]
        # keep columns the queries equate (they carry the join); refresh other key columns, whose
        # foreign-key parents are re-created by repair()
        refresh = [i for i, c in enumerate(cols) if c['pk'] > 0 and (t, c['name']) not in self.qlinked]
        if self.pkcols[t] and not refresh:
            return False
        for _ in range(n):
            row = list(base)
            for i in refresh:
                row[i] = self._fit(t, cols[i], self.fresh(self.kind[(t, cols[i]['name'])]))
            db[t].append(row)
        return True

    def clone_subtree(self, db, t, which=0):
        """Copy row `which` of table t under a new key, together with the rows that reference it
        (re-pointed to the new key, keeping their other references): the same member attends two
        events, the same driver races twice, etc. Returns False if t has no single-column key."""
        if not db.get(t) or which >= len(db[t]):
            return False
        pk = [i for i, c in enumerate(self.cols[t]) if c['pk'] > 0]
        if len(pk) != 1:
            return False
        i = pk[0]
        old = db[t][which][i]
        r = self.uf.find((t, self.cols[t][i]['name']))
        new = self.fresh_class(r) if self.cfg.profile_r is not None else self.fresh(self.cls_kind[r] if self.cls_kind[r] != 'mixed' else 'int')
        row = list(db[t][which])
        row[i] = new
        db[t].append(row)
        refs = []
        for t2 in db:
            for fk in self.s.tables[t2]['fks']:
                if fk['ref_table_resolved'] == t and len(fk['from_cols']) == 1 and fk['to_cols'] and \
                        fk['to_cols'][0] == self.cols[t][i]['name']:
                    refs.append((t2, fk['from_cols'][0]))
        if self.cfg.profile_r is not None:
            for a, b, c, d in self.cfg.profile_r.ind_fk:
                if c == t and d == self.cols[t][i]['name'] and a in db:
                    refs.append((a, b))
        for (a, b), (c, d) in self.pair.gold.equalities + self.pair.pred.equalities:
            if (c, d) == (t, self.cols[t][i]['name']) and a in db:
                refs.append((a, b))
            if (a, b) == (t, self.cols[t][i]['name']) and c in db:
                refs.append((c, d))
        for t2, c2 in set(refs):
            if t2 == t:
                continue
            j = self.colnames[t2].index(c2)
            pk2 = [k for k, c in enumerate(self.cols[t2]) if c['pk'] > 0]
            for r2 in [x for x in db[t2] if x[j] == old]:
                n2 = list(r2)
                n2[j] = new
                if len(pk2) == 1 and pk2[0] != j:
                    n2[pk2[0]] = self.new_key(t2, self.cols[t2][pk2[0]]['name'])
                db[t2].append(n2)
        return True

    def tie_probe(self, pv):
        q = dict(pv)
        order = {self.uf.find(c) for c in self.pair.gold.order_columns | self.pair.pred.order_columns if c in self.kind}
        proj = {self.uf.find(c) for c in self.pair.gold.proj_columns | self.pair.pred.proj_columns if c in self.kind}
        filt = set(self.atoms['gold']) | set(self.atoms['pred'])
        for r in self.classes:
            if self.key_class[r]:
                q[r] = self.pick(r, 'random', 1) if not (self.atoms['gold'].get(r) or self.atoms['pred'].get(r)) else q.get(r)
                if q[r] == pv.get(r):
                    q[r] = self.fresh_class(r)
            elif r in proj and r not in order and r not in filt:
                q[r] = self.fresh_class(r)
        return q

    def violate_probe(self):
        pv = self.base_probe('both')
        for r in set(self.atoms['gold']) | set(self.atoms['pred']):
            if self.key_class[r]:
                continue
            for _ in range(6):
                v = self.pick(r, 'random', 0)
                atoms = self.atoms['gold'].get(r, []) + self.atoms['pred'].get(r, [])
                if v is not None and all(approx_eval(a, v) is False for a in atoms):
                    pv[r] = v
                    break
            else:
                pv[r] = self.fresh_class(r)
        return pv

    def base_probe(self, mode):
        pv = {}
        for r in self.classes:
            pv[r] = self.pick(r, mode, 0)
        return pv


# ----------------------------------------------------------------------------- atom semantics (approx.)
def canonical_true(a, kind, sqlite_domain=True):
    out = []
    vs = a.values
    v0 = vs[0] if vs else None
    if a.op in ('=', 'in', 'like') or a.wrapper:
        for v in (vs if a.op == 'in' else [v0]):
            out += variants(v, kind, a.wrapper, a.op, sqlite_domain)[:3]
    elif a.op in ('>', '>='):
        out += variants(v0, kind, None, '=', sqlite_domain)
    elif a.op in ('<', '<='):
        out += variants(v0, kind, None, '=', sqlite_domain)
    elif a.op == 'between' and len(vs) == 2:
        out += variants(vs[0], kind, a.wrapper, '=', sqlite_domain) + variants(vs[1], kind, a.wrapper, '=', sqlite_domain)
    elif a.op == 'isnull':
        out.append(None)
    elif a.op in ('notnull', '!='):
        out += GENERIC.get(kind, GENERIC['text'])[:2]
        if v0 is not None:
            out += variants(v0, kind, None, '=', sqlite_domain)
    return [x for x in out if x is not _BAD]


def approx_eval(a, v):
    """Approximate truth of atom `a` for column value v (None = NULL)."""
    if a.op == 'isnull':
        return v is None
    if a.op == 'notnull':
        return v is not None
    if v is None:
        return None
    x = v
    w = a.wrapper or ''
    try:
        if w.startswith('strftime:') and isinstance(v, str):
            fmt = w.split(':', 1)[1]
            x = {'%Y': v[:4], '%m': v[5:7], '%d': v[8:10], '%Y-%m': v[:7], '%Y-%m-%d': v[:10], '%H': v[11:13]}.get(fmt, v)
        elif w.startswith('substr:') and isinstance(v, str):
            parts = w.split(':')
            st = int(parts[1])
            ln = int(parts[2]) if parts[2] else None
            x = v[st - 1: (st - 1 + ln) if ln else None]
        elif w in ('lower',) and isinstance(v, str):
            x = v.lower()
        elif w in ('upper',) and isinstance(v, str):
            x = v.upper()
        elif w in ('trim',) and isinstance(v, str):
            x = v.strip()
        elif w.startswith(('add:', 'sub:', 'mul:', 'div:')) and isinstance(v, (int, float)):
            k = float(w.split(':')[1])
            x = {'add': v + k, 'sub': v - k, 'mul': v * k, 'div': (v / k if k else 0)}[w.split(':')[0]]
        lits = a.values
        if a.op == 'like':
            pat = '^' + re.escape(lits[0]).replace('%', '.*').replace('_', '.') + '$'
            pat = pat.replace('\\%', '.*').replace('\\_', '.')
            return re.match(pat, str(x), re.I | re.S) is not None
        if a.op == 'in':
            return any(_eq(x, l) for l in lits)
        if a.op == 'between':
            return _cmp(x, lits[0]) >= 0 and _cmp(x, lits[1]) <= 0
        c = _cmp(x, lits[0])
        return {'=': c == 0, '!=': c != 0, '>': c > 0, '>=': c >= 0, '<': c < 0, '<=': c <= 0}[a.op]
    except Exception:  # noqa: BLE001
        return None


def _eq(x, y):
    return _cmp(x, y) == 0


def _cmp(x, y):
    if isinstance(x, str) and isinstance(y, (int, float)):
        try:
            x = float(x)
        except ValueError:
            return 1  # text > numeric in SQLite ordering
    if isinstance(y, str) and isinstance(x, (int, float)):
        try:
            y = float(y)
        except ValueError:
            return -1
    return (x > y) - (x < y)


# ----------------------------------------------------------------------------- search
@dataclass
class Result:
    found: bool
    witness: dict | None = None
    n_eval: int = 0
    elapsed: float = 0.0
    phase: str | None = None
    status_counts: dict = field(default_factory=dict)
    note: str | None = None


def differ_set(rg, rp):
    return set(rg) != set(rp)


class CGX:
    def __init__(self, schema: SchemaInfo, analyzer: Analyzer, cfg: Config):
        self.s, self.an, self.cfg = schema, analyzer, cfg

    def run(self, gold, pred):
        t0 = time.monotonic()
        rng = random.Random(self.cfg.seed)
        pair = analyze_pair(self.an, gold, pred)
        self._gold, self._pred = gold, pred
        if not pair.tables:
            return Result(False, note='no_tables', elapsed=time.monotonic() - t0)
        gen = Generator(self.s, pair, self.cfg, rng)
        ev = Evaluator(self.s, gold, pred, self.cfg.query_timeout_s)
        counts = {}
        deadline = t0 + self.cfg.budget_s
        try:
            extra = gen.cfg.realism.violations if gen.cfg.realism is not None else None
            for phase, db in self._candidates(gen, rng, deadline):
                st, rg, rp = ev.eval(db, extra)
                counts[st] = counts.get(st, 0) + 1
                if st == 'ok' and differ_set(rg, rp):
                    if not self._l1_ok(gen, db):
                        counts['l1_reject'] = counts.get('l1_reject', 0) + 1
                        continue
                    if gen.cfg.realism is not None and ev.extra_result:
                        counts['realism_reject'] = counts.get('realism_reject', 0) + 1
                        self._feedback(db, rg, rp)
                        continue
                    return Result(True, {t: rows for t, rows in db.items() if rows}, ev.n_eval,
                                  time.monotonic() - t0, phase, counts)
                if st == 'ok':
                    self._feedback(db, rg, rp)
                if time.monotonic() > deadline:
                    break
            return Result(False, None, ev.n_eval, time.monotonic() - t0, None, counts)
        finally:
            ev.close()

    def _l1_ok(self, gen, db, gold=None, pred=None):
        from .certify import certify
        rep = certify(self.s, {t: r for t, r in db.items() if r}, self._gold, self._pred,
                      referenced_tables=gen.qtables, timeout_s=1.0, formats=gen.cfg.formats)
        ok = rep.get('L1f') if gen.cfg.formats is not None else rep.get('L1')
        if ok and gen.cfg.never_null:
            cols = {(t.lower(), c.lower()) for t, c in gen.pair.gold.columns | gen.pair.pred.columns}
            for t, rows in db.items():
                for i, c in enumerate(gen.cols.get(t, [])):
                    key = (t.lower(), c['name'].lower())
                    if key in gen.cfg.never_null and key in cols and any(r[i] is None for r in rows):
                        return False
        if ok and gen.cfg.profile_r is not None and not gen.cfg.profile_r.ok({t: r for t, r in db.items() if r}):
            return False
        return bool(ok and rep.get('differ', {}).get('C_set'))

    def _realism_ok(self, gen, db):
        for kind_, (t, c), arg in gen.cfg.realism.items:
            if t not in db or kind_ not in ('in', 'between', 'not_null'):
                continue
            ci = [x['name'] for x in gen.cols[t]].index(c) if t in gen.cols else None
            if ci is None:
                continue
            for row in db[t]:
                v = row[ci]
                if kind_ == 'not_null' and v is None:
                    return False
                if v is None:
                    continue
                if kind_ == 'in' and v not in arg and str(v) not in [str(a) for a in arg]:
                    return False
                if kind_ == 'between':
                    try:
                        if not (arg[0] <= v <= arg[1]):
                            return False
                    except TypeError:
                        return False
        return True

    # ------------------------------------------------------------ candidate stream
    def _feedback(self, db, rg, rp):
        # keep databases where at least one query returns rows: good parents for mutation
        score = (len(rg) > 0) + (len(rp) > 0)
        self._pool.append((score, db))
        if len(self._pool) > 60:
            self._pool.sort(key=lambda x: -x[0])
            self._pool = self._pool[:40]

    def _candidates(self, gen, rng, deadline):
        self._pool = []
        if self.cfg.real_src is not None and self.cfg.real_phase:
            yield from self._real_candidates(gen, rng, deadline)
        if not self.cfg.synthetic:
            while time.monotonic() < deadline and self._pool:  # mutation of real sub-databases only
                _, parent = rng.choice(self._pool)
                yield 'mutate', self._mutate(gen, parent, rng)
            return
        modes = ['both', 'gold', 'pred']
        bases = []
        if self.cfg.isolation:
            # phase 1: single-probe databases satisfying each query's atoms
            for m in modes:
                pv = gen.base_probe(m)
                bases.append(pv)
                yield 'probe1', gen.build([pv])
            # phase 2: two-probe structures (duplicates, ties, mixed satisfaction)
            for a in bases:
                for b in bases:
                    pv2 = dict(b)
                    for r in gen.classes:
                        if gen.key_class[r]:
                            pv2[r] = gen.pick(r, 'random', 1)
                    yield 'probe2', gen.build([a, pv2])
            # tie probes: same ordering/filter values, fresh keys, different projected values;
            # both insertion orders (SQLite's scan order decides which tied row LIMIT keeps)
            for a in bases:
                b = gen.tie_probe(a)
                yield 'tie', gen.build([a, b])
                yield 'tie', gen.build([b, a])
            # violating probe: a row that fails the filters (empty selections, NULL aggregates)
            yield 'violate', gen.build([gen.violate_probe()])
            # literal cover: one probe per distinct equality literal of a class (e.g. two players named
            # in two CASE branches), so that every branch of both queries is exercised at once
            cover = []
            for r in gen.classes:
                if gen.key_class[r]:
                    continue
                lits = []
                for a in gen.atoms['gold'].get(r, []) + gen.atoms['pred'].get(r, []):
                    if a.op in ('=', 'in') and not a.wrapper:
                        for v in a.values:
                            c = coerce(v, gen.cls_kind[r] if gen.cls_kind[r] != 'mixed' else 'text')
                            if c is not _BAD and c not in lits:
                                lits.append(c)
                if len(lits) >= 2:
                    cover.append((r, lits[:4]))
            for a in bases:
                for r, lits in cover:
                    probes = []
                    for j, v in enumerate(lits):
                        q = gen.tie_probe(a) if j else dict(a)
                        q[r] = v
                        probes.append(q)
                    yield 'cover', gen.build(probes)
                    yield 'cover', gen.build(probes[::-1])
            # controlled growth: fan-out duplicates on the many side of a join (COUNT vs COUNT DISTINCT,
            # HAVING COUNT thresholds) and enough probes to pass LIMIT/OFFSET windows
            sizes = {2}
            for q in (gen.pair.gold, gen.pair.pred):
                sizes.update(x + 1 for x in q.flags.get('having_thresholds', []))
                lim, off = q.flags.get('limit'), q.flags.get('offset') or 0
                if isinstance(lim, int) and (off or lim > 1):
                    sizes.add(off + lim + 1)
            sizes = sorted(min(x, self.cfg.max_group_rows) for x in sizes)
            for a in bases:
                for t in gen.qtables:
                    for n in sizes:
                        db = gen.build([a])
                        if gen.fanout_rows(db, t, n - 1):
                            gen.repair(db)
                            yield 'fanout', db
                for n in sizes:
                    if n > 2:
                        probes = [a] + [gen.tie_probe(a) for _ in range(n - 1)]
                        yield 'window', gen.build(probes)
            for a in bases:
                for t in gen.qtables:
                    db = gen.build([a])
                    if gen.clone_subtree(db, t):
                        gen.repair(db)
                        yield 'clone', db
            for a in bases:
                yield from self._anchor_variants(gen, [a], rng)
        else:
            for _ in range(3):
                k = rng.randint(1, 5)
                probes = [gen.base_probe(rng.choice(modes + ['random'])) for _ in range(k)]
                yield 'multi', gen.build(probes)
        # phase 3: mutation search
        it = 0
        while time.monotonic() < deadline:
            it += 1
            if self._pool and rng.random() < 0.85:
                ws = [s + 0.25 for s, _ in self._pool]
                _, parent = rng.choices(self._pool, weights=ws)[0]
                db = self._mutate(gen, parent, rng)
            else:
                if self.cfg.isolation:
                    k = 1 if rng.random() < 0.5 else 2
                else:
                    k = rng.randint(1, 5)
                probes = []
                for i in range(k):
                    m = rng.choice(modes + ['random'])
                    pv = gen.base_probe(m)
                    for r in gen.classes:
                        if gen.key_class[r] and i > 0:
                            pv[r] = gen.pick(r, 'random', i)
                    if self.cfg.anchoring and gen.anchor_cls and rng.random() < 0.6:
                        r = rng.choice(sorted(gen.anchor_cls, key=str))
                        if gen.pools.get(r):
                            pv[r] = rng.choice(gen.pools[r])
                    probes.append(pv)
                db = gen.build(probes)
            yield 'mutate', db

    # ------------------------------------------------------------ real sub-databases (tier R)
    def _real_candidates(self, gen, rng, deadline):
        """Sub-databases of the official database: seed rows that satisfy one query's predicates and
        not the other's (diff anchoring), completed along the join graph with related real rows,
        closed under foreign keys and total participation with real rows, then grown with real
        tied rows, LIMIT windows and rows with real NULLs, and shrunk by deleting single rows."""
        from .realsrc import conj
        from .certify import qi
        src, pr = self.cfg.real_src, self.cfg.profile_r
        G, Q = gen.pair.gold, gen.pair.pred
        cidx = {t: {c: i for i, c in enumerate(gen.colnames[t])} for t in gen.rtables}

        def atoms_of(side, t):
            q = G if side == 'gold' else Q
            return [a for a in q.atoms if a.col and a.col[0] == t]

        def where(t, mode):
            gw, gp = conj(atoms_of('gold', t))
            pw, pp = conj(atoms_of('pred', t))
            if mode == 'gold':
                return gw, gp
            if mode == 'pred':
                return pw, pp
            if mode == 'both':
                return f'({gw}) AND ({pw})', gp + pp
            if mode == 'gnp':
                return f'({gw}) AND NOT COALESCE(({pw}), 0)', gp + pp
            if mode == 'png':
                return f'({pw}) AND NOT COALESCE(({gw}), 0)', pp + gp
            return '1', []
        # join edges among relevant tables: query equalities, declared and mined foreign keys
        edges = set()
        for (t1, c1), (t2, c2) in G.equalities + Q.equalities:
            if t1 in cidx and t2 in cidx and c1 in cidx[t1] and c2 in cidx[t2]:
                edges.add((t1, c1, t2, c2))
                edges.add((t2, c2, t1, c1))
        fks = []
        for t in gen.rtables:
            for fk in self.s.tables[t]['fks']:
                p = fk['ref_table_resolved']
                if p in cidx and len(fk['from_cols']) == 1 and fk['to_cols'] and fk['to_cols'][0] in cidx[p]:
                    fks.append((t, fk['from_cols'][0], p, fk['to_cols'][0]))
        for a, b, c, d in pr.ind_fk:
            if a in cidx and c in cidx:
                fks.append((a, b, c, d))
        for a, b, c, d in fks:
            if a in gen.qtables and c in gen.qtables:
                edges.add((a, b, c, d))
                edges.add((c, d, a, b))

        def add(db, t, row):
            if row not in db[t]:
                db[t].append(list(row))
                return True
            return False

        def complete(db, seed_t, mode):
            if not self.cfg.join_graph:
                return db
            seen, frontier = {seed_t}, [seed_t]
            while frontier:
                t = frontier.pop(0)
                for t1, c1, t2, c2 in sorted(edges):
                    if t1 != t or t2 in seen or t2 not in gen.qtables:
                        continue
                    vals = []
                    for r in db[t1]:
                        v = r[cidx[t1][c1]]
                        if v is not None and v not in vals:
                            vals.append(v)
                    w, p = where(t2, mode)
                    for v in vals[:3]:
                        got = src.by_value(t2, c2, v, 2, w, p) or src.by_value(t2, c2, v, 1)
                        for r in got:
                            add(db, t2, r)
                    seen.add(t2)
                    frontier.append(t2)
            return db

        def close(db):
            for _ in range(4):
                changed = False
                for a, b, c, d in fks:
                    if not db.get(a):
                        continue
                    have = {r[cidx[c][d]] for r in db[c]}
                    for r in list(db[a]):
                        v = r[cidx[a][b]]
                        if v is not None and v not in have:
                            got = src.by_value(c, d, v, 1)
                            if got:
                                changed |= add(db, c, got[0])
                            have.add(v)
                for a, b, c, d in pr.ind_total:
                    if a not in db or c not in db or not db[a]:
                        continue
                    have = {r[cidx[c][d]] for r in db[c]}
                    for r in list(db[a]):
                        v = r[cidx[a][b]]
                        if v is not None and v not in have:
                            got = src.by_value(c, d, v, 1)
                            if got:
                                changed |= add(db, c, got[0])
                            have.add(v)
                if not changed:
                    break
            return db

        def fresh_db():
            return {t: [] for t in gen.rtables}

        def union(*dbs):
            out = fresh_db()
            for d in dbs:
                for t, rows in d.items():
                    for r in rows:
                        add(out, t, r)
            return out

        def finish(db):
            db = close({t: [list(r) for r in rows] for t, rows in db.items()})
            gen.repair(db)
            return db
        anchored = {}
        modes = ['gnp', 'png', 'both', 'gold', 'pred'] if self.cfg.anchoring else ['none']
        for mode in modes:
            for t in gen.qtables:
                w, p = where(t, mode)
                if mode in ('gnp', 'png') and not (atoms_of('gold', t) or atoms_of('pred', t)):
                    continue
                for r in src.rows(t, w, p, limit=3):
                    db = fresh_db()
                    db[t].append(list(r))
                    db = complete(db, t, 'both' if mode in ('gnp', 'png') else mode)
                    anchored.setdefault(mode, []).append(db)
                    yield 'real', finish(db)
                if time.monotonic() > deadline:
                    return
        # combinations: a row only one query selects next to rows both select
        subs = anchored.get('both', []) + anchored.get('gold', []) + anchored.get('pred', []) + anchored.get('none', [])
        for x in anchored.get('gnp', [])[:3] + anchored.get('png', [])[:3]:
            for y in subs[:3]:
                yield 'real2', finish(union(x, y))
                yield 'real2', finish(union(y, x))
        for i, x in enumerate(subs[:4]):
            for y in subs[i + 1:5]:
                yield 'real2', finish(union(x, y))
        if time.monotonic() > deadline:
            return
        # real duplicates: rows of a query table that share a value of a referenced or join column,
        # among rows that satisfy both queries' predicates and join rows that do (one hop)
        refcols = G.columns | Q.columns
        for t in gen.qtables:
            w, p = where(t, 'both')
            restr, rp_ = [w], list(p)
            for t1, c1, t2, c2 in sorted(edges):
                if t2 != t or t1 == t:
                    continue
                w1, p1 = where(t1, 'both')
                if w1 != '(1) AND (1)':
                    restr.append(f'{qi(c2)} IN (SELECT {qi(c1)} FROM {qi(t1)} WHERE {w1})')
                    rp_ += p1
            base = ' AND '.join(f'({x})' for x in restr)
            for c in gen.colnames[t]:
                if (t, c) not in refcols and not any(e[0] == t and e[1] == c for e in edges):
                    continue
                got = src.rows(t, f'({base}) AND {qi(c)} IN (SELECT {qi(c)} FROM {qi(t)} WHERE {base} '
                                  f'GROUP BY {qi(c)} HAVING COUNT(*) > 1)', rp_ + rp_, limit=4, order=f'{qi(c)}')
                if len(got) < 2:
                    continue
                dbs = [complete({**fresh_db(), t: [list(r)]}, t, 'both') for r in got]
                yield 'realdup', finish(union(*dbs[:2]))
                yield 'realdup', finish(union(*dbs))
                for x in subs[:2]:
                    yield 'realdup', finish(union(x, *dbs[:2]))
            if time.monotonic() > deadline:
                return
        # real ties on ORDER BY columns, and LIMIT windows
        order_cols = [c for c in G.order_columns | Q.order_columns if c[0] in gen.qtables]
        for (t, c) in sorted(order_cols):
            w, p = where(t, 'both')
            for x in subs[:3]:
                for r in x[t][:2]:
                    v = r[cidx[t][c]]
                    for r2 in src.rows(t, f'{qi(c)} IS ? AND ({w})', [v] + p, limit=4):
                        if r2 in x[t]:
                            continue
                        d2 = complete({**fresh_db(), t: [list(r2)]}, t, 'both')
                        yield 'realtie', finish(union(x, d2))
                        yield 'realtie', finish(union(d2, x))
            lims = [q.flags.get('limit') for q in (G, Q) if isinstance(q.flags.get('limit'), int)]
            if lims:
                k = max(lims) + (max([q.flags.get('offset') or 0 for q in (G, Q)]) or 0) + 1
                for dirn in ('DESC', 'ASC'):
                    rows = src.rows(t, f'{qi(c)} IS NOT NULL AND ({w})', p, limit=min(k + 1, 16), order=f'{qi(c)} {dirn}')
                    if rows:
                        dbs = [complete({**fresh_db(), t: [list(r)]}, t, 'both') for r in rows]
                        yield 'realwin', finish(union(*dbs))
        # real NULLs in referenced columns
        for (t, c) in sorted(G.columns | Q.columns):
            if t not in gen.qtables or not (pr.col.get((t, c)) or {}).get('n_null'):
                continue
            w, p = where(t, 'both')
            for r in src.rows(t, f'{qi(c)} IS NULL AND ({w})', p, limit=2) or src.rows(t, f'{qi(c)} IS NULL', [], limit=2):
                d = complete({**fresh_db(), t: [list(r)]}, t, 'both')
                yield 'realnull', finish(d)
                for x in subs[:2]:
                    yield 'realnull', finish(union(x, d))
        if time.monotonic() > deadline:
            return
        # shrink: delete one row of a query table
        for x in subs[:4]:
            for t in gen.qtables:
                for i in range(min(len(x[t]), 3)):
                    if len(x[t]) > 1:
                        d = {tt: [list(r) for r in rows] for tt, rows in x.items()}
                        d[t].pop(i)
                        yield 'realdel', finish(d)
        # clone a real entity with the rows that reference it (repeated entities, e.g. recurring events)
        for x in subs[:4]:
            for t in gen.qtables:
                d = {tt: [list(r) for r in rows] for tt, rows in x.items()}
                if gen.clone_subtree(d, t):
                    yield 'realclone', finish(d)
        # random real seeds without predicates
        for t in gen.qtables:
            rows = src.rows(t, '1', [], limit=4)
            dbs = [complete({**fresh_db(), t: [list(r)]}, t, 'none') for r in rows]
            for i in range(len(dbs)):
                yield 'realrand', finish(dbs[i])
                if i + 1 < len(dbs):
                    yield 'realrand', finish(union(dbs[i], dbs[i + 1]))

    def _anchor_variants(self, gen, probes, rng):
        """Boundary/NULL variants on anchor classes of a single probe."""
        if not gen.anchor_cls:
            return
        for r in sorted(gen.anchor_cls, key=str):
            vals = list(gen.pools.get(r, []))
            if gen.cls_nullable[r]:
                vals.append(None)
            for v in vals[:12]:
                pv = dict(probes[0])
                pv[r] = v
                yield 'anchor', gen.build([pv])

    def _mutate(self, gen, parent, rng):
        db = {t: [list(r) for r in rows] for t, rows in parent.items()}
        nops = rng.choice([1, 1, 2, 3])
        for _ in range(nops):
            op = rng.choices(['value', 'null', 'dup', 'tie', 'decoy', 'delete', 'fanout', 'clone'],
                             weights=[5, 2, 2, 2, 1.5, 1, 1.5, 1])[0]
            tables = [t for t in gen.qtables if db.get(t)]
            if not tables:
                break
            t = rng.choice(tables)
            cols = gen.cols[t]
            if op in ('value', 'null'):
                row = rng.choice(db[t])
                cand = list(range(len(cols)))
                if gen.anchor_cls and rng.random() < 0.7:
                    an = [i for i, c in enumerate(cols) if gen.uf.find((t, c['name'])) in gen.anchor_cls]
                    if an:
                        cand = an
                i = rng.choice(cand)
                c = cols[i]
                r = gen.uf.find((t, c['name']))
                if op == 'null':
                    if not gen.nullable[(t, c['name'])] or not gen.realism_allowed(r, None):
                        continue
                    newv = None
                else:
                    newv = gen._fit(t, c, gen.pick(r, 'random', 0))
                old = row[i]
                row[i] = newv
                # keep join consistency: propagate to rows of other tables sharing the old class value
                if gen.cfg.join_graph and old is not None and gen.key_class[r] is False:
                    for (t2, c2) in gen.classes[r]:
                        if t2 in db and (t2, c2) != (t, c['name']):
                            j = [x['name'] for x in gen.cols[t2]].index(c2)
                            for row2 in db[t2]:
                                if row2[j] == old and rng.random() < 0.5:
                                    row2[j] = newv
            elif op == 'dup' and len(db[t]) < gen.cfg.max_rows_per_table:
                row = list(rng.choice(db[t]))
                for i, c in enumerate(cols):
                    if c['pk'] > 0:
                        row[i] = gen.new_key(t, c['name'])
                db[t].append(row)
            elif op == 'tie' and len(db[t]) < gen.cfg.max_rows_per_table:
                row = list(rng.choice(db[t]))
                for i, c in enumerate(cols):
                    r = gen.uf.find((t, c['name']))
                    if c['pk'] > 0:
                        row[i] = gen.new_key(t, c['name'])
                    elif r not in gen.anchor_cls and not gen.key_class[r] and rng.random() < 0.5:
                        row[i] = gen._fit(t, c, gen.pick(r, 'random', 0))
                db[t].append(row)
            elif op == 'decoy' and len(db[t]) < gen.cfg.max_rows_per_table:
                row = [gen._fit(t, c, gen.pick(gen.uf.find((t, c['name'])), 'random', 0)) for c in cols]
                for i, c in enumerate(cols):
                    r = gen.uf.find((t, c['name']))
                    if gen.key_class[r] or len(gen.classes[r]) > 1:
                        row[i] = gen._fit(t, c, gen.fresh(gen.kind[(t, c['name'])]))
                db[t].append(row)
            elif op == 'fanout' and len(db[t]) < gen.cfg.max_group_rows:
                src = rng.choice(db[t])
                db[t].remove(src)
                db[t].insert(0, src)
                gen.fanout_rows(db, t, 1)
            elif op == 'clone' and len(db[t]) < gen.cfg.max_rows_per_table:
                gen.clone_subtree(db, t, rng.randrange(len(db[t])))
            elif op == 'delete' and len(db[t]) > 1:
                db[t].pop(rng.randrange(len(db[t])))
        gen.repair(db)
        return db
