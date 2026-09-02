"""Analytic components for HSE-Laplace unified representation."""

from .modal import modal_block, modal_transition, stable_pole_chart
from .observability import (
    ObservableDecomposition,
    observable_projector,
    shared_private_missing_null,
    soft_modal_observability,
)
from .representation import UnifiedRepresentation
from .transport import block_update_witness, compensated_gaussian_drift

__all__ = [
    "ObservableDecomposition",
    "UnifiedRepresentation",
    "block_update_witness",
    "compensated_gaussian_drift",
    "modal_block",
    "modal_transition",
    "observable_projector",
    "shared_private_missing_null",
    "soft_modal_observability",
    "stable_pole_chart",
]
