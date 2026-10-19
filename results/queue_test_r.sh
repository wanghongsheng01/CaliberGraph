#!/bin/bash
# Second freeze (tier R): held-out test runs, executed ONCE after docs/FREEZE_R.md was written.
set -u
cd /home/claude/work/src_r
R=../results/test_r
mkdir -p $R
B=5
S=../data/test_subsample.json
run() { echo "$(date -Is) START $*" >> $R/queue.log; "$@"; echo "$(date -Is) END $1 $2 $3" >> $R/queue.log; }
run python3 run_method.py --method cgx_r --split test --subset exc --dedup --budget $B --procs 2 --out $R/cgx_r_exc.jsonl > $R/cgx_r_exc.log 2>&1
run python3 run_method.py --method fuzz_r --split test --subset exc --dedup --budget $B --procs 2 --out $R/fuzz_r_exc.jsonl > $R/fuzz_r_exc.log 2>&1
run python3 run_method.py --method cgx_r --split test --subset exi --dedup --budget $B --procs 2 --out $R/cgx_r_exi.jsonl > $R/cgx_r_exi.log 2>&1
run python3 run_method.py --method fuzz_r --split test --subset exi --dedup --budget $B --procs 2 --out $R/fuzz_r_exi.jsonl > $R/fuzz_r_exi.log 2>&1
run ./baselines/parseval_env.sh baselines/parseval_run.py --variant r --split test --subset exc --ids $S --budget $B --procs 2 --out $R/parseval_r_sub.jsonl > $R/parseval_r_sub.log 2>&1
python3 baselines/parseval_certify.py $R/parseval_r_sub.jsonl >> $R/parseval_r_sub.log 2>&1
python3 recertify_r.py $R/parseval_r_sub.jsonl >> $R/parseval_r_sub.log 2>&1
for m in cgx_r_noreal cgx_r_nosyn cgx_r_noanchor cgx_r_nojoin; do
  run python3 run_method.py --method $m --split test --subset exc --dedup --ids $S --budget $B --procs 2 --out $R/abl_${m}.jsonl > $R/abl_${m}.log 2>&1
done
echo "$(date -Is) ALL_DONE" >> $R/queue.log
