"""One supervised path for both M and B1-aux; no HSE replacement.

Input masks describe frozen history tokens. Output tokens are a dense global
summary, not patch-indexed observations; all output positions are consumed.
"""
from __future__ import annotations
import torch
from torch import nn
from torch.nn import functional as F

class MatchedConditioner(nn.Module):
    def __init__(self, tokens: int, width: int, target_dim: int, side_dim: int,
                 hidden: int = 32, covariance_floor: float = 1e-4):
        super().__init__()
        if min(tokens, width, target_dim, hidden) < 1 or side_dim < 0:
            raise ValueError('invalid dimensions')
        if covariance_floor < 0:
            raise ValueError('covariance floor must be nonnegative')
        self.tokens, self.width = tokens, width
        self.target_dim, self.side_dim = target_dim, side_dim
        self.hidden, self.covariance_floor = hidden, covariance_floor
        self.budget = tokens * width
        self.semantic_size = target_dim + target_dim * (target_dim + 1) // 2
        if self.semantic_size >= self.budget:
            raise ValueError('a mixed message must leave ordinary-feature capacity')
        self.trunk = nn.Sequential(
            nn.Linear(self.budget + tokens + side_dim, hidden), nn.SiLU(),
            nn.Linear(hidden, self.budget))
        # The score trains the exact ordinary code B1-aux later transmits.
        self.moment_head = nn.Linear(self.budget, self.semantic_size)
        self.register_buffer('tril', torch.tril_indices(target_dim, target_dim))
        self.frozen = False

    def config(self):
        return dict(tokens=self.tokens, width=self.width, target_dim=self.target_dim,
                    side_dim=self.side_dim, hidden=self.hidden,
                    covariance_floor=self.covariance_floor)

    def inputs(self, tokens, mask, side):
        if tokens.ndim != 3 or tuple(tokens.shape[1:]) != (self.tokens, self.width):
            raise ValueError('tokens must have the declared [B,K,D] shape')
        if mask.dtype != torch.bool or mask.shape != tokens.shape[:2]:
            raise ValueError('attention_mask must be bool [B,K], True = valid')
        if side.shape != (len(tokens), self.side_dim):
            raise ValueError('side must be [B,A], including A=0 when explicitly absent')
        if not mask.any(dim=1).all():
            raise ValueError('an empty history is outside this pilot')
        if not torch.isfinite(tokens[mask]).all() or not torch.isfinite(side).all():
            raise ValueError('valid observations and side fields must be finite')
        if self.frozen and (tokens.requires_grad or side.requires_grad):
            raise ValueError('stage two requires frozen input features and side preprocessing')
        # Masked entries are explicitly excluded, not imputed as observations.
        visible = torch.where(mask[..., None], tokens, torch.zeros_like(tokens))
        return torch.cat((visible.flatten(1), mask.to(tokens.dtype), side), dim=1)

    def ordinary(self, tokens, mask, side):
        return self.trunk(self.inputs(tokens, mask, side))

    def moments_from_code(self, ordinary):
        raw = self.moment_head(ordinary)
        mean = raw[:, :self.target_dim]
        factor = raw.new_zeros((len(raw), self.target_dim, self.target_dim))
        factor[:, self.tril[0], self.tril[1]] = raw[:, self.target_dim:]
        diagonal = torch.arange(self.target_dim, device=raw.device)
        factor[:, diagonal, diagonal] = F.softplus(factor[:, diagonal, diagonal])
        covariance = factor @ factor.transpose(-1, -2)
        if self.covariance_floor:
            # Public covariance constraint, not a hidden numerical jitter.
            covariance = covariance + self.covariance_floor * torch.eye(
                self.target_dim, device=raw.device, dtype=raw.dtype)
        factor = torch.linalg.cholesky(covariance)
        return mean, factor

    def score_parts(self, tokens, mask, side, target):
        if target.shape != (len(tokens), self.target_dim) or not torch.isfinite(target).all():
            raise ValueError('target must be finite [B,target_dim]')
        mean, factor = self.moments_from_code(self.ordinary(tokens, mask, side))
        residual = torch.linalg.solve_triangular(
            factor, (target - mean).unsqueeze(-1), upper=False).squeeze(-1)
        logdet = 2 * factor.diagonal(dim1=-2, dim2=-1).log().sum(-1)
        mahalanobis = residual.square().sum(-1)
        covariance = factor @ factor.transpose(-1, -2)
        return {'score': .5 * (logdet + mahalanobis), 'logdet': logdet,
                'mahalanobis': mahalanobis,
                'min_eigenvalue': torch.linalg.eigvalsh(covariance)[..., 0],
                'mean': mean, 'covariance': covariance}

    def freeze_for_denoising(self):
        self.zero_grad(set_to_none=True)
        self.requires_grad_(False)
        self.frozen = True
        self.eval()
        return self

    def train(self, mode=True):
        # A parent's train() cannot reactivate the frozen conditioning path.
        return super().train(False if self.frozen else mode)

    def forward(self, tokens, mask, side, arm='M'):
        if arm not in ('M', 'B1_aux', 'M0'):
            raise ValueError('arm must be M, B1_aux or M0')
        if not self.frozen:
            raise RuntimeError('select the source checkpoint and freeze before denoising')
        ordinary = self.ordinary(tokens, mask, side)
        if arm == 'B1_aux':
            return ordinary.reshape(-1, self.tokens, self.width)
        mean, factor = self.moments_from_code(ordinary)
        semantic = torch.cat((mean, factor[:, self.tril[0], self.tril[1]]), dim=-1)
        tail = ordinary[:, self.semantic_size:]
        if arm == 'M0':
            tail = torch.zeros_like(tail)
        return torch.cat((semantic, tail), -1).reshape(-1, self.tokens, self.width)

    def read_moments(self, message):
        raw = message.reshape(len(message), self.budget)
        factor = raw.new_zeros((len(raw), self.target_dim, self.target_dim))
        factor[:, self.tril[0], self.tril[1]] = raw[:, self.target_dim:self.semantic_size]
        return raw[:, :self.target_dim], factor @ factor.transpose(-1, -2)
