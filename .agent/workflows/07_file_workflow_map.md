# File and Product Map

Use this map to prevent supporting records from replacing the user's requested
product.

| Surface | Primary product | Optional support |
|---|---|---|
| Research decision | question, hypothesis, method choice | `paper.yaml`, idea notes |
| Manuscript | target Markdown/TeX section | paragraph map, verified sources |
| Code | source and relevant tests | config, `MODULE_MAP.md` when interfaces change |
| Experiment | actual outputs, metrics, plots/models | run/statistics notes |
| Figure/table | actual asset and caption | figure/table record |
| Submission | uploadable files and response letter | concise checklist/change note |
| Governance | explicitly requested policy or review finding | only necessary internal records |

A support-only change does not complete a product task unless that support file was
explicitly requested.

## Main ownership

| Path | Owner/use |
|---|---|
| `paper/kickstart/idea_candidates.yaml` | idea candidates and direction decisions |
| `paper/method/method_spec.yaml` | method mechanism and decisive comparison |
| `paper/refs/reading_matrix.md` | literature map; support for manuscript synthesis |
| `paper/experiments/evidence_matrix.md` | concise conclusion/result relationship |
| `paper/experiments/run_ledger.md` | minimum reproducibility context |
| `paper/assets/figures/*`, `paper/assets/tables/*` | actual visual/table products |
| `paper/draft/`, `paper/tex/` | active manuscript product |
| `paper/submission/` | uploadable package |
| `src/S01_Package/` | executable research implementation |
| `src/S04_Tests/` | targeted regressions for changed behavior |
| `src/MODULE_MAP.md` | explanation tasks only |
| `AGENTS.md`, `.agent/` | repository behavior tasks only |
| `external/aris` | optional pinned capability source, not a host entrypoint |

## Request rules

```text
rewrite section      -> edit the section
implement/fix code   -> edit source and closest test
run experiment       -> produce metrics and outputs
generate figure      -> produce the asset and caption
prepare submission   -> produce uploadable files
explicit review      -> report decision-changing findings
```

Supporting records update once when the product makes them stale. There is no
repository manifest, hash, receipt, or integrity package to update.

## Optional ARIS backend

PaperTrace selects the product and one allowlisted capability. Do not run ARIS
installers, expose a second skill menu, invoke disabled high-level pipelines, or
read the full submodule for one task.

## Unmapped files

Identify the nearest existing product owner. Prefer an existing route over adding
a new workflow, status file, or governance layer. Ask only when the file's role
would materially change the research or implementation decision.
