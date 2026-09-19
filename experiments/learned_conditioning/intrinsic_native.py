"""Target-intrinsic velocity training and DDIM with the original LLapDiff.

The caller supplies an identified joint reference and its acquisition operator.
SVD constructs geometry; it does not infer conditional identification. The native
backbone and scheduler are reused, with no substitute denoiser or noise schedule.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
import torch
from torch import Tensor


def eligible_basis(operator: Tensor, joint_basis: Tensor, tolerance: float = 1e-7) -> Tensor:
    """Return an orthonormal basis for range(joint_basis) intersect ker(operator).

joint_basis denotes ONE jointly justified block, not a union of marginal masks.
The normalized operator, reference metric and tolerance are source specifications.
    """
    if operator.ndim != 2 or joint_basis.ndim != 2 or operator.shape[1] != joint_basis.shape[0]:
        raise ValueError('operator and joint basis must share the reference dimension')
    if tolerance <= 0 or not torch.isfinite(operator).all() or not torch.isfinite(joint_basis).all():
        raise ValueError('finite source operators and a positive tolerance are required')
    q = joint_basis.shape[1]
    eye = torch.eye(q, dtype=joint_basis.dtype, device=joint_basis.device)
    if not torch.allclose(joint_basis.T @ joint_basis, eye, atol=tolerance, rtol=0):
        raise ValueError('joint reference basis must be orthonormal in the declared metric')
    _, singular, vh = torch.linalg.svd(operator @ joint_basis, full_matrices=True)
    rank = int((singular > tolerance).sum())
    return joint_basis @ vh[rank:].T


def intrinsic_velocity_loss(model, reference: Tensor, basis: Tensor, condition: Tensor,
                            query_time: Tensor, levels: Tensor, noise: Tensor) -> tuple[Tensor, dict]:
    """One native forward pass; loss uses only the admitted target coordinates."""
    target = reference @ basis
    if target.shape[-1] == 0:
        raise ValueError('empty eligibility has no missing-state training objective')
    if noise.shape != target.shape:
        raise ValueError('noise must have the intrinsic target shape')
    state, _ = model.scheduler.q_sample(target, levels, noise=noise)
    alpha = model.scheduler.sqrt_alpha_bars.to(state)[levels].view(-1, 1, 1)
    sigma = model.scheduler.sqrt_one_minus_alpha_bars.to(state)[levels].view(-1, 1, 1)
    velocity = alpha * noise - sigma * target
    prediction = model(state @ basis.T, levels, cond_summary=condition, dt=query_time) @ basis
    loss = (prediction - velocity).square().mean()
    clean = model.scheduler.to_x0(state, levels, prediction, param_type='v')
    weighted_clean_loss = ((clean - target) / sigma).square().mean()
    # The identity is algebraic; compare float32 reductions at their actual scale.
    # Retain both values and the absolute error rather than hiding rounding drift.
    absolute_error = (loss - weighted_clean_loss).detach().abs()
    magnitude = torch.maximum(loss.detach().abs(), weighted_clean_loss.detach().abs())
    return loss, {'velocity_loss': float(loss.detach()),
                  'weighted_clean_loss': float(weighted_clean_loss.detach()),
                  'clean_weight_identity_error': float(absolute_error),
                  'clean_weight_identity_relative_error': float(absolute_error / magnitude.clamp_min(1e-12))}


@torch.no_grad()
def intrinsic_ddim(model, basis: Tensor, condition: Tensor, query_time: Tensor,
                   observed: Tensor, levels: Sequence[int], *, generator: torch.Generator,
                   trace: Callable[[dict], None] | None = None) -> Tensor:
    """Return missing-state coordinates; never turn omitted coordinates into estimates.

observed is one fixed reference-state draw for this whole trajectory; its matching
conditioning tokens are built by the caller. Native scheduler levels decrease;
the last prediction is converted to the clean endpoint, not scheduler index zero.
    """
    if basis.shape[1] == 0:
        return observed.new_empty((*observed.shape[:-1], 0))
    if not levels or any(a <= b for a, b in zip(levels, levels[1:])):
        raise ValueError('reverse levels must be a nonempty strictly decreasing sequence')
    if min(levels) < 1 or max(levels) >= model.scheduler.timesteps:
        raise ValueError('levels must lie in the declared native noisy schedule')
    if not torch.allclose(observed @ basis, torch.zeros_like(observed @ basis), atol=1e-6, rtol=0):
        raise ValueError('observed draw must lie outside the admitted missing subspace')
    shape = (*observed.shape[:-1], basis.shape[1])
    state = torch.randn(shape, dtype=observed.dtype, device=observed.device, generator=generator)
    projector = basis @ basis.T
    complement = torch.eye(len(basis), device=basis.device, dtype=basis.dtype) - projector
    for step, level in enumerate(levels):
        t = torch.full((len(state),), level, dtype=torch.long, device=state.device)
        pred = model(state @ basis.T, t, cond_summary=condition, dt=query_time) @ basis
        if step + 1 < len(levels):
            previous = torch.full_like(t, levels[step + 1])
            state = model.scheduler.ddim_step_from(state, t, previous, pred,
                                                    param_type='v', eta=0., noise=torch.zeros_like(state))
        else:
            state = model.scheduler.to_x0(state, t, pred, param_type='v')
        if not torch.isfinite(state).all():
            raise FloatingPointError('nonfinite native intrinsic reverse state')
        if trace is not None:
            missing = state @ basis.T
            trace({'step': step, 'native_level': level,
                   'forbidden_max_abs': float((missing @ complement).abs().max()),
                   'observed_drift_max_abs': float(((observed + missing) @ complement - observed).abs().max()),
                   'state_rms': float(state.square().mean().sqrt())})
    return state
