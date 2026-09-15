# Method

## 1. Fixed feature and target paths

Let $F=HSE_0(O,a_{enc})$ and $Z_0=E_{ref}(X_{ref})$. Freeze the source-trained HSE and reference encoder, define $U=L\operatorname{vec}(Z_0)$ before comparing arms, and make the complete conditioner input $C_F=(F,M_F,a)$ explicit. Actual side columns are ordered and named. Source-only normalization, masks and deterministic patch selection remain fixed. The high-rate/reference view can supply the target but cannot become an undeclared inference input for one arm.

## 2. Shared statistical supervision

A trunk outputs $R=g_\theta(C_F)\in\mathbb R^q$. A global head on the **same code** outputs

$$
m_\psi(R),\quad S_\psi(R)=B_\psi(R)B_\psi(R)^\top+\lambda I.
$$

The nonnegative covariance floor $\lambda$ is an explicit model constraint in source-standardized target units. Train trunk and head with

$$
\mathcal L_G=\tfrac12\mathbb E_s\left[\log\det S_\psi(R)
+(U-m_\psi(R))^\top S_\psi(R)^{-1}(U-m_\psi(R))\right].
$$

The score gradient reaches the ordinary code used by B1-aux; an independent detached auxiliary head is not that control. Source validation selects one checkpoint. Log score, log-determinant, Mahalanobis term and covariance eigenvalues separately. The population optimum identifies moments conditional on R only under the stated function-class and covariance conditions; it does not establish calibration on an unseen acquisition.

## 3. Matched messages

Freeze the entire feature/trunk/head path after selection. With $d=\dim U$ and $s=d+d(d+1)/2<q$, transmit

$$
H_R=R,\qquad
H_M=[m_\psi(R),\operatorname{vech}(\operatorname{chol}S_\psi(R)),R_{s+1:q}].
$$

Both contain q scalars and share a checkpoint. These are dense **global summary tokens**, not the original patch-indexed tokens: their output mask is all-valid. The input mask remains explicitly consumed upstream. Statistical semantics are evaluated at the unnormalized readout, before any learned denoiser projection. No raw-summary copy or extra prefix stream bypasses the budget. Prefix/tail interventions test actual native consumption, not only storage.

## 4. Native conditional generation

Use the same LLapDiff architecture, frozen reference target, prediction parameterization, scheduler, query times, target mask, optimizer updates, initialization policy and checkpoint rule for both arms. In the initial pilot: v prediction, 64-step cosine schedule, uniform nonzero training times, no loss weighting, one-layer/two-head denoiser, and no dropout. These are the implemented small pilot, not final tuned settings.

Before training, independently recompute the native loss on the same batch/noise. If a later weighted objective uses a realized batch denominator, export and reuse it rather than replacing an expectation of a ratio by a ratio of expectations. Freeze means parameters, evaluation mode, buffers, preprocessing and patch realization, not `requires_grad` alone.

## 5. Four comparison levels

**Reference.** B1 uses the original ordinary HSE condition without the added source statistical objective; B0 runs the compatible official LLapDiff reference. These distinguish inherited model ability and extra supervision from message structure.

**Best single.** Train B1-aux and M with their shared selected conditioner. Select one complete trained arm using source validation. Never use target labels to choose the global winner.

**Static fusion.** For fixed trained arms, mix predictions/distributions using a single source-selected weight. Squared-error point predictions use their convex combination; classification uses normalized class probabilities; probabilistic trajectories use an actual mixture of predictive distributions, with a fixed total sampling budget. Both-arm compute must be charged. Averaging generated trajectories is not automatically sampling from the mixture. A separate same-q token-fusion model may be trained as a structural ablation, but its risk is measured as a new arm.

**Dynamic routing.** The minimal analyzed route selects one **fixed trained arm** from deployment acquisition descriptors using source-only risk estimates. It does not jointly change the denoisers. Hard headroom is only a necessary opportunity measure for such selection over those arms; compare its realized score and cost directly with static fusion. Refit neither gate nor normalization on target conditions. A soft token gate or jointly trained mixture is an optional empirical ablation with its own risk profile; it is not covered by the fixed-arm bound.

The real learned route/fusion integrations are not implemented by the toy simulator. First execute the existing two-arm native pilot. Do not build a router merely because two representations exist.

## 6. Industrial downstream head and metrics

Evaluate each frozen representation with the same linear diagnosis head, then one small MLP as a capacity control. PHMFactory alone defines PHM raw preparation, readers, labels and initial split. All exported windows retain the original file/run/bearing key available upstream. Derive acquisition views only within the frozen split. Speed/load shifts and sampling/missingness shifts are separate factors.

Report reference-latent Energy Score independently from diagnosis. For diagnosis, use recording-balanced pooled-confusion macro-F1 and show the conventional pooled-window metric separately. Source selection may use a declared additive score but does not acquire a macro-F1 theorem from that score.

## 7. Costs, interpretation and limits

Report parameters and computation for HSE, shared trunk, moment head, gate, diagnosis head and denoiser separately; charge statistical pretraining, model selection, all-arm fusion and posterior draws. Equal q is an interface match, not equal total cost. M is deterministic in R and cannot add Bayes information. A favorable finite experiment is evidence of representation accessibility under its trained model and budget, not an unrestricted sufficiency or physical-state identification guarantee.

`paper/` and `experiments/p19/` consume public CLI outputs/exported arrays, never PHMFactory factories. A revision-specific acceptance script runs inside the isolated upstream environment only to restore the unchanged upstream model and export its own datasets. It does not alter PHMFactory core. The submodule revision is accepted only for the exact reproduced MFPT reference path; it is not blanket validation of every upstream dataset or release claim.
