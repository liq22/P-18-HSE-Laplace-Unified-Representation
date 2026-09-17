# Goal05 — actual prediction metrics and figures

**Scope:** reference classification metrics are recomputed from predictions; additive group effects use common predeclared seeds; bounded policy certification has separate assumptions. **Products:** actual CSV, checkpoint verification, SVG/PDF/PNG and accurate Results. No repeated-window or seed pseudo-replication.

```bash
bash paper_TPAMI/run.sh reference-plot --csv outputs/tpami/vowels-reference-01/affine_summary.csv --output-dir outputs/tpami/vowels-reference-01/figures
bash paper_TPAMI/run.sh group-statistics --input /absolute/event_scores.csv --reference B1_aux --expected-seeds 0 1 2 --output outputs/tpami/effects.csv
```

**Acceptance:** reference figures show validation/test, with calibration values retained inCSV but not used for selection. Scores from ridge are not probabilities or automatically bounded proper losses. All groups within a condition have the same seed set; expected seeds catch a run missing everywhere. Classification F1 is recomputed, not averaged by window. Only measured comparable latency/memory supports a Pareto figure; a single fitting timer is insufficient.

**Failure:** reject malformed or incomplete comparisons; do not silently drop matching missing seeds. No expected curves, clipped error bars or invented CI from dependent utterances. Raw predictions and negative outcomes remain available.
