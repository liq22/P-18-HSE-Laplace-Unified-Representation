# Theory analysis 13 — Identifiability and failure boundaries

## Status

**Collection of proved counterexamples and explicit non-identifiability results.**

## Purpose

Existence of a representation is weaker than recoverability. This document records situations in which the proposed decomposition or canonicalization cannot be uniquely identified. These are method boundaries, not implementation corner cases.

## 1. Proposition 13.1 — common support can be trivial

### Statement

There exist individually observable acquisition domains whose common observable subspace is

\[
\mathcal H_c=\{0\}.
\]

### Construction and proof

Let \(\mathcal H=\mathbb R^2\), with

\[
\mathcal H_1^o=\operatorname{span}(e_1),
\qquad
\mathcal H_2^o=\operatorname{span}(e_2).
\]

Each domain observes one non-zero direction, but

\[
\mathcal H_1^o\cap\mathcal H_2^o=\{0\}.
\]

Hence no non-trivial shared coordinate exists. ∎

### Consequence

The model must support an empty shared block. A forced positive shared dimension introduces invented common information.

## 2. Proposition 13.2 — the observation operator is not identifiable from observations alone

### Statement

Without additional constraints, the factorization

\[
Y=A\Theta
\]

is invariant under any invertible latent change of coordinates.

### Proof

Let \(R\in\mathbb R^{m\times m}\) be invertible. Define

\[
\widetilde\Theta=R\Theta,
\qquad
\widetilde A=AR^{-1}.
\]

Then

\[
\widetilde A\widetilde\Theta
=AR^{-1}R\Theta
=A\Theta
=Y.
\]

Thus the same observations admit infinitely many latent coordinate systems. ∎

### Consequence

Physical modal slots, pole ordering, sensor metadata, or paired views are needed to anchor the coordinates. A generic autoencoder latent cannot by itself identify physical shared/private modes.

## 3. Proposition 13.3 — marginal alignment does not identify semantic alignment

### Statement

Two domains can have perfectly matched representation marginals while class semantics are reversed.

### Construction and proof

Let \(Y\in\{0,1\}\) be balanced. In domain 1, define

\[
Z_1=Y.
\]

In domain 2, define

\[
Z_2=1-Y.
\]

Both marginals are Bernoulli\((1/2)\), so

\[
\operatorname{Law}(Z_1)
=
\operatorname{Law}(Z_2).
\]

However, the label meaning is reversed. A classifier trained on domain 1 fails completely on domain 2. ∎

### Consequence

MMD, adversarial domain confusion, or Wasserstein marginal matching is not enough. Canonical transport requires paired latent events, physical modal ordering, or source-only semantic constraints.

## 4. Proposition 13.4 — posterior mean is not an identifiable posterior

### Statement

Infinitely many posterior distributions share the same mean.

### Proof

For any \(a>0\),

\[
\mu_a=
\frac12\delta_{-a}+
\frac12\delta_a
\]

has mean zero. The point mass \(\delta_0\) also has mean zero. These measures have different variance, support, and decisions for nonlinear tasks. ∎

### Consequence

A deterministic embedding containing only posterior means cannot represent unobserved uncertainty in general.

## 5. Proposition 13.5 — finite-window modal representations are not globally unique

### Statement

On a finite set of query times, different modal parameter sets can produce the same sampled trajectory.

### Construction

Let query times lie on a regular grid \(t_n=n\Delta\). Frequencies \(\omega\) and

\[
\omega'=
\omega+\frac{2\pi k}{\Delta}
\]

produce identical complex phases:

\[
e^{i\omega't_n}
=e^{i\omega n\Delta}e^{i2\pi kn}
=e^{i\omega t_n}.
\]

With equal damping and adjusted residues, sampled trajectories coincide. ∎

### Consequence

Frequency slots must respect acquisition support and anti-aliasing. Irregular timestamps reduce but do not automatically eliminate every modal ambiguity.

## 6. Proposition 13.6 — private identity can conflict with a desired target joint law

Theorem 11 assumes product structure or a target compatible with identity private transport. If shared and private coordinates are correlated and the canonical target changes that dependence, the identity-private map may not reach the target. The counterexample in Theorem 11 provides a concrete construction.

## 7. Proposition 13.7 — global Laplace linearity can fail under switching

Consider a scalar switched system

\[
\dot x=
\begin{cases}
-a_1x,&t<t_s,\\
-a_2x,&t\geq t_s,
\end{cases}
\]

with \(a_1\neq a_2\). Its trajectory is piecewise exponential:

\[
x(t)=
\begin{cases}
x_0e^{-a_1t},&t<t_s,\\
x_0e^{-a_1t_s}e^{-a_2(t-t_s)},&t\geq t_s.
\end{cases}
\]

No single scalar pole reproduces both decay rates exactly over an interval containing the switch. Therefore a fixed global pole model is misspecified. Window-local modes, switching variables, or residual error are required.

## 8. Proposition 13.8 — support labels are threshold dependent

Let a Gramian have eigenvalue \(\lambda\). The corresponding mode is observable when \(\lambda\geq\tau_o\) and unobservable when \(\lambda<\tau_o\). An arbitrarily small change in \(\tau_o\) around \(\lambda\) changes the discrete assignment.

### Consequence

Hard support should be accompanied by:

- the eigenvalue margin to the threshold;
- a sensitivity sweep;
- posterior uncertainty or a soft observability score for near-threshold modes.

## 9. Identifiability conditions worth testing

The following conditions are not guaranteed by architecture:

1. **paired excitation:** paired domains observe the same latent event;
2. **spectral separation:** modal slots are separated enough to avoid permutation;
3. **operator diversity:** source acquisition operators jointly constrain the shared state;
4. **semantic anchoring:** canonical transport cannot permute task meanings;
5. **posterior calibration:** unobserved modes have honest conditional uncertainty;
6. **local adequacy:** modal residual remains bounded on the analysis window.

## 10. Required negative controls

A credible experiment suite must include:

- empty common support;
- mislabeled acquisition operator;
- class-permuted but marginally aligned domains;
- same posterior mean with different posterior variance;
- frequency aliasing without anti-alias filtering;
- a switching trajectory outside the fixed-pole model;
- near-threshold observable modes;
- correlated shared/private modes violating product OT assumptions.

## 11. Scientific boundary

The theory supports the statement:

> A unified representation can be constructed and has explicit invariants under stated observability and regularity assumptions.

It does not support the unconditional statement:

> Every heterogeneous time series admits a unique, learnable, semantically aligned unified representation.
