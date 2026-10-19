"""Random DDL-valid database fuzzing baseline (test-suite style, Zhong et al. 2020).

For each candidate database, every referenced table receives 1..max_rows random rows. Column
values are drawn from (i) the literals of BOTH queries that fit the column type, (ii) generic
type-faithful values, (iii) NULL for nullable columns. Key/join columns draw from a tiny shared
domain so that joins happen by coincidence. PKs are kept unique and FK parents are added, so
every candidate satisfies the DDL. No join-graph linking, diff anchoring or isolation is used.
"""
import random
import time

from cgx.search import Evaluator, Result, coerce, col_kind, GENERIC, _BAD
from cgx.certify import shape, TEMPORAL_NAME
from cgx.sqlinfo import analyze_pair

KEY_INT = [1, 2, 3]
KEY_TXT = ['k1', 'k2', 'k3']


def fuzz(schema, analyzer, gold, pred, budget_s, seed=0, max_rows=5, formats=None):
    t0 = time.monotonic()
    rng = random.Random(seed)
    pair = analyze_pair(analyzer, gold, pred)
    qtables = sorted(pair.tables)
    if not qtables:
        return Result(False, note='no_tables', elapsed=time.monotonic() - t0)
    rel, stack = set(qtables), list(qtables)
    while stack:
        t = stack.pop()
        for fk in schema.tables[t]['fks']:
            p = fk['ref_table_resolved']
            if p and p not in rel:
                rel.add(p)
                stack.append(p)
    rtables = sorted(rel)
    keycols = set()
    for t in rtables:
        for c in schema.tables[t]['columns']:
            if c['pk']:
                keycols.add((t, c['name']))
        for fk in schema.tables[t]['fks']:
            for a, b in zip(fk['from_cols'], fk['to_cols']):
                keycols.add((t, a))
                if fk['ref_table_resolved'] and b:
                    keycols.add((fk['ref_table_resolved'], b))
    for a, b in pair.gold.equalities + pair.pred.equalities:
        keycols.add(a)
        keycols.add(b)
    lits = pair.gold.literals + pair.pred.literals

    def pool(t, c):
        k = col_kind(c)
        key = (t, c['name'])
        shp = formats.shapes.get(key) if formats is not None and c['affinity'] == 'TEXT' else None
        if not shp and c['affinity'] == 'TEXT' and c['temporal'] is None and TEMPORAL_NAME.search(c['name']):
            k = 'tdate'
        vals = []
        for v in lits:
            x = coerce(v, k)
            if x is not _BAD and x not in vals and (not shp or not isinstance(x, str) or shape(x) in shp):
                vals.append(x)
        if shp:  # same domain knowledge as every method: observed value samples of the column
            vals += [x for x in formats.samples.get(key, [])[:8] if x not in vals]
        return k, vals

    pools = {(t, c['name']): pool(t, c) for t in rtables for c in schema.tables[t]['columns']}

    def value(t, c):
        k, vals = pools[(t, c['name'])]
        nullable = not c['notnull'] and not c['pk']
        if (t, c['name']) in keycols:
            v = rng.choice(KEY_INT if k in ('int', 'num', 'real') else KEY_TXT)
            if vals and rng.random() < 0.3:
                v = rng.choice(vals)
            x = coerce(v, k)
            return x if x is not _BAD else rng.choice(GENERIC[k] if k in GENERIC else GENERIC['text'])
        r = rng.random()
        if nullable and r < 0.1:
            return None
        if vals and r < 0.6:
            return rng.choice(vals)
        if formats is not None and (t, c['name']) in formats.shapes and vals:
            return rng.choice(vals)
        return rng.choice(GENERIC[k] if k in GENERIC else GENERIC['text'])

    ev = Evaluator(schema, gold, pred, 0.3)
    counts = {}
    deadline = t0 + budget_s
    try:
        while time.monotonic() < deadline:
            db = {t: [] for t in rtables}
            for t in qtables:
                cols = schema.tables[t]['columns']
                pki = [i for i, c in enumerate(cols) if c['pk']]
                seen = set()
                for _ in range(rng.randint(1, max_rows)):
                    row = [value(t, c) for c in cols]
                    key = tuple(row[i] for i in pki)
                    if pki and key in seen:
                        continue
                    seen.add(key)
                    db[t].append(row)
            _repair_fks(schema, db, rtables, value, rng)
            st, rg, rp = ev.eval(db)
            counts[st] = counts.get(st, 0) + 1
            if st == 'ok' and set(rg) != set(rp):
                return Result(True, {t: r for t, r in db.items() if r}, ev.n_eval, time.monotonic() - t0,
                              'fuzz', counts)
        return Result(False, None, ev.n_eval, time.monotonic() - t0, None, counts)
    finally:
        ev.close()


def _repair_fks(schema, db, rtables, value, rng):
    for _ in range(4):
        changed = False
        for t in rtables:
            tcols = [c['name'] for c in schema.tables[t]['columns']]
            for fk in schema.tables[t]['fks']:
                p = fk['ref_table_resolved']
                if p not in db:
                    continue
                pcols_meta = schema.tables[p]['columns']
                pcols = [c['name'] for c in pcols_meta]
                try:
                    fi = [tcols.index(a) for a in fk['from_cols']]
                    ti = [pcols.index(b) for b in fk['to_cols']]
                except (ValueError, TypeError):
                    continue
                have = {tuple(r[i] for i in ti) for r in db[p]}
                pki = [j for j, c in enumerate(pcols_meta) if c['pk']]
                for row in db[t]:
                    key = tuple(row[i] for i in fi)
                    if any(v is None for v in key) or key in have:
                        continue
                    newrow = [value(p, c) for c in pcols_meta]
                    for j, v in zip(ti, key):
                        newrow[j] = v
                    pkeys = {tuple(r[j] for j in pki) for r in db[p]}
                    if pki and tuple(newrow[j] for j in pki) in pkeys:
                        continue
                    db[p].append(newrow)
                    have.add(key)
                    changed = True
        if not changed:
            break
    # FK children whose parent could not be created are removed (keeps DDL validity)
    for _ in range(4):
        removed = False
        for t in rtables:
            tcols = [c['name'] for c in schema.tables[t]['columns']]
            for fk in schema.tables[t]['fks']:
                p = fk['ref_table_resolved']
                if p not in db:
                    continue
                pcols = [c['name'] for c in schema.tables[p]['columns']]
                try:
                    fi = [tcols.index(a) for a in fk['from_cols']]
                    ti = [pcols.index(b) for b in fk['to_cols']]
                except (ValueError, TypeError):
                    continue
                have = {tuple(r[i] for i in ti) for r in db[p]}
                keep = [r for r in db[t] if any(r[i] is None for i in fi) or tuple(r[i] for i in fi) in have]
                if len(keep) != len(db[t]):
                    db[t] = keep
                    removed = True
        if not removed:
            break
