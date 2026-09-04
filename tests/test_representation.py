import unittest

import numpy as np

from hse_laplace.representation import CanonicalLaplacePosterior


class CanonicalPosteriorTests(unittest.TestCase):
    def test_directional_variance_and_entropy(self) -> None:
        posterior = CanonicalLaplacePosterior(
            mean=np.array([0.0, 1.0]), covariance=np.diag([0.25, 1.0])
        )
        posterior.validate()
        self.assertAlmostEqual(
            posterior.directional_variance(np.array([1.0, 0.0])), 0.25
        )
        self.assertTrue(np.isfinite(posterior.entropy()))

    def test_non_positive_covariance_fails(self) -> None:
        posterior = CanonicalLaplacePosterior(
            mean=np.zeros(2), covariance=np.diag([1.0, 0.0])
        )
        with self.assertRaisesRegex(ValueError, "positive definite"):
            posterior.validate()


if __name__ == "__main__":
    unittest.main()
