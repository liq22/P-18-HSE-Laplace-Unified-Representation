"""Sampled known-pole diagnostics; not a trained HSE or LLapDiff.

Sparse headers include their pattern identifier. The full-statistic oracle has
more storage and is not presented as a matched-budget deployment method.
"""
import numpy as np

PATTERNS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def _spd(matrix):
    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or not np.isfinite(matrix).all():
        raise ValueError('matrix must be finite and square')
    if not np.allclose(matrix, matrix.T, rtol=0, atol=1e-10):
        raise ValueError('matrix must be symmetric')
    np.linalg.cholesky(matrix)
    return matrix


def gaussian_kl(mean, covariance, other_mean, other_covariance):
    """KL(N(mean,covariance) || N(other_mean,other_covariance)), in nats."""
    p, q = _spd(covariance), _spd(other_covariance)
    delta = np.asarray(other_mean) - np.asarray(mean)
    return float(.5 * (np.trace(np.linalg.solve(q, p)) - p.shape[0]
                       + delta @ np.linalg.solve(q, delta)
                       + np.linalg.slogdet(q)[1] - np.linalg.slogdet(p)[1]))


def precision_certificate(precision, natural, approximate_precision, approximate_natural):
    """Exact Gaussian KL and general SPD perturbation bound (Theory 12).

    This uses full oracle information for evaluation; it is not an additional
    hidden feature sent to the decoder.
    """
    p, q = _spd(precision), _spd(approximate_precision)
    eta, eta_q = np.asarray(natural, dtype=float), np.asarray(approximate_natural, dtype=float)
    if p.shape != q.shape or eta.shape != (len(p),) or eta_q.shape != eta.shape:
        raise ValueError('precision and natural-parameter dimensions must agree')
    if not np.isfinite(eta).all() or not np.isfinite(eta_q).all():
        raise ValueError('natural parameters must be finite')
    eig, vectors = np.linalg.eigh(p)
    invroot = (vectors * eig**-.5) @ vectors.T
    e = invroot @ (q-p) @ invroot
    residual = invroot @ (eta_q-eta)
    v = invroot @ eta
    eig_e = np.linalg.eigvalsh(e)
    kappa = float(1+eig_e.min())
    if kappa <= 0:
        raise ValueError('normalized approximate precision is not positive definite')
    w = residual-e@v
    spectral = float(np.sum(eig_e-np.log1p(eig_e)))
    exact = .5 * (spectral + w @ np.linalg.solve(np.eye(len(p))+e, w))
    bound = np.linalg.norm(e, 'fro')**2/(4*min(1., kappa)**2) + (w@w)/(2*kappa)
    return {'kl_nats': float(exact), 'bound_nats': float(bound),
            'relative_precision_norm': float(np.max(np.abs(eig_e))), 'kappa': kappa}


def retained_matrix(information, pattern):
    """Keep a disjoint matching, preserving PSD through principal blocks."""
    j = np.asarray(information)
    if j.shape != (4, 4):
        raise ValueError('diagnostic requires two modes / four coefficients')
    kept = np.diag(np.diag(j))
    if pattern == -1:
        return kept
    if pattern not in range(len(PATTERNS)):
        raise ValueError('pattern must be -1 (diagonal) or 0,1,2')
    for i, k in PATTERNS[pattern]:
        kept[i, k] = kept[k, i] = j[i, k]
    return kept


def encode_header(score, information, pattern):
    """4 score + 4 diagonal + 2 coupling values + 1 pattern code = 11 scalars."""
    b = np.asarray(score, dtype=float)
    if b.shape != (4,) or not np.isfinite(b).all():
        raise ValueError('score must be finite [4]')
    kept = retained_matrix(information, pattern)
    pairs = PATTERNS[pattern] if pattern >= 0 else PATTERNS[0]
    return np.r_[b, np.diag(kept), [kept[i, j] for i, j in pairs], float(pattern)]


def decode_header(header):
    """Decode without the hidden full information matrix or acquisition ID."""
    h = np.asarray(header, dtype=float)
    if h.shape != (11,) or not np.isfinite(h).all():
        raise ValueError('header must be finite [11]')
    pattern = int(h[-1])
    if pattern != h[-1] or pattern not in (-1, 0, 1, 2):
        raise ValueError('invalid pattern code')
    j = np.diag(h[4:8])
    if pattern >= 0:
        for value, (i, k) in zip(h[8:10], PATTERNS[pattern]):
            j[i, k] = j[k, i] = value
    elif np.any(h[8:10] != 0):
        raise ValueError('diagonal header must contain zero coupling slots')
    return h[:4].copy(), j


def expected_plugin_kl(information, retained, prior_covariance=None):
    """Prior-predictive expected KL for zero-mean Gaussian prior (Theory 13).

    Metadata-only criterion: no hidden coefficient, task label or observed value.
    This measures plug-in posterior error, not compressed-posterior information.
    """
    j = np.asarray(information)
    s0 = np.eye(len(j)) if prior_covariance is None else _spd(prior_covariance)
    prior_precision = np.linalg.solve(s0, np.eye(len(j)))
    p, q = prior_precision+j, prior_precision+retained
    _spd(p); _spd(q)
    s = np.linalg.solve(p, np.eye(len(j)))
    transform = np.linalg.solve(q, p)-np.eye(len(j))
    covariance_term = np.trace(q@s)-len(j)+np.linalg.slogdet(p)[1]-np.linalg.slogdet(q)[1]
    mean_term = np.trace(q@transform@(s0-s)@transform.T)
    return float(.5*(covariance_term+mean_term))


def choose_pattern(information, criterion='posterior_risk'):
    if criterion == 'posterior_risk':
        costs = [expected_plugin_kl(information, retained_matrix(information, k)) for k in range(3)]
        return int(np.argmin(costs))
    if criterion == 'magnitude':
        energy = [sum(information[i,j]**2 for i,j in pairs) for pairs in PATTERNS]
        return int(np.argmax(energy))
    raise ValueError('criterion must be posterior_risk or magnitude')


def sampled_design(rate_hz, duration_s, separation_hz, sampling='regular', patch_points=16, tokens=4):
    """Direct waveform sampling with fixed P,K; not a hardware resampling test.

    Frequencies are in Hz; exponent uses 2*pi*f*t. Missing observations are
    removed before the likelihood is formed, not interpolated or refilled.
    """
    if rate_hz <= 0 or duration_s <= 0 or separation_hz <= 0:
        raise ValueError('rate, duration and separation must be positive')
    if patch_points < 2 or tokens < 1:
        raise ValueError('invalid patch budget')
    n = int(np.floor(rate_hz*duration_s))
    if n < patch_points*tokens:
        raise ValueError('window is too short for non-overlapping declared patches')
    frequencies = np.array([100., 100.+separation_hz])
    if frequencies.max() >= rate_hz/2:
        raise ValueError('this experiment keeps nominal modes below Nyquist')
    starts = np.linspace(0, n-patch_points, tokens).astype(int)
    indices = np.concatenate([np.arange(s, s+patch_points) for s in starts])
    if len(np.unique(indices)) != len(indices):
        raise ValueError('duplicate measurements cannot be counted as independent evidence')
    times = indices/rate_hz
    if sampling == 'jitter':
        times = times + .18/rate_hz * np.sin(1.7*indices)
    elif sampling == 'block_missing':
        times = times[~((times > .28*duration_s) & (times < .60*duration_s))]
    elif sampling != 'regular':
        raise ValueError('sampling must be regular, jitter or block_missing')
    columns = []
    for frequency, damping in zip(frequencies, [12., 18.]):
        envelope = np.exp(-damping*times)
        columns.extend([envelope*np.cos(2*np.pi*frequency*times),
                        envelope*np.sin(2*np.pi*frequency*times)])
    return times, np.column_stack(columns)
