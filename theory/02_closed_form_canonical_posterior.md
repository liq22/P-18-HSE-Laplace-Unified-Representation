# Theory 2 — Closed-form canonical modal posterior

## Status

Proved for a Gaussian prior and linear-Gaussian acquisition.

## Assumptions

\[
\Theta\sim\mathcal N(\mu_0,\Sigma_0),
\qquad
X_d\mid\Theta\sim\mathcal N(A_d\Theta,R_d),
\]

with \(\Sigma_0\succ0\) and \(R_d\succ0\).

## Lemma 2.1 — posterior natural parameters

The posterior precision and natural parameter are

\[
\Lambda_d
=\Sigma_0^{-1}+J_d,
\]

\[
\eta_d
=\Sigma_0^{-1}\mu_0+b_d.
\]

### Proof

The log posterior is, up to a constant,

\[
-\frac12(\theta-\mu_0)^T\Sigma_0^{-1}(\theta-\mu_0)
-\frac12(x_d-A_d\theta)^TR_d^{-1}(x_d-A_d\theta).
\]

Collect the quadratic terms in \(\theta\):

\[
-\frac12\theta^T(\Sigma_0^{-1}+J_d)\theta.
\]

Collect the linear terms:

\[
\theta^T(\Sigma_0^{-1}\mu_0+b_d).
\]

These are the stated natural parameters. ∎

## Theorem 2 — canonical Gaussian posterior

The posterior is

\[
\boxed{
\Theta\mid X_d
\sim
\mathcal N(\mu_d,\Sigma_d)
}
\]

with

\[
\boxed{
\Sigma_d=(\Sigma_0^{-1}+J_d)^{-1}
}
\]

and

\[
\boxed{
\mu_d=\Sigma_d(\Sigma_0^{-1}\mu_0+b_d).
}
\]

### Proof

Since \(\Sigma_0^{-1}\succ0\) and \(J_d\succeq0\), \(\Lambda_d\succ0\). Complete the square:

\[
-\frac12\theta^T\Lambda_d\theta+\theta^T\eta_d
=
-\frac12(\theta-\Lambda_d^{-1}\eta_d)^T
\Lambda_d
(\theta-\Lambda_d^{-1}\eta_d)+C.
\]

The normalized density is Gaussian with covariance \(\Lambda_d^{-1}\) and mean \(\Lambda_d^{-1}\eta_d\). ∎

## Consequence for HSE–LLapDiff

Every acquisition posterior lives in the same \(\Theta\) coordinate system. Different sampling rates may produce different \(b_d,J_d\), and therefore different posterior means and covariances, without changing the semantic coordinate system.

The closed-form posterior is the strongest simple baseline. LLapDiff has a justified role only when the true conditional is nonlinear, non-Gaussian, multimodal, or otherwise outside this family.

## Executable prediction

The analytic implementation must match the displayed mean and covariance and reject non-positive-definite covariance inputs.

## Failure conditions

- The posterior is not generally Gaussian under nonlinear acquisition or non-Gaussian prior/noise.
- Correct coordinates require paired or otherwise anchored modal semantics.
- A closed-form posterior does not prove that an HSE token encoder can estimate its natural parameters from raw signals.
