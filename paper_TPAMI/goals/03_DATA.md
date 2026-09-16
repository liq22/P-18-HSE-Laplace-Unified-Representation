# Goal03 — five general domains, actual data before model claims

**Scope:** PhysioNet2012, UCI HAR, USHCN monthly, ETTh1 and Japanese Vowels, per `../experiments/DATA_DOWNLOAD_SOP.md`. Optional PHM evidence uses the TII-owned PHMFactory path. **Products:** local official raw files, literal license/version note, parsed batches, original-unit split and genuine source-trained feature/target exports.

```bash
# Execute the exact official per-domain download commands in the SOP.
# After implementing and checking that domain's converter and real encoder export:
python -m experiments.learned_conditioning.native_forward \
  --batch /absolute/exports/train.npz \
  --data-note /absolute/exports/export_note.md \
  --output-dir outputs/tpami/native-batch
```

**Acceptance:** real masks/time units/side names, raw group separation, target definition and source-only scaling verified. UCI HAR is inertial series, USHCN is explicitly monthly, Japanese Vowels is features and not leave-speaker-out. Native generation requires its reference target; classifier labels do not automatically provide one. Downloading is not integration.

**Failure:** missing license permission/archive/converter/checkpoint is an explicit unfinished prerequisite; don't call it merely a GPU limitation. Do not replace with synthetic features. Calibration group independence must be justified separately from file-ID uniqueness.
