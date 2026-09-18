import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from experiments.p19.prediction_agreement import agreement, fit_static, load_bank, evaluate, plot_csv

class PredictionAgreementTests(unittest.TestCase):
    def test_common_label_is_preserved_for_arbitrary_convex_weights(self):
        x=np.array([[[2.,1.],[0.,3.]],[[.8,.7],[-1.,2.]]])
        same,margin=agreement(x)
        self.assertTrue(same.all());self.assertGreater(margin.min(),0)
        for weight in np.linspace(0,1,21):
            np.testing.assert_array_equal((weight*x[0]+(1-weight)*x[1]).argmax(1),x[0].argmax(1))
    def test_disagreement_or_tie_is_not_strict_agreement(self):
        self.assertFalse(agreement(np.array([[[1.,0.]],[[0.,1.]]]))[0].all())
        self.assertEqual(agreement(np.array([[[1.,1.]],[[2.,1.]]]))[1][0],0)
    def test_unbounded_nonprobability_scores_are_not_normalized(self):
        x=np.array([[[100.,90.]],[[3.,-2.]]])
        same,margin=agreement(x);self.assertTrue(same.all());self.assertEqual(margin[0],5)
    def test_agreement_does_not_prove_equal_score_quality(self):
        a=np.array([[.51,.49]]);b=np.array([[.99,.01]])
        self.assertTrue(agreement(np.stack([a,b]))[0].all())
        self.assertNotEqual(np.mean((a-[1,0])**2),np.mean((b-[1,0])**2))
    def test_static_selection_does_not_read_test_truth(self):
        models=['a','b'];base=np.array([[[.6,.4],[.4,.6]],[[.9,.1],[.1,.9]]])
        bank={s:([s+'0',s+'1'],np.array([0,1]),base.copy()) for s in ['validation','calibration','test']}
        a,_=evaluate(models,bank,'a','b')
        bank['test']=(bank['test'][0],1-bank['test'][1],bank['test'][2])
        b,_=evaluate(models,bank,'a','b')
        self.assertEqual(a[0]['static_alpha'],b[0]['static_alpha'])
        self.assertNotEqual(a[-1]['accuracy'],b[-1]['accuracy'])
    def test_frozen_reference_tie(self):
        x=np.array([[.1,.9]])
        self.assertEqual(fit_static(x,x,np.array([1])),0)
    @staticmethod
    def rows():
        return [dict(model=m,split=s,group_id=s,y_true=0,y_pred=0,score_0=.8,score_1=.2)
                for s in ['validation','calibration','test'] for m in ['a','b']]
    def parse(self,rows):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'data.csv'
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
            return load_bank(p,2)
    def test_exact_pairing_and_duplicate_validation(self):
        self.parse(self.rows())
        with self.assertRaises(ValueError):self.parse(self.rows()[:-1])
        with self.assertRaises(ValueError):self.parse(self.rows()+[self.rows()[0]])
    def test_cross_split_original_ids_are_rejected(self):
        rows=self.rows()
        for r in rows:r['group_id']='same'
        with self.assertRaises(ValueError):self.parse(rows)
    def test_truth_and_decision_are_verified(self):
        rows=self.rows();rows[1]['y_true']=1
        with self.assertRaises(ValueError):self.parse(rows)
        rows=self.rows();rows[0]['y_pred']=1
        with self.assertRaises(ValueError):self.parse(rows)
    def test_plot_does_not_load_prediction_bank(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'summary.csv'
            rows=[dict(split=s,model='a',minimum_bank_label_margin=.1,onehot_score_mse=.2)
                  for s in ['validation','calibration','test']]
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
            with patch('experiments.p19.prediction_agreement.load_bank',side_effect=AssertionError('must not load')):
                plot_csv(p,Path(d)/'figures')
            self.assertTrue(all((Path(d)/'figures'/f'agreement_margin.{e}').exists() for e in ['svg','pdf','png']))

if __name__=='__main__':unittest.main()
