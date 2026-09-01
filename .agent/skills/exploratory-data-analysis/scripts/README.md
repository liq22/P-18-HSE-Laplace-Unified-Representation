# scripts/ — local README

Bundled helper for the `exploratory-data-analysis` skill. Copied (adapted) from
K-Dense-AI/scientific-agent-skills v2.53.0 (MIT); see NOTICE.md and
`../../../../.agent/references/scientific_agent_skills_source.md`.

## eda_analyzer.py

- **Purpose:** automated first-pass EDA driver. Detects the file type from the
  extension, loads the matching format reference, runs a format-appropriate
  structural / quality / statistical profile, and renders a markdown report from
  `../assets/report_template.md`. Covers the common formats across all six
  reference categories (chemistry, bioinformatics, microscopy, spectroscopy,
  proteomics/metabolomics, general scientific).
- **Public API:**
  - `detect_file_type(filepath)` -> `(extension, category, format_label)`
  - `load_reference_info(category, extension)` -> reference metadata for the format
  - `analyze_file(filepath)` -> `dict` of analysis results (format-specific analysis
    dispatched internally for general / bioinformatics / imaging categories)
  - `generate_markdown_report(analysis, output_path=None)` -> markdown report string
    (written to `output_path` when given); uses `assets/report_template.md` as the
    section guide.
  - CLI: `python scripts/eda_analyzer.py <filepath> [output.md]`
- **Inputs:** a path to a scientific data file on the local filesystem. The
  file should be an artifact referenced in `paper/experiments/run_ledger.md`
  (or supplied explicitly by the user); never analyze a fabricated path.
- **Outputs:** a markdown EDA report (string, and written to `output.md` when a
  path is given). The caller decides where to persist the report and any QC
  figures (convention: `paper/experiments/{stem}_eda_report.md` and
  `paper/assets/figures/`).
- **Network:** none. Pure local computation. The script reads only the supplied
  data file and the bundled `references/*.md` / `assets/report_template.md`.
- **File writes:** only the optional `output.md` path the caller passes. It does
  not write into `paper/` directly; the caller records provenance in
  `paper/experiments/run_ledger.md` and `paper/experiments/reproducibility.md`.
- **Credentials:** none required. No API keys, tokens, or network calls. If the
  surrounding workflow ever needs an external key, the user must provide it out
  of band; never hardcode or store a key.

## Running

```bash
# basic — report printed to stdout
python scripts/eda_analyzer.py data/runs/exp01_results.csv

# write the report to a specific path
python scripts/eda_analyzer.py data/runs/exp01_results.csv \
  paper/experiments/exp01_results_eda_report.md
```

Add `scripts/` to `sys.path` (e.g. `sys.path.insert(0, "scripts")`) before
importing when running from the repo root. For formats the script does not yet
auto-handle, fall back to custom analysis driven by the matching
`references/<category>_formats.md` entry — the reference still tells you the
reader, typical data, and EDA approach.
