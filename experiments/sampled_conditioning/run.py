"""Paired sampled-window experiment with explicitly transmitted sparse headers."""
import argparse
import csv
import json
from itertools import product
from pathlib import Path
import numpy as np
from .core import sampled_design, retained_matrix, choose_pattern, encode_header, decode_header, expected_plugin_kl


def interval(values, repetitions, rng):
    means = [values[rng.integers(0, len(values), len(values))].mean() for _ in range(repetitions)]
    return np.quantile(means, [.025, .975])


def evaluate_design(A, beta, noise, method, full_side=False):
    """Return posterior errors on the same events; no train/test target selection."""
    J = A.T@A/.25
    observations = beta@A.T + .5*noise
    b = observations@A/.25
    full_covariance = np.linalg.solve(np.eye(4)+J, np.eye(4))
    moment_costs = [np.linalg.slogdet(retained_matrix(full_covariance, k))[1] for k in range(3)]
    patterns = {'diag': -1, 'within': 0, 'magnitude': choose_pattern(J, 'magnitude'),
                'risk_oracle': choose_pattern(J), 'moment_within': 0,
                'moment_best': int(np.argmin(moment_costs)), 'full': -2}
    pattern = patterns[method]
    moment_mode = method.startswith('moment_')
    if method == 'full' or moment_mode:
        kept = J.copy()
    else:
        # The decoder only reads the actual 11-scalar header, not the hidden J.
        headers = np.repeat(encode_header(b[0], J, pattern)[None], len(b), axis=0)
        headers[:, :4] = b
        _, kept = decode_header(headers[0])
        b = headers[:, :4].copy()
    if full_side:
        kept = A.T@np.linalg.solve(.25*np.eye(len(A)), A)
    precision, q_precision = np.eye(4)+J, np.eye(4)+kept
    covariance = np.linalg.solve(precision, np.eye(4))
    q_covariance = np.linalg.solve(q_precision, np.eye(4))
    mean, q_mean = b@covariance, b@q_covariance
    if moment_mode:
        # Strong analytic control: encoder computes exact moments, decoder reads
        # only their 11-scalar header. It is not a learned moment predictor.
        headers = np.repeat(encode_header(mean[0], covariance, pattern)[None], len(mean), axis=0)
        headers[:, :4] = mean
        _, q_covariance = decode_header(headers[0])
        q_mean = headers[:, :4].copy()
        if full_side:
            # The actual side input reconstructs full covariance. The mean is
            # still read from the transmitted moment header, never hidden beta.
            q_covariance = np.linalg.solve(np.eye(4)+kept, np.eye(4))
        q_precision = np.linalg.solve(q_covariance, np.eye(4))
    delta = q_mean-mean
    constant = np.trace(q_precision@covariance)-4+np.linalg.slogdet(precision)[1]-np.linalg.slogdet(q_precision)[1]
    kl = .5*(constant + np.einsum('ni,ij,nj->n', delta, q_precision, delta))
    eig, U = np.linalg.eigh(precision)
    invroot = (U*eig**-.5)@U.T
    E = invroot@(q_precision-precision)@invroot
    kappa = 1+np.linalg.eigvalsh(E).min()
    v = b@invroot
    residual = (q_mean@q_precision-b)@invroot
    w = residual-v@E
    bound = np.linalg.norm(E, 'fro')**2/(4*min(1., kappa)**2) + np.sum(w*w, axis=1)/(2*kappa)
    if np.any(kl > bound+1e-8):
        raise AssertionError('precision error bound violated')
    coverage = np.mean(np.abs(beta-q_mean) <= 1.6448536269514722*np.sqrt(np.diag(q_covariance)), axis=1)
    return {'kl': kl, 'bound': bound, 'mse': np.mean((beta-q_mean)**2, axis=1),
            'coverage90': coverage, 'pattern': pattern,
            'expected_kl': float(.5*(np.linalg.slogdet(q_covariance)[1]-np.linalg.slogdet(covariance)[1])) if moment_mode else expected_plugin_kl(J, kept), 'kappa': float(kappa)}


def run(profile, output):
    events, repetitions = (64, 64) if profile == 'smoke' else (2048, 1000)
    seeds = [0] if profile == 'smoke' else [0, 1, 2]
    designs = list(product([1024, 2048], [.08, .2], [5., 30.], ['regular', 'jitter', 'block_missing']))
    if profile == 'smoke':
        designs = [designs[0], designs[5], designs[-1]]
    output.mkdir(parents=True, exist_ok=True)
    rows, paired = [], []
    beta = np.concatenate([np.random.default_rng(seed).normal(size=(events+384, 4))[384:] for seed in seeds])
    for design_id, (rate, duration, gap, sampling) in enumerate(designs):
        times, A = sampled_design(rate, duration, gap, sampling)
        # Separate simulator stream per acquisition; every method shares these values.
        noise = np.concatenate([np.random.default_rng(10000+100*design_id+seed).normal(size=(events, len(A))) for seed in seeds])
        results = {}
        for side in ['coarse', 'full_operator']:
            for method in ['diag', 'within', 'magnitude', 'risk_oracle', 'moment_within', 'moment_best', 'full']:
                result = evaluate_design(A, beta, noise, method, side == 'full_operator')
                results[(side, method)] = result
                lo, hi = interval(result['kl'], repetitions, np.random.default_rng(817))
                rows.append({'design': design_id, 'rate_hz': rate, 'duration_s': duration,
                             'separation_hz': gap, 'sampling': sampling, 'observations': len(times),
                             'method': method, 'side_information': side, 'events': len(beta),
                             'seeds': ';'.join(map(str, seeds)), 'header_scalars': 15 if method == 'full' else 11,
                             'pattern': result['pattern'], 'kl_nats': result['kl'].mean(), 'kl_lo': lo, 'kl_hi': hi,
                             'expected_kl_nats': result['expected_kl'], 'mean_bound_nats': result['bound'].mean(),
                             'kappa': result['kappa'], 'mean_mse': result['mse'].mean(),
                             'coverage90': result['coverage90'].mean()})
        for comparator in ['within', 'magnitude']:
            gain = results['coarse', comparator]['kl']-results['coarse', 'risk_oracle']['kl']
            lo, hi = interval(gain, repetitions, np.random.default_rng(817))
            paired.append({'design': design_id, 'comparator': comparator, 'events': len(beta),
                           'gain_nats': gain.mean(), 'lo': lo, 'hi': hi})
        print(f'Completed design {design_id}: {rate} Hz, {duration} s, {sampling}', flush=True)
    for name, table in [('sampled_summary.csv', rows), ('paired_gains.csv', paired)]:
        with (output/name).open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(table[0]))
            writer.writeheader(); writer.writerows(table)
    description = {'profile': profile, 'events_per_seed': events, 'seeds': seeds,
                   'bootstrap': repetitions, 'designs': len(designs), 'P': 16, 'K': 4,
                   'noise_std': .5, 'prior': 'known N(0,I4)',
                   'sampling': 'direct damped-waveform evaluation, not anti-alias resampling',
                   'inference': 'Gaussian precision plug-in and exact-moment block controls; not true compressed-conditional MI',
                   'replication_unit': 'latent event; reused across designs, not 24 independent datasets',
                   'formal_claim_supported': False}
    (output/'run_settings.json').write_text(json.dumps(description, indent=2), encoding='utf-8')
    return rows, paired


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', choices=['smoke', 'full'], default='smoke')
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    run(args.profile, args.output_dir)


if __name__ == '__main__':
    main()
