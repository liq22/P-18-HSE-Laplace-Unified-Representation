# Industrial results and pending method evidence

## Executed reference: PHMFactory MFPT

The exact dependency is `a0db97364e6d38a927c3ea30c643ebbb821d54d7`. The unchanged `configs/baselines/01_mfpt/mfpt_global_average_linear.yaml` ran five CPU epochs with seeds17/18/19. Initial acceptance run34765060233 and later dev CI34990021558 performed public installation, smoke, preparation, training, selected-checkpoint restoration and independent metrics.

| Seed | Test windows | Accuracy | Pooled macro-F1 | Selected epoch |
|---:|---:|---:|---:|---:|
|17|96|0.500000|0.2222222222|4|
|18|96|0.3333333333|0.1666666667|4|
|19|96|0.1666666667|0.0952380952|4|

This six-parameter reference is not the proposed HSE method. Mean accuracy is0.3333333 (sample std0.1666667); mean F1 is0.1613757 (sample std0.0636572). Independent agreement errors were below1e-6. Shapes were train160×2048×1 from10 files, validation64×2048×1 from4 files, test96×2048×1 from6 files. Since each test file has16 windows, group-balanced pooled and ordinary pooled metrics coincide in this reference; this is not general.

The initial parent-side ResolvedConfig serialization failure was corrected using `runtime_config()` without changing upstream model/data/protocol. Raw and derived waveform arrays are not uploaded. File separation is not a claim of unseen physical bearings or machines.

## Native component evidence

The retained `assets/native_component_reference.csv` records original LLapDiff loss/gradient/consumption checks with explicitly synthetic input. It does not execute genuine HSE or the reference encoder and does not show a method advantage. Older analytical posterior CSVs remain shared regression evidence with their original scope.

## Relocated general evidence

The fixed-predictor routing/fusion table and its source CSV now live under `../paper_TPAMI/`. They are not TII empirical results. The new general calibration study likewise belongs there. The move does not create additional independent evidence.

## Pending industrial method table

Actual source-trained HSE/reference checkpoints and feature extraction are still needed. M vs B1-aux, B1, industrial static fusion/selection, real acquisition changes and industrial strong baselines remain unrun. No blank slot is filled with reference accuracy, synthetic scores or anticipated improvement. `formal_claim_supported: false` concerns the learned method. A negative comparison is retained and can complete the industrial task.

## Source-supported posterior writing/theory slice — 2026-09-18

The current manuscript promotes cross-dataset source-supported posterior inference to the main problem, with HSE conditioning and restricted LLapDiff as the proposed mechanism. Existing R/head_affine/M results are unchanged and retained as condition-interface controls. No native model training was performed by this writing revision.

Executed locally with `bash paper/build_frontmatter.sh outputs/tii_support`: 31 recorded original papers are cited in the Introduction/Related Work; the same-stem Notebook produces 14 finite witness values; source SVG/PDF/PNG and a cited front-matter PDF are regenerated. The build is not a complete learned-method or full-paper experimental validation. Full current-commit CI is recorded by the merge discussion after its actual execution rather than presumed here.

| Finite check | Actual value | What it establishes |
|---|---:|---|
| Four source-role projector sum residual | 0 | Completeness in the stated finite linear example |
| Target source-common rank / target missing rank | 0 / 1 | A target can lose a direction shared by all sources |
| Ambiguous state distance under A=[1,1] / observation difference | 1.4142135623730951 / 0 | Nonzero coordinate sensitivity does not imply coordinate recoverability |
| Opposite conditionals with identical unpaired marginals | gap 1 | Source support alone does not identify a joint conditional |
| Correlated-prior null posterior mean / variance | 0.4 / 0.68 | No direct likelihood term does not imply no prior-mediated update |
| Independent-prior null variance | 1 | Contrasts the role of the assumed prior |
| 100 projected updates: forbidden component / observed drift | 0 / 0 | Algebraic support compliance of projected proposals, not correct posterior sampling |
| Empty eligibility | 0 generated coordinates; no public estimate | No sampling target is not a confident zero reconstruction |
| Source-to-target conditional reversal | gap 1 | Identification on source does not establish transportability |

These are analytical witnesses from the explicit models in `theory_main.md`, not measurements on learned industrial latent states. `assets/support_witness.csv` retains the values. Unknown source coordinate correspondence, uncertain operators and finite-window leakage remain scientific prerequisites.

## New mechanism still to implement and evaluate

The current native `run_native_pilot.py` does not implement source-qualified modal blocks, an identified joint missing target or support-projected reverse updates. The new formulation therefore requires source-reference validation and a real native restriction before an E1/E2 method result exists. Existing unrestricted native/synthetic tests cannot be renamed as that validation. Future tables separate same-target posterior quality, eligible coverage and unsupported emissions, and per-target original-group diagnostic performance. Reject-all and wrong-support controls prevent perfect structural rejection from being mistaken for useful inference. A Gaussian/mixture or ordinary latent diffusion matching LLapDiff is retained as a decisive negative result.
