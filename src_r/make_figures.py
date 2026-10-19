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
    fig, ax = plt.subplots(figsize=(4.2, 2.6))
    for name, col in (('CaliberGraph', BLUE), ('ParSEval-L1', ORANGE), ('Random fuzzing', AQUA)):
        if name in tt:
            ax.plot(bins, tt[name]['curve'], color=col, lw=2, marker='o', ms=4, label=name)
            ax.text(bins[-1] * 1.05, tt[name]['curve'][-1], f"{tt[name]['curve'][-1]}", va='center', fontsize=7, color=INK2)
    ax.set_xscale('log')
    ax.set_xlabel('Search time per distinct pair (s, log scale)')
    ax.set_ylabel('Certified witnesses found')
    ax.grid(color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=7.5, loc='upper left')
    fig.tight_layout()
    fig.savefig(os.path.join(out, 'time_to_witness.pdf'))
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--summary', required=True)
    ap.add_argument('--taxonomy')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    S = json.load(open(a.summary))
    os.makedirs(a.out, exist_ok=True)
    if 'per_system' in S:
        dumbbell(S, a.out)
    if S.get('time_to_witness'):
        cdf(S, a.out)
    if a.taxonomy and os.path.exists(a.taxonomy):
        taxonomy(json.load(open(a.taxonomy)), a.out)
    print('figures written to', a.out)


if __name__ == '__main__':
    main()
