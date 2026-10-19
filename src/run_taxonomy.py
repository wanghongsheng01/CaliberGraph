"""Root-cause labels for every certified EX false positive found by CaliberGraph (distinct pairs),
plus a reproducible random sample for manual validation of the labels.
Usage: python run_taxonomy.py --split test --file ../results/test/cgx_exc.jsonl --out ../results/test/taxonomy.json
"""
import argparse
import json
import os
import random
from collections import Counter

from cgx.certify import SchemaInfo
from cgx.sqlinfo import Analyzer
from score import is_cert
from taxonomy import label

ROOT = os.path.join(os.path.dirname(__file__), '..')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--split', default='test')
    ap.add_argument('--file', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--sample', type=int, default=100)
    a = ap.parse_args()
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    an = {db: Analyzer(SchemaInfo(s)) for db, s in ddl.items()}
    P = {json.loads(l)['pair_id']: json.loads(l) for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl'))}
    rows = [json.loads(l) for l in open(a.file)]
    labelled = []
    for r in rows:
        p = P[r['pair_id']]
        if p['split'] != a.split or p['ex'] != 'correct' or not is_cert(r, 'L1f', 'C_set', p):
            continue
        labs = label(an[p['db_id']], p['gold'], p['pred'], r['cert'])
        labelled.append(dict(pair_id=r['pair_id'], db_id=p['db_id'], labels=labs, gold=p['gold'], pred=p['pred'],
                             gold_rows=r['cert'].get('gold_rows'), pred_rows=r['cert'].get('pred_rows'),
                             witness=r['witness']))
    counts = Counter(l for x in labelled for l in x['labels'])
    rng = random.Random(7)
    sample = rng.sample(labelled, min(a.sample, len(labelled)))
    json.dump(dict(n=len(labelled), counts=dict(counts), n_labels_per_pair=Counter(len(x['labels']) for x in labelled),
                   items=labelled), open(a.out, 'w'), indent=0, default=str)
    json.dump(sample, open(a.out.replace('.json', '_sample.json'), 'w'), indent=1, default=str)
    print(len(labelled), dict(counts))


if __name__ == '__main__':
    main()
