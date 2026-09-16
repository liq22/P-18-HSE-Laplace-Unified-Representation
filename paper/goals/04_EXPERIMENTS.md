# Goal04 — minimal industrial comparison

**Scope:** exact PHM reference first; then genuine M/B1-aux, B1, strongest single, industrial static fusion and optional measured acquisition selection. **Products:** actual checkpoints, predictions, group scores, costs and industrial Results. No general-domain benchmark in the TII experiment plan.

```bash
bash experiments/p19/run.sh phm --data /absolute/data/mfpt --output /absolute/runs/mfpt-reference
CUDA_VISIBLE_DEVICES=0 bash paper/run.sh native-pilot \
 --train /absolute/exports/train.npz --validation /absolute/exports/validation.npz \
 --test /absolute/exports/test.npz --data-note /absolute/exports/export_note.md \
 --device cuda:0 --seeds 0 1 2 --output-dir outputs/tii/native
```

**Acceptance:** same supervision/checkpoint/target/loss/budget and original groups. Diagnosis F1 and latent Energy Score remain separate. Official industrial SOTA models require compatible implementations and accepted protocols before claiming a comparison. A optional router must beat the stronger static industrial reference at counted cost.

**Failure:** M loses or mixture wins: report and simplify. Missing native/export dependencies stop that slice, not substitute a new model. OOM does not authorize a two-GPU run or unmatched batch change.
