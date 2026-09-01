import unittest

import numpy as np

from hse_laplace.transport import block_euler_step, compensated_gaussian_drift


class TransportTests(unittest.TestCase):
    def test_private_coordinate_is_pathwise_invariant(self) -> None:
        shared = np.diag([1.0, 0.0, 0.0])
        private = np.diag([0.0, 1.0, 0.0])
        unobserved = np.diag([0.0, 0.0, 1.0])
        state = np.array([1.0, 7.0, -1.0])
        for _ in range(20):
            state = block_euler_step(
                state,
                shared,
                private,
                unobserved,
                shared_velocity=lambda z: -z,
                unobserved_velocity=lambda z: 0.25 * z,
                step_size=0.01,
                unobserved_noise=np.array([2.0, 3.0, -0.01]),
            )
        self.assertEqual(state[1], 7.0)

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

        # For dX = [m_dot + a(X-m)]dt + sqrt(2D)dW,
        # d Var[X]/dt = 2 a sigma^2 + 2D = 2 sigma sigma_dot.
        variance_derivative = 2.0 * centered_coefficient * sigma**2 + 2.0 * diffusion
        np.testing.assert_allclose(variance_derivative, 2.0 * sigma * sigma_dot)


if __name__ == "__main__":
    unittest.main()
