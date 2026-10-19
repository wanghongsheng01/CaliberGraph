"""Re-run the ORIGINAL SpotIt verifier (Klopfenstein et al., ICLR 2026) under our per-pair budget and
certify its counterexamples with our certifier.

What is run
  SpotIt = the VeriEQL fork https://github.com/atremante26/VeriEQL at commit 66d8343f3 (2025-09-18,
  "new results": the commit that added the released VeriEQL_results*_null files), driven exactly as its
  run.py does on the non-"--vanilla" path, i.e. WITHOUT any of the mined/LLM-validated constraints of
  SpotIt+ (only the BIRD primary/foreign keys in BIRD_schemas/table_constraints.json):
    * SQL preprocessing: gold -> upper() -> clean_up(); pred -> split('\t')[0] -> collapse whitespace
      -> upper() -> clean_up()  (clean_up turns `quoted` and "quoted" text into cleaned identifiers);
    * schema BIRD_schemas/table_to_columns.json[db] (SpotIt's cleaned column names), constraints
      table_constraints.json[db][0];
    * config: dialect=MYSQL, all_null_is_deleted=True, generate_code/timer/show_counterexample=True,
      encode_date iff 'STRFTIME' occurs, encode_string iff ' LIKE ' or 'SUBSTR' occurs or encode_date;
    * verify_sql_equivalence(pred, gold, schema, bound, constraints, **config) for bound = 1, 2, ...;
    * SpotIt's own counterexample validation (evaluation/execute_sql.py): the counterexample database
      is loaded into SQLite with columns renamed to the original names (upper-cased), the upper-cased
      original queries are executed and compared as sets (with SpotIt's empty-vs-(None,) exception).
  Determinism: VeriEQL iterates over hashed Python sets, so the z3 model (not the verdict) depends on
  the string-hash seed; the script pins PYTHONHASHSEED (--hash-seed, default 0) by re-executing itself.
  A counterexample counts as SpotIt's verdict "incorrect" only if it passes that validation; the
  smallest such bound is reported (as in evaluation_verieql.py). A failed validation moves on to
  the next bound. An exception at any bound ends the pair with SpotIt verdict "error".

Budget
  Each distinct pair runs in a child process forked from a warm worker (VeriEQL, z3 and the SpotIt
  schema files are loaded once per worker, before the fork, and are not charged to the pair). The
  child runs bounds 1..--max-bound sequentially; the parent SIGKILLs it when --budget seconds of
  wall clock have elapsed since the fork. One child per worker, so each pair uses one core.
  search_s = wall clock of the child (preprocessing + all bounds + SpotIt validation);
  wall_s = search_s + witness conversion + certification.

Output (JSONL, one row per (distinct) pair, run_method.py field names)
  pair_id, method ('spotit_rerun'), budget, found, witness, cert, search_s, wall_s, note, error,
  plus: spotit_verdict (incorrect / unknown / error, SpotIt's own semantics), ce_bound,
  max_bound_done, bounds (per-bound log), killed, unmapped, cert_R (as run_method.py),
  cert_recased (diagnostic, NOT SpotIt: certification after mapping upper-cased string values that
  equal an upper-cased literal of the original queries back to that literal's original case).

Environment (PyPI is unreachable here; everything comes from GitHub clones)
  SPOTIT_ROOT   checkout of atremante26/VeriEQL @ 66d8343f3   (default /home/claude/ext/SpotIt_iclr)
  SPOTIT_PYLIBS directory with mo_sql_parsing 8.205.22260 (+ mo-dots/mo-future/mo-imports/
                mo-parsing at the versions it pins), ordered_set 4.1.0, lark 1.2.2, a json-backed
                `ujson` stand-in, and a z3 package = SpotIt's patched z3py_libs/z3.py on top of the
                generated bindings and libz3 of Z3 4.16.0   (default /home/claude/ext/spotit_pylibs)

Usage
  python src_s3/spotit_run.py --split dev --subset exc --dedup --budget 5 --procs 1 \
      --out results/dev_spotit_rerun_5s.jsonl [--ids ids.json] [--max-bound 5]
The test split additionally requires --allow-test (pre-registration guard).
"""
import argparse
import json
import multiprocessing as mp
import os
import re
import resource
import select
import signal
import sqlite3
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(ROOT, 'src_r'))
from cgx.certify import SchemaInfo, certify, jsonable  # noqa: E402
from cgx.sqlinfo import Analyzer  # noqa: E402
from run_method import (load_realism, load_formats, load_profile_r, norm_sql,  # noqa: E402
                        referenced_tables, _qcols)
from baselines.spotit_import import to_witness  # noqa: E402

SPOTIT_ROOT = os.environ.get('SPOTIT_ROOT', '/home/claude/ext/SpotIt_iclr')
SPOTIT_PYLIBS = os.environ.get('SPOTIT_PYLIBS', '/home/claude/ext/spotit_pylibs')
METHOD = 'spotit_rerun'
_STATE = {}


# ----------------------------------------------------------------------------------------------
# SpotIt side (runs inside the forked child; VeriEQL modules are imported once per worker)
# ----------------------------------------------------------------------------------------------

class SpotItEngine:
    """Thin wrapper reproducing SpotIt's run.py (non-vanilla path) for one (gold, pred, db) pair."""

    def __init__(self, root=SPOTIT_ROOT, pylibs=SPOTIT_PYLIBS):
        # VeriEQL uses top-level module names (constants, environment, parsers, utils, ...);
        # its root must come first on sys.path, followed by the vendored dependencies.
        for p in (pylibs, root):
            if p not in sys.path:
                sys.path.insert(0, p)
        from verieql import verify_sql_equivalence
        from constants import DIALECT
        import importlib.util
        spec = importlib.util.spec_from_file_location('spotit_run_py', os.path.join(root, 'run.py'))
        run_py = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(run_py)  # module level only defines clean_up (main is guarded)
        self.clean_up = run_py.clean_up
        self.verify = verify_sql_equivalence
        self.dialect = DIALECT.MYSQL
        bs = os.path.join(root, 'BIRD_schemas')
        self.schema = json.load(open(os.path.join(bs, 'table_to_columns.json')))
        self.constraints = json.load(open(os.path.join(bs, 'table_constraints.json')))
        self.c2o = json.load(open(os.path.join(root, 'evaluation', 'column_name_mapping.json')))['clean_to_orig']

    def preprocess(self, gold, pred):
        g = self.clean_up(gold.upper())
        p = ' '.join(pred.split('\t')[0].split()).upper()
        return g, self.clean_up(p)

    def config(self, g, p):
        cfg = {'generate_code': True, 'timer': True, 'show_counterexample': True,
               'dialect': self.dialect, 'all_null_is_deleted': True}
        cfg['encode_date'] = any(k in q.upper() for k in ['STRFTIME'] for q in (p, g))
        cfg['encode_string'] = any(k in q.upper() for k in [' LIKE ', 'SUBSTR'] for q in (p, g)) \
            or cfg['encode_date']
        return cfg

    def run_bound(self, db, g, p, bound, cfg):
        return self.verify(p, g, self.schema[db], bound, self.constraints[db][0], **cfg)


def ce_tables(ce_text):
    """Load a VeriEQL counterexample script into SQLite; return {TABLE: (cols, decl_types, rows)}.

    Same identifier quoting as baselines/spotit_import.parse_ce, plus SpotIt's own two quote fixes
    from evaluation/execute_sql.py (VeriEQL does not escape apostrophes inside string values)."""
    text = ce_text.replace("JOURNEY INTO NYX HERO'S PATH", "JOURNEY INTO NYX HERO''S PATH") \
                  .replace("ANCESTOR'S CHOSEN", "ANCESTOR''S CHOSEN")
    script = []
    for line in text.splitlines():
        if line.startswith('-- ----------sql1'):
            break
        if line.startswith('--'):
            continue
        m = re.match(r'^CREATE TABLE (\S+) \($', line)
        if m:
            line = f'CREATE TABLE "{m.group(1)}" ('
        m = re.match(r'^INSERT INTO (\S+) VALUES (.*)$', line)
        if m:
            line = f'INSERT INTO "{m.group(1)}" VALUES {m.group(2)}'
        m = re.match(r'^(\s+)(\S+) (.+?)(,?)$', line)
        if m and not line.strip().startswith(('INSERT', 'CREATE', ')')):
            line = f'{m.group(1)}"{m.group(2)}" {m.group(3)}{m.group(4)}'
        script.append(line)
    con = sqlite3.connect(':memory:')
    try:
        con.executescript('\n'.join(script))
        out = {}
        for (name,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            info = list(con.execute(f'PRAGMA table_info("{name}")'))
            out[name] = ([r[1] for r in info], [r[2] for r in info], con.execute(f'SELECT * FROM "{name}"').fetchall())
        return out
    finally:
        con.close()


def spotit_calculate_ex(pred_rows, gold_rows):
    """evaluation/execute_sql.calculate_ex: True when SpotIt deems the outputs different."""
    if set(pred_rows) != set(gold_rows):
        if set(pred_rows) == set() and set(gold_rows) == {(None,)}:
            return False
        if set(gold_rows) == set() and set(pred_rows) == {(None,)}:
            return False
        return True
    return False


def spotit_validate(tables, c2o, gold, pred):
    """SpotIt's counterexample validation (evaluation/execute_sql.execute_counterexample_):
    columns renamed to original names upper-cased, upper-cased ORIGINAL queries, set comparison.
    Returns (validated, pred_rows, gold_rows, error)."""
    con = sqlite3.connect(':memory:')
    try:
        for t, (cols, types, rows) in tables.items():
            defs = ', '.join(f'"{c2o.get(c, c).upper()}" {ty}' for c, ty in zip(cols, types))
            con.execute(f'CREATE TABLE "{t}" ({defs})')
            if rows:
                con.executemany(f'INSERT INTO "{t}" VALUES ({",".join("?" * len(cols))})', rows)
        sql1 = pred.split('\t----- bird')[0].upper()
        sql2 = gold.upper()
        pr = con.execute(sql1).fetchall()
        gr = con.execute(sql2).fetchall()
        return spotit_calculate_ex(pr, gr), pr[:20], gr[:20], None
    except Exception as e:  # noqa: BLE001  (SpotIt: execution error -> not a valid counterexample)
        return False, None, None, f'{type(e).__name__}: {e}'
    finally:
        con.close()


def _child(engine, db, gold, pred, max_bound, wfd):
    """Body of the forked child: run bounds 1..max_bound, stream one JSON line per event."""
    out = os.fdopen(wfd, 'w')

    def send(d):
        out.write(json.dumps(d, default=str) + '\n')
        out.flush()

    t0 = time.monotonic()
    try:
        g, p = engine.preprocess(gold, pred)
        cfg = engine.config(g, p)
    except Exception as e:  # noqa: BLE001
        send(dict(type='error', bound=0, error=f'{type(e).__name__}: {e}', tb=traceback.format_exc()[-1500:]))
        return
    send(dict(type='prep', gold_sql=g, pred_sql=p, encode_date=cfg['encode_date'],
              encode_string=cfg['encode_string'], t=time.monotonic() - t0))
    c2o = engine.c2o.get(db, {})
    for b in range(1, max_bound + 1):
        tb = time.monotonic()
        try:
            res = engine.run_bound(db, g, p, b, cfg)
        except Exception as e:  # noqa: BLE001  (SpotIt records ERROR for this bound)
            send(dict(type='error', bound=b, error=f'{type(e).__name__}: {e}', tb=traceback.format_exc()[-1500:],
                      t_s=time.monotonic() - tb))
            return
        msg = dict(type='bound', bound=b, equivalent=res['equivalent'], time_cost=res['time_cost'])
        ce = res.get('counterexample')
        if res['equivalent']:
            msg['status'] = 'equivalent'
        elif not ce or 'CREATE TABLE' not in ce:
            msg['status'] = 'no_model'  # e.g. different #columns, or solver 'unknown'
        else:
            msg['status'] = 'ce'
            try:
                tables = ce_tables(ce)
                ok, pr, gr, err = spotit_validate(tables, c2o, gold, pred)
            except Exception as e:  # noqa: BLE001
                ok, pr, gr, err = False, None, None, f'{type(e).__name__}: {e}'
            msg.update(validated=ok, val_pred=pr, val_gold=gr, val_error=err, ce=ce)
        msg['t_s'] = time.monotonic() - tb
        send(msg)
        if msg.get('validated'):
            return


def run_with_budget(engine, db, gold, pred, budget, max_bound, mem_mb):
    """Fork a child for one pair; hard-kill it after `budget` seconds of wall clock."""
    rfd, wfd = os.pipe()
    t0 = time.monotonic()
    pid = os.fork()
    if pid == 0:  # child
        code = 0
        try:
            os.close(rfd)
            dn = os.open(os.devnull, os.O_WRONLY)
            os.dup2(dn, 1)
            os.dup2(dn, 2)  # VeriEQL prints a lot
            if mem_mb:
                lim = mem_mb * 1024 * 1024
                resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
            _child(engine, db, gold, pred, max_bound, wfd)
        except BaseException:  # noqa: BLE001
            code = 1
        finally:
            os._exit(code)
    os.close(wfd)
    deadline = t0 + budget
    buf, msgs, killed = b'', [], False
    while True:
        rem = deadline - time.monotonic()
        if rem <= 0:
            os.kill(pid, signal.SIGKILL)
            killed = True
            break
        ready, _, _ = select.select([rfd], [], [], rem)
        if not ready:
            continue
        chunk = os.read(rfd, 1 << 16)
        if not chunk:
            break
        buf += chunk
        while b'\n' in buf:
            line, buf = buf.split(b'\n', 1)
            msgs.append(json.loads(line))
    elapsed = time.monotonic() - t0
    os.close(rfd)
    _, status = os.waitpid(pid, 0)
    return msgs, elapsed, killed, status


# ----------------------------------------------------------------------------------------------
# Our side: worker state, witness conversion, certification
# ----------------------------------------------------------------------------------------------

def init_worker(budget, max_bound, mem_mb, keep_ce):
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    _STATE['schemas'] = {db: SchemaInfo(s) for db, s in ddl.items()}
    _STATE['analyzers'] = {db: Analyzer(s) for db, s in _STATE['schemas'].items()}
    _STATE['realism'] = {db: load_realism(db, s) for db, s in _STATE['schemas'].items()}
    _STATE['formats'] = {db: load_formats(db, s) for db, s in _STATE['schemas'].items()}
    _STATE['profile_r'], _STATE['templates'] = load_profile_r(_STATE['schemas'])
    _STATE.update(budget=budget, max_bound=max_bound, mem_mb=mem_mb, keep_ce=keep_ce)
    _STATE['engine'] = SpotItEngine()


def recase_witness(witness, gold, pred):
    """Diagnostic only: map string cells equal to UPPER(literal) back to the literal's original case."""
    seen = {}
    for lit in re.findall(r"'((?:[^']|'')*)'", gold + ' \n ' + pred):
        lit = lit.replace("''", "'")
        seen.setdefault(lit.upper(), set()).add(lit)
    mp_ = {u: next(iter(v)) for u, v in seen.items() if len(v) == 1 and next(iter(v)) != u}
    new = {t: [[mp_.get(v, v) if isinstance(v, str) else v for v in r] for r in rows] for t, rows in witness.items()}
    return new, new != witness


def _certify(db, witness, row):
    schema, an = _STATE['schemas'][db], _STATE['analyzers'][db]
    refs = referenced_tables(an, row['gold']) | referenced_tables(an, row['pred'])
    rep = certify(schema, witness, row['gold'], row['pred'], referenced_tables=refs,
                  realism=_STATE['realism'][db], formats=_STATE['formats'][db])
    return jsonable({k: v for k, v in rep.items()})


def work(row):
    db = row['db_id']
    t0 = time.monotonic()
    out = dict(pair_id=row['pair_id'], method=METHOD, budget=_STATE['budget'], found=False,
               hash_seed=os.environ.get('PYTHONHASHSEED'))
    if norm_sql(row['gold']) == norm_sql(row['pred']):
        out.update(note='identical_text', spotit_verdict='unknown', search_s=0.0, wall_s=0.0)
        return out
    try:
        msgs, elapsed, killed, status = run_with_budget(_STATE['engine'], db, row['gold'], row['pred'],
                                                        _STATE['budget'], _STATE['max_bound'], _STATE['mem_mb'])
        out['search_s'] = elapsed
        out['killed'] = killed
        bounds = [m for m in msgs if m['type'] in ('bound', 'error')]
        prep = next((m for m in msgs if m['type'] == 'prep'), None)
        if prep:
            out['spotit_sql'] = dict(gold=prep['gold_sql'], pred=prep['pred_sql'])
            out['encode'] = dict(date=prep['encode_date'], string=prep['encode_string'])
        out['bounds'] = [{k: v for k, v in m.items() if k not in ('ce', 'type', 'tb')} for m in bounds]
        done = [m['bound'] for m in msgs if m['type'] == 'bound']
        out['max_bound_done'] = max(done, default=0)
        err = next((m for m in msgs if m['type'] == 'error'), None)
        hit = next((m for m in msgs if m['type'] == 'bound' and m.get('validated')), None)
        if err is not None:
            out.update(spotit_verdict='error', error=err['error'], tb=err.get('tb'), note=f"error@bound{err['bound']}")
        elif hit is not None:
            out.update(spotit_verdict='incorrect', ce_bound=hit['bound'], note=f"ce@bound{hit['bound']}")
        else:
            out['spotit_verdict'] = 'unknown'
            if killed:
                out['note'] = f"budget_exhausted@bound{out['max_bound_done'] + 1}"
            elif status != 0:
                out['note'] = f'child_failed(status={status})'  # e.g. RLIMIT_AS hit inside z3
            else:
                out['note'] = f"no_ce_upto_bound{out['max_bound_done']}"
        if hit is not None:
            w, unmapped = to_witness({t: (c, r) for t, (c, _ty, r) in ce_tables(hit['ce']).items()},
                                     _STATE['schemas'][db], _STATE['engine'].c2o.get(db, {}))
            out.update(found=True, witness=w, unmapped=unmapped)
            if _STATE['keep_ce']:
                out['ce_text'] = hit['ce']
            out['cert'] = _certify(db, w, row)
            prf = _STATE['profile_r'].get(db)
            if prf is not None:
                viol = prf.violations(w)
                only = {(t.lower(), c.lower()) for t, c in _qcols(_STATE['analyzers'][db], row['gold'], row['pred'])}
                out['cert_R'] = dict(ok=not viol, okq=prf.ok(w, only), violations=viol[:8], n_violations=len(viol))
            w2, changed = recase_witness(w, row['gold'], row['pred'])
            if changed:
                out['cert_recased'] = _certify(db, w2, row)
    except Exception as e:  # noqa: BLE001
        out.update(found=False, error=f'{type(e).__name__}: {e}', tb=traceback.format_exc()[-1500:])
    out['wall_s'] = time.monotonic() - t0
    return out


def select_rows(split, subset, sources='', exclude_sources='', dedup=False, ids=''):
    """Pair selection identical to run_method.py (plus --exclude-sources)."""
    rows = [json.loads(l) for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl'))]
    rows = [r for r in rows if r['split'] == split]
    if sources:
        rows = [r for r in rows if r['source'] in sources.split(',')]
    if exclude_sources:
        rows = [r for r in rows if r['source'] not in exclude_sources.split(',')]
    if subset == 'exc':
        rows = [r for r in rows if r['ex'] == 'correct' or (r['source'] == 'parseval_model' and r.get('parseval_official') == 'EQ')]
    elif subset == 'exi':
        rows = [r for r in rows if r['ex'] == 'incorrect']
    if dedup:
        seen, uniq = set(), []
        for r in rows:
            k = (r['qid'], r['gold'].strip(), r['pred'].strip())
            if k not in seen:
                seen.add(k)
                uniq.append(r)
        rows = uniq
    if ids:
        keep = set(json.load(open(ids))['pair_ids'])
        rows = [r for r in rows if r['pair_id'] in keep]
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--split', default='dev')
    ap.add_argument('--subset', default='exc', choices=['exc', 'exi', 'all'])
    ap.add_argument('--sources', default='')
    ap.add_argument('--exclude-sources', default='')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--budget', type=float, default=5.0, help='wall-clock seconds per (distinct) pair')
    ap.add_argument('--max-bound', type=int, default=5, help='largest bound tried (SpotIt used 1..5)')
    ap.add_argument('--mem-mb', type=int, default=8000, help='address-space limit of each child (0 = none)')
    ap.add_argument('--procs', type=int, default=1)
    ap.add_argument('--out', required=True)
    ap.add_argument('--dedup', action='store_true', help='run each distinct (qid, gold, pred) once')
    ap.add_argument('--ids', default='', help='JSON file {"pair_ids": [...]} to restrict to')
    ap.add_argument('--keep-ce', action='store_true', help='store the raw VeriEQL counterexample text')
    ap.add_argument('--allow-test', action='store_true', help='required for --split test (pre-registration)')
    ap.add_argument('--hash-seed', type=int, default=0,
                    help='PYTHONHASHSEED for all processes (VeriEQL iterates over hashed sets, so the z3 model '
                         'and hence the counterexample depend on it); the script re-executes itself if needed')
    a = ap.parse_args()
    if a.split == 'test' and not a.allow_test:
        sys.exit('refusing to run on the held-out test split without --allow-test')
    if os.environ.get('PYTHONHASHSEED') != str(a.hash_seed):
        os.environ['PYTHONHASHSEED'] = str(a.hash_seed)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    rows = select_rows(a.split, a.subset, a.sources, a.exclude_sources, a.dedup, a.ids)
    if a.limit:
        rows = rows[:a.limit]
    done = set()
    if os.path.exists(a.out):
        done = {json.loads(l)['pair_id'] for l in open(a.out)}
    todo = [r for r in rows if r['pair_id'] not in done]
    print(f'{len(rows)} pairs, {len(todo)} to run (budget {a.budget}s, bounds 1..{a.max_bound}, {a.procs} procs)', flush=True)
    t0 = time.time()
    ctx = mp.get_context('fork')
    with ctx.Pool(a.procs, initializer=init_worker, initargs=(a.budget, a.max_bound, a.mem_mb, a.keep_ce),
                  maxtasksperchild=200) as pool, open(a.out, 'a') as f:
        for i, res in enumerate(pool.imap_unordered(work, todo, chunksize=1)):
            f.write(json.dumps(res, default=str) + '\n')
            f.flush()
            if (i + 1) % 20 == 0:
                print(f'{i + 1}/{len(todo)} {time.time() - t0:.0f}s', flush=True)
    print('done', round(time.time() - t0, 1))


if __name__ == '__main__':
    main()
