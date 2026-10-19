"""Independent witness certifier (CGX-Protocol v1, Sections 3-4).

Deliberately self-contained: it re-creates the database from the original DDL, inserts the
witness rows with parameter binding, checks every declared constraint, executes the ORIGINAL
SQL strings, and compares results under the declared contracts. It does not import any
generator code, so that a bug in a generator cannot certify its own output.

Witness format: {table_name: [[v1, v2, ...], ...]} with values in PRAGMA table_info column order.
"""
from __future__ import annotations

import json
import math
import re
import sqlite3
import time
from collections import Counter

DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
DATETIME_RE = re.compile(r'^\d{4}-\d{2}-\d{2}([ T]\d{2}:\d{2}(:\d{2}(\.\d+)?)?)?$')
TIME_RE = re.compile(r'^\d{2}:\d{2}(:\d{2}(\.\d+)?)?$')


def affinity(decl: str) -> str:
    d = (decl or '').upper()
    if 'INT' in d:
        return 'INTEGER'
    if 'CHAR' in d or 'CLOB' in d or 'TEXT' in d:
        return 'TEXT'
    if d == '' or 'BLOB' in d:
        return 'BLOB'
    if 'REAL' in d or 'FLOA' in d or 'DOUB' in d:
        return 'REAL'
    return 'NUMERIC'


def temporal_kind(decl: str):
    d = (decl or '').upper()
    if 'DATETIME' in d or 'TIMESTAMP' in d:
        return 'datetime'
    if 'DATE' in d:
        return 'date'
    if d.strip() == 'TIME':
        return 'time'
    return None


def qi(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


class SchemaInfo:
    """Schema facts read back from SQLite after executing the original DDL."""

    def __init__(self, ddl_list):
        self.ddl = list(ddl_list)
        con = sqlite3.connect(':memory:')
        for stmt in self.ddl:
            con.executescript(stmt)
        self.tables = {}
        for (name,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
            cols = []
            for cid, cname, ctype, notnull, dflt, pk in con.execute(f'PRAGMA table_info({qi(name)})'):
                cols.append(dict(name=cname, decl=ctype or '', notnull=bool(notnull), pk=int(pk),
                                 affinity=affinity(ctype), temporal=temporal_kind(ctype)))
            fks = {}
            for row in con.execute(f'PRAGMA foreign_key_list({qi(name)})'):
                fid, seq, ref_table, from_col, to_col = row[0], row[1], row[2], row[3], row[4]
                fks.setdefault(fid, dict(ref_table=ref_table, from_cols=[], to_cols=[]))
                fks[fid]['from_cols'].append(from_col)
                fks[fid]['to_cols'].append(to_col)
            self.tables[name] = dict(name=name, columns=cols, fks=list(fks.values()))
        con.close()
        self._lower = {t.lower(): t for t in self.tables}
        # resolve FK targets: missing to_col means the parent's primary key
        for t in self.tables.values():
            for fk in t['fks']:
                parent = self._lower.get(fk['ref_table'].lower())
                fk['ref_table_resolved'] = parent
                if parent is not None:
                    pcols = self.tables[parent]['columns']
                    pk_cols = [c['name'] for c in sorted(pcols, key=lambda c: c['pk']) if c['pk'] > 0]
                    fk['to_cols'] = [tc if tc is not None else (pk_cols[i] if i < len(pk_cols) else None)
                                     for i, tc in enumerate(fk['to_cols'])]

    def table(self, name):
        real = self._lower.get(name.lower())
        return self.tables[real] if real else None

    def column_names(self, table):
        return [c['name'] for c in self.table(table)['columns']]


def _col_resolve(cols, name):
    low = name.lower() if name else None
    for i, c in enumerate(cols):
        if c['name'].lower() == low:
            return i
    return None


def run_query(con, sql, timeout_s=5.0):
    deadline = time.monotonic() + timeout_s
    con.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 10000)
    try:
        cur = con.execute(sql)
        rows = cur.fetchall()
        return True, rows, None
    except Exception as e:  # noqa: BLE001 - every engine error is a recorded outcome
        return False, None, f'{type(e).__name__}: {e}'
    finally:
        con.set_progress_handler(None, 0)


def _norm_val(v):
    if isinstance(v, float):
        if math.isnan(v):
            return ('nan',)
        if v == int(v) and abs(v) < 2 ** 53:
            return int(v)
        return float(f'{v:.9g}')
    return v


def compare(rows1, rows2):
    """Return dict contract -> True if the results DIFFER under that contract."""
    out = {}
    out['C_set'] = set(rows1) != set(rows2)
    out['C_bag'] = Counter(rows1) != Counter(rows2)

    def lenient(rows):
        rs = [tuple(_norm_val(v) for v in r) for r in rows]
        if len(rs) == 1 and all(v is None for v in rs[0]):
            rs = []
        return set(rs)
    out['C_lenient'] = lenient(rows1) != lenient(rows2)
    return out


def load_witness_into(con, schema: SchemaInfo, witness):
    """Insert witness rows. Returns (ok, error)."""
    for tname, rows in witness.items():
        t = schema.table(tname)
        if t is None:
            return False, f'unknown table {tname}'
        if not rows:
            continue
        ncol = len(t['columns'])
        ph = ','.join('?' * ncol)
        for r in rows:
            if len(r) != ncol:
                return False, f'arity mismatch in {tname}'
            try:
                con.execute(f'INSERT INTO {qi(t["name"])} VALUES ({ph})', list(r))
            except Exception as e:  # noqa: BLE001
                return False, f'insert {tname}: {type(e).__name__}: {e}'
    return True, None


def check_fks(con, schema: SchemaInfo):
    """Value-level FK check (does not rely on PRAGMA foreign_keys, which errors on
    FKs whose parent columns are not declared unique in some BIRD schemas)."""
    violations = []
    for t in schema.tables.values():
        for fk in t['fks']:
            parent = fk['ref_table_resolved']
            if parent is None or any(c is None for c in fk['to_cols']):
                violations.append((t['name'], 'unresolvable_fk', fk['ref_table']))
                continue
            fc = ' AND '.join(f'c.{qi(a)} IS NOT NULL' for a in fk['from_cols'])
            cond = ' AND '.join(f'p.{qi(b)} = c.{qi(a)}' for a, b in zip(fk['from_cols'], fk['to_cols']))
            sql = (f'SELECT COUNT(*) FROM {qi(t["name"])} AS c WHERE {fc} AND NOT EXISTS '
                   f'(SELECT 1 FROM {qi(parent)} AS p WHERE {cond})')
            try:
                n = con.execute(sql).fetchone()[0]
            except Exception as e:  # noqa: BLE001
                violations.append((t['name'], 'fk_check_error', str(e)))
                continue
            if n:
                violations.append((t['name'], 'fk_violation', fk['ref_table']))
    return violations


def check_type_faithful(con, schema: SchemaInfo):
    """L1 value checks on the stored representation."""
    problems = []
    for t in schema.tables.values():
        cols = t['columns']
        names = ','.join(f'typeof({qi(c["name"])}), {qi(c["name"])}' for c in cols)
        for row in con.execute(f'SELECT {names} FROM {qi(t["name"])}'):
            for i, c in enumerate(cols):
                ty, v = row[2 * i], row[2 * i + 1]
                if c['pk'] and ty == 'null':
                    problems.append((t['name'], c['name'], 'null_pk'))
                if ty == 'null':
                    continue
                aff = c['affinity']
                if c['temporal']:
                    pass  # temporal columns are checked below (ISO text expected)
                elif aff in ('INTEGER', 'REAL', 'NUMERIC') and ty not in ('integer', 'real'):
                    problems.append((t['name'], c['name'], f'{ty}_in_{aff}'))
                elif aff == 'TEXT' and ty != 'text':
                    problems.append((t['name'], c['name'], f'{ty}_in_TEXT'))
                tk = c['temporal']
                if tk and ty == 'text':
                    ok = {'date': DATE_RE, 'datetime': DATETIME_RE, 'time': TIME_RE}[tk].match(v) is not None
                    if ok and tk in ('date', 'datetime'):
                        ok = con.execute('SELECT date(?) IS NOT NULL', (v,)).fetchone()[0] == 1
                    if not ok:
                        problems.append((t['name'], c['name'], f'bad_{tk}'))
                elif tk and ty != 'text':
                    problems.append((t['name'], c['name'], f'{ty}_in_{tk}'))
    return problems


class RealismConstraints:
    """SpotIt+ mined + LLM-validated constraints, mapped to original identifiers (L2)."""

    def __init__(self, constraints_json, clean_to_orig, schema: SchemaInfo):
        self.items = []
        self.unmapped = 0
        c2o = {k.upper(): v for k, v in clean_to_orig.items()}

        def resolve(ref):
            if '__' not in ref:
                return None
            tab, col = ref.split('__', 1)
            t = schema.table(tab)
            if t is None:
                return None
            orig = c2o.get(col.upper(), col)
            idx = _col_resolve(t['columns'], orig)
            if idx is None:
                idx = _col_resolve(t['columns'], col)
            if idx is None:
                return None
            return t['name'], t['columns'][idx]['name']

        def walk(x):
            if isinstance(x, list):
                for y in x:
                    walk(y)
            elif isinstance(x, dict):
                for kind, arg in x.items():
                    try:
                        if kind == 'between':
                            r = resolve(arg[0]['value'])
                            if r:
                                self.items.append(('between', r, (arg[1], arg[2])))
                            else:
                                self.unmapped += 1
                        elif kind == 'in':
                            r = resolve(arg[0]['value'])
                            if r:
                                self.items.append(('in', r, tuple(arg[1])))
                            else:
                                self.unmapped += 1
                        elif kind == 'not_null':
                            r = resolve(arg['value'])
                            if r:
                                self.items.append(('not_null', r, None))
                            else:
                                self.unmapped += 1
                        elif kind == 'dependency':
                            a, b = arg['values']
                            ra, rb = resolve(a), resolve(b)
                            if ra and rb and ra[0] == rb[0]:
                                self.items.append(('fd', ra, rb[1]))
                            else:
                                self.unmapped += 1
                        elif kind == 'primary':
                            r = resolve(arg[0]['value'])
                            if r:
                                self.items.append(('unique', r, None))
                        elif kind == 'foreign':
                            ra, rb = resolve(arg[0]['value']), resolve(arg[1]['value'])
                            if ra and rb:
                                self.items.append(('fk', ra, rb))
                            else:
                                self.unmapped += 1
                        elif isinstance(arg, (list, dict)):
                            walk(arg)  # container level, e.g. {db_name: [...]}
                    except (KeyError, IndexError, TypeError):
                        self.unmapped += 1
        walk(constraints_json)

    def violations(self, con):
        out = []
        for kind, (t, c), arg in self.items:
            T, C = qi(t), qi(c)
            if kind == 'between':
                lo, hi = arg
                sql = f'SELECT COUNT(*) FROM {T} WHERE {C} IS NOT NULL AND NOT ({C} BETWEEN ? AND ?)'
                n = con.execute(sql, (lo, hi)).fetchone()[0]
            elif kind == 'in':
                ph = ','.join('?' * len(arg))
                sql = f'SELECT COUNT(*) FROM {T} WHERE {C} IS NOT NULL AND {C} NOT IN ({ph})'
                n = con.execute(sql, list(arg)).fetchone()[0]
            elif kind == 'not_null':
                n = con.execute(f'SELECT COUNT(*) FROM {T} WHERE {C} IS NULL').fetchone()[0]
            elif kind == 'unique':
                n = con.execute(f'SELECT COUNT(*) - COUNT(DISTINCT {C}) FROM {T} WHERE {C} IS NOT NULL').fetchone()[0]
            elif kind == 'fd':
                D = qi(arg)
                n = con.execute(f'SELECT COUNT(*) FROM (SELECT {C} FROM {T} WHERE {C} IS NOT NULL '
                                f'GROUP BY {C} HAVING COUNT(DISTINCT {D}) > 1 OR (COUNT({D}) > 0 AND COUNT({D}) < COUNT(*)))').fetchone()[0]
            elif kind == 'fk':
                pt, pc = arg
                n = con.execute(f'SELECT COUNT(*) FROM {T} AS a WHERE a.{C} IS NOT NULL AND NOT EXISTS '
                                f'(SELECT 1 FROM {qi(pt)} AS b WHERE b.{qi(pc)} = a.{C})').fetchone()[0]
            else:
                continue
            if n:
                out.append((kind, t, c))
        return out


def certify(schema: SchemaInfo, witness, gold_sql, pred_sql, referenced_tables=(), realism=None,
            timeout_s=5.0, formats=None):
    """Full certification report for one witness."""
    rep = dict(inserted=False, insert_error=None, gold_ok=None, pred_ok=None, gold_error=None,
               pred_error=None, differ={}, L0=False, L1=False, L2=None, fk_violations=[],
               type_problems=[], empty_referenced=[], realism_violations=[], L1f=None, format_violations=[])
    con = sqlite3.connect(':memory:')
    try:
        for stmt in schema.ddl:
            con.executescript(stmt)
        ok, err = load_witness_into(con, schema, witness)
        rep['inserted'], rep['insert_error'] = ok, err
        if not ok:
            return rep
        rep['fk_violations'] = check_fks(con, schema)
        g_ok, g_rows, g_err = run_query(con, gold_sql, timeout_s)
        p_ok, p_rows, p_err = run_query(con, pred_sql, timeout_s)
        rep.update(gold_ok=g_ok, pred_ok=p_ok, gold_error=g_err, pred_error=p_err)
        if g_ok and p_ok:
            rep['differ'] = compare(g_rows, p_rows)
            rep['gold_rows'] = [list(r) for r in g_rows[:20]]
            rep['pred_rows'] = [list(r) for r in p_rows[:20]]
            rep['gold_nrows'], rep['pred_nrows'] = len(g_rows), len(p_rows)
        rep['L0'] = bool(g_ok and p_ok and not rep['fk_violations'])
        rep['type_problems'] = check_type_faithful(con, schema)
        for t in referenced_tables:
            tt = schema.table(t)
            if tt is not None and con.execute(f'SELECT COUNT(*) FROM {qi(tt["name"])}').fetchone()[0] == 0:
                rep['empty_referenced'].append(tt['name'])
        rep['L1'] = rep['L0'] and not rep['type_problems'] and not rep['empty_referenced']
        if formats is not None:
            rep['format_violations'] = formats.violations(con, schema)
            rep['L1f'] = rep['L1'] and not rep['format_violations']
        if realism is not None:
            rep['realism_violations'] = realism.violations(con)
            rep['L2'] = rep['L1'] and not rep['realism_violations']
        return rep
    finally:
        con.close()


def certified(rep, contract='C_set', tier='L1'):
    return bool(rep.get(tier)) and bool(rep.get('differ', {}).get(contract))


def jsonable(rep):
    return json.loads(json.dumps(rep, default=str))


# ----------------------------------------------------------------------------- format faithfulness (L1f)
TEMPORAL_NAME = re.compile(r'(date|birthday|^dob$|time$)', re.I)
TEMPORAL_TEXT = re.compile(r'^(\d{4}-\d{2}-\d{2}([ T]\d{2}:\d{2}(:\d{2}(\.\d+)?)?)?|[+]?\d{1,2}(:\d{2}){1,2}(\.\d+)?|\d{1,2}:\d{2}\.\d+)$')


def shape(v):
    """Coarse lexical shape: digits keep their count, letter runs collapse to 'A'."""
    s = re.sub(r'[0-9]', '9', str(v))
    s = re.sub(r'[A-Za-zÀ-ɏ]+', 'A', s)
    return s


class FormatProfile:
    """Per-column value shapes observed in the official BIRD databases, taken from the categorical
    value samples SpotIt+ mined and published (rule-based constraint files)."""

    def __init__(self, rule_based_json, clean_to_orig, schema: SchemaInfo):
        self.shapes = {}
        c2o = {k.upper(): v for k, v in clean_to_orig.items()}

        def resolve(ref):
            if '__' not in ref:
                return None
            tab, col = ref.split('__', 1)
            t = schema.table(tab)
            if t is None:
                return None
            orig = c2o.get(col.upper(), col)
            idx = _col_resolve(t['columns'], orig)
            if idx is None:
                idx = _col_resolve(t['columns'], col)
            return (t['name'], t['columns'][idx]['name']) if idx is not None else None

        def walk(x):
            if isinstance(x, list):
                for y in x:
                    walk(y)
            elif isinstance(x, dict):
                for k, v in x.items():
                    if k == 'in' and isinstance(v, list) and v and isinstance(v[0], dict):
                        r = resolve(v[0].get('value', ''))
                        if r and all(isinstance(z, str) for z in v[1]):
                            self.shapes.setdefault(r, set()).update(shape(z) for z in v[1])
                            self.samples = getattr(self, 'samples', {})
                            self.samples.setdefault(r, list(v[1]))
                    elif isinstance(v, (list, dict)):
                        walk(v)
        walk(rule_based_json)
        if not hasattr(self, 'samples'):
            self.samples = {}

    def violations(self, con, schema: SchemaInfo):
        out = []
        for t in schema.tables.values():
            for c in t['columns']:
                if c['affinity'] != 'TEXT':
                    continue
                key = (t['name'], c['name'])
                shapes = self.shapes.get(key)
                temporal = c['temporal'] is None and TEMPORAL_NAME.search(c['name']) is not None \
                    and key not in getattr(self, 'free_text', set())
                if not shapes and not temporal:
                    continue
                for (v,) in con.execute(f'SELECT {qi(c["name"])} FROM {qi(t["name"])} WHERE {qi(c["name"])} IS NOT NULL'):
                    if shapes and shape(v) not in shapes:
                        out.append((t['name'], c['name'], 'shape'))
                        break
                    if not shapes and temporal and not TEMPORAL_TEXT.match(str(v)):
                        out.append((t['name'], c['name'], 'temporal_text'))
                        break
        return out


def format_profile_from_db(profiles_db, schema: SchemaInfo):
    """FormatProfile built from data/format_profiles.json (official BIRD databases): every
    non-free-text TEXT column gets its observed shapes and most frequent values."""
    fp = FormatProfile.__new__(FormatProfile)
    fp.shapes, fp.samples, fp.free_text = {}, {}, set()
    for t, cols in profiles_db.items():
        tt = schema.table(t)
        if tt is None:
            continue
        for c, info in cols.items():
            idx = _col_resolve(tt['columns'], c)
            if idx is None:
                continue
            key = (tt['name'], tt['columns'][idx]['name'])
            if info.get('free_text') or not info.get('shapes'):
                fp.free_text.add(key)
                continue
            fp.shapes[key] = set(info['shapes'])
            fp.samples[key] = list(info.get('samples', []))
    return fp
