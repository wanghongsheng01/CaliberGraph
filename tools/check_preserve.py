"""Check that a polished LaTeX file preserves macros, references, citations, labels, math and numbers.
Usage: python tools/check_preserve.py OLD.tex NEW.tex   (exit code 1 if a protected token is missing or added)
Reports: protected tokens (\\V, \\ref, \\cite keys, \\label, \\Tab, \\input, inline math) whose multiset changed,
and digit sequences whose multiset changed (for manual review, e.g. 'five' -> '5' is allowed).
"""
import re
import sys
from collections import Counter


def tokens(s):
    s = re.sub(r'(?<!\\)%.*', '', s)
    prot = Counter()
    for pat in (r'\\V\{[^}]*\}', r'\\ref\{[^}]*\}', r'\\label\{[^}]*\}', r'\\Tab\{[^}]*\}', r'\\input\{[^}]*\}',
                r'\\eqref\{[^}]*\}', r'\\(?:begin|end)\{[^}]*\}'):
        prot.update(re.findall(pat, s))
    for m in re.findall(r'\\cite[pt]?\{([^}]*)\}', s):
        prot.update('cite:' + k.strip() for k in m.split(','))
    maths = Counter(re.sub(r'\s+', '', m) for m in re.findall(r'(?<!\\)\$([^$]+)\$', s))
    nums = Counter(re.findall(r'(?<![\w{\\])\d[\d,.]*\d|(?<![\w{\\])\d', re.sub(r'\\V\{[^}]*\}|\\\w+\{[^}]*\}', '', s)))
    return prot, maths, nums


def main(a, b):
    pa, ma, na = tokens(open(a).read())
    pb, mb, nb = tokens(open(b).read())
    bad = False
    for name, x, y in (('protected', pa, pb), ('math', ma, mb)):
        if x != y:
            bad = True
            print(f'[{name}] missing:', dict(x - y), ' added:', dict(y - x))
    if na != nb:
        print('[numbers, review]', 'missing:', dict(na - nb), ' added:', dict(nb - na))
    print('OK' if not bad else 'PROTECTED TOKENS CHANGED')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main(*sys.argv[1:])
