"""Verify the released files against the SHA-256 lists recorded at the two freezes.
Method and baseline code must match; analysis-only scripts that were changed after a freeze are
listed in README.md and are reported here as CHANGED.

Usage: python tools/verify_freeze.py
"""
import hashlib
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LISTS = {'docs/FREEZE_SHA256.txt': 'src', 'docs/FREEZE_R_SHA256.txt': 'src_r'}
EXPECTED_CHANGED = {'src/analyze.py', 'src/db_profile.py', 'src/recompute_ex.py', 'src/score.py',
                    'src/taxonomy.py', 'src_r/analyze_r.py'}


def main():
    unexpected = 0
    for lst, base in LISTS.items():
        ok = 0
        for line in open(os.path.join(ROOT, lst)):
            m = re.match(r'([0-9a-f]{64})\s+\*?(\S.*)$', line.strip())
            if not m:
                continue
            h, p = m.groups()
            p = os.path.normpath(p)
            cand = [os.path.join(base, p), p]
            q = next((c for c in cand if os.path.exists(os.path.join(ROOT, c))), None)
            if q is None:
                print('MISSING ', p)
                unexpected += 1
                continue
            if hashlib.sha256(open(os.path.join(ROOT, q), 'rb').read()).hexdigest() == h:
                ok += 1
            else:
                tag = 'CHANGED (analysis-only, expected)' if q in EXPECTED_CHANGED else 'CHANGED (UNEXPECTED)'
                unexpected += q not in EXPECTED_CHANGED
                print(f'{tag:34s} {q}')
        print(f'{lst}: {ok} files identical')
    print('verification', 'PASSED' if unexpected == 0 else f'FAILED ({unexpected} unexpected)')


if __name__ == '__main__':
    main()
