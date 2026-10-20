#!/bin/bash
# Post hoc analyses requested by the Information Systems pre-submission review (amendment E20). Resumable.
set -u
cd /home/claude/work
P=results/posthoc_rev
log() { echo "$(date -Is) $*" >> $P/queue.log; }
if [ ! -f $P/rerun_cg.done ]; then log START rerun cgx
  (cd src && python3 run_method.py --method cgx --split test --subset exc --dedup --ids ../$P/ids_rerun500.json --budget 5 --procs 2 --out ../$P/cgx_rerun.jsonl > ../$P/cgx_rerun.log 2>&1) && touch $P/rerun_cg.done; log END rerun cgx; fi
if [ ! -f $P/rerun_cgr.done ]; then log START rerun cgx_r
  (cd src_r && python3 run_method.py --method cgx_r --split test --subset exc --dedup --ids ../$P/ids_rerun500.json --budget 5 --procs 2 --out ../$P/cgx_r_rerun.jsonl > ../$P/cgx_r_rerun.log 2>&1) && touch $P/rerun_cgr.done; log END rerun cgx_r; fi
if [ ! -f $P/spotit60.done ]; then log START spotit 60s
  python3 src_s3/spotit_run.py --split test --subset exc --dedup --exclude-sources parseval_model --ids $P/ids_spotit150.json --budget 60 --max-bound 5 --hash-seed 0 --procs 2 --allow-test --out $P/spotit60.jsonl > $P/spotit60.log 2>&1 && touch $P/spotit60.done; log END spotit 60s; fi
log ALL_DONE
