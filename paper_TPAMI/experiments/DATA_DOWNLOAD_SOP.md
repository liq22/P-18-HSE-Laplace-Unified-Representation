# Official data SOP — TPAMI only

The five external domains remain outside the industrial TII manuscript. Japanese Vowels now has an executed official converter and affine reference. The other four domains below have frozen preparation instructions, not completed converters or benchmark results. Keep raw and derived arrays local in ignored directories; retain source, literal license, retrieval/version and split notes without a new registry.

## 1. PhysioNet / CinC Challenge 2012 v1.0.0 — pending conversion

Official source: https://physionet.org/content/challenge-2012/1.0.0/ . Database terms: Open Data Commons Attribution License v1.0, distinct from article licensing. One record describes an ICU patient's first 48 hours. Historical challenge prose and current availability of outcome files are distinct facts.

```bash
mkdir -p data/manual/physionet2012
cd data/manual/physionet2012
for f in set-a.tar.gz set-b.tar.gz Outcomes-a.txt Outcomes-b.txt; do
  curl -fL "https://physionet.org/files/challenge-2012/1.0.0/$f" -o "$f"
done
tar -xzf set-a.tar.gz
tar -xzf set-b.tar.gz
```

Parse RecordID, static descriptors, channel-specific values and hh:mm times; preserve missing masks and declare repeated-timestamp reduction. Source A supplies fixed fit/validation/calibration patient partitions, B is held-out evaluation. Future queries use only earlier history; random imputation is separate. Mortality/SAPS/SOFA are not hidden inputs. Source-fit data alone determine normalization. Patient independence and task-specific targets are checked before use.

## 2. UCI HAR 240 — pending inertial-series conversion

Official source: https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones ; DOI 10.24432/C54S4K; CC BY 4.0.

```bash
mkdir -p data/manual/uci_har
curl -fL 'https://archive.ics.uci.edu/static/public/240/human%2Bactivity%2Brecognition%2Busing%2Bsmartphones.zip' -o data/manual/uci_har/har.zip
unzip data/manual/uci_har/har.zip -d data/manual/uci_har
```

Use nine Inertial Signals channels, 128 samples per existing 50-Hz window, with the published overlap. Do not substitute the 561-dimensional engineered X_train vectors. Read subject and activity files alongside signals; labels 1–6 map explicitly to 0–5. Preserve official subject-disjoint train/test, and hold out source subjects for validation/calibration. A small number of subjects cannot be replaced with many nominally independent windows to strengthen certification.

## 3. USHCN monthly v2.5 — pending conversion

Source and format: https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ and its readme. This is **USHCN-monthly-v2.5**, not the common daily irregular benchmark. Retain NOAA's own usage/citation terms rather than inventing a Creative Commons license.

```bash
mkdir -p data/manual/ushcn_monthly
for v in tavg tmin tmax prcp; do
  curl -fL "https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ushcn.$v.latest.raw.tar.gz" -o "data/manual/ushcn_monthly/$v.raw.tar.gz"
done
curl -fL https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ushcn-v2.5-stations.txt -o data/manual/ushcn_monthly/stations.txt
```

The latest filenames are mutable: record the dated inner archive names and retrieval date. Parse station/year/month and quality flags per official fixed-width format; -9999 is missing, zero is valid. Retain temperature/precipitation units and station IDs. Align station-month channels, freeze chronological cutoffs and optional station holdouts separately. A time block is not automatically iid; do not apply the bounded iid certificate without an additional dependence argument.

## 4. ETTh1 — pending conversion/features

Source: https://github.com/zhouhaoyi/ETDataset ; reviewed fixed revision `1d16c8f4f943005d613b5bc962e9eeb06058cf07`. Repository terms CC BY-ND 4.0; keep local transformations private pending any redistribution review.

```bash
git clone https://github.com/zhouhaoyi/ETDataset.git data/manual/ETDataset
git -C data/manual/ETDataset checkout 1d16c8f4f943005d613b5bc962e9eeb06058cf07
```

Read ETT-small/ETTh1.csv, time and seven values. Declare the conventional 12/4/4 row-count split with 30×24 hours per nominal month, not literal calendar-month semantics. Normalize on source train only. Context may precede validation/test, but forecast targets must remain in the split. Use explicit temporal blocks and acknowledge dependence rather than shuffle adjacent rolling windows. This energy benchmark belongs to TPAMI, not the TII vibration table.

## 5. Japanese Vowels UCI 128 — executed raw/reference path

Source: https://archive.ics.uci.edu/dataset/128/japanese+vowels ; DOI 10.24432/C5NS47; CC BY 4.0. The official native archive is distinguished from the UEA padded representation. Archive does not supply a semantic version string; record the official endpoint, retrieval date and `acceptance.json` instead of inventing one.

```bash
mkdir -p data/manual/japanese_vowels
curl -fL 'https://archive.ics.uci.edu/static/public/128/japanese%2Bvowels.zip' -o data/manual/japanese_vowels/vowels.zip
bash paper_TPAMI/run.sh vowels-reference --archive data/manual/japanese_vowels/vowels.zip --output-dir outputs/tpami/vowels-reference-01
bash paper_TPAMI/run.sh reference-plot --csv outputs/tpami/vowels-reference-01/affine_summary.csv --output-dir outputs/tpami/vowels-reference-01/figures
```

The reader consumes ae.train, ae.test and both size_ae files directly from the archive. Twelve finite LPC coefficients per frame, native length 7–29, official 270 train and 370 test utterances, and all nine speaker block counts are checked. Source per speaker uses the first 18 utterances for fitting, next 6 validation and last 6 reserved calibration: 162/54/54. The official test partition is unchanged. This is a declared reference split, not a claim to reproduce every literature split.

LPC features advance every **6.4 ms**. The documented **10 kHz is the raw audio analysis rate**, not the feature-frame rate. Export times are relative to the first feature frame. Sequence NPZ files contain padded x, bool attention_mask, time_from_first_frame_s, label, group_id and valid length. Padding is not an extra observation. Those files are raw feature sequences, not the native generator's HSE/latent-target export format.

The executed reference uses each utterance's 12 time-mean LPC coefficients, source-fitted coordinates and onehot ridge. It saves all transformations/coefficients, reloads them, and reproduces predictions and metrics. No HSE, auxiliary conditional-moment head or VAE is substituted. Classification scores are not probabilities. Source validation selects among exactly three ridge penalties; calibration/test never fit or select. Speaker IDs are the nine classes, so this is not unseen-speaker recognition. Utterance/session dependence remains undocumented; no iid risk certificate is inferred from unique IDs.

Outputs: acceptance.json, *_sequences.npz, affine_reference.npz, source_trials.csv, predictions.csv, affine_summary.csv and SVG/PDF/PNG figures. Raw archives and sequence arrays are not committed/uploaded; CI retains numerical reference diagnostics and fitted coefficients. Use a new output directory for a distinct run.

## Remaining native feature boundary

Four raw converters remain pending. All five genuine learned HSE/reference integrations remain pending. Native generation requires tokens, attention_mask, side, side_names, targets, event_id, group_id, condition_id, z0, target_mask, query_time_s and target_map, following the existing `feature_data.py`; a speech classifier does not automatically provide a reference latent.

For optional attributed industrial transfer, use only `../../paper/experiments/DATA_DOWNLOAD_SOP.md` and the accepted PHMFactory path. Never write another parent PHM reader. Missing permissions, raw conversion, trained checkpoint and GPU capacity are distinct prerequisites and are reported separately.
