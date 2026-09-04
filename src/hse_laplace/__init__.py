"""Analytic foundations for HSE-conditioned Latent Laplace Diffusion."""

from .acquisition import (
    GaussianInformation,
    gaussian_information_statistics,
    gaussian_posterior,
    loewner_margin,
)
from .conditioning import HSEConditioningTokens, information_tokens_from_diagonal
from .modal import modal_block, modal_transition, stable_pole_chart
from .representation import CanonicalLaplacePosterior

__all__ = [
    "CanonicalLaplacePosterior",
    "GaussianInformation",
    "HSEConditioningTokens",
    "gaussian_information_statistics",
    "gaussian_posterior",
    "information_tokens_from_diagonal",
    "loewner_margin",
    "modal_block",
    "modal_transition",
    "stable_pole_chart",
]
