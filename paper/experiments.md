# Three sequential research tasks

## A — Close the actual-condition theory

Scope: definitions, full-statistic versus actual-token boundary, conditional KL decomposition and denoising projection. Retain the original Gaussian posterior/information-order and dense-`J` sufficiency witnesses. Add an actual-token collision and a full-operator side-input positive control. Gaussian plug-in error must not be relabeled as the true compressed-posterior error.

The amended/new Notebooks are 01, 03, 09 and 10. Their finite outputs go in `results.md`. No learned model, new token architecture, sampler, or large data experiment is part of this task.

## B — Paired known-pole compression experiment

**Executed slice:** finite-design linear coefficient measurements. Theory 11 and `experiments/synthetic_known_pole/compression.py` implement the true conditional, with 6,144 held-out events per prior/coupling cell. The retained table is `paper/assets/compression_summary.csv`. Physical-filter and actual HSE compression remain untested.

Freeze two damped modes and infer four cosine/sine coefficients. Use two cells: a Gaussian prior and a declared finite Gaussian-mixture prior with an exactly computable oracle. Split latent events before constructing acquisitions. Start with declared linear `A,R`; a later physical-filter cell must measure finite-window leakage rather than assume a perfect spectral null.

For the same events, observations and actual side inputs compare:

```text
full (b,J) oracle
b + diag(J)
b + declared within-mode 2x2 blocks
```

Run coarse and full `(A,R)` side-information regimes separately, with equal access within each regime. If full side information eliminates the gap, retain that result and do not hide the descriptor. Report the actual token/scalar budget and discarded cross-block information. A small block is a hypothesis, not an already sufficient condition.

The executed slice uses the joint-log-score gap `log p(beta|b,D) - log p(beta|b,summary)`. Averaging over true event draws estimates expected conditional KL; posterior densities are exact, but the expectation is Monte Carlo. Each event's four views are averaged before a 1,000-replicate paired bootstrap. There are two priors and three fixed cross couplings (0, 0.45, 0.8), with simulator seeds 0,1,2. Seed values do not represent neural training.

The exact mixture and the diagonal/block plug-in models are reported separately. Primary endpoint: expected conditional KL; denoising conditional-mean distance and central marginal coverage are secondary. Full statistics, diagonal statistics and block statistics contain 14, 8 and 10 unique scalars: an upper-information comparison, not a matched-budget result. A diagonal/block plug-in Gaussian is an approximate model and must be labeled separately. Auxiliary endpoints: modal mean error, directional variance, conditional coverage and computational cost.

The CSV and two reproducible figures are now produced by `python -m experiments.synthetic_known_pole.run_compression`. Results do not support universal block sufficiency or monotonic loss versus off-diagonal magnitude. A finite mixture is an exact model for this synthetic family; it cannot establish a Diffusion advantage.

**Before C:** replace algebraic coefficient measurements with declared sampled-window acquisition, audit whether actual side metadata already reconstructs the coupling, and retain `(P,K,D)` plus equal scalar/parameter/compute budgets. Continue only if a specific coupling feature reduces an actual condition or finite-capacity gap. No universal information manager or new model factory is needed.

## C — Minimal learned HSE to LLapDiff integration

Freeze the weights of one source-trained target VAE. Keep the modal-predictor architecture, diffusion parameterization, schedule, time weighting, reverse sampler and reference query grid identical across arms. Train the denoiser and conditioner in each arm with matched initialization policy, optimizer and budget; do not silently freeze one arm only. Change only history conditioning:

| Arm | Actual condition |
|---|---|
| B0 | original LLapDiff conditioner + common a |
| B1 | original HSE conditioner + common a |
| M | coupling-aware HSE supported by Task B + common a |

Gaussian/mixture alternatives receive the same HSE condition. The full-statistic oracle is labeled an upper-information analytical baseline, not ranked as an equal-budget implementation.

Check that tokens, time, bands, masks and `a` are actually consumed; that HSE receives training gradients; and that evaluation patch selection is declared and deterministic. Epsilon/x0/v and sampler conventions must agree. Do not add a sample-residual penalty without deriving its target effect.

Use one predeclared proper score (joint Energy Score, or marginal CRPS with a joint-dependence diagnostic). Add acquisition-stratified coverage and width, observation-dependent checks against a prior-only baseline, target mean error, posterior draw count and cost. Approximate diffusion NLL is not automatically comparable to exact Gaussian likelihood.

## Uncertainty and noise controls

- Gaussian cells check `J_H >= J_L -> Sigma_H <= Sigma_L` under their assumptions.
- General posterior cells use proper scores and conditional averaging under a justified degradation chain, not a per-event variance-order penalty.
- Resampled views of the same noisy record must not count as independent likelihood factors.
- A noisy high-rate reference conditional is not silently described as a clean-state posterior.

## Statistics and progression

The independent unit is a latent event, later a machine/run/bearing/recording. Keep training seeds and posterior Monte Carlo draws separate. Use paired event-level intervals and predeclared practical/equivalence margins; a nonsignificant difference or a wide interval does not establish equivalence.

Only after Task C succeeds move to one licensed raw recording source: split recordings first, construct anti-aliased rate views within each split, fit preprocessing on source only, and evaluate an unseen intermediate rate. Such an offline pilot does not establish cross-hardware generalization. Flow Matching stays future work.
