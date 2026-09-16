# Industrial data SOP — IEEE TII

All empirical datasets in this manuscript are industrial. PHMFactory is the exclusive source of PHM preparation, metadata, readers, labels and accepted splits. General clinical/wearable/climate/energy/speech datasets and their commands have moved to `../../paper_TPAMI/experiments/DATA_DOWNLOAD_SOP.md`; they are not part of the TII experiment list.

## Accepted MFPT path

Dependency `PHMbench/PHM-Vibench` main is `a0db97364e6d38a927c3ea30c643ebbb821d54d7`, unchanged in the latest check. Existing real acceptance restored all three selected checkpoints and recomputed metrics. Provider version/source and its declared CC BY-NC-SA4.0 terms are retained by PHMFactory metadata; this is not a new blanket permission to redistribute waveforms. Do not commit raw/derived signals.

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

Use a new empty acceptance output directory. Preparation creates metadata_mfpt.csv and raw/RM_007_MFPT/{train_data,test_data}/*.mat. Labels0 normal,1 inner-race,2 outer-race. Provider14 training and6 test recordings become10/4/6 train/validation/test files. Windows are2048×1. Verified separation is original File, not independently identified physical bearings or machines.

The parent acceptance uses unchanged official configuration, restores selected checkpoints, recomputes accuracy/F1 and exports PHMFactory-selected arrays. It does not produce HSE or reference-VAE checkpoints. Source-trained feature extraction is a subsequent local task; retain original groups through all transformations. Split before generating paired acquisition views, and report changes to physical duration separately from point-count changes.

## Additional industrial datasets

CWRU or other maintained PHM datasets may enter only after their own PHMFactory accepted preparation/reader/labels/split/checkpoint/metric checks. Record the actual official/provider version and license through that path. Do not write a second parent-side MAT reader or modify the upstream core to make an invalid protocol run. A download link or Dummy smoke alone is not real-data acceptance.

## Failure handling

Missing permission/data/checkpoint or upstream protocol failure blocks that dataset's result, not the rest of the paper. Preserve the failing command and existing dependency pointer. Never substitute random features and call them genuine HSE output. Manual data/feature prerequisites remain local; no target labels enter normalization, model selection or covariance-floor tuning.
