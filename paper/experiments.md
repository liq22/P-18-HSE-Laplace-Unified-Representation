# Industrial experiments — primary diagnosis, mechanism scores separate

## I0: analytical and interface checks

Execute the existing proofs and the actual conditioner tests. Check full-map invertibility under its rank/arithmetic conditions, same-head affine composition, numerical collision under a declared covariance floor, native loss alignment and actual field consumption. Synthetic fixtures do not enter industrial empirical tables.

## I1: accepted PHMFactory reference

Retain the unchanged accepted MFPT config, seeds17/18/19, five CPU epochs, 20 files and original10/4/6 split. Restore selected checkpoints and independently recalculate pooled metrics. PHMFactory owns raw preparation/labels/splits. Its six-parameter reference and six test files do not establish proposed-method or cross-machine performance. Additional datasets require their own upstream acceptance, not a parent-side alternate reader.

## I2: direct industrial diagnosis

Obtain genuine source-trained HSE/reference exports and original-recording identities. Main comparison: B1-aux/R, M, and raw same-head H_A. The checkpoint, auxiliary supervision, q/dtype, targets and consumer are common. Primary endpoint is recording-balanced pooled-confusion macro-F1 with a fixed ontology. Add B1 to separate auxiliary training from message layout. Use a common linear diagnosis head first, then a small MLP and matched CNN/Transformer capacity control. The existing native-generation script is not a diagnosis trainer; label-probe implementation and actual exports remain required locally.

Freeze source selection metric, HPO trials, patience, loss grid, normalization, update count, seeds and practical/equivalence margins before evaluating held-out acquisitions. Produce rate/missing/channel views after original splitting, and separate fixed-point from fixed-duration protocols. Speed/load shifts are a different axis. Broader conclusions require at least two industrial sources or sufficiently many independently identified machines/bearings; file names alone do not establish that independence.

## I3: mechanism and strong simple alternatives

| Contrast | Competing explanation |
|---|---|
| M vs same raw head H_A | nonlinear covariance-coordinate map rather than trained affine head access |
| PCA/orthogonal/whitened R, with explicit ridge penalty | scale or regularization, not statistical semantics |
| matched learned linear/small-MLP transform | generic nonlinear reparameterization |
| mean-only, covariance/mean/target shuffles | unused fields or nonspecific auxiliary information |
| R/M prefix/tail/reference latent probes | acquisition/file shortcut rather than diagnostic information |
| direct diagnosis vs LLapDiff-mediated diagnosis | generation is unnecessary |

The optional native script now executes `--arms B1_aux M head_affine` with the same anchor and denoiser setup; its Energy Score is secondary. Report native loss, score components, source/unseen residuals and actual cost. Never call them a proof of macro-F1 improvement. Gaussian/mixture heads and separately named mean-MSE/beta-NLL controls follow only after the primary path works.

## I4: industrial SOTA, fusion and costs

FISHER is a closest industrial baseline, with official sub-band access and pretrained cost recorded, alongside compatible HSE/TF-ProFM, raw Conv1D/Transformer and physical STFT/wavelet front ends. Unavailable methods remain pending. Compare strongest source-selected single and static predictive fusion before optional acquisition routing. A source hard-headroom gap does not guarantee a win over static fusion; unknown target shift remains a sensitivity parameter.

Report q, dtype/bytes, rank/scales/condition, all source-head/consumer parameters, training updates, inference latency, peak memory and draw count when actually measured. `head_affine` omits covariance factorization, so equal checkpoint parameters are not equal inference work. Only real comparable measurements enter performance–latency–memory plots.

## Outputs and go/no-go

Keep full original-group predictions and shared seed sets. For nonlinear macro-F1 pool the recording-weighted confusion matrix first and recompute under group resampling; never average window or single-class file F1. Preserve null/worse M, unchanged affine predictions, static-fusion wins and target-order reversal. They are completed findings. Method performance, current reference acceptance and synthetic interface tests remain separate in Results. All nonindustrial empirical datasets are in `paper_TPAMI/`.
