#!/bin/bash
cd /home/claude/work/src
python3 run_method.py --method cgx --split dev --subset exc --dedup --budget 5 --procs 2 --out ../results/dev_cgx_v4.jsonl > ../results/dev_cgx_v4.log 2>&1
python3 run_method.py --method cgx --split dev --subset exi --dedup --budget 5 --procs 2 --out ../results/dev_cgx_v4_exi.jsonl > ../results/dev_cgx_v4_exi.log 2>&1
echo DONE > ../results/queue_dev4.done
