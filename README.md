# HSE–Laplace Source-Supported Partial Unified Representation

This repository studies one bounded question:

> How should multiple acquisition operators represent the same local dynamical
> process when their modal supports only partially overlap?

The project does not claim a universal representation for unrelated time
series. Its current scope is one physical system family, one declared
window-local Laplace-modal dictionary, and multiple acquisition operators such
as sampling rates, sensor responses, channel sets and missingness patterns.

## Core idea: roles first, models second

The structural modal space is split into four roles:

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

```text
common observable             -> canonicalize only with an anchored map
observed private              -> preserve exactly
source-supported missing      -> infer only with an identifiability certificate
source-global null            -> unsupported; no data-driven recovery claim
```

The term **source-supported missing** is deliberate. Visibility in another
source domain makes inference eligible, but does not identify the missing
conditional. Pairing, a physical coupling model or another explicit anchor is
still required.

The representation therefore makes three decisions in order:

```text
1. role gate
   shared / observed-private / source-supported-missing / global-null

2. identifiability gate
   can the missing conditional be identified from the declared source evidence?

3. complexity gate
   is a simple affine map or Gaussian/mixture posterior already sufficient?
```

## Candidate stochastic representation

When the corresponding gates pass,

\[
C^*=T_d(C),
\qquad
P'=P,
\qquad
M'\sim q_\theta(M\mid C^*,P,\mathcal O_d).
\]

The candidate model classes are nested:

\[
T_d
\in
\{
\text{identity},
\text{affine},
\text{OT},
\text{Flow}
\},
\]

\[
q_\theta
\in
\{
\text{point},
\text{Gaussian},
\text{mixture},
\text{Diffusion}
\}.
\]

Flow and Diffusion are not mandatory modules. Flow is retained only when
simpler anchored canonicalizers leave paired nonlinear headroom. Diffusion is
retained only when simpler conditional families leave a proper-score and
calibration gap.

## Fixed HSE modal slots

The intended HSE interface keeps a fixed modal-slot budget. For slot \(k\), a
future token carries:

```text
modal state
role
structural observability
instance reliability
identifiability status
physical time support
frequency band
```

Structural observability assigns the role. Instance reliability changes
confidence for one sample without changing the slot dimension.

## Current status

```text
stage: refined theory contract + analytic witness
formal_claim_supported: false
known-pole factorial experiment: not started
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

## Repository map

| Path | Purpose |
|---|---|
| `src/hse_laplace/` | Minimal analytic implementation |
| `theory/README.md` | Theory dependency map and reading order |
| `theory/*.md` | One derivation or boundary analysis per file |
| `paper/main.md` | Core paper argument |
| `paper/experiments.md` | Falsification and model-necessity gates |
| `paper/related_work.md` | Exact novelty boundary |
| `experiments/` | Executable scientific experiments |
| `tests/` | Behavioral mathematical invariants |

## Next decisive experiment

The next research PR remains the known-pole oracle study:

```text
full / partial support overlap
×
private task-irrelevant / task-relevant
×
unimodal / multimodal source-supported missing conditional
```

Add two mandatory controls:

```text
paired versus unpaired source evidence
affine versus nonlinear shared distortion
```

A source-global-null mode remains a negative control.

## Non-claims

The repository does not yet claim:

- recovery of every source-supported missing coordinate;
- recovery of source-global-null coordinates;
- necessity of Diffusion or Flow;
- superiority of Laplace coordinates over a matched time-domain latent;
- improved real PHM diagnosis, forecasting or domain generalization.
