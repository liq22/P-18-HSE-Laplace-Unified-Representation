import unittest

import numpy as np

from hse_laplace.representation import UnifiedRepresentation


class RepresentationTests(unittest.TestCase):
    def test_distribution_valued_private_block(self) -> None:
        representation = UnifiedRepresentation(
            shared_canonical=np.array([1.0, 2.0]),
            observed_private=np.array([3.0]),
            unobserved_private_samples=np.array([[0.0], [1.0], [2.0]]),
            observability_mask=np.array([True, True, False]),
        )
        representation.validate()
        np.testing.assert_allclose(representation.posterior_mean, np.array([1.0]))
        np.testing.assert_allclose(representation.posterior_variance, np.array([1.0]))

    def test_single_sample_is_not_silently_called_a_posterior(self) -> None:
        representation = UnifiedRepresentation(
            shared_canonical=np.array([1.0]),
            observed_private=np.array([2.0]),
            unobserved_private_samples=np.array([[0.0]]),
            observability_mask=np.array([True, False]),
        )
        with self.assertRaises(ValueError):
            representation.validate()


if __name__ == "__main__":
    unittest.main()
