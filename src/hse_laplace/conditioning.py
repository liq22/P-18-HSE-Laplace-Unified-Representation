"""Fixed-token HSE conditioning from acquisition information statistics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .acquisition import GaussianInformation


@dataclass(frozen=True)
class HSEConditioningTokens:
    """Research interface for fixed physical modal conditioning tokens."""

    tokens: np.ndarray
    attention_mask: np.ndarray
    token_time_s: np.ndarray
    token_band_hz: np.ndarray
    modal_score: np.ndarray
    modal_information: np.ndarray
    observation_reliability: np.ndarray

    def validate(self) -> None:
        tokens = np.asarray(self.tokens, dtype=float)
        mask = np.asarray(self.attention_mask)
        time = np.asarray(self.token_time_s, dtype=float)
        band = np.asarray(self.token_band_hz, dtype=float)
        score = np.asarray(self.modal_score, dtype=float)
        information = np.asarray(self.modal_information, dtype=float)
        reliability = np.asarray(self.observation_reliability, dtype=float)
        if tokens.ndim != 2:
            raise ValueError("tokens must be [K, D]")
        token_count = tokens.shape[0]
        if mask.shape != (token_count,) or mask.dtype != np.bool_:
            raise ValueError("attention_mask must be a boolean [K] vector")
        if time.shape != (token_count, 2):
            raise ValueError("token_time_s must be [K, 2]")
        if band.shape != (token_count, 2):
            raise ValueError("token_band_hz must be [K, 2]")
        vectors = (score, information, reliability)
        if any(vector.shape != (token_count,) for vector in vectors):
            raise ValueError("modal statistics and reliability must be [K]")
        if np.any(time[:, 1] <= time[:, 0]):
            raise ValueError("each physical-time interval must have positive duration")
        if np.any(band[:, 1] <= band[:, 0]) or np.any(band < 0):
            raise ValueError("each frequency band must be non-negative and non-empty")
        if np.any((reliability < 0) | (reliability > 1)):
            raise ValueError("observation_reliability must lie in [0, 1]")
        arrays = (tokens, time, band, score, information, reliability)
        if any(np.any(~np.isfinite(array)) for array in arrays):
            raise ValueError("conditioning values must be finite")


def information_tokens_from_diagonal(
    statistics: GaussianInformation,
    token_time_s: np.ndarray,
    token_band_hz: np.ndarray,
    observation_reliability: np.ndarray,
    *,
    information_threshold: float = 0.0,
) -> HSEConditioningTokens:
    """Build one fixed token per declared Laplace modal slot.

    This is an analytic oracle interface. A learned HSE module should estimate
    equivalent slotwise information without receiving unavailable target values.
    """
    statistics.validate()
    score = np.asarray(statistics.score, dtype=float)
    information = np.diag(statistics.information).copy()
    if np.any(information < -1e-10):
        raise ValueError("modal information must be non-negative")
    information = np.maximum(information, 0.0)  # numerical roundoff only
    time = np.asarray(token_time_s, dtype=float)
    band = np.asarray(token_band_hz, dtype=float)
    reliability = np.asarray(observation_reliability, dtype=float)
    token_count = score.size
    if time.shape != (token_count, 2) or band.shape != (token_count, 2):
        raise ValueError("time and band metadata must have one row per modal slot")
    if reliability.shape != (token_count,):
        raise ValueError("observation_reliability must have one value per modal slot")
    if information_threshold < 0 or not np.isfinite(information_threshold):
        raise ValueError("information_threshold must be finite and non-negative")

    duration = time[:, 1] - time[:, 0]
    center_hz = 0.5 * (band[:, 0] + band[:, 1])
    bandwidth_hz = band[:, 1] - band[:, 0]
    normalized_score = score / np.sqrt(1.0 + information)
    tokens = np.column_stack(
        [
            score,
            np.log1p(information),
            np.sqrt(information),
            normalized_score,
            reliability,
            duration,
            np.log1p(center_hz),
            np.log1p(bandwidth_hz),
        ]
    )
    result = HSEConditioningTokens(
        tokens=tokens,
        attention_mask=(information > information_threshold) & (reliability > 0),
        token_time_s=time,
        token_band_hz=band,
        modal_score=score,
        modal_information=information,
        observation_reliability=reliability,
    )
    result.validate()
    return result
