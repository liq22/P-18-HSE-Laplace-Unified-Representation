# HSE–LapDiff

**Acquisition-calibrated conditioning for probabilistic cross-acquisition representation**

Use `dev` for current research. `master` remains the earlier baseline.

```bash
git clone --branch dev https://github.com/liq22/P-18-HSE-Laplace-Unified-Representation.git
cd P-18-HSE-Laplace-Unified-Representation
bash paper/run.sh setup
bash paper/run.sh all smoke
```

The active question is which acquisition information a finite HSE condition must retain for the same LLapDiff. Flow Matching is future work, not an active component.

## Read the paper

Start at [paper/README.md](paper/README.md): working abstract and Introduction, Chinese paragraph map, Method, nearest-work gaps, experiment matrix, and separate numerical results. Each numbered theoretical argument has one Markdown and one same-stem executable Notebook under `theory/`.

## Current evidence

- Full-statistic Gaussian and finite-design compressed-posterior oracles are retained.
- A new fixed-header sampled-waveform experiment distinguishes precision coupling from posterior-moment preservation.
- Nine new behavior tests and two new theory witnesses were executed locally; the PR records complete-repository CI separately.
- Learned HSE–LLapDiff and real PHM have not been run. `formal_claim_supported: false`.

The 24 sampled designs do not justify the expensive risk selector over a magnitude rule. Moment-matching is a stronger analytic control, but it performs full posterior inference at the encoder. Equal stored header size is not equal compute or a learned-method success.

## Run only the needed step

```bash
bash paper/run.sh theory
bash paper/run.sh oracle full
bash paper/run.sh sampled full
bash paper/run.sh figures outputs/paper/sampled-full/sampled_summary.csv outputs/paper/figures
```

`all` covers implemented analytic/numerical tasks only. The separate official-baseline launcher uses an external LLapDiff installation and documented CLI; it does not substitute synthetic oracles for learned baselines. Outputs stay in ignored `outputs/`. Existing Task A/B reference results are not overwritten.

No PHMFactory submodule is present in the inspected development tree. Paper code and plots do not import its internals. Optional framework-prepared data must use the explicit exported record contract in `paper/experiments.md`.
