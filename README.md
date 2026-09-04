# HSE–LapDiff

**Support-Calibrated Latent Laplace Diffusion for Probabilistic Cross-Acquisition Representation**

This repository studies one bounded problem:

> How can different sampling rates, timestamps, missingness patterns, and sensor responses condition one posterior over the same window-local Laplace latent state?

## Core idea

HSE converts a variable-length acquisition into a fixed set of physical conditioning tokens. LLapDiff then predicts a posterior in one canonical Laplace latent coordinate system.

```text
heterogeneous observation
    -> HSE physical tokens [K, D]
    -> LLapDiff history conditioning
    -> canonical Laplace latent posterior
```

The method does **not** force two acquisitions to have the same deterministic embedding. A more informative acquisition should generally produce a narrower posterior in the directions it observes.

## Current status

```text
active method: HSE + Latent Laplace Diffusion
Flow Matching: future work only
implemented evidence: linear-Gaussian analytic oracle
learned HSE-LLapDiff model: not started
real PHM evidence: not started
formal_claim_supported: false
```

## Analytic oracle

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e ".[notebooks]"
python examples/analytic_hse_llapdiff_oracle.py
python -m unittest discover -s tests -v
python theory/run_notebooks.py --timeout 180
```

The oracle validates only the linear-Gaussian special case:

1. variable-length observations admit fixed-dimensional statistics
   \(b=A^TR^{-1}x\) and \(J=A^TR^{-1}A\);
2. the Gaussian posterior has a closed form in one canonical modal space;
3. \(J_H\succeq J_L\) implies \(\Sigma_H\preceq\Sigma_L\);
4. paired observations identify a conditional relation, whereas separate marginals do not;
5. complete deterministic invariance can discard task-relevant private information.

## Repository map

| Path | Purpose |
|---|---|
| `src/hse_laplace/` | Minimal acquisition, token, posterior, and modal contracts |
| `examples/` | Executed analytic oracle |
| `theory/` | One proof or boundary per Markdown file, with one finite witness each |
| `paper/` | Single manuscript authority, experiment plan, and current results |
| `experiments/synthetic_known_pole/` | Next falsification experiment |
| `future_work/` | Flow Matching and other explicitly inactive directions |
| `literature/` | Closest prior work and novelty boundary |

## Evidence boundary

A passing test or Notebook means that a finite consequence is internally consistent. It does not validate a theorem beyond its assumptions, demonstrate a learned model, establish novelty, or prove usefulness on PHM data.
