# Goal05 — actual predictions, explicit contrasts and CSV plots

## Scope and products

Use actual retained scores/predictions, not expected curves. Affine class-score tables, native Energy Score and bounded policy certificates are different estimands. Preserve source/test provenance and independent-unit limits. Outputs are numerical CSVs and editable SVG/PDF/PNG, with no model execution inside a plot command.

## Commands

```bash
bash paper_TPAMI/run.sh reference-plot --csv paper_TPAMI/assets/vowels_affine_reference.csv --output-dir outputs/tpami/affine_figures
bash paper/run.sh native-figures comparison outputs/tpami/native_control_01/event_scores.csv outputs/tpami/native_control_01/M_vs_R --reference B1_aux --candidate M
bash paper/run.sh native-figures comparison outputs/tpami/native_control_01/event_scores.csv outputs/tpami/native_control_01/M_vs_head --reference head_affine --candidate M
bash paper_TPAMI/run.sh group-statistics --input /absolute/additive_group_scores.csv --reference R --expected-seeds 0 1 2 --output outputs/tpami/group_effects.csv
```

## Acceptance

Original groups and predeclared seeds are matched. Multi-arm native files require explicit candidate/reference; selecting a pair does not delete the other source rows. Check common posterior draws/sampler steps and actual cost before interpretation. Recompute class metrics from all fixed-ontology predictions; ridge scores are not probabilities. No iid certificate or population interval is inferred from Japanese Vowels utterance IDs. Preserve whitening's unchanged classification outcome.

## Failure handling

Duplicate, missing or inconsistent paired rows/budgets fail rather than being silently joined. A score outside the certificate assumptions stays an empirical score; it is not clipped. Unknown confidence intervals are not filled. Plot only executed results, and retain null/negative effects.
