# Theorem 1 — Observable subspace decomposition

## Status

**Proved under Axioms A0–A3.**

## Purpose

The unified representation requires a mathematically unambiguous split between:

1. modes observable in every source acquisition domain;
2. modes observable in the current domain but not in all domains;
3. modes unobservable in the current domain.

This file proves that the split is an orthogonal direct sum and therefore unique.

## 1. Definitions

For each source domain \(d\), let

\[
P_d^o
=
\mathbf 1_{[\tau_o,\infty)}(G_d),
\qquad
G_d=A_d^\top\Sigma_d^{-1}A_d.
\]

Because \(G_d\) is symmetric positive semidefinite, \(P_d^o\) is an orthogonal projector. Define

\[
\mathcal H_d^o=\operatorname{Range}(P_d^o).
\]

The common subspace is

\[
\mathcal H_c=\bigcap_{j\in\mathcal D_s}\mathcal H_j^o.
\]

For a fixed domain \(d\), define

\[
\mathcal H_{p,d}=\mathcal H_d^o\cap\mathcal H_c^\perp,
\]

\[
\mathcal H_{u,d}=(\mathcal H_d^o)^\perp.
\]

## 2. Lemma 1.1 — the common subspace is contained in each observable subspace

### Statement

For every \(d\in\mathcal D_s\),

\[
\mathcal H_c\subseteq\mathcal H_d^o.
\]

### Proof

By definition,

\[
\mathcal H_c=\bigcap_{j\in\mathcal D_s}\mathcal H_j^o.
\]

An element \(x\) belongs to an intersection only if it belongs to each set in the intersection. Hence, for every fixed \(d\),

\[
x\in\mathcal H_c
\implies
x\in\mathcal H_d^o.
\]

Therefore \(\mathcal H_c\subseteq\mathcal H_d^o\). ∎

## 3. Lemma 1.2 — an observable subspace splits into common and observed-private parts

### Statement

For every domain \(d\),

\[
\mathcal H_d^o
=
\mathcal H_c
\oplus
\left(\mathcal H_d^o\cap\mathcal H_c^\perp\right).
\]

### Proof

Take any \(x\in\mathcal H_d^o\). Because \(\mathcal H_c\) is a finite-dimensional closed subspace, the orthogonal projection \(P_cx\) exists. Write

\[
x=P_cx+(I-P_c)x.
\]

The first term satisfies

\[
P_cx\in\mathcal H_c.
\]

By Lemma 1.1, \(\mathcal H_c\subseteq\mathcal H_d^o\), so \(P_cx\in\mathcal H_d^o\). Since both \(x\) and \(P_cx\) belong to \(\mathcal H_d^o\), their difference satisfies

\[
(I-P_c)x=x-P_cx\in\mathcal H_d^o.
\]

By the defining property of an orthogonal projection,

\[
(I-P_c)x\in\mathcal H_c^\perp.
\]

Therefore

\[
(I-P_c)x
\in
\mathcal H_d^o\cap\mathcal H_c^\perp
=
\mathcal H_{p,d}.
\]

Thus every \(x\in\mathcal H_d^o\) is the sum of an element of \(\mathcal H_c\) and an element of \(\mathcal H_{p,d}\).

The sum is direct because

\[
\mathcal H_c\cap\mathcal H_c^\perp=\{0\}.
\]

It is orthogonal by construction. ∎

## 4. Theorem 1 — unique three-way decomposition

### Statement

For every source acquisition domain \(d\),

\[
\boxed{
\mathcal H
=
\mathcal H_c
\oplus
\mathcal H_{p,d}
\oplus
\mathcal H_{u,d}
}
\]

and every modal state \(\Theta\in\mathcal H\) has a unique representation

\[
\Theta
=
\Theta_c+\Theta_{p,d}+\Theta_{u,d}.
\]

### Proof

Because \(\mathcal H_d^o\) is a closed subspace of a finite-dimensional Hilbert space,

\[
\mathcal H
=
\mathcal H_d^o
\oplus
(\mathcal H_d^o)^\perp.
\]

By definition,

\[
(\mathcal H_d^o)^\perp=\mathcal H_{u,d}.
\]

By Lemma 1.2,

\[
\mathcal H_d^o
=
\mathcal H_c\oplus\mathcal H_{p,d}.
\]

Substituting the second equality into the first gives

\[
\mathcal H
=
\left(
\mathcal H_c\oplus\mathcal H_{p,d}
\right)
\oplus
\mathcal H_{u,d}.
\]

The three subspaces are pairwise orthogonal:

- \(\mathcal H_{p,d}\subseteq\mathcal H_c^\perp\), hence \(\mathcal H_c\perp\mathcal H_{p,d}\);
- \(\mathcal H_c\subseteq\mathcal H_d^o\) and \(\mathcal H_{u,d}=(\mathcal H_d^o)^\perp\), hence \(\mathcal H_c\perp\mathcal H_{u,d}\);
- \(\mathcal H_{p,d}\subseteq\mathcal H_d^o\), hence \(\mathcal H_{p,d}\perp\mathcal H_{u,d}\).

For existence, set

\[
\Theta_c=P_c\Theta,
\qquad
\Theta_{p,d}=P_{p,d}\Theta,
\qquad
\Theta_{u,d}=P_{u,d}\Theta.
\]

Because the projectors sum to the identity,

\[
\Theta
=
(P_c+P_{p,d}+P_{u,d})\Theta.
\]

For uniqueness, suppose

\[
\Theta=c+p+u=c'+p'+u'
\]

with the respective terms in the three subspaces. Subtracting gives

\[
(c-c')+(p-p')+(u-u')=0.
\]

Taking the inner product with \(c-c'\) and using pairwise orthogonality yields

\[
\|c-c'\|_2^2=0,
\]

so \(c=c'\). Repeating for the other blocks yields \(p=p'\) and \(u=u'\). ∎

## 5. Lemma 1.3 — projector formulas

### Statement

For each domain \(d\),

\[
P_{p,d}=P_d^o-P_c,
\qquad
P_{u,d}=I-P_d^o.
\]

### Proof

Since \(\mathcal H_c\subseteq\mathcal H_d^o\), the orthogonal projectors commute and satisfy

\[
P_d^oP_c=P_cP_d^o=P_c.
\]

Then

\[
(P_d^o-P_c)^2
=(P_d^o)^2-P_d^oP_c-P_cP_d^o+P_c^2
=P_d^o-P_c.
\]

The matrix is symmetric, so it is an orthogonal projector. Its range is the portion of \(\mathcal H_d^o\) orthogonal to \(\mathcal H_c\), namely \(\mathcal H_{p,d}\). The formula for \(P_{u,d}\) is the standard orthogonal complement projector. ∎

## 6. Computational characterization of the intersection

Let

\[
S=\sum_{d=1}^{D}P_d^o.
\]

### Lemma 1.4

A vector \(x\) belongs to \(\mathcal H_c\) if and only if

\[
Sx=Dx.
\]

### Proof

If \(x\in\mathcal H_c\), then \(P_d^ox=x\) for every \(d\), so \(Sx=Dx\).

Conversely, suppose \(Sx=Dx\). Taking the inner product with \(x\),

\[
D\|x\|^2
=
\sum_d\langle x,P_d^ox\rangle
=
\sum_d\|P_d^ox\|^2.
\]

For an orthogonal projector, \(\|P_d^ox\|\leq\|x\|\). The sum of \(D\) non-negative terms reaches its maximum \(D\|x\|^2\) only if every term equals \(\|x\|^2\). Equality for an orthogonal projection holds exactly when \(P_d^ox=x\). Thus \(x\in\mathcal H_d^o\) for all \(d\), so \(x\in\mathcal H_c\). ∎

This is the basis of the numerical implementation: the shared basis is the eigenspace of \(\sum_dP_d^o\) with eigenvalue \(D\).

## 7. Boundary cases

### Empty shared support

It is possible that

\[
\mathcal H_c=\{0\}.
\]

The theorem still holds, but there is no non-trivial common representation. An implementation must report a zero-dimensional shared block rather than manufacture one.

### Threshold dependence

Changing \(\tau_o\) changes each \(\mathcal H_d^o\), and therefore all three blocks. The theorem proves decomposition for a fixed threshold; it does not identify the scientifically correct threshold.

### Unknown observation operator

If \(A_d\) is misspecified, the decomposition is a decomposition under the assumed operator, not necessarily under the physical acquisition system. This uncertainty is addressed by perturbation bounds and experiments, not by this theorem.

## 8. Experimental implication

A minimal test must verify:

1. \(P_c,P_{p,d},P_{u,d}\) are symmetric and idempotent;
2. pairwise products are zero;
3. their sum is the identity;
4. a domain with no common support returns \(P_c=0\);
5. target-domain data are not used to define \(P_c\) or \(\tau_o\).
