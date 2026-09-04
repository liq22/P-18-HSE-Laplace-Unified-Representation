"""Closed-form oracle for the HSE-conditioned LLapDiff theory contract."""

from __future__ import annotations

import json

import numpy as np

from hse_laplace import (
    gaussian_information_statistics,
    gaussian_posterior,
    information_tokens_from_diagonal,
    loewner_margin,
)


def likelihood(theta: np.ndarray, operator: np.ndarray, observation: np.ndarray) -> float:
    residual = observation - operator @ theta
    return float(-0.5 * residual @ residual)


def main() -> None:
    theta = np.array([0.6, -0.8, 1.1])
    prior_mean = np.zeros(3)
    prior_covariance = np.eye(3)

    operators = {
        "low": np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
        "mid": np.array(
            [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.5]]
        ),
        "high": np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.5],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
            ]
        ),
    }

    time_s = np.array([[0.0, 0.25], [0.25, 0.50], [0.50, 0.75]])
    band_hz = np.array([[5.0, 15.0], [15.0, 35.0], [55.0, 75.0]])
    reliability = {
        "low": np.array([1.0, 1.0, 0.0]),
        "mid": np.array([1.0, 1.0, 0.6]),
        "high": np.array([1.0, 1.0, 1.0]),
    }

    statistics = {}
    posteriors = {}
    tokens = {}
    for name, operator in operators.items():
        observation = operator @ theta
        covariance = np.eye(operator.shape[0])
        statistics[name] = gaussian_information_statistics(
            operator, covariance, observation
        )
        posteriors[name] = gaussian_posterior(
            prior_mean, prior_covariance, statistics[name]
        )
        tokens[name] = information_tokens_from_diagonal(
            statistics[name],
            time_s,
            band_hz,
            reliability[name],
            information_threshold=1e-12,
        )

    information_margins = {
        "mid_minus_low": loewner_margin(
            statistics["mid"].information, statistics["low"].information
        ),
        "high_minus_mid": loewner_margin(
            statistics["high"].information, statistics["mid"].information
        ),
    }
    covariance_margins = {
        "low_minus_mid": loewner_margin(
            posteriors["low"].covariance, posteriors["mid"].covariance
        ),
        "mid_minus_high": loewner_margin(
            posteriors["mid"].covariance, posteriors["high"].covariance
        ),
    }
    if min(information_margins.values()) < -1e-10:
        raise RuntimeError("nested acquisition information order failed")
    if min(covariance_margins.values()) < -1e-10:
        raise RuntimeError("posterior covariance order failed")

    sufficient_operator = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    observation_a = np.array([0.4, -0.3, 0.2])
    likelihood_null = np.array([-1.0, -1.0, 1.0])
    observation_b = observation_a + likelihood_null
    stats_a = gaussian_information_statistics(
        sufficient_operator, np.eye(3), observation_a
    )
    stats_b = gaussian_information_statistics(
        sufficient_operator, np.eye(3), observation_b
    )
    if not np.allclose(stats_a.score, stats_b.score):
        raise RuntimeError("sufficient-statistic score changed")
    theta_grid = np.array(
        [[-1.0, -0.5], [0.0, 0.0], [0.3, -0.7], [1.0, 1.5]]
    )
    likelihood_differences = np.array(
        [
            likelihood(value, sufficient_operator, observation_b)
            - likelihood(value, sufficient_operator, observation_a)
            for value in theta_grid
        ]
    )
    likelihood_difference_spread = float(np.ptp(likelihood_differences))
    if likelihood_difference_spread > 1e-12:
        raise RuntimeError("likelihood ratio depends on the latent state")

    result = {
        "posterior_variance": {
            name: np.diag(posterior.covariance).round(12).tolist()
            for name, posterior in posteriors.items()
        },
        "posterior_entropy": {
            name: round(posterior.entropy(), 12)
            for name, posterior in posteriors.items()
        },
        "information_order_min_eigenvalue": information_margins,
        "covariance_order_min_eigenvalue": covariance_margins,
        "token_shape": {name: list(value.tokens.shape) for name, value in tokens.items()},
        "attention_mask": {
            name: value.attention_mask.tolist() for name, value in tokens.items()
        },
        "sufficient_statistic_likelihood_difference_spread": likelihood_difference_spread,
        "evidence_level": "linear_gaussian_analytic_oracle",
        "formal_claim_supported": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
