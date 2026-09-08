"""Run Task B; save one summary CSV and two plots from paired event metrics."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from .compression import evaluate_cell


def bootstrap_interval(values: np.ndarray, seed: int, repetitions: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    averages = np.empty(repetitions)
    # Chunk bootstrap indices to keep memory independent of the full replicate count.
    for first in range(0, repetitions, 64):
        count = min(64, repetitions-first)
        indices = rng.integers(0, values.size, size=(count, values.size))
        averages[first:first+count] = values[indices].mean(axis=1)
    return tuple(float(x) for x in np.quantile(averages, [.025, .975]))


def run_experiment(events_per_seed: int, seeds: list[int], repetitions: int) -> list[dict]:
    if repetitions < 2 or not seeds or len(seeds) != len(set(seeds)):
        raise ValueError('use at least two bootstrap replicates and distinct simulator seeds')
    rows = []
    for prior in ['gaussian', 'mixture']:
        for cross in [0., .45, .8]:
            results = [evaluate_cell(prior, cross, seed, events_per_seed) for seed in seeds]
            for regime, arm in results[0]:
                method = arm.split('_')[0]
                row = {'prior': prior, 'within_coupling': .6, 'cross_coupling': cross,
                       'side_information': regime, 'arm': arm,
                       'events': events_per_seed*len(seeds), 'views_per_event': 4,
                       'simulator_seeds': ';'.join(map(str, seeds)),
                       'unique_summary_scalars': {'full': 14, 'diag': 8, 'block': 10}[method],
                       'extra_operator_scalars': 16 if regime == 'full_operator' else 0}
                for metric in results[0][(regime, arm)]:
                    values = np.concatenate([r[(regime, arm)][metric] for r in results])
                    row[metric] = float(values.mean())
                    if metric in ['total_gap_nats', 'compression_nats', 'fitting_nats',
                                  'gain_over_diag_nats', 'coverage_90']:
                        lo, hi = bootstrap_interval(values, seed=7301, repetitions=repetitions)
                        row[metric+'_lo'], row[metric+'_hi'] = lo, hi
                rows.append(row)
            print(f'Completed {prior}: cross={cross}; {events_per_seed*len(seeds)} independent events')
    return rows


def plot_results(rows: list[dict], output: Path) -> None:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    matplotlib.rcParams['svg.fonttype'] = 'none'
    fig, ax = plt.subplots(figsize=(7.8, 4.8), constrained_layout=True)
    for prior, line in [('gaussian', '-'), ('mixture', '--')]:
        for arm, marker in [('diag_exact', 'o'), ('block_exact', 's')]:
            data = [r for r in rows if r['prior'] == prior and r['side_information'] == 'coarse' and r['arm'] == arm]
            x, y = [r['cross_coupling'] for r in data], [r['total_gap_nats'] for r in data]
            lo, hi = [r['total_gap_nats_lo'] for r in data], [r['total_gap_nats_hi'] for r in data]
            ax.errorbar(x, y, yerr=[np.subtract(y, lo), np.subtract(hi, y)],
                        marker=marker, linestyle=line, capsize=3, label=f'{prior}: {arm}')
    ax.set(xlabel='Cross-mode information coupling', ylabel='Estimated expected conditional KL (nats)',
           title='Exact compressed posterior: event-paired 95% intervals')
    ax.legend(fontsize=9)
    fig.savefig(output/'compression.svg')
    fig.savefig(output/'compression.png', dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.8, 4.8), constrained_layout=True)
    for prior, line in [('gaussian', '-'), ('mixture', '--')]:
        for arm in ['diag_exact', 'diag_plugin', 'block_exact', 'block_plugin']:
            row = next(r for r in rows if r['prior']==prior and r['cross_coupling']==.8
                       and r['side_information']=='coarse' and r['arm']==arm)
            ax.plot([.5, .8, .9], [row[f'coverage_{x}'] for x in [50, 80, 90]],
                    marker='o', linestyle=line, label=f'{prior}: {arm}')
    ax.plot([.45, 1.], [.45, 1.], ':', label='Nominal')
    ax.set(xlabel='Nominal central marginal coverage', ylabel='Observed coverage',
           title='True compressed conditional versus plug-in: cross coupling 0.8')
    ax.legend(fontsize=8, ncol=2)
    fig.savefig(output/'calibration.svg')
    fig.savefig(output/'calibration.png', dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--events-per-seed', type=int, default=2048)
    parser.add_argument('--seeds', nargs='+', type=int, default=[0, 1, 2])
    parser.add_argument('--bootstrap', type=int, default=1000)
    parser.add_argument('--output-dir', type=Path, default=Path('outputs/task_b'))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = run_experiment(args.events_per_seed, args.seeds, args.bootstrap)
    with (args.output_dir/'compression_summary.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    plot_results(rows, args.output_dir)
    print(json.dumps({'rows': len(rows), 'csv': str(args.output_dir/'compression_summary.csv'),
                      'evidence_level': 'finite_design_coefficient_space_oracle',
                      'formal_claim_supported': False}, indent=2))


if __name__ == '__main__':
    main()
