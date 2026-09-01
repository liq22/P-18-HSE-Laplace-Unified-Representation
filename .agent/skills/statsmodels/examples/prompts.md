# statsmodels — invocation scenarios

Realistic prompts for invoking the statsmodels implementation skill inside
the Auto-01-tiny-research workspace. Each scenario shows the kind of request
that should trigger this skill, the artifacts it reads, and the workspace
outputs it must produce. This is a TIER B tool skill — for planning the
inference strategy (which test, which family, APA reporting) prefer
`statistical-analysis` as the primary; this skill executes the model fitting.

## Scenario 1: OLS with assumption tests for a regression claim

> The paper claims variable X has a statistically significant positive effect
> on Y after controlling for Z1 and Z2, using the data logged in
> `paper/experiments/run_ledger.md` (run `R-012`, n=420). Fit OLS with a
> proper intercept, report the coefficient on X with a 95% CI, run
> Breusch-Pagan for heteroskedasticity and VIF for multicollinearity, and use
> HC3 robust standard errors if heteroskedasticity is detected. Update claim
> `C-05` in `paper/experiments/evidence_matrix.md`.

This triggers statsmodels because the request is a classical linear
regression with rigorous diagnostics and coefficient inference — exactly the
`references/linear_models.md` and `references/stats_diagnostics.md` recipes
this skill owns. The skill reads the data ref and claim requirements, fits
`sm.OLS(y, sm.add_constant(X))` (or the `smf.ols` formula), runs the
Breusch-Pagan and VIF diagnostics, applies HC3 robust SEs if warranted, and
writes the coefficient table to `paper/assets/tables/`, a run row to
`paper/experiments/run_ledger.md` (formula, robust SE type, coefficient + CI,
n, data ref, claim ID `C-05`), a note to `paper/experiments/statistics.md`,
and updates `C-05` status in `paper/experiments/evidence_matrix.md`. Versions
and formula go to `paper/experiments/reproducibility.md`. Do NOT use
scikit-learn's `LinearRegression` here — it lacks the inference/diagnostics
required; do NOT render the residual-vs-fitted plot yourself, hand the arrays
to `scientific-visualization`.

## Scenario 2: Count outcome — Poisson vs Negative Binomial with overdispersion check

> Claim `C-08` says the rate of events increases with treatment dose. The
> outcome is a count. Fit Poisson, check overdispersion via the
> Pearson-chi2 / df_resid ratio, and if overdispersed refit as Negative
> Binomial. Report rate ratios (exp(beta)) with 95% CI in
> `paper/assets/tables/count_model.tex` and `paper/experiments/ablation.md`.

This triggers statsmodels for a count-data model with an explicit
overdispersion-driven model-selection step — covered by
`references/discrete_choice.md` and `references/glm.md`. The skill fits
`sm.GLM(y, X, family=Poisson())`, computes the overdispersion ratio, and
either reports rate ratios from Poisson or refits
`NegativeBinomial` if the ratio exceeds the threshold (documenting the switch
in `paper/logs/decision_log.md`). It writes both the LaTeX table to
`paper/assets/tables/` and a mirrored markdown table to
`paper/experiments/ablation.md`, with a run row per variant in
`paper/experiments/run_ledger.md` and an overdispersion note in
`paper/experiments/statistics.md`. Model comparison uses AIC/BIC (the two are
non-nested, so no likelihood-ratio test). Do NOT use OLS on the count outcome;
do NOT silently keep Poisson when overdispersion is present.

## Scenario 3: ARIMA forecast with stationarity testing

> Claim `C-11` forecasts the next 10 steps of the monthly series in run
> `R-019`. Test stationarity with ADF and KPSS, difference if needed, choose
> (p, q) from ACF/PACF, fit ARIMA, run Ljung-Box on the residuals, and report
> the 10-step forecast with 95% prediction intervals. Target journal
> (`paper/refs/target_journal.md`) requires the forecast interval, not just
> point estimates.

This triggers statsmodels for univariate time-series modeling — covered by
`references/time_series.md`. The skill runs `adfuller` and `kpss`, differences
the series if non-stationary (recording d), inspects ACF/PACF to choose p and
q, fits `ARIMA(y, order=(p, d, q))`, and checks residual autocorrelation with
Ljung-Box. The 10-step forecast and `summary_frame()` (mean + prediction
interval) are written as a table to `paper/assets/tables/`, with the model
order, differencing decision, and Ljung-Box result recorded in a run row of
`paper/experiments/run_ledger.md` and `paper/experiments/statistics.md`. The
ACF/PACF and residual diagnostics plots are handed to `scientific-visualization`
for rendering into `paper/assets/figures/`. Do NOT fit ARIMA on non-stationary
data without differencing; do NOT report a point forecast without the
prediction interval the journal requires.
