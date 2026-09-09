# Theory 0 — Problem, targets, and actual conditioning information

## Status

Definitions and assumptions; no empirical or novelty claim. [Theory 1](01_hse_fixed_dimensional_sufficiency.md) concerns a known linear acquisition, not the learned HSE.

## 1. Keep three different objects separate

**Known-pole oracle.** Freeze a window-local dictionary

\[
\Lambda=\{(\rho_r,\omega_r)\}_{r=1}^{R_{\rm mode}},\qquad
s(t)=\Phi_\Lambda(t)\beta.
\]

The unknown is the coefficient vector `beta in R^m`. An oscillatory mode normally needs two coefficients, cosine and sine; `m=2 R_mode` in that convention. Existing oracle code and earlier theory use `Theta` for this coefficient vector. That notation does not include unknown poles. One scalar oracle token is not automatically one physical oscillatory mode or one original HSE patch.

**Learned target.** Freeze a source-trained reference encoder and define

\[
Z_0=E_{\rm ref}(X_{\rm ref}).
\]

This is a reference latent trajectory. It is not assumed equal or invertibly related to `beta`. If the reference contains noise, the learned conditional concerns that reference latent, not automatically a noise-free physical state. Source validation must check target information retention.

**Denoiser parameters.** LLapDiff's predicted poles and residues parameterize its clean-latent prediction at a diffusion step. They are not automatically identifiable physical coefficients. The linear oracle cannot be applied to those learned parameters without a separate observation model.

## 2. Heterogeneous observation and units

For fixed known `Lambda`, the analytic acquisition is

\[
X_d=A_d\beta+\epsilon_d,\qquad
\epsilon_d\sim\mathcal N(0,R_d),\quad R_d\succ0.
\]

`A_d` includes declared sensor/filter responses, observed timestamps, channel selection and mask. Its row count can vary. It must be constructed without reading the hidden coefficient being inferred. Informative sampling or state-dependent noise needs a different likelihood.

Units: physical time in seconds, damping `rho` in inverse seconds, angular frequency `omega` in rad/s, and displayed/token bands in Hz (`f=omega/(2 pi)`). A finite-window damped sinusoid is not exactly bandlimited. Ideal modal zero sensitivity and real filtering suppression are distinct experiments.

## 3. The actual decoder condition

Let `O` be the complete encoder-visible record for the **current acquisition**, including its observed values and any acquisition information available to that encoder. Let `a` denote side information actually supplied to and consumed by the denoiser. Define

\[
H=T_\psi(O,a),\qquad C=(H,a).
\]

`H` includes all exposed token/mask/time/band/reliability fields and any auxiliary condition stream. Encoder-only metadata stays inside `O`; it does not silently appear in `a` in a proof. A field on a Python object is not decoder information unless the forward path consumes it.

The analytic function `information_tokens_from_diagonal` exposes `b` and diagonal `J`, plus physical metadata. The present oracle's full Gaussian posterior uses the original `(b,J)` separately. It is not a reconstruction of the posterior from these diagonal tokens.

Two explicit diagnostic regimes are needed:

- coarse `a`: it does not reconstruct off-diagonal `J`; collisions may occur;
- full `a=(A,R)`: it reconstructs `J`; diagonal tokens retaining `b` can then be sufficient.

Every within-regime comparison gives the same `a` to all methods. These are diagnostic contracts, not a claim that the future decoder already implements either regime.

## 4. Assumptions and evidence boundaries

**A1, same event.** Split latent events before constructing acquisition views. Matching classes is not pairing. A deterministic low-rate transform of a noisy high-rate recording is not a new independent measurement; joint inference needs the correct coupled noise law.

**A2, known oracle acquisition.** `A,R,Lambda` are known and noise is independent of the hidden coefficients given the declared design. Unknown poles or estimated operators require an approximation analysis.

**A3, valid Gaussian special case.** The prior `N(mu0,Sigma0)` has `Sigma0` positive definite. Gaussian noise enables likelihood factorization; the Gaussian prior enables the closed-form Gaussian posterior. The two assumptions play different roles.

**A4, fixed actual condition.** `H=T(O,a)` is a deterministic measurable map for evaluation. Trained parameters are held fixed. Random patch selection must be frozen or its seed explicitly included. Masks that hide retained fields must be included in the information audit.

**A5, identifiable target conditional.** Paired source data, a simulator or a declared physical coupling is needed. Unpaired marginals do not determine a missing conditional; source identification alone does not establish target transportability.

**A6, task sufficiency.** When a task theorem uses a Markov assumption, state `Y` conditionally independent of `O` given the chosen target explicitly. Do not transfer sufficiency from `beta` to `Z0` without checking this assumption.

**A7, diffusion perturbation.** The forward noise is independent of `(Z0,O,a)` and the same schedule and regression target are used in every conditioning comparison. See Theory 10 for epsilon, x0 and v.

## 5. Fixed interface and scope

The intended learned HSE retains its declared patch/token budget `(P,K,D)` and does not receive hidden target values. The current scalar information-token oracle is a diagnostic, not a learned HSE implementation. Neither fixed shape nor nominal sampling rate proves posterior sufficiency or calibration.

Flow Matching remains future work. The active question is whether a minimal acquisition-information condition improves the **same LLapDiff**. No theorem here establishes real PHM performance or forces Diffusion to outperform Gaussian/mixture models.
