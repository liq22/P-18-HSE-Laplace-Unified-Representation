# HSE–Laplace Unified Representation

## Working title

**Observable-Support-Conditioned Laplace Stochastic Transport for Unified Heterogeneous Time-Series Representation**

## Central question

How can observations produced by different sampling rates, sensor responses, channel sets, timestamps, and missingness patterns be represented in a common physical space when those observations contain only partially overlapping information?

## Central claim under test

A heterogeneous observation should not be forced into a fully domain-invariant point embedding. In a stable Laplace-modal coordinate system, the representation should be split by effective observability:

\[
\mathcal H
=
\mathcal H_c
\oplus
\mathcal H_{p,d}
\oplus
\mathcal H_{u,d}.
\]

The method then applies:

\[
\begin{aligned}
\mathcal H_c &: \text{source-only canonical flow},\\
\mathcal H_{p,d} &: \text{identity},\\
\mathcal H_{u,d} &: \text{conditional diffusion posterior}.
\end{aligned}
\]

The ideal output is a conditional probability measure, not only a deterministic vector.

## Introduction argument

1. Heterogeneous acquisition changes what is observable, not merely the marginal data distribution.
2. Complete alignment can delete high-support information that has conditional task value.
3. Existing irregular-time diffusion supplies uncertainty and stable latent trajectories, but it does not assign different stochastic dynamics according to physical observability.
4. Flow matching supplies efficient probability transport, but unconstrained marginal transport does not protect private information or guarantee semantic alignment.
5. We define one observability-conditioned Laplace stochastic transport representation in which flow, identity, and diffusion have non-overlapping scientific roles.

## Method overview

```text
heterogeneous observation O_d
        ↓
HSE observation operator / effective Gramian
        ↓
shared | observed-private | unobserved modal coordinates
        ↓
flow    | identity         | diffusion posterior
        ↓
distribution-valued unified representation μ_d^U
        ↓
query-time synthesis or downstream task
```

## Theoretical contribution map

| Claim | Proof file |
|---|---|
| The three observable blocks form a unique direct sum | `theory/01_observable_subspace_decomposition.md` |
| The distribution-valued representation exists | `theory/02_constructive_existence.md` |
| Flow and compensated diffusion can share a marginal path | `theory/03_diffusion_flow_marginal_equivalence.md` |
| Observed-private information is pathwise invariant | `theory/04_observed_private_invariance.md` |
| Complete paired invariance has a task-risk lower bound | `theory/05_global_invariance_risk_lower_bound.md` |
| The exact latent posterior is sufficient for downstream decisions | `theory/06_posterior_representation_sufficiency.md` |
| Stable modal coordinates have explicit decay and forced bounds | `theory/07_laplace_modal_stability.md` |
| Shared estimation error follows observability and operator error | `theory/08_shared_estimation_perturbation_bound.md` |
| Approximation errors yield an additive risk bound | `theory/09_unified_representation_risk_bound.md` |
| Sampling-gap shift perturbs effective poles in a controlled way | `theory/10_sampling_gap_shift_bound.md` |
| Private identity is optimal under an explicit product OT model | `theory/11_private_preserving_optimal_transport.md` |
| Independent shared and unobserved generators commute | `theory/12_commuting_block_generators.md` |
| Identifiability failures are explicit | `theory/13_identifiability_and_failure_boundaries.md` |

## Contributions that may survive review

1. **Observable modal decomposition.** A representation contract that distinguishes common observable, observed-private, and unobserved physical modes using acquisition-conditioned observability.
2. **Blockwise stochastic transport.** A single representation operator that canonicalizes common modes by flow, keeps observed-private modes unchanged, and models unobserved modes by a calibrated diffusion posterior.
3. **Theory tied to diagnostics.** Direct-sum existence, risk of complete invariance, posterior sufficiency, private invariance, stable modal dynamics, gap-shift bounds, and explicit failure cases.

These are candidate contributions. They remain unsupported as empirical claims until the experiments in `paper/experiments.md` are completed.

## Strongest competing explanations

- Sampling-rate or sensor metadata conditioning is sufficient; no support decomposition is needed.
- A generic latent diffusion already models uncertainty without a physical modal representation.
- Ordinary optimal transport or CORAL canonicalizes shared information as well as flow matching.
- The apparent private advantage is dataset or sensor identity rather than fault information.
- A local finite Laplace dictionary is too restrictive for switching and non-stationary PHM signals.

## Current evidence boundary

```text
proved: mathematical implications under explicit assumptions
executed: deterministic analytic semantic tests
not executed: learned model training
not executed: real paired-rate PHM experiment
not supported: SOTA, diagnosis improvement, universal identifiability
```
