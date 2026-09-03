# HSE–Laplace Source-Supported Partial Unified Representation

This repository asks one bounded question:

> How should multiple acquisition operators represent the same window-local dynamical process when their modal supports only partially overlap?

The representation makes three decisions in order:

```text
1. role gate
   common / observed-private / source-supported-missing / source-global-null

2. identifiability gate
   is the missing conditional identified by paired or physical evidence?

3. complexity gate
   are affine maps and Gaussian/mixture posteriors already sufficient?
```

## Core representation

\[
\mathcal H
=\mathcal H_c\oplus\mathcal H_{p,d}\oplus\mathcal H_{m,d}\oplus\mathcal H_0.
\]

```text
common observable        -> anchored canonicalization
observed private         -> exact preservation
source-supported missing -> conditional inference only when identified
source-global null       -> unsupported; no data-driven recovery claim
```

When the gates pass,

\[
C^*=T_d(C),\qquad P'=P,\qquad
M'\sim q_\theta(M\mid C^*,P,\mathcal O_d,\chi_d).
\]

Flow and Diffusion are optional implementations. They are retained only after simpler alternatives leave predeclared headroom.

## Proof and executable-witness contract

Every numbered theory result has exactly two sources:

```text
theory/NN_name.md              general mathematical argument
theory/notebooks/NN_name.ipynb finite constructive, numerical, or counterexample witness
```

A Notebook is **not** a proof. It checks a finite consequence, implementation invariant, or counterexample. Source notebooks are committed without outputs. CI executes clean copies in isolated kernels.

Run all witnesses:

```bash
python -m pip install -e ".[notebooks]"
python theory/run_notebooks.py --timeout 180
```

To retain executed copies locally:

```bash
python theory/run_notebooks.py \
  --output-dir theory/outputs \
  --summary theory/outputs/summary.json
```

## Contribution admission rule

A theory result enters the paper's contribution list only when all conditions hold:

1. the Markdown states assumptions, theorem or proposition, derivation, and failure boundary;
2. the matching Notebook passes in CI;
3. the Notebook exercises the result's central finite implication or counterexample;
4. the result is specific to the proposed role–identifiability representation, rather than established background or a model-selection gate;
5. manuscript wording stays inside the proved scope.

Notebook success does not promote an empirical claim. Learned-model and real-PHM evidence remain separate gates.

## Current contribution candidates

| Theory | Status |
|---|---|
| four-way source-supported decomposition | admitted theoretical candidate |
| complete-invariance task-risk lower bound | admitted theoretical candidate |
| source support is not missing-conditional identifiability | admitted theoretical candidate |
| triangular partial stochastic representation plus paired risk control | admitted joint theoretical candidate |

Diffusion–Flow marginal equivalence, posterior sufficiency, modal stability, private-product OT, generator commutation, and the Diffusion/Flow/Laplace necessity results remain supporting, background, null-model, or complexity-gate results even when their Notebooks pass.

## Start here

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e ".[notebooks]"
python examples/analytic_unified_representation.py
python -m unittest discover -s tests -v
python theory/run_notebooks.py --timeout 180
```

## Repository map

| Path | Purpose |
|---|---|
| `src/hse_laplace/` | Minimal analytic implementation |
| `theory/README.md` | Proof-to-Notebook map and paper role |
| `theory/*.md` | General derivations and boundaries |
| `theory/notebooks/` | One output-free witness per theory file |
| `paper/main.md` | Core paper argument and contribution gate |
| `paper/experiments.md` | Falsification and model-necessity plan |
| `experiments/` | Empirical work after theory admission |

## Current evidence boundary

```text
formal mathematical status: conditional derivations under stated assumptions
executable theory witnesses: 25 / 25 locally; CI is authoritative
learned posterior: not started
learned canonical Flow: not started
known-pole factorial evidence: not started
real PHM evidence: not started
formal_claim_supported: false
```
