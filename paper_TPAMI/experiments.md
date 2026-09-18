# General experiments: specificity before expansion

## E0 — exact and finite-precision witnesses

Use the current same-stem main proof/Notebook and actual conditioner tests. Required controls: full-rank inverse, singular-prefix collision, affine-consumer collapse, same raw head H_A→M, and the actual float32 covariance-floor collision. Exact arithmetic and finite precision are different claims. Keep the earlier hard-route/fusion and source-shift counterexamples without making routing the new research center.

Commands: `bash paper_TPAMI/run.sh theory`; `bash paper/run.sh conditioner-tests`; with original LLapDiff installed, `bash paper/run.sh native-acceptance`. The last command uses explicitly synthetic component/loop inputs, not genuine HSE features.

## E1 — real affine reference before learned messages

The UCI128 Japanese Vowels converter/reference is implemented. Preserve original370 test utterances, source18/6/6 per speaker, native-length masks and0.0064-second LPC frame hop. Features are twelve time-mean LPC coefficients, not raw audio/HSE. Seven affine ridge models with source-only selection and serialized/restored coefficients produce21 summary rows. PCA/rotation and transported-whitening objectives must reproduce ordinary scores; unchanged whitening penalty is a different objective. Equal class decisions are a valid null result.

`vowels-reference` prepares and fits this reference; `reference-plot` reads CSV only. No confidence guarantee is inferred from unique utterance IDs because speaker/session dependence remains unresolved. This reference neither creates M nor validates conditional-moment utility.

## E2 — minimal genuine representation comparison

Freeze genuine source-trained encoder/reference targets, actual masks/side fields, source groups, target map, q, dtype, supervised head checkpoint, consumer, HPO count, validation criterion and practical margins. Main arms are B1-aux/R, same-head H_A and M. The explicit native `--arms B1_aux M head_affine` reuses one anchor and unchanged denoiser settings; original two-arm defaults remain available. Predeclare two comparisons: M−R and M−H_A. Do not report only the favorable one after testing.

The first primary task depends on the dataset. Classification uses direct label heads and fixed-ontology group-aware metrics; generation uses a declared probabilistic target and Energy Score with equal draw budgets. Native denoising loss, predicted-moment scores and task outcomes remain separate. A classifier does not become implemented merely because the data can enter a generation CLI.

## E3 — target, consumer and simple-alternative controls

| Contrast | Explanation to exclude |
|---|---|
| B1 vs B1-aux | extra statistical supervision rather than message layout |
| M vs H_A | trained affine head rather than nonlinear statistical coordinates |
| full-q PCA/orthogonal/whitening, correctly specified ridge penalty | scale/conditioning/regularization |
| same-budget learned linear/small MLP | generic nonlinear transformation |
| mean-only, covariance/mean/target shuffles; oracle moments where known | shape loss or errors carrying identity |
| two declared targets, two encoders, two finite consumer families | one privileged target/model explains the effect |
| q/dtype/total work and field consumption | hidden message channel or extra inference cost |

Vary one axis at a time, not a Cartesian hyperparameter search. Preserve original input/target access and independent groups. Check checkpoint rank and precision without retuning the head to force invertibility. Covariance-floor/score changes are named model constraints/ablations, not silent repairs. Report actual FLOPs/latency/memory only when measured under a common procedure.

## E4 — five external scientific domains

| Domain | Dataset / task | Strong controls | Current state |
|---|---|---|---|
| Clinical | PhysioNet2012 v1.0.0; irregular imputation/future query, patient grouping | CSDI, Neural CDE, t-PatchGNN, LLapDiff | official SOP; converter/features/model pending |
| Wearable | UCI HAR; subject-disjoint activity labels | linear/MLP, Conv1D, MOMENT | inertial-series preparation/features pending |
| Climate | USHCN monthly v2.5; station/time forecasting | seasonal baseline, DLinear, PatchTST, Moirai-MoE | explicitly monthly, not daily; conversion pending |
| Energy | ETTh1; chronological multivariate forecasting | DLinear, PatchTST, Moirai-MoE, compatible LLapDiff | local source preparation and targets pending |
| Speech features | Japanese Vowels;9-class speaker labels, native lengths | solved ridge and affine references; later learned consumers | real conversion/reference executed, learned M pending |

Use the official source/version/license/grouping in DATA_DOWNLOAD_SOP.md. Each dataset has a task-specific result table, not a mean of incompatible scores. More datasets alone do not create a distinct TPAMI contribution beyond the TII industrial intervention. Industrial transfer data come only through PHMFactory and remain attributed to the companion, not duplicated.

## E5 — single, static and optional dynamic policies

First compare strongest source-selected single and tuned static prediction/distribution fusion at actual cost. A dynamic hard selector is optional and must beat static fusion rather than only an arbitrary single model. Mixtures evaluate all required arms or use a declared fixed sampling budget; averaging trajectories is not automatically a mixture distribution. Moirai-MoE and AME-TS are direct expert-specialization predecessors, not proof that a new router is needed.

Fit/checkpoint/select on independent source groups; reserve fresh calibration groups when invoking the bounded finite-policy certificate. Unknown target drift remains a sensitivity allowance. Do not apply iid bounded-loss guarantees to raw Energy Score, cross-entropy, nonlinear F1 or correlated rolling windows. Declared block evaluation is empirical unless the dependence assumptions are separately justified. Unavailable official SOTA implementations remain pending with no fabricated scores.

## E6 — actual outputs and decisions

Retain raw predictions, source choices, selected checkpoints, all predeclared contrasts and per-group paired scores. Distinguish source/unseen acquisitions and seed/draw/recording units. Costs include q/dtype/bytes, fitted transforms, shared head/trunk, consumer, factorization, training updates and measured inference resources. Same q does not prove equal computation.

Multi-arm CSV comparison requires explicit `--reference` and `--candidate`. Each selected pair must retain exact event/condition/seed/group matching and common draw/sampler budgets. Nonlinear classification statistics are recomputed from predictions. CSV-only figures output SVG/PDF/PNG; no expected curves. A null M/head or M/PCA/MLP result, static-fusion win or negative target transfer completes the question and narrows the method claim.

## Immediate fixed-bank decision

Run `prediction-check` on the actual retained reference outputs before adding a classification gate to that bank. The present seven-model affine bank has no observed label disagreement, so this gate experiment is stopped for classification accuracy/macro-F1. A score-quality comparison is separately defined; it does not turn unnormalized ridge scores into a proper probability forecast. A new model family or task would require its own source-frozen comparison, not extrapolation of the current finite conclusion.

The genuine learned comparison continues to use the repository's `B1_aux`, `head_affine` and `M` from the same checkpoint. It is not replaced by this reference replay. Industrial label experiments remain in TII, direct diagnosis heads precede diffusion necessity claims, and all five general-domain protocols retain their actual integration status.
