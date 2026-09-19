# Goal 05 — analysis, decision rules and figures from real artifacts

## Entry condition

Do not write Results or final performance figures from planned values. Enter this goal only after Gate 2 has complete raw artifacts; main-paper Results require Gate 3 or an explicit reduced-scope decision.

## Artifact flow

```text
PHMFactory run
→ raw predictions / posterior scores / failures / cost
→ deterministic analysis
→ tables + source CSV
→ figure source code
→ SVG / PDF / PNG
→ manuscript Results
```

A plotting command never calls model inference. Expected/reference curves are not substitutes for observations.

## Required analyses

1. Recompute class metrics from raw probabilities and labels at original-group level.
2. Recompute Energy Score/coverage from retained posterior samples or sufficient score artifacts.
3. Produce paired per-target differences for E1–E4.
4. Separate group bootstrap intervals from seed variability.
5. Report failed/missing runs and denominator changes explicitly.
6. Recompute runtime/cost Pareto from actual execution metadata.

## Result-decision table

Use these decisions before rewriting contributions:

| Observed pattern | Manuscript consequence |
|---|---|
| S-L > observed-only and S-L > S-T | diagnostic net value and Laplace incremental claim may remain |
| S-L > observed-only but S-L ≈ S-T | retain restricted conditional inference; remove Laplace performance contribution |
| posterior score improves but F1 does not | report probability-quality improvement; do not claim diagnostic gain |
| qualified ≈ geometry-only | remove claim that joint qualification is empirically indispensable in that regime |
| wrong qualification does not degrade | qualification mechanism lacks practical sensitivity; narrow/remove the claim |
| H_M ≈ budget-MLP | remove statistics-coordinate specificity claim |
| all natural samples fully eligible | natural data do not validate restriction benefit; C1 relies on controlled paired-view evidence |
| cost rises materially for small gain | report performance–latency/sample Pareto, not only the best point |

A practical effect threshold must be fixed before reading Gate-3 target results if it will be used for a materiality claim. Do not select it retrospectively.

## Figures

Follow the repository's Nature-figure workflow. Every quantitative panel must trace to source CSV generated from retained artifacts. Preserve editable vector output and plotting source. Multi-panel plots use one scientific question per figure and explicit uncertainty/statistical-unit labels.

Suggested final evidence figures are limited to what survives the decision table:

1. per-target net diagnostic effect;
2. support × time-parameterization mechanism decomposition;
3. qualification coverage–risk–utility boundary;
4. acquisition/irregularity and cost Pareto if they materially explain the method.

Do not create all four mechanically.

## Sync

Numerical analysis/plot code and allowed artifacts belong with the PHMFactory experiment implementation first. The paper repository receives final source tables/figure sources only when they are small, publication-facing and reproducible, plus exact child commit/artifact references.
