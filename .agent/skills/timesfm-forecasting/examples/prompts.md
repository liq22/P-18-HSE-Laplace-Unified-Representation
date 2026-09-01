# timesfm-forecasting — invocation scenarios

Realistic prompts for using this skill inside the Auto-01-tiny-research
single-paper workspace. Each scenario names the claim it supports and the
`paper/` artifacts it must produce or update. These are prompts (recipes),
not runnable scripts — heavy ML execution happens in the project's own
analysis environment.

## Scenario 1: 12-month forecast with holdout metrics for a sales-demand claim

We are writing a paper whose central claim is that a zero-shot foundation
model produces calibrated 12-month demand forecasts that match a tuned
ARIMA baseline within a stated error margin. The TimesFM result is one arm
of an ablation; the statsmodels arm is handled separately by `statsmodels`.

> Claim `C-04` in `paper/experiments/evidence_matrix.md` needs a 12-month
> ahead forecast of the `monthly_demand` series (logged in
> `paper/experiments/run_ledger.md` as run `R-007`), with an 80% prediction
> interval and a holdout evaluation. Use TimesFM 2.5 (200M) with
> `max_context=512`, `max_horizon=12`, `normalize_inputs=True`,
> `use_continuous_quantile_head=True`, `fix_quantile_crossing=True`, and
> `infer_is_positive=True` (demand is non-negative). Hold out the last 12
> observed months, forecast them, and report MAE, RMSE, MAPE, and the
> empirical 80% PI coverage to `paper/experiments/statistics.md` under C-04.
> Append a run row (checkpoint, config, CPU/GPU tier, seed, wall-clock) to
> `paper/experiments/run_ledger.md`, write the forecast+PI table to
> `paper/assets/tables/forecast_C04_timesfm.csv`, then hand the figure
> request (history + median + 80% band) to `scientific-visualization` for
> `paper/assets/figures/fig_C04_timesfm.png`.

Acceptance: `point.shape == (1, 12)`, `quantiles.shape == (1, 12, 10)`,
`np.isnan(point).any()` is False, q10 ≤ median ≤ q90 elementwise, and 80% PI
holdout coverage is within 70–90% (else open a question in
`paper/logs/open_questions.md`).

## Scenario 2: Probabilistic anomaly flag on a sensor-vitals series

The paper argues that the TimesFM quantile bands double as a probabilistic
anomaly detector on a streaming sensor signal, and we want to defend this
against a reviewer request for an explicit outlier analysis.

> Claim `C-09` (reviewer R2.3, see `paper/reviews/ai_review.md`) asks us to
> flag anomalous sensor readings on the `temp_sensor_A` series. Use TimesFM
> 2.5 with `infer_is_positive=False` (the signal is signed/centered). Forecast
> the holdout window, take the 80% PI `[q[:,:,1], q[:,:,9]]` (index 1 = q10,
> index 9 = q90; remember index 0 is the MEAN, not a percentile), and the
> 90% PI using the same q10/q90 band; flag holdout points outside q10–q90 as
> CRITICAL and outside q20–q80 as WARNING. Separately, on the historical
> context, detrend with a linear `np.polyfit`, Z-score the residuals
> (CRITICAL_Z = 3.0, WARNING_Z = 2.0 as module constants), and record both
> the historical and forecast anomaly lists in `paper/experiments/insights.md`
> under C-09. Summarize counts in `paper/experiments/statistics.md`. If the
> forecast anomaly rate exceeds 15% of the holdout, open a question in
> `paper/logs/open_questions.md` (possible distribution shift) and note the
> decision in `paper/logs/decision_log.md`.

Acceptance: anomaly thresholds defined once as constants (never inline), the
historical detector operates on detrended residuals (not raw values), and the
forecast detector uses the q10/q90 indices 1 and 9 (not 0 — index 0 is the
mean).

## Scenario 3: Batch covariate forecast for a multi-store retail panel

The paper claims TimesFM 2.5 with exogenous covariates (price + holiday)
improves per-store forecasts over the no-covariate baseline, supporting an
ablation in `paper/experiments/ablation.md`.

> Claim `C-12` needs per-store 4-week-ahead forecasts across 30 stores, with
> and without covariates, for the ablation table. Use TimesFM 2.5 +
> `timesfm[xreg]`, `forecast_with_covariates(...)`, passing
> `dynamic_numerical_covariates={"price": ...}`,
> `dynamic_categorical_covariates={"holiday": ...}`, and
> `static_categorical_covariates={"region": ...}`. Build each covariate dict
> OUTSIDE the per-store loop (do not shadow the loop variable inside a
> comprehension), and ensure every dynamic covariate spans BOTH the context
> window AND the full 4-week horizon. Report both arms (covariate vs
> no-covariate) MAE/RMSE to `paper/experiments/statistics.md`, append two run
> rows to `paper/experiments/run_ledger.md`, and add the comparison row to
> `paper/experiments/ablation.md`. Confirm distinct price arrays per store
> before fitting.

Acceptance: every dynamic covariate array length == context + horizon; no
loop-variable shadowing in covariate construction; covariate MAE strictly
better than no-covariate MAE on the holdout, or document why not in
`paper/logs/open_questions.md`.
