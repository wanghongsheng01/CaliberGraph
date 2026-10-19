"""Build the unified CGX benchmark table.

Inputs (data/raw): BIRD dev 2024-06-27 gold (from SpotIt+ repo), BIRD DDL (ParSEval artifact),
10 SpotIt+ prediction files, their EX results on official BIRD databases, SpotIt validated
results, and the ParSEval artifact (11th prediction source, previously exposed).

Outputs (data/): pairs.jsonl (one row per question x source), split.json.
The split is deterministic and pre-registered: see docs/02 protocol.
"""
import hashlib, json, os, glob, csv, re
from collections import Counter, defaultdict

RAW = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
OUT = os.path.join(os.path.dirname(__file__), '..', 'data')

EXPOSED = """california_schools__21 california_schools__26 california_schools__31 california_schools__35 california_schools__45 card_games__341 card_games__372 card_games__389 codebase_community__632 codebase_community__677 codebase_community__704 debit_card_specializing__1479 debit_card_specializing__1490 debit_card_specializing__1503 debit_card_specializing__1526 debit_card_specializing__1532 european_football_2__1069 european_football_2__1073 european_football_2__1099 european_football_2__1111 financial__124 financial__153 financial__169 formula_1__866 formula_1__893 formula_1__981 student_club__1372 student_club__1381 student_club__1390 student_club__1435 superhero__750 superhero__765 superhero__777 superhero__834 thrombosis_prediction__1161 thrombosis_prediction__1172 thrombosis_prediction__1261 thrombosis_prediction__1300 thrombosis_prediction__1306 toxicology__220 toxicology__223 toxicology__319 toxicology__335""".split()
EXPOSED_QIDS = {int(x.split('__')[1]) for x in EXPOSED}

SALT_SCHEMA = 'cgx-holdout-schema-v1'
SALT_Q = 'cgx-question-split-v1'
N_HOLDOUT_SCHEMAS = 3
DEV_FRACTION = 0.30


def clean_pred(s):
    """Strip the BIRD submission suffix, as the official BIRD evaluator does."""
    return s.split('\t----- bird -----\t')[0].strip()


def h(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def main():
    dev = json.load(open(os.path.join(RAW, 'bird_dev_20240627.json')))
    assert len(dev) == 1534
    schemas = sorted({d['db_id'] for d in dev})
    holdout = sorted(schemas, key=lambda s: h(f'{SALT_SCHEMA}|{s}'))[:N_HOLDOUT_SCHEMAS]

    # question-level split
    split = {}
    by_stratum = defaultdict(list)
    for d in dev:
        q = d['question_id']
        if d['db_id'] in holdout:
            split[q] = 'excluded_exposed' if q in EXPOSED_QIDS else 'test'
        elif q in EXPOSED_QIDS:
            split[q] = 'dev'
        else:
            by_stratum[(d['db_id'], d['difficulty'])].append(q)
    for key, qs in sorted(by_stratum.items()):
        qs = sorted(qs, key=lambda q: h(f'{SALT_Q}|{key[0]}|{q}'))
        n_dev = round(DEV_FRACTION * len(qs))
        for i, q in enumerate(qs):
            split[q] = 'dev' if i < n_dev else 'test'

    # prediction sources
    rows = []
    gold = {d['question_id']: d for d in dev}
    sources = sorted(os.path.basename(f).replace('_sql.json', '') for f in glob.glob(os.path.join(RAW, 'predictions', '*.json')))
    for src in sources:
        preds = json.load(open(os.path.join(RAW, 'predictions', f'{src}_sql.json')))
        ex = {int(r['question_id']): r['res'] for r in csv.DictReader(open(os.path.join(RAW, 'ex', f'{src}_sql.json_EX.csv')))}
        sp = {int(r['question_id']): r for r in csv.DictReader(open(os.path.join(RAW, 'spotit', f'{src}_sql.json.csv')))}
        for q, g in gold.items():
            s = sp.get(q, {})
            rows.append(dict(
                pair_id=f'{src}:{q}', qid=q, source=src, db_id=g['db_id'], difficulty=g['difficulty'],
                split=split[q], gold=g['SQL'], pred=clean_pred(preds.get(str(q), '')),
                ex=ex.get(q), spotit=s.get('verieql_res'), spotit_bound=s.get('bound_size'),
                spotit_runtime=s.get('runtime'), spotit_ce=s.get('counterexample_path'),
                spotit_out_pred=s.get('output1'), spotit_out_gold=s.get('output2')))
    # ParSEval artifact: older BIRD gold version; dev questions only (previously exposed material)
    for l in open(os.path.join(RAW, 'parseval_disprove_bird.jsonl')):
        r = json.loads(l)
        q = int(r['index'])
        if split[q] != 'dev':
            continue
        rows.append(dict(pair_id=f'parseval_model:{q}', qid=q, source='parseval_model', db_id=r['dbid'],
                         difficulty=r['difficulty'], split='dev', gold=r['gold'], pred=r['predicted'],
                         ex=None, spotit=None, parseval_official=r['verdict'], parseval_reason=r['reason']))
    with open(os.path.join(OUT, 'pairs.jsonl'), 'w') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    meta = dict(holdout_schemas=holdout, salt_schema=SALT_SCHEMA, salt_question=SALT_Q, dev_fraction=DEV_FRACTION,
                exposed_qids=sorted(EXPOSED_QIDS), split_counts=Counter(split.values()),
                split={str(k): v for k, v in sorted(split.items())})
    json.dump(meta, open(os.path.join(OUT, 'split.json'), 'w'), indent=1)
    print('holdout schemas', holdout)
    print('question split', Counter(split.values()))
    print('pairs by source/split', Counter((r['source'], r['split']) for r in rows).most_common(30))


if __name__ == '__main__':
    main()
