# Method: statistically anchored conditioning

## 1. Task and the information available at inference

Fix a source-trained HSE extractor and reference encoder. The history features are `F=HSE_0(O,a_enc)`; the generated target is `Z0=E_ref(X_ref)`. A source-defined linear functional `U=L vec(Z0)` supplies the moment-supervision target. The reference encoder, normalization and L are identical for all arms. A known-pole coefficient vector beta is an analytical surrogate, not automatically the reference latent or LLapDiff's predicted modal parameters.

The complete conditioner input is

\[
C_F=(F,M_F,a_{\mathrm{consumed}}).
\]

`M_F` is the history-token mask, True for observed/valid. The side vector is explicitly named and includes any timestamps, acquisition descriptors or quality fields not already represented in F. It never includes target values, target labels or arbitrary dataset IDs as shortcuts. All comparators receive the same fields. A high-rate reference is common training supervision, not extra input given only to a teacher.

The history mask is consumed before the global code is formed. Invalid entries are excluded explicitly and an empty history is rejected. The current native LLapDiff receives a dense global summary through `cond_summary`, not a patch-indexed mask; `target_mask` instead controls the supervised target loss. A global summary slot is not assigned a fictitious original patch time. No second `cond_summary_raw` stream carries an uncounted copy of the moments.

## 2. One shared supervised path

Let `q=K D` be the fixed message size. A trainable trunk produces

\[
R_\theta=g_\theta(C_F)\in\mathbb R^q.
\]

A global head reads **this same R**, not a detached or unrelated branch:

\[
(m_\psi(R),B_\psi(R)),\qquad
S_\psi(R)=B_\psi(R)B_\psi(R)^T+\lambda I.
\]

The lower-triangular B has softplus diagonal. The public setting `covariance_floor=lambda` is a model constraint in the squared units of the source-standardized target. It is not silent covariance repair. The implementation refactorizes S before packing its Cholesky factor.

Stage one minimizes

\[
\mathcal L_G=\frac12\mathbb E_s\left[
\log\det S_\psi(R_\theta)
+(U-m_\psi(R_\theta))^T S_\psi(R_\theta)^{-1}(U-m_\psi(R_\theta))\right].
\]

Both theta and psi receive the score gradient. A one-batch check verifies a nonzero gradient in the trunk and an actual change in the ordinary code later used by B1-aux. A detached-head counterexample is retained as a negative test.

For a **fixed** R, unrestricted scoring identifies `E_s[U|R]` and `Cov_s(U|R)` when the conditional covariance is positive definite and the constraint is inactive. This does not prove that joint trunk training finds a globally sufficient R or that finite optimization attains the conditional moments. With a positive covariance floor, the constrained population optimum clips covariance eigenvalues at that floor; a strictly positive-factor implementation can approach the boundary without attaining it. Theory 12 gives the assumptions and proof.

Save source training/validation score, log determinant, Mahalanobis term, minimum covariance eigenvalue and fraction near the floor. Select a single source-validation checkpoint. Constant-Gaussian and ridge-mean/homoskedastic controls use the same source data. Oracle moment RMSE is reported only when such oracle moments actually exist.

## 3. Freeze once; compare two messages from the same checkpoint

After stage one, freeze HSE, source preprocessing, the trunk and moment head. Set evaluation mode and fix patch selection; do not update dropout/normalization state. Freezing only the final head while changing its inputs is not the proposed method. The source-trained reference encoder and target definition remain fixed.

For d-dimensional U, the statistical prefix costs `s=d+d(d+1)/2` scalars. Define

\[
H_{B1\text{-aux}}=R,\qquad
H_M=[m(R),\operatorname{vech}(\operatorname{chol}S(R)),R_{s+1:q}].
\]

The same checkpoint defines both messages. For `K=4,D=8,d=2`, each message has 32 scalars; M has five statistical and 27 ordinary coordinates. B1-aux receives all 32 ordinary coordinates trained through the auxiliary score. It is not a control with a supervised but unused side branch. M0 uses the same prefix and a zero tail only as a later ablation.

Both frozen message functions are evaluated before the same LLapDiff architecture. Stage two trains only the denoiser, with matched initialization, batches, perturbation noise, time sampling, update count and source-validation selection. The primary small pilot uses v-prediction, uniform nonzero training times and no weighting; other loss conventions are acceptance controls, not additional full training arms.

## 4. What a gain over B1-aux would mean

At the selected checkpoint, `H_M=T(R)` is deterministic. Thus

\[
I(Z_0;H_M)\leq I(Z_0;R),
\]

with common side inputs conditioned on when present. M cannot add Bayes information relative to this particular comparator. For a square-integrable native regression target V and common noisy latent/time input X, define the conditional means `f_R=E[V|X,R]` and `f_M=E[V|X,H_M]`. Then

\[
\mathcal R^*_M-\mathcal R^*_R=\mathbb E\|f_R-f_M\|^2\geq0.
\]

For fitted predictors, write their excess errors as `A_M` and `A_R`. The same projection argument gives

\[
\boxed{\mathcal R_M-\mathcal R_R=
\underbrace{\mathbb E\|f_R-f_M\|^2}_{\text{possible information loss}}
+\underbrace{A_M-A_R}_{\text{finite fitting/accessibility difference}}.}
\]

A finite-model improvement requires a reduction in fitting/accessibility error larger than any additional Bayes loss. This is the interpretation of the deliberately nested control, not a universal comparison between independently learned same-budget compressors. No mutual information is inferred merely from a loss curve.

Correct moments are not generally sufficient for non-Gaussian generation. The ordinary tail may preserve useful shape, but it also sacrifices prefix coordinates. Same-moment distinct-shape controls and oracle-moment replacement remain necessary: estimation error can itself encode observation identity.

## 5. Native loss and actual consumption

Use the installed original LLapDiff and `diffusion_loss`; do not replace them with an analytical denoiser. On the same batch, retain actual t, noisy targets, sampled noise, mask, prediction type, raw per-sample error, raw/effective weights and final scalar loss. Independently reconstruct the loss and compare all terms, not only the final scalar.

For batch-normalized weights, normalize with that batch's realized denominator. In general

\[
\mathbb E\left[\frac{\sum_i w_i D_i}{\sum_i w_i}\right]
\ne\frac{\mathbb E[wD]}{\mathbb E[w]}.
\]

The schedule CSV exporter describes an explicit uniform-time, non-batch measure; it is not a replacement for batch-level loss reconstruction. Randomly initialized native forward/update checks establish execution only.

At fixed noisy input and time, perturb the prefix and tail separately and confirm that the original model output changes. Also compare the frozen conditioner state before and after a denoiser update. Statistical units are assessed at the raw readout; subsequent learned projection/normalization is allowed.

## 6. Source, target and cost boundaries

Training and validation use source acquisition conditions only. Report source holdout and unseen acquisition scores separately, without refitting the moment head or normalization. Frozen source moments do not imply target calibration. Original recording/event groups must be split before windowing or constructing views; checking exported strings alone cannot establish their provenance.

Equal q is an interface constraint, not a complete compute match. Charge source supervision, all conditioner parameters, one-time extraction/anchor training, per-event message construction, denoiser training and repeated sampling separately. Fixed point count and fixed physical duration are different protocols. Independent measurements and resampled views of one noisy recording require different joint-noise models.

Paper modules consume exported arrays through the declared interface. They neither import PHMFactory internals nor change submodule revisions. The original LLapDiff is installed in a separate checkout. Flow Matching stays future work.
