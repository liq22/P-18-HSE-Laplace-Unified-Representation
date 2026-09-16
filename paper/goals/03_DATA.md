# Goal03 — industrial data and genuine features

**Scope:** only PHMFactory industrial preparation, metadata, reader and accepted split. **Products:** local official/provider data, original group keys, checked labels/time units, source-trained HSE/reference checkpoints and actual feature exports. Data details: `../experiments/DATA_DOWNLOAD_SOP.md`.

```bash
bash experiments/p19/run.sh phm-prepare --output /absolute/data/mfpt
bash experiments/p19/run.sh phm --data /absolute/data/mfpt --output /absolute/runs/mfpt-check
# Once actual source-frozen exports exist:
bash paper/run.sh native-batch --batch /absolute/exports/train.npz --data-note /absolute/exports/export_note.md
```

**Acceptance:** unchanged MFPT reference,20 files, labels0/1/2, disjoint10/4/6 records, checkpoints and metrics agree. Feature provenance additionally proves genuine HSE/ref execution and original-group isolation. No target normalization or relabelled random features. File IDs do not prove physical-bearing independence.

**Failure:** missing permission/data/checkpoint/converter is a named prerequisite, not completed by an NPZ with convenient columns. Do not build an alternate MAT reader or patch PHMFactory core. General-domain preparation is not in this goal.
