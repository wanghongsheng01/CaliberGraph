"""S3-B (docs/en/17): build the 200-item cross-model sample: the 60 human-validation items plus 140 further
attributed items (70 per stage, calibration items excluded), seed 20261018; shuffled, blind (same item
fields as the original annotators received); split into batches for the annotator.
Usage: python src_s3/s3b_build.py"""
import json, os, random
ROOT = os.path.join(os.path.dirname(__file__), '..')
A = os.path.join(ROOT, 'results', 'audit')
O = os.path.join(ROOT, 'results', 'stage3', 's3b')
hv = json.load(open(os.path.join(A, 'human_validation', 'key_DO_NOT_OPEN_BEFORE_ANNOTATING.json')))
hvk = {(k['pair_id'], k['source']) for k in hv}
pool = {1: [], 2: []}
items = {}
for prefix, stage in (('test_v4', 1), ('test_r', 2)):
    key = {k['idx']: k for k in json.load(open(os.path.join(A, prefix + '_key.json')))}
    for b in json.load(open(os.path.join(A, prefix + '_blind.json'))):
        k = key[b['idx']]
        if k['source'].startswith('calib:'):
            continue
        items[(k['pair_id'], k['source'])] = (stage, b)
        if (k['pair_id'], k['source']) not in hvk:
            pool[stage].append((k['pair_id'], k['source']))
rng = random.Random(20261018)
extra = []
for st in (1, 2):
    extra += rng.sample(sorted(pool[st]), 70)
chosen = sorted(hvk) + extra
assert len(set(chosen)) == 200 and all(c in items for c in chosen)
rng.shuffle(chosen)
blind, key = [], []
for i, c in enumerate(chosen):
    st, b = items[c]
    x = {k: v for k, v in b.items() if k != 'idx'}
    x['idx'] = i
    blind.append(x)
    key.append(dict(idx=i, pair_id=c[0], source=c[1], stage=st, hv=c in hvk))
json.dump(key, open(os.path.join(O, 'key.json'), 'w'), indent=0)
for j in range(8):
    json.dump(blind[j * 25:(j + 1) * 25], open(os.path.join(O, f'batch{j}_blind.json'), 'w'))
print(len(blind), 'items in 8 batches')
