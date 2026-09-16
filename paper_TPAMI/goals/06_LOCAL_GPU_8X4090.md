# Goal06 — local GPU experiments

**Scope:** only after genuine source-trained encoder/reference checkpoints, official raw conversion, masks, targets and original-group splits exist. The machine has8×RTX4090; first pilot uses one GPU. **Two-GPU training/world-size2 is prohibited.** Later supported implementations may use1/4/8 GPUs or independent single-GPU seeds after validation, not an automatic two-card workaround.

**Products:** real checkpoints, shared-supervision comparison, target/consumer/budget records, per-group scores, cost logs and Results. No dummy export substitutes missing local dependencies.

```bash
bash paper_TPAMI/run.sh setup
bash paper/run.sh setup-neural
export LLAPDIFF_ROOT=/absolute/LLapDiffusion
bash paper/run.sh setup-native
bash paper/run.sh native-acceptance
CUDA_VISIBLE_DEVICES=0 bash paper_TPAMI/run.sh native-pilot \
 --train /absolute/exports/train.npz --validation /absolute/exports/validation.npz \
 --test /absolute/exports/test.npz --data-note /absolute/exports/export_note.md \
 --device cuda:0 --seeds 0 1 2 --anchor-steps 150 --diffusion-steps 200 \
 --draws 8 --sampler-steps 16 --output-dir outputs/tpami/native_pilot_01
bash paper/run.sh native-figures comparison outputs/tpami/native_pilot_01/event_scores.csv outputs/tpami/native_pilot_01/figures
```

**Acceptance:** component smoke is labelled synthetic; real export is separately checked; frozen paths, same target/loss/time/noise policy and original groups are verified. Source validation chooses checkpoints; fresh calibration groups choose among frozen complete policies, then untouched test groups evaluate. No single learned M/B1-aux result is presented as all5 domains or a new TPAMI theory.

**Failure:** missing data/checkpoint/converter/export is named and stops that slice. OOM means a declared matched configuration change or no run; no two GPUs. A negative method result is deliverable. No automatic publication, master change, force-push or branch deletion.
