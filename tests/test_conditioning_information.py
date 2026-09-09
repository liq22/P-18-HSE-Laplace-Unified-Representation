"""Theoretical boundary checks through the existing diagonal tokenizer."""
import unittest
import numpy as np
from hse_laplace.acquisition import GaussianInformation, gaussian_information_statistics, gaussian_posterior
from hse_laplace.conditioning import information_tokens_from_diagonal

class ConditioningInformationTests(unittest.TestCase):
    @staticmethod
    def make_case(coupling):
        information = np.array([[1., coupling], [coupling, 1.]])
        operator = np.linalg.cholesky(information).T
        observation = np.linalg.solve(operator.T, np.array([1., .4]))
        statistics = gaussian_information_statistics(operator, np.eye(2), observation)
        tokens = information_tokens_from_diagonal(
            statistics, np.tile([0., .1], (2, 1)),
            np.tile([10., 20.], (2, 1)), np.ones(2))
        return operator, statistics, tokens

    def test_actual_diagonal_condition_collides_without_informative_side_input(self):
        _, plus, token_plus = self.make_case(.8)
        _, minus, token_minus = self.make_case(-.8)
        for field in token_plus.__dataclass_fields__:
            np.testing.assert_allclose(getattr(token_plus, field),
                getattr(token_minus, field), rtol=0, atol=1e-12)
        p = gaussian_posterior(np.zeros(2), np.eye(2), plus)
        q = gaussian_posterior(np.zeros(2), np.eye(2), minus)
        self.assertGreater(np.linalg.norm(p.mean-q.mean), .5)
        self.assertFalse(np.allclose(p.covariance, q.covariance))

    def test_full_actual_descriptor_reconstructs_the_discarded_information(self):
        for coupling in [.8, -.8]:
            operator, statistics, tokens = self.make_case(coupling)
            # Decoder reads b from tokens and J from its actual side input A,R.
            noise_covariance = np.eye(operator.shape[0])
            rebuilt_J = operator.T @ np.linalg.solve(noise_covariance, operator)
            rebuilt = GaussianInformation(tokens.tokens[:, 0], rebuilt_J)
            exact = gaussian_posterior(np.zeros(2), np.eye(2), statistics)
            decoded = gaussian_posterior(np.zeros(2), np.eye(2), rebuilt)
            np.testing.assert_allclose(decoded.mean, exact.mean, atol=1e-12)
            np.testing.assert_allclose(decoded.covariance, exact.covariance, atol=1e-12)

if __name__ == '__main__':
    unittest.main()
