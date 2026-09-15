# Experiments: estimands, contrasts and execution status

## E0 — theory and finite falsification

`bash experiments/p19/run.sh theory` runs the historical theory corpus and the main-paper same-stem Notebook. `toy --events 1024` generates independent source/test events, fits fixed-arm selectors and fusion weights on source only, and writes observed test squared losses. Four cells distinguish no crossing, crossing, soft-fusion gain without hard headroom, and target-order reversal. The toy models are declared stochastic predictors, not a stand-in for trained HSE. Its theoretical constants and Monte Carlo scores are reported separately.

## E1 — real HSE/native LLapDiff pilot

First obtain actual frozen HSE/reference exports using a source-trained checkpoint. The required arrays, masks, side meanings, group keys, target map and timestamps are validated by the existing `feature_data.py`. The export note records which checkpoint/function produced each array; random tokens cannot fill a missing dependency.

Run native batch consumption/gradient/loss checks before training. Principal arms are B1-aux and M from one shared supervised checkpoint. Three paired training seeds use the same target, initialized denoiser, time/noise policy, update budget and source-only checkpoint rule. Primary score: recording-macro joint Energy Score. Separately retain native loss, statistical score components, target residual diagnostics, parameters and actual wall time. Choose a practical/equivalence margin before viewing test differences; nonsignificance does not imply equivalence.

B1 is the original unsupervised ordinary-conditioning reference; B0 is the compatible official LLapDiff entry. Additional learned arms are not implemented merely by naming them in a table. The existing native runner implements the two-arm pilot only.

## E2 — best single, static prediction fusion and dynamic hard selection

Fit arms on source-training groups; choose checkpoints on source validation. For later gate fitting use a separate source selection split or group cross-fitting; final target groups never select the representation or gate.

| Comparison | Exact intervention | Competing explanation |
|---|---|---|
| Reference B1 vs B1-aux | ordinary code without/with auxiliary statistical training | extra supervision, not explicit moments |
| M vs B1-aux | deterministic message reparameterization, common checkpoint | finite-model utility vs information loss |
| Best single | one source-selected fixed trained arm | a global choice is adequate |
| Static prediction fusion | constant source-selected combination of predictions/distributions | complementarity alone explains a gain |
| Hard acquisition route | source-only selector among the same frozen arms | acquisition-dependent selection adds value beyond static fusion |
| Optional soft token fusion | newly trained finite model, counted independently | nonlinear mixture/capacity rather than the hard-selection theorem |

Hard headroom is not used to rule out soft fusion or to claim a win against static fusion. The main theory applies to fixed expert risks; joint retraining changes them. Gate descriptor shuffling and target-order reversal are required negative controls. Report all-arm fusion cost rather than calling equal transmitted dimension equal inference cost.

## E3 — PHMFactory vibration diagnosis

PHM data come only through PHMFactory. The accepted current-source MFPT reference uses the unchanged GlobalAverageLinear config, seeds 17/18/19 and five CPU epochs. Its 20 source files split into 10 training, 4 validation and 6 test files. Checkpoints were independently restored, predictions retained and pooled accuracy/macro-F1 independently recomputed. This qualifies the exact reference path and gitlink, not a learned HSE result or all PHMFactory datasets.

Primary method protocol: use PHMFactory's frozen raw-recording split before constructing paired rate/missing/channel views. Source representations and normalization never use target labels. Compare B1, B1-aux, M, source-selected single, static fusion and justified hard selection with the same linear diagnosis head. A small MLP is a secondary capacity ablation. MFPT file separation does not certify physical-bearing separation; CWRU or other maintained PHM datasets require their own upstream accepted reader/split check before use.

Primary classification endpoint: recording-balanced **pooled-confusion** macro-F1 over the fixed ontology. Each recording contributes equal total sample weight; compute F1 after pooling, not per-window or per-single-class recording. Retain conventional framework pooled-window accuracy/F1 for exact reproduction. Bootstrap original groups and recompute nonlinear metrics. Six test files provide a limited scope, not a cross-machine generalization claim.

Acquisition shift (rate, duration, missingness, channel set) is analyzed separately from operating-condition shift (speed/load). The latent Energy Score and diagnosis macro-F1 are distinct outcomes. Neither is substituted for the other.

## E4 — five external domains

| Domain / release | Task and independent unit | Strong starting comparison | Current status |
|---|---|---|---|
| PhysioNet 2012 v1.0.0 | irregular clinical; patient; historical imputation / declared future query split | CSDI, Neural CDE, LLapDiff | download/conversion/feature export not run |
| UCI HAR id 240 | wearable classification; subject; official split | HSE, MOMENT, same linear head | raw inertial-channel preparation pending |
| USHCN monthly v2.5 | station/time forecasting; chronological blocks | seasonal/last-value, DLinear, PatchTST | official monthly source frozen by retrieval note; not the daily-USHCN benchmark |
| ETTh1 / original ETT revision | energy forecasting; chronological time blocks | DLinear, PatchTST, task-compatible LLapDiff | local preparation pending |
| UEA/UCI Japanese Vowels | variable-length speech features; series; 9 speaker classes | same head, MOMENT, irregular-time references | preserve native lengths; no leave-speaker-out claim |

The exact source/license/labels/conversion instructions are in `experiments/DATA_DOWNLOAD_SOP.md`. These are five scientific domains, not five interchangeable metric rows. Training expects genuine feature exports and dataset-specific frozen configuration; the external launcher is not a raw-data converter.

## E5 — SOTA eligibility

Use HSE and compatible FISHER/TF-ProFM official implementations for industrial representation, with their protocol/pretraining access reported. For irregular prediction/imputation consider LLapDiff, CSDI, t-PatchGNN, Hi-Patch, HyperIMTS, ContiFormer and Neural CDE. MOMENT/UniTS/PatchTST/DLinear are task-compatible broad/simple references. Gaussian and finite-mixture probability heads receive the same condition as Diffusion.

The existing official-baseline launcher executes upstream LLapDiff's declared dataset/task CLI. It does not imply the five new external protocols are already supported by that CLI. An unavailable method is explicitly pending; do not silently use a random initialized replacement or fabricate a probability score for a point predictor.

## E6 — focused ablations

| Axis | Minimal ablation | What it can falsify |
|---|---|---|
| Loss | no auxiliary score, shared auxiliary score, declared floor; native v/epsilon/x0 check | supervision or loss mismatch explains the result |
| Representation | R, M, moment-only, oracle moment replacement where available | ordinary shape information or moment prediction error explains the gain |
| Routing | best single, static prediction fusion, hard source route, descriptor shuffle | gate usefulness and shortcut reliance |
| Structure | one smaller/larger target dimension and prefix budget | capacity rather than statistical structure |
| Statistics | pooled windows vs recording-balanced estimator | pseudoreplication / unequal recording weights |
| Explanation | prefix/tail intervention; source/unseen residuals | whether fields are consumed; not causal-mechanism proof |
| Cost | all parameters, anchor updates, inference, mixture draws, memory | extra compute rather than representation gain |

Execute one falsifying contrast at a time, not a combinatorial architecture search. Generic headroom is not the study's unique innovation. M losing, static fusion matching routing, or target ordering reversal is a completed scientific result and triggers simplification.

## E7 — outputs

Additive event scores contain method, condition_id, group_id, seed, unit_id and value. Repeated identical keys are rejected, not averaged. Classification exports contain fixed-ontology truth/prediction/class scores and original groups. Seeds and posterior draws are separate from independent recordings. Figures read retained CSV only and export SVG/PDF/PNG; no trainer is called by a plot command.
