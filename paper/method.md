# Industrial method

## 1. Acquisition and frozen targets

Use only accepted PHMFactory industrial data and original-recording splits. Let $F=HSE_0(O,a_{enc})$, $Z_0=E_{ref}(X_{ref})$, and $U=L\operatorname{vec}(Z_0)$. Freeze source-trained HSE and reference encoders. The actual input is $C_F=(F,M_F,a)$ with named side columns, observation mask, units, source-only normalization and deterministic evaluation patches. A reference view supplies supervision, not an extra undeclared inference input.

## 2. Shared statistical supervision

A trainable trunk outputs $R=g_\theta(C_F)\in\mathbb R^q$. One global head on this same code yields $m_\psi(R)$ and $S_\psi(R)=B_\psi(R)B_\psi(R)^\top+\lambda I$. The covariance floor is a declared model constraint in source-standardized units. Train with

$$
\mathcal L_G=\tfrac12\mathbb E_s[\log\det S_\psi(R)+(U-m_\psi(R))^\top S_\psi(R)^{-1}(U-m_\psi(R))].
$$

Auxiliary gradients must change the trunk subsequently consumed by B1-aux; a separate unrelated head is not this control. Select one source-validation checkpoint and freeze HSE, preprocessing, buffers, trunk and head together. Log score, log-determinant, Mahalanobis term and covariance eigenvalues separately. The score's population moment interpretation is conditional on its actual input/function class and does not establish finite optimizer success or unseen-acquisition calibration.

## 3. Equal-size messages and actual consumption

With $d=\dim U$ and $s=d+d(d+1)/2<q$, send

$$
H_R=R,\qquad H_M=[m_\psi(R),\operatorname{vech}(\operatorname{chol}S_\psi(R)),R_{s+1:q}].
$$

The two arms share checkpoint and q. Outputs are dense global summary tokens with an explicitly all-valid output mask; they are not patch-local posterior copies. The input mask is consumed upstream. Check statistical semantics at the raw readout and verify prefix/tail perturbations change the native output. A downstream learned projection need not preserve the raw units. No repeated unpriced statistics bypass the message budget.

## 4. Native model and diagnostic head

Keep the same native LLapDiff target, prediction parameterization, query grid, mask reduction, schedule, time sampling, weighting, optimizer and update budget. First independently recompute the actual native loss on the same batch/noise; retain any batch denominator. Initial pilot uses the implemented v-prediction,64-step cosine schedule, uniform nonzero times, no weighting and small no-dropout denoiser. These are pilot settings, not optimized industrial results.

For diagnosis, evaluate frozen features using the same linear head and one small MLP capacity control. Keep probabilistic reference-latent scores separate from fault-label metrics. All source/model choices precede test acquisition evaluation.

## 5. Industrial comparisons

B1 controls ordinary HSE without added statistical training; B1-aux is the strongest same-supervision ordinary code; M is the candidate message. Compare source-selected best single and constant predictive fusion before an optional acquisition-conditioned selector. Probability fusion mixes normalized probabilities or predictive distributions with a declared total draw count, not arbitrary latent averages. Charge both-arm computation. These are industrial ablations; general multi-domain policy selection and its proofs are in `../paper_TPAMI/` and are not separate TII inventions.

## 6. Industrial evidence and cost

PHMFactory alone prepares raw data, labels and initial splits. Retain original File/run/bearing keys as available, without inventing physical independence. Derive paired acquisition views after the split. Rate/missingness/channel factors differ from speed/load/machine shifts.

Primary diagnosis metric is recording-balanced pooled-confusion macro-F1 over the fixed ontology; conventional pooled-window metrics are retained for framework reproduction. For additive probabilistic scores average windows and matched seeds within each recording before equal-recording aggregation. Nonlinear F1 must be recomputed from pooled weighted confusion, not averaged by window.

Report HSE/trunk/moment/denoiser/diagnosis/gate parameters, auxiliary training and actual inference costs. Equal q is not equal total work. TII uses industrial data only; existing mathematical simulations are supporting checks, not extra empirical datasets. No paper/P19 code imports PHMFactory core; the isolated revision-specific acceptance script restores the unchanged upstream reference and exports its own dataset only.
