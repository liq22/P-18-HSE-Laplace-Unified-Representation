# Goal05 — industrial metrics and plots

**Scope:** recompute nonlinear diagnosis metrics from predictions and additive scores at original-recording level. **Products:** actual CSV, paired effects, SVG/PDF/PNG and matching TII Results.

```bash
bash experiments/p19/run.sh phm-metrics --predictions /absolute/mfpt-check/predictions.csv --reference /absolute/mfpt-check/acceptance.csv --output outputs/tii/mfpt_recomputed.csv
bash paper/run.sh native-figures comparison outputs/tii/native/event_scores.csv outputs/tii/native/figures
```

**Acceptance:** complete matched records/seeds, fixed ontology, no mean of window-F1, correct group weighting, true interval endpoints and no expected curves. Plot-only commands never train. The retained reference score is not relabelled as proposed-method accuracy. General routing/certificate plots belong to TPAMI.

**Failure:** reject incomplete/duplicate pairing or nonfinite scores; retain the original files. One recording gives no invented population interval. Preserve negative effects and report insufficient independent groups.
