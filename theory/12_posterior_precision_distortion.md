# Theory 12 — Posterior distortion from a budgeted information header

## Status and role

A finite-dimensional Gaussian calculation, independently checked against the ordinary Gaussian KL formula. This is a supporting analysis for a specific conditioner, not a claim that Gaussian perturbation theory is new. The learned HSE and LLapDiff are outside the exact theorem. See Spantini et al. (2015), DOI 10.1137/140977308, for prior work on optimal posterior approximations.

## 1. Assumptions and actual information

Let the fixed-pole coefficient vector be beta in R^m. The full posterior has natural parameters `(Lambda,eta)` and the approximation has `(Q,eta_q)`, with both precision matrices real symmetric positive definite. They use the same latent coordinates and base measure. Their means and covariances are

$$p=N(\mu,\Lambda^{-1}),\quad\mu=\Lambda^{-1}\eta,
\qquad q=N(\widetilde\mu,Q^{-1}),\quad\widetilde\mu=Q^{-1}\eta_q.$$

The approximation must be measurable with respect to the actual transmitted header and decoder side information. A bound computed with full Lambda is an oracle/encoder diagnostic: it must not silently be an extra decoder feature. Prior precision is included in Lambda and Q. Omitting likelihood couplings while retaining the prior is not the same as diagonalizing the complete posterior.

Define the symmetric normalized perturbation, natural-parameter error, and normalized full mean:

$$E=\Lambda^{-1/2}(Q-\Lambda)\Lambda^{-1/2},\qquad
r=\Lambda^{-1/2}(\eta_q-\eta),\qquad v=\Lambda^{-1/2}\eta.$$

Let `w=r-Ev` and `kappa=lambda_min(I+E)>0`. No commutativity between the two precision matrices is assumed.

## 2. Lemma 12.1 — whitening the two posterior laws

Under `y=Lambda^(1/2)(beta-mu)`, the full posterior is `N(0,I)`, while the approximate posterior is

$$N((I+E)^{-1}w,(I+E)^{-1}).$$

### Proof

The transformed approximate covariance is

$$\Lambda^{1/2}Q^{-1}\Lambda^{1/2}=(I+E)^{-1}.$$

For its mean, write `Q=Lambda^(1/2)(I+E)Lambda^(1/2)`. Then

$$\begin{aligned}
\Lambda^{1/2}(Q^{-1}\eta_q-\mu)
&=(I+E)^{-1}(v+r)-v\\
&=(I+E)^{-1}(r-Ev).
\end{aligned}$$

The same invertible affine change of variables applies to both laws, so KL is unchanged. This argument also shows why natural-parameter perturbation cannot be replaced by a precision norm alone. QED.

## 3. Theorem 12.1 — exact posterior discrepancy

$$\boxed{
2\operatorname{KL}(p\|q)
=\operatorname{tr}(E)-\log\det(I+E)
+w^T(I+E)^{-1}w.
}$$

### Detailed derivation

For `p_y=N(0,I)` and `q_y=N(a,B^-1)`, the Gaussian log-density ratio averaged under p_y gives

$$2\operatorname{KL}(p_y\|q_y)=\operatorname{tr}(B)-m-\log\det B+a^TBa.$$

This follows by expanding `(y-a)^TB(y-a)`, using `E[y]=0`, `E[yy^T]=I`, and subtracting the standard-normal quadratic expectation m. Substituting `B=I+E` and `a=B^-1 w` proves the formula. The expression is directional: it is KL(p||q), not the reverse KL. QED.

## 4. Lemma 12.2 — spectral remainder control

For every eigenvalue `e>-1`, let `g(e)=e-log(1+e)`. It satisfies `g(0)=g'(0)=0` and `g''(t)=1/(1+t)^2`. Every point between zero and e has `1+t >= min(1,1+e)`. Taylor's integral remainder therefore yields

$$0\leq g(e)\leq\frac{e^2}{2\min(1,1+e)^2}.$$

Summing over eigenvalues, and using `1+e_i>=kappa`, gives

$$\operatorname{tr}(E)-\log\det(I+E)
\leq\frac{\|E\|_F^2}{2\min(1,\kappa)^2}.$$

## 5. Theorem 12.2 — computable upper bound and small-error case

Since `(I+E)^-1 <= kappa^-1 I`, Theorem 12.1 and Lemma 12.2 imply

$$\boxed{
\operatorname{KL}(p\|q)
\leq\frac{\|E\|_F^2}{4\min(1,\kappa)^2}
+\frac{\|r-Ev\|^2}{2\kappa}.
}$$

If additionally `epsilon=||E||_2<1`, replace kappa by `1-epsilon` to obtain

$$\operatorname{KL}(p\|q)
\leq\frac{\|E\|_F^2}{4(1-\epsilon)^2}
+\frac{(\|r\|+\epsilon\|v\|)^2}{2(1-\epsilon)}.$$

The general bound requires only SPD; it may be loose near singularity. The small-error bound is not used when its assumption fails. No clipping of eigenvalues or silent diagonal loading is authorized by this theorem.

The corresponding posterior mean obeys

$$\|\widetilde\mu-\mu\|_\Lambda
=\|(I+E)^{-1}w\|\leq\|w\|/\kappa.$$

## 6. Connection to conditioning and denoising

Averaging a valid approximate decoder q over the same joint acquisition law, Theory 9 gives

$$I(\beta;O\mid H,a)\leq E_{O,a}\operatorname{KL}(p(\beta\mid O,a)\|q(\beta\mid H,a)).$$

Thus the bound can upper-bound compression loss plus fitting error. It does not identify which portion is compression. In particular, a full-operator side input makes compression zero even when an intentionally approximate solver has fitting error.

For the same Gaussian forward perturbation `z_tau=alpha beta+sigma epsilon`, `sigma>0`, conditioning additionally on z_tau adds `alpha^2/sigma^2 I` to both precisions and `alpha z_tau/sigma^2` to both natural parameters. Reapplying the mean bound controls the difference of these two Gaussian denoising predictions. Epsilon-prediction differences multiply the beta-mean difference by `alpha/sigma`; this is not a finite reverse-sampler error guarantee or an unrestricted Bayes compression identity for a plug-in q.

## 7. Falsification and contribution admission

The Notebook checks noncommuting random SPD matrices with nonzero natural-parameter error, zero perturbation, the direct KL formula, the bound, and the dependence on natural-parameter magnitude. Finite checks cannot prove the universal statement.

The contribution candidate is an explicit budgeted coupling representation whose measurable error is controlled. The general Gaussian formula and a large bound are not contributions by themselves. Unknown poles, estimated noise, mixture posteriors and learned VAE coordinates need separate validation.
