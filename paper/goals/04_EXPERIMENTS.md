# Goal 04 — execute the minimum decisive comparison

## Scope

Run CPU theory/toy and the exact MFPT reference first; the next learned task is the genuine M/B1-aux native pilot. Only then add the original B1 reference, static fusion, fixed-arm selection and task-compatible external models.

## Products

Actual prediction/score CSVs, selected checkpoints, training/score decomposition and cost curves, and updated Results. Each dataset/config/arm has a declared status: executed, failed, or awaiting prerequisite. No synthetic SOTA table.

## Commands

```bash
bash experiments/p19/run.sh toy --events 1024 --output outputs/p19/toy_routing.csv
bash experiments/p19/run.sh ablation parameterization smoke
bash experiments/p19/run.sh ablation sampled smoke
# Genuine native exports and an installed official LLapDiff are required:
bash experiments/p19/run.sh ablation native --train /absolute/train.npz --validation /absolute/validation.npz --test /absolute/test.npz --data-note /absolute/export_note.md --device cuda:0 --seeds 0 1 2 --output-dir outputs/native-pilot
# Same native entry for an explicitly prepared external domain:
bash experiments/p19/run.sh external uci_har --train /absolute/har/train.npz --validation /absolute/har/validation.npz --test /absolute/har/test.npz --data-note /absolute/har/export_note.md --device cuda:0 --seeds 0 --output-dir outputs/har-native
# Official reference CLI only, with its supported upstream dataset key:
bash experiments/p19/run.sh sota train crypto
```

## Acceptance

The two-arm pilot fixes shared supervision/checkpoint and all native target/loss/sampler settings. Fixed source selectors are evaluated on independent groups; best-single and static prediction fusion are mandatory references before routing promotion. Class metrics and probabilistic scores are not pooled. External/SOTA launchers executing a supported upstream task do not automatically reproduce this paper's protocol.

## Failure handling

M loses: finish, report and simplify. Static fusion matches a router: remove the latter. An official model lacks compatible data/outputs: leave its row pending rather than replacing it. OOM changes must be declared and matched across arms; no two-GPU workaround.
