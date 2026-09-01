---
name: pymc
description: 'Implementation skill for Bayesian modeling with PyMC: hierarchical/MCMC-NUTS, predictive checks, LOO/WAIC for paper evidence. Prefer the planning skill as primary; defer plots to scientific-visualization, classical ML to scikit-learn, deep-learning training to pytorch-lightning. Do not use for deep nets, frequentist-only inference, or GPU training.'
---

# pymc

## Purpose

Provide Bayesian probabilistic-programming guidance and reference material with
PyMC (6.x): hierarchical/multilevel models, MCMC sampling (NUTS), variational
inference (ADVI), prior and posterior predictive checks, convergence
diagnostics (R-hat, ESS, divergences), and model comparison via LOO/WAIC. In
Auto-01-tiny-research this skill is a TIER B implementation-only tool skill:
it documents and recipes the Bayesian analyses whose posterior summaries and
model-comparison results become evidence in `paper/experiments/`, cited by the
downstream `08-markdown-draft`, `09-tex-freeze-formalize`, and
`13-reviewer-response` skills. It is not a primary planning skill; when
analytic design is undecided, prefer the relevant planning skill first.

## Use When

- A claim in `paper/experiments/evidence_matrix.md` requires a Bayesian
  estimate: a posterior mean/median with HDI credible interval, a Bayesian
  regression coefficient, or a hierarchical (partial-pooling) effect.
- A reviewer asks for principled uncertainty quantification, prior
  sensitivity, or a model-comparison result (LOO/WAIC) to go into
  `paper/reviews/response_to_reviewers.md`.
- Grouped/multilevel data needs partial pooling (e.g. subjects, sites, batches)
  and the analysis must be reproducible and recorded in
  `paper/experiments/run_ledger.md`.
- A Bayesian model comparison or an ablation over model structures must be
  reported in `paper/experiments/ablation.md` and `paper/assets/tables/`.
- Convergence diagnostics (R-hat, ESS, divergences) must be documented for
  `paper/experiments/statistics.md` and `paper/experiments/reproducibility.md`.

Do not use this skill for deep neural networks or large-scale GPU training
(defer to pytorch / pytorch-lightning), classical tabular ML such as
random forests or SVMs (defer to scikit-learn), frequentist-only hypothesis
testing without a Bayesian framing (defer to statsmodels /
statistical-analysis), or producing publication figures (defer to
scientific-visualization / matplotlib). It is also not an execution harness:
in this repo it documents and recipes analyses; it does not run production
sampling jobs or ship runnable sampler scripts.

## Required Inputs

- The dataset and the claim ID(s) this analysis must support, taken from
  `paper/experiments/evidence_matrix.md` with the data referenced in
  `paper/experiments/run_ledger.md`. Do not invent or fabricate data.
- The estimand and the inferential target (posterior summary, predictive
  distribution, or model-comparison criterion) mandated by
  `paper/refs/target_journal.md` and `paper/experiments/statistics.md`.
- A target output path for any persisted summary under
  `paper/experiments/` or `paper/assets/tables/`.
- PyMC >= 6.0 (Python 3.12+) with ArviZ, NumPy, and PyTensor; optional
  `nutpie`/`numypro`/`blackjax` samplers. The user is responsible for
  installing and pinning these in the project environment; this skill does not
  ship a runtime.
- No API keys or credentials are required for PyMC itself. If any external
  data source or model hub needs a credential (e.g. a private dataset token),
  the user must provide it; never hardcode or store it.

## Workflow

1. Read the target claim and its required estimand from
   `paper/experiments/evidence_matrix.md` and `paper/refs/target_journal.md`.
   Confirm the Bayesian framing is appropriate before proceeding.
2. Load only data referenced by `paper/experiments/run_ledger.md`; if the data
   is absent or unlogged, stop (see Stop With) rather than substituting.
3. Prepare data: standardize continuous predictors, center outcomes, declare
   named dimensions via `coords`, and treat missing values as parameters
   rather than dropping them. Record these choices for
   `paper/experiments/reproducibility.md`.
4. Build the model using the patterns in `references/workflows.md` and choose
   priors/likelihoods from `references/distributions.md`. Use weakly
   informative priors, `HalfNormal`/`Exponential` for scales, and
   non-centered parameterization for hierarchical effects (avoids
   divergences).
5. Run a prior predictive check (`pm.sample_prior_predictive`) before fitting;
   if priors generate implausible data, adjust and re-check. Do not skip this.
6. Fit with the sampler from `references/sampling_inference.md`: NUTS via
   `pm.sample(draws, tune, chains=4, target_accept>=0.9, random_seed=...)`,
   requesting `idata_kwargs={'log_likelihood': True}` when model comparison is
   anticipated. Use ADVI only for initialization or quick exploration.
7. Check diagnostics (R-hat < 1.01, ESS > 400, zero or few divergences, no
   max-treedepth saturation). If diagnostics fail, raise `target_accept`,
   reparameterize, or run longer — never report a non-converged posterior.
8. Run a posterior predictive check (`pm.sample_posterior_predictive`) and
   confirm the model reproduces the observed data; record misspecification
   honestly in `paper/experiments/dead_ends.md` if it does not.
9. When comparing models, compute LOO/WAIC (`references/sampling_inference.md`)
   and inspect Pareto-k; apply the delta thresholds (Δloo < 2 similar, > 10
   strong) and prefer the simpler model when evidence is weak.
10. Persist: write posterior summaries and HDI intervals as a table to
    `paper/assets/tables/` (and mirror in `paper/experiments/ablation.md` for
    comparisons), append a run row to `paper/experiments/run_ledger.md`
    (model spec, priors, sampler config, seed, diagnostic values, data/claim
    IDs), update `paper/experiments/evidence_matrix.md` claim status, and note
    versions + seed in `paper/experiments/reproducibility.md`. Surface
    methodological choices in `paper/logs/decision_log.md`.

## Output Contract

- A run row in `paper/experiments/run_ledger.md` recording model specification,
  priors, sampler (`draws`/`tune`/`chains`/`target_accept`), `random_seed`,
  key diagnostics (max R-hat, min ESS, divergence count), and the data/claim
  IDs supported.
- Updated status in `paper/experiments/evidence_matrix.md` for every claim the
  run addresses (`supported` / `partial` / `refuted` / `unsupported`).
- Posterior summaries (mean/median with HDI credible intervals) and any
  model-comparison table (LOO/WAIC, Δ, weights) under `paper/assets/tables/`,
  mirrored in `paper/experiments/ablation.md` when multiple structures were
  compared.
- A statistical note in `paper/experiments/statistics.md` when credible
  intervals, prior-sensitivity checks, or model comparisons were computed.
- A reproducibility note in `paper/experiments/reproducibility.md` covering
  PyMC/ArviZ/PyTensor versions, sampler, `random_seed`, and exact data ref.
- Optional decision/dead-end entries in `paper/logs/decision_log.md` and
  `paper/experiments/dead_ends.md` for prior choices, reparameterizations, or
  models that failed to converge or fit.
- No executable sampling/training scripts shipped into the repo (this is a
  paper repo, not a Bayesian runtime); code stays as documented recipes in the
  references, and no NetCDF/pickle posterior blobs are persisted as evidence.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only pymc`
- `python src/S03_Scripts/validate_project.py`
- Confirm every run referenced by `paper/experiments/evidence_matrix.md` has a
  matching row in `paper/experiments/run_ledger.md` (no orphan claims).
- Confirm no posterior summary is reported for a claim the matrix marks
  `unsupported`, `missing_evidence`, or `refuted`.
- Confirm R-hat < 1.01, ESS > 400, and divergence counts are recorded for each
  reported posterior in `paper/experiments/statistics.md`; a non-converged
  chain must not be cited as evidence.
- Confirm hierarchical models used non-centered parameterization and that
  priors passed a prior predictive check (grep the cited recipe / decision
  log).
- Confirm `random_seed` and PyMC/ArviZ versions are recorded in
  `paper/experiments/reproducibility.md`.

## Boundaries

- Do not run deep-learning, LLM, or GPU-distributed training here; defer to
  pytorch / pytorch-lightning. Bayesian probabilistic models only.
- Do not fabricate posteriors, datasets, or benchmark numbers; if a result is
  missing, mark the claim `missing_evidence` and stop.
- Do not report a posterior from a chain that failed convergence diagnostics
  (R-hat > 1.01, ESS < 400, many divergences) — fix the sampler first.
- Do not skip the prior predictive check; priors that imply implausible data
  invalidate the downstream inference.
- Do not persist raw NetCDF posterior blobs or pickled model objects into the
  paper repo; record recipes, summaries, and metrics, not sampler artifacts.
- Do not copy the upstream `scripts/` executable sampling/diagnostic code or
  the `assets/` runnable model templates into this repo; this skill ships
  `references/` documentation only (TIER B heavy-ML tool).
- Do not write outputs anywhere except `paper/experiments/`,
  `paper/assets/tables/`, and the designated logs; never into `paper/tex/`,
  `paper/refs/`, or `paper/submission/`.

## Stop With

- The data needed to compute a claim is not present in
  `paper/experiments/run_ledger.md` and the user has not supplied it.
- The estimand, inferential target, or required credible-interval level is
  unspecified by `paper/refs/target_journal.md` /
  `paper/experiments/statistics.md` and the user has not disambiguated.
- Diagnostics fail and cannot be fixed by reparameterization, stronger priors,
  higher `target_accept`, or longer chains within the available compute.
- The prior predictive check produces implausible data and the user has not
  agreed on revised priors.
- LOO Pareto-k diagnostics are unreliable (k > 0.7 for many observations) and
  WAIC or k-fold CV are not viable given the data.
- PyMC or a required dependency is unavailable and the user cannot install it;
  do not silently fall back to a frequentist method or a different library.
- The result would contradict the claim's required direction and the user has
  not authorized reporting a `refuted` finding — surface it in
  `paper/logs/decision_log.md` and wait.

## References

- Distribution catalog: `.agent/skills/pymc/references/distributions.md`
- Sampling & inference methods: `.agent/skills/pymc/references/sampling_inference.md`
- Workflows & common patterns: `.agent/skills/pymc/references/workflows.md`
- Invocation scenarios: `.agent/skills/pymc/examples/prompts.md`
- Workspace artifacts: `paper/experiments/evidence_matrix.md`,
  `paper/experiments/run_ledger.md`, `paper/experiments/statistics.md`,
  `paper/experiments/ablation.md`, `paper/experiments/reproducibility.md`,
  `paper/experiments/dead_ends.md`, `paper/experiments/insights.md`,
  `paper/assets/tables/`, `paper/refs/target_journal.md`,
  `paper/logs/decision_log.md`
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://www.pymc.io/ ,
  https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html ,
  https://python.arviz.org/
