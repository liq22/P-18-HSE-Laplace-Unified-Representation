"""Selection of FIXED predictors; no assertion about a jointly retrained fusion.

Rows are acquisition strata; columns are frozen prediction arms. All losses are
smaller-is-better. The population weighting is explicit, never inferred from
unequal window counts. This module has no PHMFactory imports.
"""
from __future__ import annotations
import numpy as np


def weighted_headroom(risks, probability):
    risk = np.asarray(risks, dtype=float)
    p = np.asarray(probability, dtype=float)
    if risk.ndim != 2 or min(risk.shape) < 1 or p.shape != (len(risk),):
        raise ValueError('expected risks[conditions,arms] and probability[conditions]')
    if not np.isfinite(risk).all() or not np.isfinite(p).all() or (p < 0).any() or not np.isclose(p.sum(), 1):
        raise ValueError('finite risks and nonnegative probabilities summing to one required')
    return float(np.min(p @ risk) - p @ np.min(risk, axis=1))


def select_fixed_arms(source_risk, probability):
    risk = np.asarray(source_risk, dtype=float)
    weighted_headroom(risk, probability)
    # Stable ties choose the earlier declared arm. Only source rows enter here.
    return int(np.argmin(np.asarray(probability) @ risk)), np.argmin(risk, axis=1)


def fit_static_squared(predictions, targets):
    """Least-squares constant blend of two fixed predictions, on source only."""
    pred, y = np.asarray(predictions, float), np.asarray(targets, float)
    if pred.ndim != 2 or pred.shape[1] != 2 or y.shape != (len(pred),) or len(y) == 0:
        raise ValueError('expected predictions[N,2] and targets[N]')
    if not np.isfinite(pred).all() or not np.isfinite(y).all():
        raise ValueError('nonfinite prediction/target')
    delta = pred[:, 1] - pred[:, 0]
    denominator = float(delta @ delta)
    # Identical predictions make alpha unidentifiable; alpha=0 is an exact tie.
    return 0.0 if denominator == 0 else float(np.clip(delta @ (y-pred[:, 0]) / denominator, 0, 1))


def conditional_regret(risk, selected, probability):
    risk, selected, p = np.asarray(risk, float), np.asarray(selected), np.asarray(probability, float)
    weighted_headroom(risk, p)
    if selected.shape != (len(risk),) or selected.dtype.kind not in 'iu' or not np.isin(selected, range(risk.shape[1])).all():
        raise ValueError('one valid selected arm per condition required')
    return float(p @ (risk[np.arange(len(risk)), selected] - risk.min(axis=1)))
