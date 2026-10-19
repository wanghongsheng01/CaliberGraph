"""Record whether each gold/pred query executes on the empty schema (SQLite) -> data/exec_check.json."""
import json, os, sqlite3, time
ROOT = os.path.join(os.path.dirname(__file__), '..')
ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
cons = {}
for db, stmts in ddl.items():
    c = sqlite3.connect(':memory:')
    for s in stmts:
        c.executescript(s)
    cons[db] = c
out = {}
for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl')):
    r = json.loads(l)
    c = cons[r['db_id']]
    res = {}
    for k in ('gold', 'pred'):
        dl = time.monotonic() + 2
        c.set_progress_handler(lambda: 1 if time.monotonic() > dl else 0, 1000)
        try:
            c.execute(r[k]).fetchall(); res[k] = True
        except Exception as e:
            res[k] = str(e)[:120]
        c.set_progress_handler(None, 0)
    out[r['pair_id']] = res
json.dump(out, open(os.path.join(ROOT, 'data', 'exec_check.json'), 'w'))
import collections
print(collections.Counter((v['gold'] is True, v['pred'] is True) for v in out.values()))
