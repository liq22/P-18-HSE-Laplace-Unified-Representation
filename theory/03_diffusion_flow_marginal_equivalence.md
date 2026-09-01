# Theorem 3 — Diffusion–flow marginal equivalence

## Status

**Proved for a prescribed smooth density path and a time-dependent, state-independent positive-semidefinite diffusion matrix.**

## Purpose

This theorem is the mathematical reason diffusion and flow can be two blocks of one representation rather than two unrelated models. It does not claim that the two processes have identical sample paths. It proves equality of their one-time marginal density path.

## 1. Assumptions

Let \(z\in\mathbb R^m\), \(t\in[0,1]\), and let \(\rho_t(z)>0\) be a \(C^1\) density in time and \(C^2\) in state, with sufficient decay at infinity.

Assume a velocity field \(v_t(z)\) satisfies the continuity equation

\[
\partial_t\rho_t
=
-\nabla\cdot(\rho_tv_t).
\tag{3.1}
\]

Let \(D_t\) be a deterministic, symmetric, positive-semidefinite matrix that depends on time but not on state.

Define the score

\[
s_t(z)=\nabla_z\log\rho_t(z).
\]

## 2. Lemma 3.1 — score identity

### Statement

\[
\rho_t(z)s_t(z)=\nabla\rho_t(z).
\]

### Proof

Since \(\rho_t(z)>0\),

\[
\nabla\log\rho_t
=
\frac{\nabla\rho_t}{\rho_t}.
\]

Multiplying by \(\rho_t\) gives the result. ∎

## 3. Lemma 3.2 — Fokker–Planck equation for the compensated SDE

Consider

\[
dZ_t
=
\left[
 v_t(Z_t)+D_ts_t(Z_t)
\right]dt
+
\sqrt{2D_t}\,dW_t.
\tag{3.2}
\]

Because \(D_t\) is independent of state, the density \(p_t\) of this SDE satisfies

\[
\partial_tp_t
=
-\nabla\cdot\left[
(v_t+D_ts_t)p_t
\right]
+
\nabla\cdot(D_t\nabla p_t).
\tag{3.3}
\]

This is the standard Fokker–Planck equation for diffusion covariance \(2D_t\). ∎

## 4. Theorem 3 — identical marginal density path

### Statement

If \(Z_0\sim\rho_0\) and Equation (3.2) is well posed, then its density satisfies

\[
\boxed{p_t=\rho_t}
\]

for every \(t\in[0,1]\), provided the Fokker–Planck equation has a unique solution in the adopted class.

### Detailed proof

Substitute the candidate density \(p_t=\rho_t\) into Equation (3.3):

\[
\partial_t\rho_t
=
-\nabla\cdot\left[
(v_t+D_ts_t)\rho_t
\right]
+
\nabla\cdot(D_t\nabla\rho_t).
\]

Expand the first divergence:

\[
\partial_t\rho_t
=
-\nabla\cdot(v_t\rho_t)
-
\nabla\cdot(D_ts_t\rho_t)
+
\nabla\cdot(D_t\nabla\rho_t).
\]

By Lemma 3.1,

\[
s_t\rho_t=\nabla\rho_t.
\]

Therefore

\[
-\nabla\cdot(D_ts_t\rho_t)
+
\nabla\cdot(D_t\nabla\rho_t)
=0.
\]

The equation reduces to

\[
\partial_t\rho_t
=
-\nabla\cdot(v_t\rho_t),
\]

which is exactly the prescribed continuity equation (3.1). Since the initial density is also \(\rho_0\), uniqueness of the Fokker–Planck solution gives \(p_t=\rho_t\). ∎

## 5. Corollaries

### Corollary 3.1 — pure flow

Setting

\[
D_t=0
\]

gives

\[
dZ_t=v_t(Z_t)dt,
\]

the deterministic probability-flow ODE.

### Corollary 3.2 — a family of stochastic realizations

Any admissible \(D_t\succeq0\) gives a stochastic process with the same one-time marginals. The choice of \(D_t\) changes pathwise randomness and numerical behavior, not the prescribed marginal path.

### Corollary 3.3 — observability-conditioned block diffusion

Let

\[
D_t=\gamma_tP_{u,d},
\qquad
\gamma_t\geq0.
\]

Then stochastic forcing and score compensation act only on the unobserved block. If \(v_t\) acts on the shared block and is zero on the private block, the same theorem applies in the product coordinates.

## 6. Gaussian verification

Consider a one-dimensional prescribed path

\[
\rho_t=\mathcal N(m_t,\sigma_t^2).
\]

A continuity velocity is

\[
v_t(x)
=
\dot m_t
+
\frac{\dot\sigma_t}{\sigma_t}(x-m_t).
\]

The score is

\[
s_t(x)
=-\frac{x-m_t}{\sigma_t^2}.
\]

For scalar diffusion \(D_t\geq0\), the compensated drift is

\[
b_t(x)
=
\dot m_t
+
\left(
\frac{\dot\sigma_t}{\sigma_t}
-
\frac{D_t}{\sigma_t^2}
\right)(x-m_t).
\]

The mean equation is

\[
\frac{d}{dt}\mathbb E[X_t]
=
\dot m_t.
\]

For the variance \(V_t\), the linear SDE moment equation gives

\[
\dot V_t
=
2
\left(
\frac{\dot\sigma_t}{\sigma_t}
-
\frac{D_t}{\sigma_t^2}
\right)V_t
+2D_t.
\]

Substituting \(V_t=\sigma_t^2\),

\[
\dot V_t
=
2\sigma_t\dot\sigma_t
-2D_t
+2D_t
=
2\sigma_t\dot\sigma_t,
\]

which is exactly the derivative of \(\sigma_t^2\). This is the analytic invariant tested in the code.

## 7. Why this is not a novelty claim by itself

Probability-flow ODEs and stochastic-interpolant theory already establish broad relationships between flows and diffusions. The proposed research contribution must therefore be narrower:

\[
\text{the diffusion matrix and velocity blocks are selected by physical observability projectors in a stable Laplace modal space.}
\]

The novelty cannot be “we unified diffusion and flow.”

## 8. Failure boundaries

1. If \(D_t\) depends on state, additional divergence terms appear. The displayed compensation is then incomplete.
2. If \(\rho_t\) has zeros or is singular on the chosen coordinate space, the ordinary score may not exist.
3. Equality of marginals does not imply equality of paths, coupling, likelihood estimator, or discretization error.
4. A learned approximate score produces only approximate equality.
5. Block projectors that change discontinuously with state require a separate nonsmooth analysis.

## 9. Experimental implication

The first analytic experiment should prescribe a Gaussian modal path and verify:

- flow and compensated SDE have the same mean trajectory;
- flow and compensated SDE have the same covariance trajectory;
- pathwise variance differs when \(D_t>0\);
- observed-private coordinates remain unchanged;
- discretization error is reported separately from the theorem.
