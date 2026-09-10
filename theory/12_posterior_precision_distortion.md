# Theory 12 — Posterior parameter error, tighter bounds and the actual target

## Scope and assumptions

This is Gaussian supporting analysis, not a new general information theorem. Fix the same observation, prior, coordinates and base measure. Write

\[
P=N(\mu,\Lambda^{-1}),\quad \mu=\Lambda^{-1}\eta,
\qquad \widetilde P=N(Q^{-1}\widetilde\eta,Q^{-1}),
\quad \Lambda,Q\succ0.
\]

The actual decoder condition is `(H,a_consumed)` as in Theory 0. A calculation using full precision is an encoder/oracle diagnostic, not an uncounted decoder feature. `eta` is the natural parameter (information vector), not a diffusion score. The likelihood information and prior precision must be distinguished.

Define

\[
E=\Lambda^{-1/2}(Q-\Lambda)\Lambda^{-1/2},\quad
r=\Lambda^{-1/2}(\widetilde\eta-\eta),\quad
v=\Lambda^{-1/2}\eta,\quad w=r-Ev,\quad
\kappa=\lambda_{\min}(I+E)>0.
\]

No commutativity is assumed. All square roots are symmetric positive-definite roots.

## Lemma 12.1: simultaneous whitening

Under `y=Lambda^(1/2)(beta-mu)`, P becomes `N(0,I)` and the approximation becomes

\[
N((I+E)^{-1}w,(I+E)^{-1}).
\]

**Proof.** Factor `Q=Lambda^(1/2)(I+E)Lambda^(1/2)`. Transform its inverse by congruence. For the mean,

\[
\Lambda^{1/2}(Q^{-1}\widetilde\eta-\mu)
=(I+E)^{-1}(v+r)-v=(I+E)^{-1}w.
\]

An invertible common coordinate change preserves KL. This proves the lemma.

## Theorem 12.1: exact joint precision/natural-parameter error

\[
\boxed{2\,KL(P\|\widetilde P)
=\operatorname{tr}E-\log\det(I+E)+w^T(I+E)^{-1}w.}
\]

**Proof.** In the whitened coordinates the Gaussian log-density ratio has expectation
`tr(B)-m-logdet(B)+a^TBa`, where `B=I+E`, `a=B^-1 w`.
Expand its quadratic form and use `E_P[y]=0`, `E_P[yy^T]=I`.
Substitution gives the result. It is forward KL, not reverse KL.

The identity preserves the earlier correct result. It shows why precision and natural-parameter errors can cancel: `r=Ev` makes the entire mean-error term vanish; `r=-Ev` amplifies it. Bounding their norms separately discards this interaction.

## Lemma 12.2: tightened spectral remainder

For `e>-1`, integration of `g'(e)=e/(1+e)` gives

\[
g(e)=e-\log(1+e)=e^2\int_0^1\frac{t}{1+te}\,dt.
\]

The line segment from 1 to `1+e` stays above `min(1,1+e)`. Consequently

\[
0\leq g(e)\leq \frac{e^2}{2\min(1,1+e)}.
\]

Summing the eigenvalue inequalities gives
`tr(E)-logdet(I+E) <= ||E||_F^2/[2 min(1,kappa)]`.
The earlier denominator `min(1,kappa)^2` remains valid but is looser.

## Theorem 12.2: SPD bound and its cost

\[
\boxed{KL(P\|\widetilde P)
\leq \frac{\|E\|_F^2}{4\min(1,\kappa)}
+\frac{\|r-Ev\|^2}{2\kappa}.}
\]

**Proof.** Apply Lemma 12.2 to Theorem 12.1 and use
`(I+E)^-1 <= kappa^-1 I`. If additionally `epsilon=||E||_2<1`, replace
`kappa` by `1-epsilon` and `||w||` by `||r||+epsilon||v||`.
Also `||mu_tilde-mu||_Lambda <= ||w||/kappa`.

This is not automatically a useful online certificate. Full whitening and an eigenvalue computation are required. Report exact KL, both bounds, bound/exact ratios and candidate ordering. A small bound can certify a specified tolerance; a large bound cannot select the best layout. No diagonal loading or eigenvalue clipping is licensed by the theorem.

The existing `core.precision_certificate` and historical sampled CSV retain the previous valid Taylor bound. `parameterization_controls.bounds` compares both bounds on identical inputs. Historical results are not silently relabeled as tight-bound results.

## Theorem 12.3: project to the declared target before evaluating a denoiser

Freeze a full-row-rank linear target `z0=L beta` for this diagnostic only. Let its exact and approximate posteriors be `N(m,V)` and `N(mq,W)`, obtained by transforming their respective means and covariances with L. No equivalence with a learned reference VAE is assumed.

At a common diffusion time, let `z_tau=alpha z0+sigma epsilon`, `sigma>0`, with independent standard Gaussian epsilon. Define

\[
M=\alpha^2V+\sigma^2I,\quad N=\alpha^2W+\sigma^2I,
\quad B=M^{-1}-N^{-1},\quad\delta=m_q-m.
\]

The exact Gaussian epsilon-predictors are

\[
f_P(z)=\sigma M^{-1}(z-\alpha m),\qquad
f_q(z)=\sigma N^{-1}(z-\alpha m_q).
\]

Their squared discrepancy under the **true** noisy target is

\[
\boxed{D_\tau(P,q;L)=\sigma^2\left[
\operatorname{tr}(BMB^T)+\alpha^2\delta^TN^{-2}\delta\right].}
\]

**Proof.** Gaussian conditional expectation gives each predictor. With
`y=z-alpha m`, the difference is `sigma[B y+alpha N^-1 delta]`.
Under P, `E[y]=0` and `Cov(y)=M`. Expanding the squared norm eliminates
the cross term and yields the two displayed terms. This proves the result.

For a variance-preserving schedule and `v=alpha epsilon-sigma z0`, the v discrepancy is `D_tau/alpha^2` when `alpha>0`. At `alpha=0`, compute directly from the conditional target means instead of dividing by zero. The x0 discrepancy is `sigma^2 D_tau/alpha^2` when `alpha>0`.

This is a Gaussian **plug-in predictor discrepancy**. It equals a Bayes compression-risk gap only when q is the true induced compressed conditional of Theory 10. It is not a learned-network or finite-sampler error bound.

## Target ranking boundary

Data processing gives `KL(F#P || F#q) <= KL(P||q)` for a common measurable target map, but does not preserve rankings between q's. For `P=N(0,I2)`, mean-shifted approximations `(0,.9)` and `(1,0)` have joint KL `.405` and `.5`. Projecting onto the second coordinate gives `.405` and `0`: the ranking reverses. A target criterion must therefore use a frozen L or the actual frozen reference encoder, not whole-coefficient KL by default.

## Executable checks and admission

The same-stem Notebook retains the original noncommuting SPD and zero-error tests, then checks the tighter bound, joint-error cancellation/amplification, target ranking and the target denoiser formula against Monte Carlo. It records bound looseness rather than merely checking an inequality.

Spantini et al. (2015, 2017) and Oko et al. (2025) are direct analytical predecessors. The candidate novelty must come from a concrete target-relevant conditioner at declared information and computation budgets. None of the generic Gaussian identities alone is admitted as a new contribution.
