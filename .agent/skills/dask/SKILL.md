---
name: dask
description: 'Implementation skill scaling pandas/NumPy beyond RAM with Dask. Use when a logged paper/experiments/ dataset is too large for memory and an out-of-core aggregation or multi-file ETL backs a claim. Do not use for ML modeling, figures, or training; prefer the planning skill (scikit-learn, scientific-visualization, pytorch-lightning, pymc) as primary.'
---

# dask

## Purpose

Provide parallel and out-of-core data-processing guidance with Dask so that
the single paper can compute statistics, aggregations, and ETL over datasets
that exceed available RAM. In Auto-01-tiny-research this is a **TIER B tool
skill** — an implementation-only supporting skill. It exists to unblock the
analytic steps that produce evidence for `paper/experiments/`, but it does not
own the scientific planning: it executes data movement, chunking, and
scheduler choices, and hands results (metrics, tables, persisted arrays) to
the skills that own the claim, the statistics, and the figures. Use the
relevant planning/capability skill as primary and reach for Dask only when
the data volume forces it.

## Use When

- A dataset referenced in `paper/experiments/run_ledger.md` is larger than RAM
  and a required aggregation, groupby, join, or reduction must still be
  computed to support a claim in `paper/experiments/evidence_matrix.md`.
- Many files (CSV / Parquet / JSON / text logs) must be processed together as
  one logical table or bag before downstream analysis.
- A large numeric array (HDF5 / Zarr / NetCDF) must be reduced or transformed
  in chunks for a statistic reported in `paper/experiments/statistics.md`.
- A custom parallel task graph (parameter sweep, per-fold feature extraction)
  is needed and a `dask.distributed` client gives the dashboard for
  reproducibility notes in `paper/experiments/reproducibility.md`.

Do not use this skill for final figure or table rendering (defer to
scientific-visualization / matplotlib / seaborn), classical ML model fitting
(scikit-learn), deep-learning training engineering (pytorch-lightning), or
Bayesian modeling (pymc). It is also not an execution harness for production
jobs: in this repo it documents and recipes the data step only; it does not
ship runtime cluster infrastructure.

## Required Inputs

- A path to data already logged in `paper/experiments/run_ledger.md`, or a
  glob the user explicitly supplies (`data/2024-*.parquet`,
  `s3://bucket/prefix/*.csv`). Do not invent data.
- The claim ID(s) the computation must support, from
  `paper/experiments/evidence_matrix.md`, so each output can be tied back.
- The exact metric / aggregation mandated by `paper/refs/target_journal.md`
  and `paper/experiments/statistics.md` — Dask should reproduce the same
  definition, just out of core.
- A target output path under `paper/experiments/` or `paper/assets/tables/`
  for any persisted result.
- Dask >= 2025.1 with pandas 2+ and PyArrow 16+ for DataFrame I/O; optional
  `s3fs` / `gcsfs` for cloud paths; `dask[complete]` for the distributed
  scheduler and dashboard. The user is responsible for installing these; this
  skill does not pin or ship a runtime.
- No API keys or credentials are required for local files. If a cloud path
  (`s3://`, `gcs://`, `az://`) or any other external data source needs a
  credential, the user must provide it; never hardcode or store it.

## Workflow

1. Confirm the volume genuinely exceeds RAM. First try the simpler route
   (Parquet instead of CSV, a downsample, or a compiled kernel); only reach
   for Dask when those are insufficient. Record the decision in
   `paper/logs/decision_log.md`.
2. Read the required aggregation and the claim it supports from
   `paper/experiments/evidence_matrix.md` and `paper/refs/target_journal.md`.
   Do not pick a metric the claim or journal does not sanction.
3. Load only data referenced by `paper/experiments/run_ledger.md`. Let Dask
   own the loading (`dd.read_parquet`, `da.from_zarr`) — never load the whole
   dataset with pandas/NumPy and then hand it to Dask.
4. Choose the component per `references/` (dataframes / arrays / bags /
   futures / schedulers): tabular -> DataFrames, numeric -> Arrays, text/JSON
   -> Bags (then convert), custom dynamic tasks -> Futures.
5. Set chunk / partition sizes targeting ~100 MB per chunk and >=10 chunks
   per worker core; pick the scheduler (threads for NumPy/Pandas,
   processes for pure Python, distributed for the dashboard). Fix any seed.
6. Build the lazy graph, fuse operations with `map_partitions` /
   `map_blocks`, and avoid repeated `compute()` calls. Check graph size with
   `len(ddf.__dask_graph__())` before computing.
7. Compute once, persist intermediate results only if reused, and free them
   when done. Capture the distributed dashboard link if used.
8. Persist outputs to the workspace: append a run row to
   `paper/experiments/run_ledger.md` (data ref, scheduler, chunk size,
   worker count, runtime, claim ID), update
   `paper/experiments/evidence_matrix.md` status, and add a reproducibility
   note (Dask/pandas/PyArrow versions, seed, cluster shape) to
   `paper/experiments/reproducibility.md`.
9. Surface non-trivial choices (chunking trade-offs, scheduler switch) in
   `paper/logs/decision_log.md`; record honest negative results (e.g. the
   out-of-core number disagreed with the in-memory pilot) in
   `paper/experiments/dead_ends.md`.

## Output Contract

- A run row in `paper/experiments/run_ledger.md` with: data ref, Dask
  component used, scheduler, chunk/partition size, worker count, runtime, and
  the claim ID(s) the computation supports.
- Updated status in `paper/experiments/evidence_matrix.md` for every claim
  the run addresses (`supported` / `partial` / `refuted` / `unsupported`).
- A persisted result (Parquet / Zarr / CSV summary) under
  `paper/experiments/` or a table under `paper/assets/tables/` when an
  aggregation table is required; never into `paper/tex/` or `paper/refs/`.
- A reproducibility note in `paper/experiments/reproducibility.md` covering
  Dask, pandas, PyArrow, and distributed versions, the seed, the scheduler,
  and the cluster shape.
- Optional entries in `paper/logs/decision_log.md` and
  `paper/experiments/dead_ends.md`.
- No executable cluster / training scripts shipped into the repo (this is a
  paper repo, not a compute runtime); code stays as documented recipes in the
  references.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only dask`
- `python src/S03_Scripts/validate_project.py`
- Confirm every run referenced by `paper/experiments/evidence_matrix.md` has a
  matching row in `paper/experiments/run_ledger.md` (no orphan claims).
- Confirm the Dask result reproduces the same metric definition the journal
  mandates — out-of-core must not silently change the aggregation semantics.
- Confirm chunk size, scheduler, worker count, and Dask/pandas/PyArrow
  versions are recorded in `paper/experiments/reproducibility.md`.
- Confirm the recipe loads data through Dask (grep for `read_csv`/
  `read_parquet` on the full dataset followed by `from_pandas` — that
  anti-pattern must be absent).

## Boundaries

- Do not render final figures or styled tables here; defer to
  scientific-visualization / matplotlib / seaborn. Dask produces the numbers
  and arrays, not the published figure.
- Do not fit classical ML models here (defer to scikit-learn), train deep
  models (defer to pytorch-lightning), or run Bayesian inference (defer to
  pymc). If Dask-ML is used, it is only to scale a scikit-learn-style step
  that the planning skill has already sanctioned.
- Do not fabricate metrics, datasets, or benchmark numbers; if a result is
  missing, mark the claim `missing_evidence` and stop.
- Do not persist raw binary artifacts (`.parquet` dumps of intermediate
  stages, `.zarr` arrays) into the paper repo beyond what
  `paper/experiments/` explicitly requires; no model/weight blobs.
- Do not write outputs anywhere except `paper/experiments/`,
  `paper/assets/tables/`, and the designated logs; never into `paper/tex/`,
  `paper/refs/`, or `paper/submission/`.
- Do not copy upstream `scripts/` executable code into this repo; this skill
  ships `references/` documentation only.

## Stop With

- The data needed to compute a claim is not present in
  `paper/experiments/run_ledger.md` and the user has not supplied a path.
- The dataset fits comfortably in RAM — fall back to pandas/NumPy and the
  relevant planning skill; Dask adds overhead without benefit.
- The required metric or aggregation is unspecified by
  `paper/refs/target_journal.md` / `paper/experiments/statistics.md` and the
  user has not disambiguated.
- Dask or a required dependency (`dask[complete]`, PyArrow, `s3fs`) is
  unavailable and the user cannot install it; do not silently substitute
  another library and report a different number.
- The out-of-core result disagrees with an existing in-memory pilot beyond
  tolerance, and the user has not authorized updating the claim — surface it
  in `paper/logs/decision_log.md` and wait rather than overwriting evidence.

## References

- DataFrames guide: `.agent/skills/dask/references/dataframes.md`
- Arrays guide: `.agent/skills/dask/references/arrays.md`
- Bags guide: `.agent/skills/dask/references/bags.md`
- Futures & distributed guide: `.agent/skills/dask/references/futures.md`
- Schedulers guide: `.agent/skills/dask/references/schedulers.md`
- Best practices & optimization: `.agent/skills/dask/references/best-practices.md`
- Invocation scenarios: `.agent/skills/dask/examples/prompts.md`
- Workspace artifacts: `paper/experiments/evidence_matrix.md`,
  `paper/experiments/run_ledger.md`, `paper/experiments/statistics.md`,
  `paper/experiments/reproducibility.md`, `paper/experiments/dead_ends.md`,
  `paper/experiments/insights.md`, `paper/assets/tables/`,
  `paper/refs/target_journal.md`, `paper/logs/decision_log.md`
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://docs.dask.org/en/stable/
