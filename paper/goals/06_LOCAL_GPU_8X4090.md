# Goal 06 — local execution on 8×4090, one GPU per run

## Hard rule

A single training run uses one GPU. No DDP/world-size=2 workaround is allowed for this study. The first Gate-1 and Gate-2 executions use GPU0 only. After Gate 2 freezes the protocol, independent folds/seeds may run concurrently across different cards, one process per GPU.

## Stage order

```text
Gate 0  data/task qualification                  CPU / no effect claims
Gate 1  one real source batch                    GPU0
Gate 2  one LODO target × one seed × key cells   GPU0
freeze protocol/config/HPO
Gate 3  independent folds/seeds                  GPU0..GPU7, one job/card
analysis/cost/figures                             no retraining unless declared
```

Do not launch full three-fold × multi-seed training before Gate 2 proves the cells are non-degenerate and artifacts are complete.

## Local data

The agent receives the actual local root out of band. Put machine paths in an untracked local YAML or CLI override, never in committed research configs.

Example shell binding:

```bash
export PHM_DATA_ROOT=/home/user/data/PHMbenchdata/PHM-Vibench
```

Use PHMFactory's public config path and existing Data Factory; do not directly open HDF5 from a P18 training script.

## Gate-1 command contract

The exact config path must come from the implemented PHMFactory P18 config index:

```bash
CUDA_VISIBLE_DEVICES=0 phmfactory preflight --config "$REAL_CONFIG" \
  --override data.data_dir="$PHM_DATA_ROOT" \
  --override data.metadata_file=metadata.xlsx \
  --override trainer.device=cuda \
  --override trainer.devices=1

CUDA_VISIBLE_DEVICES=0 phmfactory --config "$REAL_CONFIG" \
  --override data.data_dir="$PHM_DATA_ROOT" \
  --override data.metadata_file=metadata.xlsx \
  --override trainer.device=cuda \
  --override trainer.devices=1
```

`REAL_CONFIG` must exist and pass preflight. Do not pass a design YAML or a nonexistent future config.

## Gate-2 freeze checks

Before expansion verify:

- source-only fit/selection and no outer-target exposure;
- actual common ontology/shared LODO readout;
- checkpoint reload reproduces predictions;
- all key E1/E2 cells run once;
- S/C equivalence check is understood;
- A process is fully specified and does not consume complement truth;
- posterior score target is available where reported;
- group IDs/statistical units are not windows;
- runtime and peak memory fit one 4090;
- failure artifacts are retained.

Any adjustment after Gate 2 is recorded as a new frozen protocol revision before Gate 3. The target score must not decide the adjustment.

## Gate-3 scheduling

After freeze, assign each `(fold, seed, method/config)` to exactly one card. Keep deterministic run identity in the output directory/config; GPU index is not a scientific factor. Failed jobs are retained and may be rerun only to correct an identified execution failure, never merely to seek a favorable metric.

## OOM / runtime failure

A memory change is allowed only as an explicit matched protocol revision (e.g. batch size with unchanged statistical objective). Record before/after cost. Do not silently shorten windows, reduce posterior targets, change model width or add multi-GPU training for one arm only.
