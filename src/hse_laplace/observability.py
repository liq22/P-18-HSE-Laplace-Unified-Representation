"""Observable, private, and unobserved modal subspaces."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ObservableDecomposition:
    """Orthogonal projectors for one acquisition domain."""

    shared: np.ndarray
    observed_private: np.ndarray
    unobserved: np.ndarray

    def validate(self, *, atol: float = 1e-8) -> None:
        projectors = (self.shared, self.observed_private, self.unobserved)
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
    """Compute the spectral projector of the noise-weighted Gramian.

    ``A.T @ inv(Sigma) @ A`` is formed with a linear solve.  Singular noise
    covariance is rejected because it changes the statistical model.
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
        whitened = np.linalg.solve(covariance, operator)
    except np.linalg.LinAlgError as exc:
        raise ValueError("noise_covariance must be non-singular") from exc
    gramian = operator.T @ whitened
    gramian = 0.5 * (gramian + gramian.T)
    eigenvalues, eigenvectors = np.linalg.eigh(gramian)
    selected = eigenvalues >= threshold
    if not np.any(selected):
        return np.zeros_like(gramian)
    basis = eigenvectors[:, selected]
    return basis @ basis.T


def _shared_projector(
    observable_projectors: list[np.ndarray], *, atol: float
) -> np.ndarray:
    if not observable_projectors:
        raise ValueError("at least one observable projector is required")
    dimension = observable_projectors[0].shape[0]
    if any(projector.shape != (dimension, dimension) for projector in observable_projectors):
        raise ValueError("all observable projectors must be square and equally sized")
    for projector in observable_projectors:
        if not np.allclose(projector, projector.T, atol=atol):
            raise ValueError("observable projectors must be symmetric")
        if not np.allclose(projector @ projector, projector, atol=atol):
            raise ValueError("observable projectors must be idempotent")

    summed = sum(observable_projectors)
    eigenvalues, eigenvectors = np.linalg.eigh(0.5 * (summed + summed.T))
    selected = np.isclose(eigenvalues, len(observable_projectors), atol=atol)
    if not np.any(selected):
        return np.zeros((dimension, dimension), dtype=float)
    basis = eigenvectors[:, selected]
    return basis @ basis.T


def shared_private_unobserved(
    observable_projectors: list[np.ndarray],
    domain_index: int,
    *,
    atol: float = 1e-8,
) -> ObservableDecomposition:
    """Return the unique orthogonal decomposition for one source domain."""
    if not 0 <= domain_index < len(observable_projectors):
        raise IndexError("domain_index is outside observable_projectors")
    shared = _shared_projector(observable_projectors, atol=atol)
    observed = np.asarray(observable_projectors[domain_index], dtype=float)
    dimension = observed.shape[0]
    private = observed - shared
    private = 0.5 * (private + private.T)
    unobserved = np.eye(dimension) - observed
    decomposition = ObservableDecomposition(
        shared=shared,
        observed_private=private,
        unobserved=unobserved,
    )
    decomposition.validate(atol=max(atol, 1e-7))
    return decomposition
