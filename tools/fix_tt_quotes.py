"""Typography fixes for the journal manuscript (idempotent).

1. Inside \\texttt{...}: straight single quotes ' -> \\textquotesingle{} and backquotes ` -> \\textasciigrave{},
   so that SQL literals print as upright typewriter quotes in every font setup (Overleaf included).
2. Outside math and \\texttt: Unicode quotes and dashes typed in an editor -> LaTeX English quotes and dashes
   (“ ” -> `` '', ‘ ’ -> ` ', – -> --, — -> ---), and a straight " used as an opening/closing quote -> `` / ''.
Usage: python tools/fix_tt_quotes.py FILE.tex [...]
"""
import re
import sys


def fix_texttt(s):
    out, i = [], 0
    key = '\\texttt{'
    while True:
        j = s.find(key, i)
        if j < 0:
            out.append(s[i:])
            break
        out.append(s[i:j + len(key)])
        k, depth = j + len(key), 1
        while k < len(s) and depth:
            if s[k] == '\\' and k + 1 < len(s):
                k += 2
                continue
            depth += {'{': 1, '}': -1}.get(s[k], 0)
            k += 1
        body = s[j + len(key):k - 1]
        body = body.replace('\\textquotesingle{}', '\x00').replace("'", '\\textquotesingle{}').replace('\x00', '\\textquotesingle{}')
        body = body.replace('`', '\\textasciigrave{}')
        out.append(body + '}')
        i = k
    return ''.join(out)


def fix_unicode(s):
    s = s.replace('\u201c', '``').replace('\u201d', "''").replace('\u2018', '`').replace('\u2019', "'")
    s = s.replace('\u2014', '---').replace('\u2013', '--').replace('\u00a0', '~')
    # straight double quotes in running text (not in LaTeX commands like \" or in math): "word" -> ``word''
    s = re.sub(r'(?<![\\\w])"(?=\S)([^"\n$]*?\S)"', r"``\1''", s)
    return s


def main(files):
    for f in files:
        s = open(f, encoding='utf-8').read()
        t = fix_unicode(fix_texttt(s))
        if t != s:
            open(f, 'w', encoding='utf-8').write(t)
            print('fixed', f)


if __name__ == '__main__':
    main(sys.argv[1:])
