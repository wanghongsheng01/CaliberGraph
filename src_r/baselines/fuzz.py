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
from cgx.certify import shape, TEMPORAL_NAME, qi
from cgx.sqlinfo import analyze_pair

KEY_INT = [1, 2, 3]
KEY_TXT = ['k1', 'k2', 'k3']


def fuzz(schema, analyzer, gold, pred, budget_s, seed=0, max_rows=5, formats=None, accept=None, never_null=None):
    """accept(db) -> bool: optional certifier-in-the-loop acceptance (post-freeze variants fuzz_cert / fuzz_v5).
    never_null: optional set of (table, column) lower-cased keys that must not receive NULL (fuzz_v5)."""
    nn = never_null or set()
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
        nullable = not c['notnull'] and not c['pk'] and (t.lower(), c['name'].lower()) not in nn
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
            if st == 'ok' and set(rg) != set(rp) and (accept is None or accept({t: r for t, r in db.items() if r})):
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


def fuzz_r(schema, analyzer, gold, pred, budget_s, seed=0, max_rows=5, formats=None, profile_r=None, templates=None,
           real_src=None):
    """Random fuzzing at tier R with the same knowledge as CaliberGraph-R: every candidate is a random
    sub-database of the official database (1..max_rows uniformly drawn real rows per query table,
    closed under foreign keys and total participation with real rows); with probability 1/2 the
    columns the queries touch are then re-drawn from the literals of both queries, the observed
    values of the column and NULL (where observed). The shared constraint repair is applied and a
    candidate is accepted only if the certifier accepts it at L1f and it satisfies every
    data-profile constraint. No predicate-guided retrieval, join-graph completion, isolation or
    growth operators are used."""
    from cgx.search import Config, Generator
    from cgx.certify import certify
    t0 = time.monotonic()
    rng = random.Random(seed)
    pair = analyze_pair(analyzer, gold, pred)
    if not pair.tables:
        return Result(False, note='no_tables', elapsed=time.monotonic() - t0)
    cfg = Config(budget_s=budget_s, formats=formats, profile_r=profile_r, templates=templates,
                 join_graph=False, anchoring=False, isolation=False)
    gen = Generator(schema, pair, cfg, rng)   # used only for value coercion and the shared repair
    qtables = gen.qtables
    qcols = set(pair.gold.columns | pair.pred.columns)
    lits = pair.gold.literals + pair.pred.literals
    cidx = {t: {c: i for i, c in enumerate(gen.colnames[t])} for t in gen.rtables}
    maxid = {}
    if real_src is not None:
        for t in qtables:
            try:
                maxid[t] = real_src.con.execute(f'SELECT MAX(rowid) FROM {qi(t)}').fetchone()[0] or 0
            except Exception:  # noqa: BLE001
                maxid[t] = 0
    fks = []
    for t in gen.rtables:
        for fk in schema.tables[t]['fks']:
            p = fk['ref_table_resolved']
            if p in cidx and len(fk['from_cols']) == 1 and fk['to_cols'] and fk['to_cols'][0] in cidx[p]:
                fks.append((t, fk['from_cols'][0], p, fk['to_cols'][0]))
    fks += [x for x in profile_r.ind_fk if x[0] in cidx and x[2] in cidx]

    def random_rows(t, k):
        if real_src is None or not maxid.get(t):
            return [list(gen.template(t)) for _ in range(k)] if gen.template(t) else []
        ids = sorted({rng.randint(1, maxid[t]) for _ in range(3 * k)})
        rows = real_src.rows(t, f'rowid IN ({",".join(map(str, ids))})', [], limit=k)
        return rows

    def close(db):
        if real_src is None:
            return
        for _ in range(4):
            changed = False
            for a, b, c, d in fks + [(x[0], x[1], x[2], x[3]) for x in profile_r.ind_total]:
                total = (a, b, c, d) in profile_r.ind_total
                if not db.get(a) or c not in db:
                    continue
                have = {r[cidx[c][d]] for r in db[c]}
                for r in list(db[a]):
                    v = r[cidx[a][b]]
                    if v is not None and v not in have:
                        got = real_src.by_value(c, d, v, 1)
                        if got and got[0] not in db[c]:
                            db[c].append(list(got[0]))
                            changed = True
                        have.add(v)
                del total
            if not changed:
                break

    keydom = {}

    def keyvals(r):
        if r not in keydom:
            if r in gen.lookup_keys:
                keydom[r] = gen.lookup_keys[r][:3]
            elif gen.cls_kind[r] in ('int', 'num', 'real', 'mixed'):
                keydom[r] = [1, 2, 3]
            else:
                keydom[r] = [gen.fresh_class(r) for _ in range(3)]
        return keydom[r]

    def perturb(t, row):
        for j, c in enumerate(schema.tables[t]['columns']):
            r = gen.uf.find((t, c['name']))
            if gen.key_class[r]:
                row[j] = rng.choice(keyvals(r))  # small shared key domain so that joins occur
                continue
            if (t, c['name']) not in qcols or rng.random() < 0.3:
                continue
            x = rng.random()
            k = gen.kind[(t, c['name'])]
            if x < 0.4 and lits:
                v = coerce(rng.choice(lits), k)
                if v is not _BAD and profile_r.value_ok(t, c['name'], v):
                    row[j] = v
                    continue
            if x < 0.9:
                vals = gen.real_values(r, 24)
                if vals:
                    row[j] = rng.choice(vals)
                    continue
            if gen.nullable[(t, c['name'])]:
                row[j] = None
        return row

    ev = Evaluator(schema, gold, pred, 0.3)
    counts = {}
    deadline = t0 + budget_s
    try:
        while time.monotonic() < deadline:
            db = {t: [] for t in gen.rtables}
            edit = rng.random() < 0.8
            use_db = rng.random() < 0.5
            for t in qtables:
                k = rng.randint(1, max_rows)
                rows = random_rows(t, k) if use_db else [list(gen.template(t)) for _ in range(k)] if gen.template(t) else []
                for r in rows:
                    db[t].append(perturb(t, list(r)) if edit else list(r))
            close(db)
            gen.repair(db)
            st, rg, rp = ev.eval(db)
            counts[st] = counts.get(st, 0) + 1
            if st == 'ok' and set(rg) != set(rp):
                w = {t: r for t, r in db.items() if r}
                rep = certify(schema, w, gold, pred, referenced_tables=set(qtables), timeout_s=1.0, formats=formats)
                if rep.get('L1f') and rep.get('differ', {}).get('C_set') and profile_r.ok(w):
                    return Result(True, w, ev.n_eval, time.monotonic() - t0, 'fuzz_r', counts)
                counts['reject'] = counts.get('reject', 0) + 1
        return Result(False, None, ev.n_eval, time.monotonic() - t0, None, counts)
    finally:
        ev.close()
