"""Numerical checks protect the equations and actual transmitted condition."""
import unittest
import numpy as np
from experiments.sampled_conditioning.core import (
    gaussian_kl, precision_certificate, retained_matrix, encode_header, decode_header,
    expected_plugin_kl, choose_pattern, sampled_design,
)
from experiments.sampled_conditioning.run import evaluate_design

class PrecisionBudgetTests(unittest.TestCase):
    def test_bound_and_identity_with_noncommuting_precisions(self):
        rng = np.random.default_rng(12)
        for _ in range(30):
            a, b = rng.normal(size=(4,4)), rng.normal(size=(4,4))
            p, q = a@a.T+np.eye(4), b@b.T+np.eye(4)
            eta, eta_q = rng.normal(size=4), rng.normal(size=4)
            result = precision_certificate(p, eta, q, eta_q)
            direct = gaussian_kl(np.linalg.solve(p,eta),np.linalg.inv(p),
                                 np.linalg.solve(q,eta_q),np.linalg.inv(q))
            np.testing.assert_allclose(result['kl_nats'],direct,rtol=1e-10,atol=1e-10)
            self.assertLessEqual(direct,result['bound_nats']+1e-9)

    def test_zero_perturbation(self):
        p = np.array([[2., .4],[.4, 3.]])
        result = precision_certificate(p,np.ones(2),p,np.ones(2))
        self.assertEqual(result['kl_nats'],0.)
        self.assertEqual(result['bound_nats'],0.)

    def test_invalid_precision_does_not_get_repaired(self):
        with self.assertRaises(np.linalg.LinAlgError):
            precision_certificate(np.eye(2),np.zeros(2),np.diag([1.,-1.]),np.zeros(2))

    def test_actual_sparse_header_round_trip(self):
        _, a = sampled_design(1024,.08,5.)
        j = a.T@a/.25
        for pattern in [-1,0,1,2]:
            h = encode_header(np.arange(4.),j,pattern)
            self.assertEqual(h.shape,(11,))
            b, kept = decode_header(h)
            np.testing.assert_array_equal(b,np.arange(4.))
            np.testing.assert_allclose(kept,retained_matrix(j,pattern))

    def test_selector_is_minimum_only_in_declared_family(self):
        _, a = sampled_design(1024,.08,30.)
        j = a.T@a/.25
        costs = [expected_plugin_kl(j,retained_matrix(j,k)) for k in range(3)]
        self.assertAlmostEqual(costs[choose_pattern(j)],min(costs))

    def test_expected_risk_matches_independent_prior_predictive_sample(self):
        rng = np.random.default_rng(44)
        _, a = sampled_design(1024,.2,30.)
        beta, noise = rng.normal(size=(40000,4)),rng.normal(size=(40000,len(a)))
        result = evaluate_design(a,beta,noise,'within')
        standard_error = result['kl'].std(ddof=1)/np.sqrt(len(beta))
        self.assertLess(abs(result['kl'].mean()-result['expected_kl']),5*standard_error)

    def test_full_side_information_closes_every_plugin_gap(self):
        rng = np.random.default_rng(9)
        _, a = sampled_design(2048,.08,5.,'block_missing')
        beta,noise = rng.normal(size=(24,4)),rng.normal(size=(24,len(a)))
        for method in ['diag','within','magnitude','risk_oracle','moment_within','moment_best','full']:
            result=evaluate_design(a,beta,noise,method,True)
            np.testing.assert_allclose(result['kl'],0.,atol=1e-10)

    def test_moment_projection_is_not_worse_than_same_partition_plugin(self):
        rng=np.random.default_rng(7)
        _,a=sampled_design(1024,.08,5.)
        beta,noise=rng.normal(size=(64,4)),rng.normal(size=(64,len(a)))
        q=evaluate_design(a,beta,noise,'within')
        moment=evaluate_design(a,beta,noise,'moment_within')
        self.assertTrue(np.all(moment['kl']<=q['kl']+1e-9))
        np.testing.assert_allclose(moment['kl'],moment['expected_kl'],atol=1e-10)

    def test_missingness_is_not_refilled_and_timestamps_are_ordered(self):
        times,_=sampled_design(1024,.08,5.,'block_missing')
        self.assertLess(len(times),64)
        self.assertTrue(np.all(np.diff(times)>0))
        self.assertFalse(np.any((times>.28*.08)&(times<.60*.08)))

if __name__=='__main__':
    unittest.main()
