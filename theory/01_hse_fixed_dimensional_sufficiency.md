# Theory 1 — Full acquisition sufficiency and actual token limits

## Status

Exact likelihood factorization for known linear-Gaussian acquisition. The actual diagonal-token witness below is a counterexample to unconditional token sufficiency, not a refutation of that factorization. Unknown poles are outside this theorem.

## 1. Fixed-dimensional statistics

Write `theta` for the fixed-pole coefficient vector (`beta` in Theory 0). Define

\[
b=A^TR^{-1}x\in\mathbb R^m,\qquad J=A^TR^{-1}A\in\mathbb R^{m\times m}.
\]

The observation length can vary without changing these dimensions. The full symmetric matrix requires `m(m+1)/2` scalars, so fixed dimension in observation length does not imply an arbitrary fixed token budget can preserve it.

## 2. Lemma 1.1 — Gaussian likelihood factorization

For known fixed `A,R`,

\[
p(x\mid\theta,A,R)=h_{A,R}(x)
\exp\{\theta^Tb-\tfrac12\theta^TJ\theta\},
\]

where `h` does not depend on `theta`.

### Detailed proof

Expand the Gaussian quadratic form:

\[
\begin{aligned}
(x-A\theta)^TR^{-1}(x-A\theta)
=x^TR^{-1}x-2\theta^TA^TR^{-1}x+\theta^TA^TR^{-1}A\theta.
\end{aligned}
\]

The normalization and the first term form `h`; the remaining terms have the displayed natural parameters. ∎

## 3. Theorem 1.1 — complete-statistic sufficiency

Conditionally on known `A,R`, `(b,J)` is sufficient for `theta`. Indeed, `J` is fixed under a fixed design, so `b` alone is sufficient when the decoder knows that design.

### Proof

The Fisher–Neyman factorization follows from Lemma 1.1. Equivalently, for a declared prior with a proper posterior, Bayes' rule gives

\[
p(d\theta\mid x,A,R)\propto p(d\theta\mid A,R)
\exp\{\theta^Tb-\tfrac12\theta^TJ\theta\}.
\]

With a common design-independent prior, retaining `(b,J)` also gives a portable posterior description across known acquisition designs. If the prior depends on design, the relevant prior information must also be supplied. A Gaussian prior is not required for sufficiency; it is required for the Gaussian posterior in Theory 2. ∎

## 4. Lemma 1.2 — equal complete statistics

For a fixed design, two observations sharing `(b,J)` have a likelihood ratio independent of `theta`: their exponential factors cancel, leaving `h(x)/h(x')`. This is the original dense-information Notebook witness and is retained.

## 5. Proposition 1.2 — what the actual condition must preserve

Let `C=(H,a)` be the **consumed** condition from Theory 0. If measurable functions of `C` recover `(b,J)` and the relevant prior, the posterior above is a measurable function of `C`; hence no posterior information is lost.

This holds, for example, when `H` retains `b` and `a=(A,R)`. It does not require off-diagonal entries to appear inside the token array. Conversely, shape `[K,D]`, a mask, and diagonal information alone do not establish this recoverability.

## 6. Counterexample — actual diagonal-token collision

Choose

\[
J_+=\begin{bmatrix}1&0.8\\0.8&1\end{bmatrix},\quad
J_-=\begin{bmatrix}1&-0.8\\-0.8&1\end{bmatrix},\quad
b=\begin{bmatrix}1\\0.4\end{bmatrix}.
\]

Both matrices are positive definite. They are realizable acquisition statistics: take `R=I`, `A_pm=chol(J_pm)^T`, and `x_pm=(A_pm^T)^{-1}b`. Then the existing `gaussian_information_statistics` returns the specified pair.

Give both cases identical time/band/reliability metadata and pass their statistics through the **existing** `information_tokens_from_diagonal`. All exposed token fields and masks coincide up to roundoff. This is a collision only if the actual side information does not reveal the different operators.

Under prior `N(0,I)`, the full posterior is

\[
\mu_\pm=(I+J_\pm)^{-1}b,\qquad \Sigma_\pm=(I+J_\pm)^{-1}.
\]

Solving gives

\[
\mu_+=(0.5,0)^T,\qquad
\mu_-=(0.6904761905,0.4761904762)^T.
\]

Their mean distance is approximately `0.512873`, and the directed Gaussian KL from `+` to `-` is `0.5714285714` nats. This KL is a two-posterior separation, **not** the compression mutual information of Theory 9.

This is not merely a single zero-probability collision: if both acquisition designs have positive probability, the induced `b` laws have full support. Their differing posterior covariance and continuously differing means cannot be selected from identical diagonal conditions on the common support. Once `a=(A,R)` is supplied, the conditions differ and the collision argument no longer applies.

## 7. Approximation and deployment boundary

A per-mode cosine/sine `2x2` block preserves within-mode coupling only. It is not sufficient when cross-mode blocks matter. No claim that a small block solves this problem is made before the paired compression experiment.

Replacing `J` with a diagonal or block approximation in a Gaussian formula defines a plug-in model. Under uncertain design this model need not equal the true induced conditional `p(theta | H,a)`. Separate approximation error from information loss.

The oracle currently computes its Gaussian posterior using full statistics, not by decoding its diagonal tokens. The learned HSE has not been proved to preserve these statistics. Masked-away score values, encoder-only metadata, unknown poles and misspecified covariance need their own stated treatment.

## 8. Executable witness and use in the paper

The same-stem Notebook retains the dense-`J` likelihood-ratio check, then exercises the real diagonal tokenizer, its hidden-coupling counterexample, and the full-side-information positive control. Tests protect these actual code paths.

This result is an analytic baseline and implementation boundary. A useful coupling token and its same-budget learned advantage remain candidate work, not an admitted contribution.
