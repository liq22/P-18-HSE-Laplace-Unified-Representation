"""Stable real coordinates for complex-conjugate Laplace modes."""

from __future__ import annotations

import numpy as np


def _softplus(x: np.ndarray) -> np.ndarray:
    """Numerically stable softplus without hiding invalid inputs."""
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
    """Map unconstrained parameters to stable, band-limited modal poles.

    The decoded pole is ``-rho + i * omega``.  The function fails when a band
    is empty; it never swaps malformed endpoints or clips them silently.
    """
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
    if rho_min <= 0:
        raise ValueError("rho_min must be strictly positive")
    if np.any(~np.isfinite(raw_damping)) or np.any(~np.isfinite(raw_frequency)):
        raise ValueError("raw modal parameters must be finite")
    if np.any(~np.isfinite(band_low)) or np.any(~np.isfinite(band_high)):
        raise ValueError("modal bands must be finite")
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


def modal_transition(rho: float, omega: float, t: float) -> np.ndarray:
    """Closed-form state transition ``exp(A t)`` for one modal block."""
    if t < 0 or not np.isfinite(t):
        raise ValueError("t must be finite and non-negative")
    modal_block(rho, omega)  # validates parameters
    decay = np.exp(-rho * t)
    angle = omega * t
    rotation = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
        dtype=float,
    )
    return decay * rotation


def synthesize_modes(
    times: np.ndarray,
    rho: np.ndarray,
    omega: np.ndarray,
    cosine_residue: np.ndarray,
    sine_residue: np.ndarray,
) -> np.ndarray:
    """Evaluate a finite real Laplace-modal expansion at arbitrary times."""
    times = np.asarray(times, dtype=float)
    rho = np.asarray(rho, dtype=float)
    omega = np.asarray(omega, dtype=float)
    cosine_residue = np.asarray(cosine_residue, dtype=float)
    sine_residue = np.asarray(sine_residue, dtype=float)
    if times.ndim != 1:
        raise ValueError("times must be one-dimensional")
    if np.any(np.diff(times) < 0) or np.any(times < 0):
        raise ValueError("times must be sorted and non-negative")
    if rho.ndim != 1 or omega.shape != rho.shape:
        raise ValueError("rho and omega must be one-dimensional with equal shape")
    if cosine_residue.shape != sine_residue.shape:
        raise ValueError("cosine and sine residues must have equal shape")
    if cosine_residue.shape[0] != rho.size:
        raise ValueError("the leading residue dimension must equal the number of modes")
    if np.any(rho <= 0):
        raise ValueError("all damping rates must be strictly positive")

    phase = times[:, None] * omega[None, :]
    decay = np.exp(-times[:, None] * rho[None, :])
    weights_cos = decay * np.cos(phase)
    weights_sin = decay * np.sin(phase)
    return weights_cos @ cosine_residue + weights_sin @ sine_residue
