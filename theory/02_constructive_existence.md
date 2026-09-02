# Theorem 2 — Constructive existence of a source-supported unified representation

## Status

**Proved under Axioms A0–A8 and the additional regularity stated below.**

## Purpose

This theorem proves that the revised four-block object is mathematically
well-defined. It also corrects two possible overclaims:

1. canonicalization is a source-population marginal property, not equality of
   every observation-conditioned posterior with one barycenter;
2. global-null modes are not included in data-driven recovery claims.

The theorem does not establish identifiability or learnability from finite PHM
data.

## 1. Target object

For domain \(d\), Theorem 1 gives

\[
\Theta
=
\Theta_c+\Theta_{p,d}+\Theta_{m,d}+\Theta_0.
\]

The data-supported latent variable is

\[
\Theta_d^{\mathrm{sup}}
=
(\Theta_c,\Theta_{p,d},\Theta_{m,d}).
\]

The representation for observation \(o\) is

\[
\mu_d^U(\cdot\mid o)
=
\operatorname{Law}
\left(
T_d\Theta_c,
\Theta_{p,d},
\Theta_{m,d}
\mid
\mathcal O_d=o
\right).
\tag{2.1}
\]

The global-null projector \(P_0\) is returned as support metadata, but
\(\Theta_0\) is not called a recovered component.

## 2. Additional assumptions

### Assumption E1 — source shared marginals

For each source domain,

\[
\mu_d^c
=
\operatorname{Law}(\Theta_c\mid d)
\in
\mathcal P_2(\mathcal H_c).
\]

### Assumption E2 — source-only canonical target

Weights satisfy

\[
\alpha_d>0,
\qquad
\sum_d\alpha_d=1,
\]

and the canonical shared population law is a source-only solution of

\[
\mu_*^c
\in
\arg\min_{\mu\in\mathcal P_2(\mathcal H_c)}
\sum_d\alpha_dW_2^2(\mu_d^c,\mu).
\tag{2.2}
\]

A paired physical anchor may replace the barycenter. No held-out target data
define the anchor.

### Assumption E3 — deterministic transport when claimed

A deterministic map \(T_d\) is asserted only when the source shared law is
absolutely continuous and the chosen cost satisfies the conditions of a Monge
solution. Otherwise the construction uses a coupling.

### Assumption E4 — source support for the missing block

Every coordinate in \(\mathcal H_{m,d}\) is structurally observable in at
least one declared source domain by definition. Learning a conditional model
additionally requires paired events, shared physical anchors or another
declared source-supported identification mechanism. The theorem proves
existence of the conditional law, not that a finite dataset identifies it.

### Assumption E5 — dynamic regularity

The shared ODE and the recoverable-missing SDE satisfy the regularity required
for existence on the finite transport interval.

## 3. Lemma 2.1 — the supported conditional posterior exists

There exists a regular conditional probability kernel

\[
q_d^{\mathrm{sup}}(B\mid o)
=
\mathbb P(
\Theta_d^{\mathrm{sup}}\in B
\mid
\mathcal O_d=o)
\]

on

\[
\mathcal H_c
\times
\mathcal H_{p,d}
\times
\mathcal H_{m,d},
\]

unique for \(\mathbb P_{\mathcal O_d}\)-almost every \(o\).

### Proof

The ambient modal space is finite dimensional and therefore Polish. Orthogonal
projection onto the three supported blocks is a continuous linear map. Its
image is again a standard Borel space. Axiom A7 then gives a regular
conditional probability for the projected latent state. ∎

## 4. Lemma 2.2 — a source-population canonical law exists

The objective in Equation (2.2) has at least one minimizer.

### Proof

Choose a minimizing sequence \(\{\nu_n\}\). Bounded objective value relative
to any fixed source law gives a uniform second-moment bound through the
triangle inequality in \(W_2\). The sequence is tight, so Prokhorov's theorem
gives a weakly convergent subsequence. Uniform integrability of second moments
and lower semicontinuity of \(W_2^2\) imply that the limit attains the
infimum. Uniqueness is not claimed without additional assumptions. ∎

## 5. Lemma 2.3 — shared transport exists in coupling form

For each source law \(\mu_d^c\), the quadratic Kantorovich problem between
\(\mu_d^c\) and \(\mu_*^c\) has an optimal coupling

\[
\pi_d^*
\in
\Pi(\mu_d^c,\mu_*^c).
\]

If \(\mu_d^c\) is absolutely continuous, a Brenier map exists almost
everywhere:

\[
T_d=\nabla\varphi_d,
\qquad
(T_d)_\#\mu_d^c=\mu_*^c.
\]

### Proof

Finite second moments give tightness of admissible couplings and finite
quadratic cost. Lower semicontinuity yields a Kantorovich minimizer. The
deterministic statement is the finite-dimensional Brenier result under
absolute continuity. ∎

## 6. Lemma 2.4 — the conditional push-forward is well-defined

Let

\[
F_d(c,p,m)
=
(T_d(c),p,m).
\]

Then

\[
\mu_d^U(\cdot\mid o)
=
(F_d)_\#
q_d^{\mathrm{sup}}(\cdot\mid o)
\]

is a probability kernel.

### Proof

The map \(F_d\) is measurable. A measurable push-forward of a probability
kernel is a probability kernel. ∎

## 7. Lemma 2.5 — canonicality is a population statement

Averaging the conditional representation over observations from source domain
\(d\), the shared marginal satisfies

\[
\operatorname{Law}(T_d\Theta_c\mid d)
=
\mu_*^c.
\tag{2.3}
\]

Equation (2.3) does not imply

\[
\operatorname{Law}
(T_d\Theta_c\mid\mathcal O_d=o)
=
\mu_*^c
\]

for every \(o\).

### Proof

The first equality follows directly from
\((T_d)_\#\mu_d^c=\mu_*^c\). For the non-implication, consider an observation
that exactly identifies \(\Theta_c\). The conditional law is then a point
mass, while a non-degenerate population barycenter is not. ∎

## 8. Lemma 2.6 — triangular dynamic realization

Suppose the shared flow solves

\[
\frac{dC_t}{dt}
=
v_t^c(C_t,a_d),
\]

the private block solves

\[
dP_t=0,
\]

and the missing block solves

\[
dM_t
=
b_t^m(
M_t,C_t,P_t,\mathcal O_d)\,dt
+
\sigma_t^m(
M_t,C_t,P_t,\mathcal O_d)\,dW_t.
\]

Under Assumption E5, these equations admit a finite-interval solution. The
missing posterior may condition on the evolving or terminal canonical shared
state; order independence is not claimed for this triangular model.

### Proof

Solve the shared ODE first under the standard local-Lipschitz and linear-growth
conditions. The private solution is constant. Substituting the resulting
adapted shared path and fixed private path into the missing SDE leaves a
time-inhomogeneous SDE with the stated well-posedness assumptions. ∎

## 9. Theorem 2 — constructive existence

Under the preceding assumptions, for every source domain \(d\) and almost
every observation \(o\), the source-supported representation in Equation
(2.1) exists. Its properties are:

1. the source-domain population marginal of the shared coordinate is
   \(\mu_*^c\);
2. the observed-private coordinate is unchanged;
3. the recoverable-missing coordinate remains a conditional probability law;
4. the global-null support is declared but excluded from data-driven recovery.

### Detailed proof

Theorem 1 supplies unique orthogonal projections onto the four blocks.
Lemma 2.1 supplies the conditional posterior of the three source-supported
blocks. Lemma 2.3 supplies a source-to-canonical shared coupling or map. Lemma
2.4 applies that map to the conditional posterior while leaving the other
supported coordinates unchanged. Lemma 2.5 gives population canonicality.
Lemma 2.6 supplies a triangular ODE/SDE realization when a dynamic
implementation is required. The global-null block is outside the supported
product space and therefore receives no learned recovery semantics. ∎

## 10. Corollary 2.1 — finite summaries

If the recoverable-missing posterior has finite second moment, then

\[
\mathbb E[
\Theta_{m,d}\mid\mathcal O_d],
\qquad
\operatorname{Cov}(
\Theta_{m,d}\mid\mathcal O_d)
\]

exist. A tensor interface may store samples or moments, structural support,
instance reliability and the global-null mask. A posterior mean alone is not
equivalent to the full measure.

## 11. Failure boundaries

1. A canonical population marginal does not guarantee semantic alignment.
2. A source-supported missing coordinate may still be statistically
   unidentifiable without paired excitation or a physical anchor.
3. A deterministic Monge map may not exist.
4. The barycenter may be non-unique.
5. Strong shared–private dependence can make an identity-private target
   incompatible with a desired joint canonical law.
6. The global-null classification depends on the declared source operator set.
7. The theorem proves existence, not posterior calibration or finite-sample
   learnability.

## 12. Experimental implication

A valid prototype must show:

1. all four projectors form a direct sum;
2. source-population shared marginals, not per-observation posteriors, are used
   for the canonicality claim;
3. observed-private coordinates are unchanged;
4. recoverable-missing coordinates have at least two posterior samples or an
   explicit parametric distribution;
5. global-null coordinates are marked unsupported;
6. target-domain observations do not define structural support or the
   canonical target;
7. a paired or physical anchor prevents class-permuting transport.
