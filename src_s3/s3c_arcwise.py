"""Stage-3 S3-C: cross-check of our benchmark-issue list against the Arcwise-Plat corrections
of Jin et al. (docs/en/17_stage3_preregistration.md, section S3-C).

Inputs
  ext/s3/jin/data/arcwise_plat_sql_only_with_diff.json  (Arcwise-Plat-SQL, 498 BIRD dev questions)
  ext/s3/jin/data/arcwise_plat_full_with_diff.json      (Arcwise-Plat-full, same 498 questions)
  data/raw/bird_dev_20240627.json                       (BIRD dev gold used in the study)
  data/split.json                                       (question split; population O = 'test')
  results/audit/benchmark_issues_flags.json             (our 123 issue questions)
  data/official/dev_databases/<db>/<db>.sqlite          (official BIRD dev databases, read-only)

Definitions (as pre-registered)
  SQL corrected      : Arcwise-Plat-SQL query differs from the BIRD gold after whitespace+case
                       normalisation (collapse whitespace, lower-case, strip trailing ';') AND its
                       result differs from the gold result under set equality (30 s timeout per
                       query; a timeout or error of either query counts as "differs").
  Question corrected : in Arcwise-Plat-full, question or evidence differs from BIRD dev after
                       whitespace normalisation (collapse whitespace, strip; case-sensitive).
                       A missing (null) evidence is read as the empty string.
  Groups             : O = Arcwise questions in the test split; G / A = our gold_wrong / ambiguous
                       questions in O; N = O minus all 123 issue questions.
  H-C1               : Fisher exact (one-sided, 'greater'), SQL-corrected rate G > N.
  H-C2               : Fisher exact (one-sided, 'greater'), (question OR SQL)-corrected rate A > N.
p-values are unadjusted (Holm across the S3-F family is applied elsewhere).

Usage: python src_s3/s3c_arcwise.py  -> results/stage3/s3c_arcwise.json
"""
import json
import os
import re
import sqlite3
import time
from collections import Counter

from scipy.stats import fisher_exact

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EXT = os.path.abspath(os.path.join(ROOT, '..', 'ext', 's3', 'jin', 'data'))
F_SQL = os.path.join(EXT, 'arcwise_plat_sql_only_with_diff.json')
F_FULL = os.path.join(EXT, 'arcwise_plat_full_with_diff.json')
F_BIRD = os.path.join(ROOT, 'data', 'raw', 'bird_dev_20240627.json')
F_SPLIT = os.path.join(ROOT, 'data', 'split.json')
F_FLAGS = os.path.join(ROOT, 'results', 'audit', 'benchmark_issues_flags.json')
DB_ROOT = os.path.join(ROOT, 'data', 'official', 'dev_databases')
OUT = os.path.join(ROOT, 'results', 'stage3', 's3c_arcwise.json')
TIMEOUT_S = 30.0


def norm_sql(s):
    s = re.sub(r'\s+', ' ', s or '').strip().lower()
    while s.endswith(';'):
        s = s[:-1].rstrip()
    return s


def norm_text(s):
    return re.sub(r'\s+', ' ', s or '').strip()


_CON = {}


def run(db, sql):
    """Execute sql on the official dev database; returns (status, rows|message)."""
    if db not in _CON:
        _CON[db] = sqlite3.connect(f'file:{os.path.join(DB_ROOT, db, db + ".sqlite")}?mode=ro', uri=True)
    con = _CON[db]
    dl = time.monotonic() + TIMEOUT_S
    con.set_progress_handler(lambda: 1 if time.monotonic() > dl else 0, 10000)
    try:
        return 'ok', con.execute(sql).fetchall()
    except sqlite3.OperationalError as e:
        return ('timeout' if 'interrupted' in str(e) else 'error'), str(e)[:200]
    except Exception as e:  # noqa: BLE001
        return 'error', str(e)[:200]
    finally:
        con.set_progress_handler(None, 0)


def exec_diff(db, gold, arc):
    """True iff results differ under set equality (timeout/error of either query = differs)."""
    sg, rg = run(db, gold)
    sa, ra = run(db, arc)
    if sg != 'ok' and sa != 'ok':
        return True, f'gold_{sg}+arcwise_{sa}'
    if sg != 'ok':
        return True, f'gold_{sg}: {rg}'
    if sa != 'ok':
        return True, f'arcwise_{sa}: {ra}'
    return (set(rg) != set(ra)), ('result_differs' if set(rg) != set(ra) else 'result_equal')


def rate(k, n):
    return {'k': k, 'n': n, 'rate': (k / n if n else None)}


def fisher(k1, n1, k0, n0):
    table = [[k1, n1 - k1], [k0, n0 - k0]]
    odds, p = fisher_exact(table, alternative='greater')
    return {'table_[[grp_yes,grp_no],[N_yes,N_no]]': table, 'odds_ratio': odds, 'p_one_sided': p}


def main():
    arc_sql = json.load(open(F_SQL))
    arc_full = {r['question_id']: r for r in json.load(open(F_FULL))}
    bird = {int(r['question_id']): r for r in json.load(open(F_BIRD))}
    split = {int(k): v for k, v in json.load(open(F_SPLIT))['split'].items()}
    flags = json.load(open(F_FLAGS))
    kind = {int(f['question_id']): f['kind'] for f in flags}
    assert len(kind) == len(flags) == 123
    assert len(arc_sql) == len(arc_full) == 498

    records = []
    for r in sorted(arc_sql, key=lambda x: int(x['question_id'])):
        qid = int(r['question_id'])
        b, f = bird[qid], arc_full[r['question_id']]
        assert b['db_id'] == r['db_id'] == f['db_id'], qid
        sp = split.get(qid)
        in_o = sp == 'test'
        k = kind.get(qid)
        group = ({'gold_wrong': 'G', 'ambiguous': 'A'}[k] if k else 'N') if in_o else \
            ({'gold_wrong': 'G_outside_O', 'ambiguous': 'A_outside_O'}[k] if k else 'not_O')
        text_diff = norm_sql(r['SQL']) != norm_sql(b['SQL'])
        if text_diff:
            ed, note = exec_diff(r['db_id'], b['SQL'], r['SQL'])
        else:
            ed, note = False, 'text_identical'
        qd = norm_text(f['question']) != norm_text(b['question'])
        evd = norm_text(f['evidence']) != norm_text(b['evidence'])
        records.append({
            'question_id': qid, 'db_id': r['db_id'], 'split': sp, 'issue_kind': k, 'group': group,
            'sql_text_diff': text_diff, 'sql_exec_diff': ed, 'exec_note': note,
            'sql_corrected': text_diff and ed,
            'question_diff': qd, 'evidence_diff': evd, 'question_corrected': qd or evd,
            'full_sql_equals_sqlonly_sql': norm_sql(f['SQL']) == norm_sql(r['SQL']),
        })

    by = lambda g: [x for x in records if x['group'] == g]  # noqa: E731
    groups = ['G', 'A', 'N', 'G_outside_O', 'A_outside_O', 'not_O']

    def table(rs, sql_key):
        n = len(rs)
        s = sum(x[sql_key] for x in rs)
        q = sum(x['question_corrected'] for x in rs)
        e = sum(x[sql_key] or x['question_corrected'] for x in rs)
        both = sum(x[sql_key] and x['question_corrected'] for x in rs)
        return {'n': n, 'sql_corrected': s, 'question_corrected': q, 'both': both, 'either': e,
                'neither': n - e, 'rate_sql_corrected': s / n if n else None,
                'rate_either': e / n if n else None}

    conc = {g: table(by(g), 'sql_corrected') for g in groups}
    conc['O_all'] = table([x for x in records if x['split'] == 'test'], 'sql_corrected')
    conc['Arcwise_all'] = table(records, 'sql_corrected')
    conc_text = {g: table(by(g), 'sql_text_diff') for g in groups}
    conc_text['O_all'] = table([x for x in records if x['split'] == 'test'], 'sql_text_diff')
    conc_text['Arcwise_all'] = table(records, 'sql_text_diff')

    def hyp(sql_key):
        G, A, N = by('G'), by('A'), by('N')
        g = sum(x[sql_key] for x in G); n1 = sum(x[sql_key] for x in N)
        a = sum(x[sql_key] or x['question_corrected'] for x in A)
        n2 = sum(x[sql_key] or x['question_corrected'] for x in N)
        return {
            'H-C1': {'desc': 'SQL-corrected rate G > N', 'G': rate(g, len(G)), 'N': rate(n1, len(N)),
                     **fisher(g, len(G), n1, len(N))},
            'H-C2': {'desc': '(question OR SQL)-corrected rate A > N', 'A': rate(a, len(A)),
                     'N': rate(n2, len(N)), **fisher(a, len(A), n2, len(N))},
        }

    issue_in_arc = [x for x in records if x['issue_kind']]
    unchanged = {g: [x['question_id'] for x in by(g) if not (x['sql_corrected'] or x['question_corrected'])]
                 for g in ['G', 'A', 'G_outside_O', 'A_outside_O']}
    notes = Counter(x['exec_note'].split(':')[0] for x in records)

    out = {
        'spec': 'docs/en/17_stage3_preregistration.md S3-C',
        'inputs': {'arcwise_sql_only': os.path.relpath(F_SQL, ROOT), 'arcwise_full': os.path.relpath(F_FULL, ROOT),
                   'bird_dev': os.path.relpath(F_BIRD, ROOT), 'split': os.path.relpath(F_SPLIT, ROOT),
                   'issues': os.path.relpath(F_FLAGS, ROOT), 'timeout_s': TIMEOUT_S},
        'sizes': {
            'arcwise_questions': len(records),
            'O': sum(x['split'] == 'test' for x in records),
            'arcwise_by_split': dict(Counter(str(x['split']) for x in records)),
            'issues_total': len(kind), 'issues_in_arcwise': len(issue_in_arc),
            'issues_in_arcwise_by_kind': dict(Counter(x['issue_kind'] for x in issue_in_arc)),
            'issues_in_O': sum(x['group'] in ('G', 'A') for x in records),
            'G': len(by('G')), 'A': len(by('A')), 'N': len(by('N')),
            'G_outside_O': len(by('G_outside_O')), 'A_outside_O': len(by('A_outside_O')),
        },
        'confirmatory_unadjusted': hyp('sql_corrected'),
        'descriptive': {
            'concordance': conc,
            'issue_questions_unchanged_by_arcwise': {g: {'count': len(v), 'question_ids': v}
                                                    for g, v in unchanged.items()},
            'arcwise_corrections_among_N': {
                'sql_corrected': conc['N']['sql_corrected'], 'question_corrected': conc['N']['question_corrected'],
                'either': conc['N']['either'], 'n': conc['N']['n']},
            'exec_note_counts_all_arcwise': dict(notes),
            'full_vs_sqlonly_sql_differs_count': sum(not x['full_sql_equals_sqlonly_sql'] for x in records),
        },
        'secondary_descriptive_sql_text_diff_only': {
            'label': 'SECONDARY, descriptive only: SQL-corrected = text difference only, no execution check',
            'concordance': conc_text, 'tests_same_form_unadjusted': hyp('sql_text_diff'),
        },
        'records': records,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w'), indent=1)
    s, h = out['sizes'], out['confirmatory_unadjusted']
    print(json.dumps(s))
    for k in ('H-C1', 'H-C2'):
        print(k, {kk: vv for kk, vv in h[k].items() if kk != 'desc'})


if __name__ == '__main__':
    main()
