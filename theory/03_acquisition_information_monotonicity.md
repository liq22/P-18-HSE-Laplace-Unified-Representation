# Theory 3 — Acquisition information and posterior uncertainty monotonicity

## Status

Proved under Loewner ordering of acquisition information matrices.

## Purpose

The central calibration prediction is not “higher sampling rate always means lower uncertainty.” It is:

\[
J_H\succeq J_L
\quad\Longrightarrow\quad
\Sigma_H\preceq\Sigma_L.
\]

Sampling rate, sensor response, noise, filtering, and missingness influence this order through \(J=A^TR^{-1}A\).

## Lemma 3.1 — inverse reverses positive-definite order

If

\[
B\succeq A\succ0,
\]

then

\[
B^{-1}\preceq A^{-1}.
\]

### Proof

Let \(C=A^{-1/2}BA^{-1/2}\). Then \(C\succeq I\). Every eigenvalue of \(C\) is at least one, so every eigenvalue of \(C^{-1}\) is at most one. Hence \(C^{-1}\preceq I\). Congruence by \(A^{-1/2}\) gives

\[
B^{-1}=A^{-1/2}C^{-1}A^{-1/2}\preceq A^{-1}.
\]

∎

## Theorem 3 — posterior covariance order

If

\[
J_H\succeq J_L,
\]

then

\[
\boxed{
\Sigma_H
=(\Sigma_0^{-1}+J_H)^{-1}
\preceq
(\Sigma_0^{-1}+J_L)^{-1}
=\Sigma_L.
}
\]

### Proof

Adding \(\Sigma_0^{-1}\succ0\) preserves the Loewner order:

\[
\Sigma_0^{-1}+J_H
\succeq
\Sigma_0^{-1}+J_L
\succ0.
\]

Apply Lemma 3.1. ∎

## Corollary 3.1 — directional uncertainty

For every direction \(u\),

\[
u^T\Sigma_Hu\leq u^T\Sigma_Lu.
\]

Thus every modal direction has no larger posterior variance under the information-dominating acquisition.

## Corollary 3.2 — Gaussian entropy

For dimension \(m\),

\[
H(\Theta\mid X_d)
=\frac12\log\left((2\pi e)^m\det\Sigma_d\right).
\]

The covariance order implies

\[
\det\Sigma_H\leq\det\Sigma_L,
\]

and therefore

\[
H(\Theta\mid X_H)\leq H(\Theta\mid X_L).
\]

## Executable prediction

For deliberately nested acquisition operators, the smallest eigenvalues of

\[
J_H-J_L
\]

and

\[
\Sigma_L-\Sigma_H
\]

must be non-negative up to numerical tolerance.

## Failure conditions

- A higher nominal sampling rate does not guarantee \(J_H\succeq J_L\).
- Different sensor noise or bandwidth can reverse the order.
- Approximate learned posterior variances may violate the theorem; such violation is evidence of miscalibration or model misspecification, not a refutation of the linear-Gaussian result.
