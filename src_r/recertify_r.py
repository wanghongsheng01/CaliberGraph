"""Add the tier-R check (data-profile constraints mined from the official databases) to stored
results of any method, under the key 'cert_R'; the pre-registered 'cert' is left untouched.
Usage: python recertify_r.py FILE.jsonl [...]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from cgx.certify import SchemaInfo  # noqa: E402
from run_method import load_profile_r  # noqa: E402
from score import qcols  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')


def main(files):
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    schemas = {db: SchemaInfo(s) for db, s in ddl.items()}
    prof, _ = load_profile_r(schemas)
    pairs = {json.loads(l)['pair_id']: json.loads(l) for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl'))}
    for path in files:
        rows = [json.loads(l) for l in open(path)]
        n = ok = 0
        for r in rows:
            w = r.get('witness')
            p = pairs.get(r['pair_id'])
            if not w or p is None:
                continue
            s = schemas[p['db_id']]
            w2 = {}
            for t, rr in w.items():
                tt = s.table(t)
                if tt is not None:
                    w2[tt['name']] = rr
            try:
                viol = prof[p['db_id']].violations(w2)
            except Exception as e:  # noqa: BLE001
                viol = [f'error {type(e).__name__}: {e}']
            try:
                okq = prof[p['db_id']].ok(w2, qcols(p))
            except Exception:  # noqa: BLE001
                okq = False
            r['cert_R'] = dict(ok=not viol, okq=okq, violations=viol[:8], n_violations=len(viol))
            n += 1
            ok += not viol
        with open(path + '.tmp', 'w') as f:
            for r in rows:
                f.write(json.dumps(r, default=str) + '\n')
        os.replace(path + '.tmp', path)
        print(path, 'checked', n, 'R-ok', ok, flush=True)


if __name__ == '__main__':
    main(sys.argv[1:])
