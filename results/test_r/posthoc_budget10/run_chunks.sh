#!/bin/sh
# Post-hoc budget sensitivity: frozen second-freeze code, 10 s per distinct pair, one worker (one core),
# on the random test subsample split into 4 chunks (each background job must finish within 2 h).
# Usage: run_chunks.sh METHOD CHUNK...
cd /home/claude/work/src_r
R=../results/test_r/posthoc_budget10
m=$1; shift
for c in "$@"; do
  echo "$(date -Is) START $m chunk$c" >> $R/queue.log
  python3 run_method.py --method $m --split test --subset exc --dedup --ids $R/chunk$c.json --budget 10 --procs 1 \
     --out $R/${m}_b10_chunk$c.jsonl > $R/${m}_b10_chunk$c.log 2>&1
  echo "$(date -Is) END $m chunk$c rc=$?" >> $R/queue.log
done
