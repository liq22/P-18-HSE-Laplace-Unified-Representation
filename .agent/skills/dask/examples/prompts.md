# dask — invocation scenarios

Realistic prompts for invoking the dask tool skill inside the
Auto-01-tiny-research workspace. Each scenario shows the kind of request that
should trigger this skill, the artifacts it reads, and the workspace outputs
it must produce. dask is a TIER B implementation skill: it owns the
out-of-core data step only and hands results to the planning/capability
skills that own the claim, the statistics, and the figures.

## Scenario 1: Out-of-core groupby aggregation for a large logged dataset

> The dataset behind run `R-014` in `paper/experiments/run_ledger.md` is
> ~120 GiB of Parquet across `data/runs/2024-*.parquet` — too big for RAM.
> Claim `C-05` in `paper/experiments/evidence_matrix.md` needs a per-cohort
> mean and 95% CI of `latency_ms`, stratified by `region`. The target
> journal (`paper/refs/target_journal.md`) wants the CI computed by bootstrap
> over the per-cohort mean. Compute the aggregation out of core and update
> the claim row.

This triggers dask: a larger-than-RAM tabular aggregation backing a specific
claim. The skill reads the data ref and the metric, uses
`dask.dataframe.read_parquet` (never `pandas.read_parquet` then
`from_pandas`), chooses chunk sizes near 128 MB, builds the lazy groupby +
`map_partitions` bootstrap graph, and computes once with the distributed
scheduler (capturing the dashboard link). It appends a run row to
`paper/experiments/run_ledger.md` (data ref, scheduler, chunk size, worker
count, runtime, claim ID), updates `C-05` in
`paper/experiments/evidence_matrix.md`, records Dask/pandas/PyArrow versions
+ seed in `paper/experiments/reproducibility.md`, and notes the bootstrap
method in `paper/experiments/statistics.md`. Do NOT render a figure here —
if a per-region bar chart is wanted, hand the aggregated numbers to
matplotlib / scientific-visualization for `paper/assets/figures/`.

## Scenario 2: Multi-file JSON ETL feeding a downstream ML claim

> We have ~50,000 JSON log files under `logs/raw/*.json` that need to be
> filtered to `status=="valid"`, projected to `{id, value, cohort}`, and
> written as a single Parquet table the scikit-learn step can consume. The
> resulting file must be logged so claim `C-07` can cite it. The full set
> won't fit in memory.

This triggers dask: an unstructured-to-structured ETL over many files that
exceeds RAM. The skill uses `dask.bag.read_text('logs/raw/*.json').map(json.loads)`,
filters, projects, converts to a DataFrame with `.to_dataframe()`, and writes
Parquet with `.to_parquet('data/derived/C-07-features.parquet')` in
partitioned form. It logs the new derived file as a run row in
`paper/experiments/run_ledger.md` with a content hash and row count, links it
to claim `C-07` in `paper/experiments/evidence_matrix.md`, and records the
ETL config (scheduler, partition count, versions) in
`paper/experiments/reproducibility.md`. Do NOT fit any model here — once the
Parquet exists, the scikit-learn skill owns the modeling step that consumes
it; this skill only guarantees the data step is reproducible and out of core.

## Scenario 3: Chunked array reduction for a large gridded statistic

> Claim `C-09` requires the global mean and standard deviation of a ~200 GiB
> Zarr array (`data/grid/field.zarr`) so we can z-score normalize it before
> the downstream analysis. Report mean and std with the journal-mandated
> precision in `paper/experiments/statistics.md`.

This triggers dask: a large numeric array reduction that must be done in
chunks. The skill uses `dask.array.from_zarr`, sets `chunks` near 100 MB per
block, builds the lazy mean/std reductions, and computes once (threads
scheduler for NumPy-backed arrays). It writes the mean/std into
`paper/experiments/statistics.md` with the claim ID, appends a run row to
`paper/experiments/run_ledger.md`, and records the chunk shape + versions in
`paper/experiments/reproducibility.md`. If the normalized array itself needs
to be persisted, it goes to `paper/experiments/` (not `paper/tex/` or
`paper/refs/`); the actual normalization step belongs to the analytic
pipeline the planning skill owns, not to this helper.
