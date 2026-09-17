# Experiments: test representation specificity before general expansion

## G0. Shared calculations and fixed-policy witnesses

The historical analytical studies and existing policy/certification witnesses remain regression evidence with their stated scope. No new routing theorem is added. Exact Gaussian mean dimensions/nonfinite rejection and condition-wide common seed sets are mandatory before numerical interpretation. Formal studies supply `--expected-seeds` so a missing seed everywhere is not mistaken for a smaller planned experiment.

## G1. Actual first external reference

`vowels-reference` converts the official UCI128 archive, preserving native lengths and original test labels. Source utterances are divided18/6/6 per speaker into fit/validation/calibration; test370 is unchanged. Fit full-q identity/PCA/orthogonal/whitened coordinates on source-fit time-mean LPC features only. Each isotropic ridge model gets the same three source-validation trials; coordinate-matched controls use the selected R penalty. Calibration/test never choose transforms or hyperparameters.

The consumer is closed-form onehot ridge with an intercept. Its nine outputs are class scores, not normalized probabilities. Main metrics are accuracy and fixed-ontology macro-F1. Onehot MSE is an auxiliary score, not a certified Brier loss. Check coefficient restore, per-utterance predictions and exact transported-penalty equivalence. This is a real external data/reference slice, not a conditional-moment or HSE method comparison. No IID confidence guarantee is asserted from unique utterance IDs; the archive does not identify independent sessions.

## G2. Minimal learned contrast and fixed choices

Next use actual source-trained encoder/checkpoints to produce a common R and conditional-moment map. The first genuine pilot compares M against B1-aux, exact R→T composition, full-q PCA/whitening/orthogonal, and a same-budget linear/small-MLP reparameterization. Preserve B1 without auxiliary supervision, mean-only, shuffled mean/covariance and shuffled auxiliary-target controls. Execute the identity/plain controls first, then learned alternatives; a listed arm is not an implemented trainer.

Freeze source checkpoint criterion, auxiliary-loss grid, HPO trials, early stopping, normalization, seed set, q/dtype, consumer architecture, update budget and original groups before inspecting test. Native defaults150 anchor/200 denoiser updates are only smoke-pilot settings, not tuned method results. A fair expanded learned configuration must give every paired arm its declared share of fitting and search. No test-conditioned floor, target map or dataset replacement.

Classification: start with R/M + linear and small MLP, then the same direct CNN/Transformer head if appropriate. LLapDiff-based classification must outperform these before generator necessity is claimed. Forecast/imputation: same target and query protocol, simple Gaussian/mixture heads, then native LLapDiff. Main task metric and squared denoising/latent scores remain distinct. Genuine HSE/reference exports and these learned comparisons are pending; the implemented native entry still runs only B1-aux/M generation.

## G3. Five fixed external families

| Domain | Source | Task / evaluation unit | Current status |
|---|---|---|---|
| Clinical | PhysioNet2012 v1.0.0 | imputation/future queries; patient | SOP ready; real converter/features pending |
| Wearable | UCI HAR240 | activity classification; subject | SOP ready; real inertial-series conversion pending |
| Climate | USHCN monthly v2.5 | station forecasting; chronological blocks | monthly protocol, not daily; conversion pending |
| Energy | ETTh1 | forecasting; chronological blocks | official version specified; conversion/features pending |
| Speech features | Japanese Vowels UCI128 | nine-class recognition; utterance with dependence limits | official conversion, source-fitted affine reference, restored predictions executed; learned HSE pending |

Do not average incompatible domain metrics into one score. At least two encoder and consumer families plus target/budget changes are needed before a broad general conclusion. Industrial PHM transfer, when reused, is attributed to TII; it is not a new duplicate empirical contribution.

## G4. Strong baselines, policy and ablations

| Axis | Required comparison | Explanation tested |
|---|---|---|
| Representation | raw/full-q PCA/whitened/orthogonal; matched regularizer | ordinary coordinate conditioning |
| Structure | M vs mean-only, covariance fields, generic learned linear/MLP | statistical versus generic nonlinear feature |
| Loss | same auxiliary supervision; mean-MSE, Gaussian score; beta-NLL optional with its exact definition | auxiliary training or unstable variance |
| Target/reference | label/proper-score probes for R,prefix,tail,Z0; acquisition and speed/load probes where observed | nuisance/target-map preference rather than task information |
| Consumer | linear/small MLP/direct task head versus diffusion | unnecessary generator or capacity advantage |
| Policy | best single and source-selected static mixture; hard route optional afterward | ensembling explains apparent routing gain |
| Statistics | original-group weights; common predeclared seeds; fresh calibration | pseudoreplication/selection bias |
| Explanation | actual field interventions, source/unseen residuals and paired retrieval | stored but unused statistics; not causal identification |
| Cost | dtype/bytes/rank/scales, encoder/readout/consumer work, training/search, latency/memory | extra information access or unpriced work |

A file-ID closed-set probe is undefined for held-out unseen file labels; use a separately named within-source diagnostic or same-event retrieval rather than adding test identities to training. Acquisition predictability alone is not proof of a shortcut: it is harmful only in relation to target evidence or generalization loss. Covariance shuffling/normalization choices are declared before testing.

Task-compatible SOTA candidates remain MOMENT/UniTS, Moirai-MoE/AME-TS, Neural CDE/t-PatchGNN/Hi-Patch/HyperIMTS/ContiFormer, CSDI/LLapDiff and simple PatchTST/DLinear. Match official task/input/pretraining access and budgets; unavailable code stays pending. Industrial FISHER and TF-ProFM remain TII closest controls, not automatically run on all five nonindustrial domains.

## G5. Results and stop rules

Plot actual prediction/metric CSVs only. A performance-latency-memory Pareto figure requires all three actual compatible measurements; the present one-shot CPU fit timer is not enough. Report null effects and limited independent groups. Failure to beat PCA/MLP means statistical specificity is unsupported. Direct classification matching diffusion removes generator necessity; static fusion dominating routing removes a compulsory router. These outcomes finish a comparison, rather than trigger a new model or replacement test dataset.
