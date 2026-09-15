# Notation and empirical targets

| Symbol | Meaning |
|---|---|
| $O$ | Current acquired history; no future or reference targets as inference input |
| $a$ or random $A$ | Deployment-available rate, duration, mask/channel information; not a dataset-name shortcut |
| $F=HSE_0(O,a_{enc})$, $M_F$ | Frozen HSE features and explicit valid-history mask |
| $C_F=(F,M_F,a)$ | Complete input actually used by the conditioner |
| $Z_0=E_{ref}(X_{ref})$ | Frozen reference-latent target, not an identified physical coefficient vector |
| $U=L\operatorname{vec}(Z_0)$ | Source-declared target functional for moment supervision |
| $R=g_\theta(C_F)\in\mathbb R^q$ | Complete statistically supervised ordinary code |
| $M=T_\psi(R)\in\mathbb R^q$ | Statistical-prefix message and retained ordinary tail |
| $\rho_j^d(a)$ | Population loss of a fixed trained arm under evaluation law $d$, conditional on acquisition $a$ |
| $\widehat\rho_j^s(a)$ | Source-validation estimate, not a population guarantee |
| $\pi(a)$ | Declared acquisition weighting; balanced and prevalence-weighted targets differ |
| $\Gamma(a)$ | Nonnegative Bayes information penalty of M relative to R for the common squared target |
| $\mathcal E_j(a)$ | Actual finite predictor excess relative to its own conditional expectation |
| $\mathcal H_{hard}$ | Best-global versus conditionwise-hard-selector risk gap; not a soft-fusion bound |
| $\epsilon(a),b(a)$ | Assumed source estimation error and source–target conditional shift bound |

For additive scores, the paper target averages windows inside each original recording, matched seeds inside the recording, then recordings equally. Uncertainty from resampling recordings is conditional on the evaluated training seeds; it does not estimate all optimizer randomness.

For classification, **do not average window F1 or single-class recording F1**. Use a pooled confusion matrix with each original recording carrying total weight one, then calculate macro-F1 over the fixed complete label ontology. Retain the framework's unweighted pooled-window accuracy/F1 separately for exact reproduction. Group bootstrap must recompute the nonlinear metric from predictions. MFPT currently has six test files: this establishes file separation, not unseen physical bearings or six independent machines.

The nested-message proof assumes the acquisition variable is included in the conditioning information and a fixed common square-integrable target. The routing loss and the final macro-F1 are different quantities. All checkpoint/normalization/static-weight/gate choices use source groups only. No result asserts conditional transportability on an unseen acquisition without an explicit assumption and a held-out evaluation.
