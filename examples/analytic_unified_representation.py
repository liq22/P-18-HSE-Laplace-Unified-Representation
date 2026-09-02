"""Deterministic witness for the four-block representation contract."""

from __future__ import annotations

import numpy as np

from hse_laplace.modal import modal_transition
from hse_laplace.observability import shared_private_missing_null
from hse_laplace.transport import block_update_witness


def main() -> None:
    low = np.diag([1.0, 1.0, 0.0, 0.0, 0.0])
    high_a = np.diag([1.0, 1.0, 1.0, 0.0, 0.0])
    high_b = np.diag([1.0, 1.0, 0.0, 1.0, 0.0])
    decomposition = shared_private_missing_null(
        [low, high_a, high_b], domain_index=1
    )

    state = np.array([1.0, -1.0, 4.0, 0.5, 9.0])
    initial_private = decomposition.observed_private @ state
    initial_global_null = decomposition.global_null @ state

    for _ in range(10):
        state = block_update_witness(
            state,
            decomposition,
            shared_velocity=lambda z: -0.2 * z,
            recoverable_missing_velocity=lambda m, c, p: -0.1 * m + 0.05 * c,
            step_size=0.05,
            recoverable_missing_increment=np.array([0.0, 0.0, 0.0, 0.01, 0.0]),
        )

    if not np.allclose(
        decomposition.observed_private @ state, initial_private
    ):
        raise RuntimeError("observed-private coordinate changed")
    if not np.allclose(decomposition.global_null @ state, initial_global_null):
        raise RuntimeError("global-null coordinate was modeled")

    transition_norm = np.linalg.norm(modal_transition(0.4, 5.0, 2.0), ord=2)
    expected_bound = np.exp(-0.8)
    if not np.isclose(transition_norm, expected_bound):
        raise RuntimeError("stable modal transition violated its analytic norm")

    print("four-block observable decomposition: passed")
    print("observed-private identity: passed")
    print("global-null exclusion: passed")
    print("stable Laplace modal chart: passed")
    print("evidence level: analytic witness only")
    print("formal_claim_supported: false")


if __name__ == "__main__":
    main()
