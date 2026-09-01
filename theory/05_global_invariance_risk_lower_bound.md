# Theorem 5 — Task-risk lower bound for complete cross-acquisition invariance

## Status

**Proved for paired deterministic invariance and Bayes-optimal logarithmic loss.**

## Purpose

This theorem formalizes the main HSE objection to global domain invariance: if a high-information acquisition observes task-relevant private content that a low-information acquisition cannot observe, forcing their complete representations to be equal removes that information.

## 1. Random variables

Let

\[
C
\]

be the common observable content and

\[
P
\]

be information available only in the higher-support acquisition. Define

\[
X_H=(C,P),
\qquad
X_L=C.
\]

Let \(Y\) be the downstream target.

## 2. Definition — paired complete invariance

A deterministic pair of encoders \((f_H,f_L)\) satisfies paired complete invariance when

\[
f_H(C,P)=f_L(C)
\quad\text{almost surely}.
\tag{5.1}
\]

This is stronger than equality of marginal distributions. The theorem does not apply when only

\[
f_H(X_H)\overset{d}=f_L(X_L)
\]

is enforced.

Let the common representation be

\[
Z=f_H(C,P)=f_L(C).
\]

## 3. Lemma 5.1 — invariant representation is measurable with respect to common content

### Statement

There exists a measurable function \(g\) such that

\[
Z=g(C)
\quad\text{almost surely}.
\]

### Proof

By Equation (5.1),

\[
Z=f_L(C).
\]

Choose \(g=f_L\). Therefore \(Z\) is a measurable function of \(C\). ∎

## 4. Lemma 5.2 — Bayes logarithmic risk equals conditional entropy

Let a probabilistic predictor output a conditional distribution \(q(\cdot\mid Z)\). Under logarithmic loss,

\[
\ell(q,Y)=-\log q(Y\mid Z).
\]

The Bayes-optimal predictor is the true conditional distribution

\[
q^*(\cdot\mid Z)=p(\cdot\mid Z),
\]

and the optimal risk is

\[
\mathcal R_{\log}^*(Z)=H(Y\mid Z).
\]

### Proof

For every fixed \(Z=z\), cross entropy decomposes as

\[
\mathbb E[-\log q(Y\mid z)\mid Z=z]
=
H(Y\mid Z=z)
+
D_{\mathrm{KL}}
\left(
 p(\cdot\mid z)
 \|q(\cdot\mid z)
\right).
\]

The KL term is non-negative and equals zero only when \(q=p\) almost everywhere. Averaging over \(Z\) gives the result. ∎

## 5. Theorem 5 — lower bound

### Statement

Under paired complete invariance,

\[
\boxed{
\mathcal R_{\log}^*(Z)
-
\mathcal R_{\log}^*(X_H)
\geq
I(Y;P\mid C)
}
\]

### Detailed proof

By Lemma 5.1, \(Z=g(C)\). Hence the variables form a Markov chain

\[
Y
\longleftrightarrow
C
\longrightarrow
Z.
\]

Conditioning on the less informative function \(Z=g(C)\) cannot reduce conditional entropy below conditioning on \(C\):

\[
H(Y\mid Z)
\geq
H(Y\mid C).
\tag{5.2}
\]

By Lemma 5.2,

\[
\mathcal R_{\log}^*(Z)=H(Y\mid Z),
\]

and because \(X_H=(C,P)\),

\[
\mathcal R_{\log}^*(X_H)=H(Y\mid C,P).
\]

Therefore

\[
\begin{aligned}
\mathcal R_{\log}^*(Z)
-
\mathcal R_{\log}^*(X_H)
&=
H(Y\mid Z)-H(Y\mid C,P)
\\
&\geq
H(Y\mid C)-H(Y\mid C,P)
\\
&=
I(Y;P\mid C).
\end{aligned}
\]

The last equality is the definition of conditional mutual information. ∎

## 6. Corollary 5.1 — strict harm condition

If

\[
I(Y;P\mid C)>0,
\]

then the Bayes-optimal logarithmic risk from a fully invariant representation is strictly worse than the Bayes-optimal risk from the high-support observation.

## 7. Corollary 5.2 — when complete invariance is harmless

If

\[
Y\perp\!\!\!\perp P\mid C,
\]

then

\[
I(Y;P\mid C)=0.
\]

The theorem gives no positive lower bound. In this case, private information may be irrelevant for the chosen task even though it remains physically present.

## 8. Tightness example

Let \(C\) be constant, let \(P\sim\operatorname{Bernoulli}(1/2)\), and set \(Y=P\). Then

\[
I(Y;P\mid C)=H(Y)=\log2.
\]

Any paired invariant representation is constant because it must be a function of constant \(C\). Its Bayes log risk is \(\log2\). The full high-support input determines \(Y\), so its Bayes log risk is zero. Equality holds in the theorem.

## 9. Counterexample to a weaker interpretation

Equality of representation marginals does not imply the theorem's measurability conclusion. It is possible to choose two encoders whose outputs have the same distribution while the high-domain output still encodes \(P\) through a measure-preserving relabeling. Therefore the paper must distinguish:

```text
paired pointwise invariance
from
marginal domain confusion
```

## 10. Experimental implication

A decisive experiment must create paired acquisition views of the same latent event and vary only the private component. It should compare:

1. complete paired alignment;
2. shared-only alignment with private retention;
3. no alignment.

The experiment must estimate whether private information has incremental task value beyond shared information. A practical statistic is the performance or proper-scoring-rule improvement from adding the private block to a shared-only predictor. If no incremental value is observed, this theorem does not support a claimed task advantage.
