"""SVG/PDF/PNG from retained additive-metric CSVs; no trainer or simulator."""
import argparse
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def plot_rows(rows, output):
    if not rows:raise ValueError('empty summary')
    effect=np.array([float(r['effect_positive_is_better']) for r in rows])
    lo=np.array([float(r['ci_low']) for r in rows]);hi=np.array([float(r['ci_high']) for r in rows])
    valid=np.isfinite(lo)&np.isfinite(hi)
    if not np.isfinite(effect).all() or np.any(np.isfinite(lo)!=np.isfinite(hi)) or np.any(lo[valid]>hi[valid]):
        raise ValueError('nonfinite effects, incomplete or reversed interval')
    plt.rcParams.update({'svg.fonttype':'none','pdf.fonttype':42,'ps.fonttype':42,'font.size':9})
    fig,ax=plt.subplots(figsize=(6.8,max(2.5,.34*len(rows)+1.2)))
    y=np.arange(len(rows));ax.axvline(0,linewidth=.8);ax.scatter(effect,y,s=22)
    # Percentile intervals need not contain their point estimate. Preserve endpoints.
    ax.hlines(y[valid],lo[valid],hi[valid],linewidth=1)
    labels=[f"{r['condition_id'].replace('_',' ')} (n={r['groups']})" for r in rows]
    methods={r['method'] for r in rows}
    if len(methods)==1:
        ax.set_title(next(iter(methods)).replace('_',' '))
    else:
        labels=[f"{r['method'].replace('_',' ')} | {label}" for r,label in zip(rows,labels)]
    ax.set_yticks(y,labels);ax.invert_yaxis();ax.set_xlabel('Paired group effect (positive = candidate better)')
    ax.spines[['top','right']].set_visible(False);fig.tight_layout()
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    for ext in ['svg','pdf','png']:fig.savefig(out/f'paired_effects.{ext}',dpi=300)
    plt.close(fig)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True);p.add_argument('--output-dir',required=True)
    p.add_argument('--method', help='plot one explicitly selected method')
    args=p.parse_args()
    with Path(args.input).open(newline='',encoding='utf-8') as f:rows=list(csv.DictReader(f))
    if args.method:rows=[r for r in rows if r['method']==args.method]
    plot_rows(rows,args.output_dir)
    print(f'CSV-only figure rows={len(rows)}')

if __name__=='__main__':main()
