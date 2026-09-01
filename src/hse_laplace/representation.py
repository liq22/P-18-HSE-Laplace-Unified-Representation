"""Data object for a distribution-valued unified representation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class UnifiedRepresentation:
    """Finite representation of the blockwise posterior measure.

    The Monte Carlo axis of ``unobserved_private_samples`` is explicit.  A
    posterior mean is not silently substituted for a posterior distribution.
    """

    shared_canonical: np.ndarray
    observed_private: np.ndarray
    unobserved_private_samples: np.ndarray
    observability_mask: np.ndarray

    def validate(self) -> None:
        shared = np.asarray(self.shared_canonical, dtype=float)
        private = np.asarray(self.observed_private, dtype=float)
        samples = np.asarray(self.unobserved_private_samples, dtype=float)
        mask = np.asarray(self.observability_mask)
        if shared.ndim != 1 or private.ndim != 1:
            raise ValueError("shared and observed-private coordinates must be vectors")
        if samples.ndim != 2:
            raise ValueError("unobserved_private_samples must be [num_samples, dimension]")
        if samples.shape[0] < 2:
            raise ValueError("at least two posterior samples are required")
        if mask.ndim != 1:
            raise ValueError("observability_mask must be a vector")
        if mask.dtype != np.bool_:
            raise ValueError("observability_mask must have boolean dtype")
        arrays = (shared, private, samples)
        if any(np.any(~np.isfinite(array)) for array in arrays):
            raise ValueError("representation coordinates must be finite")

    @property
    def posterior_mean(self) -> np.ndarray:
        self.validate()
        return np.mean(self.unobserved_private_samples, axis=0)

    @property
    def posterior_variance(self) -> np.ndarray:
        self.validate()
        return np.var(self.unobserved_private_samples, axis=0, ddof=1)
