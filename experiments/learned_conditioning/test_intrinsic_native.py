"""Scientific path tests; native tests require the original installed LLapDiff."""
import unittest
import torch
from .intrinsic_native import eligible_basis, intrinsic_velocity_loss, intrinsic_ddim


class GeometryTests(unittest.TestCase):
    def test_nondiagonal_joint_block(self):
        operator = torch.tensor([[1., 1., 0., 0.]], dtype=torch.float64)
        joint = torch.eye(4, dtype=torch.float64)[:, :3]
        basis = eligible_basis(operator, joint)
        self.assertEqual(tuple(basis.shape), (4, 2))
        torch.testing.assert_close(basis.T @ basis, torch.eye(2, dtype=basis.dtype), atol=1e-12, rtol=0)
        torch.testing.assert_close(operator @ basis, torch.zeros(1, 2, dtype=basis.dtype), atol=1e-12, rtol=0)
        self.assertEqual(float(basis[3].abs().max()), 0.)

    def test_empty_target_does_not_call_model(self):
        basis = eligible_basis(torch.eye(4), torch.eye(4))
        observed = torch.randn(2, 6, 4)
        result = intrinsic_ddim(object(), basis, torch.empty(2, 1, 16), torch.zeros(2, 6),
                                observed, [], generator=torch.Generator())
        self.assertEqual(tuple(result.shape), (2, 6, 0))


class NativePathTests(unittest.TestCase):
    def setUp(self):
        from llapdiffusion.models.llapdiff import LLapDiff
        torch.set_num_threads(1); torch.manual_seed(19)
        self.model = LLapDiff(data_dim=4, hidden_dim=16, num_layers=1, num_heads=2,
                             laplace_k=4, predict_type='v', timesteps=64,
                             dropout=0., attn_dropout=0., block_summary_adaln=True,
                             analysis_summary_qk=True)
        self.z = torch.randn(2, 6, 4)
        self.c = torch.randn(2, 2, 16)
        self.time = torch.arange(6).repeat(2, 1).float() * .01
        self.t = torch.tensor([13, 51])

    def test_full_basis_matches_original_velocity_loss(self):
        from llapdiffusion.models.llapdiff_utils import diffusion_loss
        noise = torch.randn_like(self.z)
        self.model.eval()
        loss, details = intrinsic_velocity_loss(self.model, self.z, torch.eye(4), self.c,
                                                self.time, self.t, noise)
        xt, _ = self.model.scheduler.q_sample(self.z, self.t, noise=noise)
        native = diffusion_loss(self.model, self.model.scheduler, self.z, self.t,
                                cond_summary=self.c, dt=self.time, predict_type='v',
                                weight_scheme='none', minsnr_normalize='none',
                                target_mask=torch.ones(2, 6, dtype=torch.bool),
                                reuse_xt_eps=(xt, noise))
        torch.testing.assert_close(loss, native, atol=2e-6, rtol=1e-6)
        self.assertLess(details['clean_weight_identity_error'], 2e-6)

    def test_restricted_gradient_sampling_and_no_hidden_target(self):
        operator = torch.eye(4)[:2]
        basis = eligible_basis(operator, torch.eye(4))
        noise = torch.randn(2, 6, 2)
        loss, _ = intrinsic_velocity_loss(self.model, self.z, basis, self.c, self.time, self.t, noise)
        changed_complement = self.z.clone(); changed_complement[..., :2] += 100
        alternate, _ = intrinsic_velocity_loss(self.model, changed_complement, basis,
                                               self.c, self.time, self.t, noise)
        torch.testing.assert_close(loss, alternate, rtol=0, atol=0)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=.001)
        optimizer.zero_grad(set_to_none=True); loss.backward()
        self.assertGreater(sum(float(p.grad.abs().sum()) for p in self.model.parameters() if p.grad is not None), 0)
        optimizer.step(); self.model.eval()
        observed = self.z @ (torch.eye(4) - basis @ basis.T)
        trace = []
        result = intrinsic_ddim(self.model, basis, self.c, self.time, observed, [63, 31, 1],
                                generator=torch.Generator().manual_seed(3), trace=trace.append)
        self.assertEqual(tuple(result.shape), (2, 6, 2))
        self.assertTrue(torch.isfinite(result).all())
        self.assertEqual(len(trace), 3)
        self.assertLess(max(x['forbidden_max_abs'] for x in trace), 1e-6)
        self.assertLess(max(x['observed_drift_max_abs'] for x in trace), 1e-6)


if __name__ == '__main__':
    unittest.main()
