"""Plot saved sampled-window results without executing an experiment.

Figure logic follows the referenced nature-figure contract: one question per
figure, original values, readable physical size, uncertainty and editable text.
This script does not claim an external journal-format certification.
"""
import argparse
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

LABELS={'diag':'Diagonal precision','within':'Within-mode precision',
        'magnitude':'Magnitude-selected precision','risk_oracle':'Risk-selected precision',
        'moment_within':'Within-mode posterior moments','moment_best':'Selected posterior moments',
        'full':'Full posterior (larger header)'}


def read_rows(path):
    with Path(path).open(newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    if not rows or 'kl_nats' not in rows[0]:
        raise ValueError('expected sampled_summary.csv from sampled_conditioning.run')
    for row in rows:
        for field in ['design','kl_nats','kl_lo','kl_hi','coverage90','mean_bound_nats']:
            row[field]=float(row[field])
    return rows


def save(fig,path):
    # Keep dimensions fixed; text is real SVG/PDF text, not a raster screenshot.
    fig.savefig(path.with_suffix('.svg'))
    fig.savefig(path.with_suffix('.pdf'))
    fig.savefig(path.with_suffix('.png'),dpi=300)
    plt.close(fig)


def plot(source,output):
    rows=read_rows(source);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'sans-serif','font.size':8,'svg.fonttype':'none',
                         'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,
                         'axes.linewidth':.8,'legend.frameon':False})
    coarse=[r for r in rows if r['side_information']=='coarse']
    methods=list(dict.fromkeys(r['method'] for r in coarse))
    fig,ax=plt.subplots(figsize=(180/25.4,115/25.4),layout='constrained')
    for method in methods:
        data=sorted((r for r in coarse if r['method']==method),key=lambda r:r['design'])
        x=[r['design'] for r in data];y=[r['kl_nats'] for r in data]
        ax.plot(x,y,marker='.',markersize=4,linestyle='none',label=LABELS[method])
        ax.vlines(x,[r['kl_lo'] for r in data],[r['kl_hi'] for r in data],linewidth=.6)
    ax.set(xlabel='Declared acquisition design (all evaluated designs)',ylabel='Forward posterior KL (nats)',
           title='Fixed header storage: allocation and posterior parameterization')
    ax.set_yscale('symlog',linthresh=.01)
    ax.set_ylabel('Forward posterior KL (nats; symmetric-log scale)')
    ax.legend(fontsize=6,loc='upper center',bbox_to_anchor=(.5,-.19),ncol=2)
    save(fig,output/'sampled_distortion')
    fig,ax=plt.subplots(figsize=(180/25.4,105/25.4),layout='constrained')
    for method in methods:
        data=sorted((r for r in coarse if r['method']==method),key=lambda r:r['design'])
        ax.plot([r['design'] for r in data],[r['coverage90'] for r in data],'.-',linewidth=.8,label=LABELS[method])
    ax.axhline(.9,linestyle=':',linewidth=1)
    ax.set(xlabel='Declared acquisition design',ylabel='Central marginal 90% coverage',ylim=(0,1.03),
           title='Moment matching preserves marginals, not all joint information')
    ax.legend(fontsize=6,loc='upper center',bbox_to_anchor=(.5,-.18),ncol=2)
    save(fig,output/'sampled_coverage')
    fig,ax=plt.subplots(figsize=(120/25.4,105/25.4),layout='constrained')
    nonzero=[r for r in coarse if r['kl_nats']>1e-10]
    ax.scatter([r['kl_nats'] for r in nonzero],[r['mean_bound_nats'] for r in nonzero],s=12)
    maximum=max(r['mean_bound_nats'] for r in nonzero)
    ax.plot([0,maximum],[0,maximum],':',linewidth=1)
    ax.set(xlabel='Measured mean Gaussian KL (nats)',ylabel='Mean perturbation bound (nats)',
           title='Precision bound: validity and looseness')
    save(fig,output/'precision_bound')
    print(f'Read {len(rows)} rows; plotted all {len(coarse)} coarse-condition rows. Full-side zero controls remain in CSV.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args();plot(args.csv,args.output_dir)
