"""Plot only observed selection CSVs; seeds are shown, not pseudo-replicated CIs."""
import argparse
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def plot(path, output):
    with Path(path).open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    required={'scenario','calibration_groups','seed','best_lower_bound','test_net_improvement'}
    if not rows or required-set(rows[0]): raise ValueError('selection summary columns required')
    keys=[(r['scenario'],r['calibration_groups'],r['seed']) for r in rows]
    if len(set(keys))!=len(keys): raise ValueError('duplicate scenario/calibration/seed')
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'svg.fonttype':'none','pdf.fonttype':42,'font.size':9})
    cells=sorted({(r['scenario'],int(r['calibration_groups'])) for r in rows})
    for column,label,name in [('best_lower_bound','Simultaneous net-gain lower bound','selection_bounds'),
                              ('test_net_improvement','Observed selected-policy net gain','selection_test_gain')]:
        fig,ax=plt.subplots(figsize=(7.2,4.5))
        for i,(scenario,n) in enumerate(cells):
            subset=sorted([r for r in rows if r['scenario']==scenario and int(r['calibration_groups'])==n],key=lambda r:int(r['seed']))
            v=np.asarray([float(r[column]) for r in subset])
            if not np.isfinite(v).all(): raise ValueError('nonfinite observed value')
            ax.scatter(v,i+np.linspace(-.10,.10,len(v)),s=20)
        ax.axvline(0,linewidth=.8)
        if column=='best_lower_bound':
            ax.axvline(.01,linestyle='--',linewidth=.8,label='Declared margin 0.01');ax.legend(frameon=False)
        ax.set_yticks(range(len(cells)),[f"{c.replace('_',' ')} | n={n}" for c,n in cells])
        ax.set_xlabel(label);ax.invert_yaxis();ax.spines[['top','right']].set_visible(False)
        ax.set_title('Observed policies after independent calibration\nThree simulation seeds per setting (descriptive)')
        fig.tight_layout()
        for ext in ['svg','pdf','png']: fig.savefig(output/f'{name}.{ext}',dpi=300)
        plt.close(fig)
    print(f'Plotted all {len(rows)} observed summary rows into two figures')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--csv',required=True);p.add_argument('--output-dir',required=True)
    args=p.parse_args();plot(args.csv,args.output_dir)

if __name__=='__main__':main()
