"""Structural observability and four-way modal decomposition."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ObservableDecomposition:
    """Orthogonal projectors for one acquisition domain.

    ``recoverable_missing`` is hidden in the current domain but observable in at
    least one source domain. ``global_null`` is unobservable in every source
    domain and is excluded from data-driven recovery claims.
    """

    shared: np.ndarray
    observed_private: np.ndarray
    recoverable_missing: np.ndarray
    global_null: np.ndarray

    def validate(self, *, atol: float = 1e-8) -> None:
        projectors = (
            self.shared,
            self.observed_private,
            self.recoverable_missing,
            self.global_null,
        )
        shape = self.shared.shape
        if len(shape) != 2 or shape[0] != shape[1]:
            raise ValueError("projectors must be square")
        if any(projector.shape != shape for projector in projectors):
            raise ValueError("all projectors must have the same shape")
        identity = np.eye(shape[0])
        for projector in projectors:
            if not np.allclose(projector, projector.T, atol=atol):
                raise ValueError("projectors must be symmetric")
            if not np.allclose(projector @ projector, projector, atol=atol):
                raise ValueError("projectors must be idempotent")
        for left_index, left in enumerate(projectors):
            for right in projectors[left_index + 1 :]:
                if not np.allclose(left @ right, 0.0, atol=atol):
                    raise ValueError("projectors must be mutually orthogonal")
        if not np.allclose(sum(projectors), identity, atol=atol):
            raise ValueError("projectors must sum to the identity")


def observable_projector(
    observation_operator: np.ndarray,
    noise_covariance: np.ndarray,
    threshold: float,
) -> np.ndarray:
    """Return the spectral projector of the noise-weighted Gramian.

    The covariance must be symmetric positive definite. The function rejects an
    indefinite covariance instead of treating invertibility as sufficient.
    """
    operator = np.asarray(observation_operator, dtype=float)
    covariance = np.asarray(noise_covariance, dtype=float)
    if operator.ndim != 2:
        raise ValueError("observation_operator must be a matrix")
    if covariance.shape != (operator.shape[0], operator.shape[0]):
        raise ValueError("noise_covariance shape must match observation rows")
    if threshold <= 0 or not np.isfinite(threshold):
        raise ValueError("threshold must be finite and strictly positive")
    if not np.allclose(covariance, covariance.T):
        raise ValueError("noise_covariance must be symmetric")
    try:
        chol = np.linalg.cholesky(covariance)
    except np.linalg.LinAlgError as exc:
        raise ValueError("noise_covariance must be positive definite") from exc

    whitened_operator = np.linalg.solve(chol, operator)
    gramian = whitened_operator.T @ whitened_operator
    gramian = 0.5 * (gramian + gramian.T)
    eigenvalues, eigenvectors = np.linalg.eigh(gramian)
    selected = eigenvalues >= threshold
    if not np.any(selected):
        return np.zeros_like(gramian)
    basis = eigenvectors[:, selected]
    return basis @ basis.T


def soft_modal_observability(
    gramian_diagonal: np.ndarray,
    threshold: float,
    temperature: float,
) -> np.ndarray:
    """Return soft structural observability weights for fixed modal slots."""
    values = np.asarray(gramian_diagonal, dtype=float)
    if values.ndim != 1:
        raise ValueError("gramian_diagonal must be one-dimensional")
    if np.any(~np.isfinite(values)):
        raise ValueError("gramian_diagonal must be finite")
    if np.any(values < -1e-12):
        raise ValueError("Gramian diagonal entries must be non-negative")
    if threshold <= 0 or not np.isfinite(threshold):
        raise ValueError("threshold must be finite and strictly positive")
    if temperature <= 0 or not np.isfinite(temperature):
        raise ValueError("temperature must be finite and strictly positive")

    scaled = (values - threshold) / temperature
    positive = scaled >= 0
    weights = np.empty_like(scaled)
    weights[positive] = 1.0 / (1.0 + np.exp(-scaled[positive]))
    exp_scaled = np.exp(scaled[~positive])
    weights[~positive] = exp_scaled / (1.0 + exp_scaled)
    return weights


def _validate_observable_projectors(
    observable_projectors: list[np.ndarray], *, atol: float
) -> list[np.ndarray]:
    if not observable_projectors:
        raise ValueError("at least one observable projector is required")
    arrays = [np.asarray(projector, dtype=float) for projector in observable_projectors]
    dimension = arrays[0].shape[0]
    if any(projector.shape != (dimension, dimension) for projector in arrays):
        raise ValueError("all observable projectors must be square and equally sized")
    for projector in arrays:
        if not np.allclose(projector, projector.T, atol=atol):
            raise ValueError("observable projectors must be symmetric")
        if not np.allclose(projector @ projector, projector, atol=atol):
            raise ValueError("observable projectors must be idempotent")
    return arrays


def _intersection_projector(
    observable_projectors: list[np.ndarray], *, atol: float
) -> np.ndarray:
    arrays = _validate_observable_projectors(observable_projectors, atol=atol)
    dimension = arrays[0].shape[0]
    summed = sum(arrays)
    eigenvalues, eigenvectors = np.linalg.eigh(0.5 * (summed + summed.T))
    selected = np.isclose(eigenvalues, len(arrays), atol=atol)
    if not np.any(selected):
        return np.zeros((dimension, dimension), dtype=float)
    basis = eigenvectors[:, selected]
    return basis @ basis.T


def _union_projector(
    observable_projectors: list[np.ndarray], *, atol: float
) -> np.ndarray:
    arrays = _validate_observable_projectors(observable_projectors, atol=atol)
    dimension = arrays[0].shape[0]
    summed = sum(arrays)
    eigenvalues, eigenvectors = np.linalg.eigh(0.5 * (summed + summed.T))
    selected = eigenvalues > atol
    if not np.any(selected):
        return np.zeros((dimension, dimension), dtype=float)
    basis = eigenvectors[:, selected]
    return basis @ basis.T


def shared_private_missing_null(
    observable_projectors: list[np.ndarray],
    domain_index: int,
    *,
    atol: float = 1e-8,
) -> ObservableDecomposition:
    """Return the four-way source-supported decomposition for one domain."""
    arrays = _validate_observable_projectors(observable_projectors, atol=atol)
    if not 0 <= domain_index < len(arrays):
        raise IndexError("domain_index is outside observable_projectors")

    shared = _intersection_projector(arrays, atol=atol)
    union = _union_projector(arrays, atol=atol)
    observed = arrays[domain_index]
    dimension = observed.shape[0]

    private = 0.5 * ((observed - shared) + (observed - shared).T)
    missing = 0.5 * ((union - observed) + (union - observed).T)
    global_null = 0.5 * (
        (np.eye(dimension) - union) + (np.eye(dimension) - union).T
    )
    decomposition = ObservableDecomposition(
        shared=shared,
        observed_private=private,
        recoverable_missing=missing,
        global_null=global_null,
    )
    decomposition.validate(atol=max(atol, 1e-7))
    return decomposition
