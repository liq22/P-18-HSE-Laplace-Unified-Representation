# Results — general study

## 1. Migrated evidence, not a new independent experiment

`assets/routing_controls.csv` is the unchanged prior fixed-predictor CPU study formerly stored in the TII folder. It showed a hard source route losing to static fusion in the crossing cell (MSE0.178489 vs0.127112) and becoming worse than the selected single under target reversal (0.327892 vs0.254393). The move assigns general evidence to the correct manuscript; it does not multiply the number of observations or prove a new method.

## 2. Independent finite-policy calibration study

Executed command:

```bash
bash paper_TPAMI/run.sh toy --seeds 0 1 2 --calibration-groups 64 2048
```

Four settings × two calibration sizes × three simulator seeds produce24 summary rows. Each run first fits its static reference/hard rule on512 source events, then uses independent calibration groups and4096 test events. Policies predict Bernoulli probabilities. Score is binary Brier; cost penalties0.01/0.0105/0.02 are declared toy utilities, not measured GPU costs. Family size3, alpha0.05 and practical margin0.01 are fixed.

| Calibration n | Scenario | Selected policies across3 seeds | Observed test net gains |
|---:|---|---|---|
|64|all four settings|reference/reference/reference|0,0,0|
|2048|same best|reference/reference/reference|0,0,0|
|2048|complementary|hard/hard/hard|0.10231250,0.10158008,0.09908984|
|2048|target reversal, assumed beta=0|hard/hard/hard|-0.25305859,-0.25628125,-0.26331250|
|2048|same reversal data, beta=0.4|reference/reference/reference|0,0,0|

The simultaneous radii are0.3576985708 for64 groups and0.0632327713 for2048. Small calibration samples do not certify a gain even when the source policy is beneficial. The zero-shift certificate selects an unfavorable policy when target conditional order reverses; its transfer assumption is false. Reusing the identical observations with a declared0.4 shift allowance retains the reference. This demonstrates the boundary, not an ability to estimate target drift without data.

All24 rows are retained in `assets/selection_summary.csv`; group-level score files are generated under ignored outputs. Three simulator seeds are descriptive repetitions, not an extra confidence interval or thousands of independent trained models. Source certification does not guarantee a favorable finite test realization.

## 3. Current evidence level

Local selected-source validation executed10 new behavioral tests, the certificate Notebook and both actual CSV-generated figures. Combined-repository CI must separately validate the new branch before merge; its actual completion is recorded in the PR, not prefilled here. The moved generic theorem remains an antecedent-backed proof and witness; the certificate is a classical finite-family specialization.

No genuine multi-domain HSE/reference checkpoint, learned single/static/dynamic comparison, SOTA run or TPAMI method advantage has been obtained in this study. The MFPT reference is owned by the companion TII result file and is not copied as a new general benchmark score.

## 4. Planned result tables

One table per domain and task: actual target/consumer/q, best single, tuned static reference, hard policy, calibration decision where valid, independent group count, primary metric and cost. A second table compares encoder/consumer/target/budget axes; an uncertainty table states which assumptions permit a certificate and which allow only empirical blocked estimates. Do not populate these tables until actual source-trained models and official data protocols run. Failure, non-selection, equality and negative transfer are retained outcomes.
