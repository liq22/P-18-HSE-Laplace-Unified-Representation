# Experiments: native acceptance before expansion

## A. Integrate the current branch, not an obsolete overlay

Read the actual PR head, AGENTS and existing implementations. Preserve the completed shared-supervision path and all earlier correct Gaussian/shape controls. Do not apply the old 799f2cf-based ZIP over a newer branch. Run all current tests and the complete same-stem Notebook corpus at the same final revision. Counts from different revisions are not additive.

The theory stage is not another open-ended review. Only append implementation-relevant implications to existing Theory 12 and its Notebook. No new theory number, manager, registry or framework is required.

## B. Original LLapDiff component and real upstream exports

The original component must be installed from a declared checkout. First run `native-acceptance` on explicit synthetic fixtures. Verify shared auxiliary gradients, frozen states, actual field consumption, and exact native-loss conventions on one batch. The native scheduler export is separate from the realized batch-normalized objective.

Then run a genuine exported batch. A source-trained HSE and frozen reference encoder must actually have produced the inputs. An interface check on synthetic features is not a substitute. The export note records original source classes and revisions, checkpoints, preprocessing, deterministic patch selection, normalization state, physical units and original group split. If dependencies are missing, stop only this dependent slice rather than inventing replacement models.

### Required export fields

| Field | Shape and meaning |
|---|---|
| tokens | `[N,K,D]`, genuine frozen HSE features |
| attention_mask | bool `[N,K]`, True = valid history token |
| side / side_names | `[N,A]` and names `[A]`; A=0 is explicit |
| targets | `[N,d]`, declared moment target |
| event_id / group_id / condition_id | `[N]`, event, original recording/run, acquisition condition |
| z0 | `[N,H,Z]`, same frozen-reference latent target |
| target_mask | bool `[N,H]`, supervised target positions |
| query_time_s | `[N,H]`, actual query time in seconds |
| target_map | `[d,H*Z]`, `targets=flatten(z0) @ target_map.T` |

The global moment readout conditions on the selected R produced from tokens, history mask and side. Information not represented in tokens must be explicitly exposed when it is part of the actual readout condition. Do not silently replace missing masks with all-valid defaults. Distinct window IDs do not excuse overlap of their original group_id across train, validation and test.

The native dense summary has no reused patch mask: the history mask is already consumed in forming it. Target masks affect the loss, not summary availability. There is no unpriced second moment stream.

### Native equality checks

Use the same z0, actual t and noise for native and independent loss calculation. Compare eps/v/x0 targets, per-sample valid-element normalization, raw/effective weights and final mean. Test none/global/batch normalization. For the batch scheme use its realized denominator. Exercise a denoiser update; intervene on prefix/tail at a fixed noisy input; confirm frozen conditioner parameters and state remain unchanged.

## C. First learned comparison: M versus effective B1-aux

One source-selected shared trunk/moment checkpoint is used for both arms. B1-aux sends R; M sends `[moments(R), tail(R)]`. The auxiliary Gaussian score updates the same trunk whose R reaches B1-aux. The detached auxiliary-head construction is an invalid-control negative test, not a baseline.

The current minimal pilot exposes two arms. B1 remains a reference using the actual ordinary HSE path; do not substitute a random projection to fill its table. B0 may first confirm the official reference entry. M0 and the full five-arm table are deferred until the primary comparison runs correctly.

Initial pilot settings are deliberately small: training seeds 0/1/2, 150 shared-readout updates, 200 native-denoiser updates, 8 posterior draws and 16 requested DDIM steps. The native model is one layer, two heads, 64-step cosine schedule, v prediction, uniform nonzero training times, no loss weighting and no dropout. Record actual runtime and generated function evaluations: requested sampler steps need not equal unique native time indices. These settings are a pilot, not a tuned final benchmark.

Keep the same target/reference encoder, data access, masks, code dimension, denoiser initialization policy, batches/noise/time strategy, update budget and source-validation selection. The input HSE and reference encoder stay frozen. Do not refit any normalization, code or moment head using the unseen acquisition test set.

### Primary endpoint and statistical unit

The primary endpoint is joint Energy Score on source-standardized reference latents, restricted to the declared valid target coordinates and divided by the square root of that event's valid target dimension. This normalizes scale; it does not make different masks the same task. Stratify source holdout and unseen acquisition and keep actual mask patterns comparable across methods.

Use an unbiased cross-draw term for Energy Score with at least two independently initialized draws. Posterior draws are Monte Carlo accuracy, not independent equipment or training replicates. Report draw count, sampler configuration and native cost separately.

For each acquisition condition, pair M/B1-aux by event and training seed. Average the executed paired seeds within event, events within original recording/group, then groups equally. Bootstrap original groups. The interval is conditional on these trained seeds; it does not establish an infinite-seed population claim. One original group cannot provide a between-group confidence interval. Missing method/event/seed pairs must not be silently dropped.

Predeclare a practical/equivalence margin from source repeatability and task needs before reading the test ranking. `p>0.05`, wide intervals or three optimization seeds do not establish equivalence. Preserve unfavorable values and failed runs separately from completed scores.

### Decision

CONTINUE: native comparison is correct, target benefit is repeatable and meaningful at declared cost. Then expand the study.

SIMPLIFY: M has no useful gain or is worse than equally supervised R. Keep the simpler conditioner and report the negative result.

BLOCKED: a genuine export, checkpoint or native dependency is missing. Name that dependency; do not replace it with random data and claim the native pipeline is complete.

Completion means correct implementation, valid comparison, reproducible outputs and an accurate conclusion. It never requires M to win.

## D. Deferred ablations

| Ablation | Question |
|---|---|
| B0 / B1 / B1-aux / M0 / M | inherited model, ordinary code, effective auxiliary supervision, moment bottleneck, candidate |
| predicted moments replaced by oracle moments where available | whether prediction error itself carries condition identity |
| remove or shuffle ordinary tail | whether non-Gaussian shape comes from ordinary features |
| declared covariance floor / alternative explicit constraint | whether the score gains come from variance collapse or a changed feasible family |
| two same-dimensional targets, one crossing a modal group | whether the target affects learned conditioning rather than only post-hoc scoring |
| fixed points versus fixed physical duration | observation-budget and physical-support confounding |
| equal/full actual side inputs | already-available information versus finite computational accessibility |
| source holdout versus unseen acquisition | source statistical semantics versus target generalization |

Do not add new modules because an ablation fails. Gaussian and finite-mixture conditional heads on the same features remain strong controls against claiming Diffusion is necessary from non-Gaussianity alone.

## E. External strong methods, only after the pilot

Maintain task compatibility. LLapDiff is the primary generative reference. CSDI is a probabilistic imputation comparison, not a substitute for forecasting. t-PatchGNN, ContiFormer and Neural CDE cover irregular-time prediction. Add Hi-Patch and HyperIMTS (ICML2025) as modern irregular multivariate representation/forecasting candidates. PatchTST and DLinear are point-forecast controls; do not invent their probability densities or rank them by an unavailable NLL.

For a probability table, either use an explicitly trained matched probability head or report the method only on compatible point metrics. Official baseline commands are reference launchers; shell syntax passing is not baseline execution. No SOTA table receives guessed values.

Analytical controls remain complete statistics, natural/precision blocks, true marginal moments, prior/goal-oriented low-rank approximations and the full-side-information null. Their dense exact inference cost is not equated with amortized HSE cost.

## F. Real PHM and plotting boundary

Only after the minimal native comparison is interpretable, use a licensed raw-recording source. Split original recording/machine groups first; construct anti-aliased rate views within each split. Native high/low hardware measurements and resampling one noisy recording have different noise dependence. No target labels, target normalization fit or target-based checkpoint selection is allowed. An offline single-source pilot is not cross-hardware or universal PHM evidence.

Paper code consumes exported arrays and original split/group information, not PHMFactory factories or internal module paths. No submodule update is required for analytical/native component checks.

Use CSV-only `paper/plot_native.py` for scoring parts, native equality checks and paired pilot effects. Each figure answers one question, retains editable SVG/PDF text and keeps negative/null outcomes. Quantitative figures never use generated image values. This follows the requested nature-figure data-first/vector principles without importing its full governance system.
