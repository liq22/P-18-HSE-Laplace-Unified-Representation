"""Native loop test with EXPLICIT synthetic fixtures, not a benchmark."""
import csv
import tempfile
import unittest
from pathlib import Path
import torch
from .fit_moment_probe import generate
from .run_native_pilot import pilot

class NativePilotControlTests(unittest.TestCase):
    def test_three_arms_share_checkpoint_and_complete_real_native_loop(self):
        torch.set_num_threads(1)
        splits=[]
        for seed in [91,92,93]:
            data=generate(4,seed)
            g=torch.Generator().manual_seed(seed+100)
            data['z0']=torch.randn(4,4,2,generator=g)
            data['target_mask']=torch.ones(4,4,dtype=torch.bool)
            data['query_time_s']=torch.arange(4)[None,:].repeat(4,1).float()*.01
            data['targets']=data['z0'][:,0].clone()
            splits.append(data)
        with tempfile.TemporaryDirectory() as d:
            output=Path(d)
            pilot(*splits,[0],1,1,2,2,torch.device('cpu'),output,
                  ('B1_aux','M','head_affine'))
            with (output/'event_scores.csv').open() as f: rows=list(csv.DictReader(f))
            self.assertEqual(len(rows),12)
            self.assertEqual({r['arm'] for r in rows},{'B1_aux','M','head_affine'})
            self.assertTrue(all(torch.isfinite(torch.tensor(float(r['energy_score']))) for r in rows))
            checkpoints=[torch.load(output/f'{a}_seed0.pt',map_location='cpu',weights_only=False)
                         for a in ('B1_aux','M','head_affine')]
            for ckpt in checkpoints:
                self.assertEqual(ckpt['selected_step'],1)
                for key,value in ckpt['conditioner'].items():
                    torch.testing.assert_close(value,checkpoints[0]['conditioner'][key],rtol=0,atol=0)
            with (output/'costs.csv').open() as f: costs=list(csv.DictReader(f))
            self.assertEqual({int(r['message_bytes_per_event']) for r in costs},{128})
            self.assertEqual(len({r['denoiser_parameters'] for r in costs}),1)
            # Plot actual generated score rows, never an expected performance curve.
            from paper.plot_native import select_comparison_rows, render_comparison
            pair=select_comparison_rows(rows,'head_affine','M',explicit=True)
            render_comparison(pair,output/'figures','head_affine','M')
            self.assertTrue(all((output/'figures'/f'native_paired_comparison.{ext}').is_file()
                                for ext in ('svg','pdf','png')))
            print('native_three_arm_integration: checkpoints=3 event_scores=12 figures=3; synthetic fixture, no method result')

if __name__=='__main__':unittest.main()
