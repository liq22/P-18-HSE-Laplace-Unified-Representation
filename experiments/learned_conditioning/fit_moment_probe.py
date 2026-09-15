"""Source-supervised shared code, with decomposed scoring diagnostics.

This fits a conditioner, not HSE or LLapDiff. Real files require an explicit
feature-export note; --synthetic is a separate and visibly labeled experiment.
"""
import argparse
import copy
import csv
import json
from pathlib import Path
import numpy as np
import torch
from .moment_conditioner import MatchedConditioner
from .feature_data import load_features, check_splits, inputs


def generate(n, seed):
    rng = np.random.default_rng(seed)
    h = rng.normal(size=(n, 4, 8)).astype('float32')
    mask = np.ones((n, 4), dtype=bool)
    side = rng.normal(size=(n, 1)).astype('float32')
    mean = np.column_stack([.6*h[:, 0, 0]+.2*side[:, 0], -.4*h[:, 1, 0]])
    variance = np.column_stack([.25+.12/(1+np.exp(-h[:, 0, 1])),
                               .35+.15/(1+np.exp(-h[:, 1, 1]))])
    y = mean+np.sqrt(variance)*rng.normal(size=(n, 2))
    return {'tokens': torch.tensor(h), 'attention_mask': torch.tensor(mask),
            'side': torch.tensor(side), 'targets': torch.tensor(y, dtype=torch.float32),
            'event_id': np.array([f'{seed}-e{i}' for i in range(n)]),
            'group_id': np.array([f'{seed}-g{i}' for i in range(n)]),
            'condition_id': np.array(['source']*n), 'side_names': np.array(['observed_scalar']),
            'oracle_mean': mean, 'oracle_variance': variance}


def diagnostics(model, data, index=slice(None)):
    with torch.no_grad():
        d = model.score_parts(*inputs(data, index), data['targets'][index])
    return {'score': float(d['score'].mean()), 'logdet': float(d['logdet'].mean()),
            'mahalanobis': float(d['mahalanobis'].mean()),
            'min_eigenvalue': float(d['min_eigenvalue'].min()),
            'fraction_near_floor': float((d['min_eigenvalue'] <= model.covariance_floor*1.05).float().mean())}


def fit_shared(train, validation, steps=600, seed=71, floor=1e-4):
    torch.manual_seed(seed)
    model = MatchedConditioner(train['tokens'].shape[1], train['tokens'].shape[2],
                              train['targets'].shape[1], train['side'].shape[1], covariance_floor=floor)
    optimizer = torch.optim.Adam(model.parameters(), lr=.003)
    best = diagnostics(model, validation)['score']; best_step = 0
    best_state = copy.deepcopy(model.state_dict()); rows = []
    for step in range(steps+1):
        if step:
            batch = torch.randint(0, len(train['tokens']), (min(128, len(train['tokens'])),))
            optimizer.zero_grad(set_to_none=True)
            loss = model.score_parts(*inputs(train, batch), train['targets'][batch])['score'].mean()
            if not torch.isfinite(loss):
                raise FloatingPointError('nonfinite Gaussian score; no silent covariance repair')
            loss.backward(); optimizer.step()
        if step % 25 == 0 or step == steps:
            tr, va = diagnostics(model, train), diagnostics(model, validation)
            rows.append({'step': step, **{f'train_{k}': v for k, v in tr.items()},
                         **{f'validation_{k}': v for k, v in va.items()}})
            if va['score'] < best:
                best, best_step = va['score'], step
                best_state = copy.deepcopy(model.state_dict())
    model.load_state_dict(best_state)
    model.freeze_for_denoising()
    return model, rows, best_step


def constant_score(train, test, floor):
    y = train['targets'].double()
    mean = y.mean(0); centered = y-mean
    covariance = centered.T@centered/len(y)+floor*torch.eye(y.shape[1], dtype=y.dtype)
    factor = torch.linalg.cholesky(covariance)
    r = torch.linalg.solve_triangular(factor, (test['targets'].double()-mean).T, upper=False)
    return float(.5*(2*factor.diag().log().sum()+r.square().sum(0)).mean())


def ridge_score(model, train, test, floor, ridge=1e-3):
    """Source-only linear mean and homoskedastic residual covariance control."""
    x=model.inputs(*inputs(train)).double()
    xt=model.inputs(*inputs(test)).double()
    x=torch.cat((x,torch.ones(len(x),1,dtype=x.dtype)),1)
    xt=torch.cat((xt,torch.ones(len(xt),1,dtype=xt.dtype)),1)
    penalty=ridge*torch.eye(x.shape[1],dtype=x.dtype);penalty[-1,-1]=0
    coefficient=torch.linalg.solve(x.T@x+penalty,x.T@train['targets'].double())
    error=train['targets'].double()-x@coefficient
    covariance=error.T@error/len(error)+floor*torch.eye(error.shape[1],dtype=error.dtype)
    factor=torch.linalg.cholesky(covariance)
    residual=torch.linalg.solve_triangular(factor,(test['targets'].double()-xt@coefficient).T,upper=False)
    return float(.5*(2*factor.diag().log().sum()+residual.square().sum(0)).mean())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--synthetic', action='store_true')
    for name in ['train', 'validation', 'test', 'data-note']:
        p.add_argument('--'+name, type=Path)
    p.add_argument('--steps', type=int, default=600); p.add_argument('--seed', type=int, default=71)
    p.add_argument('--covariance-floor', type=float, default=1e-4)
    p.add_argument('--output-dir', type=Path, required=True)
    args = p.parse_args()
    if args.steps < 1 or args.covariance_floor <= 0:
        p.error('this finite pilot requires positive steps and an explicit positive covariance floor')
    if args.synthetic:
        if any(x is not None for x in [args.train, args.validation, args.test, args.data_note]):
            p.error('synthetic and real feature files are separate experiments')
        train, validation, test = generate(2048, 10), generate(512, 11), generate(2048, 12)
    else:
        if not all(x is not None for x in [args.train, args.validation, args.test, args.data_note]):
            p.error('provide three feature files and --data-note, or explicitly use --synthetic')
        if not args.data_note.is_file():
            p.error('feature-export note is missing')
        train, validation, test = [load_features(f) for f in [args.train, args.validation, args.test]]
    check_splits(train, validation, test)
    torch.set_num_threads(1)
    model, rows, selected_step = fit_shared(train, validation, args.steps, args.seed, args.covariance_floor)
    result = {'evidence': 'synthetic shared-path witness' if args.synthetic else 'user-exported frozen features',
              'native_hse_or_llapdiff_trained': False, 'seed': args.seed, 'selected_step': selected_step,
              'covariance_floor': args.covariance_floor, 'input_condition': 'tokens + mask + explicit side',
              'test': diagnostics(model, test), 'source_constant_gaussian_score': constant_score(train, test, args.covariance_floor),
              'source_ridge_homoskedastic_score': ridge_score(model, train, test, args.covariance_floor),
              'conditions': {c: diagnostics(model, test, np.flatnonzero(test['condition_id']==c))
                             for c in np.unique(test['condition_id'])},
              'message_scalars': model.budget, 'semantic_scalars': model.semantic_size,
              'conditioner_parameters': sum(p.numel() for p in model.parameters()),
              'all_conditioner_parameters_frozen': not any(p.requires_grad for p in model.parameters())}
    if args.synthetic:
        with torch.no_grad():
            d = model.score_parts(*inputs(test), test['targets'])
        scale = train['targets'].std(0).numpy()
        result['mean_rmse'] = float(np.sqrt(np.mean((d['mean'].numpy()-test['oracle_mean'])**2)))
        result['mean_rmse_in_source_sd'] = float(np.sqrt(np.mean(((d['mean'].numpy()-test['oracle_mean'])/scale)**2)))
        result['variance_rmse'] = float(np.sqrt(np.mean((d['covariance'].diagonal(dim1=-2,dim2=-1).numpy()-test['oracle_variance'])**2)))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    torch.save({'config': model.config(), 'state_dict': model.state_dict()}, args.output_dir/'shared_conditioner.pt')
    with (args.output_dir/'score_parts.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    (args.output_dir/'moment_probe.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
