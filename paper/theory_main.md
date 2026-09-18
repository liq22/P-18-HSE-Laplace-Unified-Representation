# Source-supported partial posterior: assumptions and analysis

## 1. Scope

Consider a finite-dimensional real reference space H and source acquisitions x_e=A_e z+epsilon_e. Operators and noise laws are fixed independently of unobserved z, or their dependence is included in the likelihood. Coordinates have the same declared meaning across acquisitions; a learned reference needs an established induced observation relation. All complements use the reference inner product.

Let O_e=range(A_e^T), U_s=sum_j O_j and C_s=intersection_j O_j. The deployment scope assumes O_e subset U_s. Source-global-null means invisible to the declared source operators, not to every possible sensor. Exact nullity differs from noisy ill-conditioning.

## 2. Proposition 1 — source-relative role decomposition

Define C_e=C_s intersection O_e, P_e=O_e intersection C_e^perp, M_e=U_s intersection O_e^perp and N_0=U_s^perp. Then

$$
H=C_e\oplus P_e\oplus M_e\oplus N_0.
$$

**Proof.** Since C_e subset O_e subset U_s subset H, successively decompose O_e into C_e and its orthogonal complement inside O_e, U_s into O_e and its orthogonal complement inside U_s, and H into U_s and U_s^perp. Substitution gives the four orthogonal components. Their projectors sum to the identity. $\square$

For source domains C_e=C_s. A target can lose a source-common direction, requiring a new C_e. If O_e is not contained in U_s, genuinely new measurements fall outside this four-role scope. With A=[1,1], positive diagonal entries of A^T A do not identify either coordinate separately: z and z+(1,-1) have identical measurements. These are elementary subspace facts, not a new observability theorem.

## 3. Proposition 2 — common source views do not identify the full-input conditional

Let C and P be independent Bernoulli(1/2) variables. In world W_plus let M=P; in world W_minus let M=1-P. Source A observes (C,P), source B observes (C,M), and their events are unpaired. Both source observation laws are identical across the two worlds, yet

$$
p_+(M=1\mid C=1,P=1)=1,\qquad
p_-(M=1\mid C=1,P=1)=0.
$$

**Proof.** In both worlds, C is independent of P and of M, and each bit is fair. Hence each observed pair has the same uniform distribution on four outcomes. The conditional statements follow from the respective deterministic relationships between P and M. $\square$

The source-B conditional p(M given C) is the same uniform law in both worlds. It is identified in this example, while p(M given C,P) is not. The source-common variable C is therefore not automatically a conditional-independence separator. Adding observed private evidence changes the required conditional; a model trained for one cannot simply be claimed to represent the other. Removing C recovers the earlier two-marginal counterexample, so the new witness strengthens rather than contradicts that boundary.

Fix the source observation law and declared model class. For a source-selected candidate I_e subset M_e and a fixed complete conditioning function C_T, require agreement of p(Z_I given C_T) across every compatible joint law, almost surely on the supported conditioning domain. When diagnosis consumes coherent observed/missing draws, require the corresponding joint p(Z_o,Z_I given C_T). Separate marginal identification is insufficient. No automatic largest admissible subspace or empirical reconstruction threshold is implied by this definition.

A joint source acquisition revealing (C,P,M) distinguishes these finite worlds. More generally, pairing requires an identifiable observation/noise model. Suitable corruption ensembles can also identify distributions, as studied in Ambient Diffusion and related corrupted-data work. Paired clean data are not a universal necessity. Source identification remains distinct from transportability: changing a target from M=P to M=1-P leaves every source-validation result unchanged. A deployment guarantee requires an explicit conditional-transport and overlap assumption.

## 4. Proposition 3 — source-null likelihood and prior-mediated inference

Let P_0 project onto N_0. For every source, A_e P_0=0. If the declared noise law has no additional dependence on z_0 given z_s, then

$$
p(\{x_e\}_e\mid z_s,z_0)=p(\{x_e\}_e\mid z_s).
$$

**Proof.** Substitute A_e(z_s+z_0)=A_e z_s into the correctly specified joint measurement likelihood, allowing dependent noise where declared. $\square$

This does not imply an unchanged marginal posterior under a correlated prior. Two prior extensions with the same supported-state marginal but different p(z_0 given z_s) produce the same source observation law. Source likelihood alone does not identify that extension.

For unit-variance Gaussian (Z_s,Z_0) with correlation 0.8 and X=Z_s+epsilon with independent unit Gaussian noise, X=1 gives

$$
\mathbb E[Z_0\mid X=1]=0.4,\qquad
\operatorname{Var}(Z_0\mid X)=1-0.8^2/2=0.68.
$$

An independent prior instead gives mean zero and variance one. Excluding N_0 from recovered-value outputs declares an evidential scope; it does not prohibit externally assumed Bayesian beliefs.

## 5. Proposition 4 — support-preserving reverse proposals

Let G_e be the fixed orthogonal projector onto an admitted I_e subset M_e. Initialize v_K in I_e and let F_k be any measurable proposal. Set

$$
v_{k-1}=G_eF_k(v_k,C_T,\xi_k).
$$

Then v_k lies in I_e at every step and (I-G_e)v_k=0. A separately retained r_o orthogonal to I_e remains unchanged in r_o+v_k.

**Proof.** The initialization lies in range(G_e), and applying G_e maps each proposal to that range. Induction and orthogonality give both statements. $\square$

With rank(G_e)=0 there is no missing-state sampler. Internal zero means no update, not a certain zero-valued reconstruction. Changing projectors during sampling or mixing blocks through a dense physical decoder requires a different support analysis. The proposition establishes structural compliance, not posterior correctness. Missing-only and null-space generation have predecessors in CSDI, SSSD and DDNM.

## 6. Inherited error identities on a fixed admitted target

Fix an acquisition and admitted target Z_m. Let the complete consumed C_T be a deterministic function of full visible C_F, including all actual side inputs. With compatible conditional densities and finite expected KL,

$$
\mathbb E\operatorname{KL}\{p(Z_m\mid C_F)\Vert q_\theta(Z_m\mid C_T)\}
=I(Z_m;C_F\mid C_T)
+\mathbb E\operatorname{KL}\{p(Z_m\mid C_T)\Vert q_\theta(Z_m\mid C_T)\}.
$$

**Derivation.** Insert p(Z_m given C_T) in the log ratio. The first expected term is conditional mutual information; conditioning and the tower property give the second conditional KL. This applies the shared compression identity, not a new information principle. A Gaussian plug-in need not equal the true compressed conditional.

For a common square-integrable denoising target V_tau and nested information sets containing the same noisy target, time and metadata,

$$
\mathcal R_T^\star-\mathcal R_F^\star
=\mathbb E\|f_F^\star-f_T^\star\|^2.
$$

**Derivation.** Expand V_tau-f_T as (V_tau-f_F)+(f_F-f_T); conditional-mean orthogonality cancels the cross term. Fitted consumers have additional approximation/optimization errors. Different target parameterizations, weights, schedules or masks require their actual objectives rather than an unweighted substitution.

Neither identity proves diagnostic macro-F1 improvement or transport of an unidentified conditional. Posterior samples use the same observations plus source learning and randomness. If labels require omitted unsupported components, the partial posterior need not be task-sufficient.

## 7. Executable and empirical scope

The same-stem Notebook checks role algebra, target loss of common support, mixed-coordinate ambiguity, the overlapping-source counterexample, prior-mediated null inference, projected proposals and conditional reversal. Its 14 retained numerical values are finite theoretical witnesses. They are not trained restricted-LLapDiff results. The source-reference calibration, actual native projected training and industrial LODO remain required. Rejecting every target is assessed with admitted coverage and diagnostic utility, not structural compliance alone.
