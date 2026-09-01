# Theorem 9 — Downstream risk bound for an approximate unified representation

## Status

**Proved for a Lipschitz conditional risk functional and Wasserstein-1 approximation errors.**

## Purpose

The ideal unified representation is not available exactly. The shared flow, unobserved posterior, modal dictionary, and observable support are all approximated. This theorem separates their contributions to downstream risk.

## 1. Ideal and approximate representations

Let the ideal distribution-valued representation be

\[
\mu^U
=
\operatorname{Law}(Z_c^*,Z_p,Z_u).
\]

Let an implementation produce

\[
\widehat\mu^U
=
\operatorname{Law}(\widehat Z_c,\widehat Z_p,\widehat Z_u).
\]

Equip the product space with the additive metric

\[
d(z,z')
=
\|z_c-z_c'\|_2
+
\|z_p-z_p'\|_2
+
\|z_u-z_u'\|_2.
\tag{9.1}
\]

Let a fixed downstream decision rule \(h\) have conditional risk function

\[
\varphi_h(z)
=
\mathbb E[\ell(h(z),Y)\mid Z=z].
\]

Assume \(\varphi_h\) is \(L\)-Lipschitz under (9.1):

\[
|\varphi_h(z)-\varphi_h(z')|
\leq
L d(z,z').
\tag{9.2}
\]

This is the key task-regularity assumption.

## 2. Lemma 9.1 — risk difference is bounded by Wasserstein distance

### Statement

\[
\left|
\int\varphi_h\,d\widehat\mu^U
-
\int\varphi_h\,d\mu^U
\right|
\leq
L W_1(\widehat\mu^U,\mu^U).
\]

### Proof

The Kantorovich–Rubinstein duality states

\[
W_1(\widehat\mu^U,\mu^U)
=
\sup_{\|f\|_{\mathrm{Lip}}\leq1}
\left|
\int f\,d\widehat\mu^U
-
\int f\,d\mu^U
\right|.
\]

The function \(f=\varphi_h/L\) is 1-Lipschitz by Equation (9.2). Therefore

\[
\left|
\int\frac{\varphi_h}{L}\,d\widehat\mu^U
-
\int\frac{\varphi_h}{L}\,d\mu^U
\right|
\leq
W_1(\widehat\mu^U,\mu^U).
\]

Multiplying by \(L\) proves the lemma. ∎

## 3. Lemma 9.2 — componentwise coupling bound

Suppose there exists a joint coupling of ideal and approximate blocks such that

\[
\mathbb E\|
\widehat Z_c-Z_c^*
\|
\leq
\varepsilon_{\mathrm{flow}},
\]

\[
\mathbb E\|
\widehat Z_p-Z_p
\|
\leq
\varepsilon_{\mathrm{private}},
\]

\[
\mathbb E\|
\widehat Z_u-Z_u
\|
\leq
\varepsilon_{\mathrm{post}}.
\]

Then

\[
W_1(\widehat\mu^U,\mu^U)
\leq
\varepsilon_{\mathrm{flow}}
+
\varepsilon_{\mathrm{private}}
+
\varepsilon_{\mathrm{post}}.
\]

### Proof

The Wasserstein distance is the infimum of expected transport cost over all couplings. Evaluate it at the stated coupling. By the additive metric,

\[
\begin{aligned}
\mathbb E d(\widehat Z,Z)
={}&
\mathbb E\|\widehat Z_c-Z_c^*\|
+
\mathbb E\|\widehat Z_p-Z_p\|
+
\mathbb E\|\widehat Z_u-Z_u\|\\
\leq{}&
\varepsilon_{\mathrm{flow}}
+
\varepsilon_{\mathrm{private}}
+
\varepsilon_{\mathrm{post}}.
\end{aligned}
\]

Taking the infimum cannot increase the value. ∎

## 4. Modal and support approximation

Let \(S\) denote the ideal modal analysis map and \(\widehat S\) its approximation. Let \(P=(P_c,P_p,P_u)\) and \(\widehat P\) be the true and estimated projector triples.

Define

\[
\varepsilon_{\mathrm{modal}}
=
\mathbb E\|
\widehat S(O)-S(O)
\|,
\]

and

\[
\varepsilon_{\mathrm{support}}
=
\mathbb E\left[
\sum_{b\in\{c,p,u\}}
\|(
\widehat P_b-P_b
)S(O)\|
\right].
\]

These errors occur before flow and posterior approximation.

## 5. Theorem 9 — additive representation-risk bound

### Statement

If observed-private identity is exact, so \(\varepsilon_{\mathrm{private}}=0\), then

\[
\boxed{
|
\widehat{\mathcal R}(h)-\mathcal R(h)
|
\leq
L
\left(
\varepsilon_{\mathrm{flow}}
+
\varepsilon_{\mathrm{post}}
+
\varepsilon_{\mathrm{modal}}
+
\varepsilon_{\mathrm{support}}
\right)
}
\]

for the coupled approximation described below.

### Detailed proof

1. Introduce an intermediate representation \(\widetilde Z\) obtained by applying the ideal projectors and ideal transport/posterior to the approximate modal state. By the triangle inequality,

   \[
   W_1(\widehat\mu^U,\mu^U)
   \leq
   W_1(\widehat\mu^U,\widetilde\mu^U)
   +
   W_1(\widetilde\mu^U,\mu^U).
   \]

2. The first term collects flow, posterior, and support-assignment errors. Using Lemma 9.2 and exact private identity,

   \[
   W_1(\widehat\mu^U,\widetilde\mu^U)
   \leq
   \varepsilon_{\mathrm{flow}}
   +
   \varepsilon_{\mathrm{post}}
   +
   \varepsilon_{\mathrm{support}}.
   \]

3. The second term changes only the modal state from \(\widehat S(O)\) to \(S(O)\). Under the adopted coupling and a one-Lipschitz block extraction convention,

   \[
   W_1(\widetilde\mu^U,\mu^U)
   \leq
   \varepsilon_{\mathrm{modal}}.
   \]

   If the transport or decoder has Lipschitz constant greater than one, that constant must multiply this term; the displayed theorem assumes the error terms are measured after their respective maps or have already absorbed those constants.

4. Therefore

   \[
   W_1(\widehat\mu^U,\mu^U)
   \leq
   \varepsilon_{\mathrm{flow}}
   +
   \varepsilon_{\mathrm{post}}
   +
   \varepsilon_{\mathrm{modal}}
   +
   \varepsilon_{\mathrm{support}}.
   \]

5. Apply Lemma 9.1. ∎

## 6. Corollary 9.1 — private leakage adds a separate term

If the implementation does not preserve the private block exactly, then

\[
|
\widehat{\mathcal R}-\mathcal R
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
\right).
\]

The structural identity theorem sets \(\varepsilon_{\mathrm{private}}=0\) in the ideal method.

## 7. Interpretation

The bound is useful because every term maps to a distinct diagnostic:

| Error | Observable diagnostic |
|---|---|
| \(\varepsilon_{\mathrm{flow}}\) | shared endpoint \(W_1/W_2\), paired retrieval |
| \(\varepsilon_{\mathrm{post}}\) | CRPS, NLL, interval coverage, posterior \(W_1\) |
| \(\varepsilon_{\mathrm{modal}}\) | waveform and spectral reconstruction error |
| \(\varepsilon_{\mathrm{support}}\) | private-to-shared intervention leakage |
| \(\varepsilon_{\mathrm{private}}\) | pre/post private-coordinate distance |

The theorem does not justify averaging these diagnostics into a single score. They identify different failure mechanisms.

## 8. Failure boundaries

1. The conditional risk may not be Lipschitz, especially near a discontinuous hard decision boundary.
2. A small marginal Wasserstein distance can coexist with semantic class permutation.
3. The additive metric may assign scientifically inappropriate relative scales to damping, frequency, and residues; a weighted physical metric should be declared.
4. Error terms can interact. The additive bound is conservative and not a causal attribution of observed performance loss.
5. The theorem evaluates a fixed decision rule or regular conditional risk. Re-training a downstream model on each representation introduces optimization and estimation error.

## 9. Experimental implication

An experiment should vary one error source at a time:

- perturb sensor response for support error;
- reduce modal rank for modal error;
- vary flow integration steps for flow error;
- vary diffusion score quality for posterior error;
- deliberately allow private mixing as a negative control.

The observed task degradation should be compared with the corresponding diagnostic. The bound is supported only if the measurement pipeline estimates all declared error terms on independent units.
