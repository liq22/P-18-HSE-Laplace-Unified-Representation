"""Protect the posterior being evaluated, not documentation keywords."""
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
import numpy as np
from experiments.synthetic_known_pole.compression import (
    acquisition_family, prior_parameters, retained_information, matching_designs,
    conditional_posterior, paired_events, evaluate_cell, _lognormal,
)

class CompressedPosteriorTests(unittest.TestCase):
    def test_family_has_declared_spd_and_summary_classes(self):
        family = acquisition_family(.45)
        self.assertGreater(np.linalg.eigvalsh(family).min(), 0)
        for method, count in [('diag', 4), ('block', 2), ('full', 1)]:
            indices = matching_designs(family, retained_information(family[0], method), method)
            self.assertEqual(indices.size, count)

    def test_gaussian_full_condition_matches_closed_form(self):
        family = acquisition_family(.45)
        b = np.array([[1., -.3, .4, .7]])
        p = conditional_posterior(b, family, np.array([0]), prior_parameters('gaussian'))
        covariance = np.linalg.solve(np.eye(4)+family[0], np.eye(4))
        np.testing.assert_allclose(p.mean()[0], covariance @ b[0], atol=1e-12)
        np.testing.assert_allclose(p.covariances[0], covariance, atol=1e-12)

    def test_hidden_design_weights_use_b_likelihood_and_jacobian(self):
        family = acquisition_family(.45)
        b = np.array([[2., .3, -1., .4]])
        p = conditional_posterior(b, family, np.arange(4), prior_parameters('gaussian'))
        direct = []
        for J in family:
            A = np.linalg.cholesky(J).T
            x = np.linalg.solve(A.T, b.T).T
            # x -> b has determinant det(A.T); this check uses observation space.
            direct.append(_lognormal(x, np.zeros(4), A @ A.T+np.eye(4))[0] - np.linalg.slogdet(A)[1])
        direct = np.exp(np.array(direct) - np.max(direct)); direct /= direct.sum()
        np.testing.assert_allclose(np.exp(p.log_weights[0]), direct, atol=1e-12)
        self.assertGreater(np.ptp(direct), .05)

    def test_block_is_exact_without_cross_mode_coupling(self):
        family = acquisition_family(0)
        b = np.array([[.5, 1., -.7, .2], [-1., .3, .2, 1.]])
        prior = prior_parameters('mixture')
        full = conditional_posterior(b, family, np.array([0]), prior)
        group = matching_designs(family, retained_information(family[0], 'block'), 'block')
        block = conditional_posterior(b, family, group, prior)
        np.testing.assert_allclose(block.log_prob(b), full.log_prob(b), atol=1e-12)
        np.testing.assert_allclose(block.mean(), full.mean(), atol=1e-12)

    def test_coarse_condition_does_not_use_hidden_design(self):
        family = acquisition_family(.8)
        b = np.array([[.4, .2, .7, -.3]])
        prior = prior_parameters('gaussian')
        groups = [matching_designs(family, retained_information(J, 'diag'), 'diag') for J in family]
        for group in groups:
            np.testing.assert_array_equal(group, np.arange(4))
        exact = conditional_posterior(b, family, groups[0], prior)
        plugin = conditional_posterior(b, np.diag(np.diag(family[0]))[None], np.array([0]), prior)
        self.assertGreater(abs(exact.log_prob(b)[0] - plugin.log_prob(b)[0]), .01)

    def test_full_side_input_closes_all_gaps_and_decomposition_is_pointwise(self):
        results = evaluate_cell('mixture', .45, 17, 32)
        for (regime, _), r in results.items():
            np.testing.assert_allclose(r['total_gap_nats'], r['compression_nats']+r['fitting_nats'], atol=1e-12)
            if regime == 'full_operator':
                np.testing.assert_allclose(r['total_gap_nats'], 0, atol=1e-12)
                np.testing.assert_allclose(r['epsilon_predictor_gap'], 0, atol=1e-12)

    def test_event_generation_is_reproducible_and_keeps_views_together(self):
        prior = prior_parameters('gaussian')
        first = paired_events(prior, 9, 16)
        second = paired_events(prior, 9, 16)
        for a, b in zip(first, second):
            np.testing.assert_array_equal(a, b)
        self.assertEqual(first[0].shape, (16, 4))
        self.assertEqual(first[1].shape, (16, 4, 4))
        self.assertFalse(np.allclose(first[1][:, 0], first[1][:, 1]))

    def test_diffusion_pure_noise_has_zero_epsilon_condition_gap(self):
        family, prior = acquisition_family(.45), prior_parameters('mixture')
        b = np.array([[1., 0., -.5, .7]])
        p = conditional_posterior(b, family, np.arange(4), prior)
        noisy = np.array([[.1, -.2, .7, .9]])
        predicted = (noisy - 0*p.denoising_mean(noisy, 0, 1))/1
        np.testing.assert_array_equal(predicted, noisy)

    def test_jacobian_is_detected_when_design_determinants_differ(self):
        family = np.tile(1.5*np.eye(4), (2, 1, 1))
        family[:, 0, 1] = family[:, 1, 0] = [.1, 1.3]
        b = np.array([[.4, -.2, .3, 1.]])
        prior = prior_parameters('gaussian')
        group = matching_designs(family, retained_information(family[0], 'diag'), 'diag')
        exact = conditional_posterior(b, family, group, prior)
        raw_logs, log_determinants = [], []
        for J in family:
            A = np.linalg.cholesky(J).T
            x = np.linalg.solve(A.T, b.T).T
            raw_logs.append(_lognormal(x, np.zeros(4), A@A.T+np.eye(4))[0])
            log_determinants.append(np.linalg.slogdet(A)[1])
        raw_logs, log_determinants = np.array(raw_logs), np.array(log_determinants)
        corrected = np.exp(raw_logs-log_determinants-np.max(raw_logs-log_determinants))
        corrected /= corrected.sum()
        omitted = np.exp(raw_logs-raw_logs.max()); omitted /= omitted.sum()
        np.testing.assert_allclose(np.exp(exact.log_weights[0]), corrected, atol=1e-12)
        self.assertGreater(np.max(np.abs(corrected-omitted)), .1)

    def test_design_subset_cannot_reweight_or_truncate_indices(self):
        family, prior = acquisition_family(.45), prior_parameters('gaussian')
        for indices in ([0, 0, 1], [0.9, 1.9], [[0, 1]], [True, False], []):
            with self.subTest(indices=indices), self.assertRaises(ValueError):
                conditional_posterior(np.zeros((1, 4)), family, np.asarray(indices), prior)

    def test_prior_components_cannot_be_silently_dropped(self):
        family = acquisition_family(.45)
        weights, means, covs = prior_parameters('mixture')
        for prior in ((weights, means[:1], covs), (weights, means, covs[:1]),
                      (np.array([.2, .2]), means, covs)):
            with self.assertRaises(ValueError):
                conditional_posterior(np.zeros((1, 4)), family, np.arange(4), prior)

    def test_nonsymmetric_or_indefinite_prior_is_not_a_covariance(self):
        family = acquisition_family(.45)
        weights, means, covs = prior_parameters('gaussian')
        asymmetric = covs.copy(); asymmetric[0, 0, 1] = .4
        indefinite = covs.copy(); indefinite[0, 0, 0] = -1.
        with self.assertRaises(ValueError):
            conditional_posterior(np.zeros((1, 4)), family, np.arange(4), (weights, means, asymmetric))
        with self.assertRaises(np.linalg.LinAlgError):
            conditional_posterior(np.zeros((1, 4)), family, np.arange(4), (weights, means, indefinite))

    def test_plot_only_does_not_call_the_experiment(self):
        from experiments.synthetic_known_pole import run_compression as runner
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)/'results.csv'
            source.write_text('prior,cross_coupling,side_information,arm,total_gap_nats,'
                              'total_gap_nats_lo,total_gap_nats_hi,coverage_50,coverage_80,coverage_90\n'
                              'gaussian,0.45,coarse,diag_exact,0.1,0.08,0.12,0.5,0.8,0.9\n')
            with patch('sys.argv', ['run_compression', '--plot-only', str(source),
                                   '--output-dir', directory]), \
                 patch.object(runner, 'run_experiment', side_effect=AssertionError('must not simulate')), \
                 patch.object(runner, 'plot_results') as plot:
                runner.main()
                plot.assert_called_once()
                self.assertEqual(plot.call_args.args[0][0]['cross_coupling'], .45)

if __name__ == '__main__':
    unittest.main()
