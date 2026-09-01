---
name: exploratory-data-analysis
description: 'Format-aware first-pass EDA on a scientific data file a paper/experiments/ run produced: detect format, profile structure, quality, and distributions, and write a markdown report with preprocessing recommendations. Use when a dataset needs profiling before confirmatory analysis. Do not use for hypothesis testing, modeling, rendering, or prose.'
---

# Exploratory Data Analysis

## Purpose

Provide a systematic, format-aware exploratory data analysis (EDA) capability for the
single-paper research workflow: given a scientific data file (one that
`paper/experiments/run_ledger.md` records as a run artifact, or the user supplies
explicitly), detect its type, read it with the correct library, profile its structure,
dimensions, missingness, distributions, outliers, and metadata, and emit a comprehensive
markdown report plus concrete preprocessing recommendations that bind directly back to
`paper/experiments/`. This is the **TIER A core** EDA skill — the first quantitative
pass over a dataset, before any confirmatory testing or modeling.

The skill is responsible for *characterizing* the data honestly: it surfaces quality
issues (missing values, format non-compliance, outliers, suspected corruption, batch
artifacts), records what the file actually contains versus what was expected, and
recommends downstream steps. It does not test hypotheses, fit models, or assert
scientific conclusions — it produces an accurate, reproducible characterization that
`statistical-analysis`, `scikit-learn`, and `scientific-writing` can trust.

## Use When

- A run recorded in `paper/experiments/run_ledger.md` produced a new data file and you
  need to understand its structure, content, and quality before analysis.
- The user provides a path to a scientific data file and asks to "explore", "profile",
  "summarize", or "characterize" it.
- You need format-specific metadata, typical-data description, and the right Python
  reader for an unfamiliar extension (200+ formats covered across the references).
- You must assess data quality / completeness / format compliance before committing to a
  downstream test or model.
- You need to recommend preprocessing (normalization, imputation, outlier handling,
  format conversion) grounded in the actual data characteristics.
- An `paper/logs/open_questions.md` entry asks "is this dataset even usable / what is
  in it?" and an EDA report is the honest answer.

## Required Inputs

- A scientific data file path. Ideally the file is an artifact referenced in
  `paper/experiments/run_ledger.md` (with provenance: commit / source / instrument); if
  the user supplies a path ad hoc, record its provenance into the ledger before/after
  analysis. Never fabricate or hand-edit data to look cleaner.
- The research context if known: the research question / hypothesis from
  `paper/refs/reading_matrix.md` or a claim row in
  `paper/experiments/evidence_matrix.md` this dataset will eventually support. This lets
  the report recommend analyses that actually answer the question.
- The reporting target from `paper/refs/target_journal.md` (so EDA artifacts use the
  field's expected vocabulary and figure conventions).
- The relevant format reference under `references/` (auto-selected by extension):
  `chemistry_molecular_formats.md`, `bioinformatics_genomics_formats.md`,
  `microscopy_imaging_formats.md`, `spectroscopy_analytical_formats.md`,
  `proteomics_metabolomics_formats.md`, `general_scientific_formats.md`.

**Environment / libraries.** Core: `numpy`, `pandas`, `scipy`. Format-specific readers
loaded on demand per the reference entry (e.g. `biopython`/`pysam` for genomics,
`rdkit`/`mdanalysis` for chemistry, `tifffile`/`nd2reader`/`aicsimageio` for
microscopy, `nmrglue`/`pymzml`/`pyteomics` for spectroscopy). Install via
`uv pip install ...` when a reader is missing and surface the requirement clearly.

**Credentials.** No API keys are required for EDA itself — all analysis is local. If an
optional external helper (e.g. an LLM narrative helper reachable via OpenRouter) is ever
used, the user must provide the key out of band; never hardcode, store, or echo a key,
token, or credential in this skill, its scripts, or any workspace file. Treat any
encountered secret string as `<user-provided-key>`.

## Workflow

1. **Detect the file type.** Extract the extension and look it up in the matching
   `references/<category>_formats.md` (search for the `### .<ext>` heading). Identify
   the category, format description, typical data, and the canonical Python reader.
   `scripts/eda_analyzer.py` can do extension-to-category detection for the common
   formats; otherwise resolve manually from the reference.
2. **Load format-specific guidance.** From the reference entry pull: typical data
   content, common use cases, the recommended Python library (with code snippet), and
   the format-specific EDA approach. Do not load entire reference files into context —
   grep for the extension section and cache it when analyzing multiple files of the
   same type.
3. **Read the data.** Load with the recommended reader (pandas for tabular, `np.load`
   for arrays, Biopython/pysam for sequences, tifffile/nd2reader for imaging, etc.).
   For very large files, sample (first N records), memory-map (HDF5, NPY), or stream in
   chunks (CSV, FASTQ); state the sampling strategy in the report.
4. **Profile structure.** Dimensions / shape, dtypes, coordinate axes (XYZCT for
   imaging; sequence/count matrices for omics), hierarchical groups (HDF5/Zarr), and
   metadata (instrument, software versions, spatial/temporal calibration, sample info).
5. **Assess quality.** Missingness (counts + pattern), range/validity checks, format
   compliance, duplicate detection, suspected corruption, and consistency between stated
   metadata and actual data. Flag anomalies explicitly — do not silently drop or
   "correct" anything.
6. **Compute statistical summaries.** Numerical variables: descriptive stats, value
   distribution, skew/kurtosis, NaN/inf counts, sparsity, correlation structure.
   Categorical variables: counts, cardinality, imbalances. Image/sequence/omics: the
   domain-specific summaries listed in the reference EDA-approach block.
7. **Surface key findings.** Notable patterns, suspected batch effects, outliers,
   under/over-represented strata, and any quality red flag that would bias a downstream
   confirmatory test or model.
8. **Recommend downstream steps.** Concrete, file-type-aware preprocessing
   (normalization, imputation, batch correction, format conversion), the appropriate
   next analyses, and the tools/methods to run them — pointing forward to
   `statistical-analysis` (testing), `scikit-learn` (modeling), and
   `scientific-visualization` (rendering), not doing those jobs here.
9. **Write the report + ledger entries.** Render the report from
   `assets/report_template.md`, save it under `paper/experiments/` (pattern
   `{stem}_eda_report.md`), record provenance and the pinned environment in
   `paper/experiments/reproducibility.md` and `paper/experiments/run_ledger.md`, log the
   decision in `paper/logs/decision_log.md`, and push unresolved quality concerns to
   `paper/logs/open_questions.md`.

## Output Contract

- `paper/experiments/{stem}_eda_report.md` — comprehensive markdown EDA report built
  from `assets/report_template.md`: basic info, format details, structure, quality
  assessment, statistical summary, key findings, and recommendations.
- `paper/experiments/run_ledger.md` — a row pinning the analyzed file's provenance
  (source / commit / artifact hash / instrument).
- `paper/experiments/reproducibility.md` — pinned library versions and the exact command
  to reproduce the EDA (e.g. the `scripts/eda_analyzer.py` invocation or the custom
  notebook path).
- `paper/experiments/statistics.md` — descriptive-statistics blocks produced by EDA
  (means, SDs, distributions), tagged as exploratory and keyed to the dataset — never a
  hypothesis-test result.
- `paper/experiments/evidence_matrix.md` — optional: if the EDA reveals a data-quality
  blocker for a claim row, record it as an open/inconclusive status with a pointer to
  the EDA report rather than hiding the problem.
- `paper/assets/figures/` — exploratory figures (distribution / correlation / QC plots)
  the EDA generated, named to match the dataset; rendering hand-off to
  `scientific-visualization` for formal figures.
- `paper/logs/decision_log.md` — the sampling strategy, reader/library chosen, and any
  quality red flag plus the remediation chosen.
- `paper/logs/open_questions.md` — unresolved quality concerns (e.g. suspected
  corruption, metadata mismatch, ambiguous format) that block confirmatory analysis.
- `paper/logs/insights.md` — exploratory patterns worth a hypothesis (stated as
  predictions to be tested, never as results); hand off hypothesis generation to
  `hypothesis-generation`.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only exploratory-data-analysis`
- `python src/S03_Scripts/validate_project.py`
- Every descriptive statistic in the EDA report resolves to the recorded data file in
  `paper/experiments/run_ledger.md`; no number is fabricated or hand-edited.
- The reader/library chosen matches the format entry in the matching
  `references/<category>_formats.md`; the pinned versions in
  `paper/experiments/reproducibility.md` reproduce the report from a clean environment.
- Quality issues (missingness, outliers, format non-compliance, suspected corruption)
  are surfaced explicitly and pushed to `paper/logs/open_questions.md` rather than
  silently dropped or "corrected".
- Any sampling strategy used for large files is stated and reproducible; estimates are
  labeled as sample-based.
- No hypothesis test, p-value, model fit, or rendered formal figure is produced by this
  skill (those belong to `statistical-analysis`, `scikit-learn`, `scientific-visualization`).
- No API key, token, or credential appears anywhere in the report, script output, or
  workspace file; any external helper key is `<user-provided-key>`.

## Boundaries

- Do not fabricate, impute-then-hide, or hand-edit data to improve the apparent quality;
  record issues honestly in `paper/logs/open_questions.md`.
- Do not run hypothesis tests, compute p-values, fit predictive models, or produce
  confirmatory statistics — hand off to `statistical-analysis` and `scikit-learn`. EDA
  produces *descriptive* summaries only.
- Do not render formal publication figures or write manuscript prose — hand off to
  `scientific-visualization` (rendering) and `scientific-writing` (prose). Exploratory
  QC plots are in scope; figures destined for the manuscript are not.
- Do not run the experiment or manage compute — that is `experiment-ops`; this skill
  only profiles files the ledger already records (or the user explicitly supplies).
- Do not silently change the analysis target or reader after seeing anomalies; record
  the change and reason in `paper/logs/decision_log.md`.
- Do not hardcode, store, or echo any API key, token, or credential; any external helper
  key is user-provided out of band and treated as `<user-provided-key>`.
- Do not overwrite a frozen `paper/tex/` artifact without a change record in
  `paper/logs/change_log.md`.
- A clean EDA is necessary but not sufficient: it characterizes the data; it does not by
  itself establish a claim (a confirmatory test, effect size, and design do).

## Stop With

- The data file is not in `paper/experiments/run_ledger.md` and the user has not
  supplied it — do not profile a guessed or fabricated dataset.
- The extension is not in any reference file and the format cannot be confirmed with the
  user — stop, log the gap in `paper/logs/open_questions.md`, and ask.
- The file is corrupted, password-protected, or fails the integrity check in a way that
  no reader can recover; record the red flag rather than reporting partial numbers as if
  trustworthy.
- A required reader library cannot be installed in the environment and no robust
  fallback exists — surface the requirement and stop.
- Quality issues are severe enough that no confirmatory analysis is interpretable
  (e.g. >X% missingness in a critical variable, suspected systemic batch artifact);
  record this and hand the decision back to the user / to `hypothesis-generation`.
- The file size or memory footprint exceeds what the environment can handle even with
  sampling / chunking / memory-mapping; record the constraint and propose an alternative
  (sub-sampling plan, cluster run) rather than crashing silently.
- The reporting standard in `paper/refs/target_journal.md` is missing and the user
  cannot clarify what level of detail the EDA report needs.

## References

- Format references (auto-selected by extension):
  - `.agent/skills/exploratory-data-analysis/references/chemistry_molecular_formats.md`
    (60+ chemistry / molecular formats)
  - `.agent/skills/exploratory-data-analysis/references/bioinformatics_genomics_formats.md`
    (50+ bioinformatics formats)
  - `.agent/skills/exploratory-data-analysis/references/microscopy_imaging_formats.md`
    (45+ imaging formats)
  - `.agent/skills/exploratory-data-analysis/references/spectroscopy_analytical_formats.md`
    (35+ spectroscopy formats)
  - `.agent/skills/exploratory-data-analysis/references/proteomics_metabolomics_formats.md`
    (30+ omics formats)
  - `.agent/skills/exploratory-data-analysis/references/general_scientific_formats.md`
    (30+ general formats)
- EDA report template: `.agent/skills/exploratory-data-analysis/assets/report_template.md`.
- Analyzer helper: `.agent/skills/exploratory-data-analysis/scripts/eda_analyzer.py`
  (see `scripts/README.md` for purpose / inputs / outputs / network / writes).
- Workspace artifacts: `paper/experiments/` (`{stem}_eda_report.md`, `run_ledger.md`,
  `reproducibility.md`, `statistics.md`, `evidence_matrix.md`),
  `paper/assets/figures/`, `paper/refs/target_journal.md`,
  `paper/refs/reading_matrix.md`, `paper/logs/decision_log.md`,
  `paper/logs/open_questions.md`, `paper/logs/insights.md`,
  `paper/logs/change_log.md`.
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0 (MIT);
  see NOTICE.md and `.agent/references/scientific_agent_skills_source.md`.
- Upstream texts: McKinney (2017) *Python for Data Analysis*; Tukey (1977)
  *Exploratory Data Analysis*; Wickham & Grolemund (2017) *R for Data Science*.
