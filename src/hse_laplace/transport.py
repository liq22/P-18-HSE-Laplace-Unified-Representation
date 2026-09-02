"""Analytic block-transport utilities."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from .observability import ObservableDecomposition


def compensated_gaussian_drift(
    x: np.ndarray,
    mean: np.ndarray,
    mean_derivative: np.ndarray,
    standard_deviation: np.ndarray,
    standard_deviation_derivative: np.ndarray,
    diffusion: np.ndarray,
) -> np.ndarray:
    """Drift that preserves a prescribed diagonal Gaussian probability path."""
    x = np.asarray(x, dtype=float)
    mean = np.asarray(mean, dtype=float)
    mean_derivative = np.asarray(mean_derivative, dtype=float)
    sigma = np.asarray(standard_deviation, dtype=float)
    sigma_derivative = np.asarray(standard_deviation_derivative, dtype=float)
    diffusion = np.asarray(diffusion, dtype=float)
    if not (
        x.shape
        == mean.shape
        == mean_derivative.shape
        == sigma.shape
        == sigma_derivative.shape
        == diffusion.shape
    ):
        raise ValueError("all Gaussian path arrays must have equal shapes")
    if np.any(sigma <= 0) or np.any(diffusion < 0):
        raise ValueError("standard deviations must be positive and diffusion non-negative")
    centered = x - mean
    continuity_velocity = mean_derivative + (sigma_derivative / sigma) * centered
    score = -centered / (sigma**2)
    return continuity_velocity + diffusion * score


def block_update_witness(
    state: np.ndarray,
    decomposition: ObservableDecomposition,
    shared_velocity: Callable[[np.ndarray], np.ndarray],
    recoverable_missing_velocity: Callable[
        [np.ndarray, np.ndarray, np.ndarray], np.ndarray
    ],
    *,
    step_size: float,
    recoverable_missing_increment: np.ndarray | None = None,
) -> np.ndarray:
    """Apply one transparent triangular block update.

    This function is an analytic witness, not an Euler--Maruyama solver. The
    optional stochastic increment must already contain its numerical scaling.
    Shared coordinates are updated first; the recoverable-missing update may
    condition on the updated shared coordinate and the unchanged private block.
    Global-null coordinates are not modeled and remain unchanged.
    """
    state = np.asarray(state, dtype=float)
    if state.ndim != 1:
        raise ValueError("state must be a vector")
    decomposition.validate()
    projectors = (
        decomposition.shared,
        decomposition.observed_private,
        decomposition.recoverable_missing,
        decomposition.global_null,
    )
    if any(projector.shape != (state.size, state.size) for projector in projectors):
        raise ValueError("projector shapes must match state dimension")
    if step_size <= 0 or not np.isfinite(step_size):
        raise ValueError("step_size must be finite and positive")

    shared_state = decomposition.shared @ state
    private_state = decomposition.observed_private @ state
    missing_state = decomposition.recoverable_missing @ state

    shared_update = decomposition.shared @ np.asarray(
        shared_velocity(shared_state), dtype=float
    )
    if shared_update.shape != state.shape:
        raise ValueError("shared_velocity must return a vector matching state")
    shared_next = shared_state + step_size * shared_update

    missing_update = decomposition.recoverable_missing @ np.asarray(
        recoverable_missing_velocity(missing_state, shared_next, private_state),
        dtype=float,
    )
    if missing_update.shape != state.shape:
        raise ValueError(
            "recoverable_missing_velocity must return a vector matching state"
        )

    result = state + step_size * (shared_update + missing_update)
    if recoverable_missing_increment is not None:
        increment = np.asarray(recoverable_missing_increment, dtype=float)
        if increment.shape != state.shape:
            raise ValueError("recoverable_missing_increment must match state")
        result = result + decomposition.recoverable_missing @ increment
    return result
