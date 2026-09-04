# Theory 5 — Information loss under complete deterministic invariance

## Status

Proved for paired deterministic invariance and Bayes-optimal logarithmic loss.

## Setup

Let a high-support acquisition observe

\[
X_H=(C,P),
\]

where \(C\) is common information and \(P\) is information unavailable to the low-support acquisition

\[
X_L=C.
\]

Let deterministic encoders satisfy complete paired invariance:

\[
f_H(C,P)=f_L(C)=Z
\quad\text{almost surely}.
\]

## Lemma 5.1 — the invariant representation is a function of common information

There exists \(g\) such that

\[
Z=g(C)
\quad\text{almost surely}.
\]

### Proof

Take \(g=f_L\). The equality follows from the invariance condition. ∎

## Lemma 5.2 — optimal log-loss risk

For any representation \(V\), the Bayes-optimal logarithmic risk is

\[
\mathcal R^*_{\log}(V)=H(Y\mid V).
\]

### Proof

Conditional cross entropy equals conditional entropy plus a non-negative conditional KL divergence. It is minimized by the true conditional distribution. ∎

## Theorem 5 — task-risk lower bound

\[
\boxed{
\mathcal R^*_{\log}(Z)
-
\mathcal R^*_{\log}(X_H)
\geq
I(Y;P\mid C).
}
\]

### Proof

By Lemma 5.1, \(Z\) is a function of \(C\), so

\[
H(Y\mid Z)\geq H(Y\mid C).
\]

Using Lemma 5.2 and \(X_H=(C,P)\),

\[
\begin{aligned}
\mathcal R^*_{\log}(Z)-\mathcal R^*_{\log}(X_H)
&=H(Y\mid Z)-H(Y\mid C,P)\\
&\geq H(Y\mid C)-H(Y\mid C,P)\\
&=I(Y;P\mid C).
\end{aligned}
\]

∎

## Tightness example

Let \(C\) be constant, \(P\sim\operatorname{Bernoulli}(1/2)\), and \(Y=P\). Then complete invariance makes \(Z\) constant, yielding risk \(\log2\), while \(X_H\) predicts \(Y\) exactly. Equality holds.

## HSE–LLapDiff implication

The proposed method uses a common coordinate system but permits different posterior uncertainty and private information across acquisitions. It does not force the entire deterministic output to be equal.

## Failure conditions

- If \(I(Y;P\mid C)=0\), the theorem gives no positive penalty.
- Equality of marginal representation distributions is weaker than paired pointwise invariance and is not covered by this theorem.
- The result does not prove that LLapDiff is the best way to preserve uncertainty.
