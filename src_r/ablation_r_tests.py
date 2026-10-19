"""Exact McNemar tests for the second-freeze ablation (each configuration vs the full CaliberGraph-R
at tier R on the random test subsample of distinct pairs). Writes summary_r['ablation_R_tests'].
This script replaces the inline snippet with which these values were first computed; it reproduces
them exactly (checked on 2026-10-16).

Usage: python ablation_r_tests.py --summary ../results/test_r/summary_r.json --ids ../data/test_subsample.json \
          --full ../results/test_r/cgx_r_exc.jsonl \
          "--abl=-real sub-databases=../results/test_r/abl_cgx_r_noreal.jsonl" ... [--check]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from score import load_pairs, is_cert  # noqa: E402
from stats_eval import mcnemar_exact  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--summary', required=True)
    ap.add_argument('--ids', required=True)
    ap.add_argument('--full', required=True)
    ap.add_argument('--abl', action='append', default=[])
    ap.add_argument('--split', default='test')
    ap.add_argument('--check', action='store_true', help='compare with the stored values instead of writing')
    a = ap.parse_args()
    P = {p['pair_id']: p for p in load_pairs(a.split) if p['source'] != 'parseval_model'}
    sub = [k for k in json.load(open(a.ids))['pair_ids'] if k in P]

    def outcome(path):
        byid = {json.loads(l)['pair_id']: json.loads(l) for l in open(path)}
        return {k: bool(is_cert(byid.get(k), 'R', 'C_set', P[k])) for k in sub}
    full = outcome(a.full)
    res = {}
    for spec in a.abl:
        name, path = spec.split('=', 1)
        o = outcome(path)
        b = sum(1 for k in sub if full[k] and not o[k])
        c = sum(1 for k in sub if o[k] and not full[k])
        res[name] = dict(full_only=b, abl_only=c, p=mcnemar_exact(b, c))
    S = json.load(open(a.summary))
    if a.check:
        old = S.get('ablation_R_tests', {})
        for k, v in res.items():
            same = old.get(k, {}).get('full_only') == v['full_only'] and old.get(k, {}).get('abl_only') == v['abl_only'] \
                and abs(old.get(k, {}).get('p', -1) - v['p']) < 1e-12
            print(k, v, 'identical' if same else f'DIFFERS from stored {old.get(k)}')
        return
    S['ablation_R_tests'] = res
    json.dump(S, open(a.summary, 'w'), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
