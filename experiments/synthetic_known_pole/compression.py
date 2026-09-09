"""Exact compressed-condition oracle for a finite family of acquisitions.

Two fixed damped modes have four cosine/sine coefficients. This module studies
linear coefficient measurements, not sampled hardware or a learned HSE.
"""
from dataclasses import dataclass
from math import erf, sqrt
import numpy as np


def _logsumexp(x: np.ndarray, axis: int = -1) -> np.ndarray:
    maximum = np.max(x, axis=axis, keepdims=True)
    return np.squeeze(maximum + np.log(np.exp(x - maximum).sum(axis=axis, keepdims=True)), axis)


def _lognormal(x: np.ndarray, mean: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    """Log density; x/mean may contain a leading observation dimension."""
    chol = np.linalg.cholesky(covariance)
    residual = np.linalg.solve(chol, (x - mean).T).T
    return -.5 * (x.shape[-1] * np.log(2*np.pi)
                  + 2*np.log(np.diag(chol)).sum() + np.sum(residual**2, axis=-1))


def acquisition_family(cross: float, within: float = .6) -> np.ndarray:
    """J = 1.5 I + within*u*W + cross*v*X, u,v in {-1,1}."""
    if not np.isfinite([cross, within]).all() or cross < 0 or within < 0 or cross + within >= 1.5:
        raise ValueError('require nonnegative couplings with within + cross < 1.5')
    W = np.zeros((4, 4)); X = np.zeros((4, 4))
    W[0, 1] = W[1, 0] = W[2, 3] = W[3, 2] = 1
    X[0, 2] = X[2, 0] = X[1, 3] = X[3, 1] = 1
    return np.array([1.5*np.eye(4) + within*u*W + cross*v*X
                     for u in [-1, 1] for v in [-1, 1]])


def prior_parameters(name: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if name == 'gaussian':
        return np.ones(1), np.zeros((1, 4)), np.eye(4)[None]
    if name == 'mixture':
        mu = np.array([1., 0., -1., .5])
        return np.array([.5, .5]), np.stack([-mu, mu]), np.tile(.35*np.eye(4), (2, 1, 1))
    raise ValueError('prior must be gaussian or mixture')


def retained_information(J: np.ndarray, method: str) -> np.ndarray:
    if method == 'full':
        return J.copy()
    if method == 'diag':
        return np.diag(np.diag(J))
    if method == 'block':
        kept = np.zeros_like(J)
        kept[:2, :2], kept[2:, 2:] = J[:2, :2], J[2:, 2:]
        return kept
    raise ValueError('method must be full, diag or block')


def matching_designs(family: np.ndarray, retained: np.ndarray, method: str) -> np.ndarray:
    """Only retained information determines membership; no true-design input."""
    indices = [i for i, J in enumerate(family)
               if np.allclose(retained_information(J, method), retained, rtol=0, atol=1e-12)]
    if not indices:
        raise ValueError('retained information does not belong to the declared acquisition family')
    return np.array(indices, dtype=int)


@dataclass(frozen=True)
class ConditionalMixture:
    """Event-dependent weights/means and event-independent component covariances."""
    log_weights: np.ndarray  # [N, L]
    means: np.ndarray        # [N, L, 4]
    covariances: np.ndarray  # [L, 4, 4]

    def mean(self) -> np.ndarray:
        return np.einsum('nl,nlm->nm', np.exp(self.log_weights), self.means)

    def log_prob(self, values: np.ndarray) -> np.ndarray:
        parts = [_lognormal(values, self.means[:, j], covariance)
                 for j, covariance in enumerate(self.covariances)]
        return _logsumexp(np.stack(parts, axis=1) + self.log_weights)

    def marginal_cdf(self, values: np.ndarray) -> np.ndarray:
        """PIT for central marginal coverage; not a joint-coverage statistic."""
        z = (values[:, None, :] - self.means) / np.sqrt(np.diagonal(self.covariances, axis1=1, axis2=2))[None]
        cdf = .5 * (1 + np.fromiter((erf(x/sqrt(2)) for x in z.ravel()), float, z.size).reshape(z.shape))
        return np.einsum('nl,nlm->nm', np.exp(self.log_weights), cdf)

    def denoising_mean(self, noisy: np.ndarray, alpha: float, sigma: float) -> np.ndarray:
        """E[beta | noisy,b,retained] with the same independent diffusion noise."""
        if not np.isfinite([alpha, sigma]).all() or sigma <= 0:
            raise ValueError('alpha must be finite and sigma positive')
        masses, means = [], []
        for j, covariance in enumerate(self.covariances):
            predictive = alpha**2 * covariance + sigma**2*np.eye(4)
            gain = np.linalg.solve(predictive, alpha*covariance).T
            masses.append(self.log_weights[:, j] + _lognormal(noisy, alpha*self.means[:, j], predictive))
            means.append(self.means[:, j] + (noisy-alpha*self.means[:, j]) @ gain.T)
        logw = np.stack(masses, axis=1)
        logw -= _logsumexp(logw)[:, None]
        return np.einsum('nl,nlm->nm', np.exp(logw), np.stack(means, axis=1))


def conditional_posterior(b: np.ndarray, family: np.ndarray, design_indices: np.ndarray,
                          prior: tuple[np.ndarray, np.ndarray, np.ndarray]) -> ConditionalMixture:
    """Exact p(beta | b, retained J), using the implied design-mixture weights.

    Designs have a declared uniform prior independent of beta. Importantly,
    weights use p(b | design), not p(x | design) evaluated at the hidden x.
    """
    b = np.asarray(b, dtype=float)
    family = np.asarray(family, dtype=float)
    indices = np.asarray(design_indices)
    if b.ndim != 2 or b.shape[1] != 4 or not np.isfinite(b).all():
        raise ValueError('b must be finite [N,4]')
    if family.ndim != 3 or family.shape[1:] != (4, 4) or not np.isfinite(family).all():
        raise ValueError('family must be finite [D,4,4] information matrices')
    if (indices.ndim != 1 or indices.size == 0
            or not np.issubdtype(indices.dtype, np.integer)
            or np.any(indices < 0) or np.any(indices >= len(family))
            or np.unique(indices).size != indices.size):
        raise ValueError('design_indices must be a nonempty set of distinct integer indices')
    weights, prior_means, prior_covs = (np.asarray(value, dtype=float) for value in prior)
    if (weights.ndim != 1 or weights.size == 0
            or prior_means.shape != (weights.size, 4)
            or prior_covs.shape != (weights.size, 4, 4)):
        raise ValueError('prior weights, means and covariances must have matching component counts')
    if (not all(np.isfinite(value).all() for value in (weights, prior_means, prior_covs))
            or np.any(weights <= 0) or not np.isclose(weights.sum(), 1., rtol=0, atol=1e-12)):
        raise ValueError('prior must be finite with positive weights summing to one')
    # Duplicated designs or truncated priors silently change the declared joint law.
    for matrices in (family, prior_covs):
        if not np.allclose(matrices, matrices.swapaxes(-1, -2), rtol=0, atol=1e-12):
            raise ValueError('information and prior covariance matrices must be symmetric')
        np.linalg.cholesky(matrices)
    component_means, component_covs, log_masses = [], [], []
    for i in indices:
        J = family[i]
        for weight, mu, covariance in zip(weights, prior_means, prior_covs):
            precision = np.linalg.solve(covariance, np.eye(4))
            post_cov = np.linalg.solve(precision + J, np.eye(4))
            post_mean = (b + precision @ mu) @ post_cov.T
            b_mean, b_cov = J @ mu, J @ covariance @ J + J
            log_masses.append(np.log(weight/len(family)) + _lognormal(b, b_mean, b_cov))
            component_means.append(post_mean)
            component_covs.append(post_cov)
    logw = np.stack(log_masses, axis=1)
    logw -= _logsumexp(logw)[:, None]
    return ConditionalMixture(logw, np.stack(component_means, axis=1), np.stack(component_covs))


def paired_events(prior: tuple[np.ndarray, np.ndarray, np.ndarray], seed: int,
                  test_count: int, train_count: int = 256, validation_count: int = 128) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Assign splits first; latent_event_id=(seed, 'test', row) groups all views."""
    if test_count < 2:
        raise ValueError('test_count must be at least 2')
    total = train_count + validation_count + test_count
    split = np.array(['train']*train_count + ['validation']*validation_count + ['test']*test_count)
    rng = np.random.default_rng(seed)
    weights, means, covs = prior
    component = rng.choice(len(weights), total, p=weights)
    beta = means[component] + np.einsum('nij,nj->ni', np.linalg.cholesky(covs[component]), rng.normal(size=(total, 4)))
    # Noise is independent across designs, with the same beta shared by all views.
    observation_noise = rng.normal(size=(total, 4, 4))
    diffusion_noise = rng.normal(size=(total, 4, 4))
    return beta[split == 'test'], observation_noise[split == 'test'], diffusion_noise[split == 'test']


def evaluate_cell(prior_name: str, cross: float, seed: int, test_count: int,
                  alpha: float = .8, sigma: float = .6) -> dict[tuple[str, str], dict[str, np.ndarray]]:
    """Return event-level, design-averaged metrics; no fitting or hidden-index decoding."""
    family, prior = acquisition_family(cross), prior_parameters(prior_name)
    beta, noises, eps = paired_events(prior, seed, test_count)
    by_arm = {}
    for d, J in enumerate(family):
        A = np.linalg.cholesky(J).T
        observation = beta @ A.T + noises[:, d]
        b = observation @ A
        side_R = np.eye(A.shape[0])
        side_J = A.T @ np.linalg.solve(side_R, A)
        full_indices = matching_designs(family, side_J, 'full')
        full = conditional_posterior(b, family, full_indices, prior)
        full_lp = full.log_prob(beta)
        noisy = alpha*beta + sigma*eps[:, d]
        full_eps = (noisy - alpha*full.denoising_mean(noisy, alpha, sigma))/sigma
        for regime in ['coarse', 'full_operator']:
            for method in ['full', 'diag', 'block']:
                kept = retained_information(J, method)
                # Full side information is supplied equally to every arm.
                indices = full_indices if regime == 'full_operator' else matching_designs(family, kept, method)
                exact = conditional_posterior(b, family, indices, prior)
                comp_lp = exact.log_prob(beta)
                candidates = [(method + '_exact', exact)]
                if method != 'full':
                    plug_J = side_J if regime == 'full_operator' else kept
                    candidates.append((method + '_plugin', conditional_posterior(b, plug_J[None], np.array([0]), prior)))
                for name, posterior in candidates:
                    key = (regime, name)
                    lp = posterior.log_prob(beta)
                    mean = posterior.mean()
                    pit = posterior.marginal_cdf(beta)
                    predicted_eps = (noisy-alpha*posterior.denoising_mean(noisy, alpha, sigma))/sigma
                    metrics = {
                        'total_gap_nats': full_lp-lp,
                        'compression_nats': full_lp-comp_lp,
                        'fitting_nats': comp_lp-lp,
                        'mean_mse': np.mean((mean-beta)**2, axis=1),
                        'epsilon_predictor_gap': np.sum((full_eps-predicted_eps)**2, axis=1),
                    }
                    for level in [.5, .8, .9]:
                        metrics[f'coverage_{int(100*level)}'] = np.mean((pit >= (1-level)/2) & (pit <= (1+level)/2), axis=1)
                    if key not in by_arm:
                        by_arm[key] = {metric: values/len(family) for metric, values in metrics.items()}
                    else:
                        for metric, values in metrics.items():
                            by_arm[key][metric] += values/len(family)
    # A density log-ratio can be negative for one event; never clip it to zero.
    for (regime, name), metrics in by_arm.items():
        metrics['gain_over_diag_nats'] = by_arm[(regime, 'diag_exact')]['total_gap_nats'] - metrics['total_gap_nats']
        if not all(np.isfinite(values).all() for values in metrics.values()):
            raise ValueError(f'nonfinite result: {regime}/{name}')
        np.testing.assert_allclose(metrics['total_gap_nats'], metrics['compression_nats']+metrics['fitting_nats'], atol=1e-12)
    return by_arm
