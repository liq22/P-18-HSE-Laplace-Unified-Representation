"""Blockwise deterministic and stochastic transport utilities."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np


def compensated_gaussian_drift(
    x: np.ndarray,
    mean: np.ndarray,
    mean_derivative: np.ndarray,
    standard_deviation: np.ndarray,
    standard_deviation_derivative: np.ndarray,
    diffusion: np.ndarray,
) -> np.ndarray:
    """Drift that preserves a prescribed diagonal Gaussian probability path.

    For each coordinate, the continuity velocity is
    ``m_dot + sigma_dot / sigma * (x - m)``.  Adding ``D score`` and diffusion
    covariance ``2D`` yields the same one-time marginals.
    """
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


def block_euler_step(
    state: np.ndarray,
    shared_projector: np.ndarray,
    private_projector: np.ndarray,
    unobserved_projector: np.ndarray,
    shared_velocity: Callable[[np.ndarray], np.ndarray],
    unobserved_velocity: Callable[[np.ndarray], np.ndarray],
    *,
    step_size: float,
    unobserved_noise: np.ndarray | None = None,
) -> np.ndarray:
    """One transparent Euler step of the blockwise representation process."""
    state = np.asarray(state, dtype=float)
    projectors = [
        np.asarray(shared_projector, dtype=float),
        np.asarray(private_projector, dtype=float),
        np.asarray(unobserved_projector, dtype=float),
    ]
    if state.ndim != 1:
        raise ValueError("state must be a vector")
    if any(projector.shape != (state.size, state.size) for projector in projectors):
        raise ValueError("projector shapes must match state dimension")
    if step_size <= 0 or not np.isfinite(step_size):
        raise ValueError("step_size must be finite and positive")

    shared_state = projectors[0] @ state
    unobserved_state = projectors[2] @ state
    shared_update = projectors[0] @ np.asarray(shared_velocity(shared_state), dtype=float)
    unobserved_update = projectors[2] @ np.asarray(
        unobserved_velocity(unobserved_state), dtype=float
    )
    if shared_update.shape != state.shape or unobserved_update.shape != state.shape:
        raise ValueError("velocity functions must return vectors matching state")

    result = state + step_size * (shared_update + unobserved_update)
    if unobserved_noise is not None:
        noise = np.asarray(unobserved_noise, dtype=float)
        if noise.shape != state.shape:
            raise ValueError("unobserved_noise must match state")
        result = result + projectors[2] @ noise
    return result
