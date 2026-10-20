"""Paper figures from results/<split>/summary.json (+ taxonomy json). Static PDF, palette slots 1-3.
Usage: python make_figures.py --summary ../results/test/summary.json --taxonomy ../results/test/taxonomy.json --out ../paper/figs
"""
import argparse
import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'
COLUMN = False  # --column: sizes for one column of a two-column (IEEE) page
INK, INK2, GRID = '#0b0b0b', '#52514e', '#e4e3df'
plt.rcParams.update({'font.family': 'serif', 'font.size': 8.5, 'axes.edgecolor': INK2, 'axes.labelcolor': INK,
                     'xtick.color': INK2, 'ytick.color': INK2, 'axes.spines.top': False, 'axes.spines.right': False,
                     'pdf.fonttype': 42})


def dumbbell(S, out):
    per = S['per_system']
    keys = sorted(per, key=lambda k: per[k]['ex'])
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    for i, k in enumerate(keys):
        e, c = 100 * per[k]['ex'], 100 * per[k]['corrected']
        ax.plot([c, e], [i, i], color=GRID, lw=2, zorder=1, solid_capstyle='round')
        ax.scatter([e], [i], s=30, color=BLUE, zorder=3, edgecolor='white', linewidth=1)
        ax.scatter([c], [i], s=30, color=ORANGE, zorder=3, edgecolor='white', linewidth=1)
        ax.text(e + 0.6, i, f'{e:.1f}', va='center', fontsize=7, color=INK2)
        ax.text(c - 0.6, i, f'{c:.1f}', va='center', ha='right', fontsize=7, color=INK2)
    ax.set_yticks(range(len(keys)))
    ax.set_yticklabels([per[k]['name'] for k in keys])
    ax.set_xlabel('Accuracy on held-out questions (%)')
    ax.grid(axis='x', color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    lo = min(100 * per[k]['corrected'] for k in keys) - 4
    hi = max(100 * per[k]['ex'] for k in keys) + 4
    ax.set_xlim(lo, hi)
    ax.scatter([], [], color=BLUE, s=30, label='Execution accuracy (EX)')
    ax.scatter([], [], color=ORANGE, s=30, label='EX minus certified false positives')
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False, fontsize=7.5)
    fig.tight_layout()
    fig.savefig(os.path.join(out, 'accuracy_dumbbell.pdf'))
    plt.close(fig)


def cdf(S, out):
    tt = S['time_to_witness']
    bins = [0.01, 0.03, 0.1, 0.3, 1, 2, 3, 4, 5]
    fig, ax = plt.subplots(figsize=(3.45, 2.5) if COLUMN else (4.2, 2.9))
    for name, col in (('CaliberGraph', BLUE), ('ParSEval-L1', ORANGE), ('Random fuzzing', AQUA)):
        if name in tt:
            ax.plot(bins, tt[name]['curve'], color=col, lw=2, marker='o', ms=4, label=name)
            ax.text(bins[-1] * 1.05, tt[name]['curve'][-1], f"{tt[name]['curve'][-1]}", va='center', fontsize=7, color=INK2)
    ax.set_xscale('log')
    ax.set_xlabel('Search time per distinct pair (s, log scale)')
    ax.set_ylabel('Distinct pairs with witness' if COLUMN else 'Certified witnesses found')
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    # legend below the axes, so that it covers no curve
    ax.legend(frameon=False, fontsize=7.5, loc='upper center', bbox_to_anchor=(0.5, -0.32), ncol=3,
              handlelength=1.5, columnspacing=1.0)
    fig.tight_layout()
    fig.savefig(os.path.join(out, 'time_to_witness.pdf'), bbox_inches='tight')
    plt.close(fig)


def taxonomy(T, out):
    items = sorted(T['counts'].items(), key=lambda x: x[1])
    labels = {'empty_aggregate': 'Empty result vs. NULL aggregate', 'null_semantics': 'NULL handling',
              'duplicates_distinct': 'Duplicates / DISTINCT / join fan-out', 'order_limit_ties': 'ORDER BY + LIMIT (ties, windows)',
              'numeric_type_division': 'Numeric type / integer division', 'filter_predicate': 'Filter predicate',
              'join_path': 'Join path / tables', 'projection': 'Projected columns', 'grouping': 'Grouping', 'other': 'Other'}
    fig, ax = plt.subplots(figsize=(4.8, 2.8))
    ys = range(len(items))
    ax.barh(list(ys), [v for _, v in items], color=BLUE, height=0.62)
    for y, (k, v) in zip(ys, items):
        ax.text(v + max(x for _, x in items) * 0.01, y, f'{v} ({100 * v / T["n"]:.0f}%)', va='center', fontsize=7, color=INK2)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([labels.get(k, k) for k, _ in items])
    ax.set_xlabel('Certified EX false positives (multi-label)')
    ax.grid(axis='x', color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.set_xlim(0, max(v for _, v in items) * 1.22)
    fig.tight_layout()
    fig.savefig(os.path.join(out, 'taxonomy.pdf'))
    plt.close(fig)


def attribution(rows, out):
    """rows: list of (label, counts dict, n). Stacked horizontal bars of the attribution classes."""
    cls = [('pred_wrong', 'Prediction error', ORANGE), ('both_wrong', None, ORANGE), ('gold_wrong', 'Gold error', BLUE),
           ('ambiguous', 'Ambiguous question', AQUA), ('implausible_data', 'Implausible data', GRID)]
    fig, ax = plt.subplots(figsize=(3.45, 0.26 * len(rows) + 0.9) if COLUMN else (5.6, 0.32 * len(rows) + 1.0))
    for y, (label, c, n) in enumerate(rows):
        left = 0
        segs = [(c.get('pred_wrong', 0) + c.get('both_wrong', 0), ORANGE), (c.get('gold_wrong', 0), BLUE),
                (c.get('ambiguous', 0), AQUA), (c.get('implausible_data', 0), '#c9c7c1')]
        for v, col in segs:
            w = 100 * v / n
            ax.barh([y], [w], left=left, color=col, height=0.62, edgecolor='white', linewidth=0.6)
            if w >= 6:
                ax.text(left + w / 2, y, f'{w:.0f}', ha='center', va='center', fontsize=7 if COLUMN else 6.5, color=INK if col != ORANGE else 'white')
            left += w
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows])
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel('Share of sampled witnesses (%)')
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=ORANGE, label='Prediction error'), Patch(color=BLUE, label='Gold error'),
                       Patch(color=AQUA, label='Ambiguous question'), Patch(color='#c9c7c1', label='Implausible data')],
              loc='lower center', bbox_to_anchor=(0.35 if COLUMN else 0.45, 1.0), ncol=2 if COLUMN else 4, frameon=False,
              fontsize=7 if COLUMN else 6.5)
    del cls
    fig.tight_layout()
    fig.savefig(os.path.join(out, 'attribution.pdf'), bbox_inches='tight')
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--summary', required=True)
    ap.add_argument('--taxonomy')
    ap.add_argument('--out', required=True)
    ap.add_argument('--attr-v4', dest='attr_v4')
    ap.add_argument('--summary-r', dest='summary_r')
    ap.add_argument('--column', action='store_true', help='one-column sizes (IEEE two-column layout)')
    a = ap.parse_args()
    global COLUMN
    COLUMN = a.column
    S = json.load(open(a.summary))
    os.makedirs(a.out, exist_ok=True)
    if 'per_system' in S:
        dumbbell(S, a.out)
    if S.get('time_to_witness'):
        cdf(S, a.out)
    if a.taxonomy and os.path.exists(a.taxonomy):
        taxonomy(json.load(open(a.taxonomy)), a.out)
    rows = []
    names = {'CaliberGraph@L1f': 'CaliberGraph ($\\mathcal{A}_{1f}$)', 'Fuzz@L1f': 'Random fuzzing ($\\mathcal{A}_{1f}$)',
             'ParSEval-L1@L1f': 'ParSEval-L1 ($\\mathcal{A}_{1f}$)', 'SpotIt@L0': 'SpotIt ($\\mathcal{A}_0$)' if COLUMN else 'SpotIt, re-certified ($\\mathcal{A}_0$)',
             'SpotIt+@L0': 'SpotIt+ ($\\mathcal{A}_0$)' if COLUMN else 'SpotIt+, re-certified ($\\mathcal{A}_0$)', 'CaliberGraph-R@R': 'CaliberGraph-R ($\\mathcal{A}_R$)',
             'Fuzz-R@R': 'Random fuzzing-R ($\\mathcal{A}_R$)'}
    if a.attr_v4 and os.path.exists(a.attr_v4):
        for src, v in json.load(open(a.attr_v4))['methods'].items():
            rows.append((names.get(src, src), v['counts'], v['n']))
    if a.summary_r and os.path.exists(a.summary_r):
        for src, v in json.load(open(a.summary_r)).get('attribution', {}).items():
            if src in names and not src.startswith('_'):
                rows.append((names[src], v['counts'], v['n']))
    order = list(names.values())
    rows.sort(key=lambda r: order.index(r[0]) if r[0] in order else 99)
    if rows:
        attribution(rows, a.out)
    print('figures written to', a.out)


if __name__ == '__main__':
    main()
