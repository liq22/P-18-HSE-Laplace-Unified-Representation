# Data download and conversion SOP

## PHM: exclusively through PHMFactory

Accepted parent dependency: `PHMbench/PHM-Vibench main` at `a0db97364e6d38a927c3ea30c643ebbb821d54d7`, checked 2026-09-15. The exact MFPT public path passed in Actions run 34765060233. Provider/source revision, source repository and declared CC BY-NC-SA 4.0 license are retained by PHMFactory metadata. This is the provider's license declaration, not a new blanket permission to redistribute original or derived waveforms. No raw data or exported waveform arrays are committed/uploaded by this project.

```bash
git submodule update --init external/phmfactory
python -m venv .venv-phm
source .venv-phm/bin/activate
python -m pip install 'torch==2.6.0' 'torchvision==0.21.0' --index-url https://download.pytorch.org/whl/cpu
python -m pip install -e external/phmfactory
phmfactory doctor
phmfactory preflight --config smoke
phmfactory demo
bash experiments/p19/run.sh phm-prepare --output /absolute/phm-data/mfpt
bash experiments/p19/run.sh phm --data /absolute/phm-data/mfpt --output /absolute/runs/mfpt-acceptance
```

Preparation creates `metadata_mfpt.csv` and `raw/RM_007_MFPT/{train_data,test_data}/*.mat`. Do not rerun into a nonempty output directory. Labels are 0 normal, 1 inner-race, 2 outer-race. The provider has 14 training and 6 test recordings; PHMFactory selects 10/4 source train/validation recordings. Windows are 2048×1. Verified independent separation is by original `File`; physical bearing identity is not established by this metadata alone.

The acceptance command runs the unchanged official config, restores each of the three best checkpoints, recomputes accuracy/F1, and exports PHMFactory-selected arrays. It does not provide HSE or reference-VAE features. Source-trained feature extraction is a subsequent local step recorded in Goal 06. No second MAT reader, alternate split or PHM core edit is permitted.

## External sources: not PHMFactory datasets

These download steps are instructions, not claims that the data were downloaded here. Keep `data/manual/` ignored. Record archive name/retrieval date, literal license text, raw folder, target, original independent key, conversion choice and source-only normalization. Do not store a second repository-level integrity system.

### 1. PhysioNet / CinC Challenge 2012, version 1.0.0

Official source: https://physionet.org/content/challenge-2012/1.0.0/ . The database page specifies Open Data Commons Attribution License v1.0; distinguish it from the article license. Each text record is one patient's first 48 hours. Static descriptors, time-stamped values and missing values are separate fields.

```bash
mkdir -p data/manual/physionet2012
cd data/manual/physionet2012
for f in set-a.tar.gz set-b.tar.gz Outcomes-a.txt Outcomes-b.txt; do
  curl -fL "https://physionet.org/files/challenge-2012/1.0.0/$f" -o "$f"
done
tar -xzf set-a.tar.gz
tar -xzf set-b.tar.gz
```

Use patient ID as the indivisible unit. For this planned protocol, deterministic source A train/validation (80/20 by sorted patient IDs) and B held-out evaluation are declared separately from any literature's alternative split. Convert time `hh:mm` to hours or seconds consistently; retain channel-specific observed masks and repeated-timestamp aggregation rules. Fit scaling on source train only. Outcomes such as in-hospital death are labels, not model inputs. For forecasting, restrict input to times before the query horizon; for imputation, declare the mask protocol. Do not conflate the two tasks.

### 2. UCI HAR, dataset 240

Official source: https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones ; DOI 10.24432/C54S4K; UCI declares CC BY 4.0.

```bash
mkdir -p data/manual/uci_har
curl -fL 'https://archive.ics.uci.edu/static/public/240/human%2Bactivity%2Brecognition%2Busing%2Bsmartphones.zip' -o data/manual/uci_har/har.zip
unzip data/manual/uci_har/har.zip -d data/manual/uci_har
```

Use the nine `Inertial Signals` channels (three body acceleration, three gyroscope, three total acceleration), not `X_train.txt`'s 561 engineered features. Each existing window has 128 samples at 50 Hz and 50% overlap. Preserve official subject-level train/test separation; derive validation by holding out source subjects, not random windows. Labels 1–6 are the six published activities; conversion to 0–5 must be stored explicitly. Stack each signal file as `[window,128,channel]`; read `subject_*.txt` and `y_*.txt` alongside it. These are already processed windows, not untouched raw recordings.

### 3. USHCN monthly v2.5

Official source and format: https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ and `readme.txt`. This is **monthly**, not the commonly used daily-USHCN irregular benchmark. Use a separate benchmark name `USHCN-monthly-v2.5`.

```bash
mkdir -p data/manual/ushcn_monthly
for v in tavg tmin tmax prcp; do
  curl -fL "https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ushcn.$v.latest.raw.tar.gz" -o "data/manual/ushcn_monthly/$v.raw.tar.gz"
done
curl -fL https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ushcn-v2.5-stations.txt -o data/manual/ushcn_monthly/stations.txt
```

`latest` is mutable; record the date-bearing inner filenames and retrieval date. Retain the official NOAA usage/citation statement rather than inventing a dataset-specific Creative Commons license. Parse station ID, year, 12 monthly fixed-width values and flags using the official readme. Mark -9999 missing, retain quality flags, temperature hundredths Celsius and precipitation tenths of millimetres per official format. Do not treat zero as missing. Align station/month across the four elements; preserve original station IDs. Freeze a chronological cutoff before training; report station-held-out and time-held-out protocols separately. Monthly target imputation/forecasting is not a reproduction of a daily result.

### 4. ETTh1 / ETT original repository

Official repository: https://github.com/zhouhaoyi/ETDataset ; reviewed `main` revision `1d16c8f4f943005d613b5bc962e9eeb06058cf07`. Its LICENSE is **CC BY-ND 4.0**. Keep locally transformed arrays private and review the terms before distributing any derivative data.

```bash
git clone https://github.com/zhouhaoyi/ETDataset.git data/manual/ETDataset
git -C data/manual/ETDataset checkout 1d16c8f4f943005d613b5bc962e9eeb06058cf07
```

Read `ETT-small/ETTh1.csv`, hourly date column and seven numerical variables. A conventional fixed 30-day-month protocol uses first 12×30×24 rows for train, next 4×30×24 for validation, next 4×30×24 for test; explicitly label this row-count convention rather than calendar-month semantics. Fit mean/std only on train. Validation/test may use prior context, but no forecast target may cross back into training. Independent uncertainty units are declared nonoverlapping time blocks, not adjacent overlapping forecast windows. Do not randomize time rows.

### 5. Japanese Vowels: UEA classification / original UCI 128

Official archive description: https://timeseriesclassification.com/description.php?Dataset=JapaneseVowels ; original data https://archive.ics.uci.edu/dataset/128/japanese+vowels , DOI 10.24432/C5NS47, UCI declares CC BY 4.0.

```bash
mkdir -p data/manual/japanese_vowels
curl -fL 'https://archive.ics.uci.edu/static/public/128/japanese%2Bvowels.zip' -o data/manual/japanese_vowels/vowels.zip
unzip data/manual/japanese_vowels/vowels.zip -d data/manual/japanese_vowels
```

The original sequences contain 12 speech coefficients over 7–29 frames, not raw audio. Parse blank-line-separated sequences from `ae.train`/`ae.test`. Labels are nine speaker identities: training has 30 sequences per speaker; test counts are 31,35,88,44,29,24,40,50,29, matching the published block order. Preserve the official 270/370 train/test assignment. Split validation within source series with a fixed declared rule. Native-length evaluation must be labelled separately from UEA's padded length-29 representation. Because speakers are the classes, this is not leave-speaker-out generalization.

## Feature conversion and acceptance before GPU

For each external dataset the local conversion must retain original group IDs, times, explicit masks, raw labels/targets, source split and transformation notes. It then exports genuine frozen HSE/reference features in the **existing** `experiments/learned_conditioning/feature_data.py` fields: tokens, attention_mask, side, side_names, targets, event_id, group_id, condition_id; native generation also requires z0, target_mask, query_time_s and target_map. A classification-only dataset is not silently assigned a latent-generation result without training a compatible source reference encoder.

No universal raw-data converter or accepted feature checkpoint for these five domains is shipped by this update. Implement each declared local conversion and one parsed-batch/split check before using the native external entry. Missing data, export code or checkpoint is a named prerequisite, not a GPU failure and not an excuse to substitute synthetic features. The first learned stop point remains the genuine HSE/reference export plus local GPU pilot.
