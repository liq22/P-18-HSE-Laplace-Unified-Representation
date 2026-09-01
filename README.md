# HSE–Laplace Unified Representation

This repository studies one question:

> How can heterogeneous time-series observations be represented in a common physical space when their observable information only partially overlaps?

The proposed representation acts differently on three observable subspaces:

```text
common observable modes     -> flow-based canonical coordinates
observed private modes      -> identity preservation
unobserved private modes    -> diffusion posterior
```

The common state is a stable Laplace-modal representation. Diffusion and flow are therefore not two stacked models. They are two blocks of one observability-conditioned stochastic transport operator.

## Current status

```text
stage: theory contract + analytic prototype
formal_claim_supported: false
evidence: mathematical derivations and deterministic semantic tests
real PHM evidence: not started
```

The repository does not yet claim improved diagnosis, forecasting, imputation, or domain generalization.

## Mathematical object

For acquisition domain `d`, the modal space is decomposed as

\[
\mathcal H
=
\mathcal H_c
\oplus
\mathcal H_{p,d}
\oplus
\mathcal H_{u,d}.
\]

The unified representation is distribution-valued:

\[
\mu_d^U
=
\operatorname{Law}
\left(
T_d\Theta_c,
\Theta_{p,d},
\Theta_{u,d}\mid\mathcal O_d
\right),
\]

where `T_d` transports common observable modes to source-only canonical coordinates, observed private modes are unchanged, and unobserved modes remain a conditional posterior rather than a fabricated point estimate.

## Start here

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e .
python examples/analytic_unified_representation.py
python -m unittest discover -s tests -v
```

## Repository map

| Path | Purpose |
|---|---|
| `src/hse_laplace/` | Minimal mathematical implementation |
| `theory/` | One theorem or theory analysis per Markdown file |
| `tests/` | Tests of scientific invariants, not coverage targets |
| `examples/` | Deterministic analytic prototype |
| `paper/` | Single manuscript authority and experiment design |
| `literature/` | Closest prior work and reproducible download list |

## Theory index

1. [`00_axioms_and_notation.md`](theory/00_axioms_and_notation.md)
2. [`01_observable_subspace_decomposition.md`](theory/01_observable_subspace_decomposition.md)
3. [`02_constructive_existence.md`](theory/02_constructive_existence.md)
4. [`03_diffusion_flow_marginal_equivalence.md`](theory/03_diffusion_flow_marginal_equivalence.md)
5. [`04_observed_private_invariance.md`](theory/04_observed_private_invariance.md)
6. [`05_global_invariance_risk_lower_bound.md`](theory/05_global_invariance_risk_lower_bound.md)
7. [`06_posterior_representation_sufficiency.md`](theory/06_posterior_representation_sufficiency.md)
8. [`07_laplace_modal_stability.md`](theory/07_laplace_modal_stability.md)
9. [`08_shared_estimation_perturbation_bound.md`](theory/08_shared_estimation_perturbation_bound.md)
10. [`09_unified_representation_risk_bound.md`](theory/09_unified_representation_risk_bound.md)
11. [`10_sampling_gap_shift_bound.md`](theory/10_sampling_gap_shift_bound.md)
12. [`11_private_preserving_optimal_transport.md`](theory/11_private_preserving_optimal_transport.md)
13. [`12_commuting_block_generators.md`](theory/12_commuting_block_generators.md)
14. [`13_identifiability_and_failure_boundaries.md`](theory/13_identifiability_and_failure_boundaries.md)

Each proof states its assumptions, lemmas, theorem, derivation, failure boundary, and measurable experimental consequence. A result is valid only under the assumptions written in its own document.

## Research order

```text
1. freeze observable decomposition and stable modal chart
2. verify analytic flow–diffusion representation
3. build a known-pole paired-acquisition falsification experiment
4. learn the unobserved-mode posterior
5. test source-only shared canonical transport
6. enter recording-level paired-rate PHM experiments
```

Do not add event routers, codebooks, learned poles, or foundation-model pretraining before the known-pole experiment distinguishes this representation from simpler metadata-conditioned baselines.
