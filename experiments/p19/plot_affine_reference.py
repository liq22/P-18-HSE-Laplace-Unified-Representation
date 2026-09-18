"""Actual UCI128 affine-reference CSV only; no simulation or training."""
import argparse
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def plot(csv_path, output):
    with Path(csv_path).open(newline='',encoding='utf-8') as f:rows=list(csv.DictReader(f))
    if not rows:raise ValueError('empty reference summary')
    keys=[(r['model'],r['split']) for r in rows]
    if len(set(keys))!=len(keys):raise ValueError('duplicate model/split')
    methods=list(dict.fromkeys(r['model'] for r in rows))
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'svg.fonttype':'none','pdf.fonttype':42,'font.size':9})
    for metric,label in [('accuracy','Classification accuracy'),('macro_f1','Macro-F1')]:
        fig,ax=plt.subplots(figsize=(7.2,4.4))
        for split,offset in [('validation',-.08),('test',.08)]:
            selected=[next(r for r in rows if r['model']==m and r['split']==split) for m in methods]
            values=np.array([float(r[metric]) for r in selected])
            if not np.isfinite(values).all() or (values<0).any() or (values>1).any():raise ValueError('invalid classification metric')
            ax.scatter(values,np.arange(len(methods))+offset,label=split,s=22)
        ax.set_yticks(range(len(methods)),[m.replace('_',' ') for m in methods]);ax.invert_yaxis()
        ax.set_xlabel(label);ax.set_xlim(0,1);ax.legend(frameon=False)
        ax.set_title('Japanese Vowels: source-fitted affine reference\nMean LPC features + closed-form ridge; not HSE method results')
        ax.spines[['top','right']].set_visible(False);fig.tight_layout()
        for ext in ('svg','pdf','png'):fig.savefig(output/f'affine_{metric}.{ext}',dpi=300)
        plt.close(fig)
    print(f'CSV-only figures from {len(rows)} retained evaluation rows; no confidence interval asserted')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--csv',required=True);p.add_argument('--output-dir',required=True)
    a=p.parse_args();plot(a.csv,a.output_dir)

if __name__=='__main__':main()
