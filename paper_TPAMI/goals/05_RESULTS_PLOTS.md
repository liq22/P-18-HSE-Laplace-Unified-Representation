# Goal05 — paired results and independent vector plots

**Scope:** bounded group-policy certification is different from empirical native Energy Score or nonlinear macro-F1. **Products:** exact decision JSON, observed CSV summaries, source/test separation, SVG/PDF/PNG with editable text and actual negative outcomes.

```bash
bash paper_TPAMI/run.sh statistics \
 --input outputs/tpami/selection/complementary_n2048_seed0_group_scores.csv \
 --reference static_reference --margin .01 --output outputs/tpami/selection/decision.json
bash paper_TPAMI/run.sh plot --csv paper_TPAMI/assets/selection_summary.csv --output-dir outputs/tpami/figures
# Existing additive event CSVs use the shared empirical, not certificate, route:
bash paper_TPAMI/run.sh group-statistics --input /absolute/event_scores.csv --reference B1-aux --output outputs/tpami/effects.csv
```

**Acceptance:** no target data select a policy; duplicates/incomplete pairs fail; costs are declared versus measured; all24 finite-study rows are plotted with seeds shown descriptively. Raw Energy Score is never called bounded by normalization after the fact. Figures never trigger training/simulation.

**Failure:** incomplete data or unsupported loss blocks certification. Keep empirical results with their real limitations rather than invent intervals or clip inputs. With one group no population interval is asserted. For nonlinear classification recompute the metric from predictions, not average per-window F1.
