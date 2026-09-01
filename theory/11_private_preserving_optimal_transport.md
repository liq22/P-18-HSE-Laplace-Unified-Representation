# Theorem 11 — Private-preserving optimal transport

## Status

**Proved under a product-measure assumption and an additive transport cost.**

## Purpose

The shared block must be transported to canonical coordinates, while the observed-private block should remain unchanged. This theorem shows that identity on the private block is not only feasible but optimal under explicit assumptions.

## 1. Measures and cost

Let the source representation distribution factor as

\[
\mu=
\mu_c\otimes\mu_p
\]

on \(\mathcal H_c\times\mathcal H_p\). Let the canonical target preserve the same private marginal:

\[
\nu=
\nu_c\otimes\mu_p.
\]

Let the transport cost be additive:

\[
c((x,p),(y,q))
=
c_c(x,y)+\lambda\|p-q\|_2^2,
\qquad
\lambda>0,
\tag{11.1}
\]

where \(c_c\geq0\) is a lower-semicontinuous shared-coordinate cost.

## 2. Lemma 11.1 — every joint coupling induces a shared coupling

### Statement

If

\[
\Pi\in\Pi(\mu,\nu),
\]

then its \((x,y)\)-marginal \(\Pi_c\) belongs to

\[
\Pi(\mu_c,\nu_c).
\]

### Proof

The first marginal of \(\Pi\) is \(\mu_c\otimes\mu_p\), so the marginal distribution of \(x\) is \(\mu_c\). The second marginal is \(\nu_c\otimes\mu_p\), so the marginal distribution of \(y\) is \(\nu_c\). Therefore the joint marginal of \((x,y)\) is a coupling between \(\mu_c\) and \(\nu_c\). ∎

## 3. Lemma 11.2 — lower bound on every admissible cost

### Statement

For every \(\Pi\in\Pi(\mu,\nu)\),

\[
\int c\,d\Pi
\geq
\inf_{\pi_c\in\Pi(\mu_c,\nu_c)}
\int c_c(x,y)d\pi_c(x,y).
\]

### Proof

By Equation (11.1),

\[
\int c\,d\Pi
=
\int c_c(x,y)d\Pi
+
\lambda\int\|p-q\|^2d\Pi.
\]

The second term is non-negative, so

\[
\int c\,d\Pi
\geq
\int c_c(x,y)d\Pi.
\]

The first term depends only on the \((x,y)\)-marginal \(\Pi_c\). By Lemma 11.1, \(\Pi_c\in\Pi(\mu_c,\nu_c)\). Hence

\[
\int c_c(x,y)d\Pi_c
\geq
\inf_{\pi_c\in\Pi(\mu_c,\nu_c)}
\int c_c d\pi_c.
\]

Combining the inequalities proves the lemma. ∎

## 4. Lemma 11.3 — construction of a private-identity coupling

Let \(\pi_c^*\) be an optimal shared coupling. Define a coupling \(\Pi^*\) by sampling

\[
(X,Y)\sim\pi_c^*,
\qquad
P\sim\mu_p
\]

independently and setting

\[
Q=P.
\]

Then \(\Pi^*\in\Pi(\mu,\nu)\), and

\[
\int c\,d\Pi^*
=
\int c_c\,d\pi_c^*.
\]

### Proof

The source pair \((X,P)\) has law \(\mu_c\otimes\mu_p=\mu\). The target pair \((Y,Q)=(Y,P)\) has law \(\nu_c\otimes\mu_p=\nu\) because \(Y\) and \(P\) are independent. Moreover,

\[
\|P-Q\|^2=0
\]

almost surely. The cost therefore reduces to the optimal shared cost. ∎

## 5. Theorem 11 — existence of an optimal private-preserving transport

### Statement

There exists an optimal coupling \(\Pi^*\) whose private coordinates satisfy

\[
\boxed{Q=P\quad\text{almost surely}.}
\]

If an optimal deterministic shared map \(T_c\) exists, then

\[
\boxed{
T(x,p)=(T_c(x),p)
}
\]

is an optimal deterministic map from \(\mu\) to \(\nu\).

### Detailed proof

Lemma 11.2 gives a lower bound equal to the optimal shared transport cost. Lemma 11.3 constructs a feasible joint coupling that attains exactly this lower bound while setting the private coordinates equal. Therefore that coupling is globally optimal.

If \(T_c\) exists and \((T_c)_\#\mu_c=\nu_c\), define

\[
T(x,p)=(T_c(x),p).
\]

Under the product source measure, its push-forward is

\[
T_\#(\mu_c\otimes\mu_p)
=
(T_c)_\#\mu_c\otimes(I)_\#\mu_p
=
\nu_c\otimes\mu_p
=
\nu.
\]

Its cost is the optimal shared cost plus zero private cost, so it is optimal. ∎

## 6. Corollary 11.1 — block-diagonal vector field

A dynamic transport realizing \(T\) may use

\[
v_t(x,p)=(v_t^c(x),0).
\]

The private component remains fixed, matching Theorem 4.

## 7. Important limitation: product independence

The product assumption

\[
\mu=
\mu_c\otimes\mu_p
\]

means shared and private coordinates are independent. This may be false in PHM data. For example, fault severity may influence both low-frequency shared energy and high-frequency private resonance.

If the source law is

\[
\mu(dx,dp)=\mu_c(dx)\kappa_x(dp),
\]

then the identity map on \(p\) transports the dependence structure according to the movement of \(x\). A target specified only through marginals may not retain the desired conditional law. The theorem cannot be applied without checking how the canonical target treats \(\kappa_x\).

## 8. Counterexample when the target changes private dependence

Let \(X=P\in\{-1,1\}\) with equal probability, so shared and private variables are perfectly correlated. Suppose the target requires \(Y=-Q\) while retaining the same individual marginals. The identity-private map \(Q=P\) combined with a shared identity map \(Y=X\) cannot satisfy the target dependence. Marginal preservation alone is insufficient.

## 9. Experimental implication

Before using this theorem as a method justification, test:

- empirical dependence between shared and private blocks;
- whether canonicalization changes conditional private distributions;
- private identity distance;
- task utility from joint versus factorized representations.

If strong shared–private dependence is observed, the paper should state that identity preservation is a design constraint, not the unique unconstrained optimal transport.
