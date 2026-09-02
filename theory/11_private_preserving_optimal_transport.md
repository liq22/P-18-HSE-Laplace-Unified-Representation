# Theorem 11 — Product-case optimality of private-identity transport

## Status

**Proved only for a product source law, an unchanged private marginal and an
additive cost.**

## Purpose

Identity preservation of observed-private coordinates is a method design
constraint. Under a special product model it is also optimal transport. This
document states the narrow case precisely and prevents it from being presented
as a general private-preserving OT theorem.

## 1. Product model

Let

\[
\mu
=
\mu_c\otimes\mu_p
\]

and

\[
\nu
=
\nu_c\otimes\mu_p
\]

on \(\mathcal H_c\times\mathcal H_p\). Let

\[
c((x,p),(y,q))
=
c_c(x,y)
+
\lambda\|p-q\|_2^2,
\qquad
\lambda>0.
\tag{11.1}
\]

## 2. Lemma 11.1 — joint couplings induce shared couplings

If \(\Pi\in\Pi(\mu,\nu)\), its \((x,y)\)-marginal belongs to
\(\Pi(\mu_c,\nu_c)\).

### Proof

The source and target marginals of \(x\) and \(y\) are \(\mu_c\) and
\(\nu_c\), respectively. ∎

## 3. Lemma 11.2 — lower bound

Every admissible coupling satisfies

\[
\int c\,d\Pi
\geq
\inf_{\pi_c\in\Pi(\mu_c,\nu_c)}
\int c_c\,d\pi_c.
\]

### Proof

The private cost is non-negative. The remaining shared term is evaluated under
a valid shared coupling by Lemma 11.1. ∎

## 4. Lemma 11.3 — identity-private construction

Let \(\pi_c^*\) be an optimal shared coupling. Draw

\[
(X,Y)\sim\pi_c^*,
\qquad
P\sim\mu_p
\]

independently, and set \(Q=P\). The resulting joint coupling is feasible and
has cost equal to the optimal shared cost.

### Proof

Product independence gives source law
\(\mu_c\otimes\mu_p\) and target law
\(\nu_c\otimes\mu_p\). The private cost is zero almost surely. ∎

## 5. Theorem 11 — product-case optimality

There exists an optimal coupling with

\[
\boxed{Q=P\quad\text{almost surely}.}
\]

If an optimal deterministic shared map \(T_c\) exists, then

\[
T(x,p)
=
(T_c(x),p)
\]

is an optimal deterministic map from \(\mu\) to \(\nu\).

### Detailed proof

Lemma 11.2 gives a lower bound equal to the optimal shared cost. Lemma 11.3
constructs a feasible joint coupling attaining that lower bound while leaving
the private coordinate unchanged. Hence it is globally optimal in the stated
product model.

For a deterministic \(T_c\),

\[
T_\#(\mu_c\otimes\mu_p)
=
(T_c)_\#\mu_c\otimes(I)_\#\mu_p
=
\nu_c\otimes\mu_p,
\]

and the private cost remains zero. ∎

## 6. Counterexample — correlated private structure

Let \(X=P\in\{-1,1\}\) with equal probability. Suppose the target requires
\(Y=-Q\) while preserving the same one-dimensional marginals. The identity
private map cannot in general realize that target joint dependence together
with an arbitrary shared map. Marginal agreement is insufficient.

## 7. Method interpretation

The final method preserves observed-private coordinates because changing them
would destroy acquisition-specific evidence, not because Theorem 11 applies to
all PHM distributions. When shared and private coordinates are dependent,
identity preservation remains an explicit constrained objective.

## 8. Failure boundaries

1. Shared and private independence may be false.
2. The canonical target may change their conditional dependence.
3. A non-additive cost can reward private changes.
4. The theorem does not justify transporting recoverable-missing or global-null
   coordinates.
5. Product-case optimality does not imply semantic alignment of the shared map.

## 9. Experimental implication

Report:

- dependence between shared and private coordinates;
- private drift under every alignment baseline;
- task utility of the joint representation;
- whether the canonical target changes conditional private distributions.

When dependence is strong, cite this theorem only as a special case and
describe identity preservation as a design constraint.
