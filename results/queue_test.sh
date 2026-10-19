#!/bin/bash
# Held-out test runs. Executed ONCE after the code freeze recorded in docs/FREEZE.md.
set -u
cd /home/claude/work/src
R=../results/test
mkdir -p $R
B=5
run() { echo "$(date -Is) START $*" >> $R/queue.log; "$@"; echo "$(date -Is) END $1 $2 $3" >> $R/queue.log; }
# primary population (EX-correct), all distinct pairs
run python3 run_method.py --method cgx --split test --subset exc --dedup --budget $B --procs 2 --out $R/cgx_exc.jsonl > $R/cgx_exc.log 2>&1
run ./baselines/parseval_env.sh baselines/parseval_run.py --variant l1 --split test --subset exc --budget $B --procs 2 --out $R/parseval_l1_exc.jsonl > $R/parseval_l1_exc.log 2>&1
python3 baselines/parseval_certify.py $R/parseval_l1_exc.jsonl >> $R/parseval_l1_exc.log 2>&1
run python3 run_method.py --method fuzz --split test --subset exc --dedup --budget $B --procs 2 --out $R/fuzz_exc.jsonl > $R/fuzz_exc.log 2>&1
run python3 run_method.py --method cgx_sc --split test --subset exc --dedup --budget $B --procs 2 --out $R/cgx_sc_exc.jsonl > $R/cgx_sc_exc.log 2>&1
# known positives (EX-incorrect)
run python3 run_method.py --method cgx --split test --subset exi --dedup --budget $B --procs 2 --out $R/cgx_exi.jsonl > $R/cgx_exi.log 2>&1
run ./baselines/parseval_env.sh baselines/parseval_run.py --variant l1 --split test --subset exi --budget $B --procs 2 --out $R/parseval_l1_exi.jsonl > $R/parseval_l1_exi.log 2>&1
python3 baselines/parseval_certify.py $R/parseval_l1_exi.jsonl >> $R/parseval_l1_exi.log 2>&1
run python3 run_method.py --method fuzz --split test --subset exi --dedup --budget $B --procs 2 --out $R/fuzz_exi.jsonl > $R/fuzz_exi.log 2>&1
# official ParSEval disprove (set semantics), EX-correct
run ./baselines/parseval_env.sh baselines/parseval_run.py --variant official --split test --subset exc --budget $B --procs 2 --out $R/parseval_official_exc.jsonl > $R/parseval_official_exc.log 2>&1
python3 baselines/parseval_certify.py $R/parseval_official_exc.jsonl >> $R/parseval_official_exc.log 2>&1
# ablations on the 1,000-pair subsample
S=../data/test_subsample.json
for m in cgx_noanchor cgx_noiso cgx_nojoin cgx_nodomain; do
  run python3 run_method.py --method $m --split test --subset exc --dedup --ids $S --budget $B --procs 2 --out $R/abl_${m}.jsonl > $R/abl_${m}.log 2>&1
done
# budget sensitivity (10 s) on the subsample
run python3 run_method.py --method cgx --split test --subset exc --dedup --ids $S --budget 10 --procs 2 --out $R/budget10_cgx.jsonl > $R/budget10_cgx.log 2>&1
run ./baselines/parseval_env.sh baselines/parseval_run.py --variant l1 --split test --subset exc --ids $S --budget 10 --procs 2 --out $R/budget10_parseval_l1.jsonl > $R/budget10_parseval_l1.log 2>&1
python3 baselines/parseval_certify.py $R/budget10_parseval_l1.jsonl >> $R/budget10_parseval_l1.log 2>&1
echo "$(date -Is) ALL_DONE" >> $R/queue.log
