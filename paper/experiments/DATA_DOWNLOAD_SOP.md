# Data SOP — PHM data through PHMFactory, external benchmarks through official sources

A download or metadata row is not evidence that a dataset is integrated. This paper uses **PHMFactory as the only PHM data execution path**. The parent paper repository does not maintain a second CWRU/Paderborn/MFPT reader or a duplicate PHM metadata table.

## 1. PHM data authority: PHMFactory

Current reviewed upstream: `PHMbench/PHM-Vibench` `main`. Re-read the exact revision before execution. PHMFactory's own data documentation states that non-Dummy experiments use a local data root containing a metadata file and `raw/<Name>/<File>`, with dataset readers under its data factory. It also lists its maintained external data sources (ModelScope/Hugging Face) but explicitly warns that source availability and licensing must be checked before publication or redistribution.

The paper therefore follows this contract:

```text
official/raw source or PHMFactory-maintained data source
        ↓
PHMFactory metadata + public reader/config
        ↓
PHMFactory public preflight / execution
        ↓
exported waveform or representation arrays + label + acquisition metadata
+ original recording/bearing/run group + frozen split
        ↓
experiments/p19 and paper statistics
```

The paper never imports `src.data_factory`, factories, registries or reader internals. A paper-specific need that PHMFactory cannot represent is reported as BLOCKED or upstream issue; the parent does not patch PHMFactory core.

### Required PHMFactory local run note

Keep an untracked `PHM_DATA_NOTE.md` with:

- exact PHMFactory commit;
- dataset `Name`/metadata row or accepted config;
- original source and license/usage statement as recorded/verified by PHMFactory maintainers;
- local `data.data_dir` and `data.metadata_file` (do not commit machine-local absolute paths);
- label mapping;
- independent unit: machine / physical bearing / run / original recording;
- train/validation/test group lists or deterministic split command;
- acquisition descriptors used by this paper: sampling rate, observed duration, channel/mask fields and any declared quality variable;
- normalization fit set;
- exact PHMFactory preflight/run command;
- selected checkpoint and primary-metric recomputation command;
- export command/path for the arrays consumed by `experiments/p19`.

### Acceptance order

```bash
python -m pip install -e /absolute/PHM-Vibench
phmfactory doctor
phmfactory preflight --config smoke
phmfactory demo

# Then the exact accepted real-data config, for example only after its metadata/data exist:
phmfactory preflight \
  --config /absolute/PHM-Vibench/configs/demo/01_cross_domain/cwru_dg.yaml \
  --override data.data_dir=/absolute/phm-data \
  --override data.metadata_file=metadata.xlsx

phmfactory \
  --config /absolute/PHM-Vibench/configs/demo/01_cross_domain/cwru_dg.yaml \
  --override data.data_dir=/absolute/phm-data \
  --override data.metadata_file=metadata.xlsx
```

The CWRU demo above is only a wiring example until its exact current-source labels, split, checkpoint and metrics are accepted. At the reviewed upstream revision the config itself is still marked a draft. Do not promote it merely because it parses.

### PHM split rule

PHMFactory must expose or allow auditing the original independent group **before** paper windows/views are created. If PHMFactory's executed split cannot guarantee that windows from one original recording/bearing/run stay in one set, the paper PHM slice is rejected. The parent repo must not reconstruct a different split after the fact and call it the PHMFactory result.

## 2. External non-PHM benchmark families

These are intentionally outside PHMFactory and follow their own official sources.

### PhysioNet/CinC Challenge 2012

- Official version: PhysioNet Challenge 2012 v1.0.0.
- Independent unit: patient/record.

```bash
mkdir -p data/manual/physionet2012
wget -r -N -c -np https://physionet.org/files/challenge-2012/1.0.0/ \
  -P data/manual/physionet2012
```

Verify the current dataset license/credential terms on PhysioNet before redistribution. Keep patients indivisible across splits.

### UCI HAR

- Official UCI dataset id 240, DOI 10.24432/C54S4K.
- License shown by UCI: CC BY 4.0.
- Independent unit: subject; preserve the official subject-level train/test separation unless a reproduced protocol explicitly differs.

```bash
python -m pip install ucimlrepo
python - <<'PY'
from ucimlrepo import fetch_ucirepo
fetch_ucirepo(id=240)
print('UCI HAR fetched through the official UCI client')
PY
```

### USHCN v2.5

- Official NOAA/NCEI source: `https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/`.
- Independent unit: station; chronological time blocks for forecasting.

```bash
mkdir -p data/manual/ushcn
wget -c https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ushcn.tavg.latest.raw.tar.gz \
  -O data/manual/ushcn/ushcn.tavg.latest.raw.tar.gz
wget -c https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ushcn-v2.5-stations.txt \
  -O data/manual/ushcn/ushcn-v2.5-stations.txt
```

Record retrieval date because `latest` is mutable.

### ETT

- Original project: `https://github.com/zhouhaoyi/ETDataset`.
- Use the reproduced chronological split; do not randomize time rows.

```bash
git clone --depth 1 https://github.com/zhouhaoyi/ETDataset.git data/manual/ETDataset
```

Verify the current repository license before redistribution.

### UEA multivariate time-series classification archive

- Official archive: `https://timeseriesclassification.com/`.
- Independent unit: original case/series.
- Preserve archive train/test splits where valid; verify each selected dataset's terms.

```bash
python -m pip install aeon
python - <<'PY'
from aeon.datasets import load_classification
X, y, meta = load_classification('BasicMotions', meta_data=True)
print(type(X), len(y), meta)
PY
```

## 3. Common external-data note

For every non-PHM external dataset keep an untracked `DATA_NOTE.md`: official source, version/retrieval date, license, raw path, label/target definition, independent unit, split, normalization fit set, conversion command and exclusions.

No dataset is marked integrated until a parsed batch, split audit and task-compatible baseline run have succeeded.
