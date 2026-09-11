# Experiments — IEEE TII evidence chain

Every experiment is mapped to one innovation or one competing explanation. The sequence is staged: a failed early mechanism stops unnecessary later complexity.

## E0. Theory and native-contract checks

**Question.** Are the mathematical objects aligned with the actual conditioner and native LLapDiff loss?

Run the full theory corpus, the nested-message/routing toy, and native one-batch acceptance. Keep existing Gaussian positive controls, same-moment/non-Gaussian counterexamples, covariance-floor diagnostics and eps/v/x0 loss reconstruction.

**Evidence:** theorem/toy numerical residuals, native loss discrepancy, shared-gradient and field-consumption checks. These are not method performance.

## E1. Minimal genuine HSE–LLapDiff pilot

**Question.** Does M improve over the equally supervised complete ordinary code B1-aux on genuine frozen HSE/reference exports?

Arms: B1-aux and M. Keep B1 as reference. Use exactly the same \(Z_0\), source split, stage-one checkpoint, denoiser initialization policy, time/noise draws, updates and selection rule. Three paired training seeds are the first pilot; posterior draws are Monte Carlo samples, not independent training units.

Primary generative endpoint: group-macro joint Energy Score on the frozen reference latent. Secondary: acquisition-stratified moment score, coverage diagnostics and cost.

**Decision:** M does not need to win. If it fails to exceed a predeclared practical margin at comparable cost, retain B1-aux and stop promoting the statistical prefix.

## E2. Representation-selection ladder

This experiment is run only after E1 is valid.

| Level | Method | Competing explanation |
|---|---|---|
| Reference | B1 original HSE conditioner | extra supervision may explain all gains |
| Best single | source-selected min(B1-aux, M) | one global representation is sufficient |
| Static fusion | one source-selected global α | simple combination explains gains |
| Dynamic route | source-only α(a), same q | acquisition-dependent accessibility is needed |

Before fitting the dynamic gate, compute group-level routing headroom. If headroom is below the declared practical margin, dynamic routing is **not run as a headline method**. Report that the theory correctly selected the simpler representation.

For routing, stratify by sampling rate, observed duration, missingness and channel pattern. Dataset ID and target labels are forbidden gate inputs. Compare source holdout and one or more unseen acquisition conditions without target refitting.

## E3. PHMFactory vibration-fault diagnosis — primary TII experiment

PHM evidence is primary. PHMFactory is an external execution dependency and is not imported by paper modules.

### Acceptance before any paper table

1. Pin the reviewed upstream `PHMbench/PHM-Vibench` accepted `main` revision.
2. Install through its documented package route.
3. Run `phmfactory doctor`, `preflight --config smoke`, and `demo`.
4. For a real-data config, audit official raw source, label mapping, independent recording/bearing/run key, split-before-windowing, checkpoint selection and configured metric closure.
5. Recompute the primary metric from retained predictions or the documented result table; do not accept a terminal summary alone.
6. Only then add/update the parent `external/phmfactory` submodule pointer.

Upstream currently states that release readiness is blocked until a real-data configuration is requalified as `baseline_valid`; therefore the pointer must not be added merely because Dummy smoke succeeds.

### Primary PHM protocol

Start with one dataset with raw recordings and clear acquisition information. CWRU is a candidate because the official source includes 12 kHz and 48 kHz drive-end data; Paderborn is a second candidate with documented operating conditions and CC BY-NC 4.0 terms. The exact first dataset is frozen only after the data audit in `paper/experiments/DATA_DOWNLOAD_SOP.md`.

Split original recording/bearing/run before windows or synthetic acquisition views. Construct rate/missingness views only within each split. Compare all four representation levels above with the same fault head. Primary diagnostic metric: recording-macro macro-F1. Secondary: AUROC, worst-condition F1, calibration, reference-latent Energy Score, latency/memory.

### Acquisition versus operating-condition domain

Report two axes separately:
- **acquisition shift:** sampling rate, missingness, channel pattern, observed duration;
- **operating-condition shift:** speed/load/system domain defined by the dataset.

Do not call a speed/load transfer result evidence for acquisition routing unless acquisition descriptors actually change.

## E4. External time-series benchmark families

At least five benchmark families are required, but they do not all use one metric.

1. **Irregular clinical:** PhysioNet Challenge 2012; patient is the independent unit; mortality/irregular-observation tasks use task-compatible heads.
2. **Human activity sensors:** UCI HAR; subject-level split; classification.
3. **Climate/environment:** USHCN; station/time split; forecasting or imputation according to the reproduced baseline protocol.
4. **Regular long-horizon forecasting:** ETT/Weather/Electricity; standard chronological split; MSE/MAE and probabilistic score only for methods with a matched probability head.
5. **Multivariate time-series classification:** UEA/TSML archive; use original train/test where valid and dataset-specific licensing; macro/accuracy according to benchmark convention.
6. **Optional irregular multimodal stress test:** TIME-IMM after its exact data license/download route is frozen.

External results test transfer of the conditioning principle. They are not pooled with PHM metrics.

## E5. SOTA and strong baselines

### Industrial

- HSE;
- FISHER official checkpoint/code where compatible;
- TF-ProFM if an official executable implementation and compatible data path are available;
- representative recent TII cross-domain diagnosis methods only when code/protocol can be reproduced;
- same backbone with rate/mask metadata only.

### General/irregular time series

- LLapDiff reference;
- CSDI for imputation;
- t-PatchGNN, Hi-Patch, HyperIMTS and Neural CDE for compatible irregular tasks;
- MOMENT and UniTS for task-compatible transfer;
- PatchTST and DLinear as strong simple regular-time baselines.

A method is omitted from a metric it does not define. Missing official code is recorded as unavailable, not replaced with an unverified reimplementation in the main SOTA table.

## E6. Ablations

| Axis | Required ablation | Explanation tested |
|---|---|---|
| Loss | no moment score; matched score; covariance floor; native v/eps/x0 acceptance | extra objective versus statistical semantics |
| Representation | B1, B1-aux, M0, M, oracle moments when available | ordinary code versus moments versus non-Gaussian tail |
| Routing | best single, static α, dynamic α(a), shuffled acquisition descriptor | conditional headroom versus extra gate capacity |
| Structure | target dimension, statistical-prefix size, residual-tail size | budget allocation |
| Statistics | event/window versus recording grouping; source versus unseen condition | pseudo-replication and transportability |
| Explanation | prefix/tail intervention, gate response to physical acquisition variables, domain-ID shortcut probe | what the model consumes |
| Cost | message scalars, parameters, updates, FLOPs, latency, memory, sampling draws | whether gains come from more compute |

Every ablation is tied to a competing explanation. Do not run a combinatorial Cartesian product when a one-factor falsifying experiment suffices.

## E7. Statistics

Independent unit is latent event for synthetic paired studies and machine/bearing/run/recording (or subject/station/patient) for real datasets. Pair methods at the finest common unit, average seeds within event, events/windows within original group, then groups equally. Bootstrap groups, not windows. Report actual seed count and posterior draw count separately.

Equivalence requires a predeclared practical margin and a confidence interval/equivalence rule. `p>0.05` is not evidence of equality. The routing gate is promoted only if its improvement over the best source-selected single representation is positive beyond the practical margin and reproducible on unseen acquisition conditions.

## E8. Results and figures

All quantitative figures are generated from retained CSV files only. No plotting command calls a trainer or synthesizes expected curves. Export SVG, PDF and PNG. Each main figure answers one Results-level question: theory/headroom, native validity, PHM main result, routing behavior, external generalization, ablation or cost.

The plotting contract follows the requested nature-figure principles: conclusion first, data/figure code separated, physical-size legibility and vector text. It is not a claim of Nature-format certification.
