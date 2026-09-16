import unittest
import numpy as np
from experiments.p19.policy_certificate import certify, evaluate_rows
from experiments.p19.certified_selection_demo import experiment


class CertificateTests(unittest.TestCase):
    def test_radius_and_insufficient_evidence(self):
        r=certify(np.full(64,.3),np.full((64,3),.2),np.zeros(3),margin=.01)
        self.assertAlmostEqual(r['radius'],np.sqrt(2*np.log(60)/64))
        self.assertEqual(r['selected_index'],-1)
    def test_large_sample_and_cost(self):
        r=certify(np.full(2048,.3),np.full((2048,3),.2),np.zeros(3),margin=.01)
        self.assertEqual(r['selected_index'],0)
        self.assertEqual(certify(np.full(2048,.3),np.full((2048,3),.2),np.full(3,.1))['selected_index'],-1)
    def test_shift_bound_is_explicit(self):
        r=certify(np.full(2048,.3),np.full((2048,1),.2),[0],shift_bound=.1)
        self.assertEqual(r['selected_index'],-1)
    def test_no_clipping_unbounded_loss(self):
        with self.assertRaises(ValueError):certify([2],[[.1]],[0])
    def test_multiple_comparisons_are_counted(self):
        a=certify(np.ones(100),np.zeros((100,1)),[0])
        b=certify(np.ones(100),np.zeros((100,10)),np.zeros(10))
        self.assertGreater(b['radius'],a['radius'])
    @staticmethod
    def rows():
        return [dict(split=s,group_id=f'{s}:{i}',policy=p,loss=v,cost_penalty=0)
                for s in ['calibration','test'] for i in range(128) for p,v in [('ref',.4),('candidate',.1)]]
    def test_test_scores_cannot_choose_the_policy(self):
        rows=self.rows();a=evaluate_rows(rows,'ref')
        for r in rows:
            if r['split']=='test':r['loss']=1-float(r['loss'])
        b=evaluate_rows(rows,'ref')
        self.assertEqual(a['selected_policy'],b['selected_policy'])
        self.assertLess(b['realized_test_net_improvement'],0)
    def test_duplicate_and_missing_group_rejected(self):
        rows=self.rows()
        with self.assertRaises(ValueError):evaluate_rows(rows+[rows[0]],'ref')
        with self.assertRaises(ValueError):evaluate_rows(rows[1:],'ref')
    def test_overlapping_groups_rejected(self):
        rows=self.rows()
        for r in rows:r['group_id']=r['group_id'].split(':')[1]
        with self.assertRaises(ValueError):evaluate_rows(rows,'ref')
    def test_cost_is_not_sampled_latency(self):
        rows=self.rows();rows[0]['cost_penalty']=1
        with self.assertRaises(ValueError):evaluate_rows(rows,'ref')
    def test_shift_sensitivity_reuses_same_draws(self):
        results,raw=experiment(2048,0)
        a,b=results[2:]
        self.assertAlmostEqual(a['best_lower_bound']-b['best_lower_bound'],.4)
        self.assertEqual(a['selected_policy'],'hard_source_route')
        self.assertEqual(b['selected_policy'],'static_reference')
        self.assertLess(a['test_net_improvement'],0)
        self.assertEqual(b['test_net_improvement'],0)

if __name__=='__main__':unittest.main()
