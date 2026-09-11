# Paper execution entry

The canonical TII execution goals now live in [`paper/goals/`](goals/README.md). This file remains only as the stable entry expected by existing local-agent workflows.

Current order:

1. `goals/01_SYNC_PHMFACTORY.md` — validate the exact upstream PHMFactory revision; do **not** add the gitlink before real-data acceptance.
2. `goals/02_THEORY_MANUSCRIPT.md` — keep notation, estimands, theorem assumptions and claims synchronized.
3. `goals/03_DATA.md` — acquire/audit data and freeze independent units/splits.
4. `goals/04_EXPERIMENTS.md` — run toy → genuine HSE pilot → PHM → external/SOTA/ablations.
5. `goals/05_RESULTS_FIGURES.md` — statistics and CSV-only SVG/PDF/PNG figures.
6. `goals/06_LOCAL_GPU_8X4090.md` — local GPU execution; first pilot uses one 4090, and **2-GPU execution is forbidden**.

Every completed slice must leave: **an executable change or frozen config + the actual command/result + the corresponding manuscript change**. A plan-only update is not completion.

Do not force-push, modify `master`, delete branches, add hash/checksum/receipt systems, or alter PHMFactory core code for this paper. Keep `formal_claim_supported=false` until real evidence supports the corresponding claim.
