"""Rule-based root-cause labels for certified non-equivalences (RQ3).

Labels are multi-valued and derived from (i) structural differences between the two queries and
(ii) the observed outputs on the certified witness. They are heuristics; a random sample is
checked by hand (docs/03) and the agreement rate is reported.
"""
import re

from cgx.sqlinfo import analyze_pair

LABELS = ['empty_aggregate', 'null_semantics', 'duplicates_distinct', 'order_limit_ties',
          'numeric_type_division', 'filter_predicate', 'join_path', 'projection', 'grouping', 'other']


def _has_null(rows):
    return any(v is None for r in rows for v in r)


def label(analyzer, gold, pred, cert):
    p = analyze_pair(analyzer, gold, pred)
    g, q = p.gold, p.pred
    s = p.structural
    gr, pr = cert.get('gold_rows') or [], cert.get('pred_rows') or []
    gn, pn = cert.get('gold_nrows', len(gr)), cert.get('pred_nrows', len(pr))
    out = set()
    # empty-result semantics: [] vs one all-NULL row (or 0 for COUNT)
    # empty selection: one side returns no row, the other one all-NULL row produced by an aggregate
    if (gn == 0 and pn == 1 and all(v is None for v in pr[0]) and q.flags.get('agg')) or \
            (pn == 0 and gn == 1 and all(v is None for v in gr[0]) and g.flags.get('agg')):
        out.add('empty_aggregate')
    elif s['agg'][0] != s['agg'][1] and (gn == 0 or pn == 0):
        out.add('empty_aggregate')
    # NULL semantics
    gnull = {a.text for a in g.atoms if a.op in ('isnull', 'notnull')}
    pnull = {a.text for a in q.atoms if a.op in ('isnull', 'notnull')}
    if gnull != pnull or ('empty_aggregate' not in out and _has_null(gr) != _has_null(pr)):
        out.add('null_semantics')
    if bool(re.search(r'count\s*\(\s*\*\s*\)', gold, re.I)) != bool(re.search(r'count\s*\(\s*\*\s*\)', pred, re.I)) and \
            (_has_null(gr) or _has_null(pr) or 'count' in gold.lower()):
        out.add('null_semantics')
    # duplicates / DISTINCT
    if s['distinct'][0] != s['distinct'][1] or \
            (len(re.findall(r'distinct', gold, re.I)) != len(re.findall(r'distinct', pred, re.I))):
        out.add('duplicates_distinct')
    if set(map(tuple, gr)) == set(map(tuple, pr)) and gn != pn:
        out.add('duplicates_distinct')
    # ordering / LIMIT ties
    if s['limit'][0] is not None or s['limit'][1] is not None:
        if s['limit'][0] != s['limit'][1]:
            out.add('order_limit_ties')
        elif gn == pn and gn > 0 and set(map(tuple, gr)) != set(map(tuple, pr)) and \
                (g.order_columns == q.order_columns or not p.anchor_atoms):
            out.add('order_limit_ties')
    # numeric type / integer division
    if (re.search(r'cast\s*\(.*as\s+(real|float)', gold, re.I) is None) != \
            (re.search(r'cast\s*\(.*as\s+(real|float)', pred, re.I) is None) or \
            ('100.0' in gold) != ('100.0' in pred):
        out.add('numeric_type_division')
    # predicates
    if any(a.op not in ('isnull', 'notnull') for a in p.anchor_atoms):
        out.add('filter_predicate')
    if s['tables_differ'] or {frozenset(e) for e in g.equalities} != {frozenset(e) for e in q.equalities}:
        out.add('join_path')
    if s['n_proj'][0] != s['n_proj'][1] or g.proj_columns != q.proj_columns:
        out.add('projection')
    if s['group'][0] != s['group'][1] or g.group_columns != q.group_columns:
        out.add('grouping')
    if not out:
        out.add('other')
    return sorted(out)
