# Theorem 12 — Commuting shared-flow and unobserved-diffusion generators

## Status

**Proved when the two generators act on disjoint coordinates and their coefficients do not cross-condition.**

## Purpose

The unified representation has a shared deterministic transport and an unobserved stochastic transport. This theorem identifies the conditions under which their execution order is mathematically irrelevant.

## 1. Product coordinates

Let

\[
z=(c,p,u)
\in
\mathcal H_c\times\mathcal H_p\times\mathcal H_u.
\]

For a smooth test function \(f(c,p,u)\), define a shared-flow generator

\[
\mathcal L_cf
=
 v_c(c,t)^\top\nabla_cf,
\tag{12.1}
\]

and an unobserved-diffusion generator

\[
\mathcal L_uf
=
 b_u(u,t)^\top\nabla_uf
+
\frac12
\operatorname{tr}
\left[
 a_u(u,t)\nabla_u^2f
\right].
\tag{12.2}
\]

The coefficients of \(\mathcal L_c\) depend only on \(c,t\), and the coefficients of \(\mathcal L_u\) depend only on \(u,t\). Neither generator differentiates the private coordinate.

For the commutator proof, fix time or use time-ordered evolution on a small interval with frozen coefficients. The autonomous notation is used below.

## 2. Lemma 12.1 — mixed partial derivatives commute

For \(f\in C^3\),

\[
\nabla_c\nabla_uf
=
\nabla_u\nabla_cf,
\]

and

\[
\nabla_c\nabla_u^2f
=
\nabla_u^2\nabla_cf.
\]

This follows from equality of mixed partial derivatives under the stated smoothness. ∎

## 3. Theorem 12.1 — generator commutation

### Statement

Under Equations (12.1)–(12.2),

\[
\boxed{
[\mathcal L_c,\mathcal L_u]f
=
\mathcal L_c\mathcal L_uf
-
\mathcal L_u\mathcal L_cf
=0
}
\]

for every sufficiently smooth test function.

### Detailed proof

Apply \(\mathcal L_c\) to \(\mathcal L_uf\):

\[
\mathcal L_c\mathcal L_uf
=
 v_c^\top\nabla_c
\left(
 b_u^\top\nabla_uf
+
\frac12\operatorname{tr}(a_u\nabla_u^2f)
\right).
\]

Because \(b_u\) and \(a_u\) do not depend on \(c\), the \(c\)-derivative acts only on derivatives of \(f\):

\[
\mathcal L_c\mathcal L_uf
=
 v_c^\top b_u^\top
\nabla_c\nabla_uf
+
\frac12 v_c^\top
\nabla_c
\operatorname{tr}(a_u\nabla_u^2f).
\tag{12.3}
\]

Now apply \(\mathcal L_u\) to \(\mathcal L_cf\):

\[
\mathcal L_u\mathcal L_cf
=
 b_u^\top\nabla_u(v_c^\top\nabla_cf)
+
\frac12
\operatorname{tr}
\left[
 a_u\nabla_u^2(v_c^\top\nabla_cf)
\right].
\]

Because \(v_c\) does not depend on \(u\),

\[
\mathcal L_u\mathcal L_cf
=
 b_u^\top v_c^\top
\nabla_u\nabla_cf
+
\frac12
\operatorname{tr}
\left[
 a_uv_c^\top\nabla_u^2\nabla_cf
\right].
\tag{12.4}
\]

By Lemma 12.1, the first terms of (12.3) and (12.4) are equal. Linearity of trace and equality of the higher mixed derivatives make the second terms equal. Therefore their difference is zero. ∎

## 4. Corollary 12.1 — semigroup factorization

Assume the generators define strongly continuous Markov semigroups and strongly commute. Then

\[
\boxed{
 e^{t(\mathcal L_c+\mathcal L_u)}
 =
 e^{t\mathcal L_c}
 e^{t\mathcal L_u}
 =
 e^{t\mathcal L_u}
 e^{t\mathcal L_c}
}
\]

on their common domain.

Thus, under the theorem's assumptions, applying shared canonical flow before unobserved diffusion gives the same transition operator as reversing the order.

## 5. Elementary linear-Gaussian verification

Let

\[
dC_t=MC_tdt,
\]

\[
dU_t=NU_tdt+LdW_t.
\]

The joint solution is

\[
C_t=e^{Mt}C_0,
\]

\[
U_t=e^{Nt}U_0+
\int_0^te^{N(t-s)}LdW_s.
\]

The shared solution contains no \(U\), and the unobserved solution contains no \(C\). Applying either transition first changes only its own coordinate, so the transition kernels commute directly.

## 6. Non-commuting extension

If the shared velocity depends on \(u\), or the unobserved score depends on \(c\), then generally

\[
[\mathcal L_c,\mathcal L_u]\neq0.
\]

For a small numerical step \(h\), Lie–Trotter splitting gives

\[
e^{h(\mathcal L_c+\mathcal L_u)}
-
e^{h\mathcal L_c}e^{h\mathcal L_u}
=
-\frac{h^2}{2}
[\mathcal L_c,\mathcal L_u]
+O(h^3)
\]

formally on sufficiently smooth functions. The commutator magnitude therefore measures first-order coupling error in a split implementation.

## 7. Scientific interpretation

There are two method variants:

### Independent blocks

```text
shared flow depends only on shared coordinates
unobserved diffusion depends only on unobserved coordinates and observation context
```

This variant receives the exact commuting theorem.

### Coupled blocks

```text
shared flow conditions on uncertainty in unobserved modes
or
unobserved diffusion conditions on canonical shared coordinates
```

This may be more expressive but loses order independence. It requires a joint solver or an explicit splitting-error study.

## 8. Failure boundaries

1. Time-dependent non-autonomous generators require chronological ordering; pointwise commutation is sufficient but must hold across times.
2. Learned projectors that move with the state create cross-derivative terms.
3. A shared encoder that consumes concatenated private features violates the disjoint-coordinate assumption even if its output is later projected.
4. Numerical integrators can introduce order-dependent discretization error even when the exact semigroups commute.

## 9. Experimental implication

For an independent-block implementation, run both orders:

```text
flow then diffusion
diffusion then flow
```

with identical initial states and random numbers. Their endpoint distributions should agree within numerical error, and their observed-private coordinates must match exactly. If a coupled architecture is used, report order sensitivity or solve the joint process directly.
