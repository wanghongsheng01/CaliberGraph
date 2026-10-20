#!/bin/bash
# Whole-paper preservation check: concatenates main.tex, sections, tables and figure sources before/after.
# Usage: tools/check_all.sh ORIG_DIR NEW_DIR
cat_all() { cat "$1"/main.tex "$1"/sections/*.tex "$1"/tables/*.tex "$1"/figs/*.tex 2>/dev/null; }
T=$(mktemp -d); cat_all "$1" > $T/a.tex; cat_all "$2" > $T/b.tex
python3 /home/claude/work/tools/check_preserve.py $T/a.tex $T/b.tex
