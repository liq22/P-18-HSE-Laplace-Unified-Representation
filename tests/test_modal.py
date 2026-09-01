import unittest

import numpy as np

from hse_laplace.modal import modal_transition, stable_pole_chart, synthesize_modes


class ModalStabilityTests(unittest.TestCase):
    def test_transition_norm_is_exact_decay(self) -> None:
        rho = 0.7
        omega = 3.2
        time = 1.4
        transition = modal_transition(rho, omega, time)
        spectral_norm = np.linalg.norm(transition, ord=2)
        self.assertAlmostEqual(spectral_norm, np.exp(-rho * time), places=12)

    def test_chart_enforces_stability_and_band(self) -> None:
        raw_rho = np.array([-100.0, 0.0, 100.0])
        raw_omega = np.array([-100.0, 0.0, 100.0])
        low = np.array([1.0, 10.0, 20.0])
        high = np.array([2.0, 12.0, 25.0])
        rho, omega = stable_pole_chart(raw_rho, raw_omega, low, high)
        self.assertTrue(np.all(rho > 0))
        self.assertTrue(np.all(omega >= low))
        self.assertTrue(np.all(omega <= high))

    def test_synthesis_queries_irregular_times(self) -> None:
        times = np.array([0.0, 0.07, 0.31, 0.9])
        result = synthesize_modes(
            times,
            rho=np.array([0.5]),
            omega=np.array([2.0]),
            cosine_residue=np.array([[1.0]]),
            sine_residue=np.array([[0.0]]),
        )
        expected = np.exp(-0.5 * times) * np.cos(2.0 * times)
        np.testing.assert_allclose(result[:, 0], expected)


if __name__ == "__main__":
    unittest.main()
