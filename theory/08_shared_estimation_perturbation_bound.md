# Theorem 8 — Noise-weighted perturbation bound for shared-mode estimation

## Status

**Proved for a linear shared observation model and the generalized
least-squares estimator implied by Axiom A2.**

## Purpose

The previous least-squares form ignored the noise metric used to define the
observable Gramian. This document aligns the estimator and the theory with the
same covariance model. The result connects shared-representation error to
whitened noise, acquisition-operator error and structural observability.

## 1. Setup

Let \(U_c\in\mathbb R^{m\times r}\) have orthonormal columns spanning
\(\mathcal H_c\), and write

\[
\Theta_c=U_c\alpha.
\]

For domain \(d\), define

\[
B_d=A_dU_c,
\qquad
C_d=\Sigma_d^{-1/2}B_d.
\]

The true observation is

\[
y_d=(B_d+\Delta B_d)\alpha+\varepsilon_d.
\tag{8.1}
\]

Let

\[
\Delta C_d
=
\Sigma_d^{-1/2}\Delta B_d,
\qquad
\eta_d
=
\Sigma_d^{-1/2}\varepsilon_d.
\]

Assume \(C_d\) has full column rank and

\[
\sigma_{\min}(C_d)
\geq
\gamma_d>0.
\tag{8.2}
\]

The nominal generalized least-squares estimator is

\[
\widehat\alpha_d
=
(B_d^\top\Sigma_d^{-1}B_d)^{-1}
B_d^\top\Sigma_d^{-1}y_d
=
C_d^\dagger\Sigma_d^{-1/2}y_d.
\tag{8.3}
\]

## 2. Lemma 8.1 — whitened pseudoinverse norm

For full-column-rank \(C_d\),

\[
\|C_d^\dagger\|_2
=
\frac{1}{\sigma_{\min}(C_d)}
\leq
\frac{1}{\gamma_d}.
\]

### Proof

Apply the singular value decomposition
\(C_d=U\Sigma V^\top\). Then
\(C_d^\dagger=V\Sigma^{-1}U^\top\), and orthogonal factors have norm one. ∎

## 3. Theorem 8.1 — single-domain GLS error

The shared-state estimate
\(\widehat\Theta_c^{(d)}=U_c\widehat\alpha_d\) satisfies

\[
\boxed{
\|
\widehat\Theta_c^{(d)}-\Theta_c
\|_2
\leq
\frac{
\|\Delta C_d\|_2\|\alpha\|_2
+
\|\eta_d\|_2
}{
\gamma_d
}
}.
\tag{8.4}
\]

### Detailed proof

Premultiply Equation (8.1) by \(\Sigma_d^{-1/2}\):

\[
\Sigma_d^{-1/2}y_d
=
(C_d+\Delta C_d)\alpha+\eta_d.
\]

Using Equation (8.3),

\[
\begin{aligned}
\widehat\alpha_d
&=
C_d^\dagger
\left[
(C_d+\Delta C_d)\alpha+\eta_d
\right]\\
&=
\alpha
+
C_d^\dagger\Delta C_d\alpha
+
C_d^\dagger\eta_d,
\end{aligned}
\]

because \(C_d^\dagger C_d=I_r\). Hence

\[
\widehat\alpha_d-\alpha
=
C_d^\dagger\Delta C_d\alpha
+
C_d^\dagger\eta_d.
\]

Taking norms and applying Lemma 8.1 yields

\[
\|
\widehat\alpha_d-\alpha
\|_2
\leq
\frac{
\|\Delta C_d\|_2\|\alpha\|_2
+
\|\eta_d\|_2
}{
\gamma_d
}.
\]

Finally, \(U_c\) is an isometry on \(\mathbb R^r\), so the same bound holds
for the modal state. ∎

## 4. Corollary 8.1 — paired cross-acquisition discrepancy

For two domains observing the same latent event,

\[
\begin{aligned}
\|
\widehat\Theta_c^{(d)}
-
\widehat\Theta_c^{(e)}
\|_2
\leq{}&
\frac{
\|\Delta C_d\|\|\alpha\|
+
\|\eta_d\|
}{\gamma_d}
\\
&+
\frac{
\|\Delta C_e\|\|\alpha\|
+
\|\eta_e\|
}{\gamma_e}.
\end{aligned}
\]

### Proof

Insert the common true state and apply the triangle inequality, then apply
Theorem 8.1 to both terms. ∎

## 5. Corollary 8.2 — exact covariance under the nominal noise model

Assume \(\Delta B_d=0\),
\(\mathbb E\varepsilon_d=0\) and
\(\operatorname{Cov}(\varepsilon_d)=\Sigma_d\). Then

\[
\operatorname{Cov}
(\widehat\alpha_d-\alpha)
=
(B_d^\top\Sigma_d^{-1}B_d)^{-1}.
\tag{8.5}
\]

### Proof

From Equation (8.3),

\[
\widehat\alpha_d-\alpha
=
M_d\varepsilon_d,
\]

where

\[
M_d
=
(B_d^\top\Sigma_d^{-1}B_d)^{-1}
B_d^\top\Sigma_d^{-1}.
\]

Therefore

\[
\begin{aligned}
\operatorname{Cov}(\widehat\alpha_d-\alpha)
&=
M_d\Sigma_dM_d^\top\\
&=
(B_d^\top\Sigma_d^{-1}B_d)^{-1}.
\end{aligned}
\]

∎

## 6. Lemma 8.2 — structural support and instance reliability have different roles

The structural constant

\[
\gamma_d
=
\sigma_{\min}
(\Sigma_d^{-1/2}B_d)
\]

depends on the acquisition design. A sample-level mask or low SNR changes the
realized \(\eta_{d,i}\) or an instance-specific information matrix, but does
not change the definition of \(\mathcal H_c\) in this theorem.

### Consequence

The method should store both:

- structural observability for slot classification;
- instance reliability for posterior precision and confidence.

Conflating them produces sample-dependent subspace dimensions and invalidates
the fixed-projector theorem.

## 7. Support-estimation error

If the estimated common projector is \(\widehat P_c\), then

\[
\|
\widehat P_c\widehat\Theta
-
P_c\Theta
\|
\leq
\|
\widehat P_c(\widehat\Theta-\Theta)
\|
+
\|
(\widehat P_c-P_c)\Theta
\|.
\]

The second term is bounded by

\[
\|
\widehat P_c-P_c
\|_2
\|\Theta\|_2.
\]

A Davis--Kahan bound may control the projector error when a non-zero spectral
gap separates the selected support from the threshold. Near-threshold slots
should additionally report soft observability and threshold sensitivity.

## 8. Failure boundaries

1. If \(C_d\) is rank deficient, the shared coordinate is not identifiable.
2. If \(\gamma_d\) is small, the bound is large and may be uninformative.
3. The paired corollary requires the same latent event; class-sorted independent
   samples do not satisfy it.
4. A wrong covariance model yields a wrong whitening metric.
5. Nonlinear acquisition requires a linearization-remainder term.
6. Canonical Flow cannot recover information lost before shared-state
   estimation.

## 9. Experimental implication

For each shared modal slot report:

- the smallest singular value of the whitened operator;
- whitened noise magnitude;
- paired shared-state error;
- operator-perturbation sensitivity;
- support-threshold margin;
- instance reliability.

Increasing whitened noise or decreasing \(\gamma_d\) should degrade the
paired shared estimate in the direction predicted by Equation (8.4).
