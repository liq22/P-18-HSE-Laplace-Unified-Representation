"""Paired original-group means with a condition-wide common training-seed set.

Average units within group-seed, the same seeds within each group, then groups
equally. The bootstrap conditions on these trained seeds; it does not estimate
the population of training randomness. Macro-F1 requires pooled predictions.
"""
from __future__ import annotations
import argparse
import csv
from collections import defaultdict
from pathlib import Path
import numpy as np

REQUIRED={'method','condition_id','group_id','seed','unit_id','value'}


def read_rows(path):
    with Path(path).open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    if not rows or REQUIRED-set(rows[0]):
        raise ValueError('nonempty CSV with method, condition_id, group_id, seed, unit_id, value required')
    seen=set()
    for r in rows:
        if any(not r[k].strip() for k in REQUIRED): raise ValueError('empty identifier or value')
        key=tuple(r[k] for k in ['method','condition_id','group_id','seed','unit_id'])
        if key in seen: raise ValueError(f'duplicate observation: {key}')
        seen.add(key)
        r['value']=float(r['value'])
        if not np.isfinite(r['value']): raise ValueError('nonfinite metric value')
    return rows


def reduce_method(rows, method, condition):
    selected=[r for r in rows if r['method']==method and r['condition_id']==condition]
    if not selected: raise ValueError(f'no rows for {method}/{condition}')
    unit={}
    group_seed=defaultdict(list)
    for r in selected:
        key=(r['group_id'],r['seed'],r['unit_id'])
        if key in unit: raise ValueError(f'duplicate observation for {method}/{condition}')
        unit[key]=float(r['value']);group_seed[key[:2]].append(float(r['value']))
    groups=defaultdict(list)
    for (g,_),values in group_seed.items():groups[g].append(float(np.mean(values)))
    return unit,{g:float(np.mean(values)) for g,values in groups.items()}


def interval(values, draws=2000):
    arr=np.asarray(values,float)
    if arr.ndim!=1 or len(arr)==0 or not np.isfinite(arr).all() or draws<1:
        raise ValueError('finite nonempty group effects and positive bootstrap count required')
    if len(arr)<2:return float('nan'),float('nan')
    rng=np.random.default_rng(0)
    means=[np.mean(rng.choice(arr,size=len(arr),replace=True)) for _ in range(draws)]
    return tuple(float(x) for x in np.quantile(means,[.025,.975]))


def summarize(rows, reference, direction='lower', draws=2000, expected_seeds=None):
    if direction not in ('lower','higher'):raise ValueError('direction must be lower or higher')
    methods=sorted({r['method'] for r in rows})
    if reference not in methods or len(methods)<2:raise ValueError('reference and candidate required')
    declared=None if expected_seeds is None else {str(s) for s in expected_seeds}
    if declared is not None and not declared:raise ValueError('expected seed set cannot be empty')
    output=[]
    for condition in sorted({r['condition_id'] for r in rows}):
        selected=[r for r in rows if r['condition_id']==condition]
        seeds={str(r['seed']) for r in selected} if declared is None else declared
        by_group=defaultdict(set)
        for r in selected:by_group[(r['method'],r['group_id'])].add(str(r['seed']))
        for (method,group),observed in by_group.items():
            if observed!=seeds:
                raise ValueError(f'nonuniform seed set: {condition}/{method}/{group}; expected {sorted(seeds)}, got {sorted(observed)}')
        ru,rg=reduce_method(rows,reference,condition)
        for method in methods:
            if method==reference:continue
            cu,cg=reduce_method(rows,method,condition)
            if set(cu)!=set(ru):raise ValueError(f'unpaired units for {method}/{condition}')
            diffs=[(rg[g]-cg[g]) if direction=='lower' else (cg[g]-rg[g]) for g in sorted(rg)]
            lo,hi=interval(diffs,draws)
            output.append(dict(condition_id=condition,reference=reference,method=method,groups=len(diffs),
                effect_positive_is_better=float(np.mean(diffs)),ci_low=lo,ci_high=hi))
    return output


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True);p.add_argument('--reference',required=True)
    p.add_argument('--output',required=True);p.add_argument('--direction',choices=['lower','higher'],default='lower')
    p.add_argument('--bootstrap',type=int,default=2000)
    p.add_argument('--expected-seeds',nargs='+',help='predeclared seeds; catches a seed missing from every arm/group')
    args=p.parse_args()
    rows=summarize(read_rows(args.input),args.reference,args.direction,args.bootstrap,args.expected_seeds)
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(f'comparisons={len(rows)} output={out}')

if __name__=='__main__':main()
