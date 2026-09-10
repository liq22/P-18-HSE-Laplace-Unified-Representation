# Paper workspace

The integration target is `dev`; this work remains on Draft PR #8 until review. `master` is not changed.

## Start here

Read **[GOAL.md](GOAL.md)** for the Chinese execution package and comment decisions. `main.md` contains the English abstract and full Introduction; `introduction_outline.md` maps each paragraph to its purpose and verified references. `method.md`, `related_work.md` and `experiments.md` separate current analytical results from the candidate learned method.

Results have distinct scopes: `results.md` is the inherited finite-design oracle, `results_sampled.md` is the 24-design sampled-header study, and `results_parameterization.md` is the new same-partition/target control. They must not be conflated. Proofs live only in `../theory/`, each paired with a same-stem Notebook.

## Local execution

From another working directory, use the absolute script path; it resolves the repository root. Installation is explicit:

```bash
bash paper/run.sh setup
bash paper/run.sh all smoke
```

The implemented experiments can run separately:

```bash
bash paper/run.sh theory
bash paper/run.sh oracle full
bash paper/run.sh sampled full
bash paper/run.sh parameterization full
```

`ablation full` aliases the sampled run; it is not a second independent experiment. `all` runs theory, oracle, sampled and parameterization tasks only. It does not train the unimplemented HSE–LLapDiff.

Replot without rerunning any experiment:

```bash
bash paper/run.sh figures outputs/paper/sampled-full/sampled_summary.csv outputs/paper/figures
bash paper/run.sh parameterization-figures paper/assets/parameterization_controls.csv outputs/paper/parameterization-reference
```

Exploratory outputs stay under ignored `outputs/`; retained numeric source tables stay in `paper/assets/`. SVG/PDF/PNG figures are reproducible from those tables. Plot editing does not overwrite reference numbers.

## Official external baselines

The checked CLI belongs to `pixelhero98/LLapDiffusion`. Install it in a separate environment/checkout, activate it, and provide its absolute root:

```bash
export LLAPDIFF_ROOT=/path/to/LLapDiffusion
bash /path/to/this-repo/paper/run_official_baselines.sh train crypto
export BASELINE_SOURCE_ROOT=/path/to/upstream-baseline-checkouts
bash /path/to/this-repo/paper/run_official_baselines.sh forecasting crypto
bash /path/to/this-repo/paper/run_official_baselines.sh imputation crypto
```

The launcher does not silently install dependencies or replace the official model with an oracle. Only its shell syntax was tested here; data-dependent training commands were not run. The crypto preset is an upstream reproduction target, not PHM evidence.

## Decoupling and plotting

Paper experiments import neither PHMFactory nor submodule internals. The inspected branch has no PHMFactory gitlink. Any later framework integration exports the arrays and recording-level splits declared in `experiments.md`; the paper must still run without the external checkout.

Figure conventions reference `Yuan1z0825/nature-skills/skills/nature-figure`: one scientific question, explicit source data and uncertainty, editable vector text and final physical dimensions. Python matplotlib remains the sole drawing backend. No image model generates quantitative data, no full figure-governance framework is copied, and no Nature submission certification is claimed.

The inherited comparison plot uses a labeled symmetric-log scale. New parameterization panels use linear axes and categorical markers without joining method categories into a fictitious trajectory. The full source tables retain zero controls and equal results. Every caption distinguishes exact encoder-side inference, unequal storage and target-only representations.
