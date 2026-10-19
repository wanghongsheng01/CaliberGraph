"""S3-D descriptive: size of the mined data profile on BIRD vs. Spider dev (docs/en/17, S3-D 'Descriptive').
Usage: python src_s3/s3d_profile.py -> results/stage3/s3d/profile_compare.json"""
import json, os, sqlite3, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src_r'))
from cgx.certify import SchemaInfo  # noqa: E402
from cgx.profile_r import ProfileR  # noqa: E402


def stats(root):
    ddl = json.load(open(os.path.join(root, 'data', 'raw', 'bird_schema_ddl.json')))
    P = json.load(open(os.path.join(root, 'data', 'official', 'profile_R.json')))
    F = json.load(open(os.path.join(root, 'data', 'official', 'profile_FD.json')))
    out = dict(databases=0, tables=0, columns=0, rows=0, domain_cols=0, categorical_cols=0, ucc=0, ind_fk=0,
               ind_total=0, fd=0, cross=0, lookup_tables=0, never_null_cols=0)
    for db, d in ddl.items():
        s = SchemaInfo(d)
        if db not in P:
            continue
        p = dict(P[db]); p.update(F.get(db, {}))
        pr = ProfileR(p, s)
        out['databases'] += 1
        out['tables'] += len(s.tables)
        out['columns'] += sum(len(t['columns']) for t in s.tables.values())
        con = sqlite3.connect(f"file:{os.path.join(root, 'data', 'official', 'dev_databases', db, db + '.sqlite')}?mode=ro", uri=True)
        for t in s.tables:
            out['rows'] += con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        out['domain_cols'] += len(pr.dom)
        out['categorical_cols'] += len(pr.categorical)
        out['ucc'] += len(pr.ucc); out['ind_fk'] += len(pr.ind_fk); out['ind_total'] += len(pr.ind_total)
        out['fd'] += len(pr.fd); out['cross'] += len(pr.cross); out['lookup_tables'] += len(pr.lookup)
        out['never_null_cols'] += sum(1 for k, v in pr.col.items() if v.get('n_null', 1) == 0 and v.get('n', 0) > 0)
    out['rows_per_table'] = out['rows'] / out['tables']
    out['domain_share'] = out['domain_cols'] / out['columns']
    out['categorical_share'] = out['categorical_cols'] / out['columns']
    out['ucc_per_table'] = out['ucc'] / out['tables']
    out['fd_per_table'] = out['fd'] / out['tables']
    return out


res = {'BIRD': stats(ROOT), 'Spider': stats(os.path.join(ROOT, 'spider'))}
os.makedirs(os.path.join(ROOT, 'results', 'stage3', 's3d'), exist_ok=True)
json.dump(res, open(os.path.join(ROOT, 'results', 'stage3', 's3d', 'profile_compare.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
