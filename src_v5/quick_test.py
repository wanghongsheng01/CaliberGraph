"""Run CGX on specific pair ids (development diagnostics only)."""
import json, sys, time
import run_method as rm
ids = sys.argv[2:]
method = sys.argv[1]
rm.init_worker(method, 5.0)
P = {json.loads(l)['pair_id']: json.loads(l) for l in open('../data/pairs.jsonl')}
n = 0
for i in ids:
    r = rm.work(P[i])
    ok = bool((r.get('cert') or {}).get('L1f')) and r['cert']['differ']['C_set']
    n += ok
    print(i, 'FOUND' if ok else '-', r.get('phase'), round(r.get('search_s', 0), 2), r.get('error', ''))
print('total', n, '/', len(ids))
