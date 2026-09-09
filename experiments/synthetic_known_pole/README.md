# Paired coefficient-space compression experiment

Run from the repository root:

```bash
python -m pip install -e ".[notebooks,experiments]"
python -m experiments.synthetic_known_pole.run_compression --events-per-seed 2048 --seeds 0 1 2 --bootstrap 1000 --output-dir outputs/task_b
```

Outputs: `compression_summary.csv`, `compression.svg/png`, and `calibration.svg/png`. Only the small source table is retained in `paper/assets/`; plots are regenerated rather than maintained twice.

`compression.py` defines one finite linear acquisition population and exact Gaussian-mixture conditionals. `run_compression.py` runs it, aggregates independent events and plots. There is no trainer, experiment manager or model registry.

## What is compared

Two fixed-mode coefficient priors (Gaussian and a two-component mixture), three cross couplings (0,0.45,0.8), coarse versus full operator side inputs, and full/diagonal/block summaries. Exact compressed conditionals are separated from plug-in approximations. Every four-view group shares a coefficient event; noise is independent across acquisitions. Resampling a noisy waveform would require a different joint noise model.

The actual scalar budgets are 14/8/10. This is an information diagnostic, not an equal-budget neural benchmark. With full side input, every arm reconstructs J from A,R. A reduced token cannot be called insufficient merely because its matrix entries are absent from the token array.

## Interpretation

Theorem 11 explains why hidden designs create conditional mixtures, even with a Gaussian coefficient prior. The mixture weights depend on the retained score. Blocks are exact with no hidden cross-mode coupling, and incomplete when cross-mode coupling remains. A finite mixture is an exact oracle here; no Diffusion necessity is established.

The experiment does not yet simulate physical anti-aliasing, variable-rate waveforms, HSE patches or a reference VAE. Those are the next verification layer before learned integration. Full results and decisions live only in `paper/results.md`.
