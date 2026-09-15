import tempfile
import unittest
from pathlib import Path
import numpy as np
import torch
from .feature_data import load_features, check_splits
from .run_native_pilot import energy_score

class ExportTests(unittest.TestCase):
    def fixture(self, prefix='a'):
        return dict(tokens=np.ones((4,4,8),dtype=np.float32),attention_mask=np.ones((4,4),dtype=bool),
            side=np.ones((4,1),dtype=np.float32),side_names=np.array(['sampling_rate_hz']),
            targets=np.ones((4,2),dtype=np.float32),event_id=np.array([f'{prefix}{i}' for i in range(4)]),
            group_id=np.array([f'{prefix}record{i}' for i in range(4)]),condition_id=np.array(['low']*4))

    def load(self, data, directory, name):
        path=Path(directory)/name;np.savez(path,**data);return load_features(path)

    def test_missing_mask_cannot_be_assumed_valid(self):
        with tempfile.TemporaryDirectory() as d:
            data=self.fixture();del data['attention_mask']
            with self.assertRaises(ValueError):self.load(data,d,'a.npz')

    def test_distinct_events_do_not_hide_a_shared_recording(self):
        with tempfile.TemporaryDirectory() as d:
            left=self.fixture('a');right=self.fixture('b');right['group_id'][0]=left['group_id'][0]
            with self.assertRaises(ValueError):check_splits(self.load(left,d,'a.npz'),self.load(right,d,'b.npz'))

    def test_side_column_semantics_are_fixed(self):
        with tempfile.TemporaryDirectory() as d:
            left=self.fixture('a');right=self.fixture('b');right['side_names']=np.array(['noise_sd'])
            with self.assertRaises(ValueError):check_splits(self.load(left,d,'a.npz'),self.load(right,d,'b.npz'))

    def test_valid_exports_keep_acquisition_groups_for_reporting(self):
        with tempfile.TemporaryDirectory() as d:
            a=self.load(self.fixture('a'),d,'a.npz');b=self.load(self.fixture('b'),d,'b.npz')
            check_splits(a,b)
            self.assertEqual(a['condition_id'][0],'low');self.assertEqual(a['tokens'].shape,(4,4,8))

    def test_energy_score_ignores_only_explicitly_masked_targets(self):
        target=torch.tensor([[[1.],[7.]]]);mask=torch.tensor([[True,False]])
        samples=target[None].repeat(3,1,1,1);samples[:,:,1,:]=-100
        torch.testing.assert_close(energy_score(samples,target,mask),torch.zeros(1))
        with self.assertRaises(ValueError):energy_score(samples[:1],target,mask)

if __name__=='__main__':unittest.main()
