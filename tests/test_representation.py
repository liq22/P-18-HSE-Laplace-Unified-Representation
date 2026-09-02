import unittest

import numpy as np

from hse_laplace.representation import UnifiedRepresentation


class RepresentationTests(unittest.TestCase):
    def test_recoverable_missing_distribution_is_explicit(self) -> None:
        representation = UnifiedRepresentation(
            shared_canonical=np.array([1.0, 2.0]),
            observed_private=np.array([3.0]),
            recoverable_missing_samples=np.array([[0.0], [1.0], [2.0]]),
            structural_observability=np.array([1.0, 1.0, 1.0, 0.0]),
            instance_reliability=np.array([0.9, 0.8, 0.7, 0.0]),
            global_null_mask=np.array([False, False, False, True]),
        )
        representation.validate()
        np.testing.assert_allclose(
            representation.missing_posterior_mean, np.array([1.0])
        )
        np.testing.assert_allclose(
            representation.missing_posterior_variance, np.array([1.0])
        )

    def test_single_sample_is_not_silently_called_a_posterior(self) -> None:
        representation = UnifiedRepresentation(
            shared_canonical=np.array([1.0]),
            observed_private=np.array([2.0]),
            recoverable_missing_samples=np.array([[0.0]]),
            structural_observability=np.array([1.0, 0.0]),
            instance_reliability=np.array([1.0, 0.0]),
            global_null_mask=np.array([False, True]),
        )
        with self.assertRaises(ValueError):
            representation.validate()

    def test_global_null_slot_cannot_be_marked_observable(self) -> None:
        representation = UnifiedRepresentation(
            shared_canonical=np.array([1.0]),
            observed_private=np.array([]),
            recoverable_missing_samples=np.array([[0.0], [1.0]]),
            structural_observability=np.array([1.0, 0.1]),
            instance_reliability=np.array([1.0, 0.0]),
            global_null_mask=np.array([False, True]),
        )
        with self.assertRaisesRegex(ValueError, "global-null"):
            representation.validate()


if __name__ == "__main__":
    unittest.main()
