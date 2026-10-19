"""Run a witness-search method over benchmark pairs and certify every witness independently.

Usage: python run_method.py --method cgx --split dev --subset exc --out ../results/dev_cgx.jsonl
Methods: cgx, cgx_noanchor, cgx_noiso, cgx_nojoin, cgx_nodomain, cgx_sc, fuzz
"""
import argparse
import json
import multiprocessing as mp
import os
import signal
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(__file__))
from cgx.certify import SchemaInfo, RealismConstraints, certify, jsonable  # noqa: E402
from cgx.sqlinfo import Analyzer  # noqa: E402
from cgx.search import CGX, Config  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
_STATE = {}


def load_realism(db, schema):
    base = os.path.join(ROOT, 'data', 'raw', 'spotit_constraints', 'LLM', f'{db}_constraints_LLM.json')
    if not os.path.exists(base):
        return None
    cons = json.load(open(base))
    mapping = json.load(open(os.path.join(ROOT, 'data', 'raw', 'spotit', 'column_name_mapping.json')))['clean_to_orig']
    return RealismConstraints(cons, mapping.get(db, {}), schema)


def load_formats(db, schema):
    from cgx.certify import FormatProfile, format_profile_from_db
    dbp = os.path.join(ROOT, 'data', 'format_profiles.json')
    if os.path.exists(dbp):  # official-database profiles take precedence (protocol amendment A10)
        prof = json.load(open(dbp))
        if db in prof:
            return format_profile_from_db(prof[db], schema)
    rb = json.load(open(os.path.join(ROOT, 'data', 'raw', 'spotit_constraints', 'rule_based', 'all_constraints.json')))
    mapping = json.load(open(os.path.join(ROOT, 'data', 'raw', 'spotit', 'column_name_mapping.json')))['clean_to_orig']
    return FormatProfile({db: rb.get(db, [])}, mapping.get(db, {}), schema)


def init_worker(method, budget):
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    _STATE['schemas'] = {db: SchemaInfo(s) for db, s in ddl.items()}
    _STATE['analyzers'] = {db: Analyzer(s) for db, s in _STATE['schemas'].items()}
    _STATE['realism'] = {db: load_realism(db, s) for db, s in _STATE['schemas'].items()}
    _STATE['formats'] = {db: load_formats(db, s) for db, s in _STATE['schemas'].items()}
    _STATE['method'] = method
    _STATE['budget'] = budget


def make_cfg(method, budget, realism):
    cfg = Config(budget_s=budget)
    if method == 'cgx_noanchor':
        cfg.anchoring = False
    elif method == 'cgx_noiso':
        cfg.isolation = False
    elif method == 'cgx_nojoin':
        cfg.join_graph = False
    elif method == 'cgx_nodomain':
        cfg.sqlite_domain = False
    elif method == 'cgx_sc':
        cfg.realism = realism
    elif method == 'cgx_v5':
        pass  # never_null is set by work()
    return cfg


def norm_sql(s):
    import re
    return re.sub(r'\s+', ' ', s.strip().rstrip(';').strip())


def referenced_tables(analyzer, sql):
    try:
        return analyzer.analyze(sql).tables
    except Exception:  # noqa: BLE001
        return set()


def _qcols(an, gold, pred):
    from cgx.sqlinfo import analyze_pair
    p = analyze_pair(an, gold, pred)
    return p.gold.columns | p.pred.columns


def work(row):
    db = row['db_id']
    schema, an = _STATE['schemas'][db], _STATE['analyzers'][db]
    method, budget = _STATE['method'], _STATE['budget']
    t0 = time.monotonic()
    out = dict(pair_id=row['pair_id'], method=method, budget=budget)
    if norm_sql(row['gold']) == norm_sql(row['pred']):
        # identical query text cannot produce different results on any database
        out.update(found=False, note='identical_text', n_eval=0, search_s=0.0, wall_s=0.0)
        return out
    try:
        if method in ('fuzz', 'fuzz_cert', 'fuzz_v5'):
            from baselines.fuzz import fuzz
            accept, nn = None, None
            if method in ('fuzz_cert', 'fuzz_v5'):
                refs0 = referenced_tables(an, row['gold']) | referenced_tables(an, row['pred'])
                if method == 'fuzz_v5':
                    from score import observed_not_null
                    nn = observed_not_null(db)[1]
                    qc = {(t.lower(), c.lower()) for t, c in _qcols(an, row['gold'], row['pred'])}

                def accept(w, refs0=refs0, nn=nn):
                    rep = certify(schema, w, row['gold'], row['pred'], referenced_tables=refs0, timeout_s=1.0,
                                  formats=_STATE['formats'][db])
                    if not (rep.get('L1f') and rep.get('differ', {}).get('C_set')):
                        return False
                    if nn:
                        for t, rows_ in w.items():
                            for i, c in enumerate(schema.tables[t]['columns']):
                                k = (t.lower(), c['name'].lower())
                                if k in nn and k in qc and any(x[i] is None for x in rows_):
                                    return False
                    return True
            res = fuzz(schema, an, row['gold'], row['pred'], budget, seed=0, formats=_STATE['formats'][db],
                       accept=accept, never_null=nn)
        else:
            cfg = make_cfg(method, budget, _STATE['realism'][db])
            cfg.formats = _STATE['formats'][db]
            if method == 'cgx_v5':
                from score import observed_not_null
                cfg.never_null = observed_not_null(db)[1]
            res = CGX(schema, an, cfg).run(row['gold'], row['pred'])
        out.update(found=res.found, n_eval=res.n_eval, search_s=res.elapsed, phase=res.phase,
                   status_counts=res.status_counts, note=res.note)
        if res.found:
            refs = referenced_tables(an, row['gold']) | referenced_tables(an, row['pred'])
            rep = certify(schema, res.witness, row['gold'], row['pred'], referenced_tables=refs,
                          realism=_STATE['realism'][db], formats=_STATE['formats'][db])
            out['cert'] = jsonable({k: v for k, v in rep.items()})
            out['witness'] = res.witness
    except Exception as e:  # noqa: BLE001
        out.update(found=False, error=f'{type(e).__name__}: {e}', tb=traceback.format_exc()[-1500:])
    out['wall_s'] = time.monotonic() - t0
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--method', default='cgx')
    ap.add_argument('--split', default='dev')
    ap.add_argument('--subset', default='exc', choices=['exc', 'exi', 'all'])
    ap.add_argument('--sources', default='')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--budget', type=float, default=10.0)
    ap.add_argument('--procs', type=int, default=2)
    ap.add_argument('--out', required=True)
    ap.add_argument('--dedup', action='store_true', help='run each distinct (qid, pred) once')
    ap.add_argument('--ids', default='', help='JSON file with pair_ids to restrict to')
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl'))]
    rows = [r for r in rows if r['split'] == a.split]
    if a.sources:
        rows = [r for r in rows if r['source'] in a.sources.split(',')]
    if a.subset == 'exc':
        rows = [r for r in rows if r['ex'] == 'correct' or (r['source'] == 'parseval_model' and r.get('parseval_official') == 'EQ')]
    elif a.subset == 'exi':
        rows = [r for r in rows if r['ex'] == 'incorrect']
    if a.dedup:
        seen, uniq = set(), []
        for r in rows:
            k = (r['qid'], r['gold'].strip(), r['pred'].strip())
            if k not in seen:
                seen.add(k)
                uniq.append(r)
        rows = uniq
    if a.ids:
        keep = set(json.load(open(a.ids))['pair_ids'])
        rows = [r for r in rows if r['pair_id'] in keep]
    if a.limit:
        rows = rows[:a.limit]
    done = set()
    if os.path.exists(a.out):
        done = {json.loads(l)['pair_id'] for l in open(a.out)}
    todo = [r for r in rows if r['pair_id'] not in done]
    print(f'{len(rows)} pairs, {len(todo)} to run', flush=True)
    t0 = time.time()
    with mp.Pool(a.procs, initializer=init_worker, initargs=(a.method, a.budget), maxtasksperchild=200) as pool, \
            open(a.out, 'a') as f:
        for i, res in enumerate(pool.imap_unordered(work, todo, chunksize=1)):
            f.write(json.dumps(res, default=str) + '\n')
            f.flush()
            if (i + 1) % 50 == 0:
                print(f'{i + 1}/{len(todo)} {time.time() - t0:.0f}s', flush=True)
    print('done', time.time() - t0)


if __name__ == '__main__':
    main()
