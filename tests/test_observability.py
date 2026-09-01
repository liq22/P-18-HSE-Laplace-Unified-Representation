import unittest

import numpy as np

from hse_laplace.observability import observable_projector, shared_private_unobserved


class ObservableDecompositionTests(unittest.TestCase):
    def test_known_intersection(self) -> None:
        low = np.diag([1.0, 1.0, 0.0, 0.0])
        high = np.diag([1.0, 1.0, 1.0, 0.0])
        decomposition = shared_private_unobserved([low, high], domain_index=1)
        np.testing.assert_allclose(decomposition.shared, np.diag([1.0, 1.0, 0.0, 0.0]))
        np.testing.assert_allclose(
            decomposition.observed_private, np.diag([0.0, 0.0, 1.0, 0.0])
        )
        np.testing.assert_allclose(decomposition.unobserved, np.diag([0.0, 0.0, 0.0, 1.0]))
        decomposition.validate()

    def test_empty_shared_support_is_explicit(self) -> None:
        first = np.diag([1.0, 0.0])
        second = np.diag([0.0, 1.0])
        decomposition = shared_private_unobserved([first, second], domain_index=0)
        np.testing.assert_allclose(decomposition.shared, np.zeros((2, 2)))
        decomposition.validate()

    def test_gramian_threshold(self) -> None:
        operator = np.diag([2.0, 0.1])
        covariance = np.eye(2)
        projector = observable_projector(operator, covariance, threshold=1.0)
        np.testing.assert_allclose(projector, np.diag([1.0, 0.0]))


if __name__ == "__main__":
    unittest.main()
