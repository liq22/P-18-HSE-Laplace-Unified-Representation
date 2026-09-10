# Method: acquisition-calibrated conditioning

## 1. Targets and observations

For one local event, use a fixed physical dictionary `Phi_Lambda(t)` and coefficient vector beta. The analytic measurement is

$$x_d=A_d\beta+\epsilon_d,\quad\epsilon_d\sim N(0,R_d),\quad
\beta\sim N(0,S_0).$$

Timestamps, sensor response, mask and declared noise determine A and R. A mask is applied to rows, not replaced by fabricated observations. The learned target will instead be `Z0=E_ref(X_ref)` from a frozen source-trained reference encoder. Physical coefficients, this latent trajectory, and the denoiser's predicted poles are different objects.

The actual generator condition is `C=(H,a_consumed)`. Audit all tokens, time/band features and masks. Unknown descriptor fields are not silently available to a teacher. A high-quality paired reference can provide supervision but is not an extra observation given only to one conditional model.

## 2. Sufficient statistics and the compression problem

The Gaussian sufficient quantities are `b=A^T R^-1 x` and `J=A^T R^-1 A`. Their dimensions are independent of observation length, but dense J costs quadratic storage. Its off-diagonal terms measure overlap of the observed basis columns. For example,

$$J_{ij}=\sum_{n\in\mathcal I_{obs}}\phi_i(t_n)\phi_j(t_n)/\sigma_n^2.$$

Finite windows, nearby modes and missing intervals prevent general orthogonality. A nominal frequency below Nyquist does not imply zero cross-mode coupling. Our sampled study evaluates these columns directly; it does not claim an ideal anti-alias null for a finite-window decaying sinusoid.

## 3. Directly decoded equal-storage header

For two modes, there are four coefficients. The sparse header has 11 stored scalars:

$$h_{\rm precision}=[b_1,\ldots,b_4,J_{11},\ldots,J_{44},J_{e_1},J_{e_2},s].$$

The layout s selects one of three disjoint pairings. The decoder reconstructs a block-diagonal information matrix from the header alone. Every compared sparse method transmits its layout code. The diagonal method pads the coupling slots; the full upper-information baseline transmits 15 scalars. These counts are physical storage layouts, not minimal information-theoretic bitrates.

Compare fixed within-mode pairs, maximum coupling magnitude, and a design-only posterior-risk oracle. All inspect the same acquisition metadata at the encoder; their computational costs differ. The risk oracle is not justified as a deployable addition if it chooses the same pattern as a cheaper rule.

## 4. Error-aware selection and assessment

With full precision Lambda and approximate precision Q, define normalized error `E=Lambda^-1/2(Q-Lambda)Lambda^-1/2`. Theory 12 derives the exact Gaussian KL including natural-parameter error and a computable SPD bound. The bound is an assessment of a particular approximate decoder, not automatically true compression mutual information.

For a zero-mean Gaussian source prior, Theory 13 integrates the mean-dependent term over the prior-predictive observation distribution. This enables a layout score using design information only, without test labels or hidden event coefficients. Its optimality is restricted to the three predeclared layouts, the stated prior and a plug-in posterior.

## 5. Strong moment-matching control

A precision header can induce poor uncertainty after inversion even when it retains large interactions. Compare a second 11-scalar header:

$$h_{\rm moment}=[\mu_1,\ldots,\mu_4,\Sigma_{11},\ldots,\Sigma_{44},\Sigma_{e_1},\Sigma_{e_2},s].$$

The analytic encoder calculates full posterior moments before compressing them. The decoder receives only the header. The approximate posterior matches the full mean and block marginal covariance. For a fixed partition this minimizes forward Gaussian KL and preserves all univariate marginals; cross-block dependence can still be lost. Encoder-side inference cost must be reported. This is a mandatory analytic control, not a learned HSE success.

## 6. Proposed learned conditioner intervention

Preserve the original HSE patch points P, token count K and dimension D. Reserve a declared condition budget inside, rather than append an uncounted auxiliary stream. All baseline arms receive the same measured acquisition descriptors. Compare a precision-style coupling feature with a source-trained posterior-moment prediction feature. Any moment teacher must use the same observation O and declared a, or be explicitly labeled privileged supervision with a matched privileged baseline.

Train each conditioner with the same LLapDiff denoiser architecture, identical target VAE weights and identical diffusion schedule. Keep v-prediction as the official default unless all arms use a declared alternative. The primary loss is the same native conditional denoising objective. A teacher-posterior distillation term is optional only after its calibrated teacher and target are specified; do not add an observation-residual penalty and assume it leaves the target posterior unchanged.

A schematic objective is

$$\mathcal L=E\|v-v_\theta(z_\tau,\tau,H_\psi(O,a),a)\|^2
+\lambda E\,D(p_{teacher}(Z_0|O,a),q_\psi(Z_0|H,a)).$$

The second term is not currently implemented for real data. Test lambda=0 and matched supervision. The teacher may be exact only in the known-pole oracle. No theorem transfers coefficient sufficiency to arbitrary learned VAE coordinates.

## 7. Falsification and complexity

Full actual A,R is a required null control; it can make an additional information header redundant. Fixed-width output must include all side streams in the budget. Missing or invalid input must fail explicitly. Evaluate 1/2/3-channel shape and gradients before multichannel claims. Different channels can be stacked only with their actual noise covariance; two resampled copies of one noisy recording are not independent observations.

The current implementation covers the analytic headers and sampled Gaussian study. The learned HSE intervention and official-model comparison are specified but not implemented here. Flow Matching remains future work until a validated posterior sampler has a measured latency limitation.
