# Applied analysis of the industrial conditioner

The full coordinate/inverse proofs and their numerical witnesses are in `../paper_TPAMI/theory_main.md` and its Notebook; they are shared supporting analysis, not independent discoveries in both papers. TII retains the consequences needed by its actual diagnostic experiment.

## Defined variables and interpretation

Freeze HSE, reference target, preprocessing and the source-selected shared trunk/head. X includes acquisition A, native noisy target/time and all common consumed side information. R is the complete code, h=WR+b the raw head, H_A=(h,R_tail) the same-head affine control, and M=Φ(H_A) its statistical-coordinate version.

An affine consumer after H_A is affine in R by composition. M and H_A determine one another on the exact attainable image of the mathematical softplus/Cholesky map, with known covariance floor. Recover C from M, obtain L=chol(CCᵀ−λI), invert diagonal softplus, and recover h; the tail is unchanged. No rank condition on W is needed for this H_A/M equivalence. Recovering all R additionally requires a nonsingular replaced-coordinate block W_p. These facts do not assure statistical calibration or floating-point inversion.

## Finite square-risk decomposition

For a common square-integrable native target V, let f_R=E[V|X,R], f_M=E[V|X,M], and fixed fitted consumers d_j. Then for almost every acquisition condition,

$$
\rho_M(a)-\rho_R(a)
=\mathbb E[\|f_R-f_M\|^2\mid A=a]+\mathcal E_M(a)-\mathcal E_R(a).
$$

**Proof.** The conditional information sets are nested because M is deterministic in R. Expand V−f_M into V−f_R plus f_R−f_M; conditional orthogonality removes the cross term. Expand V−d_j about f_j similarly and subtract. A belongs to X, so the conditional argument applies at each supported acquisition stratum. ∎

In the exact full-rank case M/R has zero Bayes penalty. M/H_A has zero penalty on its exact attainable image regardless of W_p rank. Its finite-consumer difference then reflects approximation, optimization or regularization rather than new observations. An unmatched native batch-normalized objective needs its actual weighting, not an unweighted substitution.

## What the analysis does not claim

This is not a macro-F1, Energy Score, finite reverse-sampling or target-calibration guarantee. A conditional-moment score identifies only the declared moments at a population optimum under its model assumptions; finite optimization and partial observations remain empirical. Direct industrial heads and strong generic reparameterizations, not additional routing theory, determine the method's value. Mathematical witnesses remain supporting tests; TII empirical datasets are industrial only.
