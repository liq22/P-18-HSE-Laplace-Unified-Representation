import unittest

import numpy as np

from hse_laplace.acquisition import gaussian_information_statistics
from hse_laplace.conditioning import information_tokens_from_diagonal


class HSEConditioningTests(unittest.TestCase):
    def test_fixed_token_shape_and_support_mask(self) -> None:
        operator = np.array([[1.0, 0.0, 0.0], [0.0, 2.0, 0.0]])
        statistics = gaussian_information_statistics(
            operator, np.eye(2), np.array([0.3, -0.4])
        )
        result = information_tokens_from_diagonal(
            statistics,
            token_time_s=np.array([[0.0, 0.1], [0.1, 0.2], [0.2, 0.3]]),
            token_band_hz=np.array([[5.0, 15.0], [15.0, 35.0], [55.0, 75.0]]),
            observation_reliability=np.array([1.0, 0.8, 0.0]),
            information_threshold=1e-12,
        )
        self.assertEqual(result.tokens.shape, (3, 8))
        self.assertEqual(result.attention_mask.tolist(), [True, True, False])
        result.validate()

    def test_invalid_physical_interval_fails(self) -> None:
        statistics = gaussian_information_statistics(
            np.eye(2), np.eye(2), np.ones(2)
        )
        with self.assertRaisesRegex(ValueError, "positive duration"):
            information_tokens_from_diagonal(
                statistics,
                token_time_s=np.array([[0.0, 0.1], [0.2, 0.2]]),
                token_band_hz=np.array([[1.0, 2.0], [2.0, 3.0]]),
                observation_reliability=np.ones(2),
            )


if __name__ == "__main__":
    unittest.main()
