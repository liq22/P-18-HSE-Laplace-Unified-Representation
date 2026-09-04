"""Canonical Laplace-posterior representation used by the analytic oracle."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class CanonicalLaplacePosterior:
    """Gaussian posterior in one fixed canonical modal coordinate system."""

    mean: np.ndarray
    covariance: np.ndarray

    def validate(self) -> None:
        mean = np.asarray(self.mean, dtype=float)
        covariance = np.asarray(self.covariance, dtype=float)
        if mean.ndim != 1:
            raise ValueError("mean must be one-dimensional")
        if covariance.shape != (mean.size, mean.size):
            raise ValueError("covariance shape must match the modal dimension")
        if np.any(~np.isfinite(mean)) or np.any(~np.isfinite(covariance)):
            raise ValueError("posterior parameters must be finite")
        if not np.allclose(covariance, covariance.T, atol=1e-10):
            raise ValueError("covariance must be symmetric")
        try:
            np.linalg.cholesky(covariance)
        except np.linalg.LinAlgError as exc:
            raise ValueError("covariance must be positive definite") from exc

    def directional_variance(self, direction: np.ndarray) -> float:
        self.validate()
        vector = np.asarray(direction, dtype=float)
        if vector.shape != self.mean.shape:
            raise ValueError("direction shape must match the modal dimension")
        norm = np.linalg.norm(vector)
        if norm == 0:
            raise ValueError("direction must be non-zero")
        unit = vector / norm
        return float(unit @ self.covariance @ unit)

    def entropy(self) -> float:
        """Differential entropy of the Gaussian posterior."""
        self.validate()
        dimension = self.mean.size
        sign, logdet = np.linalg.slogdet(self.covariance)
        if sign <= 0:
            raise ValueError("covariance determinant must be positive")
        return float(0.5 * (dimension * np.log(2.0 * np.pi * np.e) + logdet))
