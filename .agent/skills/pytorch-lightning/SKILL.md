---
name: pytorch-lightning
description: 'Implementation skill for engineering deep-learning training runs with PyTorch Lightning (LightningModule, Trainer, callbacks, loggers, DDP/FSDP/DeepSpeed) backing a paper/experiments/ claim. Do not use for classical ML (scikit-learn), Bayesian inference (pymc), plotting, or as a training engine — prefer the relevant planning skill as primary.'
---

# pytorch-lightning

## Purpose

Provide implementation reference material for organizing PyTorch deep-learning
training engineering with PyTorch Lightning (the `lightning` package): how to
structure a `LightningModule`, configure a `Trainer`, encapsulate data with a
`LightningDataModule`, wire in callbacks and experiment loggers (TensorBoard,
Weights & Biases, MLflow, Comet), and choose a distributed strategy (DDP, FSDP,
DeepSpeed). In Auto-01-tiny-research this is a TIER B **tool / implementation**
skill: it documents how the neural-network runs that generate the paper's
evidence are engineered, and maps every resulting metric onto
`paper/experiments/` so downstream skills (`08-markdown-draft`,
`09-tex-freeze-formalize`, `11-reference-audit`, `13-reviewer-response`) can
cite it. It is not a planning skill and not an execution harness.

## Use When

- A claim in `paper/experiments/evidence_matrix.md` requires a deep-learning
  result (e.g. model accuracy/loss/F1 from a neural network) that must be
  engineered reproducibly with PyTorch Lightning.
- You need to document how a `LightningModule` (training/validation/test/predict
  steps, `configure_optimizers`, `save_hyperparameters`) should be structured
  for the run logged in `paper/experiments/run_ledger.md`.
- A `Trainer` configuration (accelerator, devices, precision, gradient
  accumulation, max_epochs, callbacks, logger) must be specified and recorded
  for reproducibility in `paper/experiments/reproducibility.md`.
- A reviewer asks how training was scaled across GPUs — you must document the
  distributed strategy (DDP vs FSDP vs DeepSpeed) and justify the choice in
  `paper/reviews/response_to_reviewers.md`.
- A `LightningDataModule` data pipeline (prepare_data / setup / dataloaders)
  or a callback (ModelCheckpoint, EarlyStopping, LearningRateMonitor) must be
  specified and tied to the evidence ledger.

Do not use this skill for classical/tabular ML (defer to scikit-learn),
Bayesian inference (defer to pymc), static figure generation (defer to
scientific-visualization / matplotlib), or any non-PyTorch deep-learning stack.
It is also not an execution harness: in this repo it documents and recipes
training engineering; it does not run production training jobs and ships
`references/` docs only — never executable `scripts/`.

## Required Inputs

- The claim ID(s) this training run must support, from
  `paper/experiments/evidence_matrix.md`, and the data ref already logged in
  `paper/experiments/run_ledger.md`. Do not invent data or fabricate metrics.
- The metric(s), split protocol, and reproducibility constraints mandated by
  `paper/refs/target_journal.md` and `paper/experiments/statistics.md`
  (e.g. seed, mixed precision policy, eval protocol).
- A target output path for any persisted result under `paper/experiments/` or
  `paper/assets/tables/`.
- Python 3.10+ with `lightning` 2.6+ (the `pytorch-lightning` package name still
  installs the same library; `import lightning as L`). GPU/CUDA training,
  optional loggers (`wandb`, `mlflow`, `comet-ml`), and `deepspeed` are separate
  installs the user is responsible for; this skill does not pin or ship a
  runtime.
- **Credentials:** if an experiment logger needs an API key (e.g. a W&B /
  MLflow / Comet token), the **user must provide it; never hardcode or store
  it.** Do not put real keys in `references/`, the run ledger, or any committed
  file — reference `<user-provided-key>` and load from the environment at run
  time only.

## Workflow

1. Read the target claim, required metric, and reproducibility constraints from
   `paper/experiments/evidence_matrix.md`, `paper/refs/target_journal.md`, and
   `paper/experiments/statistics.md`. Do not pick a metric the journal or the
   claim does not sanction.
2. Confirm the data ref exists in `paper/experiments/run_ledger.md`; if the data
   is absent or unlogged, stop (see Stop With) rather than substituting.
3. Document the `LightningModule` structure following
   `references/lightning_module.md`: `__init__` with `save_hyperparameters()`,
   `training_step` / `validation_step` / `test_step` / `predict_step`, and
   `configure_optimizers`. Use device-agnostic code (`self.device`, not
   `.cuda()`).
4. Specify the `LightningDataModule` from `references/data_module.md`
   (`prepare_data` single-process, `setup` per-GPU, the three dataloaders) so
   the data pipeline is reproducible and leakage-safe (no fit-time statistics
   leaking across splits).
5. Configure the `Trainer` per `references/trainer.md`: accelerator, devices,
   precision, gradient accumulation/clipping, `max_epochs`, and the callbacks
   from `references/callbacks.md` (ModelCheckpoint, EarlyStopping,
   LearningRateMonitor). Record the exact config in
   `paper/experiments/reproducibility.md`.
6. Wire a logger from `references/logging.md` (TensorBoard default, or W&B /
   MLflow). If the logger needs a credential, load it from the environment at
   run time only — never commit a real key.
7. Pick the distributed strategy from `references/distributed_training.md`
   (DDP < 500M params, FSDP 500M+, DeepSpeed for fine-grained control) and
   justify it in `paper/logs/decision_log.md` if scaling was non-trivial.
8. Apply the patterns in `references/best_practices.md`: `seed_everything()`,
   `Trainer(deterministic=True)` where possible, `fast_dev_run=True` to smoke
   test, and `self.log()` for automatic cross-device aggregation.
9. Persist the result: append a run row to `paper/experiments/run_ledger.md`
   (model, Trainer config, strategy, precision, metric, seed, data ref, claim
   ID), update `paper/experiments/evidence_matrix.md` status
   (`supported` / `partial` / `refuted`), record versions + seed in
   `paper/experiments/reproducibility.md`, and surface any variant comparison
   in `paper/experiments/ablation.md` / `paper/assets/tables/`.
10. Record honest negative results in `paper/experiments/dead_ends.md` and any
    non-trivial methodological decision in `paper/logs/decision_log.md`.

## Output Contract

- A run row in `paper/experiments/run_ledger.md` capturing: model
  (LightningModule summary), Trainer config (accelerator/devices/precision/
  max_epochs/strategy), logger, callbacks, point metric, seed, and the
  data/claim IDs it supports.
- Updated status in `paper/experiments/evidence_matrix.md` for every claim the
  run addresses (`supported` / `partial` / `refuted` / `unsupported`).
- A reproducibility note in `paper/experiments/reproducibility.md` covering
  `lightning` / `torch` / CUDA versions, seed, strategy, precision policy, and
  exact data ref.
- An ablation/model-comparison table under `paper/assets/tables/` when more
  than one variant was compared; mirror it into
  `paper/experiments/ablation.md`.
- Optional entries in `paper/logs/decision_log.md` (e.g. DDP-vs-FSDP choice)
  and `paper/experiments/dead_ends.md` (negative results).
- No executable training/inference scripts shipped into the repo and no model
  weight artifacts (`.pt`/`.pth`/`.ckpt`/`.bin`/`.safetensors`) committed; this
  skill ships `references/` documentation and recipes only.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only pytorch-lightning`
- `python src/S03_Scripts/validate_project.py`
- Confirm every deep-learning run referenced in
  `paper/experiments/evidence_matrix.md` has a matching row in
  `paper/experiments/run_ledger.md` (no orphan claims).
- Confirm the Trainer config (accelerator, devices, precision, strategy),
  `lightning`/`torch` versions, and seed are recorded in
  `paper/experiments/reproducibility.md` for every run.
- Confirm no model weight artifact (`.pt`/`.pth`/`.ckpt`/`.bin`/`.safetensors`)
  and no real API key / token is committed under `.agent/skills/pytorch-lightning/`
  or referenced by the run row (grep for `sk-`, `gh[pousr]_`, `AKIA`,
  `BEGIN ... PRIVATE KEY`, and the denylist extensions — must be absent).
- Confirm a leakage-safe data pipeline is documented (DataModule `setup` per
  split, no fit-time statistics computed on the validation/test fold).

## Boundaries

- Do not run training as an execution engine here; this is a paper repo, not an
  ML runtime. Document and recipe; do not execute production training jobs.
- Do not copy the upstream `scripts/` executable training/inference code into
  this repo; this skill ships `references/` documentation only.
- Do not commit model weights or binary artifacts (`.pt`/`.pth`/`.ckpt`/
  `.bin`/`.safetensors`/`.joblib`); record configs, recipes, and metrics, not
  weights.
- Do not hardcode or store API keys / tokens (W&B, MLflow, Comet, model-hub);
  the user must provide them and they must be loaded from the environment at
  run time only.
- Do not fabricate metrics, datasets, or benchmark numbers; if a result is
  missing, mark the claim `missing_evidence` and stop.
- Do not write outputs anywhere except `paper/experiments/`,
  `paper/assets/tables/`, and the designated logs; never into `paper/tex/`,
  `paper/refs/`, or `paper/submission/`.
- Do not handle classical ML (defer to scikit-learn), Bayesian inference
  (pymc), or figure rendering (scientific-visualization) — stay in the
  deep-learning training-engineering lane.

## Stop With

- The data needed to compute a claim is not present in
  `paper/experiments/run_ledger.md` and the user has not supplied it.
- The required metric, split protocol, or precision policy is unspecified by
  `paper/refs/target_journal.md` / `paper/experiments/statistics.md` and the
  user has not disambiguated.
- A leakage risk is unavoidable given the data shape (e.g. no clean train/val
  split, group/temporal leakage with no grouping variable) — report and pause
  rather than report a biased number.
- `lightning` / `torch` or a required logger / DeepSpeed dependency is
  unavailable and the user cannot install it; do not silently fall back to a
  different library or a non-reproducible setup.
- The distributed strategy choice (DDP vs FSDP vs DeepSpeed) materially changes
  the result and the user has not authorized one — surface the trade-off in
  `paper/logs/decision_log.md` and wait.
- The result would contradict the claim's required direction and the user has
  not authorized reporting a `refuted` finding — surface it honestly in
  `paper/experiments/dead_ends.md` and wait.

## References

- LightningModule guide: `.agent/skills/pytorch-lightning/references/lightning_module.md`
- Trainer configuration: `.agent/skills/pytorch-lightning/references/trainer.md`
- LightningDataModule patterns: `.agent/skills/pytorch-lightning/references/data_module.md`
- Callbacks (built-in + custom): `.agent/skills/pytorch-lightning/references/callbacks.md`
- Logging integrations: `.agent/skills/pytorch-lightning/references/logging.md`
- Distributed training (DDP/FSDP/DeepSpeed): `.agent/skills/pytorch-lightning/references/distributed_training.md`
- Best practices & pitfalls: `.agent/skills/pytorch-lightning/references/best_practices.md`
- Invocation scenarios: `.agent/skills/pytorch-lightning/examples/prompts.md`
- Workspace artifacts: `paper/experiments/evidence_matrix.md`,
  `paper/experiments/run_ledger.md`, `paper/experiments/statistics.md`,
  `paper/experiments/ablation.md`, `paper/experiments/reproducibility.md`,
  `paper/experiments/dead_ends.md`, `paper/experiments/insights.md`,
  `paper/assets/tables/`, `paper/refs/target_journal.md`,
  `paper/reviews/response_to_reviewers.md`, `paper/logs/decision_log.md`
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://lightning.ai/docs/pytorch/stable/
