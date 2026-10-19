#!/bin/bash
# Runs the Stage-3 queues for at most ~105 minutes, then stops cleanly (both queues are resumable; rule S3-0.4).
# Before resuming, a truncated last line of any result file (from a hard stop) is removed.
for f in /home/claude/work/spider/results/*.jsonl /home/claude/work/minidev/results/*.jsonl; do
  [ -f "$f" ] || continue
  python3 - "$f" <<'P'
import json, sys
p = sys.argv[1]
lines = open(p).read().split('\n')
ok = []
for l in lines:
    if not l.strip():
        continue
    try:
        json.loads(l); ok.append(l)
    except ValueError:
        print('dropped truncated line in', p)
open(p, 'w').write('\n'.join(ok) + ('\n' if ok else ''))
P
done
timeout --signal=TERM 6300 bash -c '/home/claude/work/src_s3/queue_spider.sh && /home/claude/work/src_s3/queue_minidev.sh'
echo "chunk exit $?"
pkill -f "run_method.py" 2>/dev/null
tail -3 /home/claude/work/spider/results/queue.log
