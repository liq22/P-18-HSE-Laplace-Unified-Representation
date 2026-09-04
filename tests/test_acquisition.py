import unittest

import numpy as np

from hse_laplace.acquisition import (
    gaussian_information_statistics,
    gaussian_posterior,
    loewner_margin,
)


class GaussianAcquisitionTests(unittest.TestCase):
    def test_variable_length_observations_have_fixed_modal_statistics(self) -> None:
        short_operator = np.array([[1.0, 0.0], [0.0, 1.0]])
        long_operator = np.array(
            [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [2.0, -1.0]]
        )
        short = gaussian_information_statistics(
            short_operator, np.eye(2), np.array([0.2, -0.4])
        )
        long = gaussian_information_statistics(
            long_operator, np.eye(4), np.array([0.2, -0.4, -0.2, 0.8])
        )
        self.assertEqual(short.score.shape, (2,))
        self.assertEqual(long.score.shape, (2,))
        self.assertEqual(short.information.shape, (2, 2))
        self.assertEqual(long.information.shape, (2, 2))

    def test_sufficient_statistic_equivalence_has_constant_likelihood_ratio(self) -> None:
        operator = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
        first = np.array([0.4, -0.3, 0.2])
        second = first + np.array([-1.0, -1.0, 1.0])
        stats_first = gaussian_information_statistics(operator, np.eye(3), first)
        stats_second = gaussian_information_statistics(operator, np.eye(3), second)
        np.testing.assert_allclose(stats_first.score, stats_second.score)
        np.testing.assert_allclose(stats_first.information, stats_second.information)
        values = np.array([[-1.0, 0.3], [0.0, 0.0], [0.5, -0.7], [2.0, 1.0]])
        differences = []
        for theta in values:
            residual_first = first - operator @ theta
            residual_second = second - operator @ theta
            differences.append(
                -0.5 * residual_second @ residual_second
                + 0.5 * residual_first @ residual_first
            )
        self.assertLess(np.ptp(differences), 1e-12)

    def test_information_order_reverses_posterior_covariance_order(self) -> None:
        prior_mean = np.zeros(2)
        prior_covariance = np.eye(2)
        low_operator = np.array([[1.0, 0.0]])
        high_operator = np.array([[1.0, 0.0], [0.0, 2.0]])
        low_stats = gaussian_information_statistics(
            low_operator, np.eye(1), np.array([0.2])
        )
        high_stats = gaussian_information_statistics(
            high_operator, np.eye(2), np.array([0.2, -0.8])
        )
        low_posterior = gaussian_posterior(prior_mean, prior_covariance, low_stats)
        high_posterior = gaussian_posterior(prior_mean, prior_covariance, high_stats)
        self.assertGreaterEqual(
            loewner_margin(high_stats.information, low_stats.information), -1e-12
        )
        self.assertGreaterEqual(
            loewner_margin(low_posterior.covariance, high_posterior.covariance),
            -1e-12,
        )
        self.assertLess(high_posterior.entropy(), low_posterior.entropy())

    def test_indefinite_noise_covariance_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "positive definite"):
            gaussian_information_statistics(
                np.eye(2), np.diag([1.0, -1.0]), np.zeros(2)
            )


if __name__ == "__main__":
    unittest.main()
