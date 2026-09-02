import unittest

import numpy as np

from hse_laplace.observability import shared_private_missing_null
from hse_laplace.transport import block_update_witness, compensated_gaussian_drift


class TransportTests(unittest.TestCase):
    def test_private_and_global_null_coordinates_are_invariant(self) -> None:
        low = np.diag([1.0, 1.0, 0.0, 0.0, 0.0])
        high_a = np.diag([1.0, 1.0, 1.0, 0.0, 0.0])
        high_b = np.diag([1.0, 1.0, 0.0, 1.0, 0.0])
        decomposition = shared_private_missing_null(
            [low, high_a, high_b], domain_index=1
        )
        state = np.array([1.0, -1.0, 7.0, -1.0, 9.0])
        initial_private = decomposition.observed_private @ state
        initial_global_null = decomposition.global_null @ state

        for _ in range(20):
            state = block_update_witness(
                state,
                decomposition,
                shared_velocity=lambda z: -z,
                recoverable_missing_velocity=lambda m, c, p: 0.25 * m + 0.1 * c,
                step_size=0.01,
                recoverable_missing_increment=np.array(
                    [2.0, 3.0, 4.0, -0.01, 8.0]
                ),
            )

        np.testing.assert_allclose(
            decomposition.observed_private @ state, initial_private
        )
        np.testing.assert_allclose(
            decomposition.global_null @ state, initial_global_null
        )

    def test_missing_update_can_condition_on_canonical_shared_state(self) -> None:
        first = np.diag([1.0, 0.0])
        second = np.diag([1.0, 1.0])
        decomposition = shared_private_missing_null(
            [first, second], domain_index=0
        )
        state = np.array([2.0, 0.0])
        result = block_update_witness(
            state,
            decomposition,
            shared_velocity=lambda z: -0.5 * z,
            recoverable_missing_velocity=lambda m, c, p: np.array([0.0, c[0]]),
            step_size=0.1,
        )
        self.assertAlmostEqual(result[0], 1.9)
        self.assertAlmostEqual(result[1], 0.19)

    def test_compensated_sde_has_prescribed_gaussian_moments(self) -> None:
        x = np.array([1.4])
        mean = np.array([0.7])
        mean_dot = np.array([0.3])
        sigma = np.array([1.2])
        sigma_dot = np.array([-0.2])
        diffusion = np.array([0.4])
        drift = compensated_gaussian_drift(
            x, mean, mean_dot, sigma, sigma_dot, diffusion
        )
        centered_coefficient = sigma_dot / sigma - diffusion / sigma**2
        expected = mean_dot + centered_coefficient * (x - mean)
        np.testing.assert_allclose(drift, expected)

        variance_derivative = 2.0 * centered_coefficient * sigma**2 + 2.0 * diffusion
        np.testing.assert_allclose(variance_derivative, 2.0 * sigma * sigma_dot)


if __name__ == "__main__":
    unittest.main()
