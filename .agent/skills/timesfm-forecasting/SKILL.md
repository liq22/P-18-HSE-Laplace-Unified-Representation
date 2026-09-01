---
name: timesfm-forecasting
description: 'Implementation skill: zero-shot univariate forecasting with TimesFM (point + quantile intervals, holdout metrics, anomaly flags). Do not use for interpretable ARIMA/VAR (statsmodels), Bayesian forecasting (pymc), DL training (pytorch-lightning), or plotting (scientific-visualization). Prefer statistical-analysis as primary planning skill.'
---

# timesfm-forecasting

## Purpose

Provide an implementation-only supporting skill for zero-shot time-series
forecasting with Google's TimesFM foundation model (a pretrained decoder-only
transformer, ~200M params for the recommended 2.5 checkpoint). Feed any
univariate series and get back a median point forecast plus a 10-slice
quantile forecast that yields calibrated prediction intervals, with no model
training. In Auto-01-tiny-research this skill owns the forecasting recipes and
the evaluation/metric procedures whose results become the evidence backing the
paper's forecasting claims, mapping every forecast, holdout score, and
anomaly flag onto `paper/experiments/` so downstream skills
(`08-markdown-draft`, `09-tex-freeze-formalize`, `13-reviewer-response`) can
cite it and `06-experiment-ops` / `07-experiment-audit` can reproduce it.

This is a TIER B tool skill (implementation support). It is not a planning
skill: for choosing the forecasting strategy, designing the evaluation
protocol, or selecting metrics, prefer `statistical-analysis` as the primary
planning skill and execute the chosen TimesFM recipe here. Classical
statistical forecasting with interpretable coefficients (ARIMA/SARIMAX, VAR,
exponential smoothing) defers to `statsmodels`; Bayesian time-series modeling
defers to `pymc`; training/fine-tuning any deep-learning model defers to
`pytorch-lightning`; and rendering forecast figures with prediction-interval
bands into `paper/assets/figures/` defers to `scientific-visualization`.

## Use When

- A claim in `paper/experiments/evidence_matrix.md` requires a forecast of a
  univariate series (sales, demand, sensor, vitals, price, energy, weather,
  load) with point values AND prediction intervals — and a zero-shot
  foundation model is acceptable instead of a hand-tuned statistical model.
- A reviewer asks for a modern neural-baseline forecast to compare against a
  classical baseline (e.g. TimesFM vs the statsmodels ARIMA baseline), to be
  tabulated in `paper/assets/tables/` and discussed in
  `paper/experiments/ablation.md`.
- A holdout evaluation is needed: forecast the last H steps and report MAE /
  RMSE / MAPE plus 80% prediction-interval coverage, logged to
  `paper/experiments/statistics.md` and `paper/experiments/run_ledger.md`.
- Batch forecasting of many related series (e.g. per-store, per-sensor) is
  needed, where the model handles variable lengths and a shared horizon.
- A probabilistic anomaly check is needed: flag future or holdout points
  outside the q10–q90 band, recorded in `paper/experiments/insights.md` or
  `paper/experiments/dead_ends.md`.

Do not use this skill for: multivariate VAR / Granger causality (defer
`statsmodels`); time-series classification or clustering (use `aeon` or
`scikit-learn`); tabular (non-temporal) regression (defer `scikit-learn`);
interpretable coefficient inference (defer `statsmodels` or `pymc`); or any
task that actually requires training or fine-tuning a neural network (defer
`pytorch-lightning`). It is also not an execution harness in this repo:
Auto-01-tiny-research is a paper repo, not an ML runtime, so this skill
documents and recipes the analysis; it does not ship runnable training or
inference scripts (heavy ML tool — references/docs only).

## Required Inputs

- A univariate time series as a 1-D numeric array / `pandas.Series`, or a
  path to a CSV already registered in `paper/experiments/run_ledger.md`.
  TimesFM takes a **list of 1-D arrays** (one per series), never a 2-D matrix.
- The horizon `H` to forecast and the context window (`max_context`) — context
  must be ≥ 32 points (model minimum); warn and truncate if shorter.
- The claim ID(s) this forecast must support, from
  `paper/experiments/evidence_matrix.md`, and the metric / reporting style
  mandated by `paper/refs/target_journal.md` and
  `paper/experiments/statistics.md` (e.g. point forecast + 80% PI, or MAE with
  95% CI).
- For covariate forecasting (`forecast_with_covariates`, TimesFM 2.5 only):
  dynamic numerical / categorical and static covariate arrays spanning BOTH
  context and the full horizon — future covariates are mandatory, not
  optional.
- Environment note: TimesFM weights (~800 MB) download on demand from
  HuggingFace on first use and cache under `~/.cache/huggingface/` (or
  `$HF_HOME`). Any HuggingFace token or cache credential needed for gated or
  rate-limited access must be provided by the user; never hardcode or store
  such secrets in this repo (use `<user-provided-key>`). The model checkpoint
  `google/timesfm-2.5-200m-pytorch` is public, so a token is normally NOT
  required.

## Workflow

1. **Preflight resource check.** Before loading the model on any new machine,
   verify RAM ≥ 4 GB free (warn if 2–4 GB; block if < 2 GB), detect GPU/VRAM,
   confirm ≥ 2 GB free disk for the ~800 MB weights, and confirm Python 3.10+.
   This is a recipe step documented here — there is no bundled checker script
   in this port. Record the resource verdict in `paper/logs/decision_log.md`.
2. **Load the recommended checkpoint.**
   `timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")`.
   Avoid the archived v1/v2 (500M) checkpoints unless the run ledger
   justifies them; they need ≥ 16–32 GB RAM.
3. **Compile before forecasting** with a `timesfm.ForecastConfig`. Always set
   `normalize_inputs=True`, `use_continuous_quantile_head=True`, and
   `fix_quantile_crossing=True`. Set `max_context`/`max_horizon` to the run's
   values. Set `infer_is_positive=True` only for strictly non-negative series
   (counts, sales); set it `False` for temperature, returns, or signed
   anomalies. Call `torch.set_float32_matmul_precision("high")` on Ampere+.
4. **Prepare data.** Read the CSV/Series logged in `run_ledger.md`, drop or
   interpolate internal NaNs, cast to `np.float32`, and assemble a list of
   1-D arrays (one per series). Confirm `np.isnan(...).any()` is False.
5. **Forecast.** `point, quantiles = model.forecast(horizon=H, inputs=...)`.
   Returns `point` shape `(n_series, H)` and `quantiles` shape
   `(n_series, H, 10)`. For covariate-driven series, use
   `forecast_with_covariates(...)` (TimesFM 2.5 + `timesfm[xreg]`).
6. **Extract intervals with the correct indices.** Index 0 = MEAN (not q0).
   q10 = index 1, q20 = index 2, q80 = index 8, q90 = index 9, median = index
   5. Define named constants `IDX_Q10, IDX_Q20, IDX_Q80, IDX_Q90 = 1, 2, 8, 9`
   to avoid the most common off-by-one bug. 80% PI = `[q[:,:,1], q[:,:,9]]`.
7. **Evaluate on a holdout** when the claim needs accuracy: train on
   `values[:-H]`, compare to `values[-H:]`; compute MAE, RMSE, MAPE, and 80%
   PI empirical coverage (target ~80%). Log all of these to
   `paper/experiments/statistics.md` and append a row to
   `paper/experiments/run_ledger.md` (config, checkpoint, context, horizon,
   metrics, seed, runtime env).
8. **Anomaly flag (optional).** Flag holdout/forecast points outside q10–q90
   as anomalies (outside q20–q80 as warnings). For historical-context
   anomalies, detrend first (linear `np.polyfit` or seasonal decomposition)
   and Z-score the residuals — never Z-score raw trending values. Record
   findings in `paper/experiments/insights.md`.
9. **Hand off to rendering.** Persist the forecast table (date, point, lower,
   upper) to `paper/assets/tables/` and request the publication figure from
   `scientific-visualization` into `paper/assets/figures/`. Do not inline
   matplotlib rendering logic beyond the minimal handoff contract.

## Output Contract

- **Point forecast**: 2-D array, shape `(n_series, H)`, the median forecast.
- **Quantile forecast**: 3-D array, shape `(n_series, H, 10)`, with the
  index→quantile mapping in step 6 above; monotonic after
  `fix_quantile_crossing=True`.
- **Prediction intervals**: 80% PI from `[q[:,:,1], q[:,:,9]]`; 60% PI from
  `[q[:,:,2], q[:,:,8]]`; all aligned to the forecast dates.
- **Holdout metrics** (when claimed): MAE, RMSE, MAPE, and 80% PI coverage —
  written to `paper/experiments/statistics.md` with the claim ID they support.
- **Run ledger row**: checkpoint, `ForecastConfig` (context, horizon, batch
  size, key flags), hardware tier (CPU/GPU + VRAM), seed, wall-clock —
  appended to `paper/experiments/run_ledger.md` for
  `paper/experiments/reproducibility.md`.
- **No model weights committed**: weights live only in the HuggingFace cache;
  never write `.pt`/`.safetensors`/`.bin`/`.h5` into this repo. Any figure or
  table written to `paper/assets/` is the only persisted artifact.

## Validation

- Run `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only timesfm-forecasting` and resolve every ERROR (and easy WARNINGs, e.g. description length 80–350, presence of a `paper/` path reference).
- Run `python src/S03_Scripts/validate_project.py` to confirm the project workspace contract still holds after the port.
- Self-check the forecast shape before citing it: `point.shape == (n_series, H)` and `quantiles.shape == (n_series, H, 10)`; `np.isnan(point).any()` must be False.
- Quantile-ordering check: after `fix_quantile_crossing=True`, confirm `q[:,:,1] <= q[:,:,5] <= q[:,:,9]` elementwise.
- Holdout coverage sanity: 80% PI empirical coverage on the holdout should land roughly in 70–90%; flag wide deviations in `paper/experiments/statistics.md`.
- No secrets: grep the skill dir for `sk-[A-Za-z0-9_-]{20,}`, `gh[pousr]_...`, `AKIA[0-9A-Z]{16}`, and `BEGIN ... PRIVATE KEY`; any hit must be replaced with `<user-provided-key>`.

## Boundaries

- **No bundled executable scripts.** This is a heavy ML tool skill ported into
  a paper repo, not an ML runtime. The upstream `scripts/check_system.py`,
  `scripts/forecast_csv.py`, and `examples/*` runnable code are intentionally
  NOT copied. Use the recipes above inside the project's own analysis
  environment; defer heavy training/fine-tuning to `pytorch-lightning`.
- **Not a planning skill.** Prefer `statistical-analysis` for choosing the
  forecasting method, evaluation design, and metric set; this skill executes
  the TimesFM recipe once the plan is set.
- **Classical / interpretable models defer out.** ARIMA/SARIMAX/VAR with
  coefficient interpretation → `statsmodels`. Bayesian forecasting with priors
  → `pymc`. Classification/clustering → `aeon` / `scikit-learn`. Tabular
  regression → `scikit-learn`.
- **Plotting defers out.** All publication figures (forecast + PI bands) are
  rendered by `scientific-visualization` into `paper/assets/figures/`; this
  skill only hands off the data table.
- **Weights never committed.** TimesFM weights (~800 MB) are downloaded on
  demand and cached under `$HF_HOME`; never copy model binaries into the repo
  or commit them to Git LFS.
- **Hardware gate.** Do not attempt the 500M v1/v2 checkpoints on machines
  with < 16 GB RAM / < 8 GB VRAM; use the 200M 2.5 checkpoint.

## Stop With

- Point forecast + quantile forecast arrays written as a dated table to
  `paper/assets/tables/`, plus a `run_ledger.md` row and (if claimed) a
  `statistics.md` metrics block — then hand the figure request to
  `scientific-visualization`.
- An open question in `paper/logs/open_questions.md` if a series is too short
  (< 32 points), has unrecoverable NaN gaps, the 80% PI coverage on the
  holdout is far outside 70–90%, or `infer_is_positive` semantics are
  ambiguous for a signed series.
- A `paper/logs/decision_log.md` entry recording WHY TimesFM was chosen over a
  statsmodels baseline (and which checkpoint / hardware tier was used), so the
  choice is auditable by `07-experiment-audit` and defensible in
  `paper/reviews/response_to_reviewers.md`.

## References

- Bundled docs (references/, docs only — no executable code):
  `references/system_requirements.md` (hardware tiers, memory formulas, GPU
  selection), `references/api_reference.md` (`from_pretrained`,
  `ForecastConfig`, output shapes), `references/data_preparation.md` (input
  format, NaN handling, covariate setup).
- Workspace artifacts touched by this skill: `paper/experiments/evidence_matrix.md`,
  `paper/experiments/run_ledger.md`, `paper/experiments/statistics.md`,
  `paper/experiments/ablation.md`, `paper/experiments/reproducibility.md`,
  `paper/experiments/insights.md`, `paper/assets/tables/`,
  `paper/assets/figures/` (via `scientific-visualization`),
  `paper/logs/decision_log.md`, `paper/logs/open_questions.md`,
  `paper/reviews/response_to_reviewers.md`, `paper/refs/target_journal.md`.
- Upstream science: Das et al., "A Decoder-Only Foundation Model for
  Time-Series Forecasting", ICML 2024 (arXiv:2310.10688); model repo
  https://github.com/google-research/timesfm ; HuggingFace checkpoints under
  `google/timesfm-*`.
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills
  v2.53.0 (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
