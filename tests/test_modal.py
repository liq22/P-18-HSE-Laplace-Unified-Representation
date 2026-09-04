import unittest

import numpy as np

from hse_laplace.modal import modal_transition, stable_pole_chart


class ModalTests(unittest.TestCase):
    def test_transition_norm_is_exact_decay(self) -> None:
        rho = 0.7
        omega = 4.0
        time_s = 1.3
        transition = modal_transition(rho, omega, time_s)
        self.assertAlmostEqual(
            np.linalg.norm(transition, ord=2), np.exp(-rho * time_s), places=12
        )

    def test_stable_chart_respects_frequency_slots(self) -> None:
        low = np.array([2.0, 10.0])
        high = np.array([8.0, 20.0])
        rho, omega = stable_pole_chart(
            np.array([-2.0, 1.0]), np.array([-1.0, 2.0]), low, high
        )
        self.assertTrue(np.all(rho > 0))
        self.assertTrue(np.all(omega >= low))
        self.assertTrue(np.all(omega <= high))


if __name__ == "__main__":
    unittest.main()
