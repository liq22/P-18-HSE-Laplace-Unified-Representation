## 2. Basic Theory and Problem Formulation

### 2.1 Problem setting

The task is fault classification on an industrial dataset excluded from model fitting. Let $d$ index a dataset, $i$ an original recording, and $a$ an acquisition configuration. Different views of one recording share its underlying event; equal fault labels in different datasets do not imply paired events. A measurement is written as

$$
x_{di}^{(a)}=\mathcal A_{d,a}\Psi_d(z_{di},u_{di})+\varepsilon_{di}^{(a)}, \tag{1}
$$

where $z_{di}$ is a reference state, $u_{di}$ the operating condition, $\Psi_d$ the mechanical response, and $\mathcal A_{d,a}$ the sampling/sensing operator. This distinction separates acquisition loss from a change in machine dynamics. Source labels and source validation groups are available; target labels enter only final evaluation. A common class ontology and a source-established reference are required for the closed-set comparison [@zhao2019invariant; @gulrajani2021domainbed].

The visible record $C_F$ contains measured values, timestamps, valid-value masks and deployment-available acquisition descriptors. Reference targets may be used during source training and held-out scoring, not as deployment inputs. A fixed observation horizon determines which times are visible. The outputs are class probabilities and, where a reference is available, a distribution over a specified missing target. A noisy reference feature is distinguished from a noise-free physical state. The resource budget specifies training/selection effort, transmitted condition size, denoiser evaluations and posterior draw count. No target-specific representation, normalization or head is fitted.

### 2.2 Relevant theoretical foundations

**Observability and conditional identification.** After calibration to a common finite-dimensional inner-product space $\mathcal H$, a linear reference model is $x_e=A_ez+\varepsilon_e$, with $e=(d,a)$. Its structurally observable space is $\mathcal O_e=\operatorname{range}(A_e^\top)$. Define the sum and intersection of source spaces as $\mathcal U_s=\sum_j\mathcal O_j$ and $\mathcal C_s=\bigcap_j\mathcal O_j$. For the deployment scope $\mathcal O_e\subseteq\mathcal U_s$, ordinary orthogonal decomposition gives

$$
\begin{aligned}
\mathcal C_e&=\mathcal C_s\cap\mathcal O_e,&
\mathcal P_e&=\mathcal O_e\cap\mathcal C_e^\perp,\\
\mathcal M_e&=\mathcal U_s\cap\mathcal O_e^\perp,&
\mathcal N_0&=\mathcal U_s^\perp,\\
\mathcal H&=\mathcal C_e\oplus\mathcal P_e\oplus\mathcal M_e\oplus\mathcal N_0.
\end{aligned} \tag{2}
$$

These roles are common-observable, observed-private, source-supported-missing and source-global-null. The algebra is an application of subspace decomposition, not a new observability result. Range/null structure already organizes inverse diffusion [@kawar2022ddrm; @wang2023ddnm]. A positive coordinate sensitivity is weaker than recoverability: $A=[1,1]$ observes a sum, not both coordinates separately. Weak noisy directions also differ from exact nullity. A nonlinear encoder does not automatically induce the required physical observation operator [@khemakhem2020ivae; @locatello2019disentanglement].

Support alone does not identify a conditional distribution. Identification concerns agreement of the required conditional across joint models compatible with the observed source law and the declared assumptions. Paired reference observations, suitable corruption ensembles or a specified physical coupling can provide identifying information [@daras2023ambient; @daras2024consistent; @rozet2024diem]. Source identification, finite-sample estimation and target-domain transport are separate questions. A correlated prior may update a source-null variable indirectly even though its likelihood has no direct sensitivity to that variable.

**Conditional denoising.** Gaussian diffusion corrupts a target while retaining the condition. With $\alpha_k^2+\sigma_k^2=1$, its forward variable and standard velocity target are

$$
w_k=\alpha_kw_0+\sigma_k\epsilon,\qquad
v_k=\alpha_k\epsilon-\sigma_kw_0,\qquad
\epsilon\sim\mathcal N(0,I). \tag{3}
$$

Conditional score training and missing-value diffusion are established mechanisms [@ho2020ddpm; @tashiro2021csdi; @alcaraz2023sssd]. Velocity, noise and clean-target prediction have different implied loss weights [@salimans2022distillation]. Stable Laplace modal functions supply a temporal inductive bias, distinct from the diffusion noise law [@holt2022neurallaplace; @you2026llapdiff].

### 2.3 Mathematical formulation

A candidate missing target is a subspace $\mathcal I_e\subseteq\mathcal M_e$, together with the conditioning information used to infer it. Let $z_o$ denote the observed-subspace reference state and $w_0$ coordinates of the missing target. Fix the source mixture weights, reference map and observation design. They induce a joint reference law $P_s^{\rm ref}(z_o,w_0,C_F,a)$. For an explicit physical model this law factorizes into a state prior and acquisition likelihood; for paired reference features it is the pushforward law of the paired records. Its regular conditional $p_s^{\rm ref}(z_o,w_0\mid C_F,a)$ is the population inference target. We call a fitted $q$ a *conditional latent distribution approximation*, or a *posterior approximation under this reference law*. A learned conditional density need not be obtained by an explicit Bayes division, but it must name the joint law it approximates. A compressed condition $C_T=\mathcal T(C_F)$ is part of the model specification, not an additional observation. Jointly distributed observed/missing samples require the joint law; knowing its separate marginals is insufficient. Compression changes the optimal conditional: the missing factor targets $p_s^{\rm ref}(w_0\mid z_o,C_T)$, which need not equal $p_s^{\rm ref}(w_0\mid z_o,C_F)$. Equality requires conditional sufficiency of $C_T$ for this target [@oko2025sufficiency].

Let $\mathcal X$ collect the fixed source groups/splits, reference, admitted target, allowed information, observation horizon, model-selection rule, diagnostic readout and resource budget. The intervention is $\iota=(r,\ell,c)$: restriction $r$, temporal parameterization $\ell$, and conditioner coordinates $c$. The fitted generator is allowed to change under $\iota$; its source data and fitting rule are controlled. For training/sampling randomness $\xi$, write

$$
\tau_i^{\iota}\sim P_{\iota}(\cdot\mid\mathcal X,C_{F,i}),\qquad
T_i^{\iota}=T(\tau_i^{\iota}),\qquad
\widehat p_i^{\iota}=D(\tau_i^{\iota}). \tag{4}
$$

Here $\tau$ includes fitting and the reverse-sampling path, $T$ records intermediate leakage, observed-evidence drift and computation, and $D$ returns diagnostic probabilities. This is an intervention on the inference procedure, not a causal claim about faults. The primary diagnostic outcome $S_{r\ell,e}$ is the expectation over fitted replicates of macro-F1 computed from the target's recording-balanced pooled confusion matrix. Individual windows do not have independent macro-F1 outcomes. Posterior quality uses a proper score on a common reference target; coverage and cost are separate outcomes [@gneiting2007proper]. Holding $c$ fixed, the restriction simple effect and interaction are

$$
\Delta_{r,e}(\ell)=S_{1\ell,e}-S_{0\ell,e},\qquad
\Delta_{\mathrm{int},e}=\Delta_{r,e}(1)-\Delta_{r,e}(0). \tag{5}
$$

The same contrasts apply separately to negative Energy Score. Neither sign is assumed favorable.

**Transfer scope.** Let $\mu_s$ and $\mu_t$ be the source and target laws of the complete deployment-visible condition (including $a$). Conditional reuse is justified on a declared region $\Omega$ only under a common reference meaning, overlap and conditional transport:

$$
\mu_t(\cdot\mid\Omega)\ll\mu_s,
\qquad
P_t^{\rm ref}(z_o,w_0\mid C_F=c)
 =P_s^{\rm ref}(z_o,w_0\mid C_F=c),\quad \mu_t\text{-a.e. }c\in\Omega.
$$

Overlap concerns where a conditional is evaluated; it does not identify its values. Likewise, geometric source visibility is not joint statistical identification. These assumptions are not certified by a low source-validation loss or by matching acquisition descriptors. The label mechanism may shift even when the state conditional transports [@zhao2019invariant]. We therefore test acquisition/conditional mismatch and diagnostic transfer separately. No finite unlabeled target batch is used to prove these population equalities or to tune the source model.

### 2.4 Existing limitation and research gap

Figure 1 separates observation support from conditional identification. Let $C,P$ be independent fair bits, with source A observing $(C,P)$ and source B observing $(C,M)$. Let $O_{\rm src}$ denote the source-indexed experiment observing either $(C,P)$ or $(C,M)$, never the full triple. The two joint worlds $M=P$ and $M=1-P$ induce identical laws of $O_{\rm src}$. They agree on $p(M\mid C)$ but disagree on $p(M\mid C,P)$. Thus, observing every component somewhere, even with a shared component, does not determine the conditional used after adding private evidence. The source model needs additional joint information or a justified coupling assumption.

![**Observation support and conditional ambiguity.** (a) An aligned reference separates four source-relative roles; rows denote observation configurations, not paired events across datasets. (b) Two binary worlds produce identical observed source pair laws and opposite conditionals after private evidence is included. The final relation states the unidentified population object. The figure defines the problem; it contains no proposed encoder, generator or decision module.](figures/motivation.pdf){width=100%}

Missing-view models, constrained diffusion and corrupted-data learning supply relevant inference capabilities [@wu2018mvae; @shi2019mmvae; @aali2025ambientdps; @hosseintabar2025diffem]. They do not remove this observed-law ambiguity by increasing model capacity. A second distinction is equally important: restricting the values produced by a sampler does not establish the correctness of their distribution. Finally, a complete-model comparison couples restriction, temporal structure and conditioning. It cannot reveal which intervention changes posterior quality or diagnosis.

### 2.5 Research objective

The primary question is whether partial latent inference restricted to a jointly source-qualified target can improve source-only cross-dataset industrial diagnosis. Laplace temporal parameterization, statistical coordinates and conditional uncertainty coupling are subordinate mechanism questions under fixed target and information access. The target, visible information and scored population are fixed for each mechanism contrast. Identification is examined using source-compatible counterexamples and known reference designs; posterior quality and diagnostic utility are evaluated separately. Section 3 specifies the inference procedure that instantiates these interventions.
