# Data download and split SOP

A download entry is not evidence that a dataset has been integrated. Every dataset moves through: official-source audit → license audit → raw download → independent-unit definition → split-before-windowing → conversion → one smoke batch → full experiment.

## 1. Primary PHM candidates

### CWRU Bearing Data Center

- Official source: Case Western Reserve University Bearing Data Center, `https://engineering.case.edu/bearingdatacenter/`.
- Official facts: drive-end vibration exists at 12 kHz and 48 kHz; fan-end data are 12 kHz; files are MATLAB; fault location/diameter and motor load/speed are documented.
- License: the official pages retrieved for this revision do **not** expose a clear redistribution license. Human license verification is required before redistributing raw files; local academic analysis may proceed only under the site's terms.
- Local directory: `data/manual/cwru/raw/`.
- Download: follow the official `12k Drive End Bearing Fault Data`, `48k Drive End Bearing Fault Data`, normal-baseline and `Download a Data File` pages. Do not scrape mirrors into the canonical dataset.
- Labels: healthy / inner-race / ball / outer-race; retain fault diameter, outer-race position, motor load and rpm as metadata rather than silently merging them into the class.
- Independent unit: original official MATLAB recording; if a single file contains several sensor channels, they remain one recording group.
- Split: split original recordings first. Only then window or construct anti-aliased rate/missingness views. Never place windows from the same original recording in different sets.
- Conversion target: an untracked metadata table with `recording_id,label,fault_size,load_hp,rpm,sensor_position,native_sample_rate,path` and arrays exported through the paper/PHMFactory public interface.

### Paderborn University Bearing DataCenter

- Official source: `https://mb.uni-paderborn.de/en/kat/research/bearing-datacenter`.
- License on official page: CC BY-NC 4.0; academic noncommercial use allowed with attribution.
- Signals: vibration and motor current; operating conditions and bearing states are documented by the official DataCenter.
- Local directory: `data/manual/paderborn/raw/`.
- Download: use the official Bearing DataCenter download links; do not substitute Kaggle/GitHub mirrors in the main experiment.
- Labels: freeze the exact bearing-state mapping from official metadata before training; artificial/real damages and operating conditions remain separate metadata fields unless a manuscript table explicitly merges them.
- Independent unit: physical bearing/run/measurement file according to official organization; split at the highest available bearing/run identity before windows.
- Split: no windows or repeated operating points from the same independent bearing/run may cross sets.

## 2. External benchmark families

### PhysioNet/CinC Challenge 2012 — irregular clinical

- Official source/version: PhysioNet Challenge 2012 v1.0.0.
- Official command:

```bash
mkdir -p data/manual/physionet2012
wget -r -N -c -np https://physionet.org/files/challenge-2012/1.0.0/ \
  -P data/manual/physionet2012
```

- Official data consist of ICU stays; patient/record ID is the independent unit.
- Task: mortality classification or the exact reproduced forecasting/imputation task; do not mix Challenge scoring with unrelated objectives.
- Split: patient records are indivisible. No target-record normalization fit.
- License: verify the dataset page's current license display before redistribution; store only derived metadata in Git.

### UCI HAR — subject-level sensor classification

- Official source: UCI ML Repository dataset 240, DOI 10.24432/C54S4K.
- License: CC BY 4.0.
- Official facts: 30 subjects, six activities, smartphone accelerometer/gyroscope sampled at 50 Hz; original split is by volunteers.
- Download option:

```bash
python - <<'PY'
from ucimlrepo import fetch_ucirepo
fetch_ucirepo(id=240)
print('UCI HAR fetched through official UCI client')
PY
```

- Independent unit: subject. Preserve the official train/test subject separation unless the external protocol explicitly declares another subject-level split.

### USHCN v2.5 — climate/environment

- Official source: NOAA/NCEI `https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/`.
- Version: v2.5; the `latest` archives are mutable and must be recorded by retrieval date in the run note.
- Example:

```bash
mkdir -p data/manual/ushcn
wget -c https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ushcn.tavg.latest.raw.tar.gz \
  -O data/manual/ushcn/ushcn.tavg.latest.raw.tar.gz
wget -c https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ushcn-v2.5-stations.txt \
  -O data/manual/ushcn/ushcn-v2.5-stations.txt
```

- Independent unit: station for cross-station evaluation; chronological blocks for forecasting. Never randomly mix future observations into training.
- License/use: NOAA public-data terms apply; preserve source citation and retrieval date.

### ETT — regular long-horizon forecasting

- Official project source: `https://github.com/zhouhaoyi/ETDataset`.
- Data period documented by the project: 2016/07–2018/07; ETT-small contains transformer load and oil temperature.
- Download:

```bash
git clone --depth 1 https://github.com/zhouhaoyi/ETDataset.git data/manual/ETDataset
```

- Split: use the reproduced baseline's chronological split; do not reshuffle rows.
- License: verify the repository's current license file before redistribution; Git stores no copied dataset.

### UEA multivariate time-series classification archive

- Official archive: `https://timeseriesclassification.com/`.
- The site hosts the 2018 UEA multivariate archive and exposes datasets through the `aeon` toolkit.
- Example:

```bash
python -m pip install aeon
python - <<'PY'
from aeon.datasets import load_classification
X, y, meta = load_classification('BasicMotions', meta_data=True)
print(type(X), len(y), meta)
PY
```

- Split: preserve archive train/test unless a dataset-specific paper requires another official protocol.
- Independent unit: original case/series.
- License: the archive hosts datasets from multiple contributors; verify each selected dataset's own terms before redistribution.

## 3. Optional families

- Weather/Electricity long-horizon data may be added only after an official or original-project download/usage path is frozen.
- TIME-IMM is optional; use only after exact release and license are checked.
- Additional PHM datasets require the same recording-level audit and may not be introduced merely to rescue a failed CWRU/Paderborn result.

## 4. Required local note for every manual dataset

Create an untracked `DATA_NOTE.md` beside the local data with: official source; retrieval date/version; license statement; raw directory; label mapping; independent unit; train/validation/test group lists or the script that deterministically generates them; normalization fit set; conversion command; exclusions and reasons.

The note is evidence for the local run. It is not a hash/checksum receipt and is not committed with private/local paths.
