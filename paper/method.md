# Acquisition-Support-Aware HSE–LLapDiff

## 1. Dataset, event and target

Let e index a dataset/acquisition domain and i an independent physical event or original recording. Write

$$
x_{ei}=\mathcal A_e\Psi_e(z_i,u_i)+\varepsilon_{ei},
$$

where u is operating condition, z a source-referenced latent state and Psi_e the mechanical response map. A common fault ontology does not imply identical Psi_e. Same-event pairing is used only for complementary source acquisitions or transformations of one recording; unrelated datasets are not paired by sorting class labels.

The first identifiable oracle fixes a source-calibrated finite dictionary and reduces this model to x_e=A_e z+epsilon_e with known noise. For a learned extension, the reference encoder must establish comparable, block-structured target coordinates across the declared mechanical family. Its support assignment is fitted from source data/physics only. An arbitrary nonlinear VAE latent does not satisfy this requirement automatically. The native LLapDiff's predicted modal parameters are not taken as ground-truth mechanical coefficients.

## 2. Structural support and inference eligibility

For the linear reference let O_e=range(A_e^T), U_s=sum_j O_j and C_s=intersection_j O_j over sources. The first deployment scope requires O_e contained in U_s. Define

$$
C_e=C_s\cap O_e,\quad P_e=O_e\cap C_e^\perp,\quad
M_e=U_s\cap O_e^\perp,\quad N_0=U_s^\perp.
$$

For a source domain C_e=C_s; for an unseen acquisition, a previously common direction may be missing. The four spaces are orthogonal and complete under the declared nesting. Their projectors need not be diagonal in raw latent coordinates. Coordinate masks are used only for an aligned, block-separable reference. A positive diagonal entry of A^T R^{-1}A signals sensitivity, not individual-mode recoverability. Near-singular directions require a source-frozen numerical tolerance and a reported sensitivity analysis, not a silent structural-null label.

Let I_e be a source-justified subspace within M_e whose required conditional distribution is identifiable, and let G_e project onto I_e. This is an inference permission, not a padding mask or a learned certainty score. Its justification is paired source joint observations with an identifiable observation map, an identifiable random corruption ensemble, or a stated physical coupling. The first implementation may use a binary all-or-none decision per declared modal block; it must not infer permissions from target test labels. Identification is required for the joint eligible target, not merely for each of its one-dimensional marginals. Source identification and source-to-target conditional transportability remain separate assumptions.

The unresolved part M_e minus I_e is retained as missing-without-an-identified-conditional. N_0 is excluded from data-supported recovery outputs. A prior can still induce beliefs on N_0; that is not a measured reconstruction and is not reported as one.

## 3. HSE condition and statistical anchor

Construct the complete encoder-visible record C_F from observed values, timestamps, valid-value mask, acquisition descriptors, support projectors/mode roles and the identification decision. HSE supplies fixed-budget features; the statistical readout anchors a source-defined target functional. The generator consumes the same declared C_T=(H,a,roles,eligibility) in every compared arm. Role/eligibility metadata and side inputs count toward transmission and computation, even if sent outside the token tensor.

The existing matched mechanism uses one source-supervised code R and a trained affine head h(R). Its messages are H_R=R, H_A=[h(R),R_tail] (`head_affine`) and H_M=Phi(H_A), where Phi converts raw covariance coordinates to a positive-definite factor. These remain conditioner ablations, not the main scientific endpoint. The auxiliary Gaussian score acts on the path later consumed by the ordinary comparator. Freeze that path after source-only selection; retain score components, covariance constraints, dtype and rank diagnostics. Conditional moments are not a complete non-Gaussian posterior, and a moment-only condition can lose distributional shape.

## 4. Conditional posterior with restricted latent dynamics

The generative target is the eligible missing component. In an orthonormal basis B_e of I_e, use Gaussian forward perturbations

$$
v_\tau=\alpha_\tau v_0+\sigma_\tau\epsilon,\quad
v_0=B_e^Tz,\quad \epsilon\sim\mathcal N(0,I).
$$

Equivalently the ambient perturbation is G_e z_tau=alpha_tau G_e z+sigma_tau G_e epsilon. A reverse update is projected into I_e before it is combined with the retained observed-evidence representation. The projection must be applied throughout the reverse process, not only to its final displayed output. For zero eligible dimension, no diffusion process is invoked; the output carries the observed representation and its support status, not confident zero-valued recovered latents.

LLapDiff parameterizes the clean latent trajectory with stable damped modes, schematically

$$
\widehat z(t)=\sum_k e^{-\rho_k t}
\{b_k\cos(\omega_k t)+c_k\sin(\omega_k t)\},\qquad \rho_k\ge0.
$$

This is Laplace-domain temporal structure, not Laplace noise. The eligibility map applies to source-identified latent blocks; an unconstrained dense decoder must not remix them into claimed physical-null reconstructions. The block-separable target/decoder relation is therefore part of the source reference definition. Event-local damping, arbitrary-time evaluation and residual adequacy motivate the parameterization. Heavy tails or spikes alone do not establish its necessity.

Observed noisy measurements are not clamped as exact latent truth. Retain their original HSE evidence path. When a full joint posterior representation is needed, use the factorization

$$
q(z_o,z_m\mid C_T)=q_o(z_o\mid C_T)\,
q_\theta(z_m\mid z_o,C_T),\qquad z_m\in I_e,
$$

and carry observed uncertainty into the conditional sampler. q_o may be analytical in the oracle or an explicitly validated source readout. No independence between observed and missing posterior blocks is assumed. Preserving observed evidence is an architectural property; it is not a claim that its noise-free state has already been recovered.

## 5. Diagnosis and attribution

A source-trained diagnostic model aggregates predictions over coherent posterior draws,

$$
\widehat p(y\mid x_e)=\frac1L\sum_{\ell=1}^L
h_y(z_o^{(\ell)},z_m^{(\ell)},a_e,\text{support status}).
$$

Use the same source label ontology and diagnostic training rule for observed-only, point, Gaussian, finite-mixture, ordinary diffusion and LLapDiff arms. Do not use a random target head as zero-shot diagnosis. A posterior-mean/variance concatenation is a named cheaper ablation, not an assertion of full-distribution sufficiency. The output does not include an inferred value for N_0 or an ineligible missing component.

The comparison fixes target, conditioner, actual side information and eligible support when isolating the generative family; it fixes the generator and support when isolating R/H_A/H_M. Measure total encoder/reference-training/generator/head costs, posterior draws and factorization cost. Static prediction fusion and direct observed-only classifiers remain strong alternatives; dynamic routing is not required by this formulation.
