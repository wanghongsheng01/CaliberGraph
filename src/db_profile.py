"""Build per-column format profiles from the official BIRD development databases.

For every TEXT-affinity column: the set of lexical shapes of its non-NULL values (see
cgx.certify.shape), their frequencies, and the most frequent values. A column with more than
MAX_SHAPES distinct shapes is marked free text (no shape constraint). Output:
data/format_profiles.json  {db: {table: {column: {...}}}}

Usage: python db_profile.py /path/to/dev_databases
"""
import json
import os
import sqlite3
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from cgx.certify import shape, affinity  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')
MAX_SHAPES = 50
COVER = 0.999   # keep the most frequent shapes covering 99.9% of non-NULL values


def profile_db(path):
    con = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    out = {}
    for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
        cols = con.execute(f'PRAGMA table_info("{t}")').fetchall()
        out[t] = {}
        for _, c, decl, *_ in cols:
            if affinity(decl) != 'TEXT':
                continue
            vals = Counter()
            n = 0
            for (v,) in con.execute(f'SELECT "{c}" FROM "{t}" WHERE "{c}" IS NOT NULL'):
                vals[v] += 1
                n += 1
            shapes = Counter()
            for v, k in vals.items():
                shapes[shape(v)] += k
            free = len(shapes) > MAX_SHAPES
            keep, acc = [], 0
            for s, k in shapes.most_common():
                if acc >= COVER * n:
                    break
                keep.append(s)
                acc += k
            out[t][c] = dict(n_nonnull=n, n_distinct=len(vals), n_shapes=len(shapes), free_text=free,
                             shapes=[] if free else keep,
                             samples=[v if isinstance(v, str) else str(v) for v, _ in vals.most_common(20)])
    con.close()
    return out


def main(root):
    prof = {}
    for db in sorted(os.listdir(root)):
        p = os.path.join(root, db, f'{db}.sqlite')
        if os.path.exists(p):
            prof[db] = profile_db(p)
            print(db, sum(len(v) for v in prof[db].values()), 'text columns')
    json.dump(prof, open(os.path.join(ROOT, 'data', 'official', 'format_profiles.json'), 'w'), ensure_ascii=False, indent=0)


if __name__ == '__main__':
    main(sys.argv[1])
