# Theorem 10 — Sampling-gap distribution shift bound

## Status

**Proved for stable scalar Laplace modes and gap distributions with finite first moment.**

## Purpose

Irregular sampling changes the event-index dynamics of a continuous-time mode. This theorem bounds how much the effective event-domain multiplier and log-pole can change when the sampling-gap distribution shifts.

## 1. Continuous-time mode

Let

\[
s=-\rho+i\omega,
\qquad
\rho\geq0.
\]

For a non-negative sampling gap \(\Delta\), one event step multiplies the modal coordinate by

\[
e^{s\Delta}.
\]

For a gap distribution \(P\) on \([0,\infty)\), define the mean event multiplier

\[
\lambda_P(s)
=
\mathbb E_{\Delta\sim P}
[e^{s\Delta}].
\]

When a consistent branch of the complex logarithm exists, define the effective log-pole

\[
\bar s_P=\operatorname{Log}\lambda_P(s).
\]

## 2. Lemma 10.1 — stable exponential is Lipschitz on non-negative gaps

### Statement

For \(a,b\geq0\),

\[
|e^{sa}-e^{sb}|
\leq
|s|\,|a-b|.
\]

### Proof

Define \(f(t)=e^{st}\). Its derivative is

\[
f'(t)=se^{st}.
\]

Since \(\operatorname{Re}(s)=-\rho\leq0\),

\[
|f'(t)|
=|s|e^{-\rho t}
\leq|s|
\quad
\text{for }t\geq0.
\]

Using the integral form of the mean-value bound along the real interval from \(a\) to \(b\),

\[
|f(a)-f(b)|
\leq
\sup_{t\text{ between }a,b}|f'(t)|\,|a-b|
\leq
|s|\,|a-b|.
\]

∎

## 3. Theorem 10.1 — event-multiplier shift

### Statement

For any two gap distributions \(P,Q\in\mathcal P_1([0,\infty))\),

\[
\boxed{
|
\lambda_P(s)-\lambda_Q(s)
|
\leq
|s|W_1(P,Q)
}
\]

### Detailed proof

Let \(\pi\in\Pi(P,Q)\) be any coupling of random gaps \((\Delta_P,\Delta_Q)\). Then

\[
\begin{aligned}
|
\lambda_P(s)-\lambda_Q(s)
|
&=
\left|
\mathbb E_\pi
\left[
 e^{s\Delta_P}-e^{s\Delta_Q}
\right]
\right|\\
&\leq
\mathbb E_\pi
\left|
 e^{s\Delta_P}-e^{s\Delta_Q}
\right|\\
&\leq
|s|
\mathbb E_\pi
|
\Delta_P-\Delta_Q
|,
\end{aligned}
\]

where the last step uses Lemma 10.1. Taking the infimum over all couplings gives

\[
|
\lambda_P(s)-\lambda_Q(s)
|
\leq
|s|W_1(P,Q).
\]

∎

## 4. Lemma 10.2 — mean stability of the event multiplier

### Statement

\[
|\lambda_P(s)|\leq1.
\]

If \(\rho>0\) and \(P(\Delta>0)>0\), then

\[
|\lambda_P(s)|<1.
\]

### Proof

By Jensen's inequality for the norm,

\[
|\lambda_P(s)|
=
|
\mathbb E e^{s\Delta}
|
\leq
\mathbb E|e^{s\Delta}|
=
\mathbb E e^{-\rho\Delta}
\leq1.
\]

If \(\rho>0\), then \(e^{-\rho\Delta}<1\) whenever \(\Delta>0\). Positive probability of a positive gap makes the expectation strictly below one. ∎

## 5. Theorem 10.2 — effective log-pole shift

### Additional branch assumption

Assume \(\lambda_P(s)\) and \(\lambda_Q(s)\) lie in a simply connected region \(\Omega\subset\mathbb C\setminus\{0\}\) on which a single analytic logarithm branch is fixed. Assume the line segment joining the two multipliers remains in \(\Omega\) and

\[
|z|\geq m>0
\]

along that segment.

### Statement

\[
\boxed{
|
\bar s_P-
\bar s_Q
|
\leq
\frac{|s|}{m}
W_1(P,Q)
}
\]

### Detailed proof

Parameterize the line segment by

\[
z(r)=\lambda_Q+r(\lambda_P-
\lambda_Q),
\qquad r\in[0,1].
\]

Because the chosen logarithm is analytic on \(\Omega\),

\[
\operatorname{Log}\lambda_P-
\operatorname{Log}\lambda_Q
=
\int_0^1
\frac{z'(r)}{z(r)}dr.
\]

Here

\[
z'(r)=\lambda_P-
\lambda_Q.
\]

Taking absolute values,

\[
\begin{aligned}
|
\bar s_P-
\bar s_Q
|
&\leq
\int_0^1
\frac{|
\lambda_P-
\lambda_Q
|}{|z(r)|}dr\\
&\leq
\frac{|
\lambda_P-
\lambda_Q
|}{m}.
\end{aligned}
\]

Apply Theorem 10.1. ∎

## 6. Small-gap expansion

When the required moments exist and \(|s\Delta|\) is small enough for a controlled Taylor remainder,

\[
\lambda_P(s)
=
1+s\mathbb E_P[\Delta]
+
\frac{s^2}{2}\mathbb E_P[\Delta^2]
+
O(\mathbb E|s\Delta|^3).
\]

Using \(\log(1+x)=x-x^2/2+O(x^3)\),

\[
\bar s_P
\approx
s\mathbb E_P[\Delta]
+
\frac{s^2}{2}
\operatorname{Var}_P(\Delta).
\]

This approximation explains why both mean gap and gap variability alter event-domain damping and phase. It is an asymptotic expansion, not a replacement for Theorems 10.1–10.2.

## 7. Failure boundaries

1. If \(\lambda_P(s)\) approaches zero, the logarithm becomes unstable and the log-pole bound can diverge.
2. Oscillatory phase cancellation can place multipliers near a branch cut.
3. Non-i.i.d. or state-dependent gaps require conditional or path-dependent analysis.
4. The bound concerns the mean event multiplier, not the full distribution of random products.
5. A small \(W_1(P,Q)\) does not guarantee a small change for extremely high-frequency modes because the factor \(|s|\) grows with \(\omega\).

## 8. Experimental implication

Construct source and target gap distributions with controlled \(W_1\) distance. For fixed physical poles, measure:

- multiplier error \(|\widehat\lambda_P-
\widehat\lambda_Q|\);
- effective log-pole error when the branch condition holds;
- error as a function of modal frequency;
- failure near phase-cancellation regimes.

The observed error should scale no faster than the bound in an oracle known-mode experiment before a learned gap-aware encoder is evaluated.
