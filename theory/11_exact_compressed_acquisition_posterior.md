# Theory 11 — Exact posterior after discarding acquisition coupling

## Status and purpose

This is a finite-design specialization of Bayes' rule and the compression identity in Theory 9. Its purpose is to compute the **true** compressed conditional in Task B. It is not a new general mixture-inference theorem or an admitted learned-method contribution. The same-stem Notebook checks the formula, its independent observation-space calculation and its failure controls.

## 1. Assumptions, targets and actual access

**B1 (fixed dictionary).** Two declared damped modes give four coefficients,

$$
\beta=(c_1,b_1,c_2,b_2)^T,\qquad
s(t)=\sum_{r=1}^2 e^{-\rho_r t}[c_r\cos(\omega_r t)+b_r\sin(\omega_r t)].
$$

The poles are fixed, not inferred. Time is in seconds, damping in inverse seconds and angular frequency in rad/s. The experiment below uses **linear measurements of coefficients**, not a simulation of anti-alias filters or a sampled-waveform HSE. A learned reference-VAE target is a different object.

**B2 (declared prior).** A coefficient vector has a known finite Gaussian-mixture prior

$$
p(\beta)=\sum_{k=1}^{L}w_k\,\mathcal N(\beta;\mu_k,S_k),\quad
w_k>0,\quad \sum_kw_k=1,\quad S_k\succ0.
$$

A single component is the Gaussian control. The prior is provided by the simulator, not estimated on evaluation data.

**B3 (finite acquisition population).** Independently of beta, a design index `D` has probability `pi_d>0`. Under design d,

$$x=A_d\beta+\epsilon,\qquad \epsilon\sim\mathcal N(0,I),\qquad A_d\in\mathbb R^{4\times4}\text{ invertible}.$$

Define `J_d=A_d^T A_d` and `b=A_d^T x`. Each method's encoder sees the same `(x,A_d)`; the condition retains b and a declared summary `s_r(J_d)`. The decoder knows the **population** of candidate designs and prior probabilities, not the hidden realized design.

**B4 (two explicit side-input regimes).** Coarse side input does not distinguish the unresolved designs. Full side input gives `A_d,R_d=I` equally to all arms; the decoder actually reconstructs J from it. We do not manufacture a token gain by hiding a descriptor only from a baseline.

**B5 (nested summaries).** `s_diag` keeps four diagonal entries; `s_block` keeps both within-mode symmetric 2x2 blocks; `s_full` keeps the full symmetric J. Together with b these contain 8, 10 and 14 unique scalars, respectively. They are **not matched storage budgets**. All other metadata are identical in this controlled family.

## 2. Lemma 11.1 — likelihood of the retained score

Conditionally on beta and d,

$$\boxed{b\mid\beta,D=d\sim\mathcal N(J_d\beta,J_d).}$$

**Proof.** Substituting x gives `b=J_d beta + A_d^T epsilon`. The transformed zero-mean Gaussian noise has covariance `A_d^T A_d=J_d`. Invertibility makes this covariance positive definite. Conditional on prior component k, integrate beta to obtain

$$p(b\mid d,k)=\mathcal N(b;J_d\mu_k,J_dS_kJ_d+J_d).$$

This Gaussian convolution keeps both signal covariance and score-noise covariance. ∎

## 3. Lemma 11.2 — component posterior

Let

$$V_{dk}=(S_k^{-1}+J_d)^{-1},\qquad m_{dk}=V_{dk}(S_k^{-1}\mu_k+b).$$

Then `p(beta | b,d,k)=N(m_dk,V_dk)`.

**Proof.** The score likelihood exponent is

$$-\tfrac12(b-J_d\beta)^TJ_d^{-1}(b-J_d\beta)
=-\tfrac12b^TJ_d^{-1}b+\beta^Tb-\tfrac12\beta^TJ_d\beta.$$

Add the prior exponent `-1/2(beta-mu_k)^T S_k^{-1}(beta-mu_k)`. Collect the precision and natural parameter and complete the square. Positive definiteness ensures a finite normalized posterior. ∎

## 4. Theorem 11.1 — actual compressed posterior

For observed summary s, define the compatible-design set

$$\mathcal D_r(s)=\{d:s_r(J_d)=s\}.$$

Then

$$\boxed{
p(\beta\mid b,s)=\sum_{d\in\mathcal D_r(s)}\sum_k\omega_{dk}(b,s)\,
\mathcal N(\beta;m_{dk},V_{dk}),
}$$

where

$$\omega_{dk}(b,s)=
\frac{\pi_dw_k\mathcal N(b;J_d\mu_k,J_dS_kJ_d+J_d)}
{\sum_{e\in\mathcal D_r(s)}\sum_j\pi_ew_j\mathcal N(b;J_e\mu_j,J_eS_jJ_e+J_e)}.$$

**Detailed proof.** The summary is a deterministic function of design. Thus the joint density of `(beta,b,d,k,s)` is the product of the design probability, component probability, coefficient density, score likelihood, and the indicator that d belongs to `D_r(s)`. Integrating beta gives Lemma 11.1's marginal likelihood times `pi_d w_k`. Normalizing these positive terms gives the displayed weights. Condition first on `(d,k)`, use Lemma 11.2, and sum over the now conditional design/component probabilities. This law uses b and the retained summary only. ∎

**Jacobian check.** For invertible A, `x=A_d^{-T}b`, and

$$p(b\mid d,k)=p(x=A_d^{-T}b\mid d,k)/|\det A_d|.$$

The determinant changes the **design** weights and cannot generally be omitted. Evaluating the hidden raw x under alternative designs is not the decoder's score likelihood. The test suite checks this formula through observation-space covariance independently of the score-space implementation. The four-sign sweep family below has equal determinants; that check alone cannot detect an omitted Jacobian. A separate two-design test fixes the diagonal at 1.5 and varies the first within-mode off-diagonal entry from 0.1 to 1.3. The resulting determinants differ; omitting the determinant then changes the posterior design weights. This test is a boundary witness, not an additional sweep or a learned-model result.

## 5. Corollary — refinement reduces compression loss, not every sample error

For the common prior and actual information access, define

$$\mathcal C_r=\mathbb E\log\frac{p(\beta\mid b,D)}{p(\beta\mid b,s_r(J_D))}
=I(\beta;D\mid b,s_r(J_D)).$$

The complete score/design pair is equivalent to the full observation/design pair for this target. Because `s_diag` is a function of `s_block`, the conditional chain rule gives

$$\boxed{
\mathcal C_{\rm diag}=\mathcal C_{\rm block}
+I(\beta;s_{\rm block}(J_D)\mid b,s_{\rm diag}(J_D)).
}$$

Consequently `C_diag >= C_block >= C_full=0`. This is a population statement. Individual log ratios and their finite Monte Carlo estimates may be negative; the implementation does not clip them.

If actual side input reveals A, all conditions reconstruct J, and all three compression losses are zero. More summaries then have no Bayes-information advantage, although finite neural capacity could still matter and is not studied here.

## 6. A family that can falsify block sufficiency

Use four equally likely designs indexed by `u,v in {-1,1}`:

$$J_{uv}=1.5I+0.6uW+cvX,$$

where W has ones at `(1,2),(2,1),(3,4),(4,3)`, and X at `(1,3),(3,1),(2,4),(4,2)`. W and X commute and have eigenvalues plus/minus one. Hence eigenvalues of J are `1.5 +/- 0.6 +/- c`; for `c in {0,0.45,0.8}` they are strictly positive. Set `A=chol(J)^T` to obtain realizable coefficient measurements.

The diagonal summary hides both signs. The block summary retains u but not v. When c=0, every unresolved v has the same J, so blocks are sufficient. When c>0, unresolved designs have different J and different full posterior laws. The prior density is positive everywhere, and their posterior likelihood ratio contains a nonconstant quadratic form. Therefore they are not conditionally independent of beta given the retained condition, and the block compression loss is positive.

This does **not** prove compression increases monotonically in c. The retained b also carries information about the unknown design. Changing c changes both posterior separation and design inferability. The sweep must be reported in full.

## 7. Exact conditional versus a plug-in model

A plug-in model replaces J by its retained matrix in the usual posterior formula. It is generally **not** the law in Theorem 11.1. In particular, a Gaussian prior can yield a mixture after acquisition identity is discarded.

For any plug-in density q using the same compressed condition, Theory 9 gives

$$\mathbb E\log(p_F/q)=\mathcal C_r+\mathbb E\log(p_r/q).$$

The second term is model mismatch; it must not be attributed to token information loss. The experiment evaluates all three terms using the same true beta and observations, making the arithmetic decomposition exact per event while non-negativity remains a population property.

## 8. Implementation assumptions and falsifying controls

The current implementation uses a **uniform** design prior. The general formula above allows arbitrary positive `pi_d`; nonuniform design priors are not silently accepted by this implementation. A compatible set must contain distinct integer indices. Duplicating an index reweights its probability; converting a fractional index to an integer changes the selected design. Both are rejected.

Prior weights, means and covariances must describe the same number of components, with normalized positive weights and symmetric positive-definite covariances. Truncating unequal arrays with `zip` would change the declared prior and invalidate the calculated conditional. No renormalization or covariance repair is performed.

The 8/10/14 figures count entries in general matrix-summary layouts. In the particular finite sign family, many entries are fixed or repeated. These counts are not measured bitrates, information entropy, or proof of an equal-budget neural comparison.

## 9. Numerical protocol and contribution boundary

The script preassigns train/validation/test event identities; no fitting or tuning uses any split. Evaluation uses 2,048 events per simulator seed (0,1,2), with four independently noisy acquisition views per event. Metrics are averaged within event before bootstrap resampling. The three seeds are simulation replicates, not training seeds. The two priors and three c values reuse corresponding event/random-noise draws to enable paired comparisons.

Posterior component formulas are exact. Expected KL, coverage and denoising distances are Monte Carlo estimates, with event-level uncertainty. Coverage is central **marginal** coverage; joint density log scores and the denoising distance are also reported. These oracle mixtures have known population parameters, not learned generalization guarantees.

A finite mixture represents the true posterior in this particular model. Thus this experiment establishes no population advantage for Diffusion. It also does not identify a same-budget learned HSE improvement, simulate physical resampling, or validate noisy-reference latent targets.

## References

The derivation uses the Gaussian factorization of Theory 1 and conditional KL decomposition of Theory 9. Approximate sufficiency and conditional denoising are prior theory (Oko et al., arXiv:2501.04641); score-based Fisher compression is prior work (Alsing and Wandelt, arXiv:1712.00012). This file makes the previously missing finite-design conditional computable rather than claiming either principle as novel.
