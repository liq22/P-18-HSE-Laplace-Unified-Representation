# Theory 9 — Actual conditioning, posterior compression, and model error

## Status and role

Analytical derivation under the assumptions below; the same-stem Notebook checks finite examples. This is an application of conditional KL and the tower property, not a claim of a new general information identity. It does not establish learned HSE sufficiency, LLapDiff accuracy, or real-PHM performance.

## 1. Objects and assumptions

Use the definitions in [Theory 0](00_problem_and_assumptions.md). Let `(Z0, O, a)` be random elements on standard Borel spaces:

- `Z0` is the fixed generation target. In the oracle it may be the known-pole coefficient vector `beta`; in the learned experiment it is the output of a frozen reference encoder. These are different targets.
- `O` contains **all information available to the conditioner encoder** for this acquisition: observed values, observed timestamps/mask and encoder-side acquisition descriptors. It contains neither an unavailable high-rate target nor the hidden state.
- `a` is only the side information actually supplied to and consumed by the conditional model.
- `H = T(O, a)` includes every exposed token, mask, time/band field and auxiliary conditioning feature, not just `tokens`.
- `C = (H, a)` is the complete decoder condition.

Encoder-only descriptors belong in `O` when they are not in `a`. A full-information teacher receives the same `(O,a)`, not an extra reference acquisition. For trained parameters, condition on the fixed training result and evaluate an independent event; otherwise training-data leakage can invalidate this experiment.

Assume deterministic measurable `T`, regular conditional distributions, and densities with respect to a common dominating measure. Let the expected KL terms below be finite. In particular, the fitted density must be positive almost everywhere that the target density is positive. A randomized tokenizer requires an explicit random seed and an extended information set; it is not silently covered here.

Define

\[
p_F(z)=p(z\mid O,a),\quad
p_C(z)=p(z\mid H,a),\quad
q(z)=q_\phi(z\mid H,a).
\]

`p_C` is induced by the **same joint law** as `p_F`. It is not an arbitrary approximation obtained by replacing `J` with `diag(J)` in a Gaussian formula.

## 2. Lemma 9.1 — compression loss is conditional mutual information

\[
\mathcal C(T)
=\mathbb E_{O,a}\operatorname{KL}(p_F\|p_C)
=I(Z_0;O\mid H,a)\geq0.
\]

### Proof

Because `H` is measurable with respect to `(O,a)`,

\[
p(z\mid O,H,a)=p(z\mid O,a).
\]

By the definition of conditional mutual information,

\[
I(Z_0;O\mid H,a)
=\mathbb E\log\frac{p(Z_0\mid O,H,a)}{p(Z_0\mid H,a)}.
\]

Substitute the first identity and integrate over `Z0` conditionally on `(O,a)`. This is exactly the expected KL. Non-negativity follows from Gibbs' inequality. Equality holds precisely when the two conditional laws agree almost surely, equivalently `Z0` and `O` are conditionally independent given `(H,a)`. ∎

## 3. Theorem 9.1 — posterior error separates compression from fitting

\[
\boxed{
\mathbb E_{O,a}\operatorname{KL}(p_F\|q_\phi)
=
I(Z_0;O\mid H,a)
+
\mathbb E_{H,a}\operatorname{KL}(p_C\|q_\phi).
}
\]

### Detailed proof

On the support of `p_F`, insert `p_C` into the logarithm:

\[
\log\frac{p_F(Z_0)}{q_\phi(Z_0)}
=\log\frac{p_F(Z_0)}{p_C(Z_0)}
+\log\frac{p_C(Z_0)}{q_\phi(Z_0)}.
\]

The expectation of the first term is Lemma 9.1. Write

\[
g(z,h,a)=\log\frac{p(z\mid h,a)}{q_\phi(z\mid h,a)}.
\]

The second term satisfies

\[
\begin{aligned}
\mathbb E_{O,a}\mathbb E[g(Z_0,H,a)\mid O,a]
&=\mathbb E[g(Z_0,H,a)]\\
&=\mathbb E_{H,a}\mathbb E[g(Z_0,H,a)\mid H,a]\\
&=\mathbb E_{H,a}\operatorname{KL}(p_C\|q_\phi).
\end{aligned}
\]

The two equalities are conditional expectation, not an interchange between independently generated acquisitions. Add the terms. Finiteness excludes an undefined infinity-minus-infinity manipulation. ∎

## 4. Consequences for the actual HSE interface

For fixed `T` and the same actual side information, any more expressive conditional generator can reduce the fitting term but not the compression term. Jointly improving `T` can change both. More sampler steps are not evidence of information recovered from an insufficient condition.

If `(H,a)` reconstructs the complete sufficient statistic `(b,J)` of Theory 1, then `C(T)=0` in that correctly specified model. This includes the case where `H` retains `b` and `a` exposes the full known acquisition operator and noise covariance. The absence of off-diagonal entries inside `tokens` alone does not imply information loss.

Conversely, diagonal-token collisions with no side information that separates them show a possible failure of sufficiency. The cross-posterior KL between two colliding cases measures their separation; it is **not** the population conditional mutual information. To calculate the latter one must specify a distribution over acquisition designs and observations.

Under uncertain design, `p(beta | b, diag(J), a)` may be a mixture of Gaussian posteriors. The Gaussian produced by substituting `diag(J)` in the precision is a candidate `q`, not automatically `p_C`. Calling its entire error “compression loss” confounds compression and fitting.

## 5. Finite witness and controls

Run `notebooks/09_conditioning_information_loss.ipynb`.

The first example has balanced binary `Z0`, a 90%-accurate binary observation, constant `H`, and fitted probability `q(Z0=1)=0.7`. It checks

\[
0.4552409007
=0.3680642072+0.0871766936
\]

in nats. It then supplies the observation through actual side information: compression becomes zero, without pretending that model fitting is also zero. A separate four-observation/two-token example checks the tower property when `H` is neither constant nor injective.

## 6. Admission and boundaries

The general equality is analytical support, not a new contribution. A method-specific contribution requires a token construction that reduces the measured gap at the same information access and declared token/compute budget. Gaussian plug-in error, Monte Carlo estimates and learned denoising loss must be labeled separately.

This result does not turn a denoising loss into an endpoint KL bound; a finite reverse sampler needs its own analysis. It does not guarantee finite-dimensional sufficiency for unknown poles, non-Gaussian noise or arbitrary VAE latents.

## References

- Oko, Lin, Cai and Mei (2025), *A Statistical Theory of Contrastive Pre-training and Multimodal Generative AI*, arXiv:2501.04641v2, Definition 1 and Proposition 3. Approximate sufficiency and its connection to conditional diffusion are prior work.
- Alsing and Wandelt (2018), *Generalized massive optimal data compression*, arXiv:1712.00012. Fisher-preserving score compression must not be equated with global posterior sufficiency.
- The complete-statistic factorization is derived in Theory 1; the denoising projection is derived separately in Theory 10.
