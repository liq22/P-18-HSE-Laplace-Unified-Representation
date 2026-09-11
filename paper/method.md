# Method — statistically anchored HSE conditioning with conditional model selection

## 1. Fixed objects and information access

Freeze a source-trained HSE extractor and a reference encoder. The observed history is \(O\), the deployment-available acquisition descriptor is \(a\), and

\[
F=HSE_0(O,a_{enc}),\qquad Z_0=E_{ref}(X_{ref}),\qquad U=L\operatorname{vec}(Z_0).
\]

The paper condition is

\[
C_F=(F,M_F,a),
\]

where \(M_F\) is the valid-history mask. A high-rate/reference view may define supervision but is never given to one comparator as a hidden inference input. The known-pole coefficient vector used by the analytical oracle is not identified with \(Z_0\) or with LLapDiff's learned modal parameters.

## 2. One supervised ordinary code and one statistical reparameterization

A trainable source-side trunk produces a fixed-budget code

\[
R=g_\theta(C_F)\in\mathbb R^q,
\]

and a global moment head reads the **same R**:

\[
m_\psi(R),\qquad
S_\psi(R)=B_\psi(R)B_\psi(R)^\top+\lambda I.
\]

The lower-triangular factor has a positive diagonal and λ is a public covariance constraint in standardized target units. Stage one minimizes

\[
\mathcal L_G=
\frac12\mathbb E_s\!\left[
\log\det S_\psi(R)+
(U-m_\psi(R))^\top S_\psi(R)^{-1}(U-m_\psi(R))
\right].
\]

The score gradient updates both the moment head and the trunk that produces R. A detached auxiliary head is an invalid-control negative test. A single checkpoint is chosen using source validation only. Record total score, log-determinant, Mahalanobis term, minimum eigenvalue and fraction at the declared covariance floor; positive definiteness alone is not calibration.

For fixed R and an unrestricted function class, the Gaussian score identifies the conditional first two moments of \(U\mid R\). It does not identify the full conditional distribution, prove joint optimization succeeds, or imply target-domain calibration.

## 3. Freeze once and form the matched messages

After stage-one selection, freeze HSE preprocessing, the trunk and the moment head; use evaluation mode and deterministic HSE patch selection. For \(d=\dim U\), let \(s=d+d(d+1)/2\). The matched messages are

\[
H_{B1aux}=R,
\]

\[
H_M=T(R)=
[m_\psi(R),\operatorname{vech}(\operatorname{chol}S_\psi(R)),R_{s+1:q}].
\]

Both have exactly q transmitted scalars. B1-aux is the strongest same-supervision control because it sends the complete ordinary code that was actually trained by the auxiliary score. M is a deterministic function of R and therefore cannot create Bayes information relative to B1-aux.

The original HSE/LLapDiff conditioner B1 remains the **reference model**. B1-aux and M are the two principal **single representations**. B0 denotes the unmodified official LLapDiff reference entry where task compatibility permits.

## 4. The four comparison levels required by the theory

### 4.1 Reference model

`REF = B1`: the ordinary HSE condition without the new stage-one statistical supervision. It answers whether any gain merely comes from the extra source objective.

### 4.2 Best single representation

Choose between B1-aux and M using source validation only:

\[
j_{single}=\arg\min_{j\in\{R,M\}}\widehat{\mathcal R}^{src}_j.
\]

The target test set never chooses this arm.

### 4.3 Static fusion

As a low-complexity control, standardize R and M using source-only statistics and form

\[
H_{static}(\alpha)=\alpha\widetilde R+(1-\alpha)\widetilde M,
\qquad \alpha\in[0,1].
\]

The scalar α is chosen on source validation and fixed for all acquisition conditions. The moment semantics are assessed before this fusion; the fused coordinates are ordinary conditioner features. This baseline adds one scalar parameter and no extra message dimension.

### 4.4 Dynamic acquisition-conditioned routing

Dynamic routing is **not activated by default**. First estimate routing headroom from group-level source validation as defined in `theory_main.md`. If the headroom exceeds a predeclared practical margin, fit the smallest source-only gate

\[
\alpha_\gamma(a)=\sigma(w^\top \widetilde a+b),
\]

and use

\[
H_{route}=\alpha_\gamma(a)\widetilde M+[1-\alpha_\gamma(a)]\widetilde R.
\]

The gate may use sampling rate, observed duration, missing fraction, channel availability and explicitly observed quality indicators. It may not use fault labels, target-test statistics, dataset identity as a shortcut, reference targets or future measurements. Gate parameters and latency are reported. If routing headroom is practically zero, the final method is the best single representation and the router is removed.

Hard source-risk selection is the limiting diagnostic used in the theory. The soft gate above is an empirical finite model; no theorem asserts it reaches the oracle selector.

## 5. Native LLapDiff stage

All arms retain the same reference encoder, \(Z_0\), target map, native LLapDiff architecture, prediction parameterization, scheduler, target mask, optimizer/update budget and checkpoint rule. Stage two updates only the denoiser (and, for the routing experiment only, the explicitly declared small gate when the protocol calls for joint source training). No arm receives an additional `cond_summary_raw` copy.

For the principal pilot, first keep the existing native setting: v-prediction, 64-step cosine schedule, uniform nonzero training times, one-layer/two-head denoiser, no dropout and no loss weighting. Other epsilon/x0/Min-SNR conventions are acceptance checks before becoming experiment factors.

On the same batch and same noise, independently reconstruct native loss components: target, valid-coordinate reduction, raw loss, raw/effective weight and final mean. Batch-normalized weights use the realized batch denominator.

## 6. Industrial diagnosis readout

The representation paper must demonstrate industrial utility, not only latent generation. For PHM experiments, freeze the evaluated conditioner after representation training and attach the same diagnostic head to each arm. The minimum head is linear; a small MLP is a secondary capacity check. Training labels are used only in this downstream diagnostic stage. Report macro-F1 as the primary class metric, AUROC where class scores are valid, and group-level confidence intervals. No target-domain labels are used to adapt the representation or router.

The reference-latent Energy Score and the diagnostic macro-F1 answer different questions and are never merged into one scalar ranking.

## 7. Population, empirical and conditional claims

Population quantities \(\mathcal R_j(a)\) and routing headroom are estimands. Their empirical counterparts are calculated from source-validation groups and can be noisy. A dynamic gate is justified only when the conditional ordering is reproducible at the independent-unit level and remains useful on an unseen acquisition condition.

The learned gate carries no unconditional generalization theorem. The plug-in routing result in `theory_main.md` is invoked only under its stated conditional-risk estimation assumption. Source calibration does not imply target calibration.

## 8. Cost and decoupling

Report message scalars, HSE/trunk/head/gate/denoiser parameters, training updates, GPU memory, per-event latency, sampling time and repeated-draw cost. Equal q is only an interface match.

`paper/` and `experiments/p19/` do not import PHMFactory internals. PHMFactory is invoked through its public CLI and exported arrays/configs. The parent repository receives an `external/phmfactory` gitlink only after the exact upstream revision has passed the real-data acceptance goal; until then the pointer is intentionally absent. No PHMFactory core code is changed to accommodate a paper-specific protocol.
