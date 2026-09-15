"""Independent metrics from PHMFactory-exported predictions, not a new reader."""
import argparse
import csv
from collections import Counter
from pathlib import Path
import numpy as np


def confusion_metrics(y, pred, groups=None, classes=3):
    y, pred=np.asarray(y),np.asarray(pred)
    if y.ndim!=1 or y.shape!=pred.shape or len(y)==0 or not np.isin(y,range(classes)).all() or not np.isin(pred,range(classes)).all():
        raise ValueError('paired labels in the declared ontology required')
    weights=np.ones(len(y))
    if groups is not None:
        if len(groups)!=len(y):raise ValueError('group length mismatch')
        counts=Counter(groups);weights=np.array([1/counts[g] for g in groups])
    cm=np.bincount(classes*y.astype(int)+pred.astype(int),weights=weights,minlength=classes**2).reshape(classes,classes)
    tp=np.diag(cm);den=cm.sum(0)+cm.sum(1)
    f1=np.divide(2*tp,den,out=np.zeros(classes),where=den>0)
    return float(tp.sum()/cm.sum()),float(f1.mean())


def recompute(rows):
    if not rows:raise ValueError('empty predictions')
    result=[]
    for seed in sorted({r['seed'] for r in rows},key=int):
        subset=[r for r in rows if r['seed']==seed]
        y=[int(r['y_true']) for r in subset];p=[int(r['y_pred']) for r in subset];g=[r['group_id'] for r in subset]
        a,f=confusion_metrics(y,p);ga,gf=confusion_metrics(y,p,g)
        result.append(dict(seed=int(seed),test_windows=len(y),recordings=len(set(g)),accuracy=a,macro_f1=f,
                           group_balanced_accuracy=ga,group_balanced_macro_f1=gf))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--predictions',required=True);p.add_argument('--output',required=True)
    p.add_argument('--reference',help='optional framework-acceptance CSV for agreement checking')
    args=p.parse_args()
    with Path(args.predictions).open(newline='') as f:rows=recompute(list(csv.DictReader(f)))
    if args.reference:
        with Path(args.reference).open(newline='') as f:ref={int(r['seed']):r for r in csv.DictReader(f)}
        if set(ref)!={r['seed'] for r in rows}:raise ValueError('seed sets differ')
        for r in rows:
            for key in ['accuracy','macro_f1']:
                np.testing.assert_allclose(r[key],float(ref[r['seed']][key]),atol=1e-6,rtol=0)
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    for r in rows:print(r)

if __name__=='__main__':main()
