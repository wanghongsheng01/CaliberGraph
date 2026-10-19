"""Import SpotIt / SpotIt+ released results and re-certify their counterexamples.

SpotIt's pipeline rewrites identifiers and upper-cases string literals before verification and
validates counterexamples against its rewritten SQL. Here each released counterexample database
is mapped back to the original BIRD schema (table names case-insensitively, columns through the
released clean_to_orig mapping) and certified against the ORIGINAL SQL strings and DDL by the same
certifier used for every method.

Output rows use the run_method.py format, with method = spotit_<variant>.
Usage: python -m baselines.spotit_import --variant vanilla_null --split dev
Variants: vanilla_null (the validated+cross-checked release, VeriEQL_results_val_cc_null),
          llm (SpotIt+ with LLM-validated constraints), rule_based (SpotIt+-NoV).
"""
import argparse
import csv
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from cgx.certify import SchemaInfo, RealismConstraints, FormatProfile, certify, jsonable  # noqa: E402
from cgx.sqlinfo import Analyzer  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
SPOT = os.environ.get('SPOTIT_EVAL', '/home/claude/ext/SpotIt-plus/verieql/evaluation')


def parse_ce(path):
    """Execute the released counterexample script in a scratch SQLite DB; return {TABLE: (cols, rows)}."""
    text = open(path).read()
    import re
    script = []
    for line in text.splitlines():
        if line.startswith('-- ----------sql1'):
            break
        if line.startswith('--'):
            continue
        # quote identifiers: released scripts contain keywords (ORDER) and digit-led names
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
    con.executescript('\n'.join(script))
    out = {}
    for (name,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        cols = [r[1] for r in con.execute(f'PRAGMA table_info("{name}")')]
        rows = con.execute(f'SELECT * FROM "{name}"').fetchall()
        out[name] = (cols, rows)
    con.close()
    return out


def to_witness(ce, schema, c2o):
    c2o_up = {k.upper(): v for k, v in c2o.items()}
    w, unmapped = {}, []
    for tname, (cols, rows) in ce.items():
        t = schema.table(tname)
        if t is None:
            unmapped.append(('table', tname))
            continue
        orig_cols = [c['name'] for c in t['columns']]
        low = {c.lower(): i for i, c in enumerate(orig_cols)}
        idx = []
        for c in cols:
            o = c2o_up.get(c.upper(), c)
            j = low.get(o.lower(), low.get(c.lower()))
            if j is None:
                unmapped.append(('column', tname, c))
            idx.append(j)
        out_rows = []
        for r in rows:
            nr = [None] * len(orig_cols)
            for v, j in zip(r, idx):
                if j is not None:
                    nr[j] = v
            out_rows.append(nr)
        w[t['name']] = out_rows
    return w, unmapped


def claimed(variant, model):
    """Return {qid: counterexample_path} for pairs the variant claims non-equivalent."""
    out = {}
    if variant == 'vanilla_null':
        f = os.path.join(SPOT, 'VeriEQL_results_val_cc_null', f'{model}_sql.json.csv')
        for r in csv.DictReader(open(f)):
            if r['verieql_res'] == 'incorrect':
                out[int(r['question_id'])] = os.path.join(SPOT, r['counterexample_path'].lstrip('./'))
        return out
    if variant == 'null_raw':
        d = os.path.join(SPOT, 'VeriEQL_results_null', f'{model}_sql.json')
    else:
        d = os.path.join(SPOT, 'VeriEQL_results', f'{model}_{variant}')
    if not os.path.exists(d):
        return out
    best = {}
    for r in csv.DictReader(open(os.path.join(d, 'results.csv'))):
        if r['equivalent'] == 'False':
            q, b = int(r['question_id']), int(r['bound_size'])
            if q not in best or b < best[q]:
                best[q] = b
    for q, b in best.items():
        out[q] = os.path.join(d, f'counterexample_{q}_bound{b}.txt')
    return out


def times(variant, model):
    """Total released verification time per question (sum over bounds), seconds."""
    if variant in ('vanilla_null', 'null_raw'):
        d = os.path.join(SPOT, 'VeriEQL_results_null', f'{model}_sql.json')
    else:
        d = os.path.join(SPOT, 'VeriEQL_results', f'{model}_{variant}')
    out = {}
    f = os.path.join(d, 'results.csv')
    if not os.path.exists(f):
        return out
    for r in csv.DictReader(open(f)):
        try:
            out[int(r['question_id'])] = out.get(int(r['question_id']), 0.0) + float(r['time_cost'] or 0)
        except ValueError:
            pass
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--variant', default='vanilla_null')
    ap.add_argument('--split', default='dev')
    a = ap.parse_args()
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    schemas = {db: SchemaInfo(s) for db, s in ddl.items()}
    ans = {db: Analyzer(s) for db, s in schemas.items()}
    mapping = json.load(open(os.path.join(ROOT, 'data', 'raw', 'spotit', 'column_name_mapping.json')))['clean_to_orig']
    realism = {}
    for db, s in schemas.items():
        f = os.path.join(ROOT, 'data', 'raw', 'spotit_constraints', 'LLM', f'{db}_constraints_LLM.json')
        realism[db] = RealismConstraints(json.load(open(f)), mapping.get(db, {}), s) if os.path.exists(f) else None
    rb = json.load(open(os.path.join(ROOT, 'data', 'raw', 'spotit_constraints', 'rule_based', 'all_constraints.json')))
    from run_method import load_formats
    formats = {db: load_formats(db, s) for db, s in schemas.items()}
    pairs = [json.loads(l) for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl'))]
    pairs = [p for p in pairs if p['split'] == a.split and p['source'] != 'parseval_model']
    claims, tms = {}, {}
    for model in sorted({p['source'] for p in pairs}):
        claims[model] = claimed(a.variant, model)
        tms[model] = times(a.variant, model)
    out_path = os.path.join(ROOT, 'results', f'{a.split}_spotit_{a.variant}.jsonl')
    n_claim = n_cert = 0
    with open(out_path, 'w') as f:
        for p in pairs:
            ce_path = claims[p['source']].get(p['qid'])
            row = dict(pair_id=p['pair_id'], method=f'spotit_{a.variant}', found=False, author_claim=ce_path is not None,
                       released_time_s=tms[p['source']].get(p['qid']))
            if ce_path is not None:
                n_claim += 1
                row['found'] = True
                row['ce_path'] = os.path.relpath(ce_path, SPOT)
                try:
                    ce = parse_ce(ce_path)
                    w, unmapped = to_witness(ce, schemas[p['db_id']], mapping.get(p['db_id'], {}))
                    an = ans[p['db_id']]
                    refs = an.analyze(p['gold']).tables | an.analyze(p['pred']).tables
                    rep = certify(schemas[p['db_id']], w, p['gold'], p['pred'], referenced_tables=refs,
                                  realism=realism[p['db_id']], formats=formats[p['db_id']])
                    row['cert'] = jsonable(rep)
                    row['unmapped'] = unmapped
                    row['witness'] = w
                    n_cert += bool(rep.get('L0') and rep.get('differ', {}).get('C_set'))
                except Exception as e:  # noqa: BLE001
                    row['error'] = f'{type(e).__name__}: {e}'
            f.write(json.dumps(row, default=str) + '\n')
    print(a.variant, a.split, 'claims', n_claim, 'certified L0/C_set', n_cert, '->', out_path)


if __name__ == '__main__':
    main()
