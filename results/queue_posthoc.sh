#!/bin/bash
# POST-FREEZE exploratory runs (not pre-registered). Started automatically after the frozen test queue.
# Code: src_v5/ (frozen src/ plus: never_null-aware generation for CGX, fuzz and ParSEval acceptance;
# certifier-in-the-loop acceptance for the fuzzing baseline, which the frozen fuzz lacked).
set -u
R=/home/claude/work/results/test
P=$R/posthoc
mkdir -p $P
while ! grep -q ALL_DONE $R/queue.log; do sleep 60; done
cd /home/claude/work/src_v5
B=5
run() { echo "$(date -Is) START $*" >> $P/queue.log; "$@"; echo "$(date -Is) END $1 $2 $3" >> $P/queue.log; }
# 1) fuzz with certifier-in-the-loop: only pairs where frozen fuzz returned a differing but non-L1f database
python3 - <<'PY'
import json, sys
sys.path.insert(0, '.')
from score import load_pairs, is_cert
P = {p['pair_id']: p for p in load_pairs('test')}
for sub in ('exc', 'exi'):
    ids = []
    for l in open(f'/home/claude/work/results/test/fuzz_{sub}.jsonl'):
        r = json.loads(l)
        if r.get('found') and not is_cert(r, 'L1f', 'C_set', P[r['pair_id']]):
            ids.append(r['pair_id'])
    json.dump(dict(pair_ids=ids), open(f'/home/claude/work/results/test/posthoc/fuzzcert_ids_{sub}.json', 'w'))
    print(sub, len(ids))
PY
for s in exc exi; do
  run python3 run_method.py --method fuzz_cert --split test --subset $s --dedup --ids $P/fuzzcert_ids_$s.json --budget $B --procs 2 --out $P/fuzz_cert_rerun_$s.jsonl > $P/fuzz_cert_rerun_$s.log 2>&1
done
# (P3 nullability-aware variants dropped: superseded by the data-profile tier R, see docs/06)
echo "$(date -Is) ALL_DONE" >> $P/queue.log
