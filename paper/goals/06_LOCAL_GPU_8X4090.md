# Goal 06 — local GPU boundary: genuine HSE–LLapDiff

## Scope and missing prerequisites

The machine has 8×RTX 4090. This update stops before expensive learned experiments. Required local inputs are a genuine source-trained HSE checkpoint, a source-trained reference encoder/checkpoint, audited raw-group splits and the exact exported features/targets. MFPT reference acceptance does not supply those representation checkpoints. Identify or train them with the existing upstream source path; do not replace them with random or analytic features.

PHMFactory remains a separate installed environment. Original LLapDiff is independently installed via `LLAPDIFF_ROOT`; paper code does not import PHMFactory core. External raw converters/checkpoints remain dataset-specific pending prerequisites, not “already integrated” benchmarks.

## Hardware and permissions

First pilot: one GPU, GPU0. Run seeds 0/1/2 sequentially there. **No world-size-2 or two-GPU training.** Later official implementations may use 1, 4 or 8 GPUs only after their distributed entry is validated; independent single-GPU seed jobs are also allowed. No force-push, master edits, branch deletion, upstream core changes or automatic submission.

## Actual commands

```bash
bash paper/run.sh setup
bash paper/run.sh setup-neural
export LLAPDIFF_ROOT=/absolute/LLapDiffusion
bash paper/run.sh setup-native
bash paper/run.sh native-acceptance
# This acceptance is a component check with explicitly synthetic input, not the next real run.
CUDA_VISIBLE_DEVICES=0 bash paper/run.sh native-pilot \
  --train /absolute/exports/train.npz \
  --validation /absolute/exports/validation.npz \
  --test /absolute/exports/test.npz \
  --data-note /absolute/exports/export_note.md \
  --device cuda:0 --seeds 0 1 2 \
  --anchor-steps 150 --diffusion-steps 200 --draws 8 --sampler-steps 16 \
  --output-dir outputs/native_pilot_01
bash paper/run.sh native-figures comparison outputs/native_pilot_01/event_scores.csv outputs/native_pilot_01/figures
```

## Products and acceptance

One shared conditioner checkpoint per seed, real native denoiser checkpoints, event scores, source/unseen statistical diagnostics, training curves, parameters/time/draw counts and record-level paired comparison. Verify the actual HSE patch/mask/side path, source-only selection and frozen statistics before interpreting gains. M need not win: correctness, reproducibility, valid comparison and a faithful Results update complete the task.

## Failure handling

No checkpoint/data/export code: name the absent dependency and stop that slice. Native objective mismatch: correct the interface, not the target or comparison data. OOM: declare a common batch-size change and rerun all paired arms; do not silently use two GPUs. No gain against B1-aux or static fusion: preserve the negative result and use the simpler model.
