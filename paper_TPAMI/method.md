# Method: conditional-moment specificity before routing

## 1. Scientific object and task

For each dataset fix observation O, deployment side information a, target U, original groups and the primary task. A frozen encoder supplies F. Let R be the complete ordinary code, source-trained with the same auxiliary supervision as its statistical message M=T(R). A comparison specifies target, consumer family, message size q, dtype and total training/inference cost. It is not a universal ranking of representations across incompatible metrics.

Classification uses direct label-prediction heads first. Future prediction/imputation uses actual measurements or one source-frozen reference target, with simple Gaussian/mixture consumers before a claim of diffusion necessity. LLapDiff remains one consumer; its native squared loss does not guarantee diagnostic macro-F1. The existing native runner is a two-arm generation pilot, not a universal classification runner.

## 2. Global conditional-moment message

Use the shared `MatchedConditioner`: source encoder and input mask/side fields → trainable trunk → R → global mean/covariance head. Gaussian scoring updates the actual R path later transmitted by B1-aux. The mean head is affine in R; the covariance path applies softplus, a declared covariance floor and Cholesky. These outputs are conditional-moment estimates, not an automatically calibrated full posterior.

Select one source-validation checkpoint, freeze input preprocessing, HSE, buffers, trunk and head, and replace a declared prefix with mean/Cholesky coordinates while retaining the ordinary tail. Both messages are global dense summaries with an explicitly all-valid output mask; original observation masks are consumed upstream. No unpriced side copy of the moments bypasses the message. Statistical units are checked at the raw readout, not required to persist through every learned downstream projection.

Gaussian score, its log-determinant/Mahalanobis parts, covariance eigenvalues and sample-out residual checks are recorded. Mean-MSE and beta-NLL are optional loss controls after the main path works. Seitzer's beta-NLL uses a detached variance weight; it cannot be silently substituted while claiming the same proper-score objective. Without oracle conditional moments, report held-out scores/residuals rather than a fictitious true-posterior RMSE. Freezing a source head does not establish target conditional calibration.

## 3. Required simple controls

Keep the actual message dimension fixed and compare R, full-q PCA, source-fitted whitening and a seeded orthogonal map. Full-dimensional transformations are invertible when their stated rank conditions hold, unlike truncated bottlenecks. Match dtype/bytes; no silent rank truncation or variance floor. For a solved ridge consumer report both ordinary isotropic regularization and the coordinate-transported penalty. The latter is an identity check, not a new learned competitor.

Add the exact R → frozen T → same consumer path: equality with M establishes packing/consumer consistency only. Then compare source-trained linear and small-MLP reparameterizations with the same supervision/search/checkpoint/update budget; these are not yet implemented by the affine CPU reference. Compare mean-only and shuffled mean/covariance/target controls to identify which statistical fields matter. A field shuffle is defined within a split and acquisition stratum with a recorded randomization; it never mixes train/test records.

## 4. Frozen tuning and costs

Before any target result, declare source checkpoint metric, loss-weight grid, HPO trial count, patience, optimizer/update budget, consumer architecture, q, dtype, normalization and paired seeds. PCA and whitening fit on source train only. Model/transform choice uses source validation; untouched calibration/test data do not choose targets, shrinkage, covariance floors or the model family.

Record dimensions and message bytes, coordinate buffers, rank/scales/condition, HSE/trunk/moment/consumer parameters, forward work, training updates, actual latency and peak memory where measured. Same q is an interface constraint, not equal information or full compute. A single CPU solve time is descriptive, not a stable inference-latency benchmark or a Pareto claim. Plot performance/latency/memory only once genuine comparable measurements exist.

## 5. Policy comparisons are secondary

The first decision is whether M beats ordinary and generic transformations on the fixed task. Keep best source-selected single and strong source-selected static prediction/distribution fusion. Add a hard acquisition selector only afterward. Generic hard headroom does not establish superiority over static fusion; soft token fusion trained jointly is another complete policy. Account for every evaluated expert and posterior draw.

Current target-drift bounds are sensitivity statements because b(a) is not observable from unlabeled target data. The independent bounded-loss certificate remains an optional tool only when its frozen-family, group independence, boundedness and shift assumptions hold. Raw Energy Score, onehot ridge score MSE, cross-entropy and nonlinear macro-F1 are not silently clipped into that theorem.

## 6. Actual external reference and remaining learned step

`japanese_vowels.py` now reads official UCI128 native-length sequences, preserves the original test set, and uses source time-mean LPC features with solved ridge. It writes masks, the correct LPC frame timing, labels and split groups, serializes/restores all fitted coefficients, and exports actual predictions. It does **not** produce HSE/reference-VAE features, posterior samples or statistically supervised messages. Their source-trained checkpoints and corresponding genuine extraction remain the next local dependency.

The other four external sources remain individually pending conversion; naming them at the native CLI does not integrate them. TII stays industrial-only through PHMFactory. This general workspace reuses `experiments/p19/`, the native conditioner and the single bibliography rather than copying trainers or upstream readers.
