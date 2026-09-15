import csv
import tempfile
import unittest
from pathlib import Path
import numpy as np
from experiments.p19.routing import weighted_headroom, conditional_regret, fit_static_squared
from experiments.p19.toy_routing import check_boundaries, run
from experiments.p19.statistics import read_rows, summarize
from experiments.p19.plot import plot_rows

class SelectionTests(unittest.TestCase):
    def test_nonuniform_weights(self):
        self.assertAlmostEqual(weighted_headroom([[0,1],[1,0]],[.9,.1]),.1)
    def test_no_headroom_does_not_rule_out_fusion(self):
        check_boundaries()
        self.assertAlmostEqual(fit_static_squared([[0,1],[0,1]],[.25,.40]),.325)
    def test_regret_with_transport_error(self):
        source=np.array([[.1,.3],[.3,.1]]);target=source[:,::-1]
        regret=conditional_regret(target,np.argmin(source,axis=1),[.5,.5])
        self.assertAlmostEqual(regret,.2)
        self.assertLessEqual(regret,2*np.max(abs(target-source)))
    def test_toy_uses_independent_simulated_test_events(self):
        rows,summary=run(64,0)
        self.assertEqual(len(summary),24);self.assertEqual(len(rows),4*6*2*64)
        self.assertTrue(all(np.isfinite(r['test_mse']) for r in summary))
    def test_duplicate_rows_rejected(self):
        row=dict(method='R',condition_id='a',group_id='g',seed='0',unit_id='u',value=1)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'x.csv'
            with path.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(row));w.writeheader();w.writerows([row,row])
            with self.assertRaises(ValueError):read_rows(path)
    def test_group_balanced_not_window_balanced(self):
        rows=[]
        for g,n,loss in [('g0',10,0),('g1',1,2)]:
            for i in range(n):
                for m,value in [('R',loss),('M',0)]:rows.append(dict(method=m,condition_id='a',group_id=g,seed='0',unit_id=str(i),value=value))
        self.assertAlmostEqual(summarize(rows,'R',draws=50)[0]['effect_positive_is_better'],1)
    def test_unpaired_units_rejected(self):
        rows=[dict(method=m,condition_id='a',group_id='g',seed='0',unit_id=m,value=0) for m in ['R','M']]
        with self.assertRaises(ValueError):summarize(rows,'R')
    def test_interval_outside_point_is_not_clipped(self):
        rows=[dict(method='M',condition_id='a',groups=3,effect_positive_is_better=0,ci_low=1,ci_high=2)]
        with tempfile.TemporaryDirectory() as d:
            plot_rows(rows,d)
            self.assertTrue(all((Path(d)/f'paired_effects.{ext}').is_file() for ext in ['svg','pdf','png']))

class ClassificationTests(unittest.TestCase):
    def test_f1_is_recomputed_not_averaged(self):
        from experiments.p19.phm_metrics import confusion_metrics
        y=[0]*10+[1];pred=[0]*11;groups=['a']*10+['b']
        acc,f1=confusion_metrics(y,pred,groups,classes=2)
        self.assertAlmostEqual(acc,.5);self.assertAlmostEqual(f1,1/3)
    def test_ontology_not_truncated(self):
        from experiments.p19.phm_metrics import confusion_metrics
        with self.assertRaises(ValueError):confusion_metrics([0.5],[0])

if __name__=='__main__':unittest.main()
