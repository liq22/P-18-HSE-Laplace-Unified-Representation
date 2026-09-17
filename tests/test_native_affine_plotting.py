import unittest
from paper.plot_native import comparison_summary, select_comparison_rows

class NativeAffinePlotTests(unittest.TestCase):
    def rows(self):
        return [dict(arm=arm,seed='0',event_id=f'e{i}',group_id=f'g{i}',condition_id='seen',
                     energy_score=value,posterior_draws='2',sampler_steps='2')
                for i in range(2) for arm,value in [('B1_aux',2.),('M',1.),('head_affine',1.5)]]
    def test_multi_arm_file_requires_explicit_selection(self):
        with self.assertRaises(ValueError):select_comparison_rows(self.rows(),'B1_aux','M')
    def test_named_pair_preserves_correct_direction(self):
        rows=select_comparison_rows(self.rows(),'head_affine','M',explicit=True)
        s=comparison_summary(rows,repetitions=50,reference='head_affine',candidate='M')
        self.assertAlmostEqual(s[0]['paired_delta'],-.5)
        self.assertEqual(s[0]['reference'],'head_affine')
    def test_draw_budget_mismatch_rejected(self):
        rows=select_comparison_rows(self.rows(),'B1_aux','M',explicit=True)
        rows[0]['posterior_draws']='3'
        with self.assertRaises(ValueError):comparison_summary(rows)
    def test_named_pair_cannot_hide_missing_event(self):
        rows=select_comparison_rows(self.rows(),'head_affine','M',explicit=True)
        with self.assertRaises(ValueError):comparison_summary(rows[:-1],reference='head_affine',candidate='M')

if __name__=='__main__':unittest.main()
