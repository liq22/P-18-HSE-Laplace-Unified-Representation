"""Scientific behavior checks. Synthetic inputs are interface witnesses only."""
import copy
import unittest
import torch
from .moment_conditioner import MatchedConditioner

class MatchedConditionerTests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(17)
        self.h = torch.randn(6, 4, 8)
        self.mask = torch.ones(6, 4, dtype=torch.bool)
        self.mask[:, 0] = False
        self.side = torch.randn(6, 2)
        self.y = torch.randn(6, 2)
        self.model = MatchedConditioner(4, 8, 2, 2)

    def test_auxiliary_gradient_updates_consumed_ordinary_path(self):
        before = self.model.ordinary(self.h, self.mask, self.side).detach().clone()
        optimizer = torch.optim.SGD(self.model.parameters(), lr=.01)
        loss = self.model.score_parts(self.h, self.mask, self.side, self.y)['score'].mean()
        loss.backward()
        self.assertGreater(sum(float(p.grad.abs().sum()) for p in self.model.trunk.parameters()), 0)
        optimizer.step()
        after = self.model.ordinary(self.h, self.mask, self.side).detach()
        self.assertGreater(float((before-after).abs().max()), 1e-6)
        self.model.freeze_for_denoising()
        torch.testing.assert_close(self.model(self.h, self.mask, self.side, 'B1_aux').flatten(1), after)

    def test_unused_auxiliary_head_is_rejected_by_the_gradient_witness(self):
        ordinary = self.model.ordinary(self.h, self.mask, self.side)
        detached = ordinary.detach()
        mean, factor = self.model.moments_from_code(detached)
        (mean.square().sum()+factor.square().sum()).backward()
        self.assertTrue(all(p.grad is None for p in self.model.trunk.parameters()))

    def test_mask_excludes_values_but_preserves_global_readout(self):
        changed = self.h.clone(); changed[:, 0] = float('nan')
        torch.testing.assert_close(self.model.ordinary(self.h, self.mask, self.side),
                                   self.model.ordinary(changed, self.mask, self.side))
        self.model.freeze_for_denoising()
        message = self.model(changed, self.mask, self.side)
        self.assertEqual(message.shape, self.h.shape)
        self.assertTrue(torch.isfinite(message).all())
        mean, covariance = self.model.read_moments(message)
        expected = self.model.score_parts(self.h, self.mask, self.side, self.y)
        torch.testing.assert_close(mean, expected['mean'])
        torch.testing.assert_close(covariance, expected['covariance'])

    def test_side_is_consumed_and_explicit(self):
        a = self.model.ordinary(self.h, self.mask, self.side)
        b = self.model.ordinary(self.h, self.mask, self.side+1)
        self.assertGreater(float((a-b).detach().abs().max()), 0)
        with self.assertRaises(ValueError):
            self.model.ordinary(self.h, self.mask, self.side[:, :1])

    def test_freezing_includes_every_conditioning_parameter(self):
        self.model.freeze_for_denoising().train()
        self.assertFalse(self.model.training)
        self.assertFalse(any(p.requires_grad for p in self.model.parameters()))
        before = copy.deepcopy(self.model.state_dict())
        a = self.model(self.h, self.mask, self.side, 'M')
        b = self.model(self.h, self.mask, self.side, 'M')
        torch.testing.assert_close(a, b, rtol=0, atol=0)
        for key, value in self.model.state_dict().items():
            torch.testing.assert_close(value, before[key], rtol=0, atol=0)
        with self.assertRaises(ValueError):
            self.model(self.h.requires_grad_(), self.mask, self.side)

    def test_positive_floor_is_a_covariance_constraint(self):
        self.model.covariance_floor = .2
        result = self.model.score_parts(self.h, self.mask, self.side, self.y)
        self.assertTrue((result['min_eigenvalue'] >= .2-1e-6).all())
        torch.testing.assert_close(result['score'], .5*(result['logdet']+result['mahalanobis']))

    def test_zero_floor_is_not_a_guarantee_against_likelihood_collapse(self):
        scores = [0.5*2*torch.log(torch.tensor(e)) for e in [1., 1e-4, 1e-8]]
        self.assertLess(scores[2], scores[1]); self.assertLess(scores[1], scores[0])

    def test_common_checkpoint_and_equal_message_budget(self):
        self.model.freeze_for_denoising()
        m = self.model(self.h, self.mask, self.side, 'M')
        b = self.model(self.h, self.mask, self.side, 'B1_aux')
        z = self.model(self.h, self.mask, self.side, 'M0')
        self.assertEqual(m.shape, b.shape)
        torch.testing.assert_close(m.flatten(1)[:, 5:], b.flatten(1)[:, 5:])
        torch.testing.assert_close(m.flatten(1)[:, :5], z.flatten(1)[:, :5])
        self.assertEqual(int(torch.count_nonzero(z.flatten(1)[:, 5:])), 0)

    def test_exact_frozen_T_composition_equals_M(self):
        self.model.freeze_for_denoising()
        ordinary = self.model(self.h, self.mask, self.side, 'B1_aux').flatten(1)
        mean, factor = self.model.moments_from_code(ordinary)
        prefix = torch.cat((mean, factor[:, self.model.tril[0], self.model.tril[1]]), -1)
        composed = torch.cat((prefix, ordinary[:, self.model.semantic_size:]), -1)
        direct = self.model(self.h, self.mask, self.side, 'M').flatten(1)
        torch.testing.assert_close(composed, direct, rtol=0, atol=0)
        consumer = torch.nn.Linear(self.model.budget, 3)
        torch.testing.assert_close(consumer(composed), consumer(direct), rtol=0, atol=0)

    def test_mean_only_and_affine_consumer_collapse_to_affine_R(self):
        self.model.freeze_for_denoising()
        ordinary = self.model(self.h, self.mask, self.side, 'B1_aux').flatten(1)
        mean, _ = self.model.moments_from_code(ordinary)
        q, d = self.model.budget, self.model.target_dim
        transform = torch.eye(q)
        shift = torch.zeros(q)
        transform[:d] = self.model.moment_head.weight[:d]
        shift[:d] = self.model.moment_head.bias[:d]
        mean_only = torch.cat((mean, ordinary[:, d:]), -1)
        consumer = torch.nn.Linear(q, 3)
        collapsed = torch.nn.functional.linear(ordinary, consumer.weight @ transform,
                                               consumer.bias + consumer.weight @ shift)
        torch.testing.assert_close(consumer(mean_only), collapsed, rtol=1e-5, atol=1e-6)

    def test_invalid_history_and_unfrozen_message_fail(self):
        with self.assertRaises(ValueError):
            self.model.ordinary(self.h, torch.zeros_like(self.mask), self.side)
        with self.assertRaises(RuntimeError):
            self.model(self.h, self.mask, self.side)

if __name__ == '__main__':
    torch.set_num_threads(1)
    unittest.main()
