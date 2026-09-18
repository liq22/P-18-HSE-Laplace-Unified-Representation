# Acquisition-Support-Aware HSE–LLapDiff

## 1. Source reference and observation model

Let e denote an acquisition domain and i an independent event or original recording:

$$
x_{ei}=\mathcal A_e\Psi_e(z_i,u_i)+\varepsilon_{ei}.
$$

The operating condition u, mechanical response map Psi and acquisition operator are distinct. A common class label does not establish a common mechanical coordinate. The first reference model uses a source-calibrated finite dictionary, giving x_e=A_e z+epsilon_e with a declared noise law. A learned extension requires validated cross-source block correspondence and a compatible decoder. Without physical calibration, its target is a reference-feature posterior, not a recovered mechanical mode. Pair source views within an original recording or a declared joint acquisition, never by sorting labels from unrelated datasets.

## 2. Qualifying a target together with its condition

Write O_e=range(A_e^T), U_s=sum_j O_j and C_s=intersection_j O_j over sources. For the declared deployment scope O_e subset U_s, define

$$
C_e=C_s\cap O_e,\quad P_e=O_e\cap C_e^\perp,\quad
M_e=U_s\cap O_e^\perp,\quad N_0=U_s^\perp.
$$

These orthogonal spaces denote currently common, observed-private, source-supported-missing and source-global-null components. Recompute C_e for the current acquisition. General operators require subspace projectors; diagonal sensitivity alone is not coordinate recoverability. Separate exact nullity from weak noisy directions, using a source-selected tolerance with sensitivity analysis.

Let C_T be the complete condition supplied to the posterior, including HSE features, private evidence, acquisition descriptors and support information. Fix a candidate target I_e subset M_e. The pair (I_e,C_T) is admissible when every joint model compatible with the source observation law and the stated physical/statistical assumptions gives the same required conditional p(Z_I given C_T), almost surely on its supported conditioning domain. Joint identification, not separate coordinate-wise identification, is required. This is a population property of the observation design and assumptions, not a score threshold that proves identifiability from a finite dataset.

For coherent observed/missing draws, the stronger required object is p(Z_o,Z_I given C_T). Its factorization into observed and missing conditionals does not supply identification by itself. In particular, identification of p(M given C) cannot authorize p(M given C,P). Source pairing with an identifiable observation model, an identifiable corruption ensemble, or an explicit physical coupling can supply the missing relationship. Source-to-target transportability and conditioning-domain overlap remain separate assumptions. The finite common-view counterexample is given in the accompanying analysis.

Freeze the chosen joint target and its orthogonal projector G_e from source information. No largest universally identifiable subspace is presumed. Ineligible missing components and N_0 have no recovered-value output; an externally assumed prior may still express beliefs about them. A target with genuinely new measured support lies outside this four-role deployment scope, rather than being rejected as invented evidence.

## 3. HSE condition and statistical anchor

The complete encoder-visible record C_F includes values, times, masks and all allowed descriptors. HSE produces a fixed-budget condition. A source-supervised ordinary code R and one trained affine moment head h(R) give three interfaces:

$$
H_R=R,\qquad H_A=[h(R),R_{\rm tail}],\qquad H_M=\Phi(H_A).
$$

Phi maps raw covariance coordinates to a positive-definite factor; H_M retains the same tail. The Gaussian auxiliary score trains the exact R path used by the ordinary comparator. Freeze the source-selected checkpoint before comparing the three interfaces. All arms receive the same allowed side information and inference eligibility; side fields count toward memory and computation. Conditional moments anchor a declared source target but do not identify a non-Gaussian conditional law. In ideal arithmetic H_A and H_M are invertible on the attainable image of the existing factor map; finite precision and conditioning remain measurable diagnostics.

## 4. Restricted temporal posterior

For an orthonormal basis B_e of I_e, perturb only the admitted target:

$$
v_\tau=\alpha_\tau v_0+\sigma_\tau\epsilon,
\qquad v_0=B_e^Tz,\qquad\epsilon\sim\mathcal N(0,I).
$$

The equivalent ambient noise has covariance sigma_tau^2 G_e. Each reverse proposal is projected by G_e. The Laplace component parameterizes the temporal prediction schematically as

$$
\widehat z(t)=\sum_k e^{-\rho_k t}
\{b_k\cos(\omega_k t)+c_k\sin(\omega_k t)\},\qquad\rho_k>0.
$$

Physical time t is distinct from diffusion time tau. Damping and arbitrary-time evaluation motivate a local temporal bias, not a claim that the predicted poles are identified machine modes. A block-consistent reference/decoder is needed to translate latent support preservation into physical support preservation. Diffusion remains iterative and uses Gaussian perturbations.

Observed noisy values are not exact clean latents. Preserve the original HSE evidence path and, when joint draws are needed, use the source-identified factorization

$$
q(z_o,z_m\mid C_T)=q_o(z_o\mid C_T)\,
q_\theta(z_m\mid z_o,C_T),\qquad z_m\in I_e.
$$

The observed posterior q_o is analytical under a known oracle or an independently evaluated source readout. The missing sampler conditions on the same sampled z_o; independently sampling the two marginal posteriors is not a substitute for the joint. For rank(G_e)=0, no missing-state sampler is invoked.

## 5. Diagnosis and algorithm

A source-trained diagnostic model averages predictions over coherent draws:

$$
\widehat p(y\mid x_e)=L^{-1}\sum_{\ell=1}^{L}
 h_y(z_o^{(\ell)},z_m^{(\ell)},a_e,\text{support status}).
$$

A posterior-moment summary is a cheaper, separately named ablation. Direct observed-only diagnosis remains a primary comparator.

**Algorithm 1 — source-qualified temporal inference.**

1. Split original source groups; establish the reference, observation/noise model and class ontology using source data only.
2. Specify the actual C_T and qualify its joint target; freeze I_e, B_e and G_e under the declared assumptions.
3. Fit the shared HSE/statistical anchor on source training groups and select its checkpoint on source validation groups.
4. Train the conditional generator on the admitted target with the specified noise schedule, target parameterization and weighting. Retain the observed-evidence branch.
5. At inference, sample the observed uncertainty and run eligible-only reverse updates for coherent missing draws; omit unestimated coordinates.
6. Apply the source-trained diagnostic rule and report posterior, diagnosis, admitted coverage and total cost separately.

The restriction–dynamics comparison fixes steps 1–3, observed uncertainty, diagnostic training and evaluation targets, changing only the declared generative restriction and temporal parameterization in steps 4–5. Comparisons use the same prediction type and conditioning horizon. Velocity-target and clean-target objectives require explicit parameterization and weighting before an equivalence comparison. Every run records the actual parameter count, active dimension, updates, draws, latency and memory.
