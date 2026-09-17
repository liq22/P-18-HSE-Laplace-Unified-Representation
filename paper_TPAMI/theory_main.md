# Representation specificity before policy selection

## Scope and notation

Fix the source-trained encoder, target, preprocessing and conditional-moment checkpoint. R is the complete ordinary code; M=T(R) is its deterministic message. Both consumers receive identical side information. X includes the noisy target, diffusion time, acquisition descriptor A and common masks/side fields. Population expectations condition on the training result and integrate over new evaluation groups and declared noise. A finite empirical risk carries a hat. A native batch-normalized objective is not silently replaced by an unweighted population identity.

The arguments below use classical function-class inclusion, coordinate changes, conditional projection and fixed-expert selection. V-information [@xu2020usable] and multi-expert deferral [@mao2024regression; @mao2025routing] are direct antecedents. These are falsification tools for the specific message, not a new general information theory. Independent-policy certification remains secondary in `theory/policy_certificate.md`; no additional theorem file is needed.

## Representation-specific checks for the implemented head

### Consumer inclusion

Let F_R contain every composition f(X,T(R)) for f in F_M. Under the same evaluation law, loss and admissible budget,

$$
\inf_{g\in\mathcal F_R}\mathbb E\ell(Y,g(X,R))
\le \inf_{f\in\mathcal F_M}\mathbb E\ell(Y,f(X,M)).
$$

**Proof.** Every candidate on the right is a candidate on the left with identical predictions. Taking infima proves the inequality; optimizer existence is unnecessary. Inclusion must also hold under the actual computation/parameter restriction. It does not mean gradient descent on R discovers T, or that installing T is free. The executable R→same frozen T→same consumer path is an identity control, not an independently trained competitor.

### The current mean readout is affine

`MatchedConditioner.moment_head` is a Linear layer. Its mean output is m(R)=W_mR+b_m. Any mean-plus-linear-tail message followed by an affine consumer is therefore an affine function of R. It cannot enlarge the original affine prediction family. A rank-deficient replacement may reduce the family.

The complete message also contains nonlinear softplus/Cholesky coordinates. Those fields must be compared with mean-only and generic nonlinear controls. The R² witness for R∈{-1,0,1} illustrates nonlinear finite-family utility, not the value of this affine mean head.

### Conditional invertibility of the complete implemented message

Let d be the supervised target dimension and s=d+d(d+1)/2. Split R=(R_p,R_t) into its first s coordinates and retained tail. The frozen head before statistical transformations is

$$
h=W_pR_p+W_tR_t+b,\qquad W_p\in\mathbb R^{s\times s}.
$$

The first d coordinates of h form m. Its remaining coordinates form a lower-triangular L, with a positive diagonal obtained from the mathematical softplus. For known λ≥0 the sent factor is C=chol(LLᵀ+λI), and the complete message is

$$
M=(m,\operatorname{vech}C,R_t).
$$

**Claim.** In exact arithmetic, with the specified injective positive-diagonal map and nonsingular W_p, M determines R. This applies to the complete M, not the tail-zeroed M0 variant.

**Constructive proof.** From the message obtain C and R_t. Since the message was constructed from L with strictly positive diagonal,

$$
L=\operatorname{chol}(CC^\top-\lambda I)
$$

is well-defined and unique. Keep the off-diagonal entries of L and apply inverse softplus log(expm1(L_ii)) to its diagonal, recovering every raw covariance coordinate of h. Together with m this recovers h. Then

$$
\boxed{R_p=W_p^{-1}(h-W_tR_t-b).}
$$

The tail was transmitted unchanged, completing the inverse. If W_p is singular, any nonzero v in its null space gives identical messages for (R_p,R_t) and (R_p+v,R_t). That demonstrates noninjectivity on the ambient code space, not necessarily loss of a particular target on a restricted data manifold. ∎

Consequently, under the full-rank ideal-map conditions, σ(X,M)=σ(X,R) and the Bayes information term Γ in Proposition1 equals zero. It is incorrect to call the current full-q message inherently lossy. A finite-consumer advantage can still be a coordinate/optimization effect. This observation does not make estimated moments statistically correct.

**Numerical boundary.** This exact proof does not guarantee bitwise inversion in float16/float32. The actual library softplus uses a thresholded numerical implementation; the finite witness checks its smooth branch rather than claiming a global inverse across all branches. Small Cholesky diagonals, subtraction of λI, quantization and a nearly singular W_p can amplify roundoff. Holding head parameters fixed,

$$
\|\widehat R_p-R_p\|_2\le
\frac{\|\widehat h-h\|_2+\|W_t\|_2\|\widehat R_t-R_t\|_2}{\sigma_{\min}(W_p)}.
$$

This follows directly by subtracting the two linear solves. It is not a global bound on the inverse-Cholesky/softplus error inside hhat; inverse-softplus derivative 1/(1-exp(-L_ii)) diverges as L_ii approaches zero. Evaluate rank, smallest singular value, preactivation range and numerical round trips on the actual selected checkpoint and message dtype. Do not add a hidden covariance repair or enforce invertibility by changing the method in this slice.

The same-stem Notebook supplies the exact-map witness; the actual Torch conditioner tests check a float64 round trip and a singular-head collision. Invertible coupling transformations have classical predecessors, notably Dinh, Sohl-Dickstein and Bengio, *Density estimation using Real NVP*, ICLR2017, Sections3.2–3.3 (https://arxiv.org/pdf/1605.08803). No new normalizing-flow principle, density model or Flow Matching component is introduced here.

### Full-dimensional coordinates and the ridge objective

Take source X∈R^(n×q), targets Y∈R^(n×k), fixed center c and nonsingular A. Set Z=(X-1cᵀ)A. Compare

$$
J_R(W,b)=n^{-1}\|Y-(X-1c^\top)W-1b^\top\|_F^2+\lambda\|W\|_F^2
$$

with

$$
J_A(V,b)=n^{-1}\|Y-ZV-1b^\top\|_F^2+\lambda\|AV\|_F^2.
$$

For λ>0 and an unpenalized intercept, predictions coincide on every evaluation input.

**Proof.** W=AV is a bijection and J_A(V,b)=J_R(AV,b), including the penalty. Ridge makes the coefficient solution unique; the intercept is determined by the residual mean. Thus W*=AV*, and predictions are equal for every x. ∎

An unchanged transformed penalty λ||V||² corresponds to λ||A^-1W||² in raw coordinates. This is the ordinary isotropic penalty for orthogonal A, but not for general whitening. Full-q PCA/random rotations are exact isotropic-ridge controls; whitening requires both penalties. Source covariance must be full rank in the present experiment. Truncation, flooring, different λ or unequal optimization budgets define separate problems.

The Notebook and `affine_controls.py` implement these statements. The real Japanese Vowels reference fits source-only full-q coordinates with untouched official test utterances. It is not an HSE or conditional-moment experiment.

## Proposition 1 — nested-message finite-risk decomposition

Assume E||V||²<∞. Put f_R=E[V|X,R], f_M=E[V|X,M] and define square-integrable fitted consumers d_j with

$$
\Gamma(a)=\mathbb E[\|f_R-f_M\|^2\mid A=a],\qquad
\mathcal E_j(a)=\mathbb E[\|d_j-f_j\|^2\mid A=a].
$$

For almost every a,

$$
\rho_M(a)-\rho_R(a)=\Gamma(a)+\mathcal E_M(a)-\mathcal E_R(a),\quad\Gamma(a)\ge0.
$$

**Proof.** M=T(R) gives nested conditional sigma-algebras. Expand V-f_M=(V-f_R)+(f_R-f_M), then V-d_j=(V-f_j)+(f_j-d_j). The conditional cross terms vanish by the tower property. A is in X, permitting acquisition-conditional subtraction. ∎

This generic identity does not favor statistical T. Under the complete-message rank conditions above Γ=0; under a lossy map M must reduce finite-consumer error by more than Γ. Neither case is a macro-F1, Energy Score or finite reverse-sampler guarantee.

## Fixed-policy interpretation (secondary)

For fixed trained arms j, ρ_j(a)=E[ℓ_j|A=a], R_j=E_πρ_j(A). Loss and acquisition weighting π are declared; balanced and prevalence-weighted conditions differ. Macro-F1 is not an additive event loss.

### Proposition 2 — hard-selection opportunity

$$
\mathcal H_{hard}=\min_j\mathbb E_\pi\rho_j(A)-\mathbb E_\pi\min_j\rho_j(A)\ge0.
$$

For finitely many arms it is zero iff a globally optimal arm is conditionwise optimal almost surely, ties allowed.

**Proof.** The pointwise minimum is no larger than each fixed arm. Integrate and minimize. Equality means the nonnegative conditional gap of a global minimizer has zero expectation, hence is zero almost surely. The converse is immediate. ∎

This is not a fusion theorem. Equally likely targets .25/.40 and fixed predictions0/1 make the zero predictor best in each condition, so hard headroom is zero. Static weight .325 nevertheless reduces MSE from .11125 to .005625; a condition-dependent weight gives zero in this example. Predictive distributions must be mixed as distributions, not by averaging arbitrary generated trajectories.

### Proposition 3 — transport sensitivity

Assume uniformly over arms on target support,

$$
|\widehat\rho_j^s(a)-\rho_j^s(a)|\le\epsilon(a),\quad
|\rho_j^s(a)-\rho_j^t(a)|\le b(a).
$$

With e=ε+b and source argmin selector jhat,

$$
\mathcal R_t(\widehat j)-\mathcal R_t(j_t^*)\le2\mathbb E_\pi e(A),\quad
|\widehat{\mathcal H}_{s,\pi}-\mathcal H_{t,\pi}|\le2\mathbb E_\pi e(A).
$$

**Proof.** Estimated source risks differ from target by at most e. Add/subtract estimated risks for the selected and target-optimal arms; the estimated difference is nonpositive, leaving2e. Integrate. The finite minimum is1-Lipschitz in sup norm; applying it to global and conditional minima gives the second bound. ∎

With declared additional selector cost λc_g, its gain over target-best fixed risk is at least Hhat_s,π-4E_πe-λE_πc_g. Arm-dependent costs belong inside arm risks. Unknown b is a sensitivity parameter, not a computable deployment guarantee from unlabeled target data. Post-hoc target evaluation never selects a zero-shot gate.

## Validation and claims

Fit transformations, targets, checkpoints, loss weights and tuning budgets on source data only. Use disjoint original groups for calibration; noisy selection-sample minima do not establish population headroom. Formal statistics use common predeclared seeds. The official LPC/ridge reference is not genuine learned R/M evidence. Strong simple controls, actual checkpoint rank/precision and direct task heads precede any diffusion or routing necessity claim. Classical projection, invertibility and calibration results do not alone establish TPAMI novelty; TII industrial findings are not counted twice.
