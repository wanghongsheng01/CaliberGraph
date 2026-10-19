"""Post-hoc correction P2 (docs/02a): replace the records of the frozen fuzzing baseline for pairs where it
returned a differing but non-L1f database by the certifier-in-the-loop rerun (same seed).
Usage: python merge_fuzzcert.py exc|exi
"""
import json
import os
import sys

sub = sys.argv[1]
D = os.path.join(os.path.dirname(__file__), '..', 'results', 'test')
orig = [json.loads(l) for l in open(os.path.join(D, f'fuzz_{sub}.jsonl'))]
re_ = {json.loads(l)['pair_id']: json.loads(l) for l in open(os.path.join(D, 'posthoc', f'fuzz_cert_rerun_{sub}.jsonl'))}
with open(os.path.join(D, f'fuzz_{sub}_corrected.jsonl'), 'w') as f:
    for r in orig:
        f.write(json.dumps(re_.get(r['pair_id'], r), default=str) + '\n')
print(sub, 'replaced', sum(1 for r in orig if r['pair_id'] in re_), 'of', len(orig))
