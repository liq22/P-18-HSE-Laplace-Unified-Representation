# Goal 03 — data and genuine feature exports

## Scope

Use PHMFactory for every PHM reader, metadata and executed split. Use the five official non-PHM sources in `paper/experiments/DATA_DOWNLOAD_SOP.md`. A downloaded archive, parsed file or three-field synthetic NPZ is not a genuine HSE/reference export.

## Products

Local official files, literal source/license/version note, original independent-unit split, one checked data batch, and source-trained HSE/reference exports with the existing explicit masks/side names/target map. No machine-local arrays or checkpoints are committed.

## Commands

```bash
bash experiments/p19/run.sh phm-prepare --output /absolute/data/mfpt
bash experiments/p19/run.sh phm --data /absolute/data/mfpt --output /absolute/runs/mfpt-data
# After actual source-trained HSE/reference extraction:
bash paper/run.sh native-batch --batch /absolute/exports/train.npz --data-note /absolute/exports/export_note.md
```

The native batch command uses the current inspected `--batch` and `--data-note` arguments. The full comparison entry, once all three exports exist, is Goal 06. Raw external conversion is intentionally not claimed implemented by a native-feature launcher.

## Acceptance

PHMFactory reference: 20 files; labels 0/1/2; source 10/4 and target 6 files; selected checkpoint/metrics agree. Genuine feature acceptance additionally proves source-trained provenance, raw group separation, query-time units, actual mask/side consumption and matching target function. Source and unseen acquisition scores remain separate. USHCN monthly is not relabelled as daily; UCI HAR uses inertial series, not engineered feature vectors.

## Failure handling

Missing archive/license permission/checkpoint/export implementation: report the exact prerequisite, execute independent available slices, and leave that dataset pending. Never fill the export with random features, change test membership, infer independent bearings from file IDs, or patch PHMFactory core.
