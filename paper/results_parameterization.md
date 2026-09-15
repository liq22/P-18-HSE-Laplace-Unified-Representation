# Same-partition posterior parameterization controls

## Scope and reproduction

Executed on 2026-09-10. This is a new analytical check, not a rerun of the earlier 24-design/336-row study or the older six-dimensional/144-row offline package. Code: `experiments/sampled_conditioning/parameterization_controls.py`. Retained numbers: `assets/parameterization_controls.csv`.

```bash
python -m experiments.sampled_conditioning.parameterization_controls --events 256 --output-dir outputs/parameterization
bash paper/run.sh parameterization-figures paper/assets/parameterization_controls.csv outputs/parameterization_figures
```

There are five stated designs and six arms per design (30 rows): one fixed six-dimensional reviewer example and four sampled geometry controls. The fixed-points and fixed-duration controls share the 1024 Hz reference by construction, so these are not five independent acquisition mechanisms. No HSE, VAE, LLapDiff, external baseline or real PHM model was trained.

## 1. The decisive fixed-partition example

Take `J=0.2 I6+2 11^T`, unit Gaussian prior, information vector `(1,-0.3,0.4,0.7,-0.8,0.2)`, and the predeclared partition `(0,1,2,3)|(4,5)`. All arms use the same observation statistics and prior. A fixed partition is shared in the protocol; it needs no per-event layout identifier. Counts are stored real scalars at equal precision, not entropy-coded bits or measured neural FLOPs.

| Representation | Statistic scalars | Coefficient forward KL | Target forward KL | Target epsilon discrepancy |
|---|---:|---:|---:|---:|
| Full posterior | 27 | 0 | 0 | 0 |
| Natural-parameter blocks | 19 | 2.643000 | 1.072153 | 0.363764 |
| Full mean + block precision covariance | 19 | 1.467540 | 0.457439 | 0.130338 |
| Full mean + marginal covariance blocks | 19 | 0.552662 | 0 | 0 |
| Trace-isotropic modal information | 9 | 3.012041 | 0.982420 | 0.427870 |
| Prior-whitened rank-two covariance update + full mean | 18 | 0.031310 | 0.009550 | 0.005427 |

KL is in nats. The fixed target selects the final two coefficients; it is not a learned reference latent. Epsilon discrepancy uses `alpha=0.8, sigma=0.6` and integrates squared prediction differences under the true perturbed target law, as derived in Theory 12. It is not the Bayes compression gap unless the comparison law equals the true compressed conditional.

The marginal-block posterior is the exact target posterior here because the target is one retained group. That zero is a construction, not a universal victory for moment tokenization. A different target mixing groups can lose dependencies. The low-rank control is a dense analytical implementation of the prior-whitened negative-update family, not a reproduction of a scalable matrix-free solver.

A target-only rank-one covariance update plus exact target mean uses four scalars and gives target KL `0.0078274451`; exact target moments use five scalars and give zero. These cannot reconstruct all six physical coefficients and must not be ranked as universal full-state representations.

The 19-scalar natural block loses `2.0903376641` nats relative to the moment block. The general product-KL identity explains the difference as a sum of marginal KL terms. Mean correction alone reduces but does not eliminate the loss; the Schur complement explains the remaining marginal covariance error.

## 2. Separate geometry from sample-count budget

For two damped modes (100 and 130 Hz; damping 12 and 18 inverse seconds), use four deterministic patches in a 0.25 s context. Fixed-points uses 16 points at both rates. Fixed-duration uses nominal half-open patch duration `16/1024` s: 16 points at 1024 Hz and 32 points at 2048 Hz. Last observed timestamps differ by the grid spacing; this is fixed physical cell duration, not identical discrete endpoint grids.

| Protocol | Rate / Hz | P | Observations | Natural-block coefficient KL | Moment-block coefficient KL |
|---|---:|---:|---:|---:|---:|
| Fixed points | 1024 | 16 | 64 | 17.912871 | 0.387735 |
| Fixed points | 2048 | 16 | 64 | 33.909044 | 0.798593 |
| Fixed duration | 1024 | 16 | 64 | 17.912871 | 0.387735 |
| Fixed duration | 2048 | 32 | 128 | 36.582948 | 0.400842 |

Each sampled setting uses 256 Gaussian coefficient events, seed 420, with the same generated observations across methods. Coefficients recur across the design controls. There is no model fitting, hyperparameter selection or confirmatory statistical test. The moment-block KL is constant across event means in these correctly specified Gaussian cells. The CSV retains target and denoising metrics for every arm.

All nominal mode centers are below Nyquist. Directly sampling damped basis functions is not anti-alias filtering of a noisy recording or evidence for a low-rate-invisible private band. These controls separate two protocols; they do not establish which is universally superior.

## 3. Bound usefulness and coordinate controls

The amended Theory 12 Notebook retains the original dense-SPD checks and compares exact KL, the older valid bound, the tightened bound, their ratios and selection indices. It also tests cancellation `r=Ev`, amplification `r=-Ev`, the target ranking reversal and the Gaussian denoiser calculation. Full whitening remains an offline oracle cost, not free decoder information.

Theory 13 retains the original header round-trip, 40,000-event expectation check and complete-side-information control. It adds the product-KL decomposition, Schur variance ordering, prior-aware low-rank control and phase transformations including a non-isotropic prior. Trace-isotropic information satisfies the same modal coordinate covariance with fewer scalars; equivariance alone therefore does not justify a full block.

Local selected-source validation: seven new behavior tests and both amended Notebooks passed in isolated kernels. The selected-source snapshot was not a full repository clone. Full-repository CI is reported separately on PR #8.

## 4. Decision

Do not retain natural blocks as the preferred fixed-prior, forward-KL parameterization. Moment and low-rank controls are mandatory. Natural statistics remain candidates only for an explicit prior-reuse, independent-evidence accumulation or measured computational constraint. Their additive algebra does not establish a speed advantage: fixed-design full inference can also be cached.

The new results are supporting analysis and falsifying controls. No new learned-method contribution is admitted. The next task is the actual-condition/target audit in `GOAL.md`, followed by the smallest matched learned comparison only when a nonredundant benefit remains. `formal_claim_supported: false`.
