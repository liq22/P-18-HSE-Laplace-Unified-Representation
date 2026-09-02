# Theorem 18 — Population and eventwise canonicality

## Status

**Proved for measurable population transports and squared-error paired anchors.**

## Purpose

Two notions of canonical representation must not be conflated.

1. Population canonicality matches a source-domain marginal to a common law.
2. Eventwise canonicality maps different acquisition views of the same latent
   event to the same physical anchor.

Only the second directly preserves event correspondence.

## 1. Population canonicality

Let

\[
C_d\sim\mu_d^c
\]

be the shared state in source domain \(d\). A measurable map \(T_d\) is
population-canonical when

\[
(T_d)_\#\mu_d^c=\mu_*^c.
\]

### Theorem 18.1

If the push-forward condition holds, then

\[
\operatorname{Law}(T_dC_d\mid d)=\mu_*^c.
\]

It does not follow that

\[
\operatorname{Law}(T_dC_d\mid O_d=o)=\mu_*^c
\]

for each observation.

### Proof

The first statement is the definition of push-forward. For the
non-implication, let \(O_d=C_d\) reveal the state exactly. Then the conditional
law of \(T_dC_d\) given \(O_d=o\) is a point mass at \(T_d(o)\), which cannot
equal a non-degenerate \(\mu_*^c\). ∎

## 2. Eventwise anchor objective

Suppose paired events provide a reference shared coordinate \(C^\dagger\) and a
domain-specific coordinate \(C_d\). Consider

\[
\mathcal J(T)
=
\mathbb E\|T(C_d)-C^\dagger\|_2^2.
\]

### Lemma 18.1 — optimal regression map

Among measurable square-integrable maps,

\[
T_d^*(c)
=
\mathbb E[C^\dagger\mid C_d=c]
\]

minimizes \(\mathcal J\).

### Proof

Condition on \(C_d=c\). For any vector \(a\),

\[
\mathbb E[
\|a-C^\dagger\|^2\mid C_d=c
]
=
\|a-\mathbb E[C^\dagger\mid C_d=c]\|^2
+
\operatorname{tr}
\operatorname{Cov}(C^\dagger\mid C_d=c).
\]

The second term does not depend on \(a\), so the conditional mean minimizes the
conditional risk. Integrate over \(c\). ∎

## 3. Theorem 18.2 — exact eventwise canonicality under deterministic invertibility

If there exists a measurable map \(\tau_d\) such that

\[
C^\dagger=\tau_d(C_d)
\quad\text{almost surely},
\]

then

\[
T_d^*=\tau_d
\quad\text{almost surely}
\]

and

\[
\boxed{
\mathbb E\|T_d^*(C_d)-C^\dagger\|^2=0.
}
\]

### Proof

Under deterministic dependence,

\[
\mathbb E[C^\dagger\mid C_d]
=
\tau_d(C_d).
\]

Apply Lemma 18.1. ∎

## 4. Relationship between the notions

Exact eventwise canonicality implies matched population marginals when all
domains share the same anchor law. The converse is false because population
matching can permute events.

## 5. Canonical-target hierarchy

Use the strongest available target in this order:

```text
known simulator modal state
paired high-fidelity acquisition
paired eventwise source anchor
source-only physically ordered barycenter
unpaired population barycenter
```

The last option supports only a population statement and requires the semantic
tests in Theory 19.

## 6. Failure boundaries

1. Paired events can have measurement error in the anchor.
2. Conditional means can blur multimodal event correspondences.
3. A barycenter can be non-unique.
4. Eventwise zero error does not prove physical correctness of the anchor.
5. Target-domain data cannot define a source-only anchor.

## 7. Experimental implication

Report both:

- eventwise paired canonical error;
- source-population distribution discrepancy.

Do not use the second as a substitute for the first.
