"""Exploratory analysis X1 (repair test), specified in docs/en/17a_stage3_amendments.md, E4,
before it was run.

For every attributed test witness, the cells that violate the mined data profile (tier A_R) are
repaired locally with real values, and the frozen certifier checks whether gold and prediction
still differ on the repaired variants.

Usage: python src_s3/x1_repair.py [--procs 2]
Output:
  results/stage3/x1_repair_items.jsonl   one row per witness
  results/stage3/x1_repair.json          cross-tabulations
"""
import argparse
import json
import multiprocessing as mp
import os
import random
import re
import sqlite3
import sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src_r'))
from cgx.certify import SchemaInfo, certify  # noqa: E402
from cgx.profile_r import _k  # noqa: E402
from run_method import load_profile_r, referenced_tables  # noqa: E402
from cgx.sqlinfo import Analyzer  # noqa: E402
from human_validation import final, parse  # noqa: E402
from run_method import _qcols  # noqa: E402
import ast  # noqa: E402

K = 20
MAX_STEPS = 200  # base; the cap is MAX_STEPS + 5 x (violations after the fill step), amendment E5
MAX_VALUES = 500
_S = {}


def q(x):
    return '"' + x.replace('"', '""') + '"'


def init():
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    _S['schemas'] = {db: SchemaInfo(s) for db, s in ddl.items()}
    _S['an'] = {db: Analyzer(s) for db, s in _S['schemas'].items()}
    _S['prof'], _S['tmpl'] = load_profile_r(_S['schemas'])
    _S['vals'] = {}
    _S['con'] = {}


def real_values(db, t, c):
    key = (db, t, c)
    if key not in _S['vals']:
        prf = _S['prof'][db]
        if (t, c) in prf.dom:
            v = sorted(prf.dom[(t, c)], key=repr)[:MAX_VALUES]
        else:
            if db not in _S['con']:
                p = os.path.join(ROOT, 'data', 'official', 'dev_databases', db, f'{db}.sqlite')
                _S['con'][db] = sqlite3.connect(f'file:{p}?mode=ro', uri=True)
            v = [r[0] for r in _S['con'][db].execute(
                f'SELECT DISTINCT {q(c)} FROM {q(t)} WHERE {q(c)} IS NOT NULL LIMIT {MAX_VALUES}')]
        _S['vals'][key] = v
    return _S['vals'][key]


def structured(prf, w):
    """Violations of the frozen ProfileR as (kind, data) tuples; mirrors ProfileR.violations."""
    out = []
    s = prf.s
    cols = {t: [c['name'] for c in s.tables[t]['columns']] for t in w}
    for t, rows in w.items():
        for ri, r in enumerate(rows):
            for ci, (c, v) in enumerate(zip(cols[t], r)):
                if not prf.value_ok(t, c, v):
                    out.append(('value', t, ri, ci))
        if t in prf.lookup:
            for ri, r in enumerate(rows):
                if tuple(r) not in prf.lookup[t]:
                    out.append(('lookup', t, ri))

    def vals(t, c):
        if t not in w:
            return None
        i = cols[t].index(c)
        return [r[i] for r in w[t]]
    for t, cs in prf.ucc:
        if t not in w or None in cs:
            continue
        idx = [cols[t].index(c) for c in cs]
        seen = set()
        for ri, r in enumerate(w[t]):
            k = tuple(r[i] for i in idx)
            if any(x is None for x in k):
                continue
            if k in seen:
                out.append(('ucc', t, ri, idx))
                break
            seen.add(k)
    for a, b, c, d in prf.ind_fk:
        ch = vals(a, b)
        if not ch:
            continue
        par = set(vals(c, d) or [])
        for ri, x in enumerate(ch):
            if x is not None and x not in par:
                out.append(('fk', a, b, c, d, ri, x))
                break
    for a, b, c, d in prf.ind_total:
        par = vals(a, b)
        if not par:
            continue
        ch = set(vals(c, d) or [])
        for x in par:
            if x is not None and x not in ch:
                out.append(('total', a, b, c, d, x))
                break
    for t, a, b in prf.symmetric:
        if t not in w:
            continue
        ia, ib = cols[t].index(a), cols[t].index(b)
        pairs = {(r[ia], r[ib]) for r in w[t]}
        for ri, r in enumerate(w[t]):
            x, y = r[ia], r[ib]
            if x is not None and y is not None and (y, x) not in pairs:
                out.append(('symmetric', t, ri, ia, ib))
                break
    for t, a, b in prf.irreflexive:
        if t not in w:
            continue
        ia, ib = cols[t].index(a), cols[t].index(b)
        for ri, r in enumerate(w[t]):
            if r[ia] is not None and r[ia] == r[ib]:
                out.append(('irreflexive', t, ri, ib))
                break
    for fi, (t, x, y, m) in enumerate(prf.fd):
        if t not in w:
            continue
        ix, iy = cols[t].index(x), cols[t].index(y)
        for ri, r in enumerate(w[t]):
            k = _k(r[ix])
            if r[ix] is not None and k in m and m[k] != r[iy] and not (
                    m[k] is not None and r[iy] is not None and str(m[k]) == str(r[iy])):
                out.append(('fd', t, ri, iy, m[k], fi))
                break
    for cj, (t, x, b, p, y, d) in enumerate(prf.cross):
        if t not in w or p not in w:
            continue
        ix, ib = cols[t].index(x), cols[t].index(b)
        iy, idd = cols[p].index(y), cols[p].index(d)
        par = {}
        for r in w[p]:
            par.setdefault(r[idd], []).append(r[iy])
        for ri, r in enumerate(w[t]):
            ys = par.get(r[ib])
            if ys and r[ix] is not None and any(v is not None and v != r[ix] for v in ys):
                out.append(('cross', t, ri, ix, next(v for v in ys if v is not None), cj))
                break
    for t, y, d in prf.year_date:
        if t not in w:
            continue
        iy, idd = cols[t].index(y), cols[t].index(d)
        for ri, r in enumerate(w[t]):
            if r[iy] is None or r[idd] is None:
                continue
            try:
                if int(str(r[idd])[:4]) != int(r[iy]):
                    out.append(('year_date', t, ri, iy, int(str(r[idd])[:4])))
                    break
            except ValueError:
                out.append(('value', t, ri, idd))
                break
    return out


def template_row(db, t, rng):
    rows = _S['tmpl'][db].get(t) or []
    return list(rng.choice(rows)) if rows else None


def rev_fd(m):
    r = {}
    for k, v in m.items():
        try:
            kv = ast.literal_eval(k) if not isinstance(k, str) or k[:1] in "-0123456789'\"" else k
        except (ValueError, SyntaxError):
            kv = k
        r.setdefault(_k(v) if v is not None else None, []).append(kv)
    return r


def repair_once(db, w0, rng, refcols):
    """refcols: lower-cased (table, column) pairs referenced by gold or prediction (amendment E5)."""
    prf = _S['prof'][db]
    s = _S['schemas'][db]
    w = {t: [list(r) for r in rows] for t, rows in w0.items()}
    ref = lambda t, c: (t.lower(), c.lower()) in refcols  # noqa: E731
    # fill step (E5): columns no query references take the values of one real template row of the table
    for t, rows in w.items():
        cn = [c['name'] for c in s.tables[t]['columns']]
        for r in rows:
            tr = template_row(db, t, rng)
            if tr is None:
                continue
            for i, c in enumerate(cn):
                if not ref(t, c):
                    r[i] = tr[i]
    cap = MAX_STEPS + 5 * len(structured(prf, w))
    for _ in range(cap):
        v = structured(prf, w)
        if not v:
            return w if prf.ok(w) else None
        x = rng.choice(v)
        kind = x[0]
        cols = lambda t: [c['name'] for c in s.tables[t]['columns']]  # noqa: E731
        if kind == 'value':
            _, t, ri, ci = x
            rv = real_values(db, t, cols(t)[ci])
            if not rv:
                return None
            w[t][ri][ci] = rng.choice(rv)
        elif kind == 'lookup':
            _, t, ri = x
            lr = prf.lookup_rows.get(t) or []
            if not lr:
                return None
            same = [r for r in lr if r[0] == w[t][ri][0]]
            w[t][ri] = list(rng.choice(same or lr))
        elif kind == 'ucc':
            _, t, ri, idx = x
            for i in idx:
                rv = real_values(db, t, cols(t)[i])
                if not rv:
                    return None
                w[t][ri][i] = rng.choice(rv)
        elif kind == 'fk':
            _, a, b, c, d, ri, val = x
            ib = cols(a).index(b)
            par = [r[cols(c).index(d)] for r in w.get(c, []) if r[cols(c).index(d)] is not None]
            if par:
                w[a][ri][ib] = rng.choice(par)
            else:
                tr = template_row(db, c, rng)
                if tr is None:
                    return None
                tr[cols(c).index(d)] = val
                w.setdefault(c, []).append(tr)
        elif kind == 'total':
            _, a, b, c, d, val = x
            tr = template_row(db, c, rng)
            if tr is None:
                return None
            tr[cols(c).index(d)] = val
            w.setdefault(c, []).append(tr)
        elif kind == 'symmetric':
            _, t, ri, ia, ib = x
            r = list(w[t][ri])
            r[ia], r[ib] = r[ib], r[ia]
            w[t].append(r)
        elif kind == 'irreflexive':
            _, t, ri, ib = x
            rv = real_values(db, t, cols(t)[ib])
            if not rv:
                return None
            w[t][ri][ib] = rng.choice(rv)
        elif kind == 'fd':
            _, t, ri, i, val, fi = x
            fdx = prf.fd[fi]
            xi = cols(t).index(fdx[1])
            if ref(t, fdx[2]) and not ref(t, fdx[1]):  # keep the referenced value, change the determinant
                cand = rev_fd(fdx[3]).get(_k(w[t][ri][i]) if w[t][ri][i] is not None else None)
                if cand:
                    w[t][ri][xi] = rng.choice(cand)
                    continue
            w[t][ri][i] = val
        elif kind == 'cross':
            _, t, ri, i, val, cj = x
            cr = prf.cross[cj]
            _, cx, cb, p, py, pd = cr
            if ref(t, cx) and not ref(p, py):  # keep the referenced child value, align the parent
                ib, iy, idd = cols(t).index(cb), cols(p).index(py), cols(p).index(pd)
                for r in w[p]:
                    if r[idd] == w[t][ri][ib]:
                        r[iy] = w[t][ri][i]
                continue
            w[t][ri][i] = val
        elif kind == 'year_date':
            _, t, ri, i, val = x
            w[t][ri][i] = val
    return None


def to_rows(db, wit):
    s = _S['schemas'][db]
    out = {}
    for t, d in wit.items():
        tt = s.table(t)
        out[tt['name']] = [list(r) for r in d['rows']]
    return out


def work(item):
    db = item['db_id']
    s, an, prf = _S['schemas'][db], _S['an'][db], _S['prof'][db]
    w = to_rows(db, item['witness'])
    refs = referenced_tables(an, item['gold']) | referenced_tables(an, item['pred'])
    res = dict(pair_id=item['pair_id'], source=item['source'], stage=item['stage'], ai=item['ai'],
               hv_no=item.get('hv_no'))
    refcols = {(t.lower(), c.lower()) for t, c in _qcols(an, item['gold'], item['pred'])}
    rep0 = certify(s, w, item['gold'], item['pred'], referenced_tables=refs, timeout_s=2.0)
    res['differs_initially'] = bool(rep0.get('differ', {}).get('C_set'))
    v0 = prf.violations(w)
    res['n_violations_initial'] = len(v0)
    res['violation_kinds_initial'] = sorted({x.split(' ')[0] for x in v0})
    if not v0:
        res.update(outcome='realistic_as_is', n_repaired=0, n_survive=0)
        return res
    n_rep = n_surv = 0
    for seed in range(K):
        rng = random.Random(f"{item['pair_id']}|{item['source']}|{seed}")
        w2 = repair_once(db, w, rng, refcols)
        if w2 is None:
            continue
        n_rep += 1
        rep = certify(s, w2, item['gold'], item['pred'], referenced_tables=refs, timeout_s=2.0)
        n_surv += bool(rep.get('differ', {}).get('C_set'))
    res.update(n_repaired=n_rep, n_survive=n_surv,
               outcome='unrepairable' if n_rep == 0 else ('survives' if n_surv else 'vanishes'))
    return res


def norm(sql):
    return re.sub(r'\s+', ' ', sql.strip().rstrip(';').strip())


def pair_level():
    """Pairs (by question and normalised prediction) with an A_R-certified witness from CG-R or Fuzz-R."""
    pairs = {json.loads(l)['pair_id']: json.loads(l) for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl'))}
    ok = {}
    for m, f in (('cgr', 'cgx_r_exc.jsonl'), ('fuzzr', 'fuzz_r_exc.jsonl')):
        for l in open(os.path.join(ROOT, 'results', 'test_r', f)):
            r = json.loads(l)
            p = pairs[r['pair_id']]
            k = (p['qid'], norm(p['pred']))
            ok.setdefault(k, {}).setdefault(m, False)
            if r.get('found') and (r.get('cert_R') or {}).get('ok'):
                ok[k][m] = True
    return pairs, ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--procs', type=int, default=2)
    a = ap.parse_args()
    D = os.path.join(ROOT, 'results', 'audit', 'human_validation')
    hkey = {k['pair_id'] + '|' + k['source']: k['no'] for k in
            json.load(open(os.path.join(D, 'key_DO_NOT_OPEN_BEFORE_ANNOTATING.json')))}
    items = []
    for prefix, stage in (('test_v4', 1), ('test_r', 2)):
        for x in final(prefix):
            it = dict(x['item'])
            it.update(source=x['source'], ai=x['ai'], stage=stage, hv_no=hkey.get(x['item']['pair_id'] + '|' + x['source']))
            items.append(it)
    print(len(items), 'items;', sum(i['hv_no'] is not None for i in items), 'human-validation items')
    with mp.Pool(a.procs, initializer=init) as pool:
        rows = pool.map(work, items, chunksize=4)
    pairs, ok = pair_level()
    for r in rows:
        p = pairs.get(r['pair_id'])
        k = (p['qid'], norm(p['pred'])) if p else None
        m = ok.get(k, {})
        r['pair_AR_cgr'] = m.get('cgr')
        r['pair_AR_fuzzr'] = m.get('fuzzr')
        r['pair_AR_any'] = (m.get('cgr') or m.get('fuzzr')) if m else None
    out = os.path.join(ROOT, 'results', 'stage3')
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'x1_repair_items.jsonl'), 'w') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')
    h1 = parse(os.path.join(D, 'sheet_annotator1.md'))
    h2 = parse(os.path.join(D, 'sheet_annotator2.md'))

    def tab(rs, by, what='outcome'):
        t = defaultdict(Counter)
        for r in rs:
            t[str(by(r))][str(r[what])] += 1
        return {k: dict(v) for k, v in sorted(t.items())}
    hv = [r for r in rows if r['hv_no'] is not None]
    for r in hv:
        r['h1'], r['h2'] = h1.get(r['hv_no']), h2.get(r['hv_no'])
        r['hcons'] = r['h1'] if r['h1'] == r['h2'] else 'disagree'
    summary = dict(
        n=len(rows), K=K,
        outcome_by_stage=tab(rows, lambda r: r['stage']),
        outcome_by_ai=tab(rows, lambda r: r['ai']),
        outcome_by_stage_ai=tab(rows, lambda r: f"{r['stage']}|{r['ai']}"),
        outcome_by_tool=tab(rows, lambda r: r['source']),
        pairAR_by_ai=tab(rows, lambda r: r['ai'], 'pair_AR_any'),
        pairAR_by_stage=tab(rows, lambda r: r['stage'], 'pair_AR_any'),
        hv_outcome_by_ai=tab(hv, lambda r: r['ai']),
        hv_outcome_by_human_consensus=tab(hv, lambda r: r['hcons']),
        hv_outcome_by_h1=tab(hv, lambda r: r['h1']),
        hv_outcome_by_h2=tab(hv, lambda r: r['h2']),
        hv_pairAR_by_ai=tab(hv, lambda r: r['ai'], 'pair_AR_any'),
        hv_pairAR_by_human_consensus=tab(hv, lambda r: r['hcons'], 'pair_AR_any'),
        hv_items=[{k: r[k] for k in ('hv_no', 'source', 'ai', 'h1', 'h2', 'outcome', 'n_repaired', 'n_survive',
                                     'pair_AR_any', 'violation_kinds_initial')} for r in sorted(hv, key=lambda r: r['hv_no'])],
        not_differing_initially=sum(not r['differs_initially'] for r in rows),
    )
    json.dump(summary, open(os.path.join(out, 'x1_repair.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in summary.items() if k != 'hv_items'}, indent=1))


if __name__ == '__main__':
    main()
