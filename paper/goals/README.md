# IEEE TII industrial execution goals

This paper repository owns the formulation, manuscript, publication figures and basic mathematical/interface witnesses. `external/phmfactory` owns the learned P18 model, data/config integration, training/evaluation and experiment artifacts. Do not build a second runtime in the paper repository.

## Execution order

1. [01 Sync](01_SYNC_PHMFACTORY.md): qualify and synchronize the exact PHMFactory child revision.
2. [02 Theory](02_THEORY_MANUSCRIPT.md): retain only theory that explains mechanism, failure boundary or measurable consequence.
3. [03 Gate 0 Data](03_DATA.md): prove that each dataset actually instantiates the scientific object; issue GO/PARTIAL/NO-GO.
4. [04 Gate 1–3 Experiments](04_EXPERIMENTS.md): one real source batch → one target/seed decisive screen → frozen full experiment.
5. [05 Results/Figures](05_RESULTS_FIGURES.md): analysis and figures only from retained real artifacts.
6. [06 Local GPU](06_LOCAL_GPU_8X4090.md): one GPU per run; parallelize independent jobs only after protocol freeze.
7. [07 Local Agent](07_LOCAL_AGENT_EXECUTION.md): copyable execution prompt for the local Agent.

## Stop rules

Do not proceed to full LODO merely because files exist. Gate 0 must first establish label ontology, independent statistical units, reference/pairing semantics and which contributions each dataset can test. Gate 1 must then execute the final learned path through PHMFactory. Gate 2 must run one target × one seed × all decisive cells before the full registered matrix begins.

A slice is scientifically complete when its executable/configuration, actual command/artifact and claim boundary all exist. Negative results, ties, ineligible datasets and failed runs are valid outcomes. Synthetic witnesses, literature scores and data-path smoke tests are not learned industrial performance.

Normal reviewed PR workflow only; preserve master, unrelated branches, prior negative results and TPAMI scope.
