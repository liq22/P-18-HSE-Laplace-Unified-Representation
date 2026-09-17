"""Same-dimensional affine controls with explicit ridge-penalty transport.

These controls test coordinate/regularization effects, not conditional moments.
All transforms are fitted on source-training features only. No rank truncation,
padding, hidden whitening floor, neural encoder or probability calibration.
"""
from __future__ import annotations
import numpy as np


def fit_coordinates(features, seed=0):
    x=np.asarray(features,dtype=np.float64)
    if x.ndim!=2 or len(x)<2 or x.shape[1]<1 or not np.isfinite(x).all():
        raise ValueError('finite source feature matrix [N,q] required')
    center=x.mean(axis=0); centered=x-center
    eigenvalues,basis=np.linalg.eigh(centered.T@centered/len(x))
    order=np.argsort(eigenvalues)[::-1]; eigenvalues=eigenvalues[order];basis=basis[:,order]
    # Full-q whitening is undefined outside the full-rank source case. A
    # truncated/floored alternative would be a separately declared experiment.
    if eigenvalues[-1]<=np.finfo(float).eps*x.shape[1]*eigenvalues[0]:
        raise ValueError('full-q whitening requires full-rank source covariance')
    orthogonal,_=np.linalg.qr(np.random.default_rng(seed).normal(size=(x.shape[1],x.shape[1])))
    return center, {'R':np.eye(x.shape[1]), 'PCA_R':basis,
                    'orthogonal_R':orthogonal, 'whitened_R':basis/np.sqrt(eigenvalues)}, eigenvalues


def ridge_fit(features, targets, center, transform, regularization, penalty='isotropic'):
    x=np.asarray(features,dtype=np.float64);y=np.asarray(targets,dtype=np.float64)
    a=np.asarray(transform,dtype=np.float64);c=np.asarray(center,dtype=np.float64)
    if x.ndim!=2 or y.ndim!=2 or len(x)!=len(y) or len(x)==0 or c.shape!=(x.shape[1],) or a.shape!=(x.shape[1],x.shape[1]):
        raise ValueError('expected paired X[N,q], Y[N,k] and same-q coordinates')
    if not all(np.isfinite(z).all() for z in [x,y,a,c]) or not np.isfinite(regularization) or regularization<=0:
        raise ValueError('finite inputs and positive declared ridge penalty required')
    if penalty not in ('isotropic','matched'):
        raise ValueError('penalty must be isotropic or matched')
    z=(x-c)@a;zmean=z.mean(axis=0);ymean=y.mean(axis=0)
    zc=z-zmean;yc=y-ymean
    metric=np.eye(x.shape[1]) if penalty=='isotropic' else a.T@a
    coefficient=np.linalg.solve(zc.T@zc/len(x)+regularization*metric,zc.T@yc/len(x))
    intercept=ymean-zmean@coefficient
    return coefficient,intercept


def predict(features, center, transform, coefficient, intercept):
    return (np.asarray(features,dtype=np.float64)-center)@transform@coefficient+intercept
