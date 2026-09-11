"""Fixed-partition posterior controls; analytical diagnostics, not learned HSE.

All arms see the same acquisition and prior. Fixed partitions are shared in the
protocol, so the statistic counts exclude a transmitted layout identifier.
"""
import argparse
import csv
from pathlib import Path
import numpy as np


def spd(value):
    value = np.asarray(value, dtype=float)
    if value.ndim != 2 or value.shape[0] != value.shape[1] or not np.isfinite(value).all():
        raise ValueError('expected a finite square matrix')
    if not np.allclose(value, value.T, rtol=0, atol=1e-10):
        raise ValueError('matrix must be symmetric')
    np.linalg.cholesky(value)
    return value


def blocks(matrix, groups):
    matrix = spd(matrix)
    indices = [i for group in groups for i in group]
    if sorted(indices) != list(range(len(matrix))):
        raise ValueError('groups must partition coordinates exactly once')
    result = np.zeros_like(matrix)
    for group in groups:
        result[np.ix_(group, group)] = matrix[np.ix_(group, group)]
    return result


def kl(mean, covariance, other_mean, other_covariance):
    s, v = spd(covariance), spd(other_covariance)
    delta = np.asarray(other_mean)-np.asarray(mean)
    return float(.5*(np.trace(np.linalg.solve(v, s))-len(s)
        + delta @ np.linalg.solve(v, delta)
        + np.linalg.slogdet(v)[1]-np.linalg.slogdet(s)[1]))


def bounds(precision, natural, approximate_precision, approximate_natural):
    """Two valid bounds and independent direct KL; full-precision oracle cost."""
    q, qt = spd(precision), spd(approximate_precision)
    h, ht = np.asarray(natural), np.asarray(approximate_natural)
    if q.shape != qt.shape or h.shape != (len(q),) or ht.shape != h.shape:
        raise ValueError('natural parameters and precision dimensions must agree')
    if not np.isfinite(h).all() or not np.isfinite(ht).all():
        raise ValueError('natural parameters must be finite')
    lam, u = np.linalg.eigh(q)
    invroot = (u*lam**-.5)@u.T
    e = invroot@(qt-q)@invroot
    w = invroot@(ht-h)-e@(invroot@h)
    kappa = float(np.linalg.eigvalsh(np.eye(len(q))+e).min())
    if kappa <= 0:
        raise ValueError('normalized precision is not positive definite')
    fro2 = float(np.sum(e*e))
    mean_bound = float(w@w)/(2*kappa)
    old = fro2/(4*min(1., kappa)**2)+mean_bound
    tight = fro2/(4*min(1., kappa))+mean_bound
    exact = kl(np.linalg.solve(q,h), np.linalg.solve(q,np.eye(len(q))),
               np.linalg.solve(qt,ht), np.linalg.solve(qt,np.eye(len(qt))))
    return {'exact_kl': exact, 'old_bound': old, 'tight_bound': tight,
            'kappa': kappa, 'mean_residual_squared': float(w@w)}


def lowrank_covariance(prior_covariance, posterior_covariance, rank):
    """Dense oracle of prior-whitened negative-update approximation.

    This evaluates the Spantini approximation family, not its matrix-free
    large-scale algorithm. Full posterior computation is charged to the encoder.
    """
    s0, s = spd(prior_covariance), spd(posterior_covariance)
    if s0.shape != s.shape or not 0 <= rank <= len(s):
        raise ValueError('invalid covariance shape or rank')
    lam, u = np.linalg.eigh(s0)
    root, invroot = (u*np.sqrt(lam))@u.T, (u/np.sqrt(lam))@u.T
    reduction = invroot@(s0-s)@invroot
    delta, v = np.linalg.eigh((reduction+reduction.T)/2)
    if delta.min() < -1e-10 or delta.max() >= 1:
        raise ValueError('requires a positive-semidefinite prior-to-posterior reduction')
    selected = np.argsort(delta)[::-1][:rank]
    if len(selected) and np.any(delta[selected] < 0):
        raise ValueError('selected reduction is negative at numerical precision')
    factor = root@v[:,selected]*np.sqrt(delta[selected])
    return spd(s0-factor@factor.T)


def representations(j, h, groups):
    """Unit-prior controls. Product-optimality requires block-diagonal prior."""
    j = spd(j)
    m = len(j)
    q = np.eye(m)+j
    s = np.linalg.solve(q,np.eye(m))
    mu = np.linalg.solve(q,h)
    qg = np.eye(m)+blocks(j,groups)
    sg = np.linalg.solve(qg,np.eye(m))
    iso = np.zeros_like(j)
    for i in range(0,m,2):
        iso[i:i+2,i:i+2] = np.trace(j[i:i+2,i:i+2])/2*np.eye(2)
    si = np.linalg.solve(np.eye(m)+iso,np.eye(m))
    budget = m+sum(len(g)*(len(g)+1)//2 for g in groups)
    rank = min(m,(budget-m)//m)
    return {
        'full': (mu,s,m+m*(m+1)//2),
        'natural_blocks': (sg@h,sg,budget),
        'mean_precision': (mu,sg,budget),
        'moment_blocks': (mu,blocks(s,groups),budget),
        'trace_isotropic': (si@h,si,m+m//2),
        'prior_lowrank': (mu,lowrank_covariance(np.eye(m),s,rank),m+m*rank),
    }


def denoiser_gap(mean, covariance, other_mean, other_covariance, alpha, sigma):
    """Exact epsilon-predictor discrepancy under the true Gaussian noisy target.

    This is not a Bayes compression gap unless the other law is the true
    compressed conditional. The target projection is applied before this call.
    """
    if sigma <= 0 or alpha < 0:
        raise ValueError('sigma must be positive and alpha nonnegative')
    v, w = spd(covariance), spd(other_covariance)
    m = alpha**2*v+sigma**2*np.eye(len(v))
    n = alpha**2*w+sigma**2*np.eye(len(w))
    difference = np.linalg.solve(m,np.eye(len(m)))-np.linalg.solve(n,np.eye(len(n)))
    delta = np.asarray(other_mean)-np.asarray(mean)
    mean_term = np.linalg.solve(n,delta)
    return float(sigma**2*(np.trace(difference@m@difference.T)
                          + alpha**2*(mean_term@mean_term)))


def benchmark(output, events=128):
    from .core import sampled_design
    designs = [('reviewer_six_dimensional', None, .2*np.eye(6)+2*np.ones((6,6)),
                ((0,1,2,3),(4,5)), 0, 0, 'coefficient', 0)]
    for protocol in ['fixed_points','fixed_duration']:
        for rate in [1024,2048]:
            points = 16 if protocol == 'fixed_points' else int(16*rate/1024)
            t,a = sampled_design(rate,.25,30.,patch_points=points)
            designs.append((f'{protocol}_{rate}',a,a.T@a/.25,
                            ((0,1),(2,3)),rate,len(t),protocol,points))
    rows = []
    for name,a,j,groups,rate,n,protocol,points in designs:
        m=len(j)
        if a is None:
            hs = np.array([[1.,-.3,.4,.7,-.8,.2]])
        else:
            rng=np.random.default_rng(420)
            beta=rng.normal(size=(events,m))
            x=beta@a.T+.5*rng.normal(size=(events,len(a)))
            hs=x@a/.25
        l=np.eye(m)[-2:]
        q=np.eye(m)+j
        s=np.linalg.solve(q,np.eye(m))
        values={key:[] for key in representations(j,hs[0],groups)}
        target_values={key:[] for key in values}
        denoising={key:[] for key in values}
        for h in hs:
            arms=representations(j,h,groups)
            mu=arms['full'][0]
            for key,(ma,sa,count) in arms.items():
                values[key].append(kl(mu,s,ma,sa))
                target_values[key].append(kl(l@mu,l@s@l.T,l@ma,l@sa@l.T))
                denoising[key].append(denoiser_gap(l@mu,l@s@l.T,l@ma,l@sa@l.T,.8,.6))
            if kl(mu,s,arms['moment_blocks'][0],arms['moment_blocks'][1]) > kl(mu,s,arms['natural_blocks'][0],arms['natural_blocks'][1])+1e-9:
                raise AssertionError('product projection inequality failed')
        sz=l@s@l.T
        sz0=l@np.eye(m)@l.T
        szr=lowrank_covariance(sz0,sz,1)
        target_goal_kl=kl(np.zeros(2),sz,np.zeros(2),szr)
        for key,(ma,sa,count) in arms.items():
            rows.append({'design':name,'protocol':protocol,'rate_hz':rate,
                'patch_points':points,'observations':n,'events':len(hs),
                'method':key,'statistic_scalars':count,'layout_scalars':0,
                'coefficient_kl':float(np.mean(values[key])),
                'target_kl':float(np.mean(target_values[key])),
                'epsilon_gap_alpha08':float(np.mean(denoising[key])),
                'goal_only_rank1_target_kl':target_goal_kl,
                'goal_only_rank1_scalars':4,'goal_only_exact_target_kl':0.,
                'goal_only_exact_scalars':5})
    output.mkdir(parents=True,exist_ok=True)
    with (output/'parameterization.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(f'{len(designs)} stated designs; {len(rows)} rows; analytical controls only')
    return rows


def plot(csv_file, output):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    mpl.rcParams.update({'svg.fonttype':'none','pdf.fonttype':42,'font.size':8,
                         'axes.spines.top':False,'axes.spines.right':False})
    with csv_file.open(newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    if not rows:
        raise ValueError('input CSV is empty')
    output.mkdir(parents=True,exist_ok=True)
    for design in dict.fromkeys(r['design'] for r in rows):
        subset=[r for r in rows if r['design']==design]
        fig,ax=plt.subplots(figsize=(6.6,3.2))
        pos=np.arange(len(subset))
        ax.plot(pos,[float(r['coefficient_kl']) for r in subset],'o',label='Coefficient posterior')
        ax.plot(pos,[float(r['target_kl']) for r in subset],'s',label='Fixed target: final mode')
        ax.set_xticks(pos,[r['method'].replace('_','\n') for r in subset])
        ax.set_ylabel('Forward KL (nats)');ax.set_title(design.replace('_',' '))
        ax.legend();fig.tight_layout()
        for ext in ['svg','pdf','png']:
            fig.savefig(output/f'{design}.{ext}',dpi=300)
        plt.close(fig)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--plot-only',type=Path)
    parser.add_argument('--events',type=int,default=128)
    args=parser.parse_args()
    if args.events<1:
        parser.error('--events must be positive')
    if args.plot_only is not None:
        plot(args.plot_only,args.output_dir)
    else:
        benchmark(args.output_dir,args.events)

if __name__=='__main__':
    main()
