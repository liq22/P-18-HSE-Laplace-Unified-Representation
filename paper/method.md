## 3. Method

### 3.1 Overview

The proposed construction first fixes a source-supported joint target, then learns its conditional distribution, and finally integrates that distribution into diagnosis. Figure 2 distinguishes inherited HSE and temporal-denoising components from the target qualification and support restriction introduced in this construction. A source reference supplies training targets only. At deployment, the measured record follows two paths: a fixed observed-evidence path and a compressed condition for the missing-state generator. The same observed-state draw conditions every reverse step of a missing-state draw. Generated samples enter a fixed source-trained diagnostic readout; unestimated coordinates do not become zero-valued physical recoveries.

![**Source-qualified temporal posterior inference.** The upper strip defines source-only preparation. The lower flow separates measured evidence, observed-state uncertainty and the eligible missing-state sampler. Solid neutral blocks denote inherited components; colored blocks mark the proposed target selection and restricted process. Dashed connections supply training/reference information or the frozen target definition, not extra deployment measurements. The inset expands the reverse loop into velocity prediction, clean/noise conversion and an eligible-only update. The intervention labels correspond to Eq. (5); posterior, diagnosis and cost are evaluated separately.](figures/overview.pdf){width=100%}

### 3.2 Source-qualified reference targets and observation conditioning

**Operational source construction.** Split original recordings before forming views. For each source recording with a reference measurement, use a source-frozen encoder $E_{\rm ref}$ and a declared acquisition transformation $\mathcal D_a$ to construct

$$
z_i^{\rm ref}=E_{\rm ref}(x_i^{\rm ref}),\quad
C_{F,i}^{(a)}=\operatorname{record}(\mathcal D_a x_i^{\rm ref},a),\quad
(z_{o,i},w_{0,i})=(P_{o,e}z_i^{\rm ref},B_e^\top z_i^{\rm ref}). \tag{6}
$$

$P_{o,e}$ projects onto $\mathcal O_e$; columns of $B_e$ form an orthonormal basis of a selected $\mathcal I_e$, and $G_e=B_eB_e^\top$. For trajectories, these maps act at each query time. They are fixed during sampling. The source-calibrated observation relation must justify this geometric assignment. If only reference-feature correspondence is established, Eq. (6) defines a reference-feature target, not a noise-free mechanical state. Finite bandwidth, filtering and reference noise are part of that target definition.

The paired tuple $(C_F,z_o,w_0)$ makes the required joint reference law observable on the source design. It does not guarantee accurate estimation or validity on a new machine. Only blocks jointly observed in a source reference design, or identified under a stated alternative observation model, are admitted together. A union of separately available blocks is not a substitute. Deployment descriptors determine which source-defined target applies; target labels never select it. A different complete condition requires its corresponding identification argument. Source-to-target conditional transport and overlap remain assumptions evaluated by held-out datasets, not consequences of pairing.

**HSE statistical condition.** A shared source-trained trunk produces $R$; the same affine head $h(R)$ parameterizes a mean $\mu$ and covariance $\Sigma=LL^\top+\lambda I$. For a predeclared reference functional $U$, its auxiliary loss is

$$
\mathcal L_{\rm anc}=\tfrac12\mathbb E\!\left[
 (U-\mu)^\top\Sigma^{-1}(U-\mu)+\log\det\Sigma\right]. \tag{7}
$$

The loss updates the trunk consumed by all ordinary-code controls. Source validation selects one checkpoint, which is then frozen. Proper moment scoring motivates the anchor, while optimization and shift remain empirical issues [@gneiting2007proper; @seitzer2022pitfalls]. The three same-width interfaces are

$$
H_R=R,\qquad H_A=[h(R),R_{\rm tail}],\qquad
H_M=\Phi(H_A),\qquad C_T=(H_c,a,\text{roles},\mathcal I_e). \tag{8}
$$

$\Phi$ converts raw covariance coordinates to the declared positive-definite factor. Extra metadata and factorization cost are included in the budget. The fixed observed-evidence and diagnostic paths receive the same $R$ across conditioner arms; only the generative interface changes in the primary conditioner contrast. Moment coordinates do not establish a complete non-Gaussian posterior.

### 3.3 Eligible-only diffusion and temporal prediction

Let $n_e$ be the number of admitted scalar targets over the query window. We fit a denoiser to Eq. (3) on those targets, sampling source groups first and views within a group. Noise levels follow a common declared distribution, and the primary objective uses unweighted velocity error:

$$
\widehat v_\theta=B_e^\top D_{\theta,\ell}
 (B_ew_k,k,C_T,z_o,\boldsymbol t),\qquad
\mathcal L_{\rm diff}=\mathbb E\!\left[
 n_e^{-1}\|\widehat v_\theta-v_k\|^2\right]. \tag{9}
$$

The same source $z_o$ conditions target generation during training. Complementary coordinates carry no clean target or loss. Empty eligibility invokes no missing-state training or sampler. Where reference targets themselves are missing, the fitted target is further restricted to a jointly available, identified block; numerical padding does not provide supervision.

For $\ell=1$, the denoiser uses LLapDiff's modal analysis/synthesis with positive damping. Its temporal basis has the form

$$
m_\theta(t)=\sum_{j=1}^{J}e^{-\rho_j\widetilde t}
 \{b_j\cos(\omega_j\widetilde t)+c_j\sin(\omega_j\widetilde t)\},
\qquad \rho_j>0,\quad\widetilde t=t-t_1\geq0. \tag{10}
$$

This is an inherited temporal bias [@you2026llapdiff], not Laplace-distributed perturbation. The modal branch is embedded in the denoiser, whose output in Eq. (9) is velocity. Therefore a decaying basis does not prove that the clean generated sample, the nonlinear denoiser or the reverse process is globally stable. The ordinary temporal comparator replaces this branch under the same condition, target, prediction type and selection budget. Physical modal interpretation additionally requires the calibrated reference; learned poles alone do not supply it.

Velocity predictions determine clean and noise estimates through the standard conversion [@salimans2022distillation]:

$$
\widehat w_0=\alpha_kw_k-\sigma_k\widehat v_\theta,
\qquad \widehat\epsilon=\sigma_kw_k+\alpha_k\widehat v_\theta. \tag{11}
$$

For a shared forward sample, $\|\widehat v-v\|^2=\|\widehat w_0-w_0\|^2/\sigma_k^2$. Thus, plain clean-target MSE is not the same objective. Any clean-target variant retains the corresponding weight or is reported as a separate loss intervention.

### 3.4 Reverse update, coherent uncertainty and diagnosis

We use a deterministic DDIM update, with unit guidance and no thresholding modification of the predicted target [@salimans2022distillation]. For successive reverse noise levels $s<k$,

$$
w_s=\alpha_s\widehat w_0+\sigma_s\widehat\epsilon,
\qquad
z_s^m=B_ew_s
 =G_e\!\left(\alpha_sB_e\widehat w_0+\sigma_sB_e\widehat\epsilon\right). \tag{12}
$$

Initialize in the admitted basis with $w_K\sim\mathcal N(0,I)$, using the same near-zero terminal signal level in all compared arms; finite terminal mismatch and finite-step sampling error are measured approximations. The endpoint uses $\alpha_0=1,\sigma_0=0$. Every state, denoiser output and update is mapped through the same $B_e$, so $(I-G_e)z_s^m=0$ at every step. Since $P_{o,e}B_e=0$, this update does not overwrite the observed branch. These are structural properties, not posterior calibration guarantees.

Training on the admitted conditional is essential. For a bivariate Gaussian $(W,V)$ with unit variances and correlation $\rho$, evaluating its joint score at $V=0$ gives $-W/(1-\rho^2)$, whereas the marginal score of $W$ is $-W$. At this fixed noise level, the restricted score corresponds to variance $1-\rho^2$ instead of 1; this is not a claim about the output variance of a finite reverse sampler. This elementary counterexample motivates target-specific fitting in Eq. (9), rather than masking the output of a differently trained posterior. E4 compares those procedures in a known-law setting.

Measured values are not clamped as clean latents. An observed-state readout $q_o(z_o\mid C_F)$ is fitted on the same source reference pairs, or calculated analytically under a known observation/noise model. The first learned readout may be Gaussian and is evaluated as an approximation. It is shared across mechanism arms. The construction samples

$$
z_o^{(b)}\sim q_o(\cdot\mid C_F),\qquad
w_0^{(b)}\sim q_\theta(\cdot\mid z_o^{(b)},C_T),\qquad
q(z_o,w_0\mid C_F)=q_o(z_o\mid C_F)q_\theta(w_0\mid z_o,C_T). \tag{13}
$$

Each $z_o^{(b)}$ remains fixed within its reverse trajectory. The factorization preserves the learned dependence; it does not make either fitted factor exact. Independently drawing the observed and missing marginal posteriors is a different, generally incoherent procedure. In the primary mechanism comparison, a common diagnostic readout $h_\psi$ is trained on source reference tuples and source labels, then frozen. It retains the same observed code $R$ and averages coherent predictions:

$$
\widehat p(y\mid C_F)=L^{-1}\sum_{b=1}^{L}
 h_\psi(y\mid R,z_o^{(b)},B_ew_0^{(b)},a,\text{support status}). \tag{14}
$$

A separately trained observed-only classifier uses the same source labels. It is not constructed by forcing a complete-state head to consume missing-state zeros. End-to-end head refitting and moment-only summaries are secondary ablations, distinct from the fixed-readout contrast. No inferred value is reported for ineligible or global-null coordinates.

### 3.5 Algorithm and mechanism contrasts

**Algorithm 1. Source-qualified temporal posterior inference.**

| Step | Operation |
|------|------------------------------------------------------------------------------------------|
| A1 | Split source recordings; fix reference, acquisition transformations, ontology and observation horizon. Construct the paired targets in Eq. (6). |
| A2 | Select a jointly identified target under the complete observation; freeze $B_e,G_e$ and their deployment descriptor rule. |
| A3 | Fit the shared anchor, observed readout and diagnostic head on source data. Select/freeze them on source validation; form $C_T$ with Eq. (8). |
| A4 | Draw a source tuple, noise level and Gaussian noise. Construct Eq. (3), predict velocity and update $\theta$ with Eq. (9). Select the generator on source validation. |
| A5 | For each deployment recording, compute the measured-evidence code. For each posterior draw, sample $z_o$ once and initialize $w_K$ in the admitted basis. |
| A6 | At each declared reverse level, predict $\widehat v$, convert with Eq. (11), and apply Eq. (12). Keep $z_o$ fixed throughout that draw. |
| A7 | Aggregate Eq. (14); report support status and unestimated components. Score the common target and original recording groups. Empty eligibility returns the observed-only prediction without a missing sampler. |

For the restriction-by-dynamics experiment, $r=1$ uses the admitted basis; $r=0$ permits an ambient missing-state trajectory, but receives only the same admitted source targets and loss. Its complementary forward state is independent nuisance noise, not an unknown clean complement. All arms receive identical support descriptors. With unrestricted function classes, independent nuisance noise supplies no additional Bayes information; any predictive benefit of restriction concerns finite-model fitting, sampling or resource use. When the entire missing space is admitted, the restriction contrast may collapse to an equivalence check. Posterior score, diagnostic macro-F1, emitted coverage and cost are reported separately using Eq. (5). Changing only the final output mask tests output suppression, not the proposed training-and-sampling intervention.
