# Theorem 2 — Constructive existence of the unified representation

## Status

**Proved under Axioms A0–A8 and the additional regularity stated below.**

## Purpose

This document proves that the proposed object is mathematically well-defined. The result is an existence theorem. It does not establish that the object is identifiable from finite data or that a neural network can learn it efficiently.

## 1. Target object

For domain \(d\), let

\[
\Theta=(\Theta_c,\Theta_{p,d},\Theta_{u,d})
\]

be the unique decomposition from Theorem 1. The desired unified representation is

\[
\mu_d^U
=
\operatorname{Law}
\left(
T_d\Theta_c,
\Theta_{p,d},
\Theta_{u,d}
\mid\mathcal O_d
\right).
\]

The map \(T_d\) transports the shared marginal to a source-only canonical shared distribution. The private coordinate uses the identity. The unobserved coordinate remains random under the conditional posterior.

## 2. Additional assumptions

### Assumption E1 — source shared marginals

For every source domain \(d\), the conditional or population shared marginal

\[
\mu_d^c=\operatorname{Law}(\Theta_c\mid d)
\]

belongs to \(\mathcal P_2(\mathcal H_c)\).

### Assumption E2 — barycenter weights

The source weights satisfy

\[
\alpha_d>0,
\qquad
\sum_{d=1}^{D}\alpha_d=1.
\]

### Assumption E3 — deterministic map when requested

A deterministic transport map is asserted only if \(\mu_d^c\) is absolutely continuous with respect to Lebesgue measure on \(\mathcal H_c\). Without this condition, the theorem uses an optimal coupling rather than claiming a Monge map.

### Assumption E4 — flow regularity

When a dynamic realization is required, its vector field is measurable in time, locally Lipschitz in state, and of at most linear growth.

### Assumption E5 — diffusion regularity

The unobserved-block conditional SDE has drift and diffusion coefficients satisfying global or local conditions sufficient for non-explosion and uniqueness on the finite transport interval.

## 3. Lemma 2.1 — existence of the conditional modal posterior

### Statement

There exists a regular conditional probability kernel

\[
q_d(B\mid o)
=
\mathbb P(\Theta\in B\mid\mathcal O_d=o)
\]

for Borel sets \(B\subseteq\mathcal H\), unique for \(\mathbb P_{\mathcal O_d}\)-almost every \(o\).

### Proof

By Axiom A0, \(\mathcal H=\mathbb R^m\) is a Polish space and hence a standard Borel space. The observation space, constructed from finite real arrays, masks, and metadata, is also assumed standard Borel by Axiom A7. For random elements taking values in standard Borel spaces, the disintegration theorem gives a regular conditional probability kernel. Therefore \(q_d(\cdot\mid o)\) exists and is unique outside an observation-null set. ∎

## 4. Lemma 2.2 — existence of a canonical shared barycenter

### Statement

The functional

\[
F(\mu)
=
\sum_{d=1}^{D}
\alpha_dW_2^2(\mu_d^c,\mu)
\]

has at least one minimizer \(\mu_*^c\in\mathcal P_2(\mathcal H_c)\).

### Proof sketch with the compactness steps made explicit

1. Choose a minimizing sequence \(\{\mu_n\}\) such that

   \[
   F(\mu_n)\downarrow\inf_{\mu}F(\mu).
   \]

2. Fix one source distribution \(\mu_1^c\). Since \(F(\mu_n)\) is bounded, the term

   \[
   \alpha_1W_2^2(\mu_1^c,\mu_n)
   \]

   is bounded. The triangle inequality in \(W_2\) implies a uniform second-moment bound on \(\mu_n\).

3. A uniform second-moment bound gives tightness. By Prokhorov's theorem, there is a weakly convergent subsequence

   \[
   \mu_{n_k}\Rightarrow\mu_*.
   \]

4. Uniform integrability of the second moments promotes the convergence to the topology required for lower semicontinuity of \(W_2^2\).

5. For each fixed \(d\),

   \[
   W_2^2(\mu_d^c,\mu_*)
   \leq
   \liminf_{k\to\infty}
   W_2^2(\mu_d^c,\mu_{n_k}).
   \]

6. Summing with positive weights gives

   \[
   F(\mu_*)
   \leq
   \liminf_{k\to\infty}F(\mu_{n_k})
   =
   \inf_\mu F(\mu).
   \]

Hence \(\mu_*^c=\mu_*\) is a minimizer. ∎

The proof uses standard finite-dimensional Wasserstein compactness. Uniqueness requires additional conditions and is not claimed here.

## 5. Lemma 2.3 — existence of shared transport

### Coupling form

For any \(\mu_d^c,\mu_*^c\in\mathcal P_2(\mathcal H_c)\), the quadratic Kantorovich problem has at least one optimal coupling

\[
\pi_d^*\in\Pi(\mu_d^c,\mu_*^c).
\]

### Deterministic-map form

If \(\mu_d^c\) is absolutely continuous, then under quadratic cost there exists an almost-everywhere unique optimal map

\[
T_d=\nabla\varphi_d
\]

for a convex potential \(\varphi_d\), satisfying

\[
(T_d)_\#\mu_d^c=\mu_*^c.
\]

### Justification

Existence of an optimal coupling follows from tightness of couplings, lower semicontinuity of the quadratic cost, and finite second moments. The deterministic result is the finite-dimensional Brenier theorem under absolute continuity of the source measure. ∎

## 6. Lemma 2.4 — existence of dynamic realizations

### ODE block

Let \(v_t^c\) satisfy Assumption E4. Then, for each initial shared coordinate, the ODE

\[
\frac{dZ_c}{dt}=v_t^c(Z_c)
\]

has a unique maximal solution. The linear-growth condition prevents explosion on the finite interval \([0,1]\), so the flow map \(\Phi_{d,t}^c\) exists.

### SDE block

Let \(b_t^u\) and \(\sigma_t^u\) satisfy Assumption E5. Then

\[
dZ_u=b_t^u(Z_u)dt+\sigma_t^u(Z_u)dW_t
\]

has a unique strong solution on \([0,1]\).

### Private block

The equation

\[
dZ_p=0
\]

has the unique solution \(Z_p(t)=Z_p(0)\).

These are standard finite-dimensional well-posedness results under the stated Lipschitz and growth conditions. ∎

## 7. Theorem 2 — existence of a distribution-valued unified representation

### Statement

Under the preceding assumptions, for every acquisition domain \(d\) and almost every observation \(o\), there exists a probability measure

\[
\boxed{
\mu_d^U(\cdot\mid o)
}
\]

on

\[
\mathcal H_c
\times
\mathcal H_{p,d}
\times
\mathcal H_{u,d}
\]

whose components are:

1. a shared coordinate with canonical marginal \(\mu_*^c\);
2. the unchanged observed-private coordinate;
3. the conditional posterior of the unobserved coordinate.

### Detailed construction

1. From Theorem 1, decompose the posterior kernel using the measurable linear map

   \[
   L_d:\Theta\mapsto
   (P_c\Theta,P_{p,d}\Theta,P_{u,d}\Theta).
   \]

   The push-forward

   \[
   \widetilde q_d
   =(L_d)_\#q_d
   \]

   is a conditional probability measure on the product space.

2. Let \(T_d\) be a deterministic optimal map when Assumption E3 holds. Otherwise augment the probability space with an optimal coupling kernel from Lemma 2.3. For notational clarity, use the deterministic case first.

3. Define the measurable block map

   \[
   F_d(c,p,u)
   =
   (T_d(c),p,u).
   \]

4. Define

   \[
   \mu_d^U
   =(F_d)_\#\widetilde q_d.
   \]

   A measurable push-forward of a probability measure is a probability measure, so \(\mu_d^U\) exists.

5. Its shared population marginal is canonical:

   \[
   \operatorname{Law}(T_d\Theta_c\mid d)
   =(T_d)_\#\mu_d^c
   =\mu_*^c.
   \]

6. Its observed-private coordinate is unchanged because the second component of \(F_d\) is the identity.

7. Its unobserved coordinate is the conditional posterior inherited from \(q_d\), not a deterministic imputation.

8. Lemma 2.4 provides a dynamic ODE/SDE realization when required.

Therefore the unified representation exists. ∎

## 8. Corollary 2.1 — finite tensor summaries exist under finite moments

If the conditional unobserved posterior has finite second moment, then the following quantities exist:

\[
\mathbb E[\Theta_u\mid\mathcal O_d],
\qquad
\operatorname{Cov}(\Theta_u\mid\mathcal O_d).
\]

A finite interface can store canonical shared coordinates, observed-private coordinates, posterior samples or moments, and observability masks. This does not make the mean alone equivalent to the full measure.

## 9. What this theorem does not prove

The theorem does not establish:

- uniqueness of the barycenter in every case;
- semantic alignment of the optimal transport;
- identifiability of \(A_d\) or the projectors;
- posterior calibration;
- learnability from finite samples;
- superiority over a metadata-conditioned baseline.

These are separate hypotheses.

## 10. Falsifiable implementation consequences

A constructive prototype must show:

1. projectors form a direct-sum decomposition;
2. a source-only canonical shared target is defined;
3. private coordinates are passed through unchanged;
4. unobserved coordinates are represented by at least two posterior samples or a declared parametric distribution;
5. an empty shared subspace remains empty;
6. no target-domain data define the canonical distribution.
