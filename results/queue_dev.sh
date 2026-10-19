#!/bin/bash
cd /home/claude/work/src
while pgrep -f "subset exi" > /dev/null; do sleep 20; done
python3 run_method.py --method cgx_sc --split dev --subset exc --dedup --budget 5 --procs 2 --out ../results/dev_cgx_sc_v3.jsonl > ../results/dev_cgx_sc_v3.log 2>&1
python3 run_method.py --method fuzz --split dev --subset exc --dedup --budget 5 --procs 2 --out ../results/dev_fuzz.jsonl > ../results/dev_fuzz.log 2>&1
./baselines/parseval_env.sh baselines/parseval_run.py --variant l1 --split dev --subset exc --budget 5 --procs 2 --out ../results/dev_parseval_l1.jsonl > ../results/dev_parseval_l1.log 2>&1
python3 baselines/parseval_certify.py ../results/dev_parseval_l1.jsonl >> ../results/dev_parseval_l1.log 2>&1
echo QUEUE_DONE > ../results/queue_dev.done
