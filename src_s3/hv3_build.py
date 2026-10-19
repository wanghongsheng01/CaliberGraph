"""Third human validation round (docs/en/17c): 150 new attributed items (75 first-stage, 75 second-stage), none used in
rounds 1-2, seed 20261022. Each of three annotators receives the same items in a different order (seeds 1, 2, 3).
Items carry the same mechanically generated facts from the official database as round 2 (src_s3/hv2_build.facts) and
the label definitions given to the AI annotator, verbatim. Item codes (R3-001 ... R3-150) are stable across sheets.
Usage: python src_s3/hv3_build.py --out results/audit/human_validation_r3
"""
import argparse
import json
import os
import random
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src_r'))
sys.path.insert(0, os.path.dirname(__file__))
from human_validation import final, fmt_table  # noqa: E402
from score import load_pairs, qcols  # noqa: E402
from hv2_build import facts  # noqa: E402

HEADER = """# Human attribution sheet, round 3 (blind) — annotator {who}

Fill in before you start and when you finish (local time):
- **Annotator ID:** {who}
- **Started (date, time):** ____
- **Finished (date, time):** ____
- **Did you use any AI tool (chat assistant, code assistant, translator) for this sheet?** ____ (yes/no; if yes, which and how)

For each item, read the question, evidence, both queries, the witness database, the two results and the facts from the real
database. Then replace `____` after **Verdict:** with exactly one of `pred_wrong`, `gold_wrong`, `both_wrong`, `ambiguous`,
`implausible_data`, and write one sentence after **Reason**. **Do not change anything else in this file**: the file is
checked automatically against the original, and any other change is reported. See INSTRUCTIONS.md for the definitions.
Work alone; do not discuss items with the other annotators until all three sheets are returned.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--seed', type=int, default=20261022)
    ap.add_argument('--n', type=int, default=75, help='items per stage')
    a = ap.parse_args()
    used = set()
    for d in ('human_validation', 'human_validation_r2'):
        used |= {(k['pair_id'], k['source']) for k in json.load(open(os.path.join(
            ROOT, 'results', 'audit', d, 'key_DO_NOT_OPEN_BEFORE_ANNOTATING.json')))}
    rng = random.Random(a.seed)
    s1 = [x for x in final('test_v4') if (x['item']['pair_id'], x['source']) not in used]
    s2 = [x for x in final('test_r') if (x['item']['pair_id'], x['source']) not in used]
    pick = rng.sample(s1, a.n) + rng.sample(s2, a.n)
    rng.shuffle(pick)
    pairs = {p['pair_id']: p for p in load_pairs('test')}
    os.makedirs(a.out, exist_ok=True)
    blocks, key = {}, []
    for n, x in enumerate(pick, 1):
        it = x['item']
        code = f'R3-{n:03d}'
        key.append(dict(code=code, pair_id=it['pair_id'], source=x['source'], ai=x['ai'],
                        stage=1 if x in s1 else 2))
        cols = qcols(pairs[it['pair_id']])
        md = [f"\n---\n\n## Item {code} ({it['db_id']})\n",
              f"**Question:** {it['question']}\n\n**Evidence:** {it.get('evidence') or '-'}\n",
              f"**Gold SQL:**\n```sql\n{it['gold']}\n```\n**Predicted SQL:**\n```sql\n{it['pred']}\n```\n",
              '**Witness database:**\n']
        for t, tv in it['witness'].items():
            md.append(fmt_table(t, tv, cols) + '\n')
        md.append(f"**Gold result on the witness:** `{it['gold_rows']}`  \n**Predicted result on the witness:** `{it['pred_rows']}`\n")
        md.append(facts(it['db_id'], it, cols))
        md.append('**Verdict:** ____  \n**Reason (one sentence):** \n')
        blocks[code] = '\n'.join(md)
    for who, s in (('A', 1), ('B', 2), ('C', 3)):
        order = sorted(blocks)
        random.Random(s).shuffle(order)
        open(os.path.join(a.out, f'sheet_r3_annotator{who}_blank.md'), 'w').write(
            HEADER.format(who=who) + ''.join(blocks[c] for c in order))
    json.dump(key, open(os.path.join(a.out, 'key_DO_NOT_OPEN_BEFORE_ANNOTATING.json'), 'w'), indent=1)
    print('wrote', len(pick), 'items x 3 orders', Counter(k['stage'] for k in key))


if __name__ == '__main__':
    main()
