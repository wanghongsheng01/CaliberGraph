"""Reproduce the corrected fuzzing baseline of post-hoc amendment P2 (docs/02a, docs/en/02a) from the
stored outputs, writing to a separate directory (src/merge_fuzzcert.py does the same merge but writes
into results/test/ in place). Fuzzing itself is NOT re-run.

How the stored files were produced (results/queue_posthoc.sh, results/test/posthoc/queue.log):
  1. Selection: pairs whose frozen fuzz record (results/test/fuzz_{exc,exi}.jsonl) has found == True but
     is not certified at L1f (score.is_cert(r, 'L1f', 'C_set')); written to
     results/test/posthoc/fuzzcert_ids_{exc,exi}.json (132 exc, 259 exi pairs).
  2. Re-run of exactly these pairs with certifier-in-the-loop acceptance and the same seed:
     src_v5/run_method.py --method fuzz_cert --split test --subset S --dedup --ids ... --budget 5 --procs 2
     -> results/test/posthoc/fuzz_cert_rerun_{exc,exi}.jsonl.
  3. Merge: every record of the frozen file whose pair_id is in the re-run is replaced by the re-run
     record; all other records are kept unchanged and in the same order (src/merge_fuzzcert.py),
     serialised with json.dumps(r, default=str), one record per line.
  4. exc only: src_r/recertify_r.py was then applied to fuzz_exc_corrected.jsonl, adding the tier-R
     field 'cert_R' to the replaced records that carry a witness (113 of the 132; the kept records
     already had it from recertifying fuzz_exc.jsonl, and recomputation leaves it unchanged).
     fuzz_exi_corrected.jsonl was not recertified (no record of fuzz_exi*.jsonl has 'cert_R').
     The official-format field 'cert_official' was not recomputed: kept records retain it, re-run
     records do not have it.

This script performs steps 1 (checked against the stored id files), 3 and, with --recertify-r, 4.
Step 4 needs data/official/profile_R.json (and profile_FD.json) and the src_r/ code.

Usage (from src/):
    python repro_fuzz_corrected.py --out-dir OUT --recertify-r
    cmp OUT/fuzz_exc_corrected.jsonl ../results/test/fuzz_exc_corrected.jsonl
    cmp OUT/fuzz_exi_corrected.jsonl ../results/test/fuzz_exi_corrected.jsonl
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from score import load_pairs, is_cert  # noqa: E402

ROOT = os.path.join(HERE, '..')
D = os.path.join(ROOT, 'results', 'test')


def select_ids(sub):
    P = {p['pair_id']: p for p in load_pairs('test')}
    ids = []
    for l in open(os.path.join(D, f'fuzz_{sub}.jsonl')):
        r = json.loads(l)
        if r.get('found') and not is_cert(r, 'L1f', 'C_set', P[r['pair_id']]):
            ids.append(r['pair_id'])
    return ids


def merge(sub, out_path):
    orig = [json.loads(l) for l in open(os.path.join(D, f'fuzz_{sub}.jsonl'))]
    re_ = {json.loads(l)['pair_id']: json.loads(l) for l in open(os.path.join(D, 'posthoc', f'fuzz_cert_rerun_{sub}.jsonl'))}
    with open(out_path, 'w') as f:
        for r in orig:
            f.write(json.dumps(re_.get(r['pair_id'], r), default=str) + '\n')
    return sum(1 for r in orig if r['pair_id'] in re_), len(orig), len(re_)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--recertify-r', action='store_true', help='apply src_r/recertify_r.py to the merged exc file')
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    for sub in ('exc', 'exi'):
        ids = select_ids(sub)
        stored = json.load(open(os.path.join(D, 'posthoc', f'fuzzcert_ids_{sub}.json')))['pair_ids']
        print(sub, 'selected', len(ids), 'matches stored id file:', ids == stored)
        out = os.path.join(a.out_dir, f'fuzz_{sub}_corrected.jsonl')
        k, n, m = merge(sub, out)
        print(sub, 'replaced', k, 'of', n, f'(re-run records: {m})', '->', out)
    if a.recertify_r:
        subprocess.run([sys.executable, os.path.join(ROOT, 'src_r', 'recertify_r.py'),
                        os.path.join(a.out_dir, 'fuzz_exc_corrected.jsonl')], check=True, cwd=os.path.join(ROOT, 'src_r'))


if __name__ == '__main__':
    main()
