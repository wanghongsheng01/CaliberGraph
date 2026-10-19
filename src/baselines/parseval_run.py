"""Run ParSEval (sfu-db/ParSEval @ 88cfe245) on benchmark pairs under a hard per-pair wall budget.

Runs in ParSEval's own dependency environment (sqlglot 23.12.1, SQLAlchemy 2.0.49, Z3 4.16.0), so it
does not import CGX. It writes each NEQ counterexample as raw rows; certification happens afterwards
with the shared certifier (src/baselines/parseval_certify.py).

Usage (see scripts/parseval_env.sh):
  python parseval_run.py --pairs ../../data/pairs.jsonl --split dev --subset exc --budget 10 --out ...
"""
import argparse
import datetime
import decimal
import json
import multiprocessing as mp
import os
import re
import time

from parseval import GenerationConfig, disprove
from parseval.catalog import Catalog
from parseval.generator import generate
from parseval.instance import Instance

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from cgx.certify import SchemaInfo, FormatProfile, certify  # stdlib-only module, safe in ParSEval's environment

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')


def conv(v):
    if isinstance(v, (datetime.datetime,)):
        return v.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(v, datetime.date):
        return v.isoformat()
    if isinstance(v, datetime.time):
        return v.strftime('%H:%M:%S')
    if isinstance(v, decimal.Decimal):
        return float(v)
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, bytes):
        return v.decode('utf-8', 'replace')
    return v


def instance_rows(inst):
    out = {}
    for decl in inst.catalog.tables():
        name = decl.name.parts[-1].text
        cols = [b.name.text for b in decl.columns]
        rows = [[conv(v) for v in r] for r in inst.rows(decl.relation)]
        if rows:
            out[name] = dict(columns=cols, rows=rows)
    return out


_FMT = {}


def formats_for(db, si):
    if db not in _FMT:
        dbp = os.path.join(ROOT, 'data', 'format_profiles.json')
        if os.path.exists(dbp):
            from cgx.certify import format_profile_from_db
            prof = json.load(open(dbp))
            if db in prof:
                _FMT[db] = format_profile_from_db(prof[db], si)
                return _FMT[db]
        rb = json.load(open(os.path.join(ROOT, 'data', 'raw', 'spotit_constraints', 'rule_based', 'all_constraints.json')))
        mp = json.load(open(os.path.join(ROOT, 'data', 'raw', 'spotit', 'column_name_mapping.json')))['clean_to_orig']
        _FMT[db] = FormatProfile({db: rb.get(db, [])}, mp.get(db, {}), si)
    return _FMT[db]


def make_provider(fmt, si):
    """ParSEval value provider with the same format knowledge every method receives: observed value
    samples for text columns that have them, ISO dates for temporal-named text columns, otherwise
    ParSEval's own sequential provider."""
    from parseval.instance.domain import sequential
    import re as _re
    from cgx.certify import TEMPORAL_NAME

    def provider(table, column, existing, unique):
        try:
            t = si.table(table.name.parts[-1].text)
            cname = column.name.text
        except Exception:  # noqa: BLE001
            return sequential(table, column, existing, unique)
        if t is not None:
            key = (t['name'], next((c['name'] for c in t['columns'] if c['name'].lower() == cname.lower()), cname))
            smp = fmt.samples.get(key)
            if smp:
                for v in smp:
                    if not unique or v not in existing:
                        return v
            col = next((c for c in t['columns'] if c['name'].lower() == cname.lower()), None)
            if col and col['affinity'] == 'TEXT' and col['temporal'] is None and TEMPORAL_NAME.search(col['name']):
                for i in range(len(existing), len(existing) + 400):
                    v = f'{2000 + (i // 336) % 30:04d}-{1 + (i // 28) % 12:02d}-{1 + i % 28:02d}'
                    if not unique or v not in existing:
                        return v
        return sequential(table, column, existing, unique)
    return provider


def l1_disprove(row, schema, ddl_list, cfg, refs, budget_s):
    """ParSEval's generation stream, but every generated database is accepted only if the shared
    certifier says it is an L1 witness under C_set (favourable to ParSEval under our protocol)."""
    si = SchemaInfo(ddl_list)
    fmt = formats_for(row['db_id'], si)
    from dataclasses import replace as _replace
    cfg = _replace(cfg, provider=make_provider(fmt, si))
    catalog = Catalog.from_ddl(schema, dialect='sqlite')
    found = {}

    def check(instance):
        raw = instance_rows(instance)
        w = raw_to_witness(raw, si)
        rep = certify(si, w, row['gold'], row['pred'], referenced_tables=refs, timeout_s=1.0, formats=fmt)
        if rep.get('L1f') and rep.get('differ', {}).get('C_set'):
            found['raw'] = raw
            return True
        return False
    reasons = []
    t0 = time.monotonic()
    seed = 0
    from dataclasses import replace
    # restart generation with new seeds until the shared wall budget is used (budget-matched)
    while time.monotonic() - t0 < budget_s - 0.2:
        c = replace(cfg, seed=seed, time_limit_s=max(0.5, min(cfg.time_limit_s, budget_s - (time.monotonic() - t0))))
        for idx, sql in enumerate((row['gold'], row['pred']), 1):
            try:
                g = generate(sql, catalog, config=c, on_instance=check)
            except Exception as e:  # noqa: BLE001
                reasons.append(f'q{idx}: {type(e).__name__}')
                continue
            if found:
                return dict(verdict='NEQ', reason=f'q{idx} database seed {seed} (L1-filtered)',
                            raw_witness=found['raw'], seeds=seed + 1)
            reasons.append(f'q{idx}: ' + ('timeout' if g.timed_out else 'no witness'))
        if len(reasons) >= 2 and all('Error' in x or 'Exception' in x for x in reasons[-2:]):
            break  # unsupported by the generator: reseeding cannot help
        seed += 1
    return dict(verdict='NO_WITNESS', reason='; '.join(sorted(set(reasons))), seeds=seed)


def raw_to_witness(raw, si):
    w = {}
    for tname, d in raw.items():
        t = si.table(tname)
        if t is None:
            continue
        names = [c['name'].lower() for c in t['columns']]
        idx = [names.index(c.lower()) if c.lower() in names else None for c in d['columns']]
        rows = []
        for r in d['rows']:
            nr = [None] * len(names)
            for v, j in zip(r, idx):
                if j is not None:
                    nr[j] = v
            rows.append(nr)
        w[t['name']] = rows
    return w


def child(row, schema, budget, q, variant='official', ddl_list=None, refs=()):
    t0 = time.monotonic()
    try:
        per_query = max(1.0, budget / 2 - 0.5)
        cfg = GenerationConfig(timeout_ms=int(min(2000, per_query * 1000)), time_limit_s=per_query,
                               set_semantics=True)
        if variant == 'l1':
            out = l1_disprove(row, schema, ddl_list, cfg, refs, budget)
        else:
            res = disprove(row['gold'], row['pred'], schema, 'sqlite:///:memory:', 'sqlite', config=cfg,
                           timeout_s=min(2.0, budget / 4), set_semantics=True)
            out = dict(verdict=res.verdict.value, reason=res.reason)
            if res.counterexample is not None:
                out['raw_witness'] = instance_rows(res.counterexample)
    except Exception as e:  # noqa: BLE001
        out = dict(verdict='ERROR', reason=f'{type(e).__name__}: {str(e)[:300]}')
    out['search_s'] = time.monotonic() - t0
    q.put(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--split', default='dev')
    ap.add_argument('--subset', default='exc')
    ap.add_argument('--budget', type=float, default=10.0)
    ap.add_argument('--procs', type=int, default=2)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--out', required=True)
    ap.add_argument('--variant', default='official', choices=['official', 'l1'])
    ap.add_argument('--ids', default='')
    a = ap.parse_args()
    ddl_lists = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    tab_re = {db: [(t, re.compile(r'(?<![\w])' + re.escape(t) + r'(?![\w])', re.I))
                   for t in SchemaInfo(l).tables] for db, l in ddl_lists.items()}
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    schemas = {db: ';\n'.join(s) for db, s in ddl.items()}
    rows = [json.loads(l) for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl'))]
    rows = [r for r in rows if r['split'] == a.split and r['source'] != 'parseval_model']
    rows = [r for r in rows if r['ex'] == ('correct' if a.subset == 'exc' else 'incorrect')]
    norm = lambda s: re.sub(r'\s+', ' ', s.strip().rstrip(';').strip())  # noqa: E731
    seen, todo = set(), []
    for r in rows:
        k = (r['qid'], r['gold'].strip(), r['pred'].strip())
        if k in seen:
            continue
        seen.add(k)
        todo.append(r)
    if a.ids:
        keep = set(json.load(open(a.ids))['pair_ids'])
        todo = [r for r in todo if r['pair_id'] in keep]
    if a.limit:
        todo = todo[:a.limit]
    done = set()
    if os.path.exists(a.out):
        done = {json.loads(l)['pair_id'] for l in open(a.out)}
    todo = [r for r in todo if r['pair_id'] not in done]
    print(len(todo), 'to run', flush=True)
    ctx = mp.get_context('fork')
    running = []
    f = open(a.out, 'a')
    t_start = time.time()
    n_done = 0

    def finish(item, out):
        nonlocal n_done
        r, _, t0 = item
        rec = dict(pair_id=r['pair_id'], method='parseval' if a.variant == 'official' else 'parseval_l1', budget=a.budget, wall_s=time.monotonic() - t0, **out)
        rec['found'] = out.get('verdict') == 'NEQ'
        f.write(json.dumps(rec, default=str) + '\n')
        f.flush()
        n_done += 1
        if n_done % 50 == 0:
            print(n_done, f'{time.time() - t_start:.0f}s', flush=True)

    queue = list(todo)
    while queue or running:
        while queue and len(running) < a.procs:
            r = queue.pop(0)
            if norm(r['gold']) == norm(r['pred']):
                finish((r, None, time.monotonic()), dict(verdict='SKIP', reason='identical_text', note='identical_text'))
                continue
            q = ctx.Queue()
            refs = {t for t, rx in tab_re[r['db_id']] if rx.search(r['gold']) or rx.search(r['pred'])}
            p = ctx.Process(target=child, args=(r, schemas[r['db_id']], a.budget, q, a.variant,
                                                ddl_lists[r['db_id']], refs))
            p.start()
            running.append(((r, q, time.monotonic()), p))
        time.sleep(0.02)
        still = []
        for item, p in running:
            r, q, t0 = item
            out = None
            try:
                out = q.get_nowait()
            except Exception:  # noqa: BLE001
                pass
            if out is not None:
                p.join(1)
                finish(item, out)
            elif time.monotonic() - t0 > a.budget + 1.0:
                p.kill()
                p.join(1)
                finish(item, dict(verdict='TIMEOUT', reason='hard wall budget'))
            elif not p.is_alive():
                try:
                    out = q.get(timeout=0.5)
                    finish(item, out)
                except Exception:  # noqa: BLE001
                    finish(item, dict(verdict='ERROR', reason=f'child exited {p.exitcode}'))
            else:
                still.append((item, p))
        running = still
    f.close()
    print('done', time.time() - t_start)


if __name__ == '__main__':
    main()
