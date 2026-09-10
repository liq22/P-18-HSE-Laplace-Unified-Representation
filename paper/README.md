# Paper workspace

This directory is the researcher's paper and execution entry. The current development base is `dev`; `master` is not changed by this work.

## Read

`main.md` contains the working abstract and full Introduction. `introduction_outline.md` gives the Chinese paragraph/idea map. `method.md` states the analytic and proposed learned methods. `related_work.md` records the exact novelty boundary. `experiments.md` separates implemented experiments from planned learned/PHM work. Prior results remain in `results.md`; the new sampled experiment is in `results_sampled.md`.

Proofs live only in `../theory/`, each with a same-stem Notebook. Do not copy their proofs into multiple planning documents.

## Local execution

From any directory, pass the script path. It resolves the repository root itself. Use your chosen environment; installation is explicit:

```bash
bash paper/run.sh setup
bash paper/run.sh all smoke
```

Full implemented numerical experiments:

```bash
bash paper/run.sh oracle full
bash paper/run.sh sampled full
```

`ablation full` is an alias for the same sampled factorial run, not a second independent experiment. `all` runs theory, the previous finite-design oracle, and the sampled-header experiment. It does not pretend to train the unimplemented learned HSE–LLapDiff.

Figures are separate from experiments:

```bash
bash paper/run.sh figures outputs/paper/sampled-full/sampled_summary.csv outputs/paper/figures
```

Edit the plotting script and rerun only this command. Output is SVG/PDF/PNG with editable vector text; no simulated result is generated while plotting.

## Official external baselines

The checked official CLI belongs to `pixelhero98/LLapDiffusion`. Install it in a separate environment/checkout, activate that environment, and provide its absolute root:

```bash
export LLAPDIFF_ROOT=/path/to/LLapDiffusion
bash /path/to/this-repo/paper/run_official_baselines.sh train crypto
export BASELINE_SOURCE_ROOT=/path/to/upstream-baseline-checkouts
bash /path/to/this-repo/paper/run_official_baselines.sh forecasting crypto
bash /path/to/this-repo/paper/run_official_baselines.sh imputation crypto
```

These launch the official package; they do not install it silently or replace it with an oracle. The current run has syntax-checked this launcher, not executed its training/data-dependent commands. The public crypto preset is a smoke reproduction target, not PHM evidence. Official dependencies and data terms still apply.

## Decoupling

`paper` imports neither PHMFactory nor a submodule's internal package. Experiments are local modules with NumPy; plotting only reads an explicitly supplied CSV. The inspected dev repository has no PHMFactory gitlink. No submodule pointer, framework API or upstream file is modified. Any future framework integration must export the explicit data contract in `experiments.md`; the paper and its analytic experiments must continue working when that external checkout is absent.

## Figure contract

The plotting logic references `Yuan1z0825/nature-skills/skills/nature-figure`: a figure answers one scientific question, includes the uncertainty appropriate to the analysis unit, and uses editable type at final physical dimensions. This project does not copy the skill's agent infrastructure or claim Nature submission certification. Plots have separate figures, 8 pt body text and at least 6 pt legends, no decorative background, SVG text preserved, PDF TrueType and PNG at 300 dpi. The comparison plot is symmetric-log near zero and is labeled accordingly.

Design IDs enumerate a factorial grid; they are not a continuous independent variable. The full-side-information zero controls are in the source table; the main plot intentionally shows the coarse-condition question. Equal curves are retained. The caption must say that moment matching is an exact encoder-side Gaussian control and the full posterior has a larger header.
