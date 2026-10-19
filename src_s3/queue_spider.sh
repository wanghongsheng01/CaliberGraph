#!/bin/bash
# Stage 3, S3-D: Spider dev, executed ONCE after docs/FREEZE_S3.md (docs/en/17, S3-D; amendment E6).
# Run nothing else on the machine meanwhile: the 5 s budget is wall-clock time (2 CPUs, --procs 2).
# Resumable: a step whose output already exists is skipped (rule S3-0.4).
set -u
W=/home/claude/work
S=$W/spider
B=5
LOG=$S/results/queue.log
mkdir -p $S/results
log() { echo "$(date -Is) $*" >> $LOG; }
if [ ! -f $S/data/build.done ]; then
  log START build
  set -e
  python3 $W/src_s3/spider_build.py --spider /home/claude/ext/spider_full/spider --out $S --mode dev --procs 2 > $S/results/build.log 2>&1
  cd $S/src_r
  D=../data/official/dev_databases
  for step in "db_profile.py $D" "mine_profile.py $D" "mine_fd.py $D" "sample_rows.py $D" "build_realdb.py $D" "exec_check.py"; do
    python3 $step >> $S/results/build.log 2>&1
  done
  for f in format_profiles.json official/profile_R.json official/profile_FD.json official/sample_rows.json exec_check.json; do
    test -s $S/data/$f
  done
  set +e
  touch $S/data/build.done
  log END build
fi
run() {  # dir method subset out
  local d=$1 m=$2 sub=$3 out=$4
  [ -f $S/results/$out.done ] && return
  log START $m $sub
  (cd $S/$d && python3 run_method.py --method $m --split test --subset $sub --dedup --budget $B --procs 2 \
      --out ../results/$out.jsonl > ../results/$out.log 2>&1) && touch $S/results/$out.done
  log END $m $sub
}
run src   cgx    exc cgx_exc
run src   fuzz   exc fuzz_exc
run src_r cgx_r  exc cgx_r_exc
run src_r fuzz_r exc fuzz_r_exc
# Fuzz baseline as in the paper (post-hoc amendment P2 of stage 1): pairs where fuzz found a witness that is
# not certified at A_1f are re-run with certifier-in-the-loop acceptance (method fuzz_cert, same seed), merged.
if [ ! -f $S/results/fuzz_exc_corrected.jsonl ]; then
  log START fuzz_cert
  python3 $W/src_s3/spider_fuzzcert.py select $S > $S/results/fuzz_cert.log 2>&1
  (cd $S/src_r && python3 run_method.py --method fuzz_cert --split test --subset exc --dedup \
      --ids ../results/fuzzcert_ids_exc.json --budget $B --procs 2 --out ../results/fuzz_cert_rerun_exc.jsonl >> ../results/fuzz_cert.log 2>&1)
  python3 $W/src_s3/spider_fuzzcert.py merge $S >> $S/results/fuzz_cert.log 2>&1
  log END fuzz_cert
fi
# tier R for the first-freeze methods
for f in cgx_exc fuzz_exc_corrected; do
  [ -f $S/results/$f.recertR.done ] && continue
  (cd $S/src_r && python3 recertify_r.py ../results/$f.jsonl >> ../results/recert_r.log 2>&1) && touch $S/results/$f.recertR.done
done
run src_r cgx_r  exi cgx_r_exi
run src_r fuzz_r exi fuzz_r_exi
log ALL_DONE
