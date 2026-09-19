# TII execution entry

The paper studies jointly source-qualified partial latent inference for source-only cross-dataset industrial diagnosis. Chapter 2 defines the source reference law, eligibility/transport boundary and intervention estimands; Chapter 3 specifies HSE conditioning, target-intrinsic Gaussian diffusion, the inherited Laplace physical-time branch, restricted reverse updates and diagnostic integration.

```bash
bash paper/build_frontmatter.sh outputs/tii_support
```

This builds Chapters 1–3, regenerates the two editable figures and replays the retained finite witnesses. Those checks are analytical/interface evidence, not learned industrial performance.

## Repository boundary

The paper repository owns manuscript/theory/basic witnesses and experiment-to-claim mapping. `external/phmfactory` owns the learned P18 model, data/config integration, training, evaluation and experiment artifacts. Do not add a second reader/trainer/runtime to the paper repository. The parent gitlink advances only after the exact child PHMFactory commit has passed its paper-specific acceptance.

## Current evidence

The intrinsic native functions and one real MFPT DCT-reference source batch already demonstrate the basic loss/update/sampling path. That batch uses reference features, all missing coordinates are admitted, observed uncertainty is a point mass, and it does not provide learned HSE, nontrivial qualification, restriction benefit, calibration or LODO evidence. Preserve this as implementation evidence; do not rerun it as a substitute for the full study.

## Next execution gates

Follow `paper/goals/` in this order:

```text
Gate 0 — prove the scientific task exists in the local industrial data
Gate 1 — implement/finalize the learned path in PHMFactory and run one real source batch
Gate 2 — one LODO target × one seed × all decisive cells
Gate 3 — freeze the protocol, then run qualified folds × preregistered seeds
Finish — recompute statistics/cost/figures and only then update Results/contributions
```

Gate 0 must explicitly distinguish reference origin, pairing, joint evidence, nontrivial eligible/ineligible targets, target truth, observed uncertainty and independent statistical units. File availability alone is not qualification.

Gate 1 must use the maintained PHMFactory Data/Model/Task/Trainer path, a shared source-trained LODO ontology/readout, true HSE deployment inputs and the actual native LLapDiff implementation. The paper-side DCT batch remains a witness, not the learned method implementation.

Gate 2 is the last technical screen. Do not redesign the method from its target score. Gate 3 uses frozen configs and registered seeds. One run uses one GPU; independent jobs may be parallelized across the local 8×4090 machine after Gate 2, but no two-GPU/DDP run is allowed.

## Decisive experiment set

- **E1 net diagnostic value:** complete `S-L` versus the strongest source-selected observed-only method, with deterministic/Gaussian/S-T and one protocol-compatible external conditional-diffusion reference.
- **E2 support process × physical-time structure:** A-T/A-L/S-T/S-L plus an ambient-clamped equivalence control; report support, Laplace and interaction effects separately.
- **E3 conditioner/dependence:** R_aux/H_A/H_M/same-budget MLP and conditional-paired versus marginal-repaired draws where the data support that claim.
- **E4 qualification/acquisition boundary:** qualified/geometry/wrong/empty together with coverage-risk-utility, and regular/irregular/long-gap/band-loss controls with Laplace versus Fourier/time-MLP.

Use original-group outcomes; target labels/reference never enter fitting or selection. Report posterior score, diagnosis, coverage/support compliance and cost separately. Three target datasets remain three environments regardless of seed count.

## Stop rule

Do not write Results or performance claims until real artifacts exist. Equal, worse or inapplicable outcomes are completed scientific findings. Preserve prior negative results and narrow/remove a contribution when its registered contrast does not support it.
