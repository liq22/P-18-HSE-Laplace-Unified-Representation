# Theorem 9 — Paired downstream-risk bound for an approximate representation

## Status

**Proved for a same-event coupling and a downstream loss that is uniformly
Lipschitz in the representation.**

## Purpose

A marginal Wasserstein distance alone cannot control task risk: two
representations may have identical marginals while reversing their label
semantics. The revised result is paired. Ideal and approximate representations
must be coupled through the same latent event and target.

## 1. Paired setup

Let

\[
(Z,\widehat Z,Y)
\]

be defined on one probability space, where

\[
Z=(Z_c,Z_p,Z_m)
\]

is the ideal source-supported representation and

\[
\widehat Z
=
(\widehat Z_c,\widehat Z_p,\widehat Z_m)
\]

is its approximation for the same latent event. Global-null coordinates are
excluded from both.

Use the additive physical metric

\[
d(z,\widehat z)
=
w_c\|z_c-\widehat z_c\|_2
+
w_p\|z_p-\widehat z_p\|_2
+
w_m\|z_m-\widehat z_m\|_2,
\tag{9.1}
\]

with declared positive unit-normalizing weights.

Let \(h\) be a fixed decision rule. Assume that for every target value \(y\),

\[
|
\ell(h(\widehat z),y)
-
\ell(h(z),y)
|
\leq
L\,d(\widehat z,z).
\tag{9.2}
\]

## 2. Lemma 9.1 — paired loss difference

Under Equation (9.2),

\[
\left|
\mathbb E[
\ell(h(\widehat Z),Y)]
-
\mathbb E[
\ell(h(Z),Y)]
\right|
\leq
L\,
\mathbb E[d(\widehat Z,Z)].
\tag{9.3}
\]

### Proof

For every sample,

\[
|
\ell(h(\widehat Z),Y)
-
\ell(h(Z),Y)
|
\leq
L\,d(\widehat Z,Z).
\]

Take expectations and use
\(|\mathbb E X|\leq\mathbb E|X|\). ∎

## 3. Lemma 9.2 — blockwise paired error

Define

\[
\varepsilon_{\mathrm{flow}}
=
w_c\,
\mathbb E\|
\widehat Z_c-Z_c
\|,
\]

\[
\varepsilon_{\mathrm{private}}
=
w_p\,
\mathbb E\|
\widehat Z_p-Z_p
\|,
\]

\[
\varepsilon_{\mathrm{missing}}
=
w_m\,
\mathbb E\|
\widehat Z_m-Z_m
\|.
\]

Then

\[
\mathbb E[d(\widehat Z,Z)]
=
\varepsilon_{\mathrm{flow}}
+
\varepsilon_{\mathrm{private}}
+
\varepsilon_{\mathrm{missing}}.
\]

### Proof

Substitute the additive metric and use linearity of expectation. ∎

## 4. Pre-transport approximation terms

Let modal-analysis and support-assignment errors be
\(\varepsilon_{\mathrm{modal}}\) and
\(\varepsilon_{\mathrm{support}}\), both evaluated under the same-event
coupling. Assume the implementation admits intermediate representations for
which

\[
\mathbb E[d(\widehat Z,Z)]
\leq
\varepsilon_{\mathrm{flow}}
+
\varepsilon_{\mathrm{private}}
+
\varepsilon_{\mathrm{post}}
+
\varepsilon_{\mathrm{modal}}
+
\varepsilon_{\mathrm{support}}.
\tag{9.4}
\]

Here \(\varepsilon_{\mathrm{post}}\) is the recoverable-missing posterior error
under a declared conditional coupling. It is not a marginal distance detached
from event identity.

## 5. Theorem 9 — additive paired risk bound

Under Equations (9.2) and (9.4),

\[
\boxed{
|
\mathcal R_{\widehat Z}(h)
-
\mathcal R_Z(h)
|
\leq
L
\left(
\varepsilon_{\mathrm{flow}}
+
\varepsilon_{\mathrm{private}}
+
\varepsilon_{\mathrm{post}}
+
\varepsilon_{\mathrm{modal}}
+
\varepsilon_{\mathrm{support}}
\right)
}.
\tag{9.5}
\]

If observed-private identity is exact, then
\(\varepsilon_{\mathrm{private}}=0\).

### Detailed proof

Lemma 9.1 bounds the task-risk difference by the paired representation error.
Equation (9.4) decomposes that error into the declared mechanisms. Substitute
Equation (9.4) into Equation (9.3). Exact private identity removes the private
term. ∎

## 6. Counterexample 9.1 — equal marginals do not control semantic risk

Let \(Y\sim\operatorname{Bernoulli}(1/2)\), and define

\[
Z=Y,
\qquad
\widehat Z=1-Y.
\]

Both representation marginals are Bernoulli\((1/2)\), so

\[
W_1(
\operatorname{Law}(Z),
\operatorname{Law}(\widehat Z))
=0.
\]

For \(h(z)=z\), the risk of \(Z\) is zero and the risk of \(\widehat Z\) is
one under 0--1 loss. Marginal equality therefore cannot replace a same-event
semantic coupling. ∎

## 7. Interpretation

| Error term | Primary diagnostic |
|---|---|
| \(\varepsilon_{\mathrm{flow}}\) | paired shared modal error after canonicalization |
| \(\varepsilon_{\mathrm{private}}\) | pre/post observed-private drift |
| \(\varepsilon_{\mathrm{post}}\) | paired CRPS, NLL or conditional transport error |
| \(\varepsilon_{\mathrm{modal}}\) | same-event modal reconstruction error |
| \(\varepsilon_{\mathrm{support}}\) | true-versus-estimated slot-role error |

Domain-level MMD, Wasserstein distance and acquisition-ID probes remain useful
secondary diagnostics. They do not substitute for the paired primary errors.

## 8. Failure boundaries

1. The theorem applies to a fixed \(h\); retraining adds estimation and
   optimization error.
2. Hard 0--1 decisions are not globally Lipschitz.
3. A valid coupling requires the same latent event or another justified
   semantic correspondence.
4. Equation (9.4) is an assumed or separately proved approximation
   decomposition; it must be measured rather than inferred from architecture.
5. Unit normalization can make one modal component dominate the metric.
6. Global-null coordinates are excluded because no source-supported paired
   target exists for them.

## 9. Experimental implication

Use \(\texttt{latent_event_id}\) as the independent paired unit. Report one
primary metric for each mechanism:

- paired shared modal error;
- observed-private drift;
- CRPS or NLL for recoverable-missing modes;
- modal reconstruction error;
- support-role error.

Estimate paired confidence intervals across latent events or, on real data,
across independent recordings or machines. A marginal alignment score alone
cannot support the task-risk claim.
