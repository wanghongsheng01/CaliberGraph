"""Static analysis of a (gold, predicted) SQL pair for CGX.

Produces, for each query: resolved table references, resolved column references, column
equalities (join graph edges), comparison atoms with literals, and simple structural flags.
For the pair: anchor columns/literals from the symmetric difference of normalized atoms and
structural features (the "diff anchors").
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import sqlglot
from sqlglot import exp

CMP = {exp.EQ: '=', exp.NEQ: '!=', exp.GT: '>', exp.GTE: '>=', exp.LT: '<', exp.LTE: '<='}
FLIP = {'=': '=', '!=': '!=', '>': '<', '>=': '<=', '<': '>', '<=': '>='}


@dataclass
class Atom:
    col: tuple | None          # resolved (table, column) of the column operand
    op: str                    # '=', '<', 'like', 'in', 'between', 'isnull', 'notnull', ...
    values: list               # literal operands (python values)
    wrapper: str | None        # function wrapper on the column side, e.g. 'year', 'substr:1:4', 'lower'
    text: str                  # normalized text, used for diffing
    negated: bool = False


@dataclass
class QueryInfo:
    sql: str
    ok: bool = True
    error: str | None = None
    tables: set = field(default_factory=set)            # real schema table names
    aliases: dict = field(default_factory=dict)
    columns: set = field(default_factory=set)           # resolved (table, col)
    proj_columns: set = field(default_factory=set)
    order_columns: set = field(default_factory=set)
    group_columns: set = field(default_factory=set)
    agg_columns: set = field(default_factory=set)
    equalities: list = field(default_factory=list)      # ((t,c),(t,c))
    atoms: list = field(default_factory=list)
    literals: list = field(default_factory=list)        # all literal values
    flags: dict = field(default_factory=dict)
    string_fallbacks: set = field(default_factory=set)  # double-quoted tokens SQLite treats as strings


def _lit_value(node):
    if isinstance(node, exp.Literal):
        if node.is_string:
            return node.this
        t = node.this
        try:
            return int(t)
        except ValueError:
            try:
                return float(t)
            except ValueError:
                return t
    if isinstance(node, exp.Null):
        return None
    if isinstance(node, exp.Boolean):
        return 1 if node.this else 0
    if isinstance(node, exp.Neg) and isinstance(node.this, exp.Literal) and not node.this.is_string:
        v = _lit_value(node.this)
        return -v if isinstance(v, (int, float)) else None
    return _NOLIT


_NOLIT = object()


class Analyzer:
    def __init__(self, schema):
        self.schema = schema
        self.colmap = {}   # lower col name -> list of (table, col)
        for t in schema.tables.values():
            for c in t['columns']:
                self.colmap.setdefault(c['name'].lower(), []).append((t['name'], c['name']))

    # ------------------------------------------------------------------ helpers
    def _resolve(self, col: exp.Column, aliases, scope_tables):
        name = col.name
        qual = col.table
        if qual:
            t = aliases.get(qual.lower())
            if t is None:
                tt = self.schema.table(qual)
                t = tt['name'] if tt else None
            if t is None:
                return None
            for c in self.schema.table(t)['columns']:
                if c['name'].lower() == name.lower():
                    return (t, c['name'])
            return None
        cands = [tc for tc in self.colmap.get(name.lower(), []) if tc[0] in scope_tables]
        if len(cands) >= 1:
            return cands[0]
        return None

    def analyze(self, sql: str) -> QueryInfo:
        qi = QueryInfo(sql=sql)
        try:
            tree = sqlglot.parse_one(sql, read='sqlite')
        except Exception as e:  # noqa: BLE001
            qi.ok, qi.error = False, f'parse: {e}'
            # regex fallback for tables
            for t in self.schema.tables:
                if re.search(r'\b' + re.escape(t) + r'\b', sql, re.I):
                    qi.tables.add(t)
            return qi
        cte_names = {c.alias_or_name.lower() for c in tree.find_all(exp.CTE)}
        for tnode in tree.find_all(exp.Table):
            if tnode.name.lower() in cte_names:
                continue
            tt = self.schema.table(tnode.name)
            if tt is None:
                continue
            qi.tables.add(tt['name'])
            qi.aliases[tnode.alias_or_name.lower()] = tt['name']
            qi.aliases[tnode.name.lower()] = tt['name']
        scope = qi.tables
        resolved = {}
        for col in tree.find_all(exp.Column):
            r = self._resolve(col, qi.aliases, scope)
            if r is None:
                if not col.table and col.this is not None and getattr(col.this, 'quoted', False):
                    qi.string_fallbacks.add(col.name)
                continue
            resolved[id(col)] = r
            qi.columns.add(r)
        self._resolved = resolved

        def rc(node):
            if isinstance(node, exp.Column):
                return resolved.get(id(node))
            return None

        # flags & role columns
        sel = tree if isinstance(tree, exp.Select) else tree.find(exp.Select)
        qi.flags['distinct'] = bool(sel and sel.args.get('distinct'))
        qi.flags['limit'] = None
        if sel and sel.args.get('limit') is not None:
            lim = sel.args['limit'].expression
            qi.flags['limit'] = _lit_value(lim) if lim is not None else None
        qi.flags['offset'] = 0
        if sel and sel.args.get('offset') is not None:
            off = _lit_value(sel.args['offset'].expression)
            qi.flags['offset'] = off if isinstance(off, int) else 0
        # numeric thresholds in HAVING (e.g. HAVING COUNT(x) > 7) -> group sizes worth building
        qi.flags['having_thresholds'] = []
        if sel and sel.args.get('having') is not None:
            for lit in sel.args['having'].find_all(exp.Literal):
                v = _lit_value(lit)
                if isinstance(v, int) and 0 < v <= 30:
                    qi.flags['having_thresholds'].append(v)
        qi.flags['order'] = bool(sel and sel.args.get('order'))
        qi.flags['group'] = bool(sel and sel.args.get('group'))
        qi.flags['agg'] = any(True for _ in tree.find_all(exp.AggFunc))
        qi.flags['subquery'] = any(True for _ in tree.find_all(exp.Subquery)) or \
            any(isinstance(x.args.get('query'), exp.Select) for x in tree.find_all(exp.In))
        qi.flags['left_join'] = any((j.args.get('side') or '').upper() == 'LEFT' for j in tree.find_all(exp.Join))
        qi.flags['n_proj'] = len(sel.expressions) if sel else None
        qi.flags['window'] = any(True for _ in tree.find_all(exp.Window))
        qi.flags['setop'] = any(isinstance(x, (exp.Union, exp.Except, exp.Intersect)) for x in tree.walk())
        if sel:
            for e in sel.expressions:
                for c in e.find_all(exp.Column):
                    if rc(c):
                        qi.proj_columns.add(rc(c))
            if sel.args.get('order'):
                for c in sel.args['order'].find_all(exp.Column):
                    if rc(c):
                        qi.order_columns.add(rc(c))
            if sel.args.get('group'):
                for c in sel.args['group'].find_all(exp.Column):
                    if rc(c):
                        qi.group_columns.add(rc(c))
        for a in tree.find_all(exp.AggFunc):
            for c in a.find_all(exp.Column):
                if rc(c):
                    qi.agg_columns.add(rc(c))

        # literals
        for lit in tree.find_all(exp.Literal):
            v = _lit_value(lit)
            if v is not _NOLIT:
                qi.literals.append(v)
        for s in qi.string_fallbacks:
            qi.literals.append(s)

        # equalities between columns (join graph), incl. IN (SELECT col ...)
        for node in tree.find_all(exp.EQ):
            a, b = rc(node.left), rc(node.right)
            if a and b and a != b:
                qi.equalities.append((a, b))
        for node in tree.find_all(exp.In):
            q = node.args.get('query')
            left = rc(node.this)
            if left and q is not None:
                inner = q.this if isinstance(q, exp.Subquery) else q
                if isinstance(inner, exp.Select) and len(inner.expressions) == 1:
                    cols = list(inner.expressions[0].find_all(exp.Column))
                    if len(cols) == 1 and rc(cols[0]):
                        qi.equalities.append((left, rc(cols[0])))
        # comparison atoms
        for node in tree.walk():
            atom = self._atom(node, rc)
            if atom is not None:
                qi.atoms.append(atom)
        return qi

    def _unwrap(self, node, rc):
        """Return ((table,col), wrapper) when node is a column possibly inside a simple function."""
        c = rc(node)
        if c:
            return c, None
        if isinstance(node, (exp.Paren,)):
            return self._unwrap(node.this, rc)
        if isinstance(node, exp.Cast):
            c, w = self._unwrap(node.this, rc)
            return (c, w or 'cast') if c else (None, None)
        if isinstance(node, (exp.Lower, exp.Upper, exp.Trim)):
            c, w = self._unwrap(node.this, rc)
            return (c, type(node).__name__.lower()) if c and w is None else (None, None)
        if isinstance(node, exp.TimeToStr):
            fmt = node.args.get('format')
            fmt = fmt.this if isinstance(fmt, exp.Literal) else None
            inner = node.this
            if isinstance(inner, (exp.TsOrDsToTimestamp, exp.TsOrDsToDate, exp.StrToTime, exp.Date)):
                inner = inner.this
            c, w = self._unwrap(inner, rc)
            return (c, f'strftime:{fmt}') if c and w is None else (None, None)
        if isinstance(node, exp.Substring):
            c, w = self._unwrap(node.this, rc)
            st = _lit_value(node.args.get('start')) if node.args.get('start') is not None else 1
            ln = _lit_value(node.args.get('length')) if node.args.get('length') is not None else None
            if c and w is None and isinstance(st, int):
                return c, f'substr:{st}:{ln if isinstance(ln, int) else ""}'
            return None, None
        if isinstance(node, (exp.Date, exp.TsOrDsToDate, exp.TsOrDsToTimestamp)):
            c, w = self._unwrap(node.this, rc)
            return (c, 'date') if c and w is None else (None, None)
        if isinstance(node, (exp.Add, exp.Sub, exp.Mul, exp.Div)):
            l, r = node.left, node.right
            lv, rv = _lit_value(l), _lit_value(r)
            if isinstance(rv, (int, float)) and not isinstance(rv, bool):
                c, w = self._unwrap(l, rc)
                if c and w is None:
                    return c, f'{type(node).__name__.lower()}:{rv}'
        return None, None

    def _atom(self, node, rc):
        neg = False
        if isinstance(node, exp.Not) and isinstance(node.this, (exp.In, exp.Like, exp.Between, exp.Is)):
            return None  # handled when visiting the child (negation recorded there)
        parent_not = isinstance(node.parent, exp.Not)
        if type(node) in CMP:
            l, r = node.left, node.right
            lv, rv = _lit_value(l), _lit_value(r)
            op = CMP[type(node)]
            if rv is not _NOLIT and lv is _NOLIT:
                c, w = self._unwrap(l, rc)
                if c:
                    return Atom(c, op, [rv], w, self._norm(node), parent_not)
            if lv is not _NOLIT and rv is _NOLIT:
                c, w = self._unwrap(r, rc)
                if c:
                    return Atom(c, FLIP[op], [lv], w, self._norm(node), parent_not)
            # comparison to a double-quoted string fallback
            if isinstance(r, exp.Column) and rc(r) is None and r.name and not r.table:
                c, w = self._unwrap(l, rc)
                if c:
                    return Atom(c, op, [r.name], w, self._norm(node), parent_not)
            return None
        if isinstance(node, (exp.Like, exp.ILike)):
            c, w = self._unwrap(node.this, rc)
            pv = _lit_value(node.expression)
            if c and isinstance(pv, str):
                return Atom(c, 'like', [pv], w, self._norm(node), parent_not)
            return None
        if isinstance(node, exp.In) and node.args.get('expressions'):
            c, w = self._unwrap(node.this, rc)
            vals = [_lit_value(e) for e in node.expressions]
            vals = [v for v in vals if v is not _NOLIT]
            if c and vals:
                return Atom(c, 'in', vals, w, self._norm(node), parent_not)
            return None
        if isinstance(node, exp.Between):
            c, w = self._unwrap(node.this, rc)
            lo, hi = _lit_value(node.args.get('low')), _lit_value(node.args.get('high'))
            if c and lo is not _NOLIT and hi is not _NOLIT:
                return Atom(c, 'between', [lo, hi], w, self._norm(node), parent_not)
            return None
        if isinstance(node, exp.Is):
            c, w = self._unwrap(node.this, rc)
            if c and isinstance(node.expression, exp.Null):
                return Atom(c, 'notnull' if parent_not else 'isnull', [], w, self._norm(node), False)
            return None
        return None

    def _norm(self, node):
        try:
            return _render_resolved(node, self._resolved)
        except Exception:  # noqa: BLE001
            return node.sql('sqlite').lower()


def _render_resolved(node, resolved):
    # copy() loses node identities, so render by walking the original tree
    s = node.sql('sqlite')
    for col in node.find_all(exp.Column):
        if id(col) in resolved:
            t, c = resolved[id(col)]
            s = s.replace(col.sql('sqlite'), f'{t}.{c}'.lower(), 1)
    return re.sub(r'\s+', ' ', s.lower())


@dataclass
class PairInfo:
    gold: QueryInfo
    pred: QueryInfo
    tables: set
    anchor_columns: set
    anchor_atoms: list
    structural: dict


def analyze_pair(analyzer: Analyzer, gold_sql: str, pred_sql: str) -> PairInfo:
    g, p = analyzer.analyze(gold_sql), analyzer.analyze(pred_sql)
    tables = set(g.tables) | set(p.tables)
    gt = {a.text for a in g.atoms}
    pt = {a.text for a in p.atoms}
    anchor_atoms = [a for a in g.atoms if a.text not in pt] + [a for a in p.atoms if a.text not in gt]
    anchors = {a.col for a in anchor_atoms if a.col}
    # structural anchors: columns used differently in projection/order/group/aggregation
    for attr in ('proj_columns', 'order_columns', 'group_columns', 'agg_columns'):
        anchors |= set(getattr(g, attr)) ^ set(getattr(p, attr))
    anchors |= (g.columns ^ p.columns)
    structural = {}
    for k in ('distinct', 'limit', 'order', 'group', 'agg', 'left_join', 'n_proj', 'subquery', 'window', 'setop'):
        structural[k] = (g.flags.get(k), p.flags.get(k))
    structural['tables_differ'] = g.tables != p.tables
    return PairInfo(g, p, tables, anchors, anchor_atoms, structural)
