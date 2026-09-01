---
name: statsmodels
description: 'Implementation skill: fit statsmodels models (OLS/GLM, discrete choice, mixed effects, ARIMA/SARIMAX) with diagnostics, coefficient inference, and assumption tests for paper/experiments/. Do not use for deep learning (defer pytorch-lightning) or Bayesian inference (defer pymc); for test selection prefer statistical-analysis as primary.'
---

# statsmodels

## Purpose

Provide an implementation-only supporting skill for fitting and diagnosing
classical statistical models with statsmodels: linear regression (OLS, WLS,
GLS, GLSAR, quantile, mixed effects), generalized linear models (logistic,
Poisson, Negative Binomial, Gamma, Tweedie), discrete-choice and count models
(Logit/Probit, MNLogit, ordinal, zero-inflated, hurdle), and time series
(ARIMA, SARIMAX, VAR, VARMAX, exponential smoothing, state space). In
Auto-01-tiny-research this skill owns the model-fitting recipes and
diagnostic procedures whose results become the evidence backing the paper's
claims, and maps every coefficient table, test statistic, and forecast onto
the `paper/experiments/` ledger so downstream skills (`08-markdown-draft`,
`09-tex-freeze-formalize`, `13-reviewer-response`) can cite it.

This is a TIER B tool skill (implementation support). For statistical
planning — choosing the right test, designing the inference strategy, or
producing APA-style reporting — prefer the `statistical-analysis` skill as the
primary; this skill executes the modeling once the plan is set. Plotting of
diagnostics/forecasts defers to `scientific-visualization` (matplotlib) for
rendering into `paper/assets/figures/`.

## Use When

- A claim in `paper/experiments/evidence_matrix.md` requires a regression
  coefficient with standard error / confidence interval / p-value (OLS, GLM,
  or mixed-effects) on tabular or panel data.
- A reviewer asks for an assumption test (Breusch-Pagan heteroskedasticity,
  Durbin-Watson / Ljung-Box autocorrelation, Jarque-Bera normality, VIF) to
  defend a fitted model in `paper/reviews/response_to_reviewers.md`.
- A count or binary outcome needs the correct link family (Poisson vs
  Negative Binomial after an overdispersion check; Logit/Probit with marginal
  effects), reported with rate/odds ratios.
- A time-series claim needs ARIMA/SARIMAX/VAR estimation, stationarity testing
  (ADF, KPSS), or a forecast with prediction intervals.
- A model-comparison table (AIC/BIC, likelihood-ratio test for nested models)
  or an ANOVA / post-hoc table is needed for `paper/assets/tables/` and
  `paper/experiments/ablation.md`.

Do not use this skill for deep learning or neural-network training (defer to
pytorch / pytorch-lightning), Bayesian model inference with priors (defer to
pymc), large-scale GPU forecasting, or non-Python stacks. It is also not an
execution harness: in this repo it documents and recipes analyses; it does
not run production jobs. For guided test selection and APA reporting, prefer
`statistical-analysis` as the primary planning skill.

## Required Inputs

- A data frame / matrix or a path to data already logged in
  `paper/experiments/run_ledger.md`. Do not invent or fabricate data.
- The claim ID(s) this model must support, from
  `paper/experiments/evidence_matrix.md`, and the metric / reporting style
  mandated by `paper/refs/target_journal.md` and
  `paper/experiments/statistics.md` (e.g. coefficient + 95% CI, robust SE
  type, link family).
- The outcome type (continuous / binary / count / ordinal / time series) so
  the model family can be matched; for time series, the time index and any
  exogenous regressors.
- A target output path for any persisted table under
  `paper/assets/tables/` or result note under `paper/experiments/`.
- statsmodels >= 0.14.6 with NumPy/SciPy/pandas; optional scikit-learn for
  cross-validation and matplotlib/seaborn for diagnostic plots (rendered by
  `scientific-visualization`). The user is responsible for installing these;
  this skill does not pin or ship a runtime.
- No API keys or credentials are required. If any external data source needs
  a credential (e.g. a private dataset token), the user must provide it;
  never hardcode or store it.

## Workflow

1. Read the target claim and its required statistic from
   `paper/experiments/evidence_matrix.md` and `paper/refs/target_journal.md`.
   Match the model family to the outcome type (continuous -> OLS/GLS;
   binary -> Logit/Probit; count -> Poisson/NB; time series -> ARIMA/SARIMAX)
   using the selection guides in the references.
2. Load only data referenced by `paper/experiments/run_ledger.md`; if absent
   or unlogged, stop (see Stop With) rather than substituting.
3. Prepare data leakage-safely: add the intercept via `sm.add_constant()`
   (unless intercept is deliberately excluded), handle missingness, encode
   categoricals (formula API or manual dummy coding). For time series, check
   stationarity (ADF/KPSS) and difference if non-stationary before fitting
   ARIMA.
4. Fit the model using `statsmodels.api` or `statsmodels.formula.api`; capture
   and record any convergence warnings — do not silently proceed.
5. Run the relevant diagnostics from `references/stats_diagnostics.md`:
   heteroskedasticity (Breusch-Pagan/White), autocorrelation (Durbin-Watson,
   Breusch-Godfrey, Ljung-Box), normality (Jarque-Bera), multicollinearity
   (VIF), influence (Cook's distance, leverage, DFFITS). For count models,
   check overdispersion and switch to Negative Binomial / zero-inflated if
   indicated.
6. Apply robust standard errors (HC0-HC3, HAC/Newey-West, or cluster-robust)
   when diagnostics warrant; document the choice.
7. Compare candidate models with AIC/BIC (non-nested) or likelihood-ratio
   test (nested); record each variant in `paper/experiments/ablation.md`.
8. Persist: write the coefficient / model-comparison table to
   `paper/assets/tables/`, append a run row to
   `paper/experiments/run_ledger.md` (model family, formula, robust SE type,
   key statistic + CI, sample size, data ref, claim ID), add a statistical
   note to `paper/experiments/statistics.md`, and update
   `paper/experiments/evidence_matrix.md` status (`supported` / `partial` /
   `refuted`).
9. Surface methodological decisions in `paper/logs/decision_log.md`; record
   failed model specifications honestly in `paper/experiments/dead_ends.md`.

## Output Contract

- A run row in `paper/experiments/run_ledger.md` with: model family + formula,
  estimator options (robust SE type, link/family), point estimate + CI / test
  statistic + p-value, sample size, and the data/claim IDs it supports.
- Updated status in `paper/experiments/evidence_matrix.md` for every claim the
  model addresses (`supported` / `partial` / `refuted` / `unsupported`).
- A coefficient table or model-comparison table under `paper/assets/tables/`
  when more than one variant is fitted; mirror it into
  `paper/experiments/ablation.md`.
- A statistical note in `paper/experiments/statistics.md` recording the test,
  assumption checks, robust SE choice, and any multiple-comparison correction.
- A reproducibility note in `paper/experiments/reproducibility.md` covering
  statsmodels/NumPy/SciPy versions, the exact formula and estimator options,
  and the data ref.
- Diagnostic plot requests handed to `scientific-visualization` for rendering
  into `paper/assets/figures/` (residual-vs-fitted, Q-Q, ACF/PACF); this
  skill produces the arrays and justification, not the rendered files.
- Optional decision / dead-end entries in `paper/logs/decision_log.md` and
  `paper/experiments/dead_ends.md`.
- No executable training/inference scripts shipped into the repo (this is a
  paper repo, not a runtime); code stays as documented recipes in
  `references/`.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only statsmodels`
- `python src/S03_Scripts/validate_project.py`
- Confirm every model referenced by `paper/experiments/evidence_matrix.md`
  has a matching row in `paper/experiments/run_ledger.md` (no orphan claims).
- Confirm no inference is reported for a claim the matrix marks
  `unsupported`, `missing_evidence`, or `refuted`.
- Confirm the intercept handling (`sm.add_constant` or `0 + ` in formula) and
  robust SE type are recorded for each fitted model.
- Confirm stationarity was checked before fitting ARIMA (grep the cited
  recipe for `adfuller` / `kpss` — must be present for any time-series claim).
- Confirm statsmodels version and exact formula are recorded in
  `paper/experiments/reproducibility.md`.
- Confirm no raw model objects (`.pickle` / `.save`) are persisted into the
  paper repo; only recipes, tables, and metrics.

## Boundaries

- Do not run deep-learning, LLM, or neural-network training here; defer to
  pytorch / pytorch-lightning. Classical statistical models only.
- Do not perform Bayesian inference with priors; defer to pymc.
- Do not fabricate coefficients, datasets, or test statistics; if a result is
  missing, mark the claim `missing_evidence` and stop.
- Do not fit ARIMA/SARIMAX on non-stationary data without differencing or
  explicit justification recorded in `paper/logs/decision_log.md`.
- Do not use Poisson when overdispersion is present without switching to
  Negative Binomial or documenting why Poisson is retained.
- Do not compare non-nested models with a likelihood-ratio test; use AIC/BIC.
- Do not persist raw fitted model objects / `.pickle` / `.save` artifacts into
  the paper repo; record recipes and metrics, not model binaries.
- Do not write outputs anywhere except `paper/experiments/`,
  `paper/assets/tables/`, and the designated logs; never into `paper/tex/`,
  `paper/refs/`, or `paper/submission/`.
- Do not copy the upstream `scripts/` executable code into this repo; this
  skill ships `references/` documentation only.

## Stop With

- The data needed to compute a claim is not present in
  `paper/experiments/run_ledger.md` and the user has not supplied it.
- The required model family, link, or robust SE type is unspecified by
  `paper/refs/target_journal.md` / `paper/experiments/statistics.md` and the
  user has not disambiguated.
- A convergence failure or perfect-separation / singular-matrix warning
  appears and cannot be resolved by simplifying the specification — report in
  `paper/experiments/dead_ends.md` and pause rather than report a fragile fit.
- Stationarity cannot be achieved for a time-series model and the user has
  not authorized an alternative (e.g. differencing, transformation).
- statsmodels or a required dependency is unavailable and the user cannot
  install it; do not silently fall back to a different library.
- The result would contradict the claim's required direction and the user has
  not authorized reporting a `refuted` finding — surface it in
  `paper/logs/decision_log.md` and wait.

## References

- Linear regression models (OLS/WLS/GLS/quantile/mixed effects, diagnostics,
  robust SEs): `.agent/skills/statsmodels/references/linear_models.md`
- Generalized linear models (families, links, interpretation, residuals):
  `.agent/skills/statsmodels/references/glm.md`
- Discrete choice & count models (Logit/Probit, MNLogit, ordinal,
  zero-inflated, hurdle, marginal effects):
  `.agent/skills/statsmodels/references/discrete_choice.md`
- Time series (AR/ARIMA/SARIMAX/VAR/VARMAX, stationarity, forecasting, IRF):
  `.agent/skills/statsmodels/references/time_series.md`
- Statistical tests & diagnostics (residual, influence, hypothesis tests,
  ANOVA, multiple comparisons, robust covariance, power):
  `.agent/skills/statsmodels/references/stats_diagnostics.md`
- Invocation scenarios: `.agent/skills/statsmodels/examples/prompts.md`
- Workspace artifacts: `paper/experiments/evidence_matrix.md`,
  `paper/experiments/run_ledger.md`, `paper/experiments/statistics.md`,
  `paper/experiments/ablation.md`, `paper/experiments/reproducibility.md`,
  `paper/experiments/dead_ends.md`, `paper/experiments/insights.md`,
  `paper/assets/tables/`, `paper/assets/figures/`,
  `paper/refs/target_journal.md`, `paper/logs/decision_log.md`
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills
  v2.53.0 (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://www.statsmodels.org/stable/ ,
  https://www.statsmodels.org/stable/user-guide.html
