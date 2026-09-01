---
name: polars
description: 'Polars DataFrame ETL/analytics for the paper workflow: expression transforms, lazy query optimization, joins, aggregations, and pandas migration feeding paper/experiments/ evidence. Implementation skill; prefer exploratory-data-analysis or statistical-analysis as primary. Do not use for plotting, classical or deep ML, or Bayesian inference.'
---

# polars

## Purpose

Provide high-performance, Apache-Arrow-based DataFrame guidance with Polars
for the data-manipulation steps of the single-paper workflow: expression-based
selection/filter/with_columns, lazy query optimization (predicate and
projection pushdown, parallel execution, streaming), joins and concatenation,
group-by aggregations and window functions (`over()`), reshaping
(pivot/unpivot), multi-format I/O (CSV, Parquet, JSON, Excel, databases,
cloud), and pandas migration. In Auto-01-tiny-research this skill is a TIER B
implementation-only supporting skill: it owns the data-wrangling mechanics
that prepare the feature tables and evidence matrices backing the paper's
claims. It is invoked by a primary planning skill (`exploratory-data-analysis`,
`statistical-analysis`, `scikit-learn`) and maps every persisted result onto
`paper/experiments/` so downstream skills (`08-markdown-draft`,
`09-tex-freeze-formalize`, `13-reviewer-response`) can cite it.

## Use When

- An analysis skill (`exploratory-data-analysis`, `statistical-analysis`) needs
  tabular data loaded, cleaned, joined, or reshaped before evaluation, and the
  data is logged in `paper/experiments/run_ledger.md` (CSV/Parquet/JSON).
- A reviewer request in `paper/reviews/response_to_reviewers.md` requires a
  re-derived feature table, a join across experiment outputs, or an aggregate
  that a baseline pandas pipeline cannot produce within memory/time budget.
- The dataset is large enough that lazy evaluation (`scan_csv` / `scan_parquet`
  + `collect`) or streaming (`collect(engine="streaming")`) is required to fit
  the run within the recorded compute envelope in
  `paper/experiments/reproducibility.md`.
- A model-comparison or ablation table in `paper/assets/tables/` must be built
  by pivoting/grouping the per-run rows of `paper/experiments/run_ledger.md`.
- Migrating a legacy pandas ETL notebook to Polars for reproducibility and
  speed, recording the migration decision in `paper/logs/decision_log.md`.

Do not use this skill for plotting or visualization (defer to
`scientific-visualization` / `matplotlib`), classical ML training (defer to
`scikit-learn`), deep-learning training engineering (defer to
`pytorch-lightning`), or Bayesian modeling (defer to `pymc`). It is also not a
primary analysis planner: when the question is "which analysis fits this
claim", invoke `statistical-analysis` / `exploratory-data-analysis` first and
use polars only for the underlying data manipulation.

## Required Inputs

- A data source path or DataFrame already referenced by
  `paper/experiments/run_ledger.md`. Do not invent or fabricate data; if the
  source is unlogged, stop (see Stop With).
- The claim ID(s) from `paper/experiments/evidence_matrix.md` that the prepared
  table must support, so each derived column can be tied back to a claim.
- The target output path for any persisted artifact under
  `paper/experiments/` or `paper/assets/tables/`.
- Polars >= 1.41 (Python 3.10+); install with `uv pip install "polars==1.41.x"`,
  optional extras (`[excel,database,fsspec,pandas,numpy]`) only when a
  specific I/O backend is needed. The user is responsible for installing these;
  this skill does not pin or ship a runtime.
- No API keys or credentials are required for local files. If a remote source
  (cloud bucket, database, private dataset token) needs a credential, the user
  must provide it; never hardcode or store it in the repo. Treat any such
  secret as `<user-provided-key>`.

## Workflow

1. Read the target claim and the data ref from
   `paper/experiments/evidence_matrix.md` and
   `paper/experiments/run_ledger.md`. Do not fabricate a source.
2. Prefer the lazy API for anything beyond a small peek: `scan_csv` /
   `scan_parquet` build a query plan that is optimized before execution
   (`references/core_concepts.md`). Use eager `read_*` only for tiny inputs or
   quick inspection.
3. Project early and filter early so the optimizer can apply projection and
   predicate pushdown: `lf.select(needed_cols).filter(predicate).collect()`
   rather than filtering on all columns first (`references/best_practices.md`).
4. Stay within the expression API for parallelism — `pl.col`, `when/then/
   otherwise`, `over()`, `.str.*` / `.dt.*` namespaces. Reach for
   `.map_elements()` only when no native expression exists, and note the
   performance cost in `paper/logs/decision_log.md`.
5. For joins, aggregations, pivots/unpivots, follow
   `references/transformations.md` and `references/operations.md`; verify key
   dtypes match before joining to avoid silent empty results.
6. For pandas-migration tasks, use the mapping table in
   `references/pandas_migration.md` (no index, strict typing, parallel
   `with_columns`) and record the migration in
   `paper/logs/change_log.md`.
7. Persist results as Parquet (recommended) or CSV under
   `paper/experiments/` or `paper/assets/tables/` via the I/O patterns in
   `references/io_guide.md`; never write outputs into `paper/tex/`,
   `paper/refs/`, or `paper/submission/`.
8. Append a run row to `paper/experiments/run_ledger.md` (source ref, transform
   summary, output path, polars version, row/column counts) and update the
   claim status in `paper/experiments/evidence_matrix.md` if the table now
   enables a previously `missing_evidence` claim.
9. Record any non-trivial transform or schema decision in
   `paper/logs/decision_log.md`; record dead-end approaches in
   `paper/experiments/dead_ends.md` instead of silently dropping them.

## Output Contract

- A prepared feature/evidence table under `paper/experiments/` or
  `paper/assets/tables/` (Parquet preferred; CSV acceptable), referenced by
  path from `paper/experiments/run_ledger.md`.
- A run row in `paper/experiments/run_ledger.md` with: source data ref, the
  Polars transform applied, output path, polars version, and the claim ID(s)
  it supports.
- An updated status in `paper/experiments/evidence_matrix.md` for any claim
  the prepared table now enables (`supported` / `partial` / `unsupported`).
- A reproducibility note in `paper/experiments/reproducibility.md` covering the
  polars version, Python version, and the exact source data ref (and any
  credential nature, never the value).
- Optional decision/change/dead-end entries in `paper/logs/decision_log.md`,
  `paper/logs/change_log.md`, and `paper/experiments/dead_ends.md`.
- No executable ETL scripts shipped into the repo as the source of truth; code
  stays as documented recipes in `references/`. Snippets in the run ledger are
  illustrative, not the runtime.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only polars`
- `python src/S03_Scripts/validate_project.py`
- Confirm every output table referenced by
  `paper/experiments/evidence_matrix.md` has a matching row in
  `paper/experiments/run_ledger.md` (no orphan evidence).
- Confirm no `.read_csv` is used on a large dataset where `scan_csv` was
  mandated by `paper/experiments/reproducibility.md` (grep the cited recipe).
- Confirm polars version and Python version are recorded in
  `paper/experiments/reproducibility.md`.
- Confirm no secret literal (cloud key, DB password, token) appears in any
  persisted snippet; any credential must be `<user-provided-key>`.

## Boundaries

- Do not plot, visualize, train ML models, run Bayesian inference, or engineer
  deep-learning training here; defer to `scientific-visualization` /
  `matplotlib`, `scikit-learn`, `pymc`, and `pytorch-lightning` respectively.
- Do not fabricate data, schema, or row counts; if a source is missing or
  unlogged, mark the claim `missing_evidence` and stop.
- Do not write outputs anywhere except `paper/experiments/`,
  `paper/assets/tables/`, and the designated logs; never into `paper/tex/`,
  `paper/refs/`, `paper/submission/`, or `paper/checklists/`.
- Do not persist raw credentials, connection strings with passwords, or cloud
  keys into the repo; redact as `<user-provided-key>`.
- Do not ship upstream executable scripts as runtime; this skill ships
  `references/` documentation only.
- Do not silently swap a lazy pipeline for an eager one on large data to "make
  it work" — that changes the compute envelope recorded in
  `paper/experiments/reproducibility.md`; record the decision first.

## Stop With

- The data source needed to build a claim's table is not present in
  `paper/experiments/run_ledger.md` and the user has not supplied it.
- The required metric/protocol for the downstream analysis is unspecified by
  `paper/refs/target_journal.md` / `paper/experiments/statistics.md` and the
  user has not disambiguated — polars cannot decide the analytic design.
- A remote source requires a credential the user has not provided; do not
  hardcode or guess it.
- A join would silently produce an empty or duplicated result due to dtype or
  key mismatch that cannot be resolved without the user's domain knowledge —
  report and pause rather than emit a misleading table.
- Polars or a required extra (e.g. database connector) is unavailable and the
  user cannot install it; do not silently fall back to pandas and pretend the
  same compute envelope holds.

## References

- Core concepts (expressions, lazy vs eager, type system):
  `.agent/skills/polars/references/core_concepts.md`
- Operations (select, filter, with_columns, group_by, window functions):
  `.agent/skills/polars/references/operations.md`
- Transformations (joins, concat, pivot/unpivot):
  `.agent/skills/polars/references/transformations.md`
- Data I/O (CSV, Parquet, JSON, Excel, databases, cloud):
  `.agent/skills/polars/references/io_guide.md`
- Pandas migration guide: `.agent/skills/polars/references/pandas_migration.md`
- Best practices (lazy, streaming, projection/predicate pushdown, typing):
  `.agent/skills/polars/references/best_practices.md`
- Invocation scenarios: `.agent/skills/polars/examples/prompts.md`
- Workspace artifacts: `paper/experiments/evidence_matrix.md`,
  `paper/experiments/run_ledger.md`, `paper/experiments/statistics.md`,
  `paper/experiments/reproducibility.md`, `paper/experiments/dead_ends.md`,
  `paper/assets/tables/`, `paper/refs/target_journal.md`,
  `paper/logs/decision_log.md`, `paper/logs/change_log.md`
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://docs.pola.rs/ ,
  https://github.com/pola-rs/polars/blob/main/LICENSE
