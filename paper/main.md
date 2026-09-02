# HSE–Laplace Source-Supported Partial Unified Representation

## Working title

**Observability- and Identifiability-Gated Laplace Stochastic Representation
for Cross-Acquisition Time Series**

## Scope

The paper studies multiple acquisition operators observing the same local
dynamical process or one declared system family. The operators may differ in
sampling rate, anti-alias response, sensor transfer function, channel set,
timestamps and sample reliability.

The paper does not cover unrelated systems, incompatible state dimensions or
arbitrary label ontologies.

## Problem

Different acquisition operators do not merely shift a common distribution.
They expose partially overlapping physical modal support. A full
domain-invariant point embedding can therefore erase information that exists
only in a higher-support view, while a generative model can fabricate confidence
for coordinates unsupported by the source evidence.

## Core representation

For domain \(d\),

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

The four roles are:

| Role | Meaning | Permitted operation |
|---|---|---|
| \(\mathcal H_c\) | observable in every declared source domain | anchored canonicalization |
| \(\mathcal H_{p,d}\) | observed now, but not common to every domain | exact identity |
| \(\mathcal H_{m,d}\) | hidden now, supported by at least one other source | conditional inference only when identifiable |
| \(\mathcal H_0\) | unsupported by every source | no data-driven recovery |

The symbol \(\mathcal H_{m,d}\) means **source-supported missing**. It is
not synonymous with statistically recoverable.

## Three gates

### Gate 1 — structural role

A fixed modal slot receives one of the four roles from the source-only
structural acquisition operators.

### Gate 2 — identifiability

A source-supported missing slot receives a learned posterior only if a declared
certificate \(\chi_{d,k}=1\) is available. Acceptable certificates include:

- the same `latent_event_id` observed by complementary acquisitions;
- a known simulator state;
- an injective physical coupling model;
- another explicitly justified semantic anchor.

Unpaired source marginals alone do not qualify.

### Gate 3 — model complexity

The operator class is escalated only when a simpler nested class fails:

\[
T_d:
\text{identity}
\rightarrow
\text{affine}
\rightarrow
\text{OT}
\rightarrow
\text{Flow},
\]

\[
q_d:
\text{point}
\rightarrow
\text{Gaussian}
\rightarrow
\text{mixture}
\rightarrow
\text{Diffusion}.
\]

Thus the contribution is not the mechanical combination of Laplace, Flow and
Diffusion. It is the rule that determines **which physical role may be changed,
which evidence is sufficient to infer it, and which model complexity is
actually needed**.

## Candidate final factorization

When the gates pass,

\[
C^*=T_d(C),
\]

\[
P'=P,
\]

\[
M'\sim
q_\theta(M\mid C^*,P,\mathcal O_d,\chi_d).
\]

The source-global-null block is excluded. The dependency is triangular:
canonical shared state first, private identity second, conditional missing
posterior third.

## HSE token contract

The learned implementation should retain fixed modal slots rather than a
sample-dependent latent dimension. A slot-level token is conceptually

\[
\operatorname{Token}_{d,i,k}
=
(
z_{d,i,k},
\pi_{d,k},
o_{d,k}^{\mathrm{struct}},
r_{d,i,k},
\chi_{d,k},
\tau_{i,k},
[\omega_k^-,\omega_k^+]
),
\]

where:

- \(\pi_{d,k}\) is the structural role;
- \(o_{d,k}^{\mathrm{struct}}\) is structural observability;
- \(r_{d,i,k}\) is sample reliability;
- \(\chi_{d,k}\) is identifiability status.

The common backbone receives a fixed token tensor and attention mask. It does
not receive dataset identity as a semantic shortcut.

## Introduction logic

1. A single local fault transient can be observed through acquisition operators
   with different modal support.
2. Complete alignment can delete task-relevant private information.
3. Current-domain absence must be separated into source-supported missing and
   source-global null.
4. Source support alone does not identify a missing conditional; unpaired
   marginals can correspond to opposite conditionals.
5. Population marginal alignment alone can reverse semantics.
6. The proposed representation uses role, identifiability and complexity gates
   before assigning Flow, identity or a probability model.
7. The known-pole experiment determines whether each mechanism has headroom
   before a learned joint architecture is built.

## Candidate novelty

> An acquisition-observability-conditioned, identifiability-gated
> representation that canonicalizes only common modal support, preserves
> observed-private evidence, models source-supported missing modes only under a
> declared coupling certificate, and excludes source-global-null modes from
> recovery claims.

## Main theory for the paper

The main text should emphasize:

1. four-way source-supported decomposition;
2. complete-invariance task-risk lower bound;
3. source support versus conditional identifiability;
4. paired semantic-risk bound;
5. triangular representation construction.

The following are necessity gates rather than headline innovations:

- Diffusion proper-score theorem;
- affine canonicalization theorem;
- window-local Laplace adequacy bound.

All other results support assumptions or appendices. See `theory/README.md`.

## Strongest competing explanations

- metadata and a hard support mask are sufficient;
- the source-supported missing conditional is not identified;
- a Gaussian or mixture posterior matches Diffusion;
- paired affine calibration or ordinary OT matches Flow;
- a matched direct time-domain latent matches Laplace coordinates;
- apparent private information is acquisition identity;
- canonical marginal alignment permutes task semantics.

## Evidence boundary

```text
proved:
conditional mathematical implications under explicit assumptions

executed:
deterministic analytic tests

not executed:
known-pole factorial experiment
learned posterior
learned canonical Flow
real paired-rate PHM experiment

not supported:
universal representation
global-null recovery
necessity of Diffusion or Flow
real diagnosis improvement
```
