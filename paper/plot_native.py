"""CSV-only figures for native checks and explicit paired comparisons.

No model import, training, or implicit deletion of unmatched observations.
Intervals condition on executed training seeds. Multi-arm CSVs need an explicit
reference/candidate choice; other arms are retained in the original file.
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
    if not rows: raise ValueError('CSV has no observations')
    return rows


def number(value):
    value = float(value)
    if not np.isfinite(value): raise ValueError('nonfinite reported number')
    return value


def select_comparison_rows(rows, reference, candidate, explicit=False):
    if reference == candidate: raise ValueError('distinct reference and candidate required')
    observed={r['arm'] for r in rows}
    chosen={reference,candidate}
    if not chosen<=observed: raise ValueError('selected arm is absent from CSV')
    if observed-chosen and not explicit:
        raise ValueError('multi-arm CSV requires explicit --reference and --candidate; no default row deletion')
    return [r for r in rows if r['arm'] in chosen]


def comparison_summary(rows, repetitions=2000, reference='B1_aux', candidate='M'):
    """Pair events; average common seeds and then events inside original groups."""
    if repetitions < 1 or reference == candidate:
        raise ValueError('positive bootstrap count and distinct arms required')
    arms = {candidate: {}, reference: {}}
    groups = {}
    for field in ('posterior_draws','sampler_steps'):
        if any(field in r for r in rows):
            if not all(field in r for r in rows): raise ValueError(f'incomplete {field} metadata')
            values={number(r[field]) for r in rows}
            minimum=2 if field=='posterior_draws' else 1
            if len(values)!=1 or any(v<minimum or v!=int(v) for v in values):
                raise ValueError(f'paired comparison requires one common valid {field}')
    for row in rows:
        arm = row['arm']
        if arm not in arms: raise ValueError('unexpected arm; select the comparison explicitly')
        event = (row['condition_id'], row['event_id'])
        group = row['group_id']
        if event in groups and groups[event] != group:
            raise ValueError('one event has inconsistent original group IDs')
        groups[event] = group
        key = (*event, row['seed'])
        if key in arms[arm]: raise ValueError('duplicate event/condition/seed/arm row')
        arms[arm][key] = number(row['energy_score'])
    if not arms[candidate] or arms[candidate].keys() != arms[reference].keys():
        raise ValueError('selected arms require exactly matching event/condition/seed keys')
    summaries = []
    rng = np.random.default_rng(0)
    for condition in sorted({k[0] for k in arms[candidate]}):
        subset = [k for k in arms[candidate] if k[0] == condition]
        seeds = {k[2] for k in subset}
        event_values = {}
        for event in sorted({k[1] for k in subset}):
            keys = [k for k in subset if k[1] == event]
            if {k[2] for k in keys} != seeds:
                raise ValueError('each event must contain every declared seed in its condition')
            event_values[event] = np.mean([arms[candidate][k] - arms[reference][k] for k in keys])
        group_values = {}
        for event, value in event_values.items():
            group_values.setdefault(groups[(condition, event)], []).append(value)
        values = np.array([np.mean(v) for v in group_values.values()])
        if len(values) >= 2:
            means = np.array([rng.choice(values, len(values), replace=True).mean()
                              for _ in range(repetitions)])
            low, high = np.quantile(means, [.025, .975])
        else: low = high = float('nan')
        summaries.append(dict(condition_id=condition, reference=reference, candidate=candidate,
                              paired_delta=float(values.mean()),ci_low=float(low),ci_high=float(high),
                              groups=len(values),events=len(event_values),training_seeds=len(seeds),
                              interval_scope='original-group bootstrap, conditional on executed seeds'))
    return summaries


def save(fig, output, name):
    import matplotlib as mpl
    mpl.rcParams.update({'svg.fonttype': 'none', 'pdf.fonttype': 42})
    output.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    for suffix in ('svg', 'pdf', 'png'): fig.savefig(output / f'{name}.{suffix}', dpi=300)
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
        ax.legend(); save(fig, output, f'moment_{metric}')


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
    ax.set(ylabel='Maximum absolute batch-loss difference',title='Native loss versus independent reconstruction')
    save(fig, output, 'native_loss_alignment')


def render_comparison(rows, output, reference='B1_aux', candidate='M'):
    import matplotlib.pyplot as plt
    summary = comparison_summary(rows, reference=reference, candidate=candidate)
    output.mkdir(parents=True, exist_ok=True)
    with (output / 'paired_comparison.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summary[0]));writer.writeheader();writer.writerows(summary)
    fig, ax = plt.subplots(figsize=(6.7, 3.4))
    for index, row in enumerate(summary):
        ax.scatter([index], [row['paired_delta']])
        if np.isfinite(row['ci_low']): ax.vlines(index, row['ci_low'], row['ci_high'])
        else: ax.annotate('one group: no CI',(index,row['paired_delta']),xytext=(5,8),textcoords='offset points')
    ax.axhline(0, linestyle='--', linewidth=.8)
    ax.set_xticks(np.arange(len(summary)), [r['condition_id'] for r in summary])
    ax.set(ylabel=f'Energy Score: {candidate} minus {reference}',xlabel='Acquisition condition',
           title='Negative favors candidate; intervals condition on executed seeds')
    save(fig, output, 'native_paired_comparison')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind', choices=['scores', 'alignment', 'comparison'])
    parser.add_argument('csv', type=Path);parser.add_argument('output', type=Path)
    parser.add_argument('--reference');parser.add_argument('--candidate')
    args = parser.parse_args()
    if bool(args.reference)!=bool(args.candidate): parser.error('supply both --reference and --candidate')
    if args.kind!='comparison' and args.reference: parser.error('arm selection applies only to comparison')
    required = {'scores': ['step', *[f'{s}_{m}' for s in ('train', 'validation')
                       for m in ('score', 'logdet', 'mahalanobis', 'min_eigenvalue')]],
                'alignment': ['prediction', 'weighting', 'normalization', 'absolute_loss_difference'],
                'comparison': ['arm', 'seed', 'event_id', 'group_id', 'condition_id', 'energy_score']}
    rows = read_rows(args.csv, required[args.kind])
    if args.kind=='comparison':
        ref,candidate=args.reference or 'B1_aux',args.candidate or 'M'
        selected=select_comparison_rows(rows,ref,candidate,explicit=bool(args.reference))
        print(f'Explicit pair: {candidate} minus {ref}; selected {len(selected)} of {len(rows)} retained rows')
        render_comparison(selected,args.output,ref,candidate)
    else: {'scores':render_scores,'alignment':render_alignment}[args.kind](rows,args.output)

if __name__ == '__main__': main()
