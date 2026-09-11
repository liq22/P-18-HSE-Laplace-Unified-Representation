"""CSV-only figures for actual native checks and supplied-feature comparisons.

No model import, fitting, simulation, or deletion of unmatched observations.
Intervals are conditional on the executed training seeds, not seed-population CIs.
"""
import argparse
import csv
from pathlib import Path
import numpy as np


def read_rows(path, required):
    with Path(path).open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        if not set(required).issubset(reader.fieldnames or []):
            raise ValueError(f'CSV must contain {required}')
        rows = list(reader)
    if not rows:
        raise ValueError('CSV has no observations')
    return rows


def number(value):
    value = float(value)
    if not np.isfinite(value):
        raise ValueError('nonfinite reported number')
    return value


def comparison_summary(rows, repetitions=2000):
    """Pair events first; average seeds, then events within original groups."""
    if repetitions < 1:
        raise ValueError('bootstrap repetitions must be positive')
    arms = {'M': {}, 'B1_aux': {}}
    groups = {}
    for row in rows:
        arm = row['arm']
        if arm not in arms:
            raise ValueError('this primary comparison accepts only M and B1_aux')
        event = (row['condition_id'], row['event_id'])
        group = row['group_id']
        if event in groups and groups[event] != group:
            raise ValueError('one event has inconsistent original group IDs')
        groups[event] = group
        key = (*event, row['seed'])
        if key in arms[arm]:
            raise ValueError('duplicate event/condition/seed/arm row')
        arms[arm][key] = number(row['energy_score'])
    if not arms['M'] or arms['M'].keys() != arms['B1_aux'].keys():
        raise ValueError('M and B1_aux require exactly matching event/condition/seed keys')
    summaries = []
    rng = np.random.default_rng(0)
    for condition in sorted({k[0] for k in arms['M']}):
        subset = [k for k in arms['M'] if k[0] == condition]
        seeds = {k[2] for k in subset}
        event_values = {}
        for event in sorted({k[1] for k in subset}):
            keys = [k for k in subset if k[1] == event]
            if {k[2] for k in keys} != seeds:
                raise ValueError('each event must contain every declared seed in its condition')
            event_values[event] = np.mean([arms['M'][k] - arms['B1_aux'][k] for k in keys])
        group_values = {}
        for event, value in event_values.items():
            group_values.setdefault(groups[(condition, event)], []).append(value)
        values = np.array([np.mean(v) for v in group_values.values()])
        if len(values) >= 2:
            means = np.array([rng.choice(values, len(values), replace=True).mean()
                              for _ in range(repetitions)])
            low, high = np.quantile(means, [.025, .975])
        else:
            low = high = float('nan')  # no between-group interval from one group
        summaries.append(dict(condition_id=condition, paired_delta=float(values.mean()),
                              ci_low=float(low), ci_high=float(high), groups=len(values),
                              events=len(event_values), training_seeds=len(seeds),
                              interval_scope='original-group bootstrap, conditional on executed seeds'))
    return summaries


def save(fig, output, name):
    import matplotlib as mpl
    mpl.rcParams.update({'svg.fonttype': 'none', 'pdf.fonttype': 42})
    output.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    for suffix in ('svg', 'pdf', 'png'):
        fig.savefig(output / f'{name}.{suffix}', dpi=300)
    import matplotlib.pyplot as plt
    plt.close(fig)


def render_scores(rows, output):
    import matplotlib.pyplot as plt
    x = np.array([number(row['step']) for row in rows])
    if len(x) > 1 and np.any(np.diff(x) <= 0):
        raise ValueError('a score-curve CSV must contain one strictly ordered run')
    for metric in ('score', 'logdet', 'mahalanobis', 'min_eigenvalue'):
        fig, ax = plt.subplots(figsize=(6.7, 3.2))
        for split in ('train', 'validation'):
            ax.plot(x, [number(row[f'{split}_{metric}']) for row in rows], label=split)
        ax.set(xlabel='Optimizer update', ylabel=metric.replace('_', ' '))
        ax.legend()
        save(fig, output, f'moment_{metric}')


def render_alignment(rows, output):
    import matplotlib.pyplot as plt
    grouped = {}
    for row in rows:
        key = (row['prediction'], row['weighting'], row['normalization'])
        grouped.setdefault(key, []).append(number(row['absolute_loss_difference']))
    keys = sorted(grouped)
    fig, ax = plt.subplots(figsize=(7.1, 3.6))
    ax.scatter(np.arange(len(keys)), [max(grouped[k]) for k in keys])
    labels = [f'{k[0]}\n{k[1].replace("weighted_min_snr", "min-SNR")}\n{k[2]}' for k in keys]
    ax.set_xticks(np.arange(len(keys)), labels, fontsize=7)
    ax.set(ylabel='Maximum absolute batch-loss difference',
           title='Native loss versus independent reconstruction')
    save(fig, output, 'native_loss_alignment')


def render_comparison(rows, output):
    import matplotlib.pyplot as plt
    summary = comparison_summary(rows)
    output.mkdir(parents=True, exist_ok=True)
    with (output / 'paired_comparison.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summary[0]))
        writer.writeheader(); writer.writerows(summary)
    fig, ax = plt.subplots(figsize=(6.7, 3.4))
    for index, row in enumerate(summary):
        ax.scatter([index], [row['paired_delta']])
        if np.isfinite(row['ci_low']):
            ax.vlines(index, row['ci_low'], row['ci_high'])
        else:
            ax.annotate('one group: no CI', (index, row['paired_delta']), xytext=(5, 8), textcoords='offset points')
    ax.axhline(0, linestyle='--', linewidth=.8)
    ax.set_xticks(np.arange(len(summary)), [r['condition_id'] for r in summary])
    ax.set(ylabel='Energy Score: M minus B1-aux', xlabel='Acquisition condition',
           title='Negative favors M; intervals condition on the executed seeds')
    save(fig, output, 'native_paired_comparison')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind', choices=['scores', 'alignment', 'comparison'])
    parser.add_argument('csv', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    required = {'scores': ['step', *[f'{s}_{m}' for s in ('train', 'validation')
                       for m in ('score', 'logdet', 'mahalanobis', 'min_eigenvalue')]],
                'alignment': ['prediction', 'weighting', 'normalization', 'absolute_loss_difference'],
                'comparison': ['arm', 'seed', 'event_id', 'group_id', 'condition_id', 'energy_score']}
    rows = read_rows(args.csv, required[args.kind])
    {'scores': render_scores, 'alignment': render_alignment,
     'comparison': render_comparison}[args.kind](rows, args.output)

if __name__ == '__main__':
    main()
