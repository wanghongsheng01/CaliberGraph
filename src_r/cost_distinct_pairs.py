"""Regenerate results/cost_and_distinct_pairs.json: per-method cost statistics on the 6,456 distinct
EX-correct test pairs (one stored record per distinct (qid, gold, pred) triple), plus the number of
SpotIt / SpotIt+ claims on EX-correct pairs whose released witness does not recertify.

Per method (one result file, counted over its records, NOT expanded to systems):
  distinct_pairs           number of records
  found                    records with found == True (method returned a differing database)
  certified_L1f            score.is_cert(r, 'L1f')   (C_set contract)
  found_not_certified_L1f  found - certified_L1f
  certified_R              score.is_cert(r, 'R'); key present only if the file carries 'cert_R'
                           (added by recertify_r.py, or computed in the loop for the -R methods)
  no_witness_in_budget     distinct_pairs - found - hard_timeout - identical_text - error
                           (ParSEval: verdicts NO_WITNESS, or EQ + UNKNOWN for the official tool)
  hard_timeout             verdict == 'TIMEOUT' (ParSEval only; key present only if > 0)
  identical_text           note == 'identical_text' (gold and pred textually identical, skipped)
  error                    verdict == 'ERROR' (key present only if > 0)
  mean_search_s            mean of search_s over all records, missing/None counted as 0
SpotIt / SpotIt+ (per (system, question) record of the released results, restricted to EX-correct pairs
of the test split, source != 'parseval_model'):
  claims_EXcorrect             author_claim is true
  claims_not_recertified_L0    claimed and not is_cert(r, 'L0')
  claims_not_recertified_L1f   claimed and not is_cert(r, 'L1f')

Usage (from src_r/):
    python cost_distinct_pairs.py --out ../results/cost_and_distinct_pairs.json
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score import load_pairs, is_cert  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')


def method_files():
    T, TR = os.path.join(ROOT, 'results', 'test'), os.path.join(ROOT, 'results', 'test_r')
    return {
        'CaliberGraph': os.path.join(T, 'cgx_exc.jsonl'),
        'CaliberGraph+SC': os.path.join(T, 'cgx_sc_exc.jsonl'),
        'ParSEval-L1': os.path.join(T, 'parseval_l1_exc.jsonl'),
        'ParSEval (official)': os.path.join(T, 'parseval_official_exc.jsonl'),
        'Random fuzzing (corrected)': os.path.join(T, 'fuzz_exc_corrected.jsonl'),
        'Random fuzzing (frozen, uncorrected)': os.path.join(T, 'fuzz_exc.jsonl'),
        'CaliberGraph-R': os.path.join(TR, 'cgx_r_exc.jsonl'),
        'Random fuzzing-R': os.path.join(TR, 'fuzz_r_exc.jsonl'),
    }


def spotit_files():
    R = os.path.join(ROOT, 'results')
    return {'SpotIt': os.path.join(R, 'test_spotit_vanilla_null.jsonl'),
            'SpotIt+': os.path.join(R, 'test_spotit_llm.jsonl')}


def cost(rows):
    n = len(rows)
    found = sum(1 for r in rows if r.get('found'))
    cert = sum(1 for r in rows if is_cert(r, 'L1f'))
    ident = sum(1 for r in rows if r.get('note') == 'identical_text')
    tout = sum(1 for r in rows if r.get('verdict') == 'TIMEOUT')
    err = sum(1 for r in rows if r.get('verdict') == 'ERROR')
    d = dict(distinct_pairs=n, found=found, certified_L1f=cert, found_not_certified_L1f=found - cert)
    if any('cert_R' in r for r in rows):
        d['certified_R'] = sum(1 for r in rows if is_cert(r, 'R'))
    d['no_witness_in_budget'] = n - found - tout - ident - err
    if tout:
        d['hard_timeout'] = tout
    d['identical_text'] = ident
    if err:
        d['error'] = err
    d['mean_search_s'] = sum((r.get('search_s') or 0.0) for r in rows) / n
    return d


def claims(rows, exc_ids):
    rr = [r for r in rows if r['pair_id'] in exc_ids and r.get('author_claim')]
    return dict(claims_EXcorrect=len(rr),
                claims_not_recertified_L0=sum(1 for r in rr if not is_cert(r, 'L0')),
                claims_not_recertified_L1f=sum(1 for r in rr if not is_cert(r, 'L1f')))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    S = {}
    for name, path in method_files().items():
        S[name] = cost([json.loads(l) for l in open(path)])
    exc_ids = {p['pair_id'] for p in load_pairs('test') if p['source'] != 'parseval_model' and p['ex'] == 'correct'}
    for name, path in spotit_files().items():
        S[name] = claims([json.loads(l) for l in open(path)], exc_ids)
    json.dump(S, open(a.out, 'w'), indent=1)
    print(json.dumps(S, indent=1))


if __name__ == '__main__':
    main()
