# Source-supported partial posterior: assumptions, proofs and boundaries

## 1. Defined scope

Consider a finite-dimensional real reference space H, with linear source acquisitions x_e=A_e z+epsilon_e. Operators and noise laws are fixed independently of the unobserved z, or their dependence is included in the likelihood. The same reference coordinate has the same stated meaning across source acquisitions. Different machines need a validated correspondence, not merely identical class names. For nonlinear learned coordinates the results apply only after a valid induced observation/support relation is established.

All orthogonal complements below use the declared reference inner product. Let O_e=range(A_e^T), U_s=sum_j O_j, C_s=intersection_j O_j. The target scope assumes O_e subset U_s. Source-global-null means invisible to every **declared source operator**, not to every possible future sensor.

## 2. Proposition 1 — source-referenced four-role decomposition

Set C_e=C_s intersection O_e, P_e=O_e intersection C_e^perp, M_e=U_s intersection O_e^perp and N_0=U_s^perp. Then

$$
H=C_e\oplus P_e\oplus M_e\oplus N_0.
$$

**Proof.** C_e is a subspace of O_e, so O_e=C_e direct-sum (O_e intersection C_e^perp). Similarly O_e subset U_s implies U_s=O_e direct-sum (U_s intersection O_e^perp). Finally H=U_s direct-sum U_s^perp. Substitute the first two decompositions into the third. Each is orthogonal; hence the four component projectors sum to the identity and have zero pairwise products. ∎

For sources C_e=C_s. For a target acquisition C_e can be smaller: keeping the old common mask fixed would misclassify previously common but now absent information. If O_e is not contained in U_s, this four-role source model does not cover its newly observed directions. Such genuine new measurements must not be called source-supported recovery of N_0.

**Sensitivity is not observability.** With A=[1,1], both diagonal entries of A^T A equal one, yet z and z+(1,-1) have the same observation. Neither individual coordinate is identified; only their sum is. Diagonal sensitivity masks therefore cannot replace row-space observability without an additional block-separable assumption. Finite-noise ill-conditioning must also be separated from exact nullity.

This is elementary subspace algebra used to define an industrial inference contract, not a new general observability theorem.

## 3. Proposition 2 — source support does not identify every conditional

Let C and M be binary and uniformly distributed marginally. The joint laws M=C and M=1-C have the same separate marginals but opposite conditionals. If source acquisition 1 observes only C and source acquisition 2 observes only M on unpaired events, the two laws produce identical observed-data distributions. Therefore that source experiment does not identify p(M|C).

**Proof.** For either law, each separately observed bit is Bernoulli(1/2). The likelihood of any unpaired sample is consequently the same, while p(M=1|C=1) is one in the first law and zero in the second. ∎

Paired events that reveal the joint state resolve this finite example. More generally, pairing still needs an identifiable observation/noise model. Conversely, suitable random corruption ensembles can identify a joint distribution without paired clean views, as shown in Ambient Diffusion. Pairing is one sufficient route under its assumptions, not a universal necessity. An inferable target is defined by invariance of its joint conditional law across all joint models compatible with the source observation law and the declared assumptions. Separately identified marginal conditionals do not establish an identified multivariate joint posterior.

A source-identified conditional does not automatically transfer. Holding source C,M fixed and changing the target relation from M=C to M=1-C leaves source validation unchanged but reverses the correct target prediction. Any deployment guarantee needs an explicit transportability condition or must remain an empirical held-out result. Source and target acquisition descriptors alone do not prove that condition.

## 4. Proposition 3 — global-null likelihood and prior-mediated updates

Let P_0 project onto N_0. Then A_e P_0=0 for each source. Writing z=z_s+z_0 gives

$$
p(\{x_e\}_e\mid z_s,z_0)=p(\{x_e\}_e\mid z_s)
$$

for a declared noise model independent of z_0 given z_s. This is a likelihood statement conditional on the supported state. It does **not** imply p(z_0|x)=p(z_0) for a correlated prior.

**Proof.** Substitute A_e(z_s+z_0)=A_e z_s into each acquisition likelihood (or its correctly correlated joint likelihood). ∎

For an unrestricted prior extension, two distributions with identical supported-state marginal but different conditional laws p(z_0|z_s) induce the same source observations. Hence that conditional extension is not identified by source likelihood alone. If an external prior fixes it, posterior inference can propagate observations through that assumed coupling.

**Finite Gaussian counterexample.** Let (Z_s,Z_0) have unit variances and correlation 0.8, and X=Z_s+epsilon with unit independent Gaussian noise. Given X=1,

$$
\mathbb E[Z_0\mid X=1]=0.4,\qquad
\operatorname{Var}(Z_0\mid X)=1-0.8^2/2=0.68.
$$

The likelihood still contains no direct Z_0 term. Under an independent prior the same observation instead leaves mean zero and variance one. These are different prior assumptions, not different source measurements. The proposed method excludes N_0 from recovery outputs to make this evidential boundary explicit; it does not claim that all Bayesian beliefs on N_0 are impossible.

## 5. Proposition 4 — eligibility-preserving generation

Let I_e be a source-justified subspace of M_e and G_e its fixed orthogonal projector. In an internal accumulator, initialize v_K in I_e and, for any measurable proposed reverse update F_k, set

$$
v_{k-1}=G_eF_k(v_k,C_T,\xi_k).
$$

Then v_k belongs to I_e at every step and (I-G_e)v_k=0. Equivalently, a representation r_o carried outside I_e remains unchanged if the full update is r_o+v_{k-1}, with r_o orthogonal to I_e.

**Proof.** The initialization is in the projector's range. Applying G_e maps any proposed update into that range, so induction proves the statement. Orthogonality eliminates the complementary component. ∎

Zero in the internal accumulator is not a claimed recovered value for an unsupported coordinate; those coordinates are omitted or marked unestimated in the public output. With rank(G_e)=0 there is no generative target. If the support projector changes during sampling, or a final dense decoder mixes supported and unsupported physical coordinates, this proof no longer certifies the corresponding physical output. It is a support-compliance property, not proof that q_theta is the correct posterior. Masked and null-space generation have direct predecessors in CSDI, SSSD and DDNM; the proposed contribution concerns the source-qualified target and its industrial coupling, not projection alone.

## 6. Existing error identities on the admitted target

Fix one acquisition/design and its eligible target Z_m. Let C_T be a deterministic measurable function of complete visible C_F, including all actual side inputs in both. With compatible conditional densities and finite expected KL,

$$
\mathbb E\operatorname{KL}\{p(Z_m\mid C_F)\Vert q_\theta(Z_m\mid C_T)\}
=I(Z_m;C_F\mid C_T)
+\mathbb E\operatorname{KL}\{p(Z_m\mid C_T)\Vert q_\theta(Z_m\mid C_T)\}.
$$

**Derivation.** Insert p(Z_m|C_T) into the log density ratio. The first expectation is conditional mutual information because C_T is determined by C_F. For the second use the tower property to integrate first conditional on C_T, obtaining its conditional KL. This is the shared Theory 09, applied to the same admitted target. An arbitrary diagonal-Gaussian plug-in is not automatically the true compressed conditional.

Under the same Gaussian diffusion schedule and a square-integrable regression target V_tau, the optimal full/compact denoisers satisfy

$$
\mathcal R_T^\star-\mathcal R_F^\star
=\mathbb E\|f_F^\star-f_T^\star\|^2.
$$

**Derivation.** Expand V_tau-f_T as (V_tau-f_F)+(f_F-f_T). The cross expectation vanishes by conditional-mean orthogonality. This requires the nested information sets to contain the same noisy target, time and consumed metadata. An actual finite model has a further fitting/optimization term. Changing target mask, sampling schedule, parameterization or batch-weight normalization changes the estimand and requires the corresponding weighting. The detailed shared Theory 10 retains those conditions.

Neither identity guarantees better diagnostic macro-F1 or identifies an unknown target conditional. The learned prior and all posterior samples are functions of the same observations plus source training/randomness; they create no new measured information. If the fault label depends on omitted unsupported components, no task-sufficiency guarantee follows for the partial posterior; this is an explicit diagnostic failure condition rather than an assumption erased by rejection.

## 7. Executable scope and contribution boundary

The same-stem Notebook checks the four-role algebra, target loss of source-common support, mixed-coordinate ambiguity, unpaired conditional counterexample, correlated-prior null update and projected sampling compliance. Its CSV records finite witnesses only. The existing full-statistic/diagonal-token collision and native three-arm tests are retained elsewhere, not relabelled as support-constrained LLapDiff training.

The current native code does not yet implement source-qualified modal blocks or their restricted reverse process. General algebra and standard information identities are supporting results. A new industrial method claim requires a validated source-reference correspondence, actual projected native training and unseen-dataset evidence against matched posteriors/conditioners. Rejecting every missing block yields perfect structural compliance but no recovery utility; report admitted support coverage and useful posterior/diagnostic performance jointly.
