# Theorem 14 — Structural observability and instance reliability

## Status

**Proved for a fixed structural acquisition operator and a linear-Gaussian
instance observation model.**

## Purpose

The acquisition design and one realized sample answer different questions.

- Structural observability asks whether a sensor configuration can observe a
  modal direction in principle.
- Instance reliability asks how much information one sample supplies about that
  structurally available direction.

Conflating them makes the modal role change with every missing-value pattern and
breaks the fixed-slot representation contract.

## 1. Setup

For acquisition domain \(d\), let

\[
Y_{d,i}=R_{d,i}A_d\Theta_i+\varepsilon_{d,i},
\qquad
\varepsilon_{d,i}\sim\mathcal N(0,\Sigma_{d,i}),
\]

where \(A_d\) is fixed by the acquisition design and \(R_{d,i}\) describes the
realized timestamps, valid mask or coverage of sample \(i\).

The structural Gramian is

\[
G_d=A_d^\top\Sigma_d^{-1}A_d.
\]

The instance information matrix is

\[
G_{d,i}^{\mathrm{inst}}
=
A_d^\top
R_{d,i}^\top
\Sigma_{d,i}^{-1}
R_{d,i}
A_d.
\]

## 2. Lemma 14.1 — instance loss cannot reveal a structural null direction

### Statement

If \(v\in\ker A_d\), then

\[
G_{d,i}^{\mathrm{inst}}v=0
\]

for every sample operator \(R_{d,i}\).

### Proof

From \(A_dv=0\),

\[
R_{d,i}A_dv=0.
\]

Therefore

\[
G_{d,i}^{\mathrm{inst}}v
=
A_d^\top R_{d,i}^\top
\Sigma_{d,i}^{-1}
R_{d,i}A_dv
=0.
\]

Thus sample-specific coverage can remove information that the design could have
provided, but it cannot create information in a structural null direction. ∎

## 3. Lemma 14.2 — Gaussian posterior precision separates role and reliability

Assume a Gaussian prior

\[
\Theta\sim\mathcal N(m_0,\Lambda_0^{-1}),
\qquad
\Lambda_0\succ0.
\]

Then the posterior precision for sample \(i\) is

\[
\Lambda_{d,i}^{\mathrm{post}}
=
\Lambda_0
+
G_{d,i}^{\mathrm{inst}}.
\]

### Proof

The negative log posterior, up to constants, is

\[
\frac12(\Theta-m_0)^\top\Lambda_0(\Theta-m_0)
+
\frac12
(Y_{d,i}-R_{d,i}A_d\Theta)^\top
\Sigma_{d,i}^{-1}
(Y_{d,i}-R_{d,i}A_d\Theta).
\]

Collecting the quadratic terms in \(\Theta\) gives the displayed precision. ∎

## 4. Theorem 14 — greater instance information narrows posterior uncertainty

Let two realizations satisfy

\[
G_{d,i}^{\mathrm{inst}}
\preceq
G_{d,j}^{\mathrm{inst}}.
\]

Then their posterior covariances satisfy

\[
\boxed{
(\Lambda_0+G_{d,j}^{\mathrm{inst}})^{-1}
\preceq
(\Lambda_0+G_{d,i}^{\mathrm{inst}})^{-1}.
}
\]

### Detailed proof

Add \(\Lambda_0\succ0\) to both sides:

\[
\Lambda_0+G_{d,i}^{\mathrm{inst}}
\preceq
\Lambda_0+G_{d,j}^{\mathrm{inst}}.
\]

For positive-definite matrices, inversion reverses Loewner order. Hence

\[
(\Lambda_0+G_{d,j}^{\mathrm{inst}})^{-1}
\preceq
(\Lambda_0+G_{d,i}^{\mathrm{inst}})^{-1}.
\]

Thus reliability changes posterior precision while the structural role remains
defined by \(A_d\). ∎

## 5. Consequence for fixed modal slots

Let \(u_k\) be a fixed unit modal vector. Define structural information

\[
g_{d,k}=u_k^\top G_du_k
\]

and instance information

\[
g_{d,i,k}^{\mathrm{inst}}
=u_k^\top G_{d,i}^{\mathrm{inst}}u_k.
\]

The slot role is assigned from \(g_{d,k}\), while sample confidence may be a
monotone function of \(g_{d,i,k}^{\mathrm{inst}}\). A low-confidence sample does
not silently change a common slot into a private or missing slot.

## 6. Failure boundaries

1. If \(A_d\) itself changes between samples, the structural domain definition
   must be refined.
2. Non-Gaussian posterior precision needs a different uncertainty summary.
3. A learned \(R_{d,i}\) can be misspecified.
4. Reliability can approach zero even for a structurally observable mode.
5. The theorem does not identify \(A_d\) from data.

## 7. Experimental implication

For each modal slot report separately:

- structural information \(g_{d,k}\);
- instance information or reliability;
- posterior variance;
- role assignment.

Vary missingness and SNR while keeping \(A_d\) fixed. The role must remain fixed,
while posterior uncertainty should increase as instance information decreases.
