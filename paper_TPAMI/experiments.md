# Experiments — general study, separate from TII industrial tables

## G0. Theoretical witnesses and fixed-policy studies

Execute the moved `theory_main.ipynb` and new `theory/policy_certificate.ipynb`. Preserve earlier no-crossing/soft-fusion and target-reversal experiments. New binary Brier study: source-fit512 events, independent calibration64 or2048, test4096, three simulator seeds; ordinary singles/static reference/acquisition selector. Full rules, utility penalties and source/target laws are frozen in `certified_selection_demo.py`. Reversal and shift-allowance cells use identical observations and fitted policies. Required output: real group-score CSVs, 24-row summary, negative results and CSV-only figures. This is a finite statistical experiment, not HSE training.

## G1. Target, consumer and budget profile

Use genuine source-frozen features and targets. Compare B1 (ordinary), B1-aux (same statistical supervision), M0 (moment-only) and M (moments plus ordinary tail). Main first contrast remains M/B1-aux. Use at least two encoder families and two finite consumer families; change only one axis per ablation. Each target function, q, optimizer budget, checkpoint rule and actual side input is frozen before evaluation. Keep the original HSE–LLapDiff instance as an attributed anchor, not the whole general contribution.

Targets: probabilistic future/missing measurements for forecasting/imputation; fixed-ontology probabilities for classification. Do not force a latent-generation metric onto a classification dataset without a declared source reference encoder. Consumers: linear vs small nonlinear diagnostic/prediction heads; native LLapDiff vs Gaussian/finite-mixture probabilistic head. Exact target and loss remain common within each comparison.

## G2. Single, static and dynamic policy comparison

Fit single models and static/gate rules on source data, reserving independent original groups for final policy calibration. The strongest source-selected static predictive mixture is a reference, not merely a weak arbitrary average. Compare fixed-policy hard selection directly with that reference. Add soft fusion as a distinct trained policy, not as a theorem-covered reweighting of fixed losses. For iid bounded group scores apply the declared calibration rule; otherwise report empirical held-out/blocked estimates and do not claim its theorem.

Hypotheses: conditional risk crossings can create hard-selection opportunity but not guaranteed benefit over static fusion; independent calibration can reject noisy apparent gains; target ordering reversal invalidates zero-shift transport. These are falsifiable checks, not evidence that every domain needs a router.

## G3. Five external domains

| Domain | Source/version | Primary task and independent unit | Strong controls | Current integration |
|---|---|---|---|---|
| Clinical | PhysioNet2012 v1.0.0 | irregular imputation/future queries; patient record | CSDI, Neural CDE, t-PatchGNN, LLapDiff | official SOP; actual conversion/features pending |
| Wearable | UCI HAR240 | six-class activity; subject | linear/MLP, matched Conv1D, MOMENT | source inertial series and subject split pending |
| Climate | USHCN monthly v2.5 | chronological station forecasting | seasonal/last-value, DLinear, PatchTST, Moirai-MoE | explicitly monthly, not daily; conversion pending |
| Energy | ETTh1 original revision | chronological multivariate forecasting | DLinear, PatchTST, Moirai-MoE, compatible LLapDiff | local raw preparation/features pending |
| Speech features | UCI128 / Japanese Vowels | nine-class speaker recognition; original utterance | matched feature head, MOMENT, irregular model | native variable length; conversion pending |

Each family has a task-specific table and group count. Do not pool incompatible scales/metrics or select the five domains after seeing results. PHMFactory may supply an optional industrial transfer check **attributed to TII**, not a sixth independent claim using the same measurements. All new raw conversions must preserve labels, masks, units, original groups and source-only preprocessing.

## G4. SOTA and nearest-neighbor eligibility

Moirai-MoE (ICML2025) is a direct sparse-specialization comparator; AME-TS (2026 preprint) is a direct supervised-structure routing neighbor, with implementation status checked before reproduction. Include task-compatible MOMENT/UniTS, PatchTST/DLinear, t-PatchGNN/Hi-Patch/HyperIMTS/ContiFormer/Neural CDE, and CSDI/LLapDiff for their proper tasks. Do not assert all are universally SOTA. Record official version, train/pretraining access, task adaptation and actual budget. A unavailable model stays pending; a --help command is not a model result.

## G5. Minimal ablations

| Axis | Contrast | Competing explanation |
|---|---|---|
| Loss | auxiliary none/shared; native parameterization/normalization; covariance score components | extra supervision or objective mismatch |
| Representation | R/M0/M, true moments where oracle exists, tail shuffle | distribution shape lost or errors encode identities |
| Structure | encoder family, consumer capacity, target and q | one architecture or privileged target explains gain |
| Policy | best single, tuned static, hard, separately trained soft; descriptor shuffle | ordinary ensembling rather than routing |
| Statistics | independent calibration vs reused validation; whole groups vs windows | selection optimism/pseudoreplication |
| Explanation | actual field consumption, target ranking and source/unseen residuals | stored fields not used; statistical not causal explanation |
| Cost | training/head/preprocessing/experts/gate/draws and measured latency | gains purchased with unreported work |

No full Cartesian search before one genuine comparison. Preserve equal/worse policies. A second TPAMI paper is not justified solely by duplicating TII training across this table.

## Outputs and decisions

Keep fit/validation/calibration/test membership fixed by original groups. For continuous time datasets, time blocks alone do not establish iid observations; temporal results and certificates are reported separately. Learned performance requires genuine encoder/reference checkpoints and local GPU runs. Raw external conversion remains a named CPU prerequisite, not falsely completed by a feature-file CLI. Figures read retained CSVs only; generic mathematical tests are not empirical real-data results.
