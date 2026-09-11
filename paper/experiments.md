# Experiments — IEEE TII evidence chain

Every experiment is mapped to one innovation or one competing explanation. A failed early mechanism stops unnecessary later complexity.

## E0. Theory and native-contract checks

Run the full theory corpus, the routing-headroom toy and native LLapDiff one-batch acceptance. Keep the existing Gaussian positive controls, same-moment/non-Gaussian counterexamples, covariance-floor diagnostics and eps/v/x0 loss reconstruction. These validate objects/contracts, not method performance.

## E1. Minimal genuine HSE–LLapDiff pilot

Use genuine frozen HSE/reference exports. Principal arms: B1-aux and M; B1 remains the reference. Same \(Z_0\), source split, stage-one checkpoint, denoiser initialization policy, time/noise draws, updates and selection rule. Three paired training seeds form the initial pilot.

Primary generative endpoint: group-macro joint Energy Score on the frozen reference latent. Secondary: acquisition-stratified statistical score, coverage diagnostics and cost. M need not win; a null/negative result simplifies the paper.

## E2. Representation-selection ladder

After E1 is valid, compare:

| Level | Method | Competing explanation |
|---|---|---|
| Reference | B1 original HSE conditioner | extra statistical supervision explains gains |
| Best single | source-selected min(B1-aux, M) | one global representation is sufficient |
| Static fusion | one source-selected global α | simple combination explains gains |
| Dynamic route | source-only α(a), same q | acquisition-dependent accessibility is needed |

Compute group-level routing headroom before promoting dynamic routing. If headroom is below a predeclared practical margin, dynamic routing is not a headline method.

## E3. PHMFactory vibration-fault diagnosis — primary TII experiment

**All PHM data and dataset semantics come through PHMFactory.** The parent paper repository does not manually reimplement CWRU/Paderborn/MFPT readers or metadata.

### Acceptance before any PHM paper table

1. Pin/re-read the latest accepted `PHMbench/PHM-Vibench main`.
2. Install through the documented public package route.
3. Run `phmfactory doctor`, `preflight --config smoke`, and `demo`.
4. Select one real PHM dataset/config through PHMFactory and audit source/license note, labels, independent recording/bearing/run key and executed split.
5. Run its public preflight/execution without editing PHMFactory core.
6. Restore the selected checkpoint and recompute every declared primary metric from the retained prediction/result source.
7. Export the arrays/labels/acquisition metadata/group/split required by `experiments/p19`.
8. Only after this real-data acceptance add/update the parent `external/phmfactory` gitlink.

At the currently reviewed upstream revision, the public CWRU DG demo is explicitly labeled a draft and PHMFactory's release documentation still says real-data `baseline_valid` is not requalified. It is therefore a candidate wiring path, not accepted paper evidence.

### PHM model comparison

Use the same PHMFactory-provided raw data/split/labels to evaluate reference B1, B1-aux, M, best single, static fusion and (only after headroom) dynamic routing with the same diagnostic head. Primary class metric: independent-group macro-F1. Secondary: AUROC when class scores are valid, worst-acquisition F1, reference-latent Energy Score, latency and memory.

Separate **acquisition shift** (sampling rate, missingness, channel pattern, observed duration) from **operating-condition shift** (speed/load/system domain). Do not call speed/load DG evidence for acquisition routing when \(a\) did not change.

## E4. External non-PHM benchmark families

At least five benchmark families are required, each through its official source and task-compatible metric:

1. PhysioNet Challenge 2012 — irregular clinical, patient independent unit.
2. UCI HAR — subject-level sensor classification.
3. USHCN v2.5 — station/time climate forecasting/imputation.
4. ETT — chronological long-horizon forecasting.
5. UEA multivariate classification archive — original case/series unit.
6. Optional TIME-IMM after exact release/license audit.

External results test transfer of the conditioning principle. They are not pooled numerically with PHM metrics.

## E5. SOTA and strong baselines

Industrial: HSE, FISHER official implementation/checkpoint where compatible, TF-ProFM if executable official code/data protocol is available, selected recent TII diagnosis methods when reproducible, and a rate/mask-metadata control.

General/irregular: LLapDiff, CSDI, t-PatchGNN, Hi-Patch, HyperIMTS, Neural CDE, MOMENT, UniTS, PatchTST and DLinear on compatible tasks. A method without a probability output is not assigned a fabricated likelihood. Missing official code is recorded as unavailable rather than replaced by an unverified main-table reimplementation.

## E6. Ablations

| Axis | Required ablation | Competing explanation |
|---|---|---|
| Loss | no statistical score; matched score; covariance floor; native v/eps/x0 acceptance | extra objective versus statistical semantics |
| Representation | B1, B1-aux, M0, M, oracle moments where available | ordinary code versus moments versus non-Gaussian tail |
| Routing | best single, static α, dynamic α(a), shuffled acquisition descriptor | conditional headroom versus gate capacity |
| Structure | target dimension, prefix size, residual-tail size | budget allocation |
| Statistics | window/event versus original PHMFactory group; source versus unseen acquisition | pseudo-replication and transportability |
| Explanation | prefix/tail intervention, gate response, domain-ID shortcut probe | what the model consumes |
| Cost | scalars, parameters, updates, FLOPs, latency, memory, draws | extra compute |

Do not run a combinatorial grid when one falsifying ablation answers the question.

## E7. Statistics

Independent unit is latent event for synthetic studies and PHMFactory's audited physical group for PHM. Pair methods at the finest common unit, average seeds within event, events/windows within original group, then groups equally. Bootstrap groups, not windows. Equivalence requires a predeclared practical margin; `p>0.05` does not establish equality.

## E8. Results and figures

All quantitative figures read retained CSVs only. No plotting command calls a trainer or generates expected curves. Export SVG, PDF and PNG with editable vector text. Each main figure answers one Results-level question and retains null/negative outcomes.
