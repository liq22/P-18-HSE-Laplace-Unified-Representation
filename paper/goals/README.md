# TII execution goals

Continue from the current `dev`/PR state, not an old overlay. This project tests one statistically anchored HSE–LLapDiff conditioner; Flow Matching remains future work.

| Goal | Scope | Current boundary |
|---|---|---|
| [01 Sync](01_SYNC_PHMFACTORY.md) | parent/dependency state and exact MFPT acceptance | real reference path passed; pointer can be recorded |
| [02 Theory and manuscript](02_THEORY_MANUSCRIPT.md) | fixed-arm theory, novelty boundary, independent Notebook | CPU witness; not learned method evidence |
| [03 Data](03_DATA.md) | PHMFactory exports and five official external protocols | PHM reference arrays generated; HSE/reference features and external conversion pending |
| [04 Experiments](04_EXPERIMENTS.md) | theory/toy/PHM/native pilot and later controls | first genuine learned comparison still required |
| [05 Results](05_RESULTS_FIGURES.md) | paired statistics and CSV-only vector figures | reference metrics and toy outputs available |
| [06 Local GPU](06_LOCAL_GPU_8X4090.md) | actual HSE/reference checkpoints and single-GPU pilot | execute locally; no two-GPU training |

A completed slice leaves the executable/configuration, exact command and numerical output, and matching Results text. A missing data export or checkpoint is reported by name. Do not call that slice complete because its launcher exists. An unfavorable comparison is a completed result; it never requires adding another module to qualify as completion.

Do not force-push, modify `master`, delete branches, rewrite data splits, or modify PHMFactory core. Merge tested CPU/documentation slices into `dev`; keep method-performance claims separate from integration readiness.
