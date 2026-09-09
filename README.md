# HSE–LapDiff

**Acquisition-Information Conditioning for Probabilistic Cross-Acquisition Representation**

Current research integration uses `dev`. `master` is unchanged by the Task A/B development integration. Start from `dev` to use the theory and compression experiment below:

```bash
git clone --branch dev https://github.com/liq22/P-18-HSE-Laplace-Unified-Representation.git
cd P-18-HSE-Laplace-Unified-Representation
```

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

## Install and verify

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -e ".[notebooks,experiments]"
python examples/analytic_hse_llapdiff_oracle.py
python -m unittest discover -s tests -v
python theory/run_notebooks.py --timeout 180
```

To retain executed copies, add `--output-dir theory/outputs --summary theory/outputs/summary.json` to the last command. Source Notebooks remain output-free. Execution establishes a finite witness, not general proof validity or novelty. CI runs on pull requests and pushes to `dev` and `master`.

## Read existing results without rerunning the experiment

```bash
python -m experiments.synthetic_known_pole.run_compression \
  --plot-only paper/assets/compression_summary.csv \
  --output-dir outputs/task_b_reference
```

This only reads the retained numerical table and regenerates the two SVG/PNG figures. It does not simulate new events, refit a posterior, or overwrite the retained CSV. Figure edits do not require repeating the full experiment.

## Reproduce the paired compression experiment

Run from the repository root:

```bash
python -m experiments.synthetic_known_pole.run_compression \
  --events-per-seed 2048 --seeds 0 1 2 --bootstrap 1000 \
  --output-dir outputs/task_b
```

This writes `compression_summary.csv`, `compression.svg/png` and `calibration.svg/png`. See `paper/results.md` for event-level intervals and limits. Exploratory outputs stay under ignored `outputs/`; the retained numerical table remains under `paper/assets/`.

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

Next: verify acquisition coupling and actual side-input consumption in fixed-window HSE before selecting the smallest learned conditioner. Development merge status does not promote a scientific claim.
