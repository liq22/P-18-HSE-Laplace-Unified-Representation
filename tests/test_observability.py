import unittest

import numpy as np

from hse_laplace.observability import (
    observable_projector,
    shared_private_missing_null,
    soft_modal_observability,
)


class ObservableDecompositionTests(unittest.TestCase):
    def test_four_way_decomposition(self) -> None:
        low = np.diag([1.0, 1.0, 0.0, 0.0, 0.0])
        high_a = np.diag([1.0, 1.0, 1.0, 0.0, 0.0])
        high_b = np.diag([1.0, 1.0, 0.0, 1.0, 0.0])
        decomposition = shared_private_missing_null(
            [low, high_a, high_b], domain_index=1
        )
        np.testing.assert_allclose(
            decomposition.shared, np.diag([1.0, 1.0, 0.0, 0.0, 0.0])
        )
        np.testing.assert_allclose(
            decomposition.observed_private,
            np.diag([0.0, 0.0, 1.0, 0.0, 0.0]),
        )
        np.testing.assert_allclose(
            decomposition.recoverable_missing,
            np.diag([0.0, 0.0, 0.0, 1.0, 0.0]),
        )
        np.testing.assert_allclose(
            decomposition.global_null,
            np.diag([0.0, 0.0, 0.0, 0.0, 1.0]),
        )
        decomposition.validate()

    def test_empty_shared_support_is_explicit(self) -> None:
        first = np.diag([1.0, 0.0, 0.0])
        second = np.diag([0.0, 1.0, 0.0])
        decomposition = shared_private_missing_null(
            [first, second], domain_index=0
        )
        np.testing.assert_allclose(decomposition.shared, np.zeros((3, 3)))
        np.testing.assert_allclose(
            decomposition.global_null, np.diag([0.0, 0.0, 1.0])
        )
        decomposition.validate()

    def test_gramian_threshold(self) -> None:
        operator = np.diag([2.0, 0.1])
        covariance = np.eye(2)
        projector = observable_projector(operator, covariance, threshold=1.0)
        np.testing.assert_allclose(projector, np.diag([1.0, 0.0]))

    def test_indefinite_noise_covariance_is_rejected(self) -> None:
        operator = np.eye(2)
        covariance = np.diag([1.0, -1.0])
        with self.assertRaisesRegex(ValueError, "positive definite"):
            observable_projector(operator, covariance, threshold=1.0)

    def test_soft_observability_is_monotone_and_half_at_threshold(self) -> None:
        weights = soft_modal_observability(
            np.array([0.5, 1.0, 1.5]), threshold=1.0, temperature=0.2
        )
        self.assertLess(weights[0], weights[1])
        self.assertLess(weights[1], weights[2])
        self.assertAlmostEqual(weights[1], 0.5)


if __name__ == "__main__":
    unittest.main()
