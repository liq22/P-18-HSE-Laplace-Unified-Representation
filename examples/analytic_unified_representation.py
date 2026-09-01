"""Small deterministic witness for the three-block representation contract."""

from __future__ import annotations

import numpy as np

from hse_laplace.modal import modal_transition
from hse_laplace.observability import shared_private_unobserved
from hse_laplace.transport import block_euler_step


def main() -> None:
    low_rate_observable = np.diag([1.0, 1.0, 0.0, 0.0])
    high_rate_observable = np.diag([1.0, 1.0, 1.0, 0.0])
    decomposition = shared_private_unobserved(
        [low_rate_observable, high_rate_observable], domain_index=1
    )

    state = np.array([1.0, -1.0, 4.0, 0.5])
    initial_private = decomposition.observed_private @ state
    for _ in range(10):
        state = block_euler_step(
            state,
            decomposition.shared,
            decomposition.observed_private,
            decomposition.unobserved,
            shared_velocity=lambda z: -0.2 * z,
            unobserved_velocity=lambda z: -0.1 * z,
            step_size=0.05,
            unobserved_noise=np.array([0.0, 0.0, 0.0, 0.01]),
        )
    final_private = decomposition.observed_private @ state
    if not np.allclose(initial_private, final_private):
        raise RuntimeError("observed-private coordinate changed")

    transition_norm = np.linalg.norm(modal_transition(0.4, 5.0, 2.0), ord=2)
    expected_bound = np.exp(-0.8)
    if not np.isclose(transition_norm, expected_bound):
        raise RuntimeError("stable modal transition violated its analytic norm")

    print("observable decomposition: passed")
    print("observed-private identity: passed")
    print("stable Laplace modal chart: passed")
    print("evidence level: analytic witness only")
    print("formal_claim_supported: false")


if __name__ == "__main__":
    main()
