# Theorem 1 — Four-way observable-support decomposition

## Status

**Proved under Axioms A0–A3 for fixed structural acquisition operators.**

## Purpose

A three-block split into shared, observed-private and unobserved components is
too coarse. Its unobserved block mixes:

1. modes hidden in the current domain but observed by another source domain;
2. modes unsupported by every source domain.

Only the first class can receive a data-supported recovery claim. This document
proves the four-way orthogonal decomposition used by the revised method.

## 1. Definitions

For every source domain \(d\), let

\[
P_d^o
=
\mathbf 1_{[\tau_o,\infty)}(G_d),
\qquad
\mathcal H_d^o=\operatorname{Range}(P_d^o).
\]

Define

\[
\mathcal H_c
=
\bigcap_{j=1}^{D}\mathcal H_j^o
\]

and

\[
\mathcal H_\cup
=
\sum_{j=1}^{D}\mathcal H_j^o,
\]

where the sum denotes the linear span of the union.

For a fixed domain \(d\),

\[
\mathcal H_{p,d}
=
\mathcal H_d^o\cap\mathcal H_c^\perp,
\]

\[
\mathcal H_{m,d}
=
\mathcal H_\cup\cap(\mathcal H_d^o)^\perp,
\]

\[
\mathcal H_0
=
\mathcal H_\cup^\perp.
\]

The symbol \(p\) denotes observed-private, \(m\) denotes
recoverable-missing, and \(0\) denotes source-global null support.

## 2. Lemma 1.1 — nested structural subspaces

For every domain \(d\),

\[
\mathcal H_c
\subseteq
\mathcal H_d^o
\subseteq
\mathcal H_\cup.
\]

### Proof

The first inclusion follows from the definition of an intersection. The second
follows because \(\mathcal H_\cup\) is the span of all source observable
subspaces and therefore contains each term in the span. ∎

## 3. Lemma 1.2 — observable support splits into common and private parts

For every domain \(d\),

\[
\mathcal H_d^o
=
\mathcal H_c
\oplus
\mathcal H_{p,d}.
\]

### Proof

Take \(x\in\mathcal H_d^o\). Because \(\mathcal H_c\) is a closed
finite-dimensional subspace, write

\[
x=P_cx+(I-P_c)x.
\]

By Lemma 1.1, \(P_cx\in\mathcal H_d^o\). Hence the residual also belongs to
\(\mathcal H_d^o\). Orthogonal projection gives
\((I-P_c)x\in\mathcal H_c^\perp\), so

\[
(I-P_c)x
\in
\mathcal H_d^o\cap\mathcal H_c^\perp
=
\mathcal H_{p,d}.
\]

The intersection of the two summands is \(\{0\}\), and they are orthogonal by
construction. ∎

## 4. Lemma 1.3 — source-observable span splits into current support and missing support

For every domain \(d\),

\[
\mathcal H_\cup
=
\mathcal H_d^o
\oplus
\mathcal H_{m,d}.
\]

### Proof

Lemma 1.1 gives \(\mathcal H_d^o\subseteq\mathcal H_\cup\). Apply the
standard orthogonal decomposition of the larger subspace relative to its closed
subspace:

\[
\mathcal H_\cup
=
\mathcal H_d^o
\oplus
\left[
\mathcal H_\cup\cap(\mathcal H_d^o)^\perp
\right].
\]

The second term is exactly \(\mathcal H_{m,d}\). ∎

## 5. Theorem 1 — unique four-way direct sum

For every source domain \(d\),

\[
\boxed{
\mathcal H
=
\mathcal H_c
\oplus
\mathcal H_{p,d}
\oplus
\mathcal H_{m,d}
\oplus
\mathcal H_0
}
\]

and every modal state has a unique representation

\[
\Theta
=
\Theta_c
+
\Theta_{p,d}
+
\Theta_{m,d}
+
\Theta_0.
\]

### Detailed proof

The source-observable span is closed because the ambient space is finite
dimensional. Therefore

\[
\mathcal H
=
\mathcal H_\cup
\oplus
\mathcal H_\cup^\perp
=
\mathcal H_\cup
\oplus
\mathcal H_0.
\tag{1.1}
\]

By Lemma 1.3,

\[
\mathcal H_\cup
=
\mathcal H_d^o
\oplus
\mathcal H_{m,d}.
\tag{1.2}
\]

By Lemma 1.2,

\[
\mathcal H_d^o
=
\mathcal H_c
\oplus
\mathcal H_{p,d}.
\tag{1.3}
\]

Substituting (1.3) into (1.2), then into (1.1), yields the displayed four-way
sum.

The summands are pairwise orthogonal:

- \(\mathcal H_c\perp\mathcal H_{p,d}\) by definition;
- both are contained in \(\mathcal H_d^o\), while
  \(\mathcal H_{m,d}\subseteq(\mathcal H_d^o)^\perp\);
- the first three are contained in \(\mathcal H_\cup\), while
  \(\mathcal H_0=\mathcal H_\cup^\perp\).

Existence follows by applying the four orthogonal projectors. Uniqueness follows
because an orthogonal direct-sum decomposition has unique coordinates: if two
such decompositions exist, subtract them and take inner products with each
summand. Every squared norm is zero. ∎

## 6. Lemma 1.4 — projector formulas

Let \(P_\cup\) be the orthogonal projector onto \(\mathcal H_\cup\). Then

\[
P_{p,d}=P_d^o-P_c,
\]

\[
P_{m,d}=P_\cup-P_d^o,
\]

\[
P_0=I-P_\cup.
\]

### Proof

For nested closed subspaces \(\mathcal U\subseteq\mathcal V\), their
orthogonal projectors commute and \(P_\mathcal V-P_\mathcal U\) is the
projector onto \(\mathcal V\cap\mathcal U^\perp\). Apply this fact to
\(\mathcal H_c\subseteq\mathcal H_d^o\) and
\(\mathcal H_d^o\subseteq\mathcal H_\cup\). The final formula is the standard
orthogonal-complement projector. ∎

## 7. Lemma 1.5 — spectral characterizations

Let

\[
S=\sum_{d=1}^{D}P_d^o.
\]

Then

\[
\mathcal H_c
=
\operatorname{Eig}(S,D),
\]

and

\[
\mathcal H_\cup
=
\operatorname{Range}(S).
\]

### Proof

If \(x\in\mathcal H_c\), then \(P_d^ox=x\) for all \(d\), hence \(Sx=Dx\).
Conversely, if \(Sx=Dx\), then

\[
D\|x\|^2
=
\sum_d\langle x,P_d^ox\rangle
=
\sum_d\|P_d^ox\|^2.
\]

Each term is at most \(\|x\|^2\); equality of the sum requires
\(P_d^ox=x\) for every \(d\). Thus \(x\in\mathcal H_c\).

For the union, the null space of \(S\) is

\[
\ker S
=
\bigcap_d\ker P_d^o
=
\left(
\sum_d\operatorname{Range}(P_d^o)
\right)^\perp.
\]

Therefore \(\operatorname{Range}(S)=\mathcal H_\cup\). ∎

## 8. Fixed modal-slot special case

For the first learned model, the project uses a declared modal dictionary in
which the structural Gramian is approximately diagonal:

\[
G_d
\approx
\operatorname{diag}(g_{d,1},\ldots,g_{d,K}).
\]

Each slot can then be categorized without rotating the token basis:

- shared when every source has structural support;
- observed-private when the current source has support but at least one source
  does not;
- recoverable-missing when the current source lacks support but another source
  has it;
- global-null when no source has support.

Near the threshold, use the soft weight

\[
o_{d,k}
=
\sigma((g_{d,k}-\tau_o)/T_o)
\]

and report the margin \(|g_{d,k}-\tau_o|\). The exact theorem remains the
hard-support reference.

## 9. Structural support versus instance reliability

The decomposition is based on domain-level acquisition capability \(A_d\).
A sample-level mask or low SNR instead changes

\[
r_{d,i,k}\in[0,1].
\]

A low reliability may broaden the posterior of a structurally observable slot,
but it does not convert the scientific definition into a different
sample-specific subspace. This separation keeps token slots fixed and avoids a
different representation dimension for every sample.

## 10. Failure boundaries

1. Exact intersections of estimated dense projectors are numerically fragile.
2. Adding a very narrow acquisition domain can shrink \(\mathcal H_c\).
3. A misspecified \(A_d\) yields the wrong four-way assignment.
4. Hard threshold assignments can flip near \(\tau_o\).
5. Recoverable-missing means supported somewhere in the declared source set; it
   does not by itself prove paired data or a learnable conditional posterior.
6. Global-null is protocol dependent. Additional sensors can move a mode from
   \(\mathcal H_0\) into \(\mathcal H_\cup\).

## 11. Experimental implication

The analytic and known-pole experiments must cover:

1. complete overlap;
2. partial overlap;
3. empty common support;
4. current-domain missing but another-source observable support;
5. support absent from every source domain;
6. a near-threshold slot;
7. perturbation of the estimated projector.

The implementation must return a zero-dimensional block when any category is
empty. It must never manufacture a positive shared or recoverable dimension.
