"""Stable real coordinates for complex-conjugate Laplace modes."""

from __future__ import annotations

import numpy as np


def _softplus(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    return np.maximum(x, 0.0) + np.log1p(np.exp(-np.abs(x)))


def _sigmoid(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    positive = x >= 0
    result = np.empty_like(x)
    result[positive] = 1.0 / (1.0 + np.exp(-x[positive]))
    exp_x = np.exp(x[~positive])
    result[~positive] = exp_x / (1.0 + exp_x)
    return result


def stable_pole_chart(
    raw_damping: np.ndarray,
    raw_frequency: np.ndarray,
    band_low: np.ndarray,
    band_high: np.ndarray,
    *,
    rho_min: float = 1e-4,
) -> tuple[np.ndarray, np.ndarray]:
    """Map unconstrained parameters to stable, band-limited modal poles."""
    raw_damping = np.asarray(raw_damping, dtype=float)
    raw_frequency = np.asarray(raw_frequency, dtype=float)
    band_low = np.asarray(band_low, dtype=float)
    band_high = np.asarray(band_high, dtype=float)
    if not (
        raw_damping.shape
        == raw_frequency.shape
        == band_low.shape
        == band_high.shape
    ):
        raise ValueError("raw parameters and frequency bands must have equal shapes")
    if rho_min <= 0 or not np.isfinite(rho_min):
        raise ValueError("rho_min must be finite and strictly positive")
    arrays = (raw_damping, raw_frequency, band_low, band_high)
    if any(np.any(~np.isfinite(array)) for array in arrays):
        raise ValueError("modal parameters and bands must be finite")
    if np.any(band_high <= band_low):
        raise ValueError("each modal band must satisfy band_high > band_low")

    rho = rho_min + _softplus(raw_damping)
    omega = band_low + (band_high - band_low) * _sigmoid(raw_frequency)
    return rho, omega


def modal_block(rho: float, omega: float) -> np.ndarray:
    """Return the real 2x2 block with eigenvalues ``-rho ± i omega``."""
    if not np.isfinite(rho) or not np.isfinite(omega):
        raise ValueError("rho and omega must be finite")
    if rho <= 0:
        raise ValueError("rho must be strictly positive")
    if omega < 0:
        raise ValueError("omega must be non-negative")
    return np.array([[-rho, -omega], [omega, -rho]], dtype=float)


def modal_transition(rho: float, omega: float, time_s: float) -> np.ndarray:
    """Closed-form transition for one modal block at physical time in seconds."""
    if time_s < 0 or not np.isfinite(time_s):
        raise ValueError("time_s must be finite and non-negative")
    modal_block(rho, omega)
    decay = np.exp(-rho * time_s)
    angle = omega * time_s
    rotation = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
        dtype=float,
    )
    return decay * rotation
