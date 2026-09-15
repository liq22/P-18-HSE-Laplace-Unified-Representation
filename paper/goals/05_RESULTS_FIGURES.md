# Goal 05 — recompute statistics and draw from actual CSV

## Scope

Additive event losses and nonlinear classification metrics use different estimators. Group resampling reflects original recording variation conditional on the evaluated seed set. Keep true interval endpoints even if a bootstrap interval does not contain the point estimate.

## Products

Recomputed reference metrics, paired group-effect CSV and editable SVG/PDF/PNG. Keep null/negative effects and number of original groups in labels. Plot commands never train or simulate.

## Commands

```bash
bash experiments/p19/run.sh phm-metrics --predictions /absolute/mfpt-check/predictions.csv --reference /absolute/mfpt-check/acceptance.csv --output outputs/p19/mfpt_recomputed.csv
bash experiments/p19/run.sh statistics --input outputs/p19/toy_routing_events.csv --reference best_single --output outputs/p19/toy_effects.csv --bootstrap 1000
bash experiments/p19/run.sh plot --input outputs/p19/toy_effects.csv --method hard_source_route --output-dir outputs/p19/hard-route-figures
bash experiments/p19/run.sh plot --input outputs/p19/toy_effects.csv --method static_prediction_fusion --output-dir outputs/p19/static-figures
# Native pilot output has a different, explicit column contract:
bash paper/run.sh native-figures comparison outputs/native-pilot/event_scores.csv outputs/native-pilot/figures
```

## Acceptance

Duplicate/missing pairs fail rather than disappearing in a join. Unequal window counts cannot change recording weights. Macro-F1 is recomputed from pooled weighted confusion, never treated as a per-window additive metric. Figures are rendered and checked at final size; text remains editable in SVG/PDF. The reference nature-figure skill informs presentation only, not statistical conclusions.

## Failure handling

Malformed CSV or mismatched groups/budgets: stop that comparison. One group: report its descriptive estimate with undefined interval, do not invent population uncertainty. Keep raw outputs and explain the missing prerequisite instead of plotting expected curves.
