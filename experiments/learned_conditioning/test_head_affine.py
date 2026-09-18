"""Exact same-head controls and the actual finite-precision boundary."""
import copy
import unittest
import torch
from .moment_conditioner import MatchedConditioner

class HeadAffineTests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(13)
        self.model = MatchedConditioner(4, 8, 2, 1).double()
        self.x = torch.randn(6, 4, 8, dtype=torch.float64)
        self.mask = torch.ones(6, 4, dtype=torch.bool)
        self.mask[:, 0] = False
        self.side = torch.randn(6, 1, dtype=torch.float64)
        self.model.freeze_for_denoising()

    def test_exact_shared_head_prefix_and_tail(self):
        model = self.model
        r = model(self.x, self.mask, self.side, 'B1_aux').flatten(1)
        a = model(self.x, self.mask, self.side, 'head_affine').flatten(1)
        m = model(self.x, self.mask, self.side, 'M').flatten(1)
        torch.testing.assert_close(a[:, :model.semantic_size], model.moment_head(r), rtol=0, atol=0)
        torch.testing.assert_close(a[:, model.semantic_size:], r[:, model.semantic_size:], rtol=0, atol=0)
        torch.testing.assert_close(a[:, :model.target_dim], m[:, :model.target_dim], rtol=0, atol=0)
        self.assertGreater(float((a[:, model.target_dim:model.semantic_size]-m[:, model.target_dim:model.semantic_size]).abs().max()), .1)
        self.assertEqual(a.numel()*a.element_size(), m.numel()*m.element_size())

    def test_affine_consumer_exact_collapse(self):
        model = self.model
        r = model(self.x, self.mask, self.side, 'B1_aux').flatten(1)
        a = model(self.x, self.mask, self.side, 'head_affine').flatten(1)
        transform = torch.eye(model.budget, dtype=torch.float64)
        offset = torch.zeros(model.budget, dtype=torch.float64)
        transform[:model.semantic_size] = model.moment_head.weight
        offset[:model.semantic_size] = model.moment_head.bias
        consumer = torch.nn.Linear(model.budget, 3).double()
        collapsed = torch.nn.functional.linear(r, consumer.weight @ transform,
                                               consumer.bias + consumer.weight @ offset)
        error = float((consumer(a)-collapsed).abs().max().detach())
        torch.testing.assert_close(consumer(a), collapsed, rtol=0, atol=1e-14)
        print('head_affine_consumer_collapse_max_error=', error)

    def test_same_parameters_frozen_and_masked_history_excluded(self):
        model = self.model
        before = copy.deepcopy(model.state_dict())
        n = sum(p.numel() for p in model.parameters())
        reference = model(self.x, self.mask, self.side, 'head_affine')
        changed = self.x.clone(); changed[:, 0] = float('nan')
        model.train()
        torch.testing.assert_close(reference, model(changed, self.mask, self.side, 'head_affine'), rtol=0, atol=0)
        self.assertEqual(n, sum(p.numel() for p in model.parameters()),)
        self.assertFalse(model.training)
        for key, value in model.state_dict().items():
            torch.testing.assert_close(before[key], value, rtol=0, atol=0)

    def test_statistical_map_reconstructed_from_head_message(self):
        model = self.model
        a = model(self.x, self.mask, self.side, 'head_affine').flatten(1)
        factor = torch.zeros(len(a), model.target_dim, model.target_dim, dtype=a.dtype)
        factor[:, model.tril[0], model.tril[1]] = a[:, model.target_dim:model.semantic_size]
        i = torch.arange(model.target_dim)
        factor[:, i, i] = torch.nn.functional.softplus(factor[:, i, i])
        covariance = factor @ factor.transpose(-1,-2) + model.covariance_floor*torch.eye(model.target_dim, dtype=a.dtype)
        c = torch.linalg.cholesky(covariance)
        reconstructed = torch.cat((a[:, :model.target_dim], c[:, model.tril[0], model.tril[1]], a[:, model.semantic_size:]), -1)
        direct = model(self.x, self.mask, self.side, 'M').flatten(1)
        torch.testing.assert_close(reconstructed, direct, rtol=0, atol=0)

    def test_public_floor_can_hide_distinct_codes_in_float32(self):
        gaps={}
        for dtype in (torch.float32,torch.float64):
            model=MatchedConditioner(4,8,2,0,covariance_floor=1e-4).to(dtype)
            with torch.no_grad():
                model.moment_head.weight.zero_();model.moment_head.bias.zero_()
                model.moment_head.weight[:,:5]=torch.eye(5,dtype=dtype)
                code=torch.zeros(2,32,dtype=dtype)
                code[:,2]=torch.tensor([-14.,-15.],dtype=dtype)
                raw=model.moment_head(code)
                mean,factor=model.moments_from_code(code)
                message=torch.cat((mean,factor[:,model.tril[0],model.tril[1]],code[:,5:]),1)
            self.assertEqual(int(torch.linalg.matrix_rank(model.moment_head.weight[:,:5])),5)
            self.assertEqual(float((raw[0]-raw[1]).abs().max()),1.)
            gaps[str(dtype)]=float((message[0]-message[1]).abs().max())
        self.assertEqual(gaps['torch.float32'],0.)
        self.assertGreater(gaps['torch.float64'],1e-11)
        print('same_head_precision_fixture:',gaps,'rank=5; not a trained-checkpoint observation')

if __name__ == '__main__': unittest.main()
