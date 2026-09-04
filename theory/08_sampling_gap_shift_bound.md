# Theory 8 — Sampling-gap distribution shift bound

## Status

Proved for a stable scalar Laplace mode and gap distributions with finite first moment.

## Setup

Let

\[
s=-\rho+i\omega,
\qquad
\rho\geq0.
\]

For a non-negative random sampling gap \(\Delta\sim P\), define the mean event multiplier

\[
\lambda_P(s)=\mathbb E_P[e^{s\Delta}].
\]

## Lemma 8.1 — Lipschitz exponential on non-negative gaps

For \(a,b\geq0\),

\[
|e^{sa}-e^{sb}|
\leq |s||a-b|.
\]

### Proof

The derivative of \(e^{st}\) has magnitude

\[
|s|e^{-\rho t}\leq|s|
\]

on \([0,\infty)\). Apply the integral mean-value bound. ∎

## Theorem 8 — gap-distribution perturbation

For \(P,Q\in\mathcal P_1([0,\infty))\),

\[
\boxed{
|\lambda_P(s)-\lambda_Q(s)|
\leq
|s|W_1(P,Q).
}
\]

### Proof

For any coupling \(\pi\) of \((\Delta_P,\Delta_Q)\),

\[
\begin{aligned}
|\lambda_P-\lambda_Q|
&\leq
\mathbb E_\pi|e^{s\Delta_P}-e^{s\Delta_Q}|\\
&\leq
|s|\mathbb E_\pi|\Delta_P-\Delta_Q|.
\end{aligned}
\]

Take the infimum over all couplings. ∎

## Interpretation

High-frequency modes have larger \(|s|\) and can be more sensitive to changes in the sampling-gap distribution. HSE temporal and reliability tokens should therefore preserve more than an average gap when irregularity is informative.

## Role in the paper

This is a supporting extension of the gap-aware rationale in LLapDiff, not a claim that renewal averaging or gap-conditioned Laplace dynamics are new.

## Failure conditions

- State-dependent or dependent gap processes require conditional analysis.
- The bound concerns a mean multiplier, not the full random product process.
- A logarithmic effective pole requires a consistent complex-log branch away from zero.
