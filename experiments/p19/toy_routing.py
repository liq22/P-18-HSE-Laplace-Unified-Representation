"""Observed finite simulations for fixed-arm routing, fusion and shift boundaries.

The simulated predictors are declared stochastic measurement devices, not trained
HSE models. Source selector fitting and test events are independent. CSVs are
actual squared losses; exact population checks remain separately labelled.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import numpy as np
from .routing import weighted_headroom, select_fixed_arms, fit_static_squared


def check_boundaries():
    p = np.array([.5, .5])
    crossing = np.array([[.15, .30], [.35, .20]])
    dominated = np.array([[.20, .25], [.30, .35]])
    np.testing.assert_allclose(weighted_headroom(crossing, p), .075)
    np.testing.assert_allclose(weighted_headroom(dominated, p), 0, atol=1e-15)
    # R=0, M=1, y=.25 or .40: R wins both strata, but soft fusion helps.
    targets = np.array([.25, .40])
    risk = np.column_stack((targets**2, (1-targets)**2))
    np.testing.assert_allclose(weighted_headroom(risk, p), 0, atol=1e-15)
    alpha = fit_static_squared(np.tile([0., 1.], (2, 1)), targets)
    np.testing.assert_allclose(alpha, .325)
    np.testing.assert_allclose(np.mean((alpha-targets)**2), .005625)
    return crossing, dominated


def simulate(scenario, events, rng, shift=False):
    a = np.tile(np.arange(2), events)
    group = np.repeat(np.arange(events), 2)
    if scenario == 'fusion_without_crossing':
        y = np.where(a == 0, .25, .40)
        pred = np.column_stack((np.zeros(len(a)), np.ones(len(a))))
    else:
        y = np.repeat(rng.normal(size=events), 2)
        risk = np.array([[.20, .25], [.30, .35]]) if scenario == 'no_headroom' else np.array([[.15, .30], [.35, .20]])
        if shift:
            risk = risk[::-1]
        pred = y[:, None] + rng.normal(size=(len(a), 2)) * np.sqrt(risk[a])
    return group, a, y, pred


def run(events, seed):
    if events < 2:
        raise ValueError('at least two independent events per split required')
    check_boundaries()
    event_rows, summary = [], []
    scenarios = ['no_headroom', 'positive_headroom', 'fusion_without_crossing', 'target_reversal']
    for k, scenario in enumerate(scenarios):
        _, sa, sy, sp = simulate(scenario, events, np.random.default_rng(seed+100*k))
        tg, ta, ty, tp = simulate(scenario, events, np.random.default_rng(seed+100*k+1), shift=scenario == 'target_reversal')
        source_risk = np.vstack([np.mean((sp[sa == c]-sy[sa == c, None])**2, axis=0) for c in range(2)])
        best, hard = select_fixed_arms(source_risk, [.5, .5])
        alpha = fit_static_squared(sp, sy)
        # This soft two-cell fit is a counterexample control, not our hard router.
        soft = np.array([fit_static_squared(sp[sa == c], sy[sa == c]) for c in range(2)])
        prediction = {'R': tp[:, 0], 'M': tp[:, 1], 'best_single': tp[:, best],
                      'static_prediction_fusion': (1-alpha)*tp[:, 0]+alpha*tp[:, 1],
                      'hard_source_route': tp[np.arange(len(tp)), hard[ta]],
                      'soft_cell_control': (1-soft[ta])*tp[:, 0]+soft[ta]*tp[:, 1]}
        for method, values in prediction.items():
            loss = (values-ty)**2
            summary.append(dict(scenario=scenario, method=method, test_mse=float(np.mean(loss)),
                                source_empirical_headroom=weighted_headroom(source_risk, [.5,.5]),
                                source_static_alpha=alpha, test_events=events, simulator_seed=seed))
            for i, value in enumerate(loss):
                event_rows.append(dict(scenario=scenario, method=method, condition_id=f'{scenario}:{ta[i]}',
                    group_id=f'{scenario}:test:{tg[i]}', seed=seed, unit_id=str(tg[i]), value=float(value)))
    return event_rows, summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--events', type=int, default=512)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--output', type=Path, default=Path('outputs/p19/toy_routing.csv'))
    args=parser.parse_args()
    rows, summary=run(args.events,args.seed)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    for path, data in [(args.output, summary), (args.output.with_name(args.output.stem+'_events.csv'), rows)]:
        with path.open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=list(data[0])); writer.writeheader(); writer.writerows(data)
    print('population hard headroom: crossing=0.075; dominated=0')
    print('fusion counterexample: hard headroom=0; best static MSE=0.005625; soft MSE=0')
    print(f'actual simulated summary_rows={len(summary)} event_rows={len(rows)}')
    for r in summary:
        print(f"{r['scenario']}/{r['method']}: {r['test_mse']:.8f}")

if __name__ == '__main__':main()
