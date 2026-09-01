# polars — invocation scenarios

Realistic prompts for invoking the polars tool skill inside the
Auto-01-tiny-research workspace. Each scenario shows the kind of request that
should trigger this skill and the workspace artifacts it produces or reads.
polars is a TIER B implementation skill: prefer `exploratory-data-analysis` or
`statistical-analysis` as the primary planning skill and use polars for the
data-wrangling step underneath them.

## Scenario 1: Lazy join of per-run results into an evidence table

> The runs logged in `paper/experiments/run_ledger.md` each wrote a Parquet
> shard under `paper/experiments/runs/*.parquet`. Join them all on `run_id`,
> add a `metric_delta` column computed against the baseline run, group by
> `ablation_variant`, and write the resulting wide evidence table to
> `paper/assets/tables/evidence_matrix_derived.parquet` so the claim rows in
> `paper/experiments/evidence_matrix.md` can reference it. The full dataset
> does not fit in memory, so use lazy scanning.

This triggers polars: the task is a lazy, out-of-core join + aggregation +
pivot pipeline over Parquet shards — exactly `scan_parquet` + projection
pushdown + `join` + `group_by` + `collect(engine="streaming")`. The skill
builds the query plan following `references/transformations.md` and
`references/best_practices.md`, persists the wide table into
`paper/assets/tables/`, appends a run row to `paper/experiments/run_ledger.md`
(source refs, transform, output path, polars version), and records the lazy
vs streaming choice in `paper/experiments/reproducibility.md`. Do NOT do the
analytic design here — `statistical-analysis` decides which metric/delta is
journal-valid per `paper/refs/target_journal.md`; polars only computes the
table the analysis consumes.

## Scenario 2: Migrate a legacy pandas ETL notebook to Polars

> Our reproducibility reviewer flagged that the pandas ETL in the supplementary
> notebook is slow and reorders columns nondeterministically. Migrate it to
> Polars using the expression API, keep the schema identical, and verify the
> output `paper/experiments/features.parquet` is byte-identical (modulo row
> order) to the old one. Record the migration in `paper/logs/change_log.md`.

This triggers polars: the request is a pandas-to-Polars migration using the
expression API and the mapping table in `references/pandas_migration.md` (no
index, strict typing, parallel `with_columns`). The skill rewrites the
pipeline, pins the column order explicitly, writes the Parquet table, logs
the polars/Python versions in `paper/experiments/reproducibility.md`, and
records the schema-preserving decision in `paper/logs/change_log.md` and the
rationale in `paper/logs/decision_log.md`. Do NOT change the feature
definition or the downstream model — that would alter the evidence and must go
through `scikit-learn` / `statistical-analysis`; polars only preserves the
existing transform.

## Scenario 3: Aggregate a large CSV into an ablation summary table

> One claim in `paper/experiments/evidence_matrix.md` needs a per-fold
> aggregation over a 4 GB CSV of raw trial outputs. Compute mean and 95th
> percentile of `latency_ms` grouped by `(variant, fold)`, unpivot the metric
> columns to long form, and write `paper/assets/tables/ablation_latency.csv`
> plus a Parquet mirror. Use lazy scanning so we don't blow the memory budget
> recorded in `paper/experiments/reproducibility.md`.

This triggers polars: large-file lazy aggregation with projection pushdown
(select only `variant, fold, latency_ms`), `group_by(...).agg(...)`, then
`unpivot` to long form, then dual CSV+Parquet export per
`references/io_guide.md` and `references/operations.md`. The skill writes the
tables into `paper/assets/tables/`, appends a run row to
`paper/experiments/run_ledger.md`, and updates the claim status in
`paper/experiments/evidence_matrix.md`. The percentile/CV choice and any
significance test belong to `statistical-analysis`; polars only produces the
aggregated table the analysis consumes.
