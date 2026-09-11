# Paper workspace — IEEE TII track

Start with [GOAL.md](GOAL.md) and the concise map in [goals/README.md](goals/README.md).

Scientific authority:

- `main.md`: evidence-limited abstract, Introduction and paper identity;
- `notation.md`: main symbols, assumptions and estimands;
- `theory_main.md`: three main-paper propositions and falsifying controls;
- `contributions.md`: candidate contribution / promote / stop ledger;
- `related_work.md`: nearest-neighbor boundary;
- `method.md`: actual conditioner, matched baselines, static fusion and conditional routing;
- `experiments.md`: TII evidence chain;
- `results_native.md`: actual results only; empty tables stay empty;
- `experiments/DATA_DOWNLOAD_SOP.md`: external/manual data authority.

Detailed proofs remain under `../theory/`; do not duplicate them in multiple paper files. The current native LLapDiff component reference is revision `0631e65cbac59d23822205573ebc7e180ecf0487`.

## Existing native acceptance

```bash
bash paper/run.sh setup
bash paper/run.sh setup-neural
export LLAPDIFF_ROOT=/absolute/path/to/LLapDiffusion
bash paper/run.sh setup-native
bash paper/run.sh native-acceptance
```

This exercises explicit synthetic component fixtures and does not claim real HSE/reference execution.

## P19 experiment entry

```bash
bash experiments/p19/run.sh theory
bash experiments/p19/run.sh toy
# Real data only after the corresponding Goal acceptance:
bash experiments/p19/run.sh phm
bash experiments/p19/run.sh external
bash experiments/p19/run.sh sota
bash experiments/p19/run.sh ablation
bash experiments/p19/run.sh statistics --input results.csv --reference B1_aux --output summary.csv
bash experiments/p19/run.sh plot --input summary.csv --output-dir figures
```

Paper code never imports PHMFactory internals. The `external/phmfactory` submodule is intentionally absent until `goals/01_SYNC_PHMFACTORY.md` passes a real-data check on the exact upstream revision. Download entry points are not evidence that data are integrated.
