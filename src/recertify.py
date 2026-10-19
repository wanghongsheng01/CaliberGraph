"""Re-certify every stored witness of a result file with the current certifier (in place copy).

Usage: python recertify.py results/dev_cgx_v1.jsonl [--out results/dev_cgx_v1.recert.jsonl]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from cgx.certify import SchemaInfo, certify, jsonable  # noqa: E402
from cgx.sqlinfo import Analyzer  # noqa: E402
from run_method import load_realism, load_formats  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--out')
    a = ap.parse_args()
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    schemas = {db: SchemaInfo(s) for db, s in ddl.items()}
    ans = {db: Analyzer(s) for db, s in schemas.items()}
    realism = {db: load_realism(db, s) for db, s in schemas.items()}
    formats = {db: load_formats(db, s) for db, s in schemas.items()}
    pairs = {json.loads(l)['pair_id']: json.loads(l) for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl'))}
    out = a.out or a.file
    rows = [json.loads(l) for l in open(a.file)]
    n = 0
    for r in rows:
        w = r.get('witness')
        if not w:
            continue
        p = pairs[r['pair_id']]
        an = ans[p['db_id']]
        refs = an.analyze(p['gold']).tables | an.analyze(p['pred']).tables
        r['cert'] = jsonable(certify(schemas[p['db_id']], w, p['gold'], p['pred'], referenced_tables=refs,
                                     realism=realism[p['db_id']], formats=formats[p['db_id']]))
        n += 1
    with open(out, 'w') as f:
        for r in rows:
            f.write(json.dumps(r, default=str) + '\n')
    print('recertified', n, '->', out)


if __name__ == '__main__':
    main()
