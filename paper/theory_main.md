# Main-paper theory: from nested information to conditional routing

This file contains only the results needed by the TII narrative. Detailed Gaussian posterior calculations remain in `../theory/12_posterior_precision_distortion.md` and `../theory/13_acquisition_only_budget_choice.md`. The statements below apply standard conditional-expectation and model-selection arguments to the actual matched conditioner; they are not claimed as new general probability theory.

## Proposition 1 — nested-message risk decomposition

Fix a trained checkpoint. Let \(R\) be the complete ordinary code and \(M=T(R)\) the statistical-prefix message. Let \(X\) contain the noisy latent, diffusion time and common side information, and let \(V\) be the square-integrable native regression target. Define

\[
f_R=\mathbb E[V\mid X,R],\qquad f_M=\mathbb E[V\mid X,M].
\]

For fitted predictors \(\widehat f_R,\widehat f_M\), let

\[
A_j=\mathbb E\|\widehat f_j-f_j\|^2.
\]

Then

\[
\boxed{\mathcal R(\widehat f_M)-\mathcal R(\widehat f_R)
=\mathbb E\|f_R-f_M\|^2+A_M-A_R.}
\]

### Proof

Because \(M\) is measurable with respect to \(R\), `(X,M)` is a sub-information set of `(X,R)`. Expand

\[
V-f_M=(V-f_R)+(f_R-f_M).
\]

The cross term has zero expectation because `E[V-f_R|X,R]=0`. This gives the Bayes-risk difference. For either fitted predictor, expand \(V-\widehat f_j=(V-f_j)+(f_j-\widehat f_j)\); its cross term also vanishes after conditioning on the arm's information set. Subtract the two identities.

### Consequence

M cannot beat R by adding Bayes information. It can win for a finite model only when the reduction in finite approximation/optimization error exceeds the nonnegative information penalty. This is the precise interpretation of an M-over-B1-aux gain.

## Definition — acquisition-conditional accessibility profile

Let \(A\) be the deployment-available acquisition condition. For every fixed trained arm j, define

\[
\rho_j(a)=\mathbb E[\ell_j\mid A=a].
\]

The collection ρ(a) is the **accessibility profile**. It is an estimand of the complete trained system, not a latent label assigned by the router.

For the nested pair, condition Proposition 1 on `A=a` to obtain

\[
\rho_M(a)-\rho_R(a)=\Gamma_{M\mid R}(a)+A_M(a)-A_R(a).
\]

A condition-dependent advantage therefore has an explicit competing explanation: lower finite fitting error versus lost Bayes information.

## Proposition 2 — routing headroom

For fixed trained arms \(j\in\mathcal J\), define

\[
\mathcal H_{route}
=\min_j\mathbb E_A\rho_j(A)-\mathbb E_A\min_j\rho_j(A).
\]

Then

\[
\boxed{\mathcal H_{route}\ge0.}
\]

It is strictly positive only if no single global arm attains the conditionwise minimum almost surely and the positive conditional gaps have nonzero measure.

### Proof

For every j and every a,

\[
\min_k\rho_k(a)\le\rho_j(a).
\]

Take expectations and then minimize the right-hand side over j. Equality holds when one global arm is a conditionwise minimizer almost surely; otherwise a strict inequality occurs whenever the losing gap contributes positive mass.

### Interpretation

The result is a **go/no-go test for routing**. If the estimated headroom is below a predeclared practical margin, the final method must use the best single representation. The existence of several representations does not justify a router.

## Proposition 3 — plug-in routing regret under conditional risk estimation

Assume a source-valid estimator satisfies, on the deployment-relevant acquisition set,

\[
|\widehat\rho_j(a)-\rho_j(a)|\le\epsilon(a)
\quad\text{for every }j.
\]

Let \(\widehat j(a)=\arg\min_j\widehat\rho_j(a)\) and \(j^*(a)=\arg\min_j\rho_j(a)\). Then

\[
\boxed{\rho_{\widehat j(a)}(a)-\rho_{j^*(a)}(a)\le2\epsilon(a),}
\]

and consequently

\[
\mathcal R_{\widehat{route}}-\mathcal R_{oracle\ route}
\le2\mathbb E_A\epsilon(A).
\]

### Proof

By optimality of the empirical choice,

\[
\widehat\rho_{\widehat j}\le\widehat\rho_{j^*}.
\]

Add and subtract the two true risks and apply the two estimation-error bounds. Integrate over A.

### Boundary

This is a conditional guarantee, not a claim that the source estimator has the stated error on an unseen target domain. The experiments must measure source and unseen-acquisition behavior separately. If the transportability assumption fails, the bound is not invoked.

## Counterexamples and validation

1. **No routing headroom:** ρ_R(a)<ρ_M(a) for every a. A learned router should collapse to R; a nontrivial router is unnecessary complexity.
2. **Positive routing headroom:** R is better at low missingness while M is better at high missingness. The oracle conditional selector beats either global arm even if their overall means are close.
3. **Spurious empirical crossing:** small validation groups create sign changes but group-bootstrap intervals cover a practical zero margin. Routing remains HOLD.
4. **Target conditional shift:** source risk crossings reverse on an unseen acquisition. A source-only router fails; the result is reported as a transportability failure, not repaired with target labels.

`experiments/p19/toy_routing.py` executes the first two algebraic cases and the plug-in-regret calculation. The toy is a theorem witness, not PHM evidence.
