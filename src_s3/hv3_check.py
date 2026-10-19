"""Round-3 process check (docs/en/17c, "Process record"): compare each returned sheet with its blank sheet.

Two levels:
  exact       -- line-by-line diff outside the Verdict and Reason lines (what 17c pre-states);
  normalised  -- the same after undoing pure Markdown re-formatting (blank lines, trailing spaces, table-cell
                 padding and separator rows, backslash escapes, `_x_` vs `*x*` emphasis, code-fence language tags),
                 so that content changes (values, queries, facts) can be told apart from editor re-formatting.
Per item, also extracts the verdict and reason, and reports header fields (start, finish, AI-tool use).
Usage: python src_s3/hv3_check.py DIR OUT.json
"""
import difflib
import json
import os
import re
import sys

LABELS = ('pred_wrong', 'gold_wrong', 'both_wrong', 'ambiguous', 'implausible_data')


def split_items(text):
    head, *rest = re.split(r'\n(?=## Item R3-\d{3})', text)
    items = {}
    for blk in rest:
        code = re.match(r'## Item (R3-\d{3})', blk).group(1)
        items[code] = blk
    return head, items


def norm_line(l):
    l = l.rstrip()
    l = l.replace('\\', '')
    l = re.sub(r'\[([^\]]+)\]\(\1\)', r'\1', l)  # editor auto-links: [URL](URL) -> URL
    l = re.sub(r'^_(\S+?)_(?= \(|$)', r'*\1*', l)  # table captions: _name_ -> *name*
    l = re.sub(r'(?<![\w*])_([^_\s][^_]*?)_(?![\w*])', r'*\1*', l)
    if re.fullmatch(r'\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?', l.strip()):
        return '|---|'
    if l.strip().startswith('|'):
        cells = [c.strip() for c in l.strip().strip('|').split('|')]
        return '|' + '|'.join(cells) + '|'
    l = re.sub(r'^```\w+$', '```', l)
    l = re.sub(r'^(\s*)[-*+] ', r'\1- ', l)
    return re.sub(r'\s+', ' ', l).strip()


def body(blk, normalised):
    out = []
    for l in blk.split('\n'):
        if re.match(r'\s*\*\*Verdict:\*\*', l) or re.match(r'\s*\*\*Reason \(one sentence\):\*\*', l):
            continue
        if normalised:
            l = norm_line(l)
            if not l:
                continue
        out.append(l)
    return out


def verdict(blk):
    m = re.search(r'\*\*Verdict:\*\*\s*`?\s*([A-Za-z_]+)', blk)
    v = m.group(1).strip().lower() if m else None
    r = re.search(r'\*\*Reason \(one sentence\):\*\*\s*(.*)', blk)
    return (v if v in LABELS else (None if v in (None, '____') else 'INVALID:' + v)), (r.group(1).strip() if r else '')


def header(head):
    g = lambda k: (re.search(re.escape(k) + r'\*\*\s*(.*)', head) or [None, None])[1]
    return dict(started=g('Started (date, time):'), finished=g('Finished (date, time):'),
                ai_tool=g('for this sheet?'))


def main(d, out):
    R = {}
    for w in 'ABC':
        blank = open(os.path.join(d, f'sheet_r3_annotator{w}_blank.md')).read()
        got = open(os.path.join(d, f'sheet_r3_annotator{w}.md')).read()
        hb, ib = split_items(blank)
        hg, ig = split_items(got)
        rec = dict(header=header(hg), n_items=len(ig), missing=sorted(set(ib) - set(ig)),
                   extra=sorted(set(ig) - set(ib)), order_same=list(ib) == list(ig), items={})
        exact_changed, norm_changed = [], []
        for c in ib:
            if c not in ig:
                continue
            v, r = verdict(ig[c])
            e = body(ib[c], False) != body(ig[c], False)
            nb, ng = body(ib[c], True), body(ig[c], True)
            n = nb != ng
            diff = [x for x in difflib.unified_diff(nb, ng, lineterm='', n=0) if x[:1] in '+-' and x[:3] not in ('+++', '---')]
            rec['items'][c] = dict(verdict=v, reason=r, exact_changed=e, content_changed=n, content_diff=diff[:20])
            if e:
                exact_changed.append(c)
            if n:
                norm_changed.append(c)
        rec['exact_changed'] = len(exact_changed)
        rec['content_changed'] = norm_changed
        rec['header_body_changed'] = body(hb, True)[5:] != body(hg, True)[5:]
        R[w] = rec
    json.dump(R, open(out, 'w'), indent=1, ensure_ascii=False)
    for w, rec in R.items():
        print(w, rec['header'], 'items', rec['n_items'], 'order_same', rec['order_same'],
              'exact_changed', rec['exact_changed'], 'content_changed', len(rec['content_changed']),
              'no_verdict', sum(1 for x in rec['items'].values() if not x['verdict']),
              'invalid', [x['verdict'] for x in rec['items'].values() if x['verdict'] and x['verdict'].startswith('INVALID')],
              'empty_reason', sum(1 for x in rec['items'].values() if not x['reason']))


if __name__ == '__main__':
    main(*sys.argv[1:])
