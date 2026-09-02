# Theorem 22 — When Diffusion has no population scoring advantage

## Status

**Decision-theoretic result for strictly proper scoring rules.**

## Purpose

Diffusion is an expressive posterior model, not an automatic scientific
contribution. If a simpler conditional family already contains the true
source-supported missing posterior, no larger model can improve the population
proper score.

## 1. Setup

Let \(X=(C^*,P,O_d)\) and let the true missing conditional be

\[
q^*(m\mid x).
\]

Let \(S(q,m)\) be a strictly proper scoring rule. Define population risk

\[
\mathcal R(q)
=
\mathbb E_{X}
\mathbb E_{M\sim q^*(\cdot\mid X)}
S(q(\cdot\mid X),M).
\]

Let

\[
\mathcal Q_{\mathrm{simple}}
\subseteq
\mathcal Q_{\mathrm{diff}}
\]

be a simpler family, such as heteroscedastic Gaussian or a finite mixture,
nested inside a more expressive Diffusion family.

## 2. Theorem 22.1 — no advantage when the truth is in the simple family

If

\[
q^*\in\mathcal Q_{\mathrm{simple}},
\]

then

\[
\boxed{
\inf_{q\in\mathcal Q_{\mathrm{simple}}}\mathcal R(q)
=
\inf_{q\in\mathcal Q_{\mathrm{diff}}}\mathcal R(q)
=
\mathcal R(q^*).
}
\]

Under strict propriety, every population minimizer equals \(q^*\) almost surely.

### Proof

Strict propriety states that for each \(x\), the conditional expected score is
uniquely minimized by the true conditional \(q^*(\cdot\mid x)\). Since
\(q^*\) belongs to both nested families, both infima are at most
\(\mathcal R(q^*)\). No candidate can have lower risk than the true
conditional under a proper score, so both infima equal that value. Strictness
gives uniqueness almost surely. ∎

## 3. Corollary 22.1 — log-score gap is conditional KL divergence

For the negative log score,

\[
S(q,m)=-\log q(m),
\]

the excess risk is

\[
\mathcal R(q)-\mathcal R(q^*)
=
\mathbb E_X
\operatorname{KL}
\left(
q^*(\cdot\mid X)
\|
q(\cdot\mid X)
\right).
\]

Thus Diffusion has population headroom only when the best simple family leaves a
positive conditional KL gap.

## 4. Multimodality is not sufficient by itself

A finite mixture may already represent a multimodal posterior. Diffusion is
justified only when the evaluated simple family fails under the same
information, capacity and optimization budget.

## 5. Failure boundaries

1. Finite-sample regularization can make a simpler model outperform a richer
   model even when the truth is outside the simple family.
2. Optimization may fail to reach either family optimum.
3. CRPS and log score emphasize different aspects.
4. Approximate Diffusion likelihoods complicate direct NLL comparison.
5. Better sample quality without better task or calibration evidence is not
   sufficient.

## 6. Experimental implication

Use the escalation ladder:

```text
posterior mean
heteroscedastic Gaussian
finite mixture
support-aware Diffusion
```

Promote Diffusion only when it yields a paired, independent-unit improvement in
a predeclared proper score and calibration metric over the strongest simpler
family.
