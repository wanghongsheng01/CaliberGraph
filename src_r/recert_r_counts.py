"""Regenerate results/test/recert_r_counts.json: per first-freeze method, the number of EX-correct
(system, question) pairs whose stored witness is certified at tiers L0, L1f, Rq and R.

Definitions (identical to analyze_r.py / score.py):
  * population: test pairs with ex == 'correct' and source != 'parseval_model' (7,995 pairs);
  * results stored on distinct (qid, gold, pred) triples are expanded to every system with score.expand;
  * certified at tier T = score.is_cert(record, T, 'C_set', pair). Rq and R use the 'cert_R' field
    (okq / ok) that src_r/recertify_r.py added to the stored result files; L0 and L1f use 'cert'.
  * 'Fuzz' is the corrected fuzzing baseline (amendment P2, results/test/fuzz_exc_corrected.jsonl);
    SpotIt / SpotIt+ are the recertified released witnesses (results/test_spotit_vanilla_null.jsonl,
    results/test_spotit_llm.jsonl), counted by their stored witness, not by the authors' claim.

Usage (from src_r/):
    python recert_r_counts.py --out ../results/test/recert_r_counts.json
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score import load_pairs, expand, is_cert  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
TIERS = ('L0', 'L1f', 'Rq', 'R')


def default_files(split='test'):
    R = os.path.join(ROOT, 'results')
    D = os.path.join(R, split)
    return {
        'CaliberGraph': os.path.join(D, 'cgx_exc.jsonl'),
        'CaliberGraph+SC': os.path.join(D, 'cgx_sc_exc.jsonl'),
        'ParSEval-L1': os.path.join(D, 'parseval_l1_exc.jsonl'),
        'Fuzz': os.path.join(D, 'fuzz_exc_corrected.jsonl'),
        'SpotIt': os.path.join(R, f'{split}_spotit_vanilla_null.jsonl'),
        'SpotIt+': os.path.join(R, f'{split}_spotit_llm.jsonl'),
    }


def exc_pairs(split='test'):
    return [p for p in load_pairs(split) if p['source'] != 'parseval_model' and p['ex'] == 'correct']


def counts(files=None, split='test', tiers=TIERS):
    exc = exc_pairs(split)
    out = {}
    for name, path in (files or default_files(split)).items():
        m = expand([json.loads(l) for l in open(path)], exc)
        out[name] = {t: sum(1 for p in exc if is_cert(m.get(p['pair_id']), t, 'C_set', p)) for t in tiers}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--split', default='test')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    S = counts(split=a.split)
    json.dump(S, open(a.out, 'w'), indent=1)
    print(json.dumps(S))


if __name__ == '__main__':
    main()
