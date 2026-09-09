# Theory 3 — Gaussian information order and general posterior coarsening

## Status

The original Gaussian covariance theorem is retained. The general statement is an averaged posterior relation under a declared degradation channel, not eventwise variance monotonicity. The same-stem Notebook checks both boundaries.

## 1. Gaussian acquisition-design order

Under the same positive-definite Gaussian prior and known linear-Gaussian acquisitions,

\[
J_H\succeq J_L\quad\Longrightarrow\quad\Sigma_H\preceq\Sigma_L.
\]

The order is in acquisition information, not nominal sampling rate.

### Lemma 3.1 — inversion reverses positive-definite order

If `B >= A > 0` in Loewner order, let `C=A^{-1/2} B A^{-1/2}`. Then `C >= I`; diagonalizing `C` shows `C^{-1} <= I`. Congruence by `A^{-1/2}` gives `B^{-1} <= A^{-1}`. ∎

### Theorem 3.1 — Gaussian posterior covariance order

\[
\boxed{
\Sigma_H=(\Sigma_0^{-1}+J_H)^{-1}
\preceq(\Sigma_0^{-1}+J_L)^{-1}=\Sigma_L.
}
\]

**Proof.** Adding the common positive-definite prior precision preserves information order. Apply Lemma 3.1. ∎

Every directional variance obeys `u^T Sigma_H u <= u^T Sigma_L u`. Congruence and eigenvalue ordering also give `det(Sigma_H) <= det(Sigma_L)`, hence ordered Gaussian differential entropies. Here posterior covariance does not depend on the realized observation; that fact is specific to this correctly specified Gaussian model.

## 2. General acquisitions related by a degradation channel

Assume, conditionally on any common declared side information,

\[
\Theta\longrightarrow O_H\longrightarrow O_L
\]

is a Markov chain. For example, `O_L` may be a declared random degradation of the same noisy `O_H`. Separate measurements that only share a clean latent event do not automatically form this chain.

### Lemma 3.2 — posterior tower relation

For every bounded measurable `f`,

\[
\boxed{
\mathbb E[f(\Theta)\mid O_L]
=\mathbb E[\mathbb E[f(\Theta)\mid O_H]\mid O_L].
}
\]

**Proof.** First condition `f(Theta)` on `(O_H,O_L)`, then on `O_L`. The Markov assumption makes the inner expectation equal to `E[f(Theta)|O_H]`; the tower property yields the formula. ∎

Equivalently, in the sense of integrals against test functions,

\[
p(\Theta\mid O_L)=\mathbb E[p(\Theta\mid O_H)\mid O_L].
\]

It does not require equality of the two posteriors of an individual paired observation.

### Theorem 3.2 — conditional covariance decomposition

With finite second moments and `mu_H=E[Theta | O_H]`,

\[
\boxed{
\operatorname{Cov}(\Theta\mid O_L)
=\mathbb E[\operatorname{Cov}(\Theta\mid O_H)\mid O_L]
+\operatorname{Cov}(\mu_H\mid O_L).
}
\]

**Proof.** Write `Theta-mu_L=(Theta-mu_H)+(mu_H-mu_L)`, where the tower relation gives `mu_L=E[mu_H|O_L]`. Expand the conditional outer product. Conditional on `(O_H,O_L)`, the first residual has mean zero by the Markov property, so both cross terms vanish. The remaining terms are the two covariances displayed above. ∎

The final term is positive semidefinite. Thus the low-information covariance dominates the **conditional average** high-information covariance, not every realized high-information covariance.

## 3. Counterexample to eventwise variance decrease

Let `Theta` take `-1,0,1` with probabilities `0.05,0.90,0.05`. Let `O_L` be constant and `O_H=abs(Theta)`. Then

\[
\operatorname{Var}(\Theta\mid O_L)=0.1,\qquad
\operatorname{Var}(\Theta\mid O_H=1)=1.
\]

The more informative observation increases variance for that outcome. Averaging over `O_H` gives `0.1`, consistent with Theorem 3.2. No Gaussian theorem is contradicted.

## 4. Same-source noise must not be counted twice

For `Theta~N(0,1)` and `x=Theta+epsilon`, `epsilon~N(0,1)`, the posterior variance is `1/2`. Appending the identical `x` gives no new information. Incorrectly treating it as an independent second observation yields `1/3`. A resampled view of one noisy recording therefore needs a joint noise model before its likelihood can be multiplied with the original.

## 5. Experimental implications and limits

Keep the Loewner test in Gaussian cells. For non-Gaussian cells use proper scores, condition-specific calibration and the posterior tower relation when the degradation channel is justified. Do not add an unconditional eventwise variance-order penalty.

Acquisition information order alone is not a calibration test: a prior-only predictor can be insensitive to all observations. Use observation-dependent prediction checks as well. A finite discrete counterexample does not quantify any specific hardware anti-alias filter.

This file supplies standard supporting probability results and a falsifying control, not a new calibration method or an empirical contribution.
