# Experiments, ablations and comparison contract

## 1. Runnable experiments and unimplemented studies

| Task | Command | Status and boundary |
|---|---|---|
| E0 theory | `bash paper/run.sh theory` | All numbered Markdown/Notebook witnesses; tests are not novelty approval |
| E1 finite acquisition family | `bash paper/run.sh oracle full` | Existing true-compressed-conditional versus plug-in experiment, preserved |
| E2 sampled-window study | `bash paper/run.sh sampled full` | Existing 24-design, 11-scalar header study, preserved |
| E3 allocation ablations | `bash paper/run.sh ablation full` | Alias for E2, not an independent experiment |
| P posterior parameterization | `bash paper/run.sh parameterization full` | New fixed-partition moment, precision, trace and low-rank controls |
| F figures from existing data | `figures` or `parameterization-figures` modes | Read CSV only; no simulation or model fitting |
| E4 official published baselines | `paper/run_official_baselines.sh` | Requires separately installed upstream code/data; launcher is not our new HSE integration |
| E5 learned HSE–LLapDiff | Three-arm protocol below | Not implemented; no oracle substituted for a training command |
| E6 real PHM | Explicit export and recording protocol below | Not executed |

`all smoke` runs implemented local studies only. Read `GOAL.md` for the sequential execution goals and `results_parameterization.md` for the new negative controls.

## 2. Preserve the earlier sampled protocol

The earlier E2 uses four coefficients from N(0,I), damping 12/18 inverse seconds, frequencies 100 and 100+delta Hz, rates 1024/2048 Hz, context durations 0.08/0.2 s, delta 5/30 Hz and regular/jitter/block-missing designs (24 cells). It deterministically selects K=4 non-overlapping P=16 patches. Missing observations are removed rather than imputed.

Full mode uses 2,048 events per simulator seed 0/1/2, with 384 reserved draws before evaluation. Coefficients recur across designs. Each acquisition gets separate measurement noise, shared across methods within that acquisition. The seven arms are diagonal, within-mode, magnitude, risk-oracle, within-mode moments, selected moments and full information, each under coarse/full-operator side inputs (336 rows). Sparse headers contain 11 scalars including layout code; full contains 15. Storage is matched across sparse arms, not inference cost or learned capacity.

Risk and magnitude select the same partition in all retained cells: equality follows from the same computation, not a nonsignificance test. Preserve the original numerical tables and valid older loose bounds; the new tighter bound is labeled separately.

## 3. New fixed-partition parameterization controls

At the same observation, prior and partition compare:

1. full posterior, explicitly larger reference;
2. natural blocks, retaining the information vector and likelihood blocks;
3. full posterior mean plus inverse precision blocks;
4. full posterior mean plus true marginal covariance blocks;
5. trace-isotropic information per full cosine/sine mode;
6. prior-whitened low-rank posterior covariance with exact mean.

Add a target-only low-rank approximation and exact target moments, explicitly not full-state representations. The six-dimensional fixed example uses a 4+2 partition, 19 scalars for all three block parameterizations and zero per-event layout cost. The new four-dimensional sampled controls use fixed within-mode pairs and 10 scalars, whereas E2 uses adaptive 11-scalar headers. Never combine these counts in a single matched-budget claim.

Report joint coefficient KL, target KL and exact Gaussian target-denoiser discrepancy under the same alpha/sigma. For fixed-point versus fixed-duration comparisons use separate tables: the latter changes P and observation count to preserve nominal physical cell duration. Do not describe these below-Nyquist direct samples as hardware anti-alias or private-band experiments.

The low-rank implementation is a dense small-matrix oracle of the published approximation family. Charge full covariance computation, prior knowledge and any factor transmission to it. Do not claim a matrix-free large-scale implementation or embedded-device timing.

## 4. Next minimal study: actual-condition and target audit

Freeze a reference encoder and define Z0 before comparison. Read the actual HSE and LLapDiff forward paths to identify O, H and consumed a. Check field consumption, deterministic evaluation patches and 1/2/3-channel shapes/gradients. A high-rate reference is common supervision, not privileged teacher input hidden in only one arm.

Two branches have different interpretations: when (H,a) loses information, estimate a true compression gap; when a reconstructs J and b is complete, test finite-network efficiency instead. Include a capacity-matched metadata MLP and an explicit solver. Do not remove available metadata to manufacture novelty.

Keep frequencies fixed and vary one non-frequency factor (a missing interval or damping) before expanding the design grid. Add one small pole-estimation mismatch. All estimated poles/noise and any decision threshold use source training/validation only. Phase tests rotate the prior as well as A,b,J; cheaper trace-isotropic and moment controls must be included. Arbitrary scalar pairings are not full-mode phase-covariant groups.

## 5. Learned comparison and ablations

Freeze one source-trained target VAE and its weights. Keep denoiser architecture, prediction parameterization, schedule, time weights, reverse sampler, batch composition and target grid equal. Train each arm's denoiser and conditioner rather than selectively freezing one.

| Arm | Condition and purpose |
|---|---|
| B0 | Original LLapDiff history summarizer + common a |
| B1 | Original HSE with fixed P,K,D + the same a |
| B2 | Metadata/capacity-matched HSE, with no hidden side stream |
| M | Simplest target-calibrated HSE feature justified by the controls |
| G / GM | Heteroscedastic Gaussian / finite mixture on the same condition |

Use the same source-validation search space where applicable, 20 maximum trials per learned arm and matched maximum optimizer updates. Report parameters, FLOPs, encoder and decoder latency separately, memory, storage precision, cache policy and training wall-clock. A +/-5% parameter/FLOP match must be measured. Dataset ID may route a task head but must not enter the embedding.

Primary metric: joint target Energy Score, with dependence diagnostics. Secondary: marginal CRPS, 50/80/90/95% condition-stratified coverage and width, observation-dependent prediction versus prior-only, paired retrieval and task log-loss/macro-F1. Approximate diffusion NLL is not interchangeable with exact mixture likelihood. Training seeds and posterior draws are distinct axes.

Ablate natural/mean-corrected/moment parameterization at fixed groups; coarse versus full a; coefficient versus target metrics; diagonal/trace/full-mode blocks; shuffled coupling/layout fields; no distillation versus matched-teacher distillation; fixed points versus physical duration; exact versus estimated poles; and STFT/wavelet/direct-time features with the same decoder. Run sequentially rather than a giant cross-product. No unproved observation-residual penalty is assumed posterior-unbiased.

## 6. Strong external comparisons, not a claimed SOTA ranking

LLapDiff is the direct parent. CSDI is for matching imputation; TimeGrad requires a matching autoregressive forecast protocol. ContiFormer, t-PatchGNN, Neural CDE and adaptable Warpformer belong in point-prediction tables unless a legitimate predictive law is provided. DLinear and PatchTST are required simple/patch forecasts. Physical controls include original HSE, Conv1D, STFT, wavelets and Prony/matrix pencil when modal estimation is compared. Spantini prior-aware and goal-oriented controls belong in analytic approximation tables. Time-IMM is an irregularity protocol reference, not a trained model.

The official LLapDiff adapters may restrict baselines to scalar target-only inputs. Match that scope or mark comparisons informationally unmatched and supplementary. Large pretrained models require a separate data/compute regime. A missing implementation is reported, never replaced silently.

## 7. Statistics and PHMFactory boundary

Independent unit: latent event, later machine/bearing/run/recording. Compute paired per-event differences before bootstrap. The earlier E2 uses 1,000 percentile bootstrap replicates per design; their intervals are diagnostic, not multiplicity-corrected universal claims. The new parameterization table uses finite analytical controls and descriptive means, not a confirmatory test. Repeated coefficient draws, rates and training seeds do not create independent machines. Freeze practical/equivalence margins before looking at the test comparison; p>0.05 is not equivalence.

No PHMFactory gitlink exists in the inspected branch. Do not add a submodule or import its internal factories to run this paper. Optional external preprocessing exports values[N,C], time_s[N] or [N,C], boolean valid_mask and a table containing recording_id, machine_id, split, sampling_rate_hz, units and sensor/channel identity. Paths are relative to an explicit data root; missing scientific fields are errors, not guessed defaults.

For E6, first audit one licensed raw vibration source and its grouping keys. Split machines/recordings before windows or rate views, fit all preprocessing on source only, then evaluate an unseen intermediate rate. Record anti-alias responses and coupled noise; filtered copies of one noisy record are not independent likelihood factors. CWRU and PU remain candidates, not admitted data or current evidence. Cross-hardware and cross-machine generalization need separate evidence.

## 8. Contribution decisions

Under fixed prior and forward KL, prefer moment/goal-oriented controls unless a measured cost or required update constraint justifies natural blocks. Do not continue searching for favorable frequency cases. Promote a learned contribution only after M improves the actual frozen target under equal information and cost relative to B1/B2 and the strongest simple probability head. Analytical correctness and CI are not novelty approval. `formal_claim_supported: false`; Flow Matching remains future work.
