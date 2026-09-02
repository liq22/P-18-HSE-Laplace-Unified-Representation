# Theory map

The theory corpus separates mathematical implications from empirical hypotheses.
Every derivation used by the core idea has one dedicated Markdown file.

Terminology note: files `00`–`13` may use **recoverable-missing** as shorthand
for membership in the source-observable union. Theory 16 is authoritative:
source support gives eligibility for conditional inference, not statistical
identifiability. The preferred term is **source-supported missing** until a
paired or physical identifiability certificate is established.

## Core representation results

| File | Result | Manuscript role |
|---|---|---|
| `00_axioms_and_notation.md` | Mathematical universe, units and non-claims | Definitions |
| `01_observable_subspace_decomposition.md` | Four-way support decomposition | Main theorem |
| `02_constructive_existence.md` | Existence of the source-supported representation | Supporting theorem |
| `04_observed_private_invariance.md` | Pathwise identity of observed-private modes | Method property |
| `05_global_invariance_risk_lower_bound.md` | Cost of forcing complete invariance | Main theorem |
| `09_unified_representation_risk_bound.md` | Same-event approximation-to-risk bound | Main theorem |

## Observability and identifiability results

| File | Result |
|---|---|
| `14_structural_observability_and_instance_reliability.md` | Structural role is fixed by the acquisition design; instance reliability changes information precision |
| `15_soft_observability_and_slot_stability.md` | Smooth slot weights converge to hard support and obey a perturbation bound |
| `16_source_supported_missing_identifiability.md` | Source support is necessary but not sufficient for identifying a missing conditional |
| `17_global_null_nonrecoverability.md` | Source-global-null coordinates have zero direct source likelihood information |
| `21_support_projector_perturbation_bound.md` | Spectral-gap control of estimated support projectors |

## Canonical transport results

| File | Result |
|---|---|
| `18_population_and_eventwise_canonicality.md` | Population marginal canonicality and paired eventwise canonicality are distinct |
| `19_semantic_anchor_necessity.md` | Marginal alignment can reverse semantics; a sufficient semantic statistic must be preserved |
| `20_triangular_stochastic_transport.md` | Flow, identity and conditional posterior form one well-defined triangular kernel |
| `11_private_preserving_optimal_transport.md` | Private identity is OT-optimal only in the stated product special case |
| `12_commuting_block_generators.md` | Commutation holds only for the decoupled null model |

## Model-necessity and physical-scope results

| File | Result |
|---|---|
| `22_diffusion_necessity_under_proper_scores.md` | Diffusion has no population proper-score advantage when a simpler family contains the true conditional |
| `23_flow_necessity_under_affine_distortion.md` | A learned nonlinear flow is unnecessary when an affine canonicalizer is exact |
| `24_window_local_laplace_adequacy.md` | Modal residual propagates through acquisition and representation with explicit bounds |
| `03_diffusion_flow_marginal_equivalence.md` | Background equivalence of prescribed marginal paths |
| `06_posterior_representation_sufficiency.md` | Exact posterior-valued representation is task sufficient under the Markov condition |
| `07_laplace_modal_stability.md` | Stable local modal dynamics |
| `08_shared_estimation_perturbation_bound.md` | Noise-weighted shared-state estimation bound |
| `10_sampling_gap_shift_bound.md` | Sampling-gap distribution perturbation |
| `13_identifiability_and_failure_boundaries.md` | Counterexample catalogue |

## Reading order

For the core paper, read:

```text
00 -> 01 -> 05 -> 16 -> 18 -> 19 -> 20 -> 09
```

Then use:

```text
22 -> 23 -> 24
```

to decide whether Diffusion, Flow and Laplace coordinates are empirically necessary.

A theorem proves only the implication written under its assumptions. It does not
promote an empirical claim.
