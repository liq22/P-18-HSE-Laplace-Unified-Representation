# Contribution–mechanism–evidence map

## Scientific question

In source-only cross-dataset industrial diagnosis, can an identified partial posterior improve diagnosis, and which effects arise from support restriction, temporal structure and conditioner coordinates?

| Contribution | Formulation / gap | Mechanism and equations | Figure / section / algorithm | Direct contrast and outcome | Current evidence |
|---|---|---|---|---|---|
| C1: conditioning-qualified target | Chapter 2: source support does not identify the full-input conditional; equal pair laws can give opposite p(M given C,P). | Source-reference tuples and joint target qualification, Eq. (6). | Fig.1; Fig.2 qualified target; Section3.2; A1–A2. | E4 joint acquisition/coupling versus unpaired views; conditional disagreement and admitted coverage. | Existing exact counterexample. Real cross-source coordinate calibration remains required. |
| C2: support-restricted temporal inference | Chapter 2: support compliance does not establish the sampled distribution. | Same-head anchor, Eqs. (7)–(8); target-specific velocity loss, Eq. (9); inherited modal branch, Eq. (10); conversion/update, Eqs. (11)–(12); coherent factors, Eq. (13). | Fig.2 HSE, denoiser, conversion/update and observed draw; Sections3.2–3.4; A3–A6. | E2 restriction × dynamics and simple posterior families; E4 post-hoc score restriction and coherent/independent draws; E5 acquisition loss. | Explicit equations and finite velocity/DDIM, score and covariance witnesses. No source-qualified native learned result. |
| C3: mechanism-resolved diagnosis | Chapter 2 Eq. (5): whole-model contrasts couple mechanisms and the downstream consumer. | Fixed source observed readout and diagnostic head, Eq. (14); independently trained observed-only baseline. | Fig.2 output/readout; Section3.4–3.5; A3/A7. | E1 per-target recording-balanced macro-F1; E2 factorial effects at a fixed readout; E3 change the generative conditioner only. Posterior score and cost separate. | Defined estimands and protocol. Industrial LODO/factorial remains unrun. |

## Foundation, adaptation and contribution

**Foundation:** linear observation/orthogonal subspaces, conditional identification, Gaussian diffusion, velocity conversion, DDIM, proper scores and same-information interpretation. HSE and LLapDiff's temporal blocks are inherited, not new backbone inventions. A damping-positive basis does not imply stable generated trajectories.

**Adaptation:** source reference pairing, a moment anchor, intrinsic eligible-coordinate diffusion, shared observed uncertainty and a fixed diagnostic readout instantiate those foundations for the stated industrial problem.

**Proposed contribution:** qualifying the target with its actual condition and coupling that target to restricted temporal inference, with separately identifiable mechanism contrasts. The new Gaussian examples justify target-specific fitting and coherent draws; their algebra is not claimed as new general probability theory. Empirical advantage still requires native industrial evidence.

The original 14 support witnesses and earlier negative results remain intact. The same Notebook adds method_witness.csv rather than replacing old results. Chapters 2 and 3 now separate problem definition from an explicit proposed algorithm. No reference acceptance, theoretical toy or literature count substitutes for learned method validation.
