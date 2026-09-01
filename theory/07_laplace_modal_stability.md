# Theorem 7 — Stability of the Laplace modal representation

## Status

**Proved for the finite block-diagonal stable modal system defined below.**

## Purpose

The unified representation is placed in Laplace-modal coordinates so that its deterministic physical-time evolution can be evaluated at arbitrary timestamps while retaining an explicit stability condition. This theorem establishes exponential stability for autonomous transients and bounded-input bounded-state behavior for forced dynamics.

## 1. One real modal block

For damping \(\rho_k>0\) and angular frequency \(\omega_k\geq0\), define

\[
A_k=
\begin{bmatrix}
-\rho_k&-\omega_k\\
\omega_k&-\rho_k
\end{bmatrix}.
\]

Write

\[
A_k=-\rho_kI+\omega_kJ,
\qquad
J=
\begin{bmatrix}
0&-1\\
1&0
\end{bmatrix}.
\]

Because \(I\) and \(J\) commute,

\[
e^{A_kt}
=e^{-\rho_kt}e^{\omega_kJt}.
\]

## 2. Lemma 7.1 — the oscillatory factor is orthogonal

### Statement

\[
e^{\omega_kJt}
=
\begin{bmatrix}
\cos(\omega_kt)&-\sin(\omega_kt)\\
\sin(\omega_kt)&\cos(\omega_kt)
\end{bmatrix}
=R(\omega_kt),
\]

and

\[
R(\omega_kt)^\top R(\omega_kt)=I.
\]

### Proof

Since \(J^2=-I\), the matrix exponential power series separates into even and odd terms:

\[
\begin{aligned}
e^{\omega Jt}
&=
I+\omega Jt+\frac{(\omega Jt)^2}{2!}+\cdots\\
&=
I\left(1-\frac{(\omega t)^2}{2!}+\cdots\right)
+J\left(\omega t-\frac{(\omega t)^3}{3!}+\cdots\right)\\
&=I\cos(\omega t)+J\sin(\omega t),
\end{aligned}
\]

which is the displayed rotation matrix. Direct multiplication gives orthogonality. ∎

## 3. Lemma 7.2 — exact transition norm

### Statement

For the Euclidean operator norm,

\[
\boxed{
\|e^{A_kt}\|_2=e^{-\rho_kt}
}
\]

for all \(t\geq0\).

### Proof

By Lemma 7.1,

\[
e^{A_kt}=e^{-\rho_kt}R(\omega_kt),
\]

and every orthogonal matrix has operator norm one. Therefore

\[
\|e^{A_kt}\|_2
=e^{-\rho_kt}\|R(\omega_kt)\|_2
=e^{-\rho_kt}.
\]

∎

## 4. Block-diagonal system

Let

\[
A=\operatorname{diag}(A_1,\ldots,A_K)
\]

and define

\[
\rho_{\min}=\min_k\rho_k>0.
\]

## 5. Theorem 7.1 — exponential stability of autonomous transients

### Statement

For

\[
\dot z(t)=Az(t),
\]

we have

\[
\boxed{
\|z(t)\|_2
\leq
 e^{-\rho_{\min}t}
 \|z(0)\|_2
}
\]

for every \(t\geq0\).

### Detailed proof

The exponential of a block-diagonal matrix is block diagonal:

\[
e^{At}
=
\operatorname{diag}
\left(
 e^{A_1t},\ldots,e^{A_Kt}
\right).
\]

The operator norm of a block-diagonal matrix is the maximum operator norm of its blocks. By Lemma 7.2,

\[
\|e^{At}\|_2
=
\max_k e^{-\rho_kt}
=
e^{-\rho_{\min}t}.
\]

The solution is \(z(t)=e^{At}z(0)\), hence

\[
\|z(t)\|_2
\leq
\|e^{At}\|_2\|z(0)\|_2
=
e^{-\rho_{\min}t}\|z(0)\|_2.
\]

∎

## 6. Theorem 7.2 — bounded forced response

Consider

\[
\dot z(t)=Az(t)+Bu(t),
\]

where \(u\) is essentially bounded:

\[
\|u\|_\infty
=
\operatorname*{ess\,sup}_{t\geq0}\|u(t)\|_2<\infty.
\]

### Statement

\[
\boxed{
\|z(t)\|_2
\leq
 e^{-\rho_{\min}t}\|z(0)\|_2
+
\frac{\|B\|_2}{\rho_{\min}}
\left(1-e^{-\rho_{\min}t}\right)
\|u\|_\infty
}
\]

and consequently

\[
\limsup_{t\to\infty}\|z(t)\|_2
\leq
\frac{\|B\|_2}{\rho_{\min}}
\|u\|_\infty.
\]

### Detailed proof

Variation of constants gives

\[
z(t)
=
e^{At}z(0)
+
\int_0^t e^{A(t-s)}Bu(s)\,ds.
\]

Taking norms and applying Theorem 7.1,

\[
\begin{aligned}
\|z(t)\|_2
&\leq
e^{-\rho_{\min}t}\|z(0)\|_2
+
\int_0^t
 e^{-\rho_{\min}(t-s)}
 \|B\|_2
 \|u(s)\|_2
 ds\\
&\leq
e^{-\rho_{\min}t}\|z(0)\|_2
+
\|B\|_2\|u\|_\infty
\int_0^t e^{-\rho_{\min}(t-s)}ds.
\end{aligned}
\]

The integral is

\[
\int_0^t e^{-\rho_{\min}(t-s)}ds
=
\frac{1-e^{-\rho_{\min}t}}{\rho_{\min}}.
\]

Substitution proves the bound. Taking \(t\to\infty\) gives the limit superior. ∎

## 7. Corollary 7.1 — output stability

For a linear readout \(y=Cz\),

\[
\|y(t)\|_2
\leq
\|C\|_2\|z(t)\|_2.
\]

Thus the same decay and forced-response bounds hold with an additional factor \(\|C\|_2\).

## 8. Corollary 7.2 — stable pole chart

The parameterization

\[
\rho_k=\rho_{\min}+\operatorname{softplus}(a_k)
\]

guarantees \(\rho_k>\rho_{\min}>0\) for every finite \(a_k\). Therefore every decoded autonomous modal system satisfies Theorem 7.1.

The bounded sigmoid frequency chart keeps \(\omega_k\) inside its declared HSE physical-frequency slot but does not affect stability because the rotation factor has norm one.

## 9. Local approximation error

Suppose the true local trajectory is

\[
s(t)=Cz(t)+r(t)
\]

with

\[
\sup_{t\in[0,T]}\|r(t)\|
\leq
\varepsilon_{\mathrm{modal}}.
\]

Then every reconstruction or prediction bound derived from the modal system inherits an additive \(\varepsilon_{\mathrm{modal}}\) term. Stability of the approximation does not make the approximation exact.

## 10. Failure boundaries

1. A forced periodic component is not expected to decay to zero. It must be represented through \(u(t)\) or a zero-damping-but-bounded forced block, not misdescribed as an autonomous transient.
2. Switching, impacts, friction, and time-varying speed may require window-local poles or exogenous phase variables.
3. A positive damping chart guarantees stability of the parameterized mean dynamics, not calibration of stochastic fluctuations.
4. Discrete numerical solvers can violate the continuous-time bound when step sizes are unstable.

## 11. Experimental implication

Tests should verify:

- \(\|e^{A_kt}\|_2=e^{-\rho_kt}\) for random admissible modes;
- no decoded damping is non-positive;
- frequencies stay inside their assigned support slots;
- irregular query timestamps produce the same closed-form trajectory as regular timestamps sampled at the same times;
- any non-decaying forced component is evaluated against the forced bound, not the autonomous bound.
