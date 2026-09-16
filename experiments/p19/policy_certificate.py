"""Paired finite-policy certificate on independent group-level bounded losses.

Policies, reference, cost penalties and loss definition must be frozen without
using the certification sample. A certificate is not a guarantee under arbitrary
acquisition shift. No predictor is trained or silently substituted in this module.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import numpy as np


def certify(reference, candidates, cost_difference, *, alpha=.05, margin=0., shift_bound=0.):
    """Return simultaneous lower bounds and -1 when retaining the reference.

    Rows are independent original groups, not windows or posterior draws.
    Candidates has one column per fixed candidate; costs are declared constants.
    Losses are in [0,1]. Clipping elsewhere changes the certified estimand.
    """
    ref, loss = np.asarray(reference, float), np.asarray(candidates, float)
    costs = np.asarray(cost_difference, float)
    if ref.ndim != 1 or loss.ndim != 2 or loss.shape[0] != len(ref) or min(loss.shape) < 1:
        raise ValueError('reference[N] and candidates[N,J] must be nonempty and paired')
    if costs.shape != (loss.shape[1],) or not np.isfinite(costs).all():
        raise ValueError('one finite fixed incremental cost per candidate required')
    if not np.isfinite(ref).all() or not np.isfinite(loss).all() or (ref < 0).any() or (ref > 1).any() or (loss < 0).any() or (loss > 1).any():
        raise ValueError('bounded losses in [0,1] required; no automatic clipping')
    if not (0 < alpha < 1) or not np.isfinite([margin, shift_bound]).all() or min(margin, shift_bound) < 0:
        raise ValueError('alpha in (0,1), nonnegative margin and shift bound required')
    radius = float(np.sqrt(2*np.log(loss.shape[1]/alpha)/len(ref)))
    improvement = np.mean(ref[:, None]-loss, axis=0)-costs
    lower = improvement-radius-shift_bound
    best = int(np.argmax(lower))
    selected = best if lower[best] > margin else -1
    return dict(selected_index=selected, independent_groups=len(ref), candidates=loss.shape[1],
                empirical_net_improvement=improvement.tolist(), lower_bound=lower.tolist(),
                radius=radius, alpha=float(alpha), margin=float(margin), shift_bound=float(shift_bound))


def _matrix(rows, split, policies):
    chosen = [r for r in rows if r['split'] == split]
    keys = {(r['policy'], r['group_id']) for r in chosen}
    if len(keys) != len(chosen):
        raise ValueError(f'duplicate group/policy in {split}; average windows upstream')
    groups = sorted({r['group_id'] for r in chosen})
    if not groups or keys != {(p,g) for p in policies for g in groups}:
        raise ValueError(f'incomplete {split} policy/group pairing')
    bykey = {(r['policy'], r['group_id']): float(r['loss']) for r in chosen}
    matrix = np.array([[bykey[p,g] for p in policies] for g in groups])
    if not np.isfinite(matrix).all() or (matrix < 0).any() or (matrix > 1).any():
        raise ValueError(f'{split} must contain losses in [0,1]')
    return groups, matrix


def evaluate_rows(rows, reference, *, alpha=.05, margin=0., shift_bound=0.):
    required = {'split','group_id','policy','loss','cost_penalty'}
    if not rows or any(required-set(r) for r in rows):
        raise ValueError('missing score columns')
    if any(not str(r[k]).strip() for r in rows for k in required):
        raise ValueError('empty score field')
    if {r['split'] for r in rows} != {'calibration','test'}:
        raise ValueError('separate calibration and test rows are required')
    names = sorted({r['policy'] for r in rows})
    if reference not in names or len(names) < 2:
        raise ValueError('reference and at least one candidate required')
    names = [reference]+[p for p in names if p != reference]
    costs=[]
    for name in names:
        values={float(r['cost_penalty']) for r in rows if r['policy']==name}
        if len(values)!=1 or not np.isfinite(list(values)).all() or min(values)<0:
            raise ValueError('cost penalties must be fixed nonnegative declarations, not sampled latency')
        costs.append(values.pop())
    groups,cal=_matrix(rows,'calibration',names)
    testgroups,test=_matrix(rows,'test',names)
    if set(groups)&set(testgroups):
        raise ValueError('original groups cross calibration/test')
    result=certify(cal[:,0],cal[:,1:],np.asarray(costs[1:])-costs[0],alpha=alpha,margin=margin,shift_bound=shift_bound)
    result['candidate_names']=names[1:]
    chosen=result['selected_index']+1
    result.update(reference=reference,selected_policy=names[chosen],test_groups=len(testgroups),
                  reference_test_risk=float(test[:,0].mean()),selected_test_risk=float(test[:,chosen].mean()),
                  realized_test_net_improvement=float((test[:,0]-test[:,chosen]).mean()-costs[chosen]+costs[0]))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True);p.add_argument('--reference',required=True)
    p.add_argument('--alpha',type=float,default=.05);p.add_argument('--margin',type=float,default=.01)
    p.add_argument('--shift-bound',type=float,default=0.)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    with args.input.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    result=evaluate_rows(rows,args.reference,alpha=args.alpha,margin=args.margin,shift_bound=args.shift_bound)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
