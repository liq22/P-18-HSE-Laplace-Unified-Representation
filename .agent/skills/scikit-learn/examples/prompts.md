# scikit-learn — invocation scenarios

Realistic prompts for invoking the scikit-learn core capability skill inside
the Auto-01-tiny-research workspace. Each scenario shows the kind of request
that should trigger this skill, the artifacts it reads, and the workspace
outputs it must produce.

## Scenario 1: Cross-validated baseline classifier for a claim

> The paper claims our method beats a logistic-regression baseline at AUC on
> the dataset logged in `paper/experiments/run_ledger.md` (run `R-007`). The
> target journal (`paper/refs/target_journal.md`) wants stratified 5-fold CV
> with a 95% CI. Build a leakage-safe pipeline (median imputation +
> `StandardScaler` on numeric, `OneHotEncoder` on categorical, then
> `LogisticRegression(max_iter=1000)`), report AUC with CI, and update the
> claim `C-03` row in `paper/experiments/evidence_matrix.md`.

This triggers scikit-learn because the request is classical tabular
classification with cross-validated evaluation and a leakage-safe pipeline —
exactly the supervised + evaluation references this skill owns. The skill
reads the data ref and claim requirements, builds a `Pipeline` wrapping a
`ColumnTransformer` (no `fit` on the full dataset), runs `GridSearchCV`/CV
with the journal's protocol, and writes a run row to
`paper/experiments/run_ledger.md`, updates `C-03` in
`paper/experiments/evidence_matrix.md`, and records the seed + versions in
`paper/experiments/reproducibility.md`. Do NOT use pytorch or any deep model
here; do NOT persist a `.joblib` model blob into the repo — record the recipe
and metrics only.

## Scenario 2: Ablation table across model families

> I need an ablation table comparing RandomForest, GradientBoosting, and
> SVM-RBF on the same split and CV protocol, to go into
> `paper/assets/tables/ablation_models.tex` and `paper/experiments/ablation.md`.
> Use the exact feature pipeline from Scenario 1 so the comparison is fair.
> Mark any variant that does not significantly beat the baseline as `partial`
> in the evidence matrix.

This triggers scikit-learn: multi-algorithm comparison on tabular features with
a fixed, leakage-safe pipeline and shared CV protocol. The skill pulls the
algorithm selection guide from `references/supervised_learning.md`, reuses the
identical `ColumnTransformer` for all three so only the estimator varies, runs
the same stratified CV, applies a multiple-comparison correction noted in
`paper/experiments/statistics.md`, and emits both the LaTeX table into
`paper/assets/tables/` and a mirrored markdown table in
`paper/experiments/ablation.md`. Each variant gets its own run row in
`paper/experiments/run_ledger.md`; the evidence matrix is updated per variant.
Honest negative results (variants that fail to beat baseline) go to
`paper/experiments/dead_ends.md` rather than being dropped.

## Scenario 3: Exploratory clustering / dimensionality reduction for insights

> Before we finalize the methods section, run an exploratory PCA + KMeans
> analysis on the feature matrix from run `R-007` to see whether the data has
> natural structure we should mention in `paper/experiments/insights.md`. Pick
> k via silhouette, project to 2D, and hand the projection plot off to
> matplotlib for rendering into `paper/assets/figures/`.

This triggers scikit-learn for the unsupervised portion: `StandardScaler` ->
`PCA(n_components=2)` and `KMeans` with k chosen by silhouette score
(`references/unsupervised_learning.md`). The skill computes the labels and
projection, records the choice of k and silhouette score in
`paper/experiments/insights.md`, and a run row in
`paper/experiments/run_ledger.md`. It does NOT render the figure itself —
matplotlib owns the low-level rendering into `paper/assets/figures/`; this
skill only produces the arrays and the analytic justification. If the
clustering does not reveal meaningful structure, record it honestly in
`paper/experiments/dead_ends.md` instead of overstating it in the draft.
