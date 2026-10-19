#!/bin/bash
# Stage 3, S3-E: Mini-Dev systems on held-out BIRD test questions, executed ONCE after docs/FREEZE_S3.md.
# Resumable (rule S3-0.4). Run nothing else meanwhile (--procs 2 on 2 CPUs, as for BIRD).
set -u
S=/home/claude/work/minidev
B=5
mkdir -p $S/results
LOG=$S/results/queue.log
for m in cgx_r fuzz_r; do
  [ -f $S/results/${m}_exc.done ] && continue
  echo "$(date -Is) START $m" >> $LOG
  (cd $S/src_r && python3 run_method.py --method $m --split test --subset exc --dedup --budget $B --procs 2 \
     --out ../results/${m}_exc.jsonl > ../results/${m}_exc.log 2>&1) && touch $S/results/${m}_exc.done
  echo "$(date -Is) END $m" >> $LOG
done
echo "$(date -Is) ALL_DONE" >> $LOG
