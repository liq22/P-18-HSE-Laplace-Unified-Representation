# Theorem 24 — Window-local Laplace adequacy and residual propagation

## Status

**Deterministic approximation bound for a bounded acquisition operator and a
Lipschitz representation map.**

## Purpose

Stable Laplace coordinates are appropriate only when a finite local modal
dictionary approximates the target window well. Stability alone does not prove
physical adequacy.

## 1. Setup

On a window \([0,T]\), write

\[
s=\Phi\Theta+r,
\]

where the modal residual satisfies

\[
\|r\|_{\mathcal X}
\leq
\varepsilon_{\mathrm{modal}}.
\]

Let the acquisition operator

\[
\mathcal A_d:\mathcal X\to\mathcal Y_d
\]

be bounded with operator norm

\[
\|\mathcal A_d\|_{\mathrm{op}}\leq M_d.
\]

## 2. Theorem 24.1 — acquisition-space residual bound

The difference between the true noiseless observation and the modal
approximation is bounded by

\[
\boxed{
\|
\mathcal A_ds
-
\mathcal A_d\Phi\Theta
\|_{\mathcal Y_d}
\leq
M_d\varepsilon_{\mathrm{modal}}.
}
\]

### Proof

By linearity,

\[
\mathcal A_ds-\mathcal A_d\Phi\Theta
=
\mathcal A_dr.
\]

Boundedness gives

\[
\|\mathcal A_dr\|
\leq
\|\mathcal A_d\|_{\mathrm{op}}\|r\|
\leq
M_d\varepsilon_{\mathrm{modal}}.
\]
∎

## 3. Corollary 24.1 — representation error propagation

Let an analysis map \(E_d:\mathcal Y_d\to\mathcal Z\) be
\(L_E\)-Lipschitz. Then

\[
\boxed{
\|
E_d(\mathcal A_ds)
-
E_d(\mathcal A_d\Phi\Theta)
\|
\leq
L_EM_d\varepsilon_{\mathrm{modal}}.
}
\]

### Proof

Apply Lipschitz continuity to Theorem 24.1. ∎

## 4. Relative adequacy ratio

Define

\[
\eta_{\mathrm{modal}}
=
\frac{
\|s-\Phi\Theta\|_{\mathcal X}
}{
\|s\|_{\mathcal X}+\epsilon
}.
\]

This is a diagnostic, not a universal threshold. The analysis window and modal
rank must be frozen before target evaluation.

## 5. Forced and switching controls

A bounded periodic forced component can be added as a matched baseline. A
single fixed pole generally cannot represent a trajectory whose decay rate
switches inside the window. These cases test whether the event-local transient
scope is adequate.

## 6. Failure boundaries

1. Nonlinear acquisition operators need a local Lipschitz rather than linear
   operator bound.
2. Small waveform residual does not guarantee correct modal interpretation.
3. A large dictionary can fit noise and lose identifiability.
4. Window selection can leak target information.
5. The direct time-domain latent may dominate at equal dimension.

## 7. Experimental implication

Compare transient-only, transient-plus-forced and switching generators. Report:

- modal residual;
- acquisition-space residual;
- support-role error;
- downstream paired error.

Stop using Laplace coordinates as the main representation if a matched direct
time-domain latent simultaneously improves reconstruction and the relevant
cross-acquisition metrics.
