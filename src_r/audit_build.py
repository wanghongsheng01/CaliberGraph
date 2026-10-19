"""Build a blinded attribution-annotation batch from certified witnesses of one or more methods.

Usage:
  python audit_build.py --split dev --out ../results/audit/NAME --seed 1 \
      --src cgx_r=../results/dev_r/cgx_r_exc.jsonl:R:100 --src v4=../results/dev_cgx_v4.jsonl:L1f:100
Writes NAME_blind.json (items without method labels, shuffled) and NAME_key.json (idx -> source).
"""
import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from cgx.certify import SchemaInfo  # noqa: E402
from score import load_pairs, is_cert  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--split', default='dev')
    ap.add_argument('--out', required=True)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--src', action='append', required=True, help='label=path:tier[:n]')
    ap.add_argument('--only', default='', help='optional JSON list of pair_ids to restrict to')
    a = ap.parse_args()
    dev = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_dev_20240627.json')))
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    S = {db: SchemaInfo(s) for db, s in ddl.items()}
    P = {p['pair_id']: p for p in load_pairs(a.split)}
    only = set(json.load(open(a.only))) if a.only else None
    rng = random.Random(a.seed)
    items = []
    for spec in a.src:
        label, rest = spec.split('=', 1)
        parts = rest.split(':')
        path, tier = parts[0], parts[1]
        n = int(parts[2]) if len(parts) > 2 else 0
        seen, cand = set(), []
        for l in open(path):
            r = json.loads(l)
            p = P.get(r['pair_id'])
            if p is None or p['ex'] != 'correct' or (only is not None and r['pair_id'] not in only):
                continue
            if not is_cert(r, tier, 'C_set', p):
                continue
            k = (p['qid'], p['gold'].strip(), p['pred'].strip())
            if k in seen:
                continue
            seen.add(k)
            cand.append((r, p))
        pick = rng.sample(cand, n) if n and n < len(cand) else cand
        for r, p in pick:
            q = dev[p['qid']]
            w = {}
            for t, rows in r['witness'].items():
                tt = S[p['db_id']].table(t)
                w[t] = dict(columns=[c['name'] for c in tt['columns']] if tt else None, rows=rows)
            c = r['cert']
            items.append(dict(source=label, pair_id=p['pair_id'], db_id=p['db_id'], question=q['question'],
                              evidence=q['evidence'], gold=p['gold'], pred=p['pred'], witness=w,
                              gold_rows=c.get('gold_rows'), pred_rows=c.get('pred_rows')))
        print(label, 'pool', len(cand), 'sampled', len(pick))
    rng.shuffle(items)
    key = []
    for i, it in enumerate(items):
        it['idx'] = i
        key.append(dict(idx=i, source=it.pop('source'), pair_id=it['pair_id']))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(items, open(a.out + '_blind.json', 'w'), indent=1, default=str, ensure_ascii=False)
    json.dump(key, open(a.out + '_key.json', 'w'), indent=1)
    print('items', len(items))


if __name__ == '__main__':
    main()
