# HSE–Laplace Source-Supported Representation

This repository studies one bounded question:

> How should different acquisition operators represent the same local dynamical
> process when their observable modal supports only partially overlap?

The project does **not** claim a universal representation for arbitrary
heterogeneous time series. The current scope is one physical system family, one
declared local Laplace-modal dictionary, and multiple acquisition operators
such as sampling rates, sensor responses, channel sets and missingness patterns.

## Core idea

A three-block split is insufficient because it mixes recoverable missing
information with information unsupported by every source. The revised
representation uses four structural roles:

```text
common observable modes       -> source-population canonical Flow
observed-private modes        -> exact identity preservation
recoverable-missing modes     -> conditional posterior, optionally Diffusion
source-global-null modes      -> unsupported; no data-driven recovery claim
```

Mathematically,

\[
\mathcal H
=
\mathcal H_c
\oplus
\mathcal H_{p,d}
\oplus
\mathcal H_{m,d}
\oplus
\mathcal H_0.
\]

Here

\[
\mathcal H_c
=
\bigcap_j\mathcal H_j^o,
\qquad
\mathcal H_\cup
=
\sum_j\mathcal H_j^o,
\]

\[
\mathcal H_{p,d}
=
\mathcal H_d^o\cap\mathcal H_c^\perp,
\]

\[
\mathcal H_{m,d}
=
\mathcal H_\cup\cap(\mathcal H_d^o)^\perp,
\]

\[
\mathcal H_0
=
\mathcal H_\cup^\perp.
\]

The source-supported distribution-valued representation is

\[
\mu_d^U(\cdot\mid o)
=
\operatorname{Law}
\left(
T_d\Theta_c,
\Theta_{p,d},
\Theta_{m,d}
\mid
\mathcal O_d=o
\right),
\]

with \(P_0\) returned only as an unsupported-support marker.

## Why Flow and Diffusion have different roles

The candidate final dependency is triangular:

\[
C^*=T_d(C),
\]

\[
P'=P,
\]

\[
M'\sim
q_\theta(M\mid C^*,P,\mathcal O_d).
\]

Flow is considered only when affine calibration, CORAL and ordinary OT cannot
canonicalize the shared modal state. Diffusion is considered only when
Gaussian or mixture posteriors cannot represent the recoverable-missing
conditional. Neither component is included merely because it is a modern
generative model.

## Structural observability versus sample reliability

The acquisition design defines structural modal support. A particular sample
also carries an instance reliability from timestamps, masks, coverage and SNR.

```text
structural observability
-> assigns the scientific role of a modal slot

instance reliability
-> controls confidence or posterior precision for that sample
```

The distinction preserves fixed modal slots and avoids a different latent
dimension for every missingness pattern.

## Current status

```text
stage: corrected theory contract + analytic witness
formal_claim_supported: false
evidence: mathematical derivations and deterministic semantic tests
learned posterior: not started
learned flow: not started
real PHM evidence: not started
```

## Start here

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e .
python examples/analytic_unified_representation.py
python -m unittest discover -s tests -v
```

The analytic witness checks the four-way decomposition, observed-private
identity, global-null exclusion and stable Laplace coordinates. It is not
learned-model evidence.

## Repository map

| Path | Purpose |
|---|---|
| `src/hse_laplace/` | Minimal mathematical implementation |
| `theory/` | One theorem or boundary analysis per Markdown file |
| `tests/` | Behavioral scientific invariants |
| `examples/` | Deterministic analytic witness |
| `paper/` | Manuscript argument, closest-work boundary and experiment plan |
| `literature/` | References and reproducible open-access source list |

## Main theory

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

## Next decisive experiment

The next PR is an oracle known-pole experiment, not a learned architecture:

\[
2\times2\times2
\]

factorial cells for:

```text
full / partial support overlap
×
private task-irrelevant / task-relevant
×
unimodal / multimodal recoverable-missing posterior
```

A source-global-null mode is added as a negative control. The experiment first
asks whether decomposition, identity and probability-valued recovery are
necessary. Learned Diffusion and Flow are blocked until simpler baselines fail.

## Non-claims

The repository does not yet claim:

- universal heterogeneous time-series representation;
- recovery of source-global-null modes;
- unique identification of acquisition operators or modal states;
- superiority over metadata conditioning, Gaussian posteriors or affine
  calibration;
- improved diagnosis, forecasting, imputation or domain generalization.
