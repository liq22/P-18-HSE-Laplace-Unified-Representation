# pytorch-lightning — invocation scenarios

Realistic prompts for invoking the pytorch-lightning implementation / tool skill
inside the Auto-01-tiny-research workspace. Each scenario shows the kind of
request that should trigger this skill, the artifacts it reads, and the
workspace outputs it must produce. Remember: this skill documents and recipes
deep-learning training engineering — it does not execute training jobs and
ships `references/` docs only.

## Scenario 1: Document a LightningModule + Trainer for a classification claim

> Claim `C-05` in `paper/experiments/evidence_matrix.md` says our fine-tuned
> transformer beats the published baseline by >=3 points F1 on the dataset
> logged in `paper/experiments/run_ledger.md` (run `R-014`). The target journal
> (`paper/refs/target_journal.md`) requires mixed-precision training on a single
> GPU, a fixed seed, and the exact optimizer/scheduler config reported for
> reproducibility. Write up how the `LightningModule` and `Trainer` should be
> structured so a reader could reproduce the number, and log it as run `R-014`.

This triggers pytorch-lightning because the request is deep-learning training
engineering: structuring a `LightningModule` (`training_step` /
`validation_step`, `configure_optimizers`, `save_hyperparameters`) and a
mixed-precision `Trainer`. The skill reads the claim and data ref, follows
`references/lightning_module.md` and `references/trainer.md`, applies the
device-agnostic and `seed_everything()` patterns from
`references/best_practices.md`, then appends a run row to
`paper/experiments/run_ledger.md` (model summary, accelerator/devices/precision,
optimizer/scheduler, F1, seed), updates `C-05` in
`paper/experiments/evidence_matrix.md`, and records `lightning`/`torch`/CUDA
versions + seed in `paper/experiments/reproducibility.md`. Do NOT use
scikit-learn (this is a neural net) and do NOT commit a `.ckpt`/`.pt` weight
blob — record the recipe and metrics only.

## Scenario 2: Multi-GPU scaling justification and FSDP vs DDP ablation

> Reviewer 2 asks why we trained on 4 GPUs with FSDP instead of DDP, and wants
> the throughput/memory numbers in `paper/reviews/response_to_reviewers.md`.
> The model is ~1.2B parameters. Document the strategy choice and add an
> ablation row comparing DDP vs FSDP wall-clock and peak memory into
> `paper/assets/tables/ablation_strategy.tex` and
> `paper/experiments/ablation.md`.

This triggers pytorch-lightning: choosing and justifying a distributed strategy
for a large model. The skill uses `references/distributed_training.md` to
justify FSDP for a 500M+ parameter model (DDP replicates full model per GPU and
would OOM; FSDP shards parameters), documents the exact
`Trainer(strategy="fsdp", accelerator="gpu", devices=4)` config, and records the
DDP-vs-FSDP comparison as an ablation. It writes the table to
`paper/assets/tables/`, mirrors it into `paper/experiments/ablation.md`, answers
the reviewer in `paper/reviews/response_to_reviewers.md`, logs the
strategy/precision/devices in `paper/experiments/reproducibility.md`, and notes
the decision in `paper/logs/decision_log.md`. Do NOT execute the training here;
do NOT ship the upstream `scripts/` executable code — record configs and numbers
only.

## Scenario 3: Specify a DataModule + W&B logger for a reproducible run

> We're starting a new experiment for claim `C-09`. The data lives in
> `paper/experiments/run_ledger.md` (run `R-021`). Specify a leakage-safe
> `LightningDataModule` (tokenization in `prepare_data`, split-specific tensors
> in `setup`, deterministic dataloaders) and a W&B logger so the run is
> traceable. The W&B API key will be supplied by the user — do not commit it.

This triggers pytorch-lightning: engineering the data pipeline and experiment
logger for a deep-learning run. The skill follows
`references/data_module.md` to specify `prepare_data` (single-process, no split
leakage), `setup` (per-GPU, split-specific), and the train/val/test
dataloaders, and `references/logging.md` to wire a `WandbLogger`. The W&B
credential is loaded from the environment at run time only — referenced as
`<user-provided-key>`, never hardcoded or stored. The skill appends the run row
to `paper/experiments/run_ledger.md`, sets `C-09` to
`missing_evidence`/`partial` as appropriate until the metric lands, and records
the logger + DataModule config in `paper/experiments/reproducibility.md`. Do
NOT use pymc or scikit-learn here, and do NOT persist raw weights into the repo.
