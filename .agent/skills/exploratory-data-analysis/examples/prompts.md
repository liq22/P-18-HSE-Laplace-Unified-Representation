# exploratory-data-analysis — invocation scenarios

Realistic invocations for the single-paper workflow. Each scenario shows the inputs read
from `paper/` and the artifacts written back. EDA produces *descriptive* characterization
only — never a hypothesis test, p-value, or model fit; those are handed off to
`statistical-analysis` and `scikit-learn`. Every descriptive statistic resolves to a run
recorded in `paper/experiments/run_ledger.md`.

## Scenario 1: First pass over a freshly produced tabular results file

Context: `experiment-ops` just finished a run and recorded an artifact in
`paper/experiments/run_ledger.md`. Before the team commits to a confirmatory analysis,
they need an honest characterization of what is actually in the file — structure,
missingness, distributions, outliers, suspected batch artifacts — and concrete
preprocessing recommendations.

Prompt:
> `paper/experiments/run_ledger.md` row `RUN-014` points at
> `data/runs/exp01_conditionA_results.csv` (artifact hash recorded). Run a comprehensive
> exploratory data analysis on it: detect the format from `references/general_scientific_formats.md`,
> load with pandas, profile dimensions / dtypes / missingness / duplicates / range-validity,
> compute descriptive statistics and the correlation structure for the numeric columns,
> and flag any suspected outliers or batch artifacts (e.g. a systematic offset by run date).
> Use `scripts/eda_analyzer.py` for the common path and fall back to custom pandas code
> where the script does not yet cover a column. Render the report from
> `assets/report_template.md` and save it as
> `paper/experiments/exp01_conditionA_results_eda_report.md`. Record the pinned library
> versions and the exact analyzer command in `paper/experiments/reproducibility.md`,
> log the sampling/reader choice in `paper/logs/decision_log.md`, push any data-quality
> blocker (e.g. >30% missingness in the response variable, suspected corruption) to
> `paper/logs/open_questions.md`, and list the preprocessing steps you would recommend
> to `statistical-analysis` / `scikit-learn` next. Do not run any hypothesis test or fit
> a model; do not fabricate or hand-edit any value.

Inputs: `paper/experiments/run_ledger.md` (RUN-014),
`paper/experiments/reproducibility.md`, `references/general_scientific_formats.md`,
`assets/report_template.md`, `scripts/eda_analyzer.py`.

Outputs: `paper/experiments/exp01_conditionA_results_eda_report.md`,
`paper/experiments/run_ledger.md` (provenance confirmed), an entry in
`paper/experiments/reproducibility.md`, a `paper/logs/decision_log.md` row, optional
open questions in `paper/logs/open_questions.md`, optional exploratory QC figures in
`paper/assets/figures/`.

## Scenario 2: Characterize an unfamiliar genomics file before deciding what to do with it

Context: a collaborator shared `data/runs/rnaseq_counts.mtx` plus sidecar barcodes/feature
files. Nobody on the team is sure the file is intact or what its dimensions and sparsity
actually are. They need a format-aware profile before deciding whether it is usable for
the expression claim a reviewer questioned.

Prompt:
> The reviewer question in `paper/reviews/ai_review.md` (point R3) asks whether the
> expression dataset can support the differential claim. Run EDA on
> `data/runs/rnaseq_counts.mtx`: resolve the format and reader from
> `references/bioinformatics_genomics_formats.md` (Matrix Market; read with
> `scipy.io.mmread` then load into a sparse / AnnData structure), profile shape, data
> type, sparsity, value range, per-barcode and per-feature non-zero counts, and check
> consistency against the sidecar barcode/feature files. Flag any integrity problem
> (dimension mismatch, all-zero features, duplicate barcodes) explicitly. Render the
> report from `assets/report_template.md`, save it as
> `paper/experiments/rnaseq_counts_eda_report.md`, record provenance in
> `paper/experiments/run_ledger.md` and pinned versions in
> `paper/experiments/reproducibility.md`. If the dataset is too sparse or shows a batch
> artifact to support the R3 claim, record that as an `inconclusive` status on the
> matching row of `paper/experiments/evidence_matrix.md` with a pointer to the EDA
> report, and push the unresolved concern to `paper/logs/open_questions.md`. Do not run
> the differential test here — that is `statistical-analysis`.

Inputs: `paper/reviews/ai_review.md` (R3),
`paper/experiments/evidence_matrix.md`, `paper/experiments/run_ledger.md`,
`references/bioinformatics_genomics_formats.md`, `assets/report_template.md`.

Outputs: `paper/experiments/rnaseq_counts_eda_report.md`, provenance row in
`paper/experiments/run_ledger.md`, reproducibility entry, an updated
`paper/experiments/evidence_matrix.md` status if the dataset is unusable, and open
questions in `paper/logs/open_questions.md`.
