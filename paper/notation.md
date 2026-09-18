# Notation for source-supported industrial posterior inference

| Symbol | Meaning and scope |
|---|---|
| e, i | Dataset/acquisition domain and independent event/original recording; different datasets are not assumed paired events |
| Y, u | Fault ontology and operating condition, kept distinct from acquisition descriptors |
| Psi_e, A_e | Mechanical response map and acquisition operator; the known linear oracle absorbs a fixed dictionary into A_e |
| H | Finite source-reference latent space with a declared inner product and cross-source coordinate meaning |
| O_e=range(A_e^T) | Structurally observable subspace, not the set of coordinates with positive diagonal sensitivity |
| U_s, C_s | Sum and intersection of the source observable subspaces |
| C_e=C_s intersection O_e | Source-common information actually observable in the current acquisition; may shrink on a target |
| P_e=O_e intersection C_e^perp | Observed-private subspace relative to the source-common component |
| M_e=U_s intersection O_e^perp | Currently missing but source-supported subspace |
| N_0=U_s^perp | Source-global-null subspace; invisible to declared source likelihood, not necessarily independent under a prior |
| I_e subset M_e; G_e | Joint-conditionally identified eligible target and its fixed orthogonal projector |
| C_F; C_T | Full current-acquisition encoder-visible record and the complete compact condition actually consumed by the generator |
| R, H_A, H_M | Existing ordinary, same-head affine and conditional-moment messages; conditioner ablations |
| z_o,z_m | Observed-subspace latent and eligible missing latent in a coherent posterior draw; observed measurements remain noisy |
| alpha_tau,sigma_tau | Gaussian forward-diffusion coefficients, separate from physical time t |
| rho_k,omega_k | Damping in inverse seconds and angular frequency in radians/second in the Laplace-modal temporal parameterization |
| q_o,q_theta | Observed-latent uncertainty model and conditional posterior over admitted missing coordinates |

The four-role decomposition assumes O_e subset U_s. An unseen acquisition with genuine new support needs an extended formulation; newly measured values are not rejected as invented source recovery. Non-diagonal operators generally require subspace projectors rather than coordinate masks. A reference VAE alone does not identify mechanical modal coordinates.

Physical time is seconds; displayed frequency is Hz=omega/(2*pi). Sampling rate, bandwidth and window duration are distinct. Finite-window damped signals need a measured filter-response/leakage analysis before claiming exact band-null support.

Primary industrial effect is a dataset-macro difference of per-target recording-balanced pooled-confusion macro-F1, supplemented by balanced accuracy. Each original group has equal total weight inside a target; F1 is calculated after pooling the weighted confusion matrix over the fixed ontology, not averaged per window. Source identification, latent posterior scoring and unseen-dataset diagnosis are separately reported. Posterior sample count and optimization seeds do not increase the number of independent target datasets or recordings.

A zero internal projected coordinate means no update, not a public estimate of zero with no uncertainty. Unsupported/ineligible recovery outputs are omitted or marked unestimated. Report admitted support coverage and diagnostic utility with rejection rates, so rejecting everything is not treated as success.
