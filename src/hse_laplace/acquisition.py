"""Linear-Gaussian acquisition oracle for HSE-conditioned Laplace posteriors."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .representation import CanonicalLaplacePosterior


@dataclass(frozen=True)
class GaussianInformation:
    """Fixed-dimensional sufficient statistics for a canonical modal state."""

    score: np.ndarray
    information: np.ndarray

    def validate(self) -> None:
        score = np.asarray(self.score, dtype=float)
        information = np.asarray(self.information, dtype=float)
        if score.ndim != 1:
            raise ValueError("score must be one-dimensional")
        if information.shape != (score.size, score.size):
            raise ValueError("information shape must match the modal dimension")
        if np.any(~np.isfinite(score)) or np.any(~np.isfinite(information)):
            raise ValueError("information statistics must be finite")
        if not np.allclose(information, information.T, atol=1e-10):
            raise ValueError("information matrix must be symmetric")
        if np.linalg.eigvalsh(information).min() < -1e-10:
            raise ValueError("information matrix must be positive semidefinite")


def _require_spd(matrix: np.ndarray, name: str) -> np.ndarray:
    array = np.asarray(matrix, dtype=float)
    if array.ndim != 2 or array.shape[0] != array.shape[1]:
        raise ValueError(f"{name} must be square")
    if np.any(~np.isfinite(array)):
        raise ValueError(f"{name} must be finite")
    if not np.allclose(array, array.T, atol=1e-10):
        raise ValueError(f"{name} must be symmetric")
    try:
        return np.linalg.cholesky(array)
    except np.linalg.LinAlgError as exc:
        raise ValueError(f"{name} must be positive definite") from exc


def gaussian_information_statistics(
    observation_operator: np.ndarray,
    noise_covariance: np.ndarray,
    observation: np.ndarray,
) -> GaussianInformation:
    """Return ``b=A^T R^-1 x`` and ``J=A^T R^-1 A``.

    The observation length may vary between acquisition domains. The score and
    information matrix depend only on the canonical modal dimension.
    """
    operator = np.asarray(observation_operator, dtype=float)
    observation = np.asarray(observation, dtype=float)
    if operator.ndim != 2:
        raise ValueError("observation_operator must be two-dimensional")
    if observation.shape != (operator.shape[0],):
        raise ValueError("observation length must match observation_operator rows")
    if np.any(~np.isfinite(operator)) or np.any(~np.isfinite(observation)):
        raise ValueError("operator and observation must be finite")
    chol = _require_spd(noise_covariance, "noise_covariance")
    if chol.shape[0] != operator.shape[0]:
        raise ValueError("noise_covariance size must match observation length")

    whitened_operator = np.linalg.solve(chol, operator)
    whitened_observation = np.linalg.solve(chol, observation)
    information = whitened_operator.T @ whitened_operator
    information = 0.5 * (information + information.T)
    score = whitened_operator.T @ whitened_observation
    result = GaussianInformation(score=score, information=information)
    result.validate()
    return result


def gaussian_posterior(
    prior_mean: np.ndarray,
    prior_covariance: np.ndarray,
    statistics: GaussianInformation,
) -> CanonicalLaplacePosterior:
    """Return the exact canonical posterior under a Gaussian prior."""
    statistics.validate()
    mean = np.asarray(prior_mean, dtype=float)
    if mean.shape != statistics.score.shape:
        raise ValueError("prior_mean shape must match the modal dimension")
    _require_spd(prior_covariance, "prior_covariance")
    prior_covariance = np.asarray(prior_covariance, dtype=float)
    identity = np.eye(mean.size)
    prior_precision = np.linalg.solve(prior_covariance, identity)
    posterior_precision = prior_precision + statistics.information
    _require_spd(posterior_precision, "posterior_precision")
    natural_parameter = prior_precision @ mean + statistics.score
    posterior_mean = np.linalg.solve(posterior_precision, natural_parameter)
    posterior_covariance = np.linalg.solve(posterior_precision, identity)
    posterior_covariance = 0.5 * (posterior_covariance + posterior_covariance.T)
    posterior = CanonicalLaplacePosterior(
        mean=posterior_mean,
        covariance=posterior_covariance,
    )
    posterior.validate()
    return posterior


def loewner_margin(larger: np.ndarray, smaller: np.ndarray) -> float:
    """Return the smallest eigenvalue of ``larger - smaller``."""
    larger = np.asarray(larger, dtype=float)
    smaller = np.asarray(smaller, dtype=float)
    if larger.shape != smaller.shape or larger.ndim != 2:
        raise ValueError("both matrices must have the same two-dimensional shape")
    difference = 0.5 * ((larger - smaller) + (larger - smaller).T)
    if np.any(~np.isfinite(difference)):
        raise ValueError("matrix difference must be finite")
    return float(np.linalg.eigvalsh(difference).min())
