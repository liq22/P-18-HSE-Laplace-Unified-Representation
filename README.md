# HSE–LapDiff

**Acquisition-Information Conditioning for Probabilistic Cross-Acquisition Representation**

The research question is whether fixed-budget HSE conditioning retains the information needed by the **same LLapDiff** to predict a canonical target across sampling rates, timestamps, masks and sensor responses.

```text
current acquisition O + encoder-visible descriptors
    -> HSE tokens, masks and physical fields H
    -> actual decoder condition C = (H, a_consumed)
    -> LLapDiff conditional latent distribution
```

The analytical oracle uses known-pole physical coefficients. A learned LLapDiff uses a frozen reference-encoder latent target; these are not assumed identical. Fixed token shape is not a sufficiency or calibration guarantee.

## Status

```text
active method: HSE + Latent Laplace Diffusion
Flow Matching: future work only
implemented model: linear-Gaussian analytic oracle
new analysis: actual-condition information loss and denoising projection
learned HSE-LLapDiff / real PHM evidence: not started
formal_claim_supported: false
```

The diagonal token implementation does not store all off-diagonal acquisition information. This can lose information **unless the actual side input already reconstructs it**. The original full-statistic oracle remains correct; it does not validate inference through the diagonal tokens.

## Run

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e ".[notebooks]"
python examples/analytic_hse_llapdiff_oracle.py
python -m unittest discover -s tests -v
python theory/run_notebooks.py --timeout 180
```

To retain executed copies, add `--output-dir theory/outputs --summary theory/outputs/summary.json` to the last command. Source Notebooks remain output-free. Execution establishes a finite witness, not general proof validity or novelty.

## Read

| Path | Purpose |
|---|---|
| `theory/README.md` | One Markdown and one same-stem Notebook per result |
| `paper/main.md` | Scientific argument and contribution candidates |
| `paper/results.md` | Numerical checks and their limits |
| `paper/experiments.md` | Three sequential tasks: theory, compression experiment, learned integration |
| `src/hse_laplace/` | Current analytical acquisition and token code |
| `future_work/flow_matching.md` | Explicitly inactive direction |

Next: compare full, diagonal and declared small-block acquisition information under identical actual side inputs. Do not add a learned coupling branch before that experiment supports it.
