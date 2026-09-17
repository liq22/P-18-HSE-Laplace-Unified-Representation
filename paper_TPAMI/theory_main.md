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

**Proof.** Each candidate on the right is, by the stated inclusion, a candidate on the left with exactly the same predictions. Taking infima proves the inequality. No existence of an optimizer is required. The inclusion must also hold under the actual parameter/computation restriction; installing T inside the R path is not cost-free. This is a population function-class comparison, not an assertion that gradient descent on R discovers T.

The executable identity control is R → the **same frozen** T → the same consumer. Its output must equal the M path. An independently trained MLP is a competing finite method, not this identity control.

### The current mean readout is affine

In `MatchedConditioner`, `moment_head` is a single Linear layer. Its mean output therefore has the form m(R)=W_m R+b_m. Appending that mean to a linear tail produces an affine map of R. Any subsequent affine classifier/regressor is consequently an affine function of R. A mean-only message cannot enlarge the unrestricted affine-consumer family of R; if the replacement is rank-deficient it can make the family smaller.

The actual M also includes softplus/Cholesky-derived covariance fields, so the whole map is not generally affine. Any method-specific claim must isolate those nonlinear fields from a mean-only control and a similarly sized generic nonlinear reparameterization. The nonlinear square-target witness R∈{-1,0,1}, T(R)=R² illustrates a possible finite-family benefit, but it does **not** explain this affine mean head by itself.

### Full-dimensional coordinates and the ridge objective

Take source X∈R^(n×q), targets Y∈R^(n×k), fixed center c and nonsingular A∈R^(q×q). Set Z=(X-1cᵀ)A. Consider

$$
J_R(W,b)=n^{-1}\|Y-(X-1c^\top)W-1b^\top\|_F^2+\lambda\|W\|_F^2,
$$

and the transformed problem

$$
J_A(V,b)=n^{-1}\|Y-ZV-1b^\top\|_F^2+\lambda\|AV\|_F^2.
$$

For λ>0 and an unpenalized intercept, the solutions make identical predictions on every source or new input.

**Proof.** W=AV is a bijection because A is nonsingular. Substitution gives J_A(V,b)=J_R(AV,b), including the penalty. The positive ridge term makes the coefficient solution unique; the intercept is fixed by centering the residual. Thus W*=AV*, and for every x, (x-c)ᵀW*+b*=(x-c)ᵀAV*+b*. This is an exact objective equivalence, not a statement about finite-precision solver error. ∎

With isotropic transformed penalty λ||V||² instead, the equivalent penalty in raw coordinates is λ||A^-1 W||². It agrees with ordinary ridge for an orthogonal A, but not for a general whitening transform. Therefore full-q PCA and random orthogonal coordinates are exact isotropic-ridge controls; whitening must be reported with both unchanged and transported penalties. Source covariance must be full rank for the present whitening experiment. Truncated PCA, covariance flooring, different λ or unequal training updates change the problem and are separately declared variants, not hidden repairs.

The same-stem Notebook and `affine_controls.py` execute this identity. The real Japanese Vowels reference uses source-fitted full-q coordinates and untouched official test utterances. It does not use HSE features or prove a conditional-moment advantage.

## Proposition 1 — nested-message finite-risk decomposition

Assume E||V||²<∞ for one common target. Put f_R=E[V|X,R], f_M=E[V|X,M]. For square-integrable fitted consumers d_j define

$$
\Gamma(a)=\mathbb E[\|f_R-f_M\|^2\mid A=a],\qquad
\mathcal E_j(a)=\mathbb E[\|d_j-f_j\|^2\mid A=a].
$$

For almost every a,

$$
\rho_M(a)-\rho_R(a)=\Gamma(a)+\mathcal E_M(a)-\mathcal E_R(a),\qquad\Gamma(a)\ge0.
$$

**Proof.** Since M=T(R), σ(X,M)⊂σ(X,R). Expand V-f_M=(V-f_R)+(f_R-f_M). Conditional expectation of the cross term vanishes by the tower property. Do the same with V-d_j=(V-f_j)+(f_j-d_j), then subtract. A is included in X so the identities can be conditioned on the acquisition stratum. ∎

M gains only if its finite-consumer error reduction exceeds Γ. This identity applies to every deterministic T, not only a statistical message. It is not a macro-F1, Energy Score, arbitrary-domain-calibration or finite-reverse-sampler guarantee.

## Fixed-policy interpretation (secondary)

For fixed trained arms j let ρ_j(a)=E[ℓ_j|A=a], R_j=E_πρ_j(A). The common integrable loss and acquisition weighting π are declared; balanced conditions and deployment prevalence define different estimands. Macro-F1 is not an additive event loss for fitting the rule.

### Proposition 2 — hard-selection opportunity

$$
\mathcal H_{hard}=\min_j\mathbb E_\pi\rho_j(A)-\mathbb E_\pi\min_j\rho_j(A)\ge0.
$$

For finitely many arms it is zero iff a globally optimal arm is conditionwise optimal almost surely, ties allowed.

**Proof.** The pointwise minimum is no larger than each fixed arm. Integrate and minimize. Equality means the nonnegative gap of a global minimizer has zero expectation and is therefore zero almost surely; the converse follows immediately. ∎

This is not a theorem about soft or newly trained fusion. With equally likely targets .25 and .40 and fixed predictions 0 and 1, the zero predictor is better in each condition and hard headroom is zero. Yet static fusion weight .325 reduces MSE from .11125 to .005625; a condition-dependent weight attains zero in this constructed example. Probability fusion must mix distributions; averaging arbitrary generated trajectories is not automatically a predictive mixture.

### Proposition 3 — transport sensitivity, not an observable deployment certificate

Suppose on target support, uniformly over arms,

$$
|\widehat\rho_j^s(a)-\rho_j^s(a)|\le\epsilon(a),\qquad
|\rho_j^s(a)-\rho_j^t(a)|\le b(a).
$$

For source plug-in selector jhat(a)=argmin_j ρhat_j^s(a), with a fixed tie rule and e=ε+b,

$$
\mathcal R_t(\widehat j)-\mathcal R_t(j_t^*)\le2\mathbb E_\pi e(A),\qquad
|\widehat{\mathcal H}_{s,\pi}-\mathcal H_{t,\pi}|\le2\mathbb E_\pi e(A).
$$

**Proof.** Each estimated source risk differs from target risk by at most e. Add/subtract estimated risks for selected and target-optimal arms; their estimated difference is nonpositive, leaving 2e. Integrate. The finite minimum is 1-Lipschitz in the sup norm; apply it to global and conditional minima for the second bound. ∎

With additional declared selector penalty λc_g, its gain versus the target-best fixed arm is at least Hhat_s,π-4E_πe-λE_πc_g. Arm-dependent costs belong inside the arm objective. If b is unknown, this is a sensitivity expression, not a computable target-deployment guarantee. Target-labelled evaluation may measure failure after the fact but cannot be used to fit a zero-shot gate.

## Validation and claims

Fit transformations, targets, checkpoints, loss weights and tuning budgets on source data only. Use disjoint original groups for policy calibration; a noisy empirical minimum on the selection sample is not evidence of population headroom. The current computational fixes enforce exact Gaussian input dimensions and a condition-wide common seed set; predeclared seeds detect globally missing runs.

The actual first external experiment is ordinary LPC coordinates plus a solved ridge consumer. A statistical-message result still needs real shared R/M features, exact-composition checks, PCA/whitening/orthogonal and generic learned controls, with direct task heads before attributing value to diffusion. Neither the coordinate identity nor a finite-policy certificate constitutes independent TPAMI novelty. TII industrial evidence remains in `paper/` and is not counted twice.
