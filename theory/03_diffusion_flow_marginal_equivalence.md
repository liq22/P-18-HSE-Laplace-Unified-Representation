# Theorem 3 — Diffusion–flow marginal equivalence

## Status

**Proved for a prescribed smooth density path and a time-dependent,
state-independent positive-semidefinite diffusion matrix. This is background
probability-path theory, not the paper's primary novelty.**

## Purpose

This theorem explains how a deterministic Flow and a compensated stochastic
process can realize the same one-time marginal path. It does not show that
either mechanism is needed for the proposed representation, and it does not
justify stochastic recovery on source-global-null coordinates.

## 1. Assumptions

Let \(z\in\mathbb R^m\), \(t\in[0,1]\), and let \(\rho_t(z)>0\) be a
\(C^1\) density in time and \(C^2\) in state, with sufficient decay at
infinity. Assume a velocity field \(v_t\) satisfies

\[
\partial_t\rho_t
=
-\nabla\cdot(\rho_tv_t).
\tag{3.1}
\]

Let \(D_t\) be deterministic, symmetric, positive semidefinite and independent
of state. Define

\[
s_t(z)=\nabla_z\log\rho_t(z).
\]

## 2. Lemma 3.1 — score identity

\[
\rho_t(z)s_t(z)=\nabla\rho_t(z).
\]

### Proof

Because \(\rho_t(z)>0\),

\[
\nabla\log\rho_t
=
\frac{\nabla\rho_t}{\rho_t}.
\]

Multiply by \(\rho_t\). ∎

## 3. Lemma 3.2 — Fokker–Planck equation

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

Its density \(p_t\) satisfies

\[
\partial_tp_t
=
-\nabla\cdot[(v_t+D_ts_t)p_t]
+
\nabla\cdot(D_t\nabla p_t).
\tag{3.3}
\]

### Proof

This is the Fokker–Planck equation for drift \(v_t+D_ts_t\) and diffusion
covariance \(2D_t\), using state independence of \(D_t\). ∎

## 4. Theorem 3 — identical one-time marginal path

If \(Z_0\sim\rho_0\), Equation (3.2) is well posed, and the
Fokker–Planck solution is unique in the adopted class, then

\[
\boxed{p_t=\rho_t}
\qquad
\text{for all }t\in[0,1].
\]

### Detailed proof

Substitute \(p_t=\rho_t\) into Equation (3.3):

\[
\partial_t\rho_t
=
-\nabla\cdot[(v_t+D_ts_t)\rho_t]
+
\nabla\cdot(D_t\nabla\rho_t).
\]

Expand the first divergence. Lemma 3.1 gives

\[
D_ts_t\rho_t=D_t\nabla\rho_t,
\]

so the two diffusion-divergence terms cancel. The remaining equation is
Equation (3.1), with the same initial density. Uniqueness yields
\(p_t=\rho_t\). ∎

## 5. Corollaries

### Corollary 3.1 — pure Flow

Setting \(D_t=0\) yields the deterministic probability-flow ODE

\[
dZ_t=v_t(Z_t)dt.
\]

### Corollary 3.2 — stochastic realizations

Every admissible \(D_t\succeq0\) gives a stochastic process with the same
one-time marginals. The sample paths and numerical behavior need not be equal.

### Corollary 3.3 — recoverable-missing stochastic block

Let

\[
D_t=\gamma_tP_{m,d},
\qquad
\gamma_t\geq0.
\]

Then stochastic forcing acts only on the recoverable-missing block. The global
null projector \(P_0\) must satisfy

\[
D_tP_0=P_0D_t=0.
\]

The theorem does not authorize a learned source-supported posterior for
\(\mathcal H_0\).

## 6. Gaussian verification

For

\[
\rho_t=\mathcal N(m_t,\sigma_t^2),
\]

a continuity velocity is

\[
v_t(x)
=
\dot m_t
+
\frac{\dot\sigma_t}{\sigma_t}(x-m_t),
\]

and the score is

\[
s_t(x)
=-\frac{x-m_t}{\sigma_t^2}.
\]

For scalar \(D_t\geq0\), the compensated drift is

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

The moment equation gives

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

Substituting \(V_t=\sigma_t^2\) yields

\[
\dot V_t=2\sigma_t\dot\sigma_t,
\]

which is the derivative of \(\sigma_t^2\).

## 7. Why this is not the novelty claim

Probability-flow and stochastic-interpolant theories already establish broad
Flow–Diffusion relationships. The candidate novelty is the acquisition-support
partition and its permissible operations, not this theorem.

## 8. Failure boundaries

1. State-dependent \(D_t\) introduces additional divergence terms.
2. A density with zeros or singular support may not have an ordinary score.
3. Equal marginals do not imply equal paths, likelihoods or semantic coupling.
4. A learned approximate score gives approximate, not exact, equality.
5. Discontinuous learned projectors require separate analysis.
6. Diffusion is unnecessary if a simpler calibrated posterior model matches it.

## 9. Experimental implication

The analytic experiment should verify:

- Flow and compensated SDE mean trajectories agree;
- their covariance trajectories agree;
- pathwise variance differs when \(D_t>0\);
- observed-private coordinates remain unchanged;
- global-null coordinates receive no stochastic update;
- numerical discretization error is reported separately.
