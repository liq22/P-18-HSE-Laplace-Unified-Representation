# TII Goal map

Use one Goal at a time. Every completed Goal must leave: **executable change or frozen config + actual command/result + corresponding manuscript update**. Plans, TODO lists and smoke-only reruns are not completion.

| Goal | Purpose | Status at this revision |
|---|---|---|
| [01](01_SYNC_PHMFACTORY.md) | Validate latest accepted PHMFactory main before adding gitlink | BLOCKED before real-data acceptance; upstream main identified |
| [02](02_THEORY_MANUSCRIPT.md) | Keep notation, estimands, propositions and claims synchronized | IMPLEMENTED in paper files; toy still to run in final CI |
| [03](03_DATA.md) | Freeze official data sources, licenses, independent units and splits | SOP implemented; manual downloads pending |
| [04](04_EXPERIMENTS.md) | Execute theory/toy/native/PHM/external/SOTA/ablation slices | CPU theory/toy ready; GPU/data slices pending |
| [05](05_RESULTS_FIGURES.md) | Group-level statistics and CSV-only SVG/PDF/PNG figures | scripts implemented; real result CSV pending |
| [06](06_LOCAL_GPU_8X4090.md) | Local GPU execution after data/dependency gates | PENDING; first pilot is one GPU; 2-GPU forbidden |

Global rules: no force push; no `master` modification; no deletion of others' branches; no hash/checksum/receipt systems; no silent fallback; no paper-specific patch to PHMFactory core; negative results are retained.
