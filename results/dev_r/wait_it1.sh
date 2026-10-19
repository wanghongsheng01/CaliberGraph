#!/bin/bash
while ! grep -q ALL_DONE /home/claude/work/results/dev_r/it1/iter.log 2>/dev/null; do sleep 20; done
/home/claude/work/results/dev_r/run_iter.sh it2 cgx_r cgx_r_exi fuzz_r
