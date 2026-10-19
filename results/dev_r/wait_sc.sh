#!/bin/bash
# wait until the frozen CGX+SC run (pid 23825) has exited (zombie counts as exited: its parent queue is paused)
while [ -e /proc/23825 ] && ! grep -q '^State:.*Z' /proc/23825/status 2>/dev/null; do sleep 30; done
/home/claude/work/results/dev_r/run_iter.sh it1 cgx_r fuzz_r cgx_r_exi fuzz_r_exi parseval_r
