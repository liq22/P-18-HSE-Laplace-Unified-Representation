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
