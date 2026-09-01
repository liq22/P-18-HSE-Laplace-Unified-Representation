# Theorem 8 — Perturbation bound for shared-mode estimation

## Status

**Proved for a linear shared observation model and a nominal least-squares estimator.**

## Purpose

A shared mode may be theoretically observable in every source domain but still be estimated poorly because of noise, sensor-model error, or weak conditioning. This theorem connects representation discrepancy to those quantities.

## 1. Setup

Let \(r=\dim\mathcal H_c\), and let \(U_c\in\mathbb R^{m\times r}\) have orthonormal columns spanning the common observable subspace. Write

\[
\Theta_c=U_c\alpha,
\qquad
\alpha\in\mathbb R^r.
\]

For domain \(d\), define the nominal shared observation matrix

\[
B_d=A_dU_c.
\]

The true observation may contain an operator perturbation \(\Delta B_d\):

\[
y_d=(B_d+\Delta B_d)\alpha+\varepsilon_d.
\tag{8.1}
\]

Assume \(B_d\) has full column rank and

\[
\sigma_{\min}(B_d)\geq\gamma_d>0.
\tag{8.2}
\]

Use the nominal least-squares estimator

\[
\widehat\alpha_d=B_d^\dagger y_d,
\]

where

\[
B_d^\dagger=(B_d^\top B_d)^{-1}B_d^\top.
\]

## 2. Lemma 8.1 — pseudoinverse norm

### Statement

For a full-column-rank matrix \(B_d\),

\[
\|B_d^\dagger\|_2
=
\frac{1}{\sigma_{\min}(B_d)}
\leq
\frac1{\gamma_d}.
\]

### Proof

Let the singular value decomposition be

\[
B_d=U\Sigma V^\top
\]

with positive singular values \(\sigma_1\geq\cdots\geq\sigma_r>0\). Then

\[
B_d^\dagger=V\Sigma^{-1}U^\top.
\]

Orthogonal factors have norm one, so

\[
\|B_d^\dagger\|_2
=\|\Sigma^{-1}\|_2
=1/\sigma_r
=1/\sigma_{\min}(B_d).
\]

Equation (8.2) gives the final inequality. ∎

## 3. Theorem 8.1 — single-domain estimation error

### Statement

\[
\boxed{
\|\widehat\Theta_c^{(d)}-\Theta_c\|_2
\leq
\frac{
\|\Delta B_d\|_2\|\alpha\|_2
+
\|\varepsilon_d\|_2
}{\gamma_d}
}
\]

where \(\widehat\Theta_c^{(d)}=U_c\widehat\alpha_d\).

### Detailed proof

Substitute Equation (8.1):

\[
\begin{aligned}
\widehat\alpha_d
&=B_d^\dagger
\left[(B_d+\Delta B_d)\alpha+\varepsilon_d\right]\\
&=B_d^\dagger B_d\alpha
+B_d^\dagger\Delta B_d\alpha
+B_d^\dagger\varepsilon_d.
\end{aligned}
\]

Because \(B_d\) has full column rank,

\[
B_d^\dagger B_d=I_r.
\]

Hence

\[
\widehat\alpha_d-\alpha
=
B_d^\dagger\Delta B_d\alpha
+B_d^\dagger\varepsilon_d.
\]

Taking norms,

\[
\begin{aligned}
\|\widehat\alpha_d-\alpha\|_2
&\leq
\|B_d^\dagger\|_2
\|\Delta B_d\|_2
\|\alpha\|_2
+
\|B_d^\dagger\|_2
\|\varepsilon_d\|_2\\
&\leq
\frac{
\|\Delta B_d\|_2\|\alpha\|_2
+
\|\varepsilon_d\|_2
}{\gamma_d},
\end{aligned}
\]

using Lemma 8.1. Since \(U_c\) has orthonormal columns,

\[
\|U_c(\widehat\alpha_d-\alpha)\|_2
=
\|\widehat\alpha_d-\alpha\|_2.
\]

This proves the result. ∎

## 4. Corollary 8.1 — paired cross-domain discrepancy

For two domains \(d\) and \(e\) observing the same latent event,

\[
\begin{aligned}
\|
\widehat\Theta_c^{(d)}
-
\widehat\Theta_c^{(e)}
\|_2
\leq{}&
\frac{
\|\Delta B_d\|\|\alpha\|
+
\|\varepsilon_d\|
}{\gamma_d}
\\
&+
\frac{
\|\Delta B_e\|\|\alpha\|
+
\|\varepsilon_e\|
}{\gamma_e}.
\end{aligned}
\]

### Proof

Use the triangle inequality around the common true state:

\[
\|
\widehat\Theta_c^{(d)}-
\widehat\Theta_c^{(e)}
\|
\leq
\|
\widehat\Theta_c^{(d)}-
\Theta_c
\|
+
\|
\Theta_c-
\widehat\Theta_c^{(e)}
\|,
\]

then apply Theorem 8.1 to both terms. ∎

## 5. Corollary 8.2 — noise amplification by weak observability

Even with a correct operator model \(\Delta B_d=0\),

\[
\|\widehat\Theta_c^{(d)}-\Theta_c\|
\leq
\|\varepsilon_d\|/\gamma_d.
\]

A mode near the observability threshold has small \(\gamma_d\) and can produce a large representation error. Binary support membership alone is therefore insufficient for uncertainty calibration.

## 6. Expected squared error under zero-mean noise

Assume \(\Delta B_d=0\), \(\mathbb E\varepsilon_d=0\), and \(\operatorname{Cov}(\varepsilon_d)=\Sigma_{\varepsilon,d}\). Then

\[
\widehat\alpha_d-\alpha=B_d^\dagger\varepsilon_d,
\]

so

\[
\operatorname{Cov}(\widehat\alpha_d-\alpha)
=
B_d^\dagger
\Sigma_{\varepsilon,d}
(B_d^\dagger)^\top.
\]

Consequently,

\[
\mathbb E\|\widehat\alpha_d-\alpha\|_2^2
=
\operatorname{tr}
\left[
B_d^\dagger
\Sigma_{\varepsilon,d}
(B_d^\dagger)^\top
\right].
\]

This exact covariance is preferable to a worst-case norm bound when the noise model is credible.

## 7. Boundary: support-estimation error

The theorem assumes the common basis \(U_c\) is correct. If an estimated projector \(\widehat P_c\) differs from \(P_c\), the total error contains an additional term:

\[
\|
\widehat P_c\widehat\Theta-
P_c\Theta
\|
\leq
\|
\widehat P_c(\widehat\Theta-
\Theta)
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
\|_2\|\Theta\|_2.
\]

A Davis–Kahan-type eigenspace bound can control the projector error when there is a non-zero spectral gap around \(\tau_o\), but that additional theorem is not assumed automatically.

## 8. Failure boundaries

1. If \(B_d\) is rank deficient, shared coordinates are not identifiable in that domain.
2. If \(\gamma_d\) is extremely small, the bound may be vacuous.
3. The result assumes paired samples share the same \(\alpha\); class-sorted independent samples do not satisfy it.
4. Nonlinear sensor effects require a local linearization remainder term.
5. Canonical flow can reduce distributional discrepancy after estimation, but it cannot recover information already lost by a rank-deficient observation.

## 9. Experimental implication

For each shared modal slot, report:

- smallest singular value of the effective shared operator;
- estimated noise level;
- paired representation discrepancy;
- sensitivity to transfer-function perturbation;
- support-projector perturbation.

A claimed shared representation should degrade in the direction predicted by the bound when noise increases or \(\gamma_d\) decreases.
