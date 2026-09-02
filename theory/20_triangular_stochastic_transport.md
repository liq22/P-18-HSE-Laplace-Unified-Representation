# Theorem 20 — Triangular stochastic transport representation

## Status

**Constructive theorem for measurable kernels; dynamic realization requires the
regularity stated in Axiom A8.**

## Purpose

The final representation is not a serial stack of an unconstrained Flow and an
unconstrained Diffusion. It is a triangular composition:

\[
C^*=T_d(C),\qquad
P'=P,\qquad
M'\sim K_d^m(\cdot\mid C^*,P,O_d).
\]

The missing posterior may depend on the canonical shared state, so the final
model is generally not covered by the commuting-generator null theorem.

## 1. Static kernel construction

Let

- \(T_d:\mathcal H_c\to\mathcal H_c\) be measurable;
- \(I_p\) be identity on the observed-private block;
- \(K_d^m(dm\mid c^*,p,o)\) be a Markov kernel on the source-supported missing
  block.

For an input posterior \(q_d(dc,dp\mid o)\), define

\[
K_d^U(B\mid o)
=
\int
\mathbf 1_B(c^*,p,m)
K_d^m(dm\mid c^*,p,o)
q_d(dc,dp\mid o),
\]

where \(c^*=T_d(c)\).

## 2. Lemma 20.1 — measurability

For every measurable set \(B\), \(K_d^U(B\mid o)\) is measurable in \(o\), and
for every \(o\), \(K_d^U(\cdot\mid o)\) is a probability measure.

### Proof

Composition of a measurable map with a Markov kernel is a Markov kernel.
Integrating a kernel against the conditional measure \(q_d\) preserves
measurability and total mass one. ∎

## 3. Theorem 20.1 — existence of the triangular representation

The kernel \(K_d^U\) is a well-defined conditional distribution on

\[
\mathcal H_c
\times
\mathcal H_{p,d}
\times
\mathcal H_{m,d}.
\]

Its private marginal equals the input private marginal, its shared coordinate
is the push-forward by \(T_d\), and its missing conditional is
\(K_d^m\).

### Detailed proof

The probability-kernel claim follows from Lemma 20.1.

For the shared marginal, integrate over all private and missing coordinates.
The missing kernel integrates to one, leaving the push-forward of the shared
coordinate under \(T_d\).

For the private marginal, integrate over shared and missing coordinates. The
second output coordinate is exactly \(p\), so the resulting marginal is the
input private marginal.

Conditioning on \((c^*,p,o)\) leaves exactly the kernel \(K_d^m\). ∎

## 4. Dynamic realization

A compatible triangular process is

\[
dC_t=v_t^c(C_t,a_d)\,dt,
\]

\[
dP_t=0,
\]

\[
dM_t
=
b_t^m(M_t,C_t,P_t,O_d)\,dt
+
\sigma_t^m(M_t,C_t,P_t,O_d)\,dW_t.
\]

Solve the shared ODE and private identity path, then the conditional missing
SDE. Under Axiom A8, the finite-interval process exists.

## 5. Corollary 20.1 — decoupled null model

If the missing kernel does not depend on \(C^*\) or \(P\), the construction
factorizes. Under the stronger coefficient assumptions in Theory 12, the
shared and missing generators commute.

This is a simpler baseline, not the default final model.

## 6. Global-null exclusion

The kernel has no coordinate for \(\mathcal H_0\). Adding a global-null sample
requires an external prior and must be labeled prior-driven.

## 7. Failure boundaries

1. The missing kernel can be misspecified or unidentifiable.
2. A non-measurable role assignment invalidates the construction.
3. State-dependent projectors add derivative terms in a dynamic model.
4. Coupled dynamics are order-sensitive.
5. The theorem proves existence, not the necessity of Flow or Diffusion.

## 8. Experimental implication

Compare:

```text
decoupled missing posterior
shared-conditioned missing posterior
private-mixed negative control
global-null generation negative control
```

The coupled model is retained only if conditioning improves a proper score or a
task that genuinely depends on the missing coordinate.
