# Theory proof and executable-witness map

A Markdown file contains the general mathematical argument. Its paired Notebook is a finite executable witness. Passing a witness cannot replace a proof and cannot establish empirical usefulness.

## Admission states

```text
DRAFT
-> proof incomplete or witness absent

WITNESSED
-> proof is stated and the paired Notebook passes

CONTRIBUTION_CANDIDATE
-> WITNESSED and method-specific under the current novelty boundary

EMPIRICALLY_SUPPORTED
-> later known-pole and real-data experiments support the relevant predictions
```

No theory result is currently `EMPIRICALLY_SUPPORTED`.

## One-to-one map

| ID | Formal source | Executable witness | Paper role |
|---:|---|---|---|
| 00 | `00_axioms_and_notation.md` | `notebooks/00_axioms_and_notation.ipynb` | definitions |
| 01 | `01_observable_subspace_decomposition.md` | `notebooks/01_observable_subspace_decomposition.ipynb` | contribution candidate |
| 02 | `02_constructive_existence.md` | `notebooks/02_constructive_existence.ipynb` | supporting theorem |
| 03 | `03_diffusion_flow_marginal_equivalence.md` | `notebooks/03_diffusion_flow_marginal_equivalence.ipynb` | established background |
| 04 | `04_observed_private_invariance.md` | `notebooks/04_observed_private_invariance.ipynb` | method property |
| 05 | `05_global_invariance_risk_lower_bound.md` | `notebooks/05_global_invariance_risk_lower_bound.ipynb` | contribution candidate |
| 06 | `06_posterior_representation_sufficiency.md` | `notebooks/06_posterior_representation_sufficiency.ipynb` | supporting theorem |
| 07 | `07_laplace_modal_stability.md` | `notebooks/07_laplace_modal_stability.ipynb` | established property |
| 08 | `08_shared_estimation_perturbation_bound.md` | `notebooks/08_shared_estimation_perturbation_bound.ipynb` | supporting bound |
| 09 | `09_unified_representation_risk_bound.md` | `notebooks/09_unified_representation_risk_bound.ipynb` | joint contribution candidate |
| 10 | `10_sampling_gap_shift_bound.md` | `notebooks/10_sampling_gap_shift_bound.ipynb` | supporting bound |
| 11 | `11_private_preserving_optimal_transport.md` | `notebooks/11_private_preserving_optimal_transport.ipynb` | product-case special result |
| 12 | `12_commuting_block_generators.md` | `notebooks/12_commuting_block_generators.ipynb` | decoupled null model |
| 13 | `13_identifiability_and_failure_boundaries.md` | `notebooks/13_identifiability_and_failure_boundaries.ipynb` | boundary catalogue |
| 14 | `14_structural_observability_and_instance_reliability.md` | `notebooks/14_structural_observability_and_instance_reliability.ipynb` | supporting distinction |
| 15 | `15_soft_observability_and_slot_stability.md` | `notebooks/15_soft_observability_and_slot_stability.ipynb` | supporting approximation |
| 16 | `16_source_supported_missing_identifiability.md` | `notebooks/16_source_supported_missing_identifiability.ipynb` | contribution candidate |
| 17 | `17_global_null_nonrecoverability.md` | `notebooks/17_global_null_nonrecoverability.ipynb` | method boundary |
| 18 | `18_population_and_eventwise_canonicality.md` | `notebooks/18_population_and_eventwise_canonicality.ipynb` | supporting distinction |
| 19 | `19_semantic_anchor_necessity.md` | `notebooks/19_semantic_anchor_necessity.ipynb` | method boundary |
| 20 | `20_triangular_stochastic_transport.md` | `notebooks/20_triangular_stochastic_transport.ipynb` | joint contribution candidate |
| 21 | `21_support_projector_perturbation_bound.md` | `notebooks/21_support_projector_perturbation_bound.ipynb` | supporting bound |
| 22 | `22_diffusion_necessity_under_proper_scores.md` | `notebooks/22_diffusion_necessity_under_proper_scores.ipynb` | Diffusion complexity gate |
| 23 | `23_flow_necessity_under_affine_distortion.md` | `notebooks/23_flow_necessity_under_affine_distortion.ipynb` | Flow complexity gate |
| 24 | `24_window_local_laplace_adequacy.md` | `notebooks/24_window_local_laplace_adequacy.ipynb` | Laplace complexity gate |

## CI contract

`python theory/run_notebooks.py` enforces:

- every numbered Markdown has exactly one same-stem Notebook;
- no extra numbered Notebook exists;
- Notebook metadata points to the formal source;
- source Notebooks contain no execution counts or stored outputs;
- every clean execution reaches its completion sentinel;
- failures stop the job immediately.

## Contribution candidates after the theory gate

The following are admitted only as **theoretical candidates**, not empirical contributions:

```text
T01
T05
T16
T20 + T09 as one joint construction-and-risk result
```

All remaining results are retained because they delimit assumptions, supply baselines, or prevent overclaiming. Passing their Notebooks does not inflate the contribution count.
