---
name: scikit-learn
description: 'Classical ML with scikit-learn for the single-paper workflow: tabular classification/regression, clustering, preprocessing, cross-validated evaluation, and hyperparameter tuning feeding paper/experiments/ evidence. Do not use for deep learning (pytorch-lightning), Bayesian inference (pymc), or as a training execution engine.'
---

# scikit-learn

## Purpose

Provide classical, interpretable machine-learning guidance and reference
material with scikit-learn: supervised learning (classification, regression),
unsupervised learning (clustering, dimensionality reduction), preprocessing,
pipelines, cross-validated model evaluation, and hyperparameter tuning. In
Auto-01-tiny-research this skill is a TIER A core capability skill: it owns the
analytic recipes that produce the evidence backing the paper's claims, and maps
every result onto the `paper/experiments/` ledger so downstream skills
(`08-markdown-draft`, `09-tex-freeze-formalize`, `13-reviewer-response`) can
cite it.

## Use When

- A claim in `paper/experiments/evidence_matrix.md` requires a classification
  or regression result (e.g. baseline accuracy, AUC, R^2) on tabular or
  bag-of-features data.
- You need clustering or dimensionality reduction for exploratory analysis
  (PCA/t-SNE/UMAP projection, K-Means segmentation) reported in
  `paper/experiments/insights.md` or `paper/experiments/ablation.md`.
- Preprocessing choices (scaling, encoding, imputation) must be made
  reproducible and leakage-safe inside a `Pipeline`/`ColumnTransformer`.
- A reviewer requests cross-validated metrics, confidence intervals, or a
  hyperparameter sweep (`paper/reviews/response_to_reviewers.md`).
- A model-comparison table or an ablation table is needed for
  `paper/assets/tables/` and the formal `paper/tex/` draft.

Do not use this skill for deep neural networks (defer to pytorch /
pytorch-lightning), Bayesian model inference (pymc), large language-model
fine-tuning, GPU-distributed training, or non-Python ML stacks. It is also not
an execution harness: in this repo it documents and recipes analyses; it does
not run production training jobs.

## Required Inputs

- A feature matrix / dataframe or a path to data already logged in
  `paper/experiments/run_ledger.md`. Do not invent or fabricate data.
- The claim ID(s) this analysis must support, from
  `paper/experiments/evidence_matrix.md`, so each metric can be tied back.
- The metric(s) and CV protocol mandated by `paper/refs/target_journal.md` and
  `paper/experiments/statistics.md` (e.g. stratified 5-fold, reported CI).
- A target output path for any persisted result under `paper/experiments/` or
  `paper/assets/tables/`.
- scikit-learn >= 1.7 with NumPy/SciPy; optional pandas/matplotlib/seaborn for
  tables and plots. The user is responsible for installing these; this skill
  does not pin or ship a runtime.
- No API keys or credentials are required. If any external data source or
  model hub needs a credential (e.g. a private dataset token), the user must
  provide it; never hardcode or store it.

## Workflow

1. Read the target claim and its required metric from
   `paper/experiments/evidence_matrix.md` and `paper/refs/target_journal.md`.
   Do not pick a metric that the journal or the claim does not sanction.
2. Load only data referenced by `paper/experiments/run_ledger.md`; if the data
   is absent or unlogged, stop (see Stop With) rather than substituting.
3. Split with leakage control: `train_test_split(..., stratify=y,
   random_state=...)` for classification, `TimeSeriesSplit`/`GroupKFold` when
   the design demands it (temporal or grouped samples). Fix and record the
   `random_state` for reproducibility.
4. Build a `Pipeline` (and `ColumnTransformer` for mixed numeric/categorical
   features). Always fit scalers/encoders/imputers inside the pipeline on the
   training fold only — never `fit` on the full dataset before CV.
5. Choose algorithms from `references/supervised_learning.md` or
   `references/unsupervised_learning.md` using the selection guides there; do
   not invent science or fabricate benchmark numbers.
6. Tune with `GridSearchCV` / `RandomizedSearchCV` over a principled grid
   (document each candidate in `paper/experiments/ablation.md`).
7. Evaluate with the journal-mandated metrics
   (`references/model_evaluation.md`); for imbalanced classification prefer
   balanced accuracy / F1 / ROC AUC, not raw accuracy.
8. Persist: write a model-comparison or ablation table to
   `paper/assets/tables/`, append a run row to
   `paper/experiments/run_ledger.md` (algorithm, CV protocol, metric, CI,
   random_state, data ref, claim ID), and update
   `paper/experiments/evidence_matrix.md` status (`supported` /
   `partial` / `refuted`).
9. Surface any non-trivial finding or methodological decision in
   `paper/logs/decision_log.md`; record negative results honestly in
   `paper/experiments/dead_ends.md` instead of suppressing them.

## Output Contract

- A run row in `paper/experiments/run_ledger.md` with: algorithm, split/CV
  protocol, hyperparameter config, point metric + CI, `random_state`, and the
  data/claim IDs it supports.
- Updated status in `paper/experiments/evidence_matrix.md` for every claim the
  run addresses (`supported` / `partial` / `refuted` / `unsupported`).
- An ablation/model-comparison table under `paper/assets/tables/` when more
  than one variant was compared; mirror it into
  `paper/experiments/ablation.md`.
- A statistical note in `paper/experiments/statistics.md` when CIs, tests, or
  multiple-comparison corrections were computed.
- A reproducibility note in `paper/experiments/reproducibility.md` covering
  scikit-learn/NumPy/SciPy versions, seed, and exact data ref.
- Optional decision/dead-end entries in `paper/logs/decision_log.md` and
  `paper/experiments/dead_ends.md`.
- No executable training scripts shipped into the repo (this is a paper repo,
  not an ML runtime); code stays as documented recipes in the references.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only scikit-learn`
- `python src/S03_Scripts/validate_project.py`
- Confirm every run referenced by `paper/experiments/evidence_matrix.md` has a
  matching row in `paper/experiments/run_ledger.md` (no orphan claims).
- Confirm no metric is reported for a claim the matrix marks `unsupported`,
  `missing_evidence`, or `refuted`.
- Confirm scalers/encoders/imputers are inside a `Pipeline` (grep the cited
  recipe for `fit_transform` called on the full dataset — must be absent).
- Confirm `random_state` and scikit-learn version are recorded in
  `paper/experiments/reproducibility.md`.

## Boundaries

- Do not run deep-learning, LLM, or GPU training here; defer to pytorch /
  pytorch-lightning skills. Classical ML only.
- Do not fabricate metrics, datasets, or benchmark numbers; if a result is
  missing, mark the claim `missing_evidence` and stop.
- Do not `fit` preprocessing on the full dataset or test fold — data leakage
  invalidates the evidence.
- Do not persist raw trained models / `.pkl` / `.joblib` artifacts into the
  paper repo (no model binary blobs); record recipes and metrics, not weights.
- Do not write outputs anywhere except `paper/experiments/`,
  `paper/assets/tables/`, and the designated logs; never into `paper/tex/`,
  `paper/refs/`, or `paper/submission/`.
- Do not copy the upstream `scripts/` executable training/inference code into
  this repo; this skill ships `references/` documentation only.

## Stop With

- The data needed to compute a claim is not present in
  `paper/experiments/run_ledger.md` and the user has not supplied it.
- The required metric or CV protocol is unspecified by
  `paper/refs/target_journal.md` / `paper/experiments/statistics.md` and the
  user has not disambiguated.
- A leakage risk is unavoidable given the data shape (e.g. group leakage with
  no grouping variable) — report and pause rather than report a biased number.
- scikit-learn or a required dependency is unavailable and the user cannot
  install it; do not silently fall back to a different library.
- The result would contradict the claim's required direction and the user has
  not authorized reporting a `refuted` finding — surface it in
  `paper/logs/decision_log.md` and wait.

## References

- Quick reference & imports: `.agent/skills/scikit-learn/references/quick_reference.md`
- Supervised learning algorithms: `.agent/skills/scikit-learn/references/supervised_learning.md`
- Unsupervised learning: `.agent/skills/scikit-learn/references/unsupervised_learning.md`
- Preprocessing: `.agent/skills/scikit-learn/references/preprocessing.md`
- Pipelines and composition: `.agent/skills/scikit-learn/references/pipelines_and_composition.md`
- Model evaluation & tuning: `.agent/skills/scikit-learn/references/model_evaluation.md`
- Invocation scenarios: `.agent/skills/scikit-learn/examples/prompts.md`
- Workspace artifacts: `paper/experiments/evidence_matrix.md`,
  `paper/experiments/run_ledger.md`, `paper/experiments/statistics.md`,
  `paper/experiments/ablation.md`, `paper/experiments/reproducibility.md`,
  `paper/experiments/dead_ends.md`, `paper/experiments/insights.md`,
  `paper/assets/tables/`, `paper/refs/target_journal.md`,
  `paper/logs/decision_log.md`
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://scikit-learn.org/stable/ ,
  https://scikit-learn.org/stable/user_guide.html
