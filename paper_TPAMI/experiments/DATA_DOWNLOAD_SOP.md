# Official external data and conversion SOP — TPAMI

These five general-domain datasets moved out of the industrial TII paper. Download instructions are not evidence of actual download, parsing or model integration. Keep raw/derived arrays local under ignored `data/manual/`; retain a short source/retrieval/version/license/split note per dataset, not a new registry.

## 1. PhysioNet / CinC Challenge2012 v1.0.0

Official source: https://physionet.org/content/challenge-2012/1.0.0/ . Database terms: Open Data Commons Attribution License v1.0 as declared by the database, separate from article licensing. Each record is one ICU patient's first48 hours. Historical challenge prose says test outcomes were withheld; the current file list contains Outcomes-a/b/c. Preserve that distinction.

```bash
mkdir -p data/manual/physionet2012
cd data/manual/physionet2012
for f in set-a.tar.gz set-b.tar.gz Outcomes-a.txt Outcomes-b.txt; do
  curl -fL "https://physionet.org/files/challenge-2012/1.0.0/$f" -o "$f"
done
tar -xzf set-a.tar.gz
tar -xzf set-b.tar.gz
```

Conversion: parse RecordID, static descriptors and channel-specific timestamp/value observations; convert hh:mm consistently, retain missing masks and declare repeated-timestamp reduction. Source normalization uses source fit only. Use patient as indivisible unit; set A supplies predeclared fit/validation/calibration partitions, set B the held-out evaluation. Freeze the patient allocation before models. This is the paper's declared protocol, not an asserted reproduction of every published split. Future queries only use earlier history; random imputation is a separate task. Mortality/SAPS/SOFA/outcomes are not hidden inference inputs.

## 2. UCI HAR240

Source: https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones ; DOI10.24432/C54S4K; UCI license CC BY4.0.

```bash
mkdir -p data/manual/uci_har
curl -fL 'https://archive.ics.uci.edu/static/public/240/human%2Bactivity%2Brecognition%2Busing%2Bsmartphones.zip' -o data/manual/uci_har/har.zip
unzip data/manual/uci_har/har.zip -d data/manual/uci_har
```

Use nine Inertial Signals channels, 128 samples per existing50-Hz window, with published50% overlap. Do not substitute X_train.txt's561 engineered features for time series. Read subject_*.txt and y_*.txt alongside signals; labels1–6 map explicitly to0–5. Preserve official subject-disjoint train/test. Source validation/calibration hold out subjects, not windows. The small number of subjects limits certification power; do not turn windows into independent samples to obtain a positive bound.

## 3. USHCN monthly v2.5

Official source: https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ and its readme. This protocol is **USHCN-monthly-v2.5**, not the common daily irregular benchmark. Retain NOAA's official usage/citation statement; no invented Creative Commons license.

```bash
mkdir -p data/manual/ushcn_monthly
for v in tavg tmin tmax prcp; do
  curl -fL "https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ushcn.$v.latest.raw.tar.gz" -o "data/manual/ushcn_monthly/$v.raw.tar.gz"
done
curl -fL https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ushcn-v2.5-stations.txt -o data/manual/ushcn_monthly/stations.txt
```

Because latest is mutable, record the dated inner filenames and retrieval date. Parse fixed-width station/year/month values and quality flags according to the official readme; -9999 is missing, zero is a possible observation. Preserve temperature/precipitation units and original station IDs. Align station-month across channels. Freeze chronological cutoffs and optional station holdouts separately. Adjacent blocks are not assumed iid; no Hoeffding certificate from timestamps alone.

## 4. ETTh1

Official source: https://github.com/zhouhaoyi/ETDataset ; fixed reviewed revision `1d16c8f4f943005d613b5bc962e9eeb06058cf07`. The repository license is CC BY-ND4.0. Keep transformations local and inspect terms before distributing derivatives.

```bash
git clone https://github.com/zhouhaoyi/ETDataset.git data/manual/ETDataset
git -C data/manual/ETDataset checkout 1d16c8f4f943005d613b5bc962e9eeb06058cf07
```

Read ETT-small/ETTh1.csv, date and seven values. Declare the conventional row-count12/4/4 split using30×24 hours per month, not actual calendar months. Fit scaling only on train. Context may precede validation/test, but forecast targets must remain in the corresponding split. Use declared nonoverlapping temporal evaluation blocks with dependence qualifications, not randomly permuted rolling windows. The general paper owns this energy benchmark; it is not added to the TII industrial vibration table.

## 5. Japanese Vowels

Official source: https://archive.ics.uci.edu/dataset/128/japanese+vowels ; DOI10.24432/C5NS47; CC BY4.0. UEA description: https://timeseriesclassification.com/description.php?Dataset=JapaneseVowels . Preserve the original-source versus padded-UEA representation distinction.

```bash
mkdir -p data/manual/japanese_vowels
curl -fL 'https://archive.ics.uci.edu/static/public/128/japanese%2Bvowels.zip' -o data/manual/japanese_vowels/vowels.zip
unzip data/manual/japanese_vowels/vowels.zip -d data/manual/japanese_vowels
```

Parse blank-line-separated ae.train/ae.test sequences:12 speech coefficients,7–29 frames; these are extracted speech features, not raw audio. Training is270 sequences,30 per speaker. Published test block counts31,35,88,44,29,24,40,50,29 identify9 speaker labels across370 sequences. Preserve official train/test assignment; define source validation/calibration before fitting. Speaker is the class, so this is not leave-speaker-out recognition. Original utterance/session dependence may be incompletely documented; series IDs alone do not establish iid groups. Label native-length versus padded representation explicitly.

## Shared conversion/feature boundary

Each converter must leave original group/utterance/patient IDs, actual timestamps/masks, labels, source-only scaling and frozen split. Genuine native generation exports follow existing `experiments/learned_conditioning/feature_data.py`: tokens, attention_mask, side, side_names, targets, event_id, group_id, condition_id, and for generation z0/target_mask/query_time_s/target_map. Classification does not acquire a latent-generation target automatically.

Raw converters, source encoder/reference checkpoints and five learned integrations are not delivered merely by naming these sources. Implement the declared converter and one real parsed-batch/split check per domain before GPU use. Missing dependencies remain explicit. For an optional industrial transfer check use only the accepted PHMFactory path in `../../paper/experiments/DATA_DOWNLOAD_SOP.md`, attribute it to the TII companion and do not duplicate its result as a new contribution.
