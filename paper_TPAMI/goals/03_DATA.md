# Goal03 — genuine data, not a feature-file placeholder

**Scope/products:** retain the five official sources in `../experiments/DATA_DOWNLOAD_SOP.md`. UCI Japanese Vowels now has a real reader, masks/frame units, original labels, 162/54/54 source split and untouched370 test utterances. The other four converters remain pending. Raw sequence exports are not HSE/reference-VAE features.

```bash
mkdir -p data/manual/japanese_vowels
curl -fL 'https://archive.ics.uci.edu/static/public/128/japanese%2Bvowels.zip' -o data/manual/japanese_vowels/vowels.zip
bash paper_TPAMI/run.sh vowels-reference --archive data/manual/japanese_vowels/vowels.zip --output-dir outputs/tpami/vowels-reference-01
# Only after genuine source-trained feature/reference extraction:
bash paper/run.sh native-batch --batch /absolute/exports/train.npz --data-note /absolute/exports/export_note.md
```

**Acceptance:** official speaker blocks/270+370 counts, native lengths and12 channels verified; 6.4ms feature-frame timing is not10kHz audio timing. No target selection. Saved affine model restores actual metrics. Patient/subject/station/session independence must be checked for each other source; unique IDs alone do not establish iid calibration. PHM uses PHMFactory exclusively in the TII-owned path.

**Failure:** missing archive, permission, converter or checkpoint is named. The other four data sources are not marked integrated from their URLs. Do not fill native fields with random features or classify all missing prerequisites as GPU work.
