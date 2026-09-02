# Theorem 23 — When nonlinear Flow canonicalization is unnecessary

## Status

**Exact result for paired invertible affine acquisition distortion.**

## Purpose

A learned Flow is unnecessary when a simple affine canonicalizer can exactly
recover the paired shared coordinate. Flow should be promoted only after a
matched affine, CORAL or ordinary-OT baseline leaves measurable headroom.

## 1. Setup

Let \(C^\dagger\in\mathbb R^r\) be the paired physical anchor. Suppose domain
\(d\) produces

\[
C_d=M_dC^\dagger+b_d,
\]

where \(M_d\) is invertible.

Define

\[
T_d^{\mathrm{aff}}(c)
=
M_d^{-1}(c-b_d).
\]

## 2. Theorem 23.1 — affine map gives exact eventwise canonicality

\[
\boxed{
T_d^{\mathrm{aff}}(C_d)=C^\dagger
\quad\text{almost surely}.
}
\]

Consequently, for any non-negative paired canonicalization loss \(L\) satisfying
\(L(z,z)=0\),

\[
\inf_T
\mathbb E L(T(C_d),C^\dagger)
=0,
\]

and no nonlinear Flow can improve below this population optimum.

### Proof

Substitute the observation model:

\[
T_d^{\mathrm{aff}}(C_d)
=
M_d^{-1}(M_dC^\dagger+b_d-b_d)
=
C^\dagger.
\]

The paired loss is therefore zero. Non-negativity makes zero the global lower
bound. ∎

## 3. Corollary 23.1 — task semantics are preserved

Any target depending on \(C^\dagger\) can be evaluated without information loss
after exact affine canonicalization because the anchor is recovered exactly.

## 4. Why CORAL is a weaker baseline

Whitening or CORAL matches first and second moments. It equals the exact affine
map only under additional conditions on the domain distributions and the
chosen square-root convention. Therefore the baseline ladder should include:

```text
identity
paired affine regression
whitening/CORAL
ordinary or minibatch OT
conditional Flow Matching
```

## 5. Nonlinear headroom example

Let scalar shared state satisfy

\[
C_d=(C^\dagger)^3
\]

on a bounded interval. The exact inverse is nonlinear:

\[
T_d(c)=\sqrt[3]{c}.
\]

An affine map cannot produce zero paired error on a non-degenerate distribution.
A sufficiently expressive monotone Flow can represent the inverse.

This demonstrates possible headroom; it does not prove a learned Flow will find
the correct map.

## 6. Failure boundaries

1. \(M_d\) may be ill-conditioned.
2. Paired affine estimation has finite-sample error.
3. An unpaired affine map can still permute semantics.
4. Flow can overfit acquisition identity.
5. Nonlinear distortion may be handled by a simpler spline or kernel map.

## 7. Experimental implication

Include both affine and nonlinear acquisition cells. Flow is retained only if
it improves paired shared error and preserves task semantics beyond all
predeclared simpler canonicalizers.
