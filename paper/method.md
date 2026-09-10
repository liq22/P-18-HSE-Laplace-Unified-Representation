# Method: target-aware posterior conditioning

## 1. Declared target, observations and budget

The known-pole oracle is `x=A beta+epsilon`, with fixed dictionary, known SPD noise R and declared Gaussian prior. It is not the learned LLapDiff target. The latter is `Z0=E_ref(X_ref)` from one source-trained frozen reference encoder. A teacher used to assess condition compression receives the same current observation O and actual side input a as its comparators; a high-rate reference is common supervision, not privileged teacher input.

All conditions include every field actually consumed downstream: tokens, attention mask, timestamp/band/reliability fields and a. Count encoded scalars, layout identifiers, precision in bits, encoder computation, decoder computation and cache state separately. Fixed P,K,D is an additional neural-interface constraint, not established by a scalar-count oracle.

The primary contract is single-window inference with a fixed prior and target. Streaming updates and prior reuse are secondary contracts; they cannot be introduced after seeing a precision-header loss merely to rescue that header.

## 2. Select posterior parameterization before layout

Write `b=A^T R^-1 x`, `J=A^T R^-1 A`, `Q=S0^-1+J`, `h=S0^-1 mu0+b`, `S=Q^-1`, `mu=Sh`.

For a fixed partition g and a block-diagonal prior in that partition, compare:

| Condition | Decoded posterior | Primary purpose |
|---|---|---|
| full | N(mu,S) | Upper-information reference |
| natural blocks | N(Qg^-1 h,Qg^-1), Qg=S0^-1+B_g(J) | Prior-reusable likelihood approximation |
| mean + precision blocks | N(mu,Qg^-1) | Isolate approximate-mean cost |
| marginal moment blocks | N(mu,B_g(S)) | Forward-KL optimal product control |
| modal trace-isotropic | N((S0^-1+I(J))^-1 h,(S0^-1+I(J))^-1) | Cheap phase-covariant control |
| prior-aware low rank | Full mean + prior-whitened negative covariance update | Direct Spantini-family control |

The block-moment control dominates any product approximation at that partition in forward KL. It needs encoder-side posterior computation, which must be charged; no learned HSE is presumed to compute it for free. Truncated precision generally underestimates true marginal covariance by the Schur-complement relation. Report mean displacement, marginal uncertainty and joint dependence loss separately.

The actual current four-coefficient adaptive headers use 11 scalars including layout. The review's six-coefficient fixed `4+2` grouping uses 19 statistics; no layout value is sent only because all arms share it in advance. Do not mix these budgets in one performance claim.

## 3. Target-space analysis

For the analytical target `Z0=L beta`, project every candidate's moments through the same L before calculating posterior KL or denoising discrepancy. Theory 12 gives the exact Gaussian epsilon-predictor discrepancy under the true noisy target. The result depends on the schedule and target covariance; a better whole-beta KL does not guarantee a better Z0 or v-prediction objective.

A goal-only oracle transmits the target moments directly. When the target has low dimension, this can be cheaper than any full-state header. It is a strong target-specific baseline, not a unified representation of all possible future tasks. The goal-oriented low-rank baseline uses the target prior and posterior covariances, as in the family studied by Spantini et al. (2017). The dense diagnostic is not a claimed reproduction of their matrix-free algorithm.

## 4. Candidate learned HSE intervention

The candidate is an **amortized target-calibrated posterior feature inside the existing HSE budget**, not a new denoiser. Freeze one reference encoder and the target grid. Reuse the actual HSE patch extractor; reserve a declared portion of each D-dimensional token for target-relevant mean and covariance-factor features, rather than append an uncounted stream. A neural covariance block is parameterized by a triangular factor with positive diagonal. This ensures validity, not calibration.

Compare the original HSE, explicit natural/coupling features and predicted moment features with the same P,K,D, common acquisition description, denoiser architecture and tuning budget. Any teacher or distillation supervision must be shared across matched controls. Start with the native LLapDiff loss only; add a distillation term only after the teacher posterior and its access to data are validated. An observation-residual penalty can alter the target posterior and is not added by default.

For variance-preserving v prediction,

\[
v=\alpha_\tau\epsilon-\sigma_\tau Z_0,
\qquad \mathcal L=E\|v-v_\theta(Z_\tau,\tau,H_\psi(O,a),a)\|^2.
\]

The proposed learned features are not implemented or validated by the Gaussian controls. Before training, verify forward consumption of every field, conditioner gradients, deterministic evaluation patches and 1/2/3-channel shape semantics. Physical coordinates and latent coordinates remain distinct.

## 5. Information-limited versus compute-limited interpretation

If a is coarse, prove an actual same-condition collision or quantify the induced conditional KL before calling a gain information recovery. If a reconstructs A,R and b is retained, complete Gaussian information is already available. Any benefit is then computational accessibility to a finite network. Measure it against a metadata MLP, an explicit solver and a width-matched conditioner; do not use information-loss terminology.

## 6. Physical and software boundaries

Fixed-point and fixed-duration protocols are reported separately. The latter may use more observations at a higher rate and is not a matched-sample-budget experiment. The present modes are below nominal Nyquist: no private-band impossibility result follows from these cells. Small pole/filter misspecification is a required stress test before physical claims.

Paper experiments consume arrays and explicit split/group information. They do not import PHMFactory internals, alter a submodule, use path injection or silently change datasets. A future PHMFactory export must supply waveform, timestamps, valid mask, rate, units, recording group and split; preprocessing fitting uses sources only. Independent acquisition noise and resampled correlated noise have different likelihoods.

Flow Matching remains future work. The active method is admitted only after target-space learned gains over the strongest simple condition under the declared cost contract.
