#!/bin/bash
# 17d: dev run (descriptive), then the single test run. Resumable (the harness skips pairs already in --out).
set -u
cd /home/claude/work
O=results/stage3/spotit
L=$O/queue.log
log() { echo "$(date -Is) $*" >> $L; }
if [ ! -f $O/dev.done ]; then
  log START dev
  python3 src_s3/spotit_run.py --split dev --subset exc --dedup --exclude-sources parseval_model --budget 5 --max-bound 5 \
     --hash-seed 0 --procs 2 --out $O/spotit_dev_exc.jsonl > $O/spotit_dev_exc.log 2>&1 && touch $O/dev.done
  log END dev
fi
if [ ! -f $O/test.done ]; then
  log START test
  python3 src_s3/spotit_run.py --split test --subset exc --dedup --exclude-sources parseval_model --budget 5 --max-bound 5 \
     --hash-seed 0 --procs 2 --allow-test --out $O/spotit_test_exc.jsonl > $O/spotit_test_exc.log 2>&1 && touch $O/test.done
  log END test
fi
log ALL_DONE
