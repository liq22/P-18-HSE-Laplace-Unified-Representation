# Theory 1 — Fixed-dimensional acquisition sufficiency

## Status

Proved for the linear-Gaussian acquisition model in Theory 0.

## Purpose

The observation length \(n_d\) may vary across acquisitions. This result shows that the latent-dependent part of the likelihood can still be represented by statistics whose dimension depends only on the canonical modal dimension \(m\).

## Definition

Define

\[
b_d=A_d^TR_d^{-1}X_d,
\qquad
J_d=A_d^TR_d^{-1}A_d.
\]

Here \(b_d\in\mathbb R^m\) and \(J_d\in\mathbb R^{m\times m}\), regardless of \(n_d\).

## Lemma 1.1 — likelihood factorization

For fixed \(A_d,R_d\), the Gaussian likelihood can be written as

\[
p(x_d\mid\theta)
=h_d(x_d)
\exp\left(
\theta^Tb_d-\frac12\theta^TJ_d\theta
\right),
\]

where \(h_d\) is independent of \(\theta\).

### Proof

The likelihood is

\[
p(x_d\mid\theta)
=(2\pi)^{-n_d/2}|R_d|^{-1/2}
\exp\left[-\frac12(x_d-A_d\theta)^TR_d^{-1}(x_d-A_d\theta)\right].
\]

Expand the quadratic form:

\[
\begin{aligned}
(x_d-A_d\theta)^TR_d^{-1}(x_d-A_d\theta)
={}&x_d^TR_d^{-1}x_d
-2\theta^TA_d^TR_d^{-1}x_d\\
&+\theta^TA_d^TR_d^{-1}A_d\theta.
\end{aligned}
\]

Substituting \(b_d\) and \(J_d\), the term containing only \(x_d\) is absorbed into \(h_d(x_d)\), yielding the factorization. ∎

## Theorem 1 — sufficient statistic

For known \(A_d,R_d\),

\[
\boxed{T_d(X_d)=(b_d,J_d)}
\]

is sufficient for \(\Theta\).

### Proof

By Lemma 1.1, the likelihood factors into a product of a function independent of \(\theta\) and a function depending on the observation only through \((b_d,J_d)\). The Fisher–Neyman factorization theorem gives sufficiency. ∎

## Lemma 1.2 — equal statistics give a latent-independent likelihood ratio

If two observations \(x\) and \(x'\) have the same \((b,J)\), then

\[
\frac{p(x\mid\theta)}{p(x'\mid\theta)}
\]

is independent of \(\theta\).

### Proof

Apply Lemma 1.1 to both observations. Their exponential factors are identical, so only \(h(x)/h(x')\) remains. ∎

## HSE interpretation

For a fixed modal dictionary, the diagonal or blockwise components of \((b_d,J_d)\) define one acquisition-evidence token per modal slot. HSE may approximate these statistics while appending physical time, frequency support, and reliability metadata.

The theorem does not prove that a neural HSE learns a minimal sufficient statistic. It provides a target semantics and an oracle baseline.

## Executable prediction

Variable-length acquisition operators with the same modal dimension must produce:

```text
score shape       [m]
information shape [m, m]
HSE token shape   [K, D]
```

independent of the number of observed samples.

## Failure conditions

- Unknown or misspecified \(A_d,R_d\) invalidate exact sufficiency.
- Nonlinear and non-Gaussian acquisition generally requires different sufficient statistics or may have no finite-dimensional sufficient statistic.
- Compressing a dense \(J_d\) to diagonal slot information loses cross-modal coupling unless the modal basis approximately diagonalizes the acquisition information.
