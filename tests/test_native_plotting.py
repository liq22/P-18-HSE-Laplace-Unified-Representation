"""Pairing and original-group aggregation for the primary M/B1-aux result."""
import unittest
from paper.plot_native import comparison_summary

class NativePlottingTests(unittest.TestCase):
    def rows(self):
        # Group a has three windows; group b one. Give groups equal, not window, weight.
        rows=[]
        for event, group, delta in [('a0','a',1.),('a1','a',1.),('a2','a',1.),('b0','b',-1.)]:
            for seed in ['0','1','2']:
                for arm in ['B1_aux','M']:
                    rows.append(dict(condition_id='held_out',event_id=event,group_id=group,
                                     seed=seed,arm=arm,energy_score=2.+(delta if arm=='M' else 0)))
        return rows

    def test_groups_not_windows_define_average(self):
        result=comparison_summary(self.rows(),64)[0]
        self.assertEqual(result['paired_delta'],0.)
        self.assertEqual(result['groups'],2)
        self.assertEqual(result['events'],4)
        self.assertEqual(result['training_seeds'],3)

    def test_unmatched_arm_is_not_silently_dropped(self):
        with self.assertRaises(ValueError): comparison_summary(self.rows()[:-1],8)

    def test_shared_group_identity_must_agree(self):
        rows=self.rows(); rows[-1]['group_id']='other'
        with self.assertRaises(ValueError): comparison_summary(rows,8)

    def test_duplicate_result_is_rejected(self):
        rows=self.rows()
        with self.assertRaises(ValueError): comparison_summary(rows+[rows[0]],8)

    def test_missing_seed_in_both_arms_is_not_reweighted(self):
        rows=[r for r in self.rows() if not (r['event_id']=='a0' and r['seed']=='2')]
        with self.assertRaises(ValueError): comparison_summary(rows,8)

if __name__=='__main__': unittest.main()
