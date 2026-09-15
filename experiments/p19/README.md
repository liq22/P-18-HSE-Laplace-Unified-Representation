# P19-named experiment directory in the P18 paper

The historical path is retained to avoid breaking user commands. This is not a second paper or a generic benchmark framework.

`run.sh` dispatches theory, toy, PHMFactory preparation/acceptance, feature-based native external runs, official SOTA entry, selected ablations, statistics and CSV plotting. `routing.py` and `toy_routing.py` concern fixed predictors only. `statistics.py` handles additive group means; `phm_metrics.py` independently recomputes classification metrics from predictions; they are not interchangeable.

No module here imports PHMFactory internals. The revision-specific restoration/export code is isolated in `.github/phmfactory_acceptance.py` and runs in the upstream environment. External raw-data converters and genuine HSE/reference checkpoints are not provided by naming a dataset at the launcher. See the data SOP and local GPU Goal for remaining prerequisites.
