# Goal 07 — local Agent execution prompt

Use this file after the user supplies the actual local PHMFactory data root. Execute work; do not return another plan-only answer.

```text
Continue P18 HSE–LLapDiff TII work using the current paper repository and its external/phmfactory submodule.

Scientific target:
source observation evidence
→ jointly qualified missing target
→ HSE-conditioned eligible-state posterior inference
→ posterior quality / support compliance
→ source-only cross-dataset diagnosis.

Repository boundary:
- parent paper repo: manuscript, theory, basic closed-form/interface witnesses, experiment/claim mapping, publication figures;
- external/phmfactory: the only learned-model/data/config/training/evaluation implementation for the industrial experiments.
Do not create a second reader/trainer/runtime in the parent and do not migrate this work to phm-agent-benchmark.

Read first:
- AGENTS.md, PAPER_SCOPE.md
- paper/GOAL.md
- paper/formulation.md, method.md, experiments.md, contributions.md, results_native.md
- paper/goals/01_SYNC_PHMFACTORY.md
- paper/goals/03_DATA.md
- paper/goals/04_EXPERIMENTS.md
- paper/goals/05_RESULTS_FIGURES.md
- paper/goals/06_LOCAL_GPU_8X4090.md
- external/phmfactory/AGENTS.md, CORE.md
- only the PHMFactory Data/Model/Task/Trainer README files and source owners needed by the current gate.

Start read-only:
git status --short
git branch --show-current
git rev-parse HEAD
git submodule status external/phmfactory
git -C external/phmfactory status --short
git -C external/phmfactory branch --show-current
git -C external/phmfactory rev-parse HEAD
Inspect active PRs in both repos. Preserve unrelated changes; no stash/reset/clean/force-push.

Local data:
set PHM_DATA_ROOT to the user-supplied absolute local path (do not commit that path).
Use existing PHMFactory Data Factory and public config entry only. Do not write a private HDF5/Pandas loader, download a substitute dataset, or change upstream splits/labels to make the study work.

Execute automatically in this order.

GATE 0 — DATA_TASK_GATE
1. Read metadata.xlsx and the local README through the maintained data path and enumerate the supplied industrial datasets.
2. For each candidate dataset record: common label ontology; highest independent group; reference origin; observed/reference pairing; Gamma/A; jointly justified Q; eligible/ineligible target; evaluation target truth; observed-state uncertainty; source-only usability; checkpoint/pretraining exposure.
3. Produce DATA_TASK_GATE.md with C1/C2/C3 = GO/PARTIAL/NO-GO and exact blockers.
4. Do not use outer-target performance to choose datasets or method settings.
5. If no natural dataset has known nontrivial qualification truth, keep natural data for external diagnostic validity and create only the predeclared same-recording controlled acquisition needed for qualification evidence. Name deterministic reference features honestly.

GATE 1 — IMPLEMENT THE FINAL METHOD IN PHMFACTORY
1. Reuse Model Factory / Task Factory / Data Factory / Trainer Factory. The P18 model must be a normal PHMFactory model/config, not a paper-side trainer.
2. Integrate one source of truth for: eligible-basis construction, target-intrinsic Gaussian velocity training, original LLapDiff physical-time branch, native scheduler reverse update, observed-state conditioning, explicit unestimated state, and shared-ontology diagnostic readout.
3. Training batches may contain reference/target supervision; deployment forward inputs may contain only allowed observed values/time/mask/acquisition descriptors and source-frozen condition information.
4. Do not use the current Dataset_id-specific classification head as unseen-dataset inference unless a shared ontology head is explicitly source-trained for all LODO folds.
5. Implement and test ambient-clamped C before interpreting A/S differences. A receives no complementary clean truth.
6. Create real PHMFactory P18 configs and a config index. Run focused tests, then phmfactory preflight, then one real source batch on GPU0.
7. Require checkpoint reload and repeated prediction/metric agreement. Retain actual commands, config, seed, source-group IDs, loss, gradient/update, support trace, class probabilities, cost and failures.
8. Gate 1 is executability evidence only; do not write a Results claim.

GATE 2 — ONE TARGET × ONE SEED DECISIVE SCREEN
1. Freeze source-only HPO and all scientific definitions before opening the chosen outer target for scoring.
2. Run the decisive E1/E2/E3/E4 configurations once: observed-only reference, deterministic/Gaussian as applicable, S-T, S-L, legal A-T/A-L, ambient-clamped equivalence, conditioner controls, and one protocol-compatible external conditional-diffusion baseline.
3. Verify common instances, ontology, target/reference access, artifact completeness, non-degenerate contrast, one-GPU memory and cost.
4. Do not redesign the method because this target's score is poor or favorable. Scientific incompatibility is recorded as NA/blocker.

GATE 3 — FROZEN FULL EXPERIMENT
Only after Gate 2 passes, execute qualified LODO folds and preregistered seeds. One run uses one GPU; independent jobs may be spread over the 8×4090 cards. No DDP/two-GPU training.

Primary estimands:
- per-target net diagnostic effect S-L minus strongest source-selected observed-only method;
- support-process effect;
- Laplace physical-time effect;
- support×Laplace interaction;
- conditioner specificity H_M minus max(H_A, same-budget MLP);
- qualification coverage/risk/utility boundary;
- Energy Score, support violation and actual compute reported separately.

Statistical unit is machine/acquisition run/raw recording, never window. Report within-target group bootstrap separately from seed variability. Three target datasets remain three target environments; do not claim population significance from 3×seeds.

Baselines:
reported literature scores are context only. Main-table rows require same-protocol reproduction/adaptation with actual data access stated. Keep one strong observed-only baseline, deterministic, Gaussian, S-T, official-semantics LLapDiff comparison where applicable, and one compatible CSDI/SSSD-style conditional diffusion. Do not add baselines mechanically.

Artifact rule:
Run → raw artifact → deterministic analysis → figure.
Plotting scripts never invoke model inference and never contain expected values. Keep failed runs, all prespecified seeds, raw probabilities/scores, config snapshots, checkpoints or their real storage paths, metrics, logs and runtime/cost.

Sync:
1. child PHMFactory code/config/test/artifacts PR and merge to its dev first;
2. rerun paper-specific acceptance at the exact child commit;
3. update the parent gitlink and experiment/evidence mapping in a separate reviewed parent PR;
4. record exact child and parent commits.
Do not force-push, edit master, delete branches or merge unrelated PHMFactory PRs.

Stop after real artifacts and sync are complete. Do not draft Results, generate expected curves, or claim the method works. Return only:
- Gate status and dataset qualification;
- changed code/config files;
- exact commands actually run;
- PASS/FAIL/NOT RUN with reasons;
- raw artifact locations and actual numeric summaries;
- child PR/commit and parent PR/commit;
- remaining scientific blocker and one next action.
```
