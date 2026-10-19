"""Stage 3, S3-D (docs/en/17): build a Spider data root for the frozen code.

Creates <out>/ with:
  src/, src_r/            byte-for-byte copies of the frozen first- and second-freeze code
  data/raw/bird_schema_ddl.json            DDL per database, from sqlite_master (same format as for BIRD)
  data/raw/spotit/column_name_mapping.json, data/raw/spotit_constraints/rule_based/all_constraints.json
                                           empty stand-ins (no SpotIt material exists for Spider)
  data/official/dev_databases/<db>/<db>.sqlite   symlinks to the Spider databases
  data/pairs.jsonl        question x system pairs, all with split 'test'
  data/ex_spider.json     EX labels (set equality, 30 s timeout; errors/timeouts incorrect)

Modes:
  --mode dev    Spider dev (1,034 questions, 20 databases), six public prediction sets
  --mode smoke  30 synthetic pairs on Spider *train* databases (gold vs. a mechanical mutation),
                used only to check that the pipeline runs (rule S3-0.3)

Usage: python src_s3/spider_build.py --spider /home/claude/ext/spider_full/spider --out spider [--mode dev]
"""
import argparse
import csv
import hashlib
import json
import multiprocessing as mp
import os
import random
import re
import shutil
import sqlite3
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROBE = '/home/claude/ext/probe'
SOURCES = {  # name -> (file, kind); all six aligned with dev.json by position
    'dailsql_gpt4': (f'{PROBE}/DAIL-SQL/results/DAIL-SQL+GPT-4.txt', 'txt'),
    'dailsql_gpt4_sc': (f'{PROBE}/DAIL-SQL/results/DAIL-SQL+GPT-4+self-consistency.txt', 'txt'),
    'graphix_t5': (f'{PROBE}/DAIL-SQL/results/graphix_result.txt', 'txt'),
    'dinsql_gpt4': (f'{PROBE}/Few-shot-NL2SQL-with-prompting/GPT4_results/DIN-SQL.csv', 'csv'),
    'gpt4_fewshot': (f'{PROBE}/Few-shot-NL2SQL-with-prompting/GPT4_results/GPT4_few_shot.csv', 'csv'),
    'gpt4_zeroshot': (f'{PROBE}/Few-shot-NL2SQL-with-prompting/GPT4_results/GPT4_zero_shot.csv', 'csv'),
}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def ddl_of(path):
    con = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    out = [r[0] for r in con.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND sql IS NOT NULL ORDER BY rowid")]
    con.close()
    return out


def fix_utf8(path):
    """Re-decode TEXT cells that are not valid UTF-8 (errors='replace'); the frozen miners read text as UTF-8."""
    con = sqlite3.connect(path)
    con.text_factory = bytes
    n = 0
    for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall():
        t = t.decode()
        for c in [r[1].decode() for r in con.execute(f'PRAGMA table_info("{t}")').fetchall()]:
            rows = con.execute(f'SELECT rowid, "{c}" FROM "{t}" WHERE typeof("{c}") = \'text\'').fetchall()
            for rid, v in rows:
                try:
                    v.decode('utf-8')
                except UnicodeDecodeError:
                    con.execute(f'UPDATE "{t}" SET "{c}" = ? WHERE rowid = ?', (v.decode('utf-8', 'replace'), rid))
                    n += 1
    con.commit()
    con.close()
    return n


def load_preds(dev):
    preds = {}
    for name, (path, kind) in SOURCES.items():
        if kind == 'txt':
            lines = [l.rstrip('\n') for l in open(path, encoding='utf-8')]
            lines = [l for l in lines if l.strip() != ''] if len(lines) != len(dev) else lines
            assert len(lines) == len(dev), (name, len(lines))
            preds[name] = [l.split('\t')[0].strip() for l in lines]
        else:
            rows = list(csv.DictReader(open(path, encoding='utf-8')))
            assert len(rows) == len(dev), (name, len(rows))
            for r, d in zip(rows, dev):
                assert r['NLQ'].strip() == d['question'].strip() and r['DATABASE'] == d['db_id'], name
            preds[name] = [r['PREDICTED SQL'].strip() for r in rows]
    return preds


_DB = {}


def _run(sql, con, timeout):
    dl = time.monotonic() + timeout
    con.set_progress_handler(lambda: 1 if time.monotonic() > dl else 0, 10000)
    try:
        return 'ok', con.execute(sql).fetchall()
    except sqlite3.OperationalError as e:
        return ('timeout' if 'interrupted' in str(e) else 'error'), str(e)[:200]
    except Exception as e:  # noqa: BLE001
        return 'error', f'{type(e).__name__}: {e}'[:200]
    finally:
        con.set_progress_handler(None, 0)


def ex_one(args):
    dbdir, row, timeout = args
    db = row['db_id']
    if db not in _DB:
        con = sqlite3.connect(f"file:{os.path.join(dbdir, db, db + '.sqlite')}?mode=ro", uri=True)
        con.text_factory = lambda b: b.decode('utf-8', 'replace')
        _DB[db] = con
    con = _DB[db]
    sg, g = _run(row['gold'], con, timeout)
    sp, p = _run(row['pred'], con, timeout)
    if sg != 'ok':
        lab = 'gold_' + sg
    elif sp != 'ok':
        lab = sp
    else:
        lab = 'correct' if set(g) == set(p) else 'incorrect'
    return row['pair_id'], lab


MUT = [(r'\bDISTINCT\s+', ''), (r'>=', '>'), (r'(?<![<>!])>(?!=)', '>='), (r'\s+LIMIT\s+1\b', '')]


def smoke_pairs(spider, rng):
    train = json.load(open(os.path.join(spider, 'train_spider.json')))
    dbs = sorted({d['db_id'] for d in train})
    rng.shuffle(dbs)
    dbs = sorted(dbs[:6])
    out = []
    for d in train:
        if d['db_id'] not in dbs:
            continue
        for pat, rep in MUT:
            m = re.sub(pat, rep, d['query'], count=1, flags=re.I)
            if m != d['query']:
                out.append((d, m))
                break
    rng.shuffle(out)
    return dbs, out[:30]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spider', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--mode', default='dev', choices=['dev', 'smoke'])
    ap.add_argument('--procs', type=int, default=3)
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    for d in ('src', 'src_r'):
        dst = os.path.join(out, d)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(ROOT, d), dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'parseval_env'))
    data = os.path.join(out, 'data')
    for d in ('raw/spotit', 'raw/spotit_constraints/rule_based', 'official/dev_databases'):
        os.makedirs(os.path.join(data, d), exist_ok=True)
    json.dump({'clean_to_orig': {}}, open(os.path.join(data, 'raw/spotit/column_name_mapping.json'), 'w'))
    json.dump({}, open(os.path.join(data, 'raw/spotit_constraints/rule_based/all_constraints.json'), 'w'))
    rng = random.Random(20261018)
    if a.mode == 'dev':
        dev = json.load(open(os.path.join(a.spider, 'dev.json')))
        dbs = sorted({d['db_id'] for d in dev})
        preds = load_preds(dev)
        rows = []
        for name in SOURCES:
            for i, d in enumerate(dev):
                rows.append(dict(pair_id=f'{name}:{i}', qid=i, source=name, db_id=d['db_id'], difficulty=None,
                                 split='test', gold=d['query'].strip(), pred=preds[name][i], spotit=None))
    else:
        dbs, sp = smoke_pairs(a.spider, rng)
        rows = [dict(pair_id=f'smoke:{i}', qid=i, source='smoke', db_id=d['db_id'], difficulty=None, split='test',
                     gold=d['query'].strip(), pred=m.strip(), spotit=None) for i, (d, m) in enumerate(sp)]
    dbdir = os.path.join(data, 'official', 'dev_databases')
    fixed = {}
    for db in dbs:  # amendment E7: real copies; invalid UTF-8 text cells re-decoded with errors='replace'
        dst = os.path.join(dbdir, db)
        if os.path.islink(dst):
            os.unlink(dst)
        os.makedirs(dst, exist_ok=True)
        shutil.copyfile(os.path.join(os.path.abspath(a.spider), 'database', db, db + '.sqlite'), os.path.join(dst, db + '.sqlite'))
        fixed[db] = fix_utf8(os.path.join(dst, db + '.sqlite'))
    ddl = {db: ddl_of(os.path.join(dbdir, db, db + '.sqlite')) for db in dbs}
    json.dump(ddl, open(os.path.join(data, 'raw', 'bird_schema_ddl.json'), 'w'), indent=0)
    with mp.Pool(a.procs) as pool:
        ex = dict(pool.map(ex_one, [(dbdir, r, 30.0) for r in rows], chunksize=16))
    for r in rows:
        r['ex'] = ex[r['pair_id']]
    with open(os.path.join(data, 'pairs.jsonl'), 'w') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')
    json.dump(ex, open(os.path.join(data, 'ex_spider.json'), 'w'))
    manifest = dict(mode=a.mode, n_pairs=len(rows), databases=dbs, utf8_cells_fixed=fixed,
                    sources={k: dict(file=v[0], sha256=sha(v[0])) for k, v in SOURCES.items()} if a.mode == 'dev' else None,
                    dev_json_sha256=sha(os.path.join(a.spider, 'dev.json')))
    json.dump(manifest, open(os.path.join(data, 'manifest.json'), 'w'), indent=1)
    from collections import Counter
    print(a.mode, len(rows), 'pairs;', Counter(ex.values()) if a.mode == 'smoke' else '(EX labels written, not printed)')


if __name__ == '__main__':
    main()
