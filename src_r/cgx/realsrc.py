"""Real-row access for CaliberGraph-R: retrieval of rows of the official database that satisfy (or
violate) the predicates of either query, and completion of such rows along the join graph into a
small sub-database whose rows are all real. Read-only; every query has a short time limit.
"""
import sqlite3
import time

from .certify import qi


def atom_sql(a):
    """SQL predicate for an atom on its (unqualified) column, or None if not translatable."""
    if a.col is None:
        return None, []
    c = qi(a.col[1])
    w = a.wrapper or ''
    if not w:
        e = c
    elif w.startswith('strftime:'):
        e = f"strftime('{w.split(':', 1)[1]}', {c})"
    elif w.startswith('substr:'):
        parts = w.split(':')
        e = f'substr({c}, {int(parts[1])}' + (f', {int(parts[2])})' if parts[2] else ')')
    elif w in ('lower', 'upper', 'trim'):
        e = f'{w}({c})'
    elif w.startswith(('add:', 'sub:', 'mul:', 'div:')):
        op = {'add': '+', 'sub': '-', 'mul': '*', 'div': '/'}[w.split(':')[0]]
        e = f'({c} {op} {float(w.split(":")[1])})'
    else:
        return None, []
    v = list(a.values)
    if a.op == 'isnull':
        s, p = f'{e} IS NULL', []
    elif a.op == 'notnull':
        s, p = f'{e} IS NOT NULL', []
    elif a.op == 'in' and v:
        s, p = f'{e} IN ({",".join("?" * len(v))})', v
    elif a.op == 'between' and len(v) == 2:
        s, p = f'{e} BETWEEN ? AND ?', v
    elif a.op == 'like' and v:
        s, p = f'{e} LIKE ?', v[:1]
    elif a.op in ('=', '!=', '<', '<=', '>', '>=') and v:
        s, p = f'{e} {a.op} ?', v[:1]
    else:
        return None, []
    if a.negated:
        s = f'NOT ({s})'
    return s, p


def conj(atoms):
    parts, params = [], []
    for a in atoms:
        s, p = atom_sql(a)
        if s:
            parts.append(f'({s})')
            params += p
    return (' AND '.join(parts) if parts else '1'), params


class RealSource:
    def __init__(self, path, schema, timeout_s=0.15, seed=0):
        self.con = sqlite3.connect(f'file:{path}?mode=ro', uri=True, check_same_thread=False)
        self.s = schema
        self.timeout_s = timeout_s
        self.seed = seed
        self.cache = {}
        self.sel = {t: ', '.join(qi(c['name']) for c in ti['columns']) for t, ti in schema.tables.items()}
        self.n_queries = 0

    def close(self):
        self.con.close()

    def rows(self, t, where='1', params=(), limit=10, order=None):
        key = (t, where, tuple(map(repr, params)), limit, order)
        if key in self.cache:
            return self.cache[key]
        if order is None:
            order = f'((rowid * 1103515245 + {12345 + self.seed}) % 2147483647)'
        sql = f'SELECT {self.sel[t]} FROM {qi(t)} WHERE {where} ORDER BY {order} LIMIT {int(limit)}'
        deadline = time.monotonic() + self.timeout_s
        self.con.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 1000)
        self.n_queries += 1
        try:
            out = [list(r) for r in self.con.execute(sql, list(params)).fetchall()]
        except sqlite3.Error:
            out = []
        finally:
            self.con.set_progress_handler(None, 0)
        self.cache[key] = out
        return out

    def by_value(self, t, c, v, limit=3, where='1', params=()):
        if v is None:
            return []
        return self.rows(t, f'{qi(c)} = ? AND ({where})', [v] + list(params), limit)
