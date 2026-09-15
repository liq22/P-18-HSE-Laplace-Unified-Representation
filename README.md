# HSE–Laplace: statistically anchored industrial conditioning

This repository studies whether a fixed-budget statistical reparameterization of HSE features helps the same finite LLapDiff model. The strongest comparator sends the complete ordinary code trained by the same auxiliary supervision. A hard acquisition selector is evaluated separately from static/soft fusion; routing is not mandatory.

## Start

```bash
python -m pip install -e '.[notebooks,experiments]'
bash experiments/p19/run.sh theory
bash experiments/p19/run.sh toy --events 1024 --output outputs/p19/toy_routing.csv
```

[Paper](paper/main.md) · [Method](paper/method.md) · [Proof + Notebook](paper/theory_main.md) · [Observed results](paper/results_native.md) · [Execution goals](paper/goals/README.md) · [Data SOP](paper/experiments/DATA_DOWNLOAD_SOP.md)

## PHM data

All PHM readers, labels and splits come through PHMFactory. `external/phmfactory` records the exact main revision whose MFPT public configuration, three selected checkpoints and independent metric recomputation passed. Initialize with `git submodule update --init external/phmfactory` and follow Goal 01 in an isolated environment. The parent does not patch upstream core or maintain another MAT reader.

## Evidence boundary

Analytical studies, native-component checks, finite routing/fusion controls and the real MFPT **reference** acceptance are available. Genuine source-trained HSE/reference features, learned M/B1-aux comparisons, learned routing and the five external-domain method experiments remain pending local data/checkpoints/GPU. A command accepting feature files is not proof those files have been produced.

First local run uses one of the 8×4090 GPUs; two-GPU training is prohibited. See Goal 06. Flow Matching remains future work until posterior validity and a real sampling bottleneck are established. `formal_claim_supported: false` refers to the proposed learned method, not to an assertion that no reference execution occurred.

CSV plotting, statistics and PHM metric recomputation are available through `bash experiments/p19/run.sh --help`. Outputs belong under ignored `outputs/`; source figures are SVG/PDF/PNG generated from actual CSVs only.
