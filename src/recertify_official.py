"""Post-hoc (not pre-registered) re-certification of stored witnesses with format profiles derived
from the official BIRD databases (data/official/format_profiles.json). Writes the report under the
key 'cert_official' so that the pre-registered 'cert' stays untouched.

Usage: python recertify_official.py results/test/cgx_exc.jsonl [more files]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from cgx.certify import SchemaInfo, certify, jsonable, format_profile_from_db  # noqa: E402
from cgx.sqlinfo import Analyzer  # noqa: E402
from run_method import load_realism  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')


def main(files):
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    schemas = {db: SchemaInfo(s) for db, s in ddl.items()}
    ans = {db: Analyzer(s) for db, s in schemas.items()}
    realism = {db: load_realism(db, s) for db, s in schemas.items()}
    prof = json.load(open(os.path.join(ROOT, 'data', 'official', 'format_profiles.json')))
    formats = {db: format_profile_from_db(prof[db], s) for db, s in schemas.items()}
    pairs = {json.loads(l)['pair_id']: json.loads(l) for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl'))}
    for path in files:
        rows = [json.loads(l) for l in open(path)]
        n = 0
        for r in rows:
            w = r.get('witness')
            if not w:
                continue
            p = pairs[r['pair_id']]
            an = ans[p['db_id']]
            refs = an.analyze(p['gold']).tables | an.analyze(p['pred']).tables
            r['cert_official'] = jsonable(certify(schemas[p['db_id']], w, p['gold'], p['pred'], referenced_tables=refs,
                                                  realism=realism[p['db_id']], formats=formats[p['db_id']]))
            n += 1
        with open(path, 'w') as f:
            for r in rows:
                f.write(json.dumps(r, default=str) + '\n')
        print(path, 'recertified', n)


if __name__ == '__main__':
    main(sys.argv[1:])
