# Representation specificity before policy selection

## Scope and notation

Fix the source-trained encoder, target, preprocessing and conditional-moment checkpoint. R is the complete ordinary code and M=T(R) its deterministic message. Both consumers receive identical side information. X includes the noisy target, diffusion time, acquisition descriptor A and common masks/side fields. Population expectations condition on the training result and integrate over new evaluation groups and declared noise. Empirical risk carries a hat. A native batch-normalized objective is not replaced by an unweighted population identity.

The arguments use classical function-class inclusion, coordinate changes, conditional projection and fixed-expert selection. V-information and multi-expert deferral are direct antecedents [@xu2020usable; @mao2024regression; @mao2025routing]. These are falsification tools for the implemented message, not a new information theory. Independent-policy certification remains secondary in `theory/policy_certificate.md`.

## 1. Consumer inclusion

If the R-consumer family contains every f(X,T(R)) with f in the M-consumer family under the same admissible computation budget,

$$
\inf_{g\in\mathcal F_R}\mathbb E\ell(Y,g(X,R))
\le\inf_{f\in\mathcal F_M}\mathbb E\ell(Y,f(X,M)).
$$

**Proof.** Every candidate on the right is a candidate on the left with identical predictions. Taking infima proves the inequality; optimizer existence is unnecessary. ∎

This does not guarantee that gradient descent on R learns T, or that installing T is free. R→the same frozen T→the same consumer is an exact implementation control, not an independently trained competitor.

## 2. The implemented mean head and a same-head affine control

`MatchedConditioner.moment_head` is Linear. With d target coordinates and s=d+d(d+1)/2, split R=(R_p,R_t), where R_p contains s replaced coordinates. The raw head is

$$
h=W_pR_p+W_tR_t+b,\qquad W_p\in\mathbb R^{s\times s}.
$$

Its first d coordinates are the mean. The others parameterize a lower-triangular L with softplus diagonal. M sends the mean, C=chol(LLᵀ+λI), and the unchanged R_t.

A mean-only replacement followed by an affine consumer is affine in R. It cannot enlarge the original affine family; a rank-deficient replacement may reduce it. The R² finite witness does not establish a benefit for this affine mean head.

### Proposition — exact factorization through the same trained raw head

Define the implemented control

$$
\boxed{H_A=(h,R_t)=A_*R+b_*,\quad
A_*=\begin{bmatrix}W_p&W_t\\0&I\end{bmatrix},\quad b_*=(b,0).}
$$

For a fixed head, M=Φ(H_A), where Φ changes only raw covariance coordinates into the sent Cholesky coordinates. In exact arithmetic with the injective mathematical softplus and known λ≥0, Φ has an inverse on its attainable image. Thus

$$
\sigma(X,H_A)=\sigma(X,M),
$$

**even if W_p is singular**. Nonsingular W_p is needed to recover R, not to equate H_A and M.

**Proof.** M gives C and the preserved mean/tail. The construction ensures CCᵀ−λI=LLᵀ with positive-definite LLᵀ. Its unique Cholesky factor is L. Keep off-diagonal coordinates and invert each diagonal softplus by log(expm1(L_ii)); this recovers the raw covariance coordinates of h. The remaining coordinates were transmitted unchanged. Forward and inverse maps are measurable on this image. ∎

For any affine consumer B H_A+c, substitution gives (BA_*)R+Bb_*+c. Hence the same-head control cannot enlarge the affine family of R. If A_* is invertible, an unchanged isotropic ridge penalty on B nevertheless changes the regularizer in R-coordinates; equal functions do not by themselves match optimization or regularization.

This control uses the **same statistical supervision, selected trunk/head weights, q and dtype** as M. It avoids additional training or a detached auxiliary branch. Raw covariance coordinates are not covariance estimates. M versus H_A isolates the effect of the nonlinear statistical coordinate map under the chosen finite consumer; its Cholesky/softplus cost remains chargeable. It does not eliminate the need for generic learned-MLP and whitening controls.

## 3. Complete-message invertibility and numerical boundary

If W_p is nonsingular, the recovered h and transmitted R_t also give

$$
R_p=W_p^{-1}(h-W_tR_t-b).
$$

Therefore M determines all R and the Bayes information penalty Γ below equals zero. Calling every full-q M inherently lossy is incorrect. If W_p is singular, a nonzero null vector v makes (R_p,R_t) and (R_p+v,R_t) collide. This is noninjectivity in the ambient code space, not proof of target information loss on the actual data manifold.

Exact invertibility does not establish float16/float32 reversibility. The actual softplus implementation uses a thresholded numerical branch; existing finite witnesses check the smooth branch. Small Cholesky diagonals, subtracting λI, quantization and a nearly singular W_p can amplify roundoff. Holding parameters fixed,

$$
\|\widehat R_p-R_p\|_2\le
\frac{\|\widehat h-h\|_2+\|W_t\|_2\|\widehat R_t-R_t\|_2}{\sigma_{\min}(W_p)}.
$$

This follows by subtracting the linear solves. It is not a global bound on inverse-Cholesky/softplus error. Inverse-softplus derivative 1/(1−exp(−L_ii)) diverges as L_ii approaches zero. Measure rank, smallest singular value, range and numerical round trips at the actual selected checkpoint and message dtype; do not silently repair covariance or modify training to force invertibility.

Real NVP [Dinh et al., ICLR2017, Sections3.2–3.3; https://arxiv.org/pdf/1605.08803] is an explicit predecessor for invertible partial-coordinate transformations. The argument here identifies the already implemented map; it does not introduce normalizing-flow density training or Flow Matching. The same-stem Notebook retains exact-map and singular examples; Torch tests additionally exercise the real code and H_A-to-M reconstruction.

## 4. Full-dimensional coordinates and the ridge objective

For source X∈R^(n×q), targets Y∈R^(n×k), a fixed center c and nonsingular A, set Z=(X−1cᵀ)A. Compare

$$
J_R(W,b)=n^{-1}\|Y-(X-1c^\top)W-1b^\top\|_F^2+\lambda\|W\|_F^2
$$

with

$$
J_A(V,b)=n^{-1}\|Y-ZV-1b^\top\|_F^2+\lambda\|AV\|_F^2.
$$

For λ>0 and an unpenalized intercept, predictions coincide for every evaluation input.

**Proof.** W=AV is a bijection and J_A(V,b)=J_R(AV,b). Ridge gives a unique coefficient solution and the residual mean fixes the intercept. Hence W*=AV*, implying identical predictions. ∎

An unchanged transformed penalty λ||V||² corresponds to λ||A^-1W||² in original coordinates. It is unchanged for orthogonal A, not for general whitening. Full-q PCA/rotations therefore supply exact isotropic-ridge controls; whitening needs both penalties. Truncation, floors, a changed λ or unequal optimization budgets define different problems. The official Japanese Vowels experiment checks this on source-only mean-LPC features, not HSE.

## 5. Nested-message finite-risk decomposition

Assume E||V||²<∞ and set f_R=E[V|X,R], f_M=E[V|X,M]. For fixed square-integrable consumers,

$$
\Gamma(a)=\mathbb E[\|f_R-f_M\|^2\mid A=a],\quad
\mathcal E_j(a)=\mathbb E[\|d_j-f_j\|^2\mid A=a],
$$

$$
\rho_M(a)-\rho_R(a)=\Gamma(a)+\mathcal E_M(a)-\mathcal E_R(a),\qquad \Gamma(a)\ge0.
$$

**Proof.** Nested conditional sigma-algebras follow from M=T(R). Expand V−f_M=(V−f_R)+(f_R−f_M), and V−d_j=(V−f_j)+(f_j−d_j). Their conditional cross terms vanish. Including A in X permits acquisition-conditional subtraction. ∎

Under complete-message full-rank conditions Γ=0. For H_A versus M, the exact-image bijection likewise yields zero information penalty without requiring W_p nonsingular. Any finite-consumer difference is then an approximation/optimization/regularization effect. These identities are not macro-F1, Energy Score or finite reverse-sampler guarantees.

## 6. Fixed-policy analysis is secondary

For fixed trained arms define ρ_j(a)=E[ℓ_j|A=a] and R_j=E_πρ_j(A), with common loss and declared acquisition weighting π. Macro-F1 is not an additive event loss.

### Hard-selection opportunity

$$
\mathcal H_{hard}=\min_j\mathbb E_\pi\rho_j(A)-\mathbb E_\pi\min_j\rho_j(A)\ge0.
$$

For finitely many arms equality holds iff a globally optimal arm is conditionwise optimal almost surely, ties allowed.

**Proof.** The pointwise minimum is no larger than any arm. Integrate and minimize. Equality means a global minimizer's nonnegative gap has zero expectation, hence vanishes almost surely. The converse is immediate. ∎

This is not a fusion theorem. Equally likely targets .25/.40 and predictions0/1 make the zero predictor conditionwise best, giving zero hard headroom. Static weight .325 still reduces MSE from .11125 to .005625; a conditional soft weight gives zero in this constructed example. Predictive distributions must be mixed as distributions, not by averaging arbitrary generated trajectories.

### Transport sensitivity, not an observable deployment guarantee

Assume uniformly over arms on target support,

$$
|\widehat\rho_j^s(a)-\rho_j^s(a)|\le\epsilon(a),\quad
|\rho_j^s(a)-\rho_j^t(a)|\le b(a).
$$

With e=ε+b and the source argmin selector,

$$
\mathcal R_t(\widehat j)-\mathcal R_t(j_t^*)\le2\mathbb E_\pi e(A),\quad
|\widehat{\mathcal H}_{s,\pi}-\mathcal H_{t,\pi}|\le2\mathbb E_\pi e(A).
$$

**Proof.** The triangle inequality gives error e between estimated and target risks. Add/subtract selected and optimal estimated risks; the selection term is nonpositive, leaving2e. Integrate. Apply the1-Lipschitz property of a finite minimum to global and conditional minima for the second inequality. ∎

Additional fixed-priced selector cost λc_g gives the sensitivity lower bound Hhat_s,π−4E_πe−λE_πc_g against target-best fixed risk. Unknown b remains an assumption; target labels cannot select a nominally zero-shot gate.

## Verification and originality

Freeze target, transforms, score/weight rules and checkpoints using source groups. Preserve a common declared seed set. Test changes do not modify source selection. The real LPC/ridge reference and native synthetic loop are not genuine HSE method results. Strong simple controls, actual numerical diagnostics and direct task heads precede a Diffusion/routing necessity claim. Classical projection, affine invertibility and calibration results alone do not establish TPAMI novelty or a second independent TII contribution.

## Finite prediction agreement before fitting a classifier selector

For one fixed evaluation example x, let s_j(x) be the saved C-class scores of J fixed predictors. Suppose they all have the same unique winning class c. For any nonnegative weights summing to one, even if those weights depend on x,

$$
\sum_j w_j(x)s_{j,c}(x)-\sum_j w_j(x)s_{j,k}(x)
=\sum_jw_j(x)[s_{j,c}(x)-s_{j,k}(x)]>0,\qquad k\ne c.
$$

Thus the mixture still predicts c. Hard selection is a vertex of that simplex. If the premise holds on every stored example, any such selector or convex score mixture has the same confusion matrix, accuracy and macro-F1 on these examples. This elementary convexity implication is a stopping check, not a new routing theorem or population performance certificate.

The actual calculation checks the minimum common-label margin over all models and competing classes. A zero margin is a tie, not strict agreement; it is not discarded with an arbitrary tolerance. The claim excludes negative/class-specific weights, changed scores, new experts, different thresholds and retrained fusion. It also does not imply identical score MSE, calibration or probabilistic utility. Saved ridge scores are not normalized probabilities and their onehot MSE is not reported as Brier loss.

`prediction_agreement.py` replays the complete saved prediction bank. A separate two-score mixture fits its single weight on source validation only, then evaluates reserved calibration/test. Since original test results were already public, this is exploratory post-hoc re-analysis, not an independently preregistered confirmation. The same-stem Notebook carries the finite convexity witness; the real CSV replay supports only the observed score-bank conclusion. No new HSE, conditional-moment or industrial performance is inferred.
