"""Post-hoc analysis (ICDE version): size of the data profile Pi per constraint class, and which
profile constraints the first-freeze witnesses at A_1f violate (share of witnesses violating each
class, on the columns either query references and on the whole witness).
Analysis only; not imported by any method. Usage:
  python profile_stats.py --out ../results/test/profile_stats.json
"""
import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from cgx.certify import SchemaInfo  # noqa: E402
from run_method import load_profile_r  # noqa: E402
from score import qcols  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
CLASSES = ['null', 'domain', 'lookup', 'ucc', 'ind', 'symmetric', 'valuedep', 'year_date']


def vclass(v):
    k = v.split(' ', 1)[0]
    if k == 'value':
        return 'null' if v.endswith('=None') else 'domain'
    return {'lookup': 'lookup', 'ucc': 'ucc', 'fk': 'ind', 'total': 'ind', 'symmetric': 'symmetric',
            'irreflexive': 'symmetric', 'fd': 'valuedep', 'cross': 'valuedep',
            'year_date': 'year_date'}.get(k, 'other')


def profile_size(prof):
    tot = collections.Counter()
    per = {}
    for db, p in prof.items():
        c = collections.Counter()
        c['columns'] = len(p.col)
        c['categorical'] = len(p.categorical)
        c['never_null'] = sum(1 for i in p.col.values() if i.get('n_null', 0) == 0)
        c['ucc'] = len(p.ucc)
        c['ind_fk'] = len(p.ind_fk)
        c['ind_total'] = len(p.ind_total)
        c['symmetric'] = len(p.symmetric) + len(p.irreflexive)
        c['lookup'] = len(p.lookup)
        c['fd_map'] = len(p.fd)
        c['cross'] = len(p.cross)
        c['year_date'] = len(p.year_date)
        per[db] = dict(c)
        tot.update(c)
    return dict(tot), per


def violations_by_class(files, prof, schemas, pairs):
    out = {}
    for name, path in files.items():
        n = 0
        anyc = collections.Counter()
        refc = collections.Counter()
        for line in open(path):
            r = json.loads(line)
            cert = r.get('cert') or {}
            if not (r.get('found') and r.get('witness') and cert.get('L1f') and cert.get('differ', {}).get('C_set')):
                continue
            p = pairs.get(r['pair_id'])
            if p is None:
                continue
            s = schemas[p['db_id']]
            w = {}
            for t, rows in r['witness'].items():
                tt = s.table(t)
                if tt is not None:
                    w[tt['name']] = rows
            pr = prof[p['db_id']]
            try:
                va = pr.violations(w)
                vr = pr.violations(w, only=qcols(p))
            except Exception:  # noqa: BLE001
                continue
            n += 1
            for c in {vclass(v) for v in va}:
                anyc[c] += 1
            for c in {vclass(v) for v in vr}:
                refc[c] += 1
        out[name] = dict(n=n,
                         whole={c: round(100 * anyc[c] / n, 1) for c in CLASSES} if n else {},
                         referenced={c: round(100 * refc[c] / n, 1) for c in CLASSES} if n else {})
        print(name, out[name], flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    schemas = {db: SchemaInfo(s) for db, s in ddl.items()}
    prof, _ = load_profile_r(schemas)
    tot, per = profile_size(prof)
    print('profile', tot, flush=True)
    pairs = {}
    for line in open(os.path.join(ROOT, 'data', 'pairs.jsonl')):
        p = json.loads(line)
        pairs[p['pair_id']] = p
    files = {'CaliberGraph': os.path.join(ROOT, 'results/test/cgx_exc.jsonl'),
             'Random fuzzing': os.path.join(ROOT, 'results/test/fuzz_exc_corrected.jsonl'),
             'ParSEval-L1': os.path.join(ROOT, 'results/test/parseval_l1_exc.jsonl')}
    viol = violations_by_class(files, prof, schemas, pairs)
    json.dump(dict(profile_total=tot, profile_per_db=per, violations=viol), open(a.out, 'w'), indent=1)


if __name__ == '__main__':
    main()
