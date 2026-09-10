# Experiments, ablations and comparison contract

## 1. Experiment map and runnable scope

| ID | Scientific question | Entry point | Implementation status |
|---|---|---|---|
| E0 | Do formal identities and counterexamples match executable calculations? | `bash paper/run.sh theory` | Implemented; each numbered result has Markdown + Notebook |
| E1 | True compressed conditional or plug-in mismatch? | `bash paper/run.sh oracle full` | Existing finite-design Task B, preserved |
| E2 | Does sampled-window coupling matter at equal header storage? | `bash paper/run.sh sampled full` | Implemented Gaussian sampled-waveform oracle |
| E3 | Which allocation, parameterization and side-input assumptions cause the effect? | `bash paper/run.sh ablation full` | Same E2 factorial run; not an extra independent experiment |
| E4 | Reproduce official LLapDiff and compatible published baselines | `paper/run_official_baselines.sh` | Verified official CLI launcher; requires separately installed upstream code/data; not executed here |
| E5 | Does the proposed conditioner improve the same learned LLapDiff? | B0/B1/M protocol below | Planned; no fake command substituting an oracle for training |
| E6 | Does the effect survive real recording splits and acquisition changes? | Local PHM export contract below | Planned; no real data trained in this update |

`all` runs E0–E3 only. The official public-dataset baseline is not a PHM result or the unimplemented learned HSE intervention.

## 2. Completed sampled protocol

One event has four coefficients drawn from known N(0,I). Two modes have damping 12 and 18 inverse seconds and frequencies 100 Hz and 100+delta Hz. Use rates 1024/2048 Hz, windows 0.08/0.2 s, delta 5/30 Hz, and regular/jitter/block-missing designs: 24 cells.

Select K=4 non-overlapping patches of P=16 raw points, deterministically over the window. Missing entries are removed, not refilled. All arms receive the same observations. Direct evaluation of damped waveforms is not a hardware anti-alias resampling experiment. A truncated damped sinusoid is not strictly bandlimited even when its nominal oscillation frequency is below Nyquist.

Each full cell uses 2,048 independent events per seed, seeds 0/1/2. Each seed reserves 384 prior draws before evaluation. No model is fit. Event coefficients are reused across designs; the cells are not 24 independent datasets. Noise is independent between separately generated acquisitions and shared across methods within one acquisition.

Arms: padded diagonal precision, fixed within-mode precision, magnitude-selected precision, design-risk-selected precision, within-mode posterior moments, selected posterior moments, and the larger full posterior. All sparse headers store 11 scalars including pattern ID; full stores 15. Moment heads perform exact inference at the encoder. Storage is matched; computation, information content and learned capacity are not all equal.

Repeat every arm with full actual A,R supplied to the decoder. This closes all header-induced inference gaps and is a required null control.

## 3. Primary estimates and uncertainty

E1 estimates true compressed-conditional expected log-ratio separately from plug-in mismatch. E2 reports exact Gaussian KL for each event between the full posterior and its plug-in or moment approximation. Do not call the latter compression mutual information.

For E2 report paired event-level means and 95% percentile bootstrap intervals (1,000 replicates) per design. Directional comparisons use the same event difference before bootstrapping. The mean over 24 designs is descriptive and does not multiply the effective sample size by 24. Risk-versus-magnitude equality is identity of selected layouts in this grid, not equivalence inferred from a nonsignificant p-value.

Secondary diagnostics: mean MSE, central marginal 90% coverage, joint Gaussian KL, normalized precision error, smallest normalized precision eigenvalue, bound looseness, actual observation count and header size. Moment matching may preserve all marginal coverages while losing joint dependence. A prior-only baseline is required in learned calibration studies.

## 4. Main learned comparison (E5)

Freeze one source-trained target VAE and its weights. Hold fixed the LLapDiff modal predictor architecture, v/x0/epsilon parameterization, schedule, time weights, sampling steps, optimizer, batch composition and evaluation grid. Train denoiser and conditioner in each arm rather than freezing one selectively.

| Arm | Change allowed | Why required |
|---|---|---|
| B0 | Official LLapDiff history summarizer | Immediate model origin |
| B1 | Original fixed-P,K,D HSE; same side input a | Benefit beyond replacing the conditioner |
| B2 | HSE + complete declared acquisition metadata | Eliminate an uncounted-information explanation |
| M | Budgeted acquisition-calibrated HSE | Candidate method |
| G | Heteroscedastic Gaussian on identical condition | Strong inexpensive probabilistic baseline |
| GM | Source-selected finite mixture on identical condition | Test diffusion complexity |

The full-statistic Gaussian and exact-moment oracles are separate analytical upper-information/upper-compute controls, not equal-budget trained models.

Use the same 20 source-validation tuning trials per learned arm and equal maximum optimizer updates. Record wall-clock, peak memory, parameters and FLOPs. A claimed +/-5% match must be measured, not assumed. All input observations and metadata are identical within an information regime. Dataset ID may route a task head but cannot enter the embedding.

Train seeds 0/1/2 and posterior Monte Carlo draws are separate axes. Select hyperparameters by one predeclared joint proper score. Use Energy Score with a dependence diagnostic or a declared exact joint likelihood. Report marginal CRPS, 50/80/90/95% coverage and width, downstream log-loss/macro-F1 and paired retrieval. Do not compare approximate diffusion NLL to exact mixture likelihood without identifying the approximation.

## 5. Mandatory ablations

| Ablation | Hypothesis | Failure interpretation |
|---|---|---|
| diagonal / within-mode / cross-mode allocation | Location matters beyond count | Equal results remove allocation contribution |
| magnitude / posterior-risk selector | Additional complexity helps | Current grid: none; retain simpler rule |
| precision / posterior-moment parameterization | Inversion amplifies omitted interactions | Do not blame all error on token information |
| full A,R side input | Alleged new information is absent | Zero gain is the correct control |
| shuffled layout ID or coupling fields | Decoder uses the advertised information | No change suggests an unused branch |
| remove distillation, lambda=0 | Teacher term explains gain | Compare matched teacher access |
| STFT/wavelet with same decoder | Laplace/HSE specificity | Narrow to general conditioning if equal |
| known / source-estimated poles and noise | Specification robustness | Oracle bound does not automatically transfer |
| physical filter mismatch, clock jitter, missing blocks | Acquisition robustness | Report degradation, not fallback preprocessing |

Do not implement the full cross-product before the B0/B1/M pilot works. E2 does not establish the learned ablations.

## 6. Published comparison set (not an asserted universal SOTA ranking)

| Category | Representative | Valid task/table |
|---|---|---|
| recent direct parent | LLapDiff (2026), official implementation | Probabilistic forecasting / declared target-horizon imputation |
| conditional diffusion | CSDI; TimeGrad when autoregressive protocol matches | Keep imputation separate from extrapolation |
| irregular modeling | ContiFormer, t-PatchGNN, Neural CDE, Warpformer if adaptable | Point MAE/MSE; no invented predictive densities |
| simple forecasting | DLinear, PatchTST | Same input scope, splits and horizons |
| physical tokenizer | fixed HSE, Conv1D, STFT, wavelet | Same condition budget and decoder |
| Bayesian approximation | diagonal/block, exact Gaussian/mixture, Spantini-style low-rank with accounted costs | Analytic diagnostics, not learned SOTA rows |
| irregularity coverage | Time-IMM taxonomy/data where relevant | Supplementary validity, not PHM substitution |

The official LLapDiff README states some adapters use target-only scalar input. Reduce the proposed method to that scope, or label an information-unmatched comparison as supplemental. Large pretrained models need a separate pretraining-data/cost regime.

## 7. Real-data plan and PHMFactory boundary

No PHMFactory submodule exists in the inspected dev tree. Do not add one to make the paper run. An external PHMFactory checkout may prepare data, but the paper consumes exports, not its internal readers/trainers.

Minimal export: per-record `values[N,C]`, `time_s[N]` or `[N,C]`, boolean `valid_mask`, and a table with `recording_id`, `machine_id`, `split`, `sampling_rate_hz`, sensor/channel identity and independently supplied labels. Declare units, sensor response and ontology. Paths are relative to an explicit data root. Missing fields are errors, not guessed defaults.

Choose a licensed raw vibration dataset after auditing recording/bearing identity. Split recordings/machines before windows or rate views. Fit normalization, poles, responses and cutoffs only on source data. Evaluate an unseen intermediate rate; record real anti-alias filters and coupled-noise structure. A filtered copy of one noisy record is not an independent measurement likelihood.

CWRU and PU are candidates, not admitted datasets or current evidence. License, native rates, grouping keys and high-frequency task value must be checked before freezing a final configuration.

## 8. Decisions

Admit a learned contribution only if M improves fixed LLapDiff under declared conditions, surpasses the strongest simple posterior alternative on proper scores or a meaningful cost/accuracy tradeoff, and retains task information. Negative calibration, prior misspecification and equal results must change the claim. Mathematical identities and CI remain supporting evidence, not novelty approval.
