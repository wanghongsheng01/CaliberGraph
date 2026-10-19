"""Draw the residual-audit sample: EX-correct test pairs (distinct predictions, not byte-identical to
the gold query) for which NO method produced a certified witness at tier L1f and SpotIt reported
no non-equivalence. Stratified by system (10 per system), seed fixed.
Usage: python residual_sample.py --out ../results/test/residual_sample.json
"""
import argparse
import json
import os
import random
import re

from score import load_pairs, expand, is_cert

ROOT = os.path.join(os.path.dirname(__file__), '..')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--per_system', type=int, default=10)
    a = ap.parse_args()
    pairs = [p for p in load_pairs('test') if p['source'] != 'parseval_model' and p['ex'] == 'correct']
    D = os.path.join(ROOT, 'results', 'test')
    files = ['cgx_exc.jsonl', 'parseval_l1_exc.jsonl', 'fuzz_exc.jsonl', 'cgx_sc_exc.jsonl', 'parseval_official_exc.jsonl']
    maps = []
    for f in files:
        p = os.path.join(D, f)
        if os.path.exists(p):
            maps.append(expand([json.loads(l) for l in open(p)], pairs))
    spot = expand([json.loads(l) for l in open(os.path.join(ROOT, 'results', 'test_spotit_llm.jsonl'))], pairs)
    norm = lambda s: re.sub(r'\s+', ' ', s.strip().rstrip(';').strip())  # noqa: E731
    residual, seen = [], set()
    for p in pairs:
        if norm(p['gold']) == norm(p['pred']):
            continue
        if any(is_cert(m.get(p['pair_id']), 'L0', 'C_set', p) for m in maps):
            continue
        if p['spotit'] == 'incorrect' or (spot.get(p['pair_id']) or {}).get('author_claim'):
            continue
        k = (p['qid'], p['gold'].strip(), p['pred'].strip())
        if k in seen:
            continue
        seen.add(k)
        residual.append(p)
    rng = random.Random(20261014)
    sample = []
    for src in sorted({p['source'] for p in residual}):
        cand = [p for p in residual if p['source'] == src]
        sample += rng.sample(cand, min(a.per_system, len(cand)))
    json.dump(dict(n_residual_distinct=len(residual), n_sample=len(sample),
                   items=[dict(pair_id=p['pair_id'], db_id=p['db_id'], gold=p['gold'], pred=p['pred']) for p in sample]),
              open(a.out, 'w'), indent=1)
    print('residual distinct', len(residual), 'sample', len(sample))


if __name__ == '__main__':
    main()
