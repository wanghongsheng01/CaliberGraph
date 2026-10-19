"""Score method result files against the protocol (tiers x contracts) and SpotIt's released results.

Usage: python score.py --split dev results/dev_cgx_v1.jsonl [more.jsonl ...]
Results computed on distinct (qid, gold, pred) runs are expanded back to all (model, qid) pairs.
"""
import argparse
import json
import os
import re
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(__file__), '..')


def norm(s):
    return re.sub(r'\s+', ' ', s.strip().rstrip(';').strip())


def load_pairs(split):
    rows = [json.loads(l) for l in open(os.path.join(ROOT, 'data', 'pairs.jsonl'))]
    return [r for r in rows if r['split'] == split]


def expand(results, pairs):
    """Map each pair to the result of its (qid, gold, pred) representative."""
    by_id = {r['pair_id']: r for r in results}
    rep = {}
    for p in pairs:
        if p['pair_id'] in by_id:
            rep[(p['qid'], p['gold'].strip(), p['pred'].strip())] = by_id[p['pair_id']]
    out = {}
    for p in pairs:
        k = (p['qid'], p['gold'].strip(), p['pred'].strip())
        if k in rep:
            out[p['pair_id']] = rep[k]
    return out


_QCOLS = {}


def qcols(pair):
    """Lower-cased (table, column) pairs referenced by either query (cached)."""
    k = pair['pair_id']
    if k not in _QCOLS:
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        from cgx.certify import SchemaInfo
        from cgx.sqlinfo import Analyzer
        if not hasattr(qcols, 'an'):
            ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
            qcols.an = {db: Analyzer(SchemaInfo(s)) for db, s in ddl.items()}
        an = qcols.an[pair['db_id']]
        cols = an.analyze(pair['gold']).columns | an.analyze(pair['pred']).columns
        _QCOLS[k] = {(t.lower(), c.lower()) for t, c in cols}
    return _QCOLS[k]


_NN = {}


def observed_not_null(db):
    """(table, column) pairs that are never NULL in the official database, as mined by SpotIt+'s
    rule-based extractor (data-observed, not LLM-validated). Used by the post-hoc tier L1n."""
    if db not in _NN:
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        from cgx.certify import SchemaInfo, RealismConstraints
        ddl = json.load(open(os.path.join(ROOT, 'data', 'raw', 'bird_schema_ddl.json')))
        rb = json.load(open(os.path.join(ROOT, 'data', 'raw', 'spotit_constraints', 'rule_based', 'all_constraints.json')))
        mp = json.load(open(os.path.join(ROOT, 'data', 'raw', 'spotit', 'column_name_mapping.json')))['clean_to_orig']
        si = SchemaInfo(ddl[db])
        off = os.path.join(ROOT, 'data', 'official', 'nullability.json')
        if os.path.exists(off):  # observed directly in the official database
            nul = json.load(open(off)).get(db, {})
            _NN[db] = (si, {(t.lower(), c.lower()) for t, cols in nul.items() for c, v in cols.items()
                            if c != '_rows' and v == 0 and cols.get('_rows', 0) > 0})
            return _NN[db]
        rc = RealismConstraints({db: rb.get(db, [])}, mp.get(db, {}), si)
        _NN[db] = (si, {(t.lower(), c.lower()) for k, (t, c), _ in rc.items if k == 'not_null'})
    return _NN[db]


def nulls_ok(r, pair):
    si, nn = observed_not_null(pair['db_id'])
    cols = qcols(pair)
    for t, rows in (r.get('witness') or {}).items():
        tt = si.table(t)
        if tt is None:
            continue
        names = [c['name'].lower() for c in tt['columns']]
        for i, c in enumerate(names):
            if (tt['name'].lower(), c) in nn and (tt['name'].lower(), c) in cols and any(row[i] is None for row in rows):
                return False
    return True


def is_cert(r, tier='L1', contract='C_set', pair=None):
    if tier.startswith('O'):  # post-hoc: certification with official-database format profiles
        if not r or not r.get('cert_official'):
            return False
        r2 = dict(r)
        r2['cert'] = r['cert_official']
        return is_cert(r2, 'L' + tier[1:], contract, pair)
    c = r.get('cert') if r else None
    if not c:
        return False
    if not c.get('differ', {}).get(contract):
        return False
    if tier == 'L2':  # protocol amendment A1: realism on query-referenced columns (on top of L1f)
        if not c.get('L1f'):
            return False
        cols = qcols(pair)
        return not any((v[1].lower(), v[2].lower()) in cols for v in c.get('realism_violations', []))
    if tier == 'Rq':  # data-profile constraints on the columns referenced by either query only
        return is_cert(r, 'L1f', contract, pair) and bool((r.get('cert_R') or {}).get('okq'))
    if tier in ('R', 'R2'):  # second freeze: L1f (+ L2) + data-profile constraints of the official DB
        base = is_cert(r, 'L1f' if tier == 'R' else 'L2', contract, pair)
        return base and bool((r.get('cert_R') or {}).get('ok'))
    if tier == 'L1n':  # post-hoc (not pre-registered): L1f + no NULL where the official DB has none
        return bool(c.get('L1f')) and nulls_ok(r, pair)
    if tier == 'L2all':
        return bool(c.get('L2'))
    return bool(c.get(tier))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--split', default='dev')
    ap.add_argument('--subset', default='exc')
    ap.add_argument('files', nargs='+')
    a = ap.parse_args()
    pairs = load_pairs(a.split)
    pairs = [p for p in pairs if p['source'] != 'parseval_model']
    if a.subset == 'exc':
        pairs = [p for p in pairs if p['ex'] == 'correct']
    else:
        pairs = [p for p in pairs if p['ex'] == 'incorrect']
        ok = json.load(open(os.path.join(ROOT, 'data', 'exec_check.json')))
        pairs = [p for p in pairs if ok[p['pair_id']]['pred'] is True]
    print(f'population: {len(pairs)} pairs ({a.split}, {a.subset})')
    spot = sum(1 for p in pairs if p['spotit'] == 'incorrect')
    print(f'SpotIt (author-reported, validated+cross-checked): {spot}')
    for f in a.files:
        res = [json.loads(l) for l in open(f)]
        m = expand(res, pairs)
        cov = len(m)
        line = [os.path.basename(f), f'covered {cov}']
        for tier in ('L0', 'L1', 'L1f', 'L2', 'L2all'):
            for con in ('C_set', 'C_bag', 'C_lenient'):
                if tier == 'L2all' and con != 'C_set':
                    continue
                n = sum(1 for p in pairs if is_cert(m.get(p['pair_id']), tier, con, p))
                line.append(f'{tier}/{con}={n}')
        claims = sum(1 for p in pairs if m.get(p['pair_id'], {}).get('author_claim'))
        if claims:
            line.append(f'author_claims={claims}')
        found_uncert = sum(1 for p in pairs if m.get(p['pair_id'], {}).get('found') and not is_cert(m.get(p['pair_id']), 'L0', 'C_set'))
        line.append(f'claimed_but_not_L0={found_uncert}')
        print('  '.join(line))
        both = sum(1 for p in pairs if is_cert(m.get(p['pair_id'])) and p['spotit'] == 'incorrect')
        only_m = sum(1 for p in pairs if is_cert(m.get(p['pair_id'])) and p['spotit'] != 'incorrect')
        only_s = sum(1 for p in pairs if not is_cert(m.get(p['pair_id'])) and p['spotit'] == 'incorrect')
        print(f'   vs SpotIt @L1/C_set: both={both} only_method={only_m} only_spotit={only_s}')
        per = defaultdict(lambda: [0, 0, 0])
        for p in pairs:
            per[p['source']][0] += 1
            per[p['source']][1] += is_cert(m.get(p['pair_id']))
            per[p['source']][2] += p['spotit'] == 'incorrect'
        print('   per-model (n, method L1, spotit):', {k: tuple(v) for k, v in sorted(per.items())})


if __name__ == '__main__':
    main()
