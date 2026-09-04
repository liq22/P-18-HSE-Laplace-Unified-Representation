# Theory 7 — Stability of local Laplace modal coordinates

## Status

Proved for stable real blocks representing complex-conjugate poles.

## Definition

For damping \(\rho>0\) and angular frequency \(\omega\geq0\), define

\[
A=
\begin{bmatrix}
-\rho&-\omega\\
\omega&-\rho
\end{bmatrix}.
\]

## Lemma 7.1 — closed-form transition

\[
e^{At}
=
e^{-\rho t}
\begin{bmatrix}
\cos\omega t&-\sin\omega t\\
\sin\omega t&\cos\omega t
\end{bmatrix}.
\]

### Proof

Write \(A=-\rho I+\omega J\), where \(J^2=-I\). The two terms commute, so their exponentials factor. The power series of \(e^{\omega Jt}\) separates into cosine and sine terms. ∎

## Theorem 7 — exact decay norm

\[
\boxed{
\|e^{At}\|_2=e^{-\rho t}.
}
\]

### Proof

The matrix multiplying \(e^{-\rho t}\) in Lemma 7.1 is orthogonal and has operator norm one. ∎

## Corollary 7.1 — block system

For a block-diagonal modal system whose damping rates satisfy \(\rho_k\geq\rho_{\min}>0\),

\[
\|z(t)\|_2
\leq
e^{-\rho_{\min}t}\|z(0)\|_2.
\]

## Role in the paper

This is a supporting property inherited from stable Laplace modal modeling. It is not the primary novelty of HSE–LLapDiff.

## Failure conditions

- Persistent forced harmonics are not autonomous decaying transients.
- Switching, impacts, and time-varying speed may require window-local or richer dynamics.
- Stability of the modal mean does not prove posterior calibration.
