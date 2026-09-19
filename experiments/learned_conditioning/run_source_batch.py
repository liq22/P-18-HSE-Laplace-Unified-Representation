"""Real PHMFactory-exported MFPT batch through the target-intrinsic native path.

A deterministic four-coordinate block-DCT reference makes the view relation
explicit. This is an implementation experiment, NOT learned HSE, physical modal
recovery, a restriction-benefit comparison, posterior calibration or LODO.
Only train/val exports are opened. Raw and derived waveforms are never uploaded.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import torch
from torch import Tensor
import numpy as np
from .intrinsic_native import eligible_basis, intrinsic_velocity_loss, intrinsic_ddim


def load_export(path: Path, split: str) -> dict:
    with np.load(path, allow_pickle=False) as data:
        out = {key: data[key].copy() for key in
               ['x', 'label', 'group_id', 'file_id', 'unit_id', 'sample_rate_hz', 'split']}
    if str(out['split'].item()) != split or out['x'].shape[1:] != (2048, 1):
        raise ValueError('expected the unchanged PHMFactory MFPT export and original split')
    if not np.isfinite(out['x']).all() or not (out['sample_rate_hz'] > 0).all():
        raise ValueError('finite waveform values and positive physical sample rates required')
    return out


def reference_features(data: dict) -> Tensor:
    """32 physical-time patches x 4 orthonormal DCT-II coordinates per waveform."""
    length = 64
    n = torch.arange(length, dtype=torch.float32)
    j = torch.arange(4, dtype=torch.float32)[:, None]
    dictionary = torch.cos(torch.pi * (n + .5) * j / length) * (2. / length) ** .5
    dictionary[0] /= 2. ** .5
    torch.testing.assert_close(dictionary @ dictionary.T, torch.eye(4), atol=2e-6, rtol=0)
    x = torch.as_tensor(data['x'], dtype=torch.float32).reshape(-1, 32, length)
    return x @ dictionary.T


def observed_condition(observed: Tensor, rates: np.ndarray) -> tuple[Tensor, Tensor]:
    """Lossless measured-reference tokens, deliberately not labelled HSE features."""
    condition = observed.new_zeros((len(observed), observed.shape[1], 16))
    condition[..., :2] = observed[..., :2]
    times = torch.arange(32, dtype=observed.dtype)[None] * 64 / torch.tensor(rates, dtype=observed.dtype)[:, None]
    condition[..., 2] = times
    condition[..., 3] = torch.log(torch.tensor(rates, dtype=observed.dtype))[:, None]
    condition[..., 4:8] = torch.tensor([1., 1., 0., 0.])  # known acquisition rows
    condition[..., 8:12] = torch.tensor([0., 0., 1., 1.])  # jointly observed source targets
    return condition, times


def summaries(z: Tensor) -> Tensor:
    return torch.cat((z.mean(1), z.std(1, unbiased=False)), -1)


def fit_head(z: Tensor, labels: np.ndarray) -> torch.nn.Module:
    """Small source-trained readout, fixed before the native generator update."""
    torch.manual_seed(19)
    head = torch.nn.Linear(z.shape[-1] * 2, 3)
    optimizer = torch.optim.Adam(head.parameters(), lr=.02)
    features = summaries(z)
    y = torch.tensor(labels, dtype=torch.long)
    for _ in range(60):
        optimizer.zero_grad(set_to_none=True)
        loss = torch.nn.functional.cross_entropy(head(features), y)
        loss.backward(); optimizer.step()
    head.eval().requires_grad_(False)
    return head


def representatives(groups: np.ndarray) -> np.ndarray:
    """One predetermined first window per original group; not a performance sample."""
    return np.unique(groups, return_index=True)[1]


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exports', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    # The package must be the installed original LLapDiff. There is no fallback.
    from llapdiffusion.models.llapdiff import LLapDiff
    torch.set_num_threads(1); torch.manual_seed(19)
    train = load_export(args.exports / 'train_waveforms.npz', 'train')
    val = load_export(args.exports / 'val_waveforms.npz', 'val')
    if set(train['group_id']) & set(val['group_id']):
        raise ValueError('original source train/validation groups overlap')
    args.output.mkdir(parents=True, exist_ok=False)
    z_train = reference_features(train)
    mean = z_train.mean((0, 1)); scale = z_train.std((0, 1), unbiased=False)
    if not (scale > 0).all():
        raise ValueError('source reference contains a constant coordinate')
    z_train = (z_train - mean) / scale
    z_val = (reference_features(val) - mean) / scale
    operator = torch.eye(4)[:2]
    basis = eligible_basis(operator, torch.eye(4))
    projector = basis @ basis.T
    observed_train = z_train @ (torch.eye(4) - projector)
    observed_val = z_val @ (torch.eye(4) - projector)
    # Reference variables are measured features with no added observation noise.
    # q_o is a point mass here; this does not claim noise-free physical states.
    ct, tt = observed_condition(observed_train, train['sample_rate_hz'])
    cv, tv = observed_condition(observed_val, val['sample_rate_hz'])
    head = fit_head(z_train, train['label'])
    observed_head = fit_head(z_train[..., :2], train['label'])
    head_state = {key: value.clone() for key, value in head.state_dict().items()}
    ti = representatives(train['group_id']); vi = representatives(val['group_id'])
    model = LLapDiff(data_dim=4, hidden_dim=16, num_layers=1, num_heads=2,
                    laplace_k=4, predict_type='v', timesteps=64, schedule='cosine',
                    dropout=0., attn_dropout=0., block_summary_adaln=True, analysis_summary_qk=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    levels = torch.arange(len(ti)) % 63 + 1
    noise = torch.randn(len(ti), 32, basis.shape[1])
    model.train(); optimizer.zero_grad(set_to_none=True)
    loss, diagnostics = intrinsic_velocity_loss(model, z_train[ti], basis, ct[ti], tt[ti], levels, noise)
    if not torch.isfinite(loss):
        raise FloatingPointError('nonfinite native source-batch loss')
    before = {key: value.clone() for key, value in model.state_dict().items()}
    loss.backward()
    gradient = sum(float(p.grad.abs().sum()) for p in model.parameters() if p.grad is not None)
    if gradient <= 0:
        raise AssertionError('intrinsic loss did not reach native model parameters')
    optimizer.step(); model.eval()
    parameter_change = max(float((value - before[key]).abs().max()) for key, value in model.state_dict().items())
    if parameter_change <= 0:
        raise AssertionError('the native model did not update')
    traces = []; draws = []
    for draw in range(4):
        def record(row):
            traces.append({'draw': draw, **row})
        w = intrinsic_ddim(model, basis, cv[vi], tv[vi], observed_val[vi],
                           [63, 47, 31, 15, 1], generator=torch.Generator().manual_seed(100 + draw), trace=record)
        draws.append(observed_val[vi] + w @ basis.T)
    complete = torch.stack(draws)
    with torch.no_grad():
        probabilities = torch.stack([head(summaries(z)).softmax(-1) for z in complete]).mean(0)
        observed_probabilities = observed_head(summaries(z_val[vi, :, :2])).softmax(-1)
    for value in (probabilities, observed_probabilities):
        if not torch.isfinite(value).all():
            raise FloatingPointError('nonfinite diagnostic probabilities')
        torch.testing.assert_close(value.sum(-1), torch.ones(len(value)), atol=1e-6, rtol=0)
    for key, value in head.state_dict().items():
        torch.testing.assert_close(value, head_state[key], atol=0, rtol=0)
    records = []
    for split, data, indices in [('train', train, ti), ('val', val, vi)]:
        for row in indices:
            records.append({'split': split, 'group_id': str(data['group_id'][row]),
                            'file_id': str(data['file_id'][row]), 'unit_id': int(data['unit_id'][row]),
                            'sample_rate_hz': float(data['sample_rate_hz'][row]),
                            'observed_rank': 2, 'eligible_rank': int(basis.shape[1]),
                            'source_joint_rank': 4, 'source_global_null_rank': 0})
    output_rows = []
    for index, row in enumerate(vi):
        output_rows.append({'group_id': str(val['group_id'][row]), 'unit_id': int(val['unit_id'][row]),
                            'label': int(val['label'][row]),
                            **{f'conditional_p{k}': float(probabilities[index, k]) for k in range(3)},
                            **{f'observed_only_p{k}': float(observed_probabilities[index, k]) for k in range(3)}})
    summary = {'scope': 'real MFPT reference-feature native batch; not HSE, calibration, factorial or LODO',
               'reference': 'first four block-DCT coordinates; 64 samples per block; source-only normalization',
               'conditioning': 'lossless measured-reference tokens; no learned HSE checkpoint',
               'identification': 'same-recording full reference paired with its exact two-coordinate acquisition',
               'observed_uncertainty': 'point-mass reference-feature conditional; no added observation noise',
               'all_missing_admitted': True, 'restriction_benefit_tested': False,
               'test_export_opened': False,
               'train_windows_available': len(z_train), 'validation_windows_available': len(z_val),
               'train_batch_recordings': len(ti), 'validation_batch_recordings': len(vi),
               'source_head_updates': 60, 'native_generator_updates': 1,
               'native_parameters': sum(p.numel() for p in model.parameters()),
               'native_gradient_l1': gradient, 'native_parameter_max_change': parameter_change,
               'basis_orthogonality_error': float((basis.T @ basis - torch.eye(basis.shape[1])).abs().max()),
               'observation_null_error': float((operator @ basis).abs().max()),
               **diagnostics, 'draws': 4, 'reverse_levels': [63, 47, 31, 15, 1],
               'max_forbidden_abs': max(row['forbidden_max_abs'] for row in traces),
               'max_observed_drift_abs': max(row['observed_drift_max_abs'] for row in traces),
               'diagnostic_rows': len(output_rows), 'diagnostic_head_unchanged': True}
    if summary['max_forbidden_abs'] > 1e-6 or summary['max_observed_drift_abs'] > 1e-6:
        raise AssertionError('native sampling changed forbidden or observed coordinates')
    if summary['clean_weight_identity_error'] > 1e-5:
        raise AssertionError('velocity/weighted clean loss identity failed')
    write_csv(args.output / 'source_batch.csv', records)
    write_csv(args.output / 'native_trace.csv', traces)
    write_csv(args.output / 'diagnostic_outputs.csv', output_rows)
    (args.output / 'source_batch_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    torch.save({'model': model.state_dict(), 'head': head.state_dict(),
                'observed_head': observed_head.state_dict(), 'reference_mean': mean,
                'reference_scale': scale, 'basis': basis, 'terminal_missing_draws': complete @ basis}, args.output / 'source_batch.pt')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
