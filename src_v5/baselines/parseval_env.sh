#!/bin/bash
# ParSEval's pinned dependency environment (no PyPI access needed; all sources cloned from GitHub)
export PYTHONPATH=/home/claude/ext/sqlglot-v23.12.1:/home/claude/ext/sqlalchemy-2.0.49/lib:/home/claude/ext/z3-4.16.0/build/python:/home/claude/ext/ParSEval/src
export LD_LIBRARY_PATH=/home/claude/ext/z3-4.16.0/build:$LD_LIBRARY_PATH
exec python3 "$@"
