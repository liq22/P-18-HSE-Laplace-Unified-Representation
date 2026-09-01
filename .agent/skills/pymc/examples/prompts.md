# pymc — invocation scenarios

Realistic prompts for invoking the pymc implementation skill inside the
Auto-01-tiny-research workspace. Each scenario shows the kind of request that
should trigger this skill, the artifacts it reads, and the workspace outputs
it must produce.

## Scenario 1: Hierarchical Bayesian estimate for a claim

> The paper claims our intervention has a positive effect that varies across
> sites. The data is logged in `paper/experiments/run_ledger.md` (run `R-014`)
> across 8 sites, and `paper/refs/target_journal.md` wants a posterior median
> with a 94% HDI. Build a hierarchical (partial-pooling) Bayesian regression
> with non-centered parameterization, run a prior predictive check, fit with
> 4 NUTS chains, report the diagnostics, and update claim `C-05` in
> `paper/experiments/evidence_matrix.md`.

This triggers pymc: hierarchical/multilevel Bayesian modeling with partial
pooling, prior predictive checks, MCMC-NUTS inference, and convergence
diagnostics. The skill reads the data ref and claim requirements from
`paper/experiments/evidence_matrix.md`, builds a non-centered model using
patterns from `references/workflows.md`, selects priors/likelihoods from
`references/distributions.md`, runs `pm.sample(draws=2000, tune=1000,
chains=4, target_accept=0.95, random_seed=...)` per
`references/sampling_inference.md`, and verifies R-hat < 1.01, ESS > 400, and
near-zero divergences before reporting. It writes posterior medians with 94%
HDI into a table under `paper/assets/tables/`, appends a run row (model spec,
priors, sampler config, seed, diagnostics) to
`paper/experiments/run_ledger.md`, records versions in
`paper/experiments/reproducibility.md`, and updates `C-05`. Do NOT use
scikit-learn here (no frequentist point estimate will satisfy the journal's
HDI requirement); do NOT ship a runnable sampler script or a NetCDF posterior
blob into the repo — record the recipe and summaries only.

## Scenario 2: Bayesian model comparison for a reviewer response

> Reviewer 2 asks us to justify our chosen model structure over two
> alternatives (`paper/reviews/response_to_reviewers.md`). Fit all three
> candidate models with `log_likelihood=True`, compare them with LOO, report
> Δloo and Pareto-k reliability, and produce a comparison table for
> `paper/assets/tables/loo_comparison.tex` mirrored in
> `paper/experiments/ablation.md`. If LOO is unreliable, fall back to WAIC and
> say so.

This triggers pymc for model comparison: fitting multiple Bayesian models and
ranking them with information criteria. The skill reuses the data and seed
from the original run, fits each candidate with NUTS and
`idata_kwargs={'log_likelihood': True}`, computes LOO via ArviZ, inspects
Pareto-k (k > 0.7 flags unreliable observations) and falls back to WAIC per
the rules in `references/sampling_inference.md`, applies the Δloo thresholds
(< 2 similar, 2-4 weak, 4-10 moderate, > 10 strong), and prefers the simpler
model when evidence is weak. It emits the LaTeX comparison table into
`paper/assets/tables/`, mirrors a markdown version in
`paper/experiments/ablation.md`, adds one run row per candidate to
`paper/experiments/run_ledger.md`, and drafts the response point in
`paper/reviews/response_to_reviewers.md`. Negative findings (a favored model
that LOO does not actually support) are recorded honestly in
`paper/experiments/dead_ends.md` rather than overstated to the reviewer.

## Scenario 3: Prior sensitivity analysis for the statistics note

> Before we freeze the methods section, run a prior sensitivity analysis on
> the hierarchical model from Scenario 1: refit with weakly informative,
> informative, and skeptical priors on the treatment effect, and confirm the
> posterior conclusion is robust. Summarize in
> `paper/experiments/statistics.md` and flag any non-robust conclusion.

This triggers pymc: the same Bayesian model refit under alternative prior
specifications to test robustness. The skill reuses the data, sampler config,
and seed, varies only the prior on the focal parameter (per the prior
selection guide in `references/distributions.md`), reruns the prior predictive
check for each, refits, and compares the posterior summaries. It records each
variant as a run row in `paper/experiments/run_ledger.md`, writes a
sensitivity table to `paper/assets/tables/`, and summarizes whether the
conclusion (sign and HDI excluding zero) is stable across priors in
`paper/experiments/statistics.md`. If the conclusion flips under a defensible
prior, the skill marks the claim `partial` in
`paper/experiments/evidence_matrix.md` and surfaces the fragility in
`paper/logs/decision_log.md` rather than hiding it.
