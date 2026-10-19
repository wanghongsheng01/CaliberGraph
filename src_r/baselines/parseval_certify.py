"""Certify ParSEval counterexamples with the shared certifier (run in the CGX environment)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from cgx.certify import SchemaInfo, certify, jsonable  # noqa: E402
from cgx.sqlinfo import Analyzer  # noqa: E402
from run_method import load_realism, load_formats  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')


def to_witness(raw, schema):
    w = {}
    for tname, d in raw.items():
        t = schema.table(tname)
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


def main(path):
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    schemas = {db: SchemaInfo(s) for db, s in ddl.items()}
    ans = {db: Analyzer(s) for db, s in schemas.items()}
    realism = {db: load_realism(db, s) for db, s in schemas.items()}
    formats = {db: load_formats(db, s) for db, s in schemas.items()}
    pairs = {json.loads(l)['pair_id']: json.loads(l) for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl'))}
    rows = [json.loads(l) for l in open(path)]
    for r in rows:
        if r.get('raw_witness'):
            p = pairs[r['pair_id']]
            s = schemas[p['db_id']]
            w = to_witness(r['raw_witness'], s)
            r['witness'] = w
            an = ans[p['db_id']]
            refs = an.analyze(p['gold']).tables | an.analyze(p['pred']).tables
            r['cert'] = jsonable(certify(s, w, p['gold'], p['pred'], referenced_tables=refs, realism=realism[p['db_id']], formats=formats[p['db_id']]))
    with open(path, 'w') as f:
        for r in rows:
            f.write(json.dumps(r, default=str) + '\n')
    print('certified', sum(1 for r in rows if r.get('cert')))


if __name__ == '__main__':
    main(sys.argv[1])
