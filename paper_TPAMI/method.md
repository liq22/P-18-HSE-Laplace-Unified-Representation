# Method: conditional-moment specificity before routing

## 1. Scientific object and primary task

Freeze observation O, deployment side information a, target U, original groups and the primary task. R is a complete ordinary code obtained through a source-trained frozen encoder and shared statistical supervision. M=T(R) is a deterministic reparameterization. A comparison specifies consumer family, q, dtype, train/validation protocol and full cost. In the full-rank exact-map case M is information-equivalent to R, not intrinsically lossy. Finite-precision behavior and actual checkpoint rank are checked separately.

Classification starts with direct label heads. Forecasting/imputation uses real targets or a fixed source reference latent, with Gaussian/mixture heads as controls. LLapDiff is one consumer, not a necessary component of all tasks. Native squared loss does not imply improved macro-F1.

## 2. Global conditional-moment message

Use the shared MatchedConditioner: frozen features plus explicit input mask/side → trainable trunk R → Linear global head h. The Gaussian score updates this exact R path, not a detached head. The mean is affine in R; raw covariance coordinates pass through softplus and declared covariance-floor/Cholesky operations. The resulting fields estimate conditional moments, not a full posterior by definition.

Choose the checkpoint on source validation and freeze preprocessing, feature extractor, buffers, trunk and head. M replaces s=d+d(d+1)/2 coordinates with mean and triangular covariance factor and retains the tail. Both outputs are dense global summaries with an explicitly all-valid output mask. Original history masks are consumed upstream. Statistics are checked at the raw readout; downstream transformations need not retain units. No unpriced parallel moment message is supplied.

## 3. Same-head affine control: the first nonlinear-specific comparison

The implemented `head_affine` arm transmits H_A=[h(R),R_tail] using the same selected parameters, targets, supervision, q and dtype. No separate fitting occurs. Only the covariance-coordinate nonlinear map differs from M. Raw covariance coordinates of H_A are not assigned moment semantics.

The proof in `theory_main.md` gives M=Φ(H_A) and an inverse of Φ on its exact attainable image; W_p need not be full rank for this equivalence. An affine consumer after H_A collapses into an affine function of R. Thus three contrasts have distinct roles:

| Contrast | What it tests |
|---|---|
| M versus B1-aux/R | complete coordinate intervention under shared supervision |
| H_A versus R | access to the same trained affine head coordinates |
| M versus H_A | nonlinear statistical covariance coordinates for the chosen finite consumer |

A win only over R does not establish statistical specificity. Equality with H_A supports the simpler transformation. Even a gain over H_A still needs generic nonlinear and cost controls; it is not automatically a full-posterior effect.

## 4. Other required simple alternatives and budgets

Retain source-fitted full-q PCA, orthogonal coordinates, and whitening with both isotropic and coordinate-transported ridge penalties. Truncation/flooring changes the declared experiment. R→same frozen T→same consumer is an identity check. Same-supervision learned linear/small-MLP alternatives, mean-only and shuffled mean/covariance/target messages are subsequent controlled arms; the CPU affine reference does not claim to train them.

Freeze loss-weight grid, HPO count, normalization, checkpoint metric/patience, consumer capacity, updates, source split and seeds before test results. Record q, dtype/bytes, coordinate rank/condition/scales and all parameters. `costs.csv` now distinguishes whether the affine head and statistical factorization were evaluated, and records head/trunk/denoiser parameter counts plus actual training/sampling time. It does not claim FLOPs or stable inference-latency/memory measurements not obtained. Equal q is not total cost equality.

## 5. Statistical semantics and diagnosis

Keep score/logdet/Mahalanobis/eigenvalue diagnostics. Mean-MSE and beta-NLL are later loss controls; the original beta-NLL uses a detached variance weight and changes the optimization rule. Without oracle moments report held-out scores and residuals, not a fabricated posterior-mean RMSE. Source supervision does not establish unseen-acquisition calibration. The primary task determines the claimed endpoint; native generation and direct classification are not substituted for one another.

## 6. Secondary policies and execution

Only after representation specificity is tested compare source-selected best single, strong static predictive fusion and optional fixed-arm acquisition routing. Hard headroom does not guarantee superiority over fusion. Unknown target drift remains a sensitivity parameter. A bounded-loss iid certificate is not applied to raw Energy Score or correlated utterances/time windows.

`run_native_pilot.py` preserves the original two-arm default; `--arms B1_aux M head_affine` explicitly runs the new comparison on supplied genuine frozen exports. Its native CI test uses four synthetic fixture events per split and one optimizer update: an integration test, not learned task evidence. CSV plots require an explicit reference/candidate when multiple arms exist; no unmentioned rows vanish.

The Japanese Vowels real reader/reference remains mean-LPC/closed-form ridge, with restored coefficients and the original test set. It is not HSE, a moment model or calibrated probability prediction. Four other external raw converters and genuine multi-domain HSE/reference checkpoints remain missing prerequisites. TII remains industrial-only through PHMFactory, with all code shared rather than copied.

## Fixed-prediction stopping check

Before fitting a classification selector for already evaluated fixed predictors, check whether their unique argmax decisions differ on the saved examples. Complete strict agreement eliminates classification-label improvement by hard selection or convex score fusion on those examples. It does not eliminate probability/score improvement or the value of a new/retrained model. The current affine reference bank satisfies this condition; no classifier gate is trained for that bank. The strong same-head control remains `head_affine` in the existing implementation; no parallel A_raw arm is introduced.
