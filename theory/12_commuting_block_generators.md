# Theorem 12 — Decoupled null model for block-generator commutation

## Status

**Proved only for disjoint, non-cross-conditioned generators. This is a null
model, not the final triangular method.**

## Purpose

A useful missing-mode posterior normally conditions on the canonical shared
state. That dependency generally destroys exact commutation. This theorem is
retained to define the simpler decoupled baseline and to quantify when
flow-before-diffusion and diffusion-before-flow can be interchanged.

## 1. Decoupled coordinates

Let

\[
z=(c,p,m)
\in
\mathcal H_c
\times
\mathcal H_p
\times
\mathcal H_m.
\]

For a smooth test function, define

\[
\mathcal L_cf
=
v_c(c,t)^\top\nabla_cf,
\]

and

\[
\mathcal L_mf
=
b_m(m,t)^\top\nabla_mf
+
\frac12
\operatorname{tr}
[
a_m(m,t)\nabla_m^2f
].
\]

The coefficients of \(\mathcal L_c\) do not depend on \(m\), and the
coefficients of \(\mathcal L_m\) do not depend on \(c\) or \(p\).

## 2. Lemma 12.1 — mixed partials commute

For \(f\in C^3\),

\[
\nabla_c\nabla_mf
=
\nabla_m\nabla_cf
\]

and

\[
\nabla_c\nabla_m^2f
=
\nabla_m^2\nabla_cf.
\]

### Proof

This is equality of mixed partial derivatives under the stated smoothness. ∎

## 3. Theorem 12.1 — decoupled generators commute

For every sufficiently smooth \(f\),

\[
\boxed{
[\mathcal L_c,\mathcal L_m]f=0.
}
\]

### Detailed proof

Apply \(\mathcal L_c\) to \(\mathcal L_mf\). Because the missing-block
coefficients do not depend on \(c\), the \(c\)-derivative acts only on
derivatives of \(f\). Apply \(\mathcal L_m\) to \(\mathcal L_cf\). Because
the shared velocity does not depend on \(m\), the missing derivatives also act
only on derivatives of \(f\). Lemma 12.1 makes the corresponding first- and
second-order mixed derivatives equal, so the difference is zero. ∎

## 4. Corollary 12.1 — semigroup factorization

When the generators define strongly continuous semigroups and strongly
commute,

\[
e^{t(\mathcal L_c+\mathcal L_m)}
=
e^{t\mathcal L_c}e^{t\mathcal L_m}
=
e^{t\mathcal L_m}e^{t\mathcal L_c}.
\]

This equality belongs to the decoupled baseline.

## 5. Final triangular method

The candidate final model instead uses

\[
C^*=T_d(C),
\]

\[
P'=P,
\]

\[
M'
\sim
q_\theta(
M\mid C^*,P,\mathcal O_d).
\]

Its missing generator depends on \(C^*\) and possibly on \(P\). In general,

\[
[\mathcal L_c,\mathcal L_m]\neq0.
\]

Flow must therefore precede the conditional missing posterior, or the joint
process must be solved with an explicitly analyzed splitting scheme.

## 6. Lemma 12.2 — first splitting-error term

Formally, for a small step \(h\),

\[
e^{h(\mathcal L_c+\mathcal L_m)}
-
e^{h\mathcal L_c}e^{h\mathcal L_m}
=
-\frac{h^2}{2}
[\mathcal L_c,\mathcal L_m]
+
O(h^3).
\]

### Proof

Expand both exponentials to second order and subtract. The unequal cross terms
combine into the commutator. ∎

## 7. Failure boundaries

1. Pointwise commutation is not sufficient for arbitrary time-dependent
   generators without compatible chronological ordering.
2. A missing score conditioned on canonical shared state violates the theorem.
3. Learned state-dependent projectors create extra derivative terms.
4. Numerical solvers can produce order error even in the exact decoupled case.
5. Global-null coordinates are absent from both generators.

## 8. Experimental implication

Use the decoupled model as a null baseline:

```text
missing posterior ignores canonical shared state
```

and compare it with the triangular model:

```text
shared flow first
then missing posterior conditioned on canonical shared and private state
```

Run order reversal only for the decoupled baseline. For the triangular method,
report the benefit of conditioning and, if split integration is used, the
measured order or step-size sensitivity.
