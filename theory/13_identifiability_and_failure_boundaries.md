# Theory analysis 13 — Identifiability and failure boundaries

## Status

**Collection of proved counterexamples and explicit non-identifiability
results.**

## Purpose

Existence of a representation is weaker than recoverability. This document
records situations in which support classification, canonical transport or
posterior recovery cannot be identified from the available data.

## 1. Proposition 13.1 — common support can be trivial

There exist individually observable acquisition domains with

\[
\mathcal H_c=\{0\}.
\]

### Construction and proof

Let

\[
\mathcal H_1^o=\operatorname{span}(e_1),
\qquad
\mathcal H_2^o=\operatorname{span}(e_2).
\]

Their intersection is \(\{0\}\). Both domains observe a non-zero direction,
but no non-trivial common coordinate exists. ∎

### Consequence

A forced positive shared dimension invents common information.

## 2. Proposition 13.2 — latent coordinates are not identified without anchors

The factorization

\[
Y=A\Theta
\]

is invariant under every invertible coordinate change \(R\).

### Proof

Set

\[
\widetilde\Theta=R\Theta,
\qquad
\widetilde A=AR^{-1}.
\]

Then

\[
\widetilde A\widetilde\Theta
=
A\Theta
=
Y.
\]

Thus observations alone admit infinitely many latent coordinate systems. ∎

### Consequence

Physical modal slots, pole ordering, paired events or calibrated acquisition
metadata are needed to anchor the representation.

## 3. Proposition 13.3 — marginal alignment can reverse semantics

Let \(Y\in\{0,1\}\) be balanced. Define

\[
Z_1=Y,
\qquad
Z_2=1-Y.
\]

Both marginals are Bernoulli\((1/2)\), but a classifier transferred from the
first domain fails on the second. ∎

### Consequence

MMD, domain confusion or Wasserstein marginal matching cannot establish
semantic canonicalization.

## 4. Proposition 13.4 — posterior means do not identify posteriors

For any \(a>0\),

\[
\mu_a
=
\frac12\delta_{-a}
+
\frac12\delta_a
\]

and \(\delta_0\) have the same mean but different variance, support and
nonlinear decisions. ∎

### Consequence

A mean-only tensor cannot generally represent recoverable-missing uncertainty.

## 5. Proposition 13.5 — sampled modal parameters can be aliased

For regular query times \(t_n=n\Delta\), frequencies

\[
\omega'
=
\omega+rac{2\pi k}{\Delta}
\]

produce identical phases:

\[
e^{i\omega't_n}
=
e^{i\omega t_n}.
\]

With equal damping and compatible residues, the sampled trajectories coincide.
∎

### Consequence

Modal slots must respect anti-aliasing and acquisition support.

## 6. Proposition 13.6 — global-null coordinates have no source likelihood evidence

Assume

\[
A_dP_0=0
\qquad
\text{for every }d\in\mathcal D_s.
\]

Then

\[
p(
\{Y_d\}_d
\mid
\Theta_c,\Theta_p,\Theta_m,\Theta_0)
=
p(
\{Y_d\}_d
\mid
\Theta_c,\Theta_p,\Theta_m).
\]

### Proof

Every source observation depends on \(A_d\Theta\). The term
\(A_dP_0\Theta_0\) is zero for every source, so changing \(\Theta_0\) leaves
the source likelihood unchanged. ∎

### Consequence

Source data cannot identify \(\Theta_0\) through the likelihood. A posterior
on this block is prior-driven or induced by additional structural assumptions;
it must not be reported as data-supported recovery.

## 7. Proposition 13.7 — private identity can conflict with a target joint law

If shared and private variables are correlated and the target changes their
dependence, an identity-private map may not reach the target joint law. The
counterexample in Theorem 11 supplies a construction.

## 8. Proposition 13.8 — one global Laplace pole set can fail under switching

Consider

\[
\dot x
=
\begin{cases}
-a_1x,&t<t_s,\\
-a_2x,&t\geq t_s,
\end{cases}
\qquad
 a_1\neq a_2.
\]

The trajectory is piecewise exponential. No single scalar pole reproduces both
decay rates exactly on an interval containing the switch. ∎

### Consequence

Use a local analysis window, a declared residual or an explicit switching
extension. Do not present a fixed global pole dictionary as universally exact.

## 9. Proposition 13.9 — hard support is threshold sensitive

A Gramian eigenvalue \(\lambda\) is assigned observable when
\(\lambda\geq\tau_o\) and unobservable otherwise. An arbitrarily small change
in \(\tau_o\) around \(\lambda\) changes the discrete role.

### Consequence

Report threshold margin and a soft structural observability weight for
near-threshold slots.

## 10. Proposition 13.10 — recoverable support does not guarantee learnability

A mode can belong to \(\mathcal H_{m,d}\) because another source operator can
observe it while the training set contains no paired event linking that
observation to the current-domain state.

### Construction and proof

Let source 1 observe \(C\), source 2 observe \(M\), and let their datasets be
unpaired samples from the two marginals. Distinct joint laws
\(p_1(C,M)\) and \(p_2(C,M)\) can have the same marginals
\(p(C)\) and \(p(M)\), but different conditionals
\(p_1(M\mid C)\neq p_2(M\mid C)\). The unpaired observations have the same
distribution under both models, so no procedure based only on those marginals
can identify which conditional is correct. ∎

### Consequence

Support elsewhere is necessary but not sufficient for conditional recovery.
Paired events, a physical coupling model or another identification assumption
is required.

## 11. Required negative controls

A credible experiment suite must include:

- empty common support;
- a recoverable-missing slot;
- a source-global-null slot;
- class-permuted but marginally aligned domains;
- identical posterior means with different posterior shapes;
- aliasing without anti-alias filtering;
- a switching trajectory outside the fixed-pole model;
- a near-threshold slot;
- correlated shared/private modes;
- unpaired marginals with non-identifiable missing conditionals.

## 12. Scientific boundary

The theory supports:

> Under declared structural operators, a source-supported four-block
> representation can be defined, with explicit invariants and failure
> boundaries.

It does not support:

> Every heterogeneous time series admits a unique, learnable and semantically
> aligned unified representation.
