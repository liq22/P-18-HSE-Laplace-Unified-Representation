# Theory 10 — HSE compression and optimal conditional denoising

## Status and role

A conditional-expectation projection derivation and finite quadrature witness. The underlying projection and score identities are established theory. The purpose is to identify the target actually learned by an HSE-conditioned LLapDiff, not to claim a new generic diffusion theorem.

## 1. Assumptions and notation

Use `(Z0,O,a,H)` from Theory 9. At a fixed diffusion time `tau`,

\[
Z_\tau=\alpha_\tau Z_0+\sigma_\tau\varepsilon,
\qquad \varepsilon\sim\mathcal N(0,I),
\qquad \varepsilon\perp(Z_0,O,a).
\]

The schedule is identical for the full and compressed conditions. The denoising target `U_tau` is square-integrable. It may be epsilon, `Z0`, or v with the precise definition below. This covers unrestricted Bayes regressors; a finite Laplace denoiser family need not contain them.

Define the nested information sets

\[
\mathcal F_\tau=\sigma(Z_\tau,O,a),\qquad
\mathcal G_\tau=\sigma(Z_\tau,H,a)\subseteq\mathcal F_\tau.
\]

Here `sigma(...)` denotes a generated sigma-algebra; `sigma_tau` is the noise standard deviation. Let

\[
f_F=\mathbb E[U_\tau\mid\mathcal F_\tau],\qquad
f_C=\mathbb E[U_\tau\mid\mathcal G_\tau].
\]

## 2. Lemma 10.1 — orthogonality of the full residual

For any square-integrable, `F_tau`-measurable vector `V`,

\[
\mathbb E\langle U_\tau-f_F,V\rangle=0.
\]

### Proof

Condition the inner product on `F_tau`. The vector `V` can be taken outside the conditional expectation, while `E[U_tau-f_F | F_tau]=0`. Integrate the resulting zero. ∎

## 3. Theorem 10.1 — exact Bayes denoising-risk gap

Let

\[
\mathcal R_F^*=\mathbb E\|U_\tau-f_F\|^2,\qquad
\mathcal R_C^*=\mathbb E\|U_\tau-f_C\|^2.
\]

Then

\[
\boxed{
\mathcal R_C^*(\tau)-\mathcal R_F^*(\tau)
=\mathbb E\|f_F-f_C\|^2\geq0.
}
\]

### Detailed proof

Write

\[
U_\tau-f_C=(U_\tau-f_F)+(f_F-f_C).
\]

Expand the squared norm and take expectations. The cross term vanishes by Lemma 10.1 with `V=f_F-f_C`, because both conditional means are `F_tau`-measurable. The remaining two terms are `R_F*` and the displayed squared difference. Rearrange. ∎

For any actual `G_tau`-measurable predictor `g`, repeat the same argument conditional on `G_tau` to obtain

\[
\boxed{
\mathbb E\|U_\tau-g\|^2
=\mathcal R_F^*
+\mathbb E\|f_F-f_C\|^2
+\mathbb E\|f_C-g\|^2.
}
\]

Thus irreducible full-observation error, conditioning loss, and approximation/optimization error are different quantities. A restricted modal predictor adds the last error even if the token is sufficient.

Integrating against the **same** non-negative time weight preserves the equality when the integral is finite. Different schedules or loss weights cannot be compared using this identity without conversion.

## 4. Conditional score and parameterization

For `sigma_tau>0`, assume differentiation can pass under the conditional Gaussian integral. Its derivative is

\[
\nabla_z p_\tau(z\mid C)
=\int -\frac{z-\alpha_\tau z_0}{\sigma_\tau^2}
\varphi_{\sigma_\tau}(z-\alpha_\tau z_0)p(dz_0\mid C).
\]

Divide by the positive density to obtain

\[
\boxed{
\nabla_z\log p_\tau(z\mid C)
=-\frac1{\sigma_\tau}\mathbb E[\varepsilon\mid Z_\tau=z,C].
}
\]

The compressed network learns the compressed conditional score, not the full-observation score automatically.

Let `m_F=E[Z0 | F_tau]`, `m_C=E[Z0 | G_tau]`, and `Delta=m_F-m_C`. At a fixed `z`,

\[
f_F^\varepsilon-f_C^\varepsilon
=-\frac{\alpha_\tau}{\sigma_\tau}\Delta.
\]

If `alpha_tau^2+sigma_tau^2=1` and

\[
v=\alpha_\tau\varepsilon-\sigma_\tau Z_0,
\]

then

\[
f_F^v-f_C^v=-\frac1{\sigma_\tau}\Delta.
\]

Therefore the three Bayes risk gaps satisfy

\[
\Delta R_{\varepsilon}
=\frac{\alpha_\tau^2}{\sigma_\tau^2}\mathbb E\|\Delta\|^2,
\quad
\Delta R_v
=\frac1{\sigma_\tau^2}\mathbb E\|\Delta\|^2,
\quad
\Delta R_{x_0}=\mathbb E\|\Delta\|^2.
\]

These conversions do not apply at `sigma_tau=0`. At `alpha_tau=0`, the epsilon gap is zero even if `H` discarded target information. One noise level alone therefore cannot certify sufficiency.

## 5. Corollary — bounded target connects Theory 9 to denoising

This paragraph **additionally** assumes `||Z0|| <= B` almost surely. It is not applied to the unbounded Gaussian coefficient oracle.

Gaussian perturbation is a common channel independent of `O` given `(Z0,H,a)`. The conditional chain rule gives

\[
I(Z_0;O\mid H,a)
=I(Z_\tau;O\mid H,a)
+I(Z_0;O\mid Z_\tau,H,a).
\]

For each noisy condition, the difference of two conditional target means has norm at most `2B TV(p_F^tau,p_C^tau)`. Pinsker's inequality, with `TV` defined as half the L1 distance, gives

\[
\mathbb E\|m_F-m_C\|^2
\leq2B^2 I(Z_0;O\mid Z_\tau,H,a)
\leq2B^2\mathcal C(T).
\]

Combine this with the parameterization identities. The factors involving `1/sigma_tau` need an integrability condition before any time-integrated bound. This is the same kind of sufficiency-to-denoising connection studied by Oko et al., not a new general principle.

## 6. Finite witness

Run `notebooks/10_conditioning_denoising_projection.ipynb`.

It uses balanced `Z0 in {-1,1}`, a binary observation that is correct with probability 0.9, constant compressed `H`, and `alpha=0.8, sigma=0.6`. Unlike a teacher that observes `Z0` exactly, this gives a nonzero full Bayes risk. Gaussian quadrature checks:

1. full and compressed risk and their projection difference;
2. vanishing cross term;
3. epsilon/x0/v scaling under the same schedule;
4. the score identity;
5. quadrature convergence;
6. zero epsilon gap at `alpha=0` despite a lossy condition.

No neural denoiser is trained.

## 7. Boundaries and paper admission

A passing finite witness is not a general proof or a novelty decision. A method contribution still requires an actual token improvement evaluated with the same raw observation, decoder side information, LLapDiff architecture, target VAE and sampler. A high-rate target may be supervision, but cannot secretly enter only the full-condition teacher.

The result does not claim that a sample-residual penalty preserves the posterior, that denoising MSE alone guarantees calibration, or that this identity bounds discretized reverse-sampling error.

## References

- Oko, Lin, Cai and Mei (2025), arXiv:2501.04641v2, Proposition 3 and Appendix D.5: encoder sufficiency bounds conditional denoising error under a bounded-target assumption.
- Song et al. (2021), *Score-Based Generative Modeling through Stochastic Differential Equations*, arXiv:2011.13456: score-based diffusion background.
- Theory 9 supplies the separate posterior compression/fitting decomposition.
