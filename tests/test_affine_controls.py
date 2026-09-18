import unittest
import numpy as np
from experiments.p19.affine_controls import fit_coordinates, ridge_fit, predict
from experiments.p19.japanese_vowels import parse_sequences, partition, class_metrics


class AffineControlTests(unittest.TestCase):
    def setUp(self):
        rng=np.random.default_rng(7)
        self.x=rng.normal(size=(64,4))*[.1,1,3,10]
        self.xt=rng.normal(size=(20,4))*[.1,1,3,10]
        self.y=rng.normal(size=(64,2))
    def test_transported_penalty_matches_raw_predictions(self):
        c,transforms,_=fit_coordinates(self.x)
        coef,inter=ridge_fit(self.x,self.y,c,transforms['R'],.1)
        ref=predict(self.xt,c,transforms['R'],coef,inter)
        for a in transforms.values():
            w,b=ridge_fit(self.x,self.y,c,a,.1,'matched')
            np.testing.assert_allclose(predict(self.xt,c,a,w,b),ref,atol=1e-10,rtol=0)
    def test_isotropic_whitening_changes_regularization(self):
        c,t,_=fit_coordinates(self.x)
        wr,br=ridge_fit(self.x,self.y,c,t['R'],.1)
        ww,bw=ridge_fit(self.x,self.y,c,t['whitened_R'],.1)
        self.assertGreater(np.max(abs(predict(self.xt,c,t['R'],wr,br)-predict(self.xt,c,t['whitened_R'],ww,bw))),.01)
    def test_rank_deficiency_not_repaired(self):
        with self.assertRaises(ValueError):fit_coordinates(np.ones((20,4)))
    def test_coordinate_shapes_same(self):
        c,t,_=fit_coordinates(self.x)
        for a in t.values():self.assertEqual(((self.x-c)@a).shape,self.x.shape)
    def test_input_arrays_not_modified(self):
        old=self.x.copy();fit_coordinates(self.x)
        np.testing.assert_array_equal(old,self.x)


class VowelsFormatTests(unittest.TestCase):
    def test_variable_length_and_blank_lines(self):
        text=(' '.join(['1']*12)+'\n')*7+'\n'+(' '.join(['2']*12)+'\n')*9
        seq=parse_sequences(text)
        self.assertEqual([len(v) for v in seq],[7,9])
    def test_wrong_channels_and_nonfinite_rejected(self):
        for text in [' '.join(['0']*11), ' '.join(['nan']*12)]:
            with self.assertRaises(ValueError):parse_sequences(text)
    def test_declared_source_partitions(self):
        seq=np.zeros((7,12));parts=partition([seq]*270,[seq]*370)
        self.assertEqual([len(parts[k]) for k in ['train','validation','calibration','test']],[162,54,54,370])
        groups=[gid for rows in parts.values() for gid,_,_ in rows]
        self.assertEqual(len(groups),len(set(groups)))
    def test_full_ontology(self):
        y=np.arange(9);a,f,m=class_metrics(y,np.eye(9))
        self.assertEqual((a,f,m),(1.,1.,0.))

if __name__=='__main__':unittest.main()
