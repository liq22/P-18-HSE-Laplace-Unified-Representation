# Chapter 2–3 notation

| Symbol | Definition |
|---|---|
| d, i, a; e=(d,a) | Dataset, original recording, acquisition configuration; an acquisition regime is not itself an independent target dataset. |
| z_di, u_di | Source-reference state and operating condition; unrelated datasets do not share an event index. |
| A_e, O_e, U_s, C_s | Calibrated linear acquisition, its row space, source-space sum and intersection. |
| C_e, P_e, M_e, N_0 | Four source-relative geometric roles under O_e subset U_s, Eq.2. |
| C_F, C_T | Complete visible record and deterministic compressed generative condition, including all actual side inputs. |
| I_e, B_e, G_e | Jointly identified missing target, orthonormal basis and fixed projector B_e B_e^T. |
| P_o,e, z_o, w_0 | Observed-space projector, observed reference state and intrinsic missing-target coordinates. |
| t; k,s | Physical query time in seconds; diffusion noise indices (s<k in reverse). |
| alpha_k, sigma_k, v_k | Forward signal/noise coefficients and velocity target, Eq.3. |
| rho_j, omega_j | Modal damping and angular frequency; not a diffusion noise distribution. |
| R, H_R, H_A, H_M | Fixed observed code and conditioner alternatives, Eq.8. |
| q_o, q_theta, h_psi | Source observed-state readout, conditional missing sampler and fixed diagnostic readout. |
| X, iota=(r,l,c), tau | Fixed experimental conditions, inference intervention and fitting/sampling trajectory, Eq.4. |
| S_rle, Delta_r, Delta_int | Recording-balanced diagnostic outcome and separately evaluated factorial effects, Eq.5. |
| L, n_e | Posterior draw count and number of admitted scalar targets. |
| $P_s^{\rm ref}$ | Source joint reference law induced by fixed mixture weights, the reference map and acquisition design; posterior approximation is relative to this law. |
| $Q_e$ | Orthonormal basis of one jointly justified source block; it is not constructed by union of marginal visibility. |
| $\mu_s,\mu_t;\Omega$ | Source/target condition laws and declared transport region. Overlap and equal conditionals are distinct assumptions. |

The observed state is sampled in its intrinsic subspace coordinates; a Gaussian readout is not assumed to have a nonsingular density on the full ambient space. The source target may be a noisy reference feature. Physical recovery terminology requires a calibrated state/observation relationship. Classifier accuracy, posterior accuracy, support compliance and resource cost are separate outcomes.

“Laplace-structured” refers to the physical-time branch. The noise remains Gaussian; the original model's name LLapDiff is retained as its citation. The fitted conditional latent distribution is not automatically a calibrated physical-state posterior.
