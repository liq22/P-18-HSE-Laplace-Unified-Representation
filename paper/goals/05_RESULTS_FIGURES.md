# Goal 05 — Statistics and figures

## Scope

Aggregate only retained result CSV files; plotting never starts training or simulation.

## Deliverables

- paired group-level summary CSV;
- practical-margin effect and interval for every main comparison;
- SVG, PDF and PNG from the same summary;
- Results prose that states the observed value and its claim boundary.

## Acceptance

- exact method/event-or-group/seed pairing; no silent inner-join deletion;
- windows/draws are not treated as independent units;
- source and unseen acquisition are separate;
- one group produces no fake between-group confidence interval;
- negative/null outcomes are plotted and retained;
- figures use physical size, legible text and editable vector output.

## Commands

```bash
bash experiments/p19/run.sh statistics --input /path/event_scores.csv \
  --reference B1_aux --output outputs/p19/summary.csv
bash experiments/p19/run.sh plot --input outputs/p19/summary.csv \
  --output-dir outputs/p19/figures
```

## Failure handling

If required pairs are missing, stop and repair the experiment record. Do not drop missing rows. If an interval crosses the practical equivalence margin, report uncertainty rather than declaring equality from a nonsignificant test.
