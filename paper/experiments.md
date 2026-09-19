# Industrial experiments: target identification, mechanism and diagnostic value

## Common design

All industrial data, labels, original-group identities and initial splits come from PHMFactory. TII uses industrial data only. Split original recordings/bearings/machines before generating paired acquisition views. Use a source-established reference and common fault ontology; unrelated datasets are not paired by matching labels. Source labels and source validation are allowed. Target labels are for final scoring only: no target normalization fitting, representation fitting, covariance-threshold choice, head fitting or hyperparameter selection. Unsupported classes require a separate open-set protocol.

The target–condition pair, source-frozen reference, noise model, query horizon, side inputs and numerical support tolerance are fixed before comparing methods. Source tuples are constructed by Eq. (6) after original-group splitting. Score a reference-feature posterior as such; do not call its target a noise-free mechanical state without calibration. Posterior scores require held-out jointly available reference targets. Where those targets are unavailable, report diagnosis and measured-evidence checks without inventing latent truth. Known synthetic laws support identification/error analysis; they do not enter industrial performance tables. Sampled windows, optimizer seeds and posterior draws do not increase the number of independent recordings or datasets.

## Stage I — real source-batch implementation experiment

Before an effect experiment, run the native intrinsic loss and reverse loop on the existing PHMFactory train/validation waveform exports. Use one predetermined first window per original recording for the batch, all training windows for the fixed source readouts, and no test-file access. A four-coordinate block-DCT reference gives an exact feature acquisition: observe coordinates 1–2, infer coordinates 3–4 from their same-recording joint targets. Normalize using source training values only. All missing coordinates are admitted and there is no source-global-null coordinate in this example; this cannot establish a restriction advantage. The observed feature conditional is a point mass because no additional observation noise is introduced. Do not label it a calibrated mechanical state or an HSE representation.

Retain source IDs/rates, basis errors, the intrinsic velocity/weighted-clean loss check, native gradient and parameter changes, reverse-step leakage/drift and fixed-head class probabilities. This experiment demonstrates the implemented path, not E1–E5 superiority. The waveform exports and checkpoint remain local to the run; numerical CSV/JSON diagnostics suffice for the report. Actual HSE/reference checkpoints and noisy conditional readouts are required for the full method comparison.

## E1 — unseen-dataset diagnosis

Train on multiple accepted source datasets and leave one complete dataset out in turn. Compare the complete proposal with observed-only HSE/direct diagnosis, the strongest source-selected same-input single method, static prediction fusion and compatible industrial references such as FISHER. Reproduce the source-only protocol rather than importing target-labelled kNN or target fine-tuning results as zero-shot baselines. HSE/TF-ProFM comparisons require available compatible implementations and equal data access.

Primary endpoint: recording-balanced pooled-confusion macro-F1 for each target, followed by the dataset-macro paired difference. Also report balanced accuracy, conventional pooled-window metrics and cost. Give each original group equal total weight, pool its weighted confusion contributions, then compute F1. Resample original groups for uncertainty; do not average single-class file F1. Freeze practical margins and selection budgets using sources. MFPT reference acceptance alone is not an E1 method result.

## E2 — posterior family and the restriction–dynamics interaction

Fix the same observed code R, observed-state readout q_o and source-trained diagnostic head h_psi in the primary mechanism comparison; fit them once on source reference tuples. End-to-end head refitting is a separate secondary experiment. First hold the same admitted target, observed condition and source supervision fixed and compare point prediction, Gaussian, finite mixture, ordinary latent diffusion and LLapDiff. The primary sample-based posterior endpoint is joint Energy Score on the common admitted target. Report uncertainty coverage, sharpness and joint dependence diagnostics separately. Exact KL/NLL is used only when its density and reference law are available. Do not compare an approximate diffusion likelihood with exact Gaussian NLL without matching conventions; a point predictor has a Dirac scoring interpretation, not a finite continuous-density NLL.

Then cross two interventions, rather than removing them together:

| Reverse-process restriction r | Ordinary temporal denoiser l=0 | Laplace temporal denoiser l=1 |
|---|---|---|
| r=0: no eligibility projection | ordinary / unrestricted | Laplace / unrestricted |
| r=1: eligible-only process | ordinary / projected | Laplace / projected |

All four arms receive identical support/eligibility descriptors, source groups, actual condition, observed-uncertainty model and diagnostic training rule. Match backbone scale, selection trials, prediction type, loss weighting, schedule and sampling steps as closely as possible. The primary path uses velocity prediction with unit loss weight and the explicit update in Method Eqs. (9)–(12). A clean-target objective must use the corresponding 1/sigma_k^2 weight at the same sampled noise levels to test parameterization equivalence. Otherwise it is an additional loss intervention. Keep guidance at one and target clipping disabled in the primary contrast. Record residual parameter/cost differences. The active state/noise geometry deliberately changes with restriction; do not describe this as identical computation.

Use one source-identified joint training/evaluation target for every arm. For each posterior draw, sample z_o once and retain it through the complete conditional reverse path. Compare this conditionally coupled procedure with independent marginal draws in a known-law dependence control; unchanged marginal coverage does not establish a correct joint law. No arm receives clean supervision for an unidentified or source-global-null coordinate. For the matched ambient-state comparison, embed the same partial target G_e z in the declared missing-state coordinates. Complementary entries are internal no-target placeholders, not clean-state labels. The unrestricted arm may perturb/evolve those entries as independent ancillary state; only the admitted component enters the training loss and proper score. No unknown clean complement is supplied to forward diffusion. Record the actual noise geometry and assess any additional emitted values separately as unsupported outputs. Independent nuisance noise cannot improve the Bayes denoising target; restriction tests finite-model fitting, sampling and resource effects, not an information gain. When every missing coordinate is admitted, r=0 and r=1 may coincide: that cell checks equivalence rather than supplying artificial restriction headroom. Diagnose effects on the same held-out groups.

For a larger-is-better outcome S, report both simple effects and

$$
\Delta_{{\rm int},e}=(S_{11,e}-S_{10,e})-(S_{01,e}-S_{00,e}).
$$

Use S=macro-F1 and S=minus Energy Score in separate analyses. Neither interaction nor either main effect is assumed positive. A joint-model win without these contrasts does not identify synergy; posterior improvement without a diagnosis gain is a posterior result only. DiEM/A-DPS/DiffEM comparisons belong in compatible known-operator corrupted-source settings, with their likelihood and training access matched, not as renamed off-the-shelf industrial baselines.

## E3 — conditioner and supervision attribution

Within a fixed eligible posterior process compare R, raw same-head H_A, statistical H_M, full-dimensional PCA/whitening/orthogonal coordinates and a matched nonlinear MLP. Keep the observed/diagnostic R bypass, q_o and h_psi fixed; change only the conditioner received by the generator. Use the same auxiliary-supervised source checkpoint when isolating the coordinate map; retain B1 without auxiliary training to isolate supervision. Transport the penalty when claiming affine equivalence. Record rank, scale, dtype, bytes, all learned parameters and covariance-factorization cost.

In the known linear oracle compare full (b,J), diagonal and declared block statistics. Equalize operator side information: full (A,R_noise) can reveal J outside the tokens. Distinguish actual conditional compression loss from a misspecified Gaussian plug-in. These comparisons test the statistical anchor, not the entire posterior formulation.

## E4 — identification and restriction boundaries

Compare no restriction, source support alone, support plus identification under the complete condition, and no missing-state inference. Report unsupported emissions, forbidden-subspace energy, admitted coverage, same-target posterior score and whole-task diagnosis. Reject-all has no posterior score on an empty target and cannot win through zero emissions alone. A wrong or uncertain support map is an explicit sensitivity condition.

Use the common-view binary witness: source A observes (C,P), source B observes (C,M), C is independent of a fair P, and M=P versus M=1-P. The two source observation laws coincide but p(M given C,P) differs. Neither alignment nor increasing the diffusion capacity distinguishes these worlds from those observations. A genuine joint source acquisition can distinguish them; alternatively an explicitly justified coupling narrows the model class. Record the extra information supplied by that intervention. A conditional-independence baseline is an assumption-dependent comparator, not a discovered physical fact.

In a separate fixed-noise Gaussian control, compare the marginal score with the joint score evaluated at a zero complementary coordinate. At correlation 0.8 the latter implies variance 0.36 rather than 1. The finite witness checks these score densities, not a finite sampler's output variance. The learned extension compares target-specific fitting with post-hoc restriction using the same known-law supervision. Add the non-diagonal-basis velocity/DDIM check before any physical support claim. These controls and the conditionally coupled-versus-independent covariance example are executed by the existing theoretical Notebook and recorded separately from industrial results.

## E5 — acquisition and temporal boundaries

Use post-split views of the same recording to compare known gain/invertible mixing, query grids, phase reference, bandwidth restriction and deletion of a task-relevant band. Separate fixed point count from fixed physical duration; anti-alias before downsampling. Finite-window damped signals are not exactly band-limited, so use filter response and leakage analysis rather than nominal Nyquist labels alone. Keep conditioning horizons equal: smoothing with later observations and history-only prediction solve different problems.

Measure support reassignment, observed/private-evidence drift, posterior error, temporal residuals, uncertainty and diagnosis. Cross the temporal parameterization with restriction as in E2. Unknown sensor mixing, modal mismatch and source-to-target conditional reversal are failure conditions. Retain equal or worse LLapDiff outcomes and direct-classifier wins; no expected curves or reference acceptance numbers fill unrun cells.

## Mechanism controls selected from the review

After the four restriction-by-temporal cells, change only the physical-time branch to Fourier features (or zero-damping modal synthesis) and a parameter-matched MLP time representation. Keep the Gaussian schedule, noise-level embedding, velocity objective, source split and query horizon fixed. Report remaining parameter/compute differences rather than claiming exact budget equality from hidden width alone. Laplace is inherited; this comparison tests its incremental value in the restricted procedure.

For uncertainty coupling compare a point observed readout, independently re-paired observed/missing marginal draws, and shared-observation conditional draws. Compute cross-covariance error only when a known conditional reference or repeated matched reference draws are available. One reference target per distinct condition does not reveal its true conditional covariance; use a proper joint score and aggregate coverage there. The index-repairing control preserves the model's marginal samples but breaks their within-condition pairing. Report downstream predictions separately. The noiseless Stage-I feature view does not exercise this uncertainty contrast.

Transport negative controls separately change (i) condition coverage, (ii) conditional coupling while preserving observed-source laws, and (iii) reference/sensor correspondence. Identical supports do not imply identical conditionals. All qualification rules, margins and model choices remain source-selected. An unchanged or worse Laplace/conditioner result completes that contrast and favors the simpler design.
