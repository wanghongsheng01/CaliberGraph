#!/bin/bash
# 1) wait for dev iteration 2, 2) run the second-freeze test queue, 3) resume the paused frozen v4 queue
while ! grep -q ALL_DONE /home/claude/work/results/dev_r/it2/iter.log 2>/dev/null; do sleep 20; done
/home/claude/work/results/queue_test_r.sh
echo "$(date -Is) resuming frozen v4 queue (pid 1823)" >> /home/claude/work/results/test/queue.log
kill -CONT 1823
