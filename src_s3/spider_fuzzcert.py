"""Fuzz baseline for a Stage-3 data root, built as in stage-1 amendment P2 (src/repro_fuzz_corrected.py):
select the pairs where fuzz found a witness that is not certified at A_1f, re-run them with
certifier-in-the-loop acceptance (method fuzz_cert, run by the queue script), and merge.

Usage: python src_s3/spider_fuzzcert.py select|merge DATA_ROOT
"""
import json
import os
import sys

cmd, S = sys.argv[1], os.path.abspath(sys.argv[2])
sys.path.insert(0, os.path.join(S, 'src_r'))
from score import load_pairs, is_cert  # noqa: E402  (the frozen copy inside the data root)

R = os.path.join(S, 'results')
if cmd == 'select':
    P = {p['pair_id']: p for p in load_pairs('test')}
    ids = [r['pair_id'] for r in map(json.loads, open(os.path.join(R, 'fuzz_exc.jsonl')))
           if r.get('found') and not is_cert(r, 'L1f', 'C_set', P[r['pair_id']])]
    json.dump({'pair_ids': ids}, open(os.path.join(R, 'fuzzcert_ids_exc.json'), 'w'))
    print('selected', len(ids))
else:
    orig = [json.loads(l) for l in open(os.path.join(R, 'fuzz_exc.jsonl'))]
    re_ = {json.loads(l)['pair_id']: json.loads(l) for l in open(os.path.join(R, 'fuzz_cert_rerun_exc.jsonl'))}
    with open(os.path.join(R, 'fuzz_exc_corrected.jsonl'), 'w') as f:
        for r in orig:
            f.write(json.dumps(re_.get(r['pair_id'], r), default=str) + '\n')
    print('replaced', sum(r['pair_id'] in re_ for r in orig), 'of', len(orig))
