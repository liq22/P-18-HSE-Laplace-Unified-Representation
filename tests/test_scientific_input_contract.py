import unittest
import numpy as np
from experiments.sampled_conditioning.core import gaussian_kl
from experiments.p19.statistics import summarize


class GaussianMeanContractTests(unittest.TestCase):
    def test_correct_vector_value(self):
        self.assertAlmostEqual(gaussian_kl([0,0],np.eye(2),[1,2],np.eye(2)),2.5)
    def test_wrong_length_both_sides(self):
        for bad in ([0.], [0.,1.,2.]):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):gaussian_kl(bad,np.eye(2),[1,2],np.eye(2))
                with self.assertRaises(ValueError):gaussian_kl([1,2],np.eye(2),bad,np.eye(2))
    def test_scalar_and_column(self):
        for bad in (0., [[0.],[0.]]):
            with self.assertRaises(ValueError):gaussian_kl(bad,np.eye(2),[1,2],np.eye(2))
    def test_nonfinite_both_sides(self):
        for value in (np.nan,np.inf,-np.inf):
            with self.assertRaises(ValueError):gaussian_kl([0,value],np.eye(2),[1,2],np.eye(2))
            with self.assertRaises(ValueError):gaussian_kl([1,2],np.eye(2),[0,value],np.eye(2))
    def test_mismatched_covariance_dimension(self):
        with self.assertRaises(ValueError):gaussian_kl([0,0],np.eye(2),[0],np.eye(1))
    def test_no_zero_dimensional_distribution(self):
        with self.assertRaises(ValueError):gaussian_kl([],np.eye(0),[],np.eye(0))


class GroupSeedContractTests(unittest.TestCase):
    @staticmethod
    def rows():
        return [dict(condition_id='source',group_id=g,seed=str(seed),unit_id='0',method=arm,
                     value=9. if seed==2 and arm=='R' else 0.)
                for g in ['a','b'] for seed in range(3) for arm in ['R','M']]
    def test_common_seed_mixture(self):
        result=summarize(self.rows(),'R',draws=10,expected_seeds=[0,1,2])
        self.assertEqual(result[0]['effect_positive_is_better'],3.)
    def test_joint_missing_seed_in_one_group_is_rejected(self):
        rows=[r for r in self.rows() if not (r['group_id']=='b' and r['seed']=='2')]
        with self.assertRaisesRegex(ValueError,'nonuniform seed set'):summarize(rows,'R')
    def test_global_absence_detected_from_declared_seeds(self):
        rows=[r for r in self.rows() if r['seed']!='2']
        with self.assertRaises(ValueError):summarize(rows,'R',expected_seeds=[0,1,2])
    def test_each_condition_has_its_own_observed_set(self):
        rows=self.rows()
        rows += [dict(r,condition_id='other') for r in self.rows() if r['seed']!='2']
        self.assertEqual(len(summarize(rows,'R',draws=10)),2)
        with self.assertRaises(ValueError):summarize(rows,'R',draws=10,expected_seeds=[0,1,2])

if __name__=='__main__':unittest.main()
