#!/bin/bash
# development iteration on dev subsamples (R tier). Usage: run_iter.sh TAG [methods...]
set -u
TAG=$1; shift
cd /home/claude/work/src_r
D=../results/dev_r/$TAG
mkdir -p $D
for m in "$@"; do
  case $m in
    parseval_r) ./baselines/parseval_env.sh baselines/parseval_run.py --variant r --split dev --subset exc --ids ../data/dev_sub_exc.json --budget 5 --procs 2 --out $D/parseval_r_exc.jsonl > $D/parseval_r_exc.log 2>&1
                python3 baselines/parseval_certify.py $D/parseval_r_exc.jsonl >> $D/parseval_r_exc.log 2>&1
                python3 recertify_r.py $D/parseval_r_exc.jsonl >> $D/parseval_r_exc.log 2>&1 ;;
    *_exi) mm=${m%_exi}; python3 run_method.py --method $mm --split dev --subset exi --dedup --ids ../data/dev_sub_exi.json --budget 5 --procs 2 --out $D/${mm}_exi.jsonl > $D/${mm}_exi.log 2>&1 ;;
    *) python3 run_method.py --method $m --split dev --subset exc --dedup --ids ../data/dev_sub_exc.json --budget 5 --procs 2 --out $D/${m}_exc.jsonl > $D/${m}_exc.log 2>&1 ;;
  esac
  echo "$(date -Is) done $m" >> $D/iter.log
done
echo "$(date -Is) ALL_DONE" >> $D/iter.log
