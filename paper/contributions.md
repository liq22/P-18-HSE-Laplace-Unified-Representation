# Contribution–mechanism–evidence map

## Scientific question

In source-only cross-dataset industrial diagnosis, when does temporal inference of a missing latent component help, once the source design identifies its conditional under the complete observed input? Does support restriction contribute independently of the temporal parameterization, conditioner and additional computation?

| Contribution | Literature-derived gap | New element in this study | Figure / formulation | Algorithm / experiment / metric | Evidence currently available |
|---|---|---|---|---|---|
| C1: conditioning-qualified formulation | Missing-view and corrupted-source learning depend on an identified joint model; a shared view does not identify every conditional with private evidence. | Qualify a source-relative target together with its actual conditioning information. | Fig.1a–b; Method2; Proposition2. | Algorithm1 steps1–2; E4 common-view/joint-acquisition contrast; conditional-law disagreement and admitted coverage. | Analytic three-variable counterexample and executable finite witness; no multi-dataset physical reference calibration. |
| C2: support-restricted temporal inference | Missing-only/null-space diffusion and stable temporal parameterizations already exist; their independent interaction is not established by stacking them. | HSE-conditioned admitted-subspace LLapDiff with observed uncertainty retained. | Fig.1c; Method3–4; Proposition4. | Steps3–5; E2 restriction × dynamics; same-target Energy Score, leakage and cost. | Projector property and existing conditioner components; restricted native learned path remains to implement. |
| C3: mechanism-resolved diagnostic evaluation | A complete-model gain confounds conditioning, generation, temporal structure and consumer effects. | Factorial simple/interaction effects linked to same-head controls and source-only industrial diagnosis. | Fig.1d; Method5. | Step6; E1–E3/E5; per-target macro-F1, balanced accuracy, posterior score and cost separately. | Defined estimands/protocol; no new industrial LODO result. |

The three statements in `main.md` are formulation, proposed mechanism and controlled experimental design, not three empirical findings. Common subspace algebra, conditional-KL identities, generic projection and Laplace dynamics retain their prior status. The new common-view example refines the existing identification boundary; it is not claimed as a new general identifiability theorem.

## Decisions from this revision

Add DiEM and DiffEM as direct corrupted-source/posterior neighbors. Correct FISHER's inspected protocol to frozen features with labelled dataset-specific kNN references. Replace the inference-eligibility shortcut with joint target–condition qualification. Add the crossed restriction–dynamics estimand rather than calling a full-model comparison evidence of interaction. Keep R/head_affine/M as E3 and retain all prior negative results. A Gaussian/mixture/direct classifier or ordinary temporal denoiser matching the proposal narrows the method claim.
