# Theorem 15 — Soft observability and fixed-slot stability

## Status

**Proved for logistic smoothing of a fixed modal-slot information score.**

## Purpose

A hard threshold can change a slot role discontinuously when the estimated
Gramian is near the threshold. Soft observability provides a continuous
diagnostic without changing the exact hard-support theorem.

## 1. Definition

For modal information \(g\ge0\), threshold \(\tau_o>0\) and temperature
\(T_o>0\), define

\[
o_{T_o}(g)
=
\sigma\!\left(\frac{g-\tau_o}{T_o}\right),
\qquad
\sigma(x)=\frac1{1+e^{-x}}.
\]

## 2. Lemma 15.1 — monotonicity and derivative bound

### Statement

\[
0<o_{T_o}(g)<1,
\qquad
\frac{d}{dg}o_{T_o}(g)
=
\frac1{T_o}o_{T_o}(g)(1-o_{T_o}(g)),
\]

and therefore

\[
\boxed{
\left|\frac{d}{dg}o_{T_o}(g)\right|
\leq
\frac1{4T_o}.
}
\]

### Proof

Differentiate the logistic function. Since \(x(1-x)\le1/4\) for
\(x\in[0,1]\), the derivative bound follows. The derivative is positive, so the
weight is monotone. ∎

## 3. Theorem 15.1 — perturbation stability

For an information perturbation \(\delta\),

\[
\boxed{
|o_{T_o}(g+\delta)-o_{T_o}(g)|
\leq
\frac{|\delta|}{4T_o}.
}
\]

### Proof

Apply the mean-value theorem and Lemma 15.1. ∎

## 4. Theorem 15.2 — hard-support limit

For \(g\neq\tau_o\),

\[
\lim_{T_o\downarrow0}o_{T_o}(g)
=
\mathbf 1\{g>\tau_o\}.
\]

At the threshold,

\[
o_{T_o}(\tau_o)=\frac12
\]

for every \(T_o\).

### Proof

If \(g>\tau_o\), the logistic argument tends to \(+\infty\); if
\(g<\tau_o\), it tends to \(-\infty\). The logistic limits are one and zero,
respectively. At equality, the argument is zero. ∎

## 5. Lemma 15.2 — four soft role weights sum to one

For a fixed slot \(k\), let \(o_j\in[0,1]\) denote source-domain support
probabilities. Interpret independent latent indicators
\(S_j\sim\mathrm{Bernoulli}(o_j)\). For current domain \(d\), define

\[
w_c=\prod_j o_j,
\]

\[
w_{p,d}=o_d-w_c,
\]

\[
w_{m,d}
=
(1-o_d)
\left[
1-\prod_{j\neq d}(1-o_j)
\right],
\]

\[
w_0=\prod_j(1-o_j).
\]

Then all weights are non-negative and

\[
\boxed{
w_c+w_{p,d}+w_{m,d}+w_0=1.
}
\]

### Proof

Non-negativity is immediate because \(w_c\le o_d\). Also,

\[
w_c+w_{p,d}=o_d.
\]

For the remaining cases,

\[
w_{m,d}+w_0
=
(1-o_d)
\left[
1-\prod_{j\neq d}(1-o_j)
\right]
+
(1-o_d)\prod_{j\neq d}(1-o_j)
=
1-o_d.
\]

Summing gives one. ∎

## 6. Interpretation

The soft weights are uncertainty diagnostics over a fixed role partition. They
do not prove that source-domain support indicators are statistically
independent. The exact four-way decomposition remains the hard reference.

## 7. Failure boundaries

1. Small \(T_o\) makes the diagnostic sensitive because the Lipschitz constant
   grows as \(1/T_o\).
2. Large \(T_o\) blurs physically distinct roles.
3. Correlated support uncertainty invalidates the independent-Bernoulli
   interpretation of the role weights.
4. Soft weight does not establish conditional recoverability.
5. The threshold must remain source-only.

## 8. Experimental implication

Report the threshold margin \(g-\tau_o\), the temperature, and sensitivity to
operator perturbation. A claim should not rely on a slot whose role changes
under perturbations smaller than the estimated acquisition uncertainty.
