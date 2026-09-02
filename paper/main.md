# HSE–Laplace Source-Supported Representation

## Working title

**Observability-Partitioned Laplace Stochastic Transport for
Cross-Acquisition Representation of Shared Local Dynamics**

## Scope

The paper studies multiple acquisition operators observing the same local
dynamical process or one system family sharing a declared local modal
dictionary. Heterogeneity may arise from sampling rate, sensor response,
channel set, timestamps and missingness.

The paper does not claim a universal representation for unrelated time series,
different state dimensions or incompatible label ontologies.

## Central question

How should a representation treat modal information that is:

1. observable in every source acquisition domain;
2. observable in the current domain but not in every domain;
3. hidden in the current domain but observable in another source domain;
4. unsupported by every source domain?

## Central claim under test

A complete domain-invariant point embedding is inappropriate when acquisition
supports only partially overlap. The structural modal space should be
partitioned as

\[
\mathcal H
=
\mathcal H_c
\oplus
\mathcal H_{p,d}
\oplus
\mathcal H_{m,d}
\oplus
\mathcal H_0,
\]

where the blocks are common, observed-private, recoverable-missing and
source-global-null.

The candidate method assigns different semantics:

\[
\begin{aligned}
\mathcal H_c
&:
\text{source-population canonical Flow},\\
\mathcal H_{p,d}
&:
\text{identity preservation},\\
\mathcal H_{m,d}
&:
\text{conditional posterior, with Diffusion only if needed},\\
\mathcal H_0
&:
\text{unsupported; no learned recovery claim}.
\end{aligned}
\]

The final dependency is triangular:

\[
C^*=T_d(C),
\qquad
P'=P,
\qquad
M'\sim q_\theta(M\mid C^*,P,\mathcal O_d).
\]

## Introduction argument

### Paragraph 1 — observed industrial failure

The same local fault transient can be recorded through different sampling
rates, anti-alias filters, sensor transfer functions and missingness patterns.
These operators change which modal components are supported, not only their
marginal statistics.

### Paragraph 2 — failure of complete alignment

If high-support observations contain task-relevant private information, forcing
their complete representation to equal a lower-support view removes that
information. The task-risk lower bound in Theorem 5 makes this loss explicit.

### Paragraph 3 — missing information is not one category

A mode hidden in the current domain but observed elsewhere can receive a
source-supported conditional posterior. A mode hidden from every source cannot.
Conflating the two lets a generative model present prior-driven samples as
recovered evidence.

### Paragraph 4 — exact gap to prior work

Laplace latent models provide stable continuous-time coordinates. Diffusion
provides probability-valued prediction. Flow Matching provides distributional
transport. Shared/private representation learning separates domains. None of
these components alone assigns transport semantics according to acquisition
observability while excluding global-null support from recovery claims.

### Paragraph 5 — proposed object and evidence

The paper proposes an observability-partitioned representation, proves its
four-way decomposition and principal risk properties, then uses an oracle
known-pole factorial experiment to determine whether posterior, Flow and
Laplace mechanisms have independent headroom before training a combined model.

## Method overview

```text
local heterogeneous observation O_d
        ↓
structural acquisition operator A_d
+ sample reliability R_d,i
        ↓
fixed Laplace modal slots
        ↓
common | observed-private | recoverable-missing | global-null
        ↓
Flow  | identity          | conditional posterior | unsupported
        ↓
source-supported distribution-valued representation
```

Structural support and instance reliability are separate:

```text
structural support
-> modal role and source-supported recoverability

instance reliability
-> confidence and posterior precision for one sample
```

## Candidate novelty

The candidate novelty is not the combination of Laplace modeling, Diffusion and
Flow. It is:

> assigning distinct stochastic-transport semantics to
> acquisition-observable modal components, distinguishing recoverable missing
> support from source-global-null support, and making the latter ineligible for
> data-driven recovery claims.

## Theoretical contribution map

| Role | Result | File |
|---|---|---|
| main | four-way source-supported decomposition | `theory/01_observable_subspace_decomposition.md` |
| support | constructive existence and population canonicality | `theory/02_constructive_existence.md` |
| background | Flow–Diffusion marginal equivalence | `theory/03_diffusion_flow_marginal_equivalence.md` |
| method property | observed-private pathwise invariance | `theory/04_observed_private_invariance.md` |
| main | complete-invariance task-risk lower bound | `theory/05_global_invariance_risk_lower_bound.md` |
| support | posterior-valued sufficiency | `theory/06_posterior_representation_sufficiency.md` |
| support | local Laplace modal stability | `theory/07_laplace_modal_stability.md` |
| main candidate | noise-weighted shared-estimation bound | `theory/08_shared_estimation_perturbation_bound.md` |
| main candidate | paired approximation-risk bound | `theory/09_unified_representation_risk_bound.md` |
| optional main/appendix | sampling-gap shift bound | `theory/10_sampling_gap_shift_bound.md` |
| special case | product-case private-identity OT | `theory/11_private_preserving_optimal_transport.md` |
| null model | decoupled generator commutation | `theory/12_commuting_block_generators.md` |
| main experimental driver | identifiability counterexamples | `theory/13_identifiability_and_failure_boundaries.md` |

The main manuscript should not present all results as independent innovations.
The main text should retain the four-way decomposition, the complete-invariance
lower bound and the paired risk bound; remaining results support assumptions,
implementation or appendices.

## Strongest competing explanations

- sampling-rate and sensor metadata are sufficient;
- a hard or soft support mask without generative modeling is sufficient;
- a heteroscedastic Gaussian or mixture posterior matches Diffusion;
- affine calibration, CORAL or ordinary OT matches Flow;
- a direct time-domain latent matches the local Laplace representation;
- private information is acquisition identity rather than fault information;
- unpaired source marginals do not identify the missing conditional.

## Current evidence boundary

```text
proved:
conditional mathematical implications under explicit assumptions

executed:
deterministic four-block semantic tests

not executed:
known-pole factorial experiment
learned posterior
learned Flow
real paired-rate PHM experiment

not supported:
universal representation
global-null recovery
SOTA
real diagnosis improvement
```
