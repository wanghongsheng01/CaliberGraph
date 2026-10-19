"""Stage 3, S3-E (docs/en/17): extra BIRD systems from the BIRD Mini-Dev prediction sets.

1. Map each Mini-Dev index to a BIRD question_id by its position in the Arcwise-Plat list (route ii of S3-E)
   and validate the mapping:
     (a) the db_id carried by the prediction equals the db_id of the mapped question (>= 99% of indices);
     (b) among indices whose prediction executes, >= 95% reference only tables of the mapped question's database
         and share at least one table with the BIRD gold.
   Supplementary diagnostic (amendment E6): string-literal overlap with the BIRD gold at offsets 0, +-1, +-2.
2. Build <out>/ with byte-for-byte copies of src_r/ (and src/), symlinks to the BIRD data the frozen code reads,
   and data/pairs.jsonl holding only NEW distinct (question, normalised prediction) representatives of questions
   in the held-out test split (representatives already present in data/pairs.jsonl of the main study are dropped).
3. EX on the official BIRD dev databases (set equality, 30 s timeout).

Usage: python src_s3/minidev_build.py --out minidev
"""
import argparse
import glob
import json
import multiprocessing as mp
import os
import re
import shutil
import sqlite3
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'src_r'))
from cgx.certify import SchemaInfo  # noqa: E402
from cgx.sqlinfo import Analyzer  # noqa: E402
sys.path.insert(0, os.path.dirname(__file__))
from spider_build import ex_one, sha  # noqa: E402

MD = '/home/claude/ext/probe/mini_dev/llm/exp_result'
ARC = '/home/claude/ext/s3/jin/data/arcwise_plat_sql_only_with_diff.json'
DBDIR = os.path.join(ROOT, 'data', 'official', 'dev_databases')


def norm(s):
    return re.sub(r'\s+', ' ', s.strip().rstrip(';').strip())


def lits(sql):
    return {m.lower() for m in re.findall(r"'([^']{2,})'", sql)} | set(re.findall(r'\b\d{3,}\b', sql))


def sysname(path):
    b = os.path.basename(path).replace('predict_mini_dev_', '').replace('.json', '')
    return ('ta_' if 'TA_output' in path else 'kg_') + re.sub(r'_(sqlite|SQLite)$', '', b)


def tables_of(an, sql):
    try:
        return {t.lower() for t in an.analyze(sql).tables}
    except Exception:  # noqa: BLE001
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--procs', type=int, default=2)
    a = ap.parse_args()
    arc = json.load(open(ARC))
    dev = {d['question_id']: d for d in json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_dev_20240627.json')))}
    split = json.load(open(os.path.join(ROOT, 'data', 'split.json')))
    split = split.get('split', split)
    split = {int(k): v for k, v in split.items()}
    ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
    an = {db: Analyzer(SchemaInfo(s)) for db, s in ddl.items()}
    files = sorted(glob.glob(f'{MD}/TA_output/*SQLite.json') + glob.glob(f'{MD}/sql_output_kg/*_sqlite.json'))
    qmap = [int(x['question_id']) for x in arc]  # position -> BIRD question_id
    report = dict(files={sysname(f): dict(file=f, sha256=sha(f)) for f in files}, arcwise_sha256=sha(ARC), systems={})
    preds = {}
    for f in files:
        p = json.load(open(f))
        name = sysname(f)
        recs = []
        for i in range(len(p)):
            sql, _, db = p[str(i)].partition('\t----- bird -----\t')
            recs.append((sql.strip(), db.strip()))
        preds[name] = recs
        n = min(len(recs), len(qmap))
        a_ok = sum(recs[i][1] == dev[qmap[i]]['db_id'] for i in range(n))
        b_n = b_ok = 0
        for i in range(n):
            db = dev[qmap[i]]['db_id']
            if recs[i][1] != db:
                continue
            con = sqlite3.connect(f"file:{os.path.join(DBDIR, db, db + '.sqlite')}?mode=ro", uri=True)
            try:
                con.execute('EXPLAIN ' + recs[i][0])
            except Exception:  # noqa: BLE001
                continue
            finally:
                con.close()
            tp, tg = tables_of(an[db], recs[i][0]), tables_of(an[db], dev[qmap[i]]['SQL'])
            if tp is None or tg is None:
                continue
            b_n += 1
            allt = {t.lower() for t in SchemaInfo(ddl[db]).tables}
            b_ok += tp <= allt and bool(tp & tg)
        diag = {}
        for off in (-2, -1, 0, 1, 2):
            hit = tot = 0
            for i in range(n):
                j = i + off
                if not 0 <= j < len(qmap):
                    continue
                lp = lits(recs[i][0])
                if not lp:
                    continue
                tot += 1
                hit += bool(lp & lits(dev[qmap[j]]['SQL'] + ' ' + dev[qmap[j]]['evidence'] + ' ' + dev[qmap[j]]['question']))
            diag[off] = round(hit / tot, 3) if tot else None
        report['systems'][name] = dict(n_pred=len(recs), n_mapped=n, a_db_match=a_ok / n, b_checked=b_n,
                                       b_ok=b_ok / b_n if b_n else None, literal_overlap_by_offset=diag)
    valid = all(s['a_db_match'] >= 0.99 and (s['b_ok'] or 0) >= 0.95 for s in report['systems'].values())
    report['mapping_valid'] = valid
    out = os.path.abspath(a.out)
    os.makedirs(os.path.join(out, 'data'), exist_ok=True)
    json.dump(report, open(os.path.join(out, 'data', 'mapping_report.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != 'files'}, indent=1))
    if not valid:
        print('MAPPING NOT VALID: S3-E is not run (pre-registered rule)')
        return
    # data root
    for d in ('src', 'src_r'):
        dst = os.path.join(out, d)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(ROOT, d), dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    for rel in ('raw', 'official', 'format_profiles.json', 'split.json'):
        link = os.path.join(out, 'data', rel)
        if not os.path.lexists(link):
            os.symlink(os.path.join(ROOT, 'data', rel), link)
    seen = {(r['qid'], norm(r['pred'])) for r in map(json.loads, open(os.path.join(ROOT, 'data', 'pairs.jsonl')))}
    rows, dropped = [], Counter()
    for name, recs in preds.items():
        for i, (sql, db) in enumerate(recs[:len(qmap)]):
            q = qmap[i]
            if split.get(q) != 'test':
                dropped['not_test'] += 1
                continue
            if db != dev[q]['db_id']:
                dropped['db_mismatch'] += 1
                continue
            k = (q, norm(sql))
            if k in seen:
                dropped['already_in_study_or_duplicate'] += 1
                continue
            seen.add(k)
            rows.append(dict(pair_id=f'md_{name}:{q}', qid=q, source=f'md_{name}', db_id=db,
                             difficulty=dev[q].get('difficulty'), split='test', gold=dev[q]['SQL'], pred=sql, spotit=None))
    with mp.Pool(a.procs) as pool:
        ex = dict(pool.map(ex_one, [(DBDIR, r, 30.0) for r in rows], chunksize=8))
    for r in rows:
        r['ex'] = ex[r['pair_id']]
    with open(os.path.join(out, 'data', 'pairs.jsonl'), 'w') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')
    json.dump(dict(n_pairs=len(rows), dropped=dict(dropped)), open(os.path.join(out, 'data', 'manifest.json'), 'w'), indent=1)
    print(len(rows), 'new pairs;', dict(dropped), '(EX labels written, not printed)')


if __name__ == '__main__':
    main()
