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
new analysis: exact compressed condition over a finite acquisition family
new experiment: paired coefficient-space compression oracle (no trained model)
learned HSE-LLapDiff / real PHM evidence: not started
formal_claim_supported: false
```

The diagonal token implementation does not store all off-diagonal acquisition information. This can lose information **unless the actual side input already reconstructs it**. The original full-statistic oracle remains correct; it does not validate inference through the diagonal tokens.

## Run the theory witnesses

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e ".[notebooks]"
python examples/analytic_hse_llapdiff_oracle.py
python -m unittest discover -s tests -v
python theory/run_notebooks.py --timeout 180
```

To retain executed copies, add `--output-dir theory/outputs --summary theory/outputs/summary.json` to the last command. Source Notebooks remain output-free. Execution establishes a finite witness, not general proof validity or novelty.

## Paired compression experiment

Run from the repository root:

```bash
python -m pip install -e ".[notebooks,experiments]"
python -m experiments.synthetic_known_pole.run_compression --events-per-seed 2048 --seeds 0 1 2 --bootstrap 1000 --output-dir outputs/task_b
```

This writes `compression_summary.csv`, `compression.svg/png` and `calibration.svg/png`. The retained numerical table is `paper/assets/compression_summary.csv`; figures are regenerated rather than maintained twice. See `paper/results.md` for event-level intervals and limits.

The exact compressed conditional differs from diagonal plug-in inference. Blocks remove the gap only when the retained coupling suffices; supplying the full operator to every arm removes all Bayes-information gaps. These controlled measurements are not a sampled-waveform HSE, a matched-storage comparison, or evidence that Diffusion is necessary.

## Read

| Path | Purpose |
|---|---|
| `theory/README.md` | One Markdown and one same-stem Notebook per result |
| `paper/main.md` | Scientific argument and contribution candidates |
| `paper/results.md` | Numerical checks and their limits |
| `paper/experiments.md` | Theory, compression experiment, then learned integration |
| `experiments/synthetic_known_pole/` | One exact-condition oracle and one runnable experiment |
| `src/hse_laplace/` | Current analytical acquisition and token code |
| `future_work/flow_matching.md` | Explicitly inactive direction |

Next: verify acquisition coupling and actual side-input consumption in fixed-window HSE before selecting the smallest learned conditioner. Flow remains future work.
