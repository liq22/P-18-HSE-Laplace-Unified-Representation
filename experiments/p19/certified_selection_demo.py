"""CPU binary forecasting experiment: single/static/hard selection with holdout.

Bernoulli events and probability forecasts are explicit statistical devices, not
trained HSE features. Fit, calibration and test draws are disjoint. A reversal
cell demonstrates the failure of transporting a source certificate without its
assumption, not a contradiction of the theorem.
"""
import argparse
import csv
from pathlib import Path
import numpy as np
from .policy_certificate import evaluate_rows


def sample(n, rng, probability):
    a=rng.integers(0,2,size=n)
    y=(rng.random(n)<np.asarray(probability)[a]).astype(float)
    return a,y


def experiment(n_calibration=2048, seed=0):
    if n_calibration<2: raise ValueError('at least two calibration groups required')
    summaries=[]; allrows={}
    for cell, name in enumerate(['same_best','complementary','target_reversal','shift_allowance']):
        # Reversal/allowance use exactly the same draws; only the declared bound changes.
        rng=np.random.default_rng(np.random.SeedSequence([seed,min(cell,2)]))
        source=[.2,.2] if name=='same_best' else [.2,.8]
        target=source if name in ['same_best','complementary'] else [.8,.2]
        a_fit,y_fit=sample(512,rng,source)
        # All fitted choices are made before the certification sample is drawn.
        qgrid=np.linspace(.2,.8,5)
        qstatic=float(qgrid[np.argmin(np.mean((qgrid[None,:]-y_fit[:,None])**2,axis=0))])
        hard=np.array([.2 if np.mean((.2-y_fit[a_fit==a])**2)<=np.mean((.8-y_fit[a_fit==a])**2) else .8 for a in [0,1]])
        rows=[]
        for split,n,prob in [('calibration',n_calibration,source),('test',4096,target)]:
            a,y=sample(n,rng,prob)
            prediction={'static_reference':np.full(n,qstatic),'single_R':np.full(n,.2),
                        'single_M':np.full(n,.8),'hard_source_route':hard[a]}
            # Fixed declared costs, not purported GPU timings. An interior static
            # blend evaluates both fixed arms; the selector pays its stated cost.
            static_cost=.01 if np.isclose(qstatic,.2) or np.isclose(qstatic,.8) else .02
            costs={'static_reference':static_cost,'single_R':.01,'single_M':.01,'hard_source_route':.0105}
            for policy,pred in prediction.items():
                for i,loss in enumerate((pred-y)**2):
                    rows.append(dict(split=split,group_id=f'{name}:{seed}:{split}:{i}',policy=policy,
                                     loss=float(loss),cost_penalty=costs[policy]))
        shift=.4 if name=='shift_allowance' else 0.
        result=evaluate_rows(rows,'static_reference',margin=.01,shift_bound=shift)
        summaries.append(dict(scenario=name,calibration_groups=n_calibration,seed=seed,
                              selected_policy=result['selected_policy'],radius=result['radius'],
                              best_lower_bound=max(result['lower_bound']),
                              reference_test_risk=result['reference_test_risk'],
                              selected_test_risk=result['selected_test_risk'],
                              test_net_improvement=result['realized_test_net_improvement'],
                              shift_bound=shift))
        allrows[name]=rows
    return summaries,allrows


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--seeds',type=int,nargs='+',default=[0,1,2])
    p.add_argument('--calibration-groups',type=int,nargs='+',default=[64,2048])
    args=p.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    summary=[]
    for n in args.calibration_groups:
        for seed in args.seeds:
            rows,raw=experiment(n,seed);summary.extend(rows)
            for name,records in raw.items():
                path=args.output_dir/f'{name}_n{n}_seed{seed}_group_scores.csv'
                with path.open('w',newline='',encoding='utf-8') as f:
                    w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    with (args.output_dir/'selection_summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
    for r in summary: print(r)

if __name__=='__main__':main()
