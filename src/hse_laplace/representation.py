"""Finite interface for the source-supported unified representation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class UnifiedRepresentation:
    """Finite summary of a distribution-valued, four-block representation.

    Global-null coordinates are marked but never represented as learned
    recoveries. The Monte Carlo axis of ``recoverable_missing_samples`` is
    explicit; a posterior mean is not silently substituted for a distribution.
    """

    shared_canonical: np.ndarray
    observed_private: np.ndarray
    recoverable_missing_samples: np.ndarray
    structural_observability: np.ndarray
    instance_reliability: np.ndarray
    global_null_mask: np.ndarray

    def validate(self) -> None:
        shared = np.asarray(self.shared_canonical, dtype=float)
        private = np.asarray(self.observed_private, dtype=float)
        samples = np.asarray(self.recoverable_missing_samples, dtype=float)
        structural = np.asarray(self.structural_observability, dtype=float)
        reliability = np.asarray(self.instance_reliability, dtype=float)
        global_null = np.asarray(self.global_null_mask)

        if shared.ndim != 1 or private.ndim != 1:
            raise ValueError("shared and observed-private coordinates must be vectors")
        if samples.ndim != 2:
            raise ValueError(
                "recoverable_missing_samples must be [num_samples, dimension]"
            )
        if samples.shape[0] < 2:
            raise ValueError("at least two posterior samples are required")
        if structural.ndim != 1 or reliability.ndim != 1:
            raise ValueError(
                "structural_observability and instance_reliability must be vectors"
            )
        if structural.shape != reliability.shape:
            raise ValueError(
                "structural_observability and instance_reliability must match"
            )
        if global_null.shape != structural.shape or global_null.dtype != np.bool_:
            raise ValueError("global_null_mask must be a boolean vector of modal slots")
        if np.any((structural < 0.0) | (structural > 1.0)):
            raise ValueError("structural_observability must lie in [0, 1]")
        if np.any((reliability < 0.0) | (reliability > 1.0)):
            raise ValueError("instance_reliability must lie in [0, 1]")
        if np.any(structural[global_null] > 0.0):
            raise ValueError("global-null slots cannot be structurally observable")
        arrays = (shared, private, samples, structural, reliability)
        if any(np.any(~np.isfinite(array)) for array in arrays):
            raise ValueError("representation coordinates must be finite")

    @property
    def missing_posterior_mean(self) -> np.ndarray:
        self.validate()
        return np.mean(self.recoverable_missing_samples, axis=0)

    @property
    def missing_posterior_variance(self) -> np.ndarray:
        self.validate()
        return np.var(self.recoverable_missing_samples, axis=0, ddof=1)
