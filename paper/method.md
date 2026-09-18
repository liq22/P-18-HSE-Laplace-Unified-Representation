# Industrial method and decisive controls

## 1. Primary task and frozen information

Primary task: industrial fault diagnosis; endpoint: recording-balanced pooled-confusion macro-F1. Native LLapDiff loss/latent Energy Score are secondary mechanism diagnostics. Direct linear, small-MLP and matched neural classifiers are required before claiming that Diffusion is necessary.

Use accepted PHMFactory data and original-recording splits. F=HSE_0(O,a_enc), Z0=E_ref(X_ref), U=L vec(Z0). HSE/reference encoders are source-trained and frozen. Declare L and its source selection before comparison. The actual conditioner input C_F=(F,M_F,a) retains mask, named side fields, units, deterministic evaluation patches and source-only normalization. The reference view may provide training targets, not an extra inference input for one arm. Acquisition-ID, fault-label, operating-condition and recording-shortcut probes test whether the reference target encodes the intended task rather than dataset identity.

## 2. Shared supervision and three messages

A trunk produces R∈R^q and a Linear head produces h=WR+b. Its first d coordinates give a mean; the rest form a lower-triangular factor with softplus diagonal. Let C=chol(LLᵀ+λI) with publicly declared λ. The Gaussian score updates the exact R path later consumed by B1-aux. Select one source-validation checkpoint, then freeze encoder, preprocessing, buffers, trunk and head.

With s=d+d(d+1)/2<q, the principal messages are

$$
H_R=R,\qquad H_A=[h,R_{s+1:q}],\qquad
H_M=[m,\operatorname{vech}C,R_{s+1:q}].
$$

H_A is implemented as `head_affine`: same trained head, target, checkpoint, q and dtype, no new weights or training. Its raw covariance coordinates are not moment estimates. M=Φ(H_A) differs only by the nonlinear statistical coordinates. The exact Φ inverse on its attainable image shows that M and H_A have the same information in ideal arithmetic even when the R-to-head map is rank deficient. The M/R inverse additionally needs a nonsingular replaced-coordinate head block. Actual rank and finite precision remain checkpoint diagnostics, not assumptions silently imposed by training.

## 3. Consumer and numerical checks

All outputs are dense global summaries with explicitly all-valid output masks; input masks remain consumed upstream. Statistical meaning is checked at the raw moment readout. Verify actual prefix/tail consumption and the exact R→same T→consumer path. An affine consumer after H_A can be absorbed into an affine consumer of R; mean-only likewise adds no affine capacity. Nonlinear covariance coordinates require the H_A and same-budget MLP controls, not a generic assertion of extra information.

Log the auxiliary score's logdet/Mahalanobis components, covariance eigenvalues and source/unseen residuals. Finite positive-definite output is not calibrated full-posterior evidence. Mean-MSE and beta-NLL are optional separately named loss controls; do not replace the score silently. No oracle moment RMSE is reported for real data lacking true conditional moments.

## 4. Matched downstream execution

The native pilot retains its original B1-aux/M default and offers explicit `--arms B1_aux M head_affine`. All arms share the anchor checkpoint and initialized native denoiser, target, times/noise policy, optimizer, update budget, mask and source checkpoint selection. First recompute the native loss on an actual batch. Synthetic integration tests exercise the code but do not substitute genuine HSE/reference exports.

For diagnosis use identical direct heads on each message. B1 without auxiliary supervision distinguishes auxiliary training from message structure. PCA/orthogonal/whitened R and a same-supervision small-MLP transformation test simple alternatives. Full-q whitening changes ridge regularization unless the penalty is transported; use both as named controls. Keep strongest source-selected single and static predictive fusion; add routing only after it beats these at measured cost.

## 5. Grouping, budget and claims

PHMFactory alone owns industrial readers, metadata, labels and initial splits. Derive acquisition views after grouping. File separation does not prove physical-bearing or machine independence. Pool the group-weighted confusion matrix before calculating macro-F1; do not average single-class file F1 or window F1.

Measure q, dtype/message bytes, actual feature rank/scales/condition, HSE/trunk/head/consumer parameters, training updates, latency and memory. The new native costs record q/bytes, trunk/head/denoiser parameter counts and execution timing; they do not provide unmeasured FLOPs or stable GPU latency. H_A evaluates the head but omits M's Cholesky/softplus work, which must be charged rather than declared equal. A gain only against R is insufficient; equality with H_A or a generic MLP favors the simpler explanation. No upstream PHMFactory core is changed.
