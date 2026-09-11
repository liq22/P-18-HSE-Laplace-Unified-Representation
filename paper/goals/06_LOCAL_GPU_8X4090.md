# Goal 06 — Local GPU execution on 8×4090

## Trigger

Use this Goal only after CPU/theory checks, data Goal, PHMFactory Goal (for PHM), and genuine HSE/reference export validation pass. The repository changes up to that boundary can be reviewed/merged without pretending GPU results exist.

## Hardware rule

Available machine: 8 × RTX 4090. **Two-GPU execution is forbidden.**

- First genuine M/B1-aux pilot: one GPU only (`cuda:0`).
- Independent seeds may run concurrently on separate single GPUs after the one-GPU command is validated, e.g. GPU 0, 1 and 2 as three independent processes.
- For later large external/SOTA work use 1, 4 or 8 GPUs only when the official implementation actually supports distributed execution and the paper config declares it. Do not create a 2-GPU special path.

## First required run

```bash
CUDA_VISIBLE_DEVICES=0 bash paper/run.sh native-pilot \
  --train /absolute/train.npz \
  --validation /absolute/validation.npz \
  --test /absolute/test.npz \
  --data-note /absolute/export_note.md \
  --device cuda:0 --seeds 0 1 2 \
  --anchor-steps 150 --diffusion-steps 200 \
  --draws 8 --sampler-steps 16 \
  --output-dir outputs/native_pilot_01
```

This command is deliberately small. Do not start five arms, SOTA sweeps or all external benchmarks before the matched pilot is interpretable.

## Parallel single-GPU seeds after validation

```bash
CUDA_VISIBLE_DEVICES=0 <seed-0-command> &
CUDA_VISIBLE_DEVICES=1 <seed-1-command> &
CUDA_VISIBLE_DEVICES=2 <seed-2-command> &
wait
```

Each process remains a single-GPU experiment and writes a distinct output directory.

## Acceptance

- no CUDA fallback;
- exact frozen export and config recorded in the local run note;
- all three seeds finish or failures are retained;
- M/B1-aux curves, final group-level scores and cost are written to CSV;
- Results text reflects the sign of the actual comparison.

## Failure handling

OOM → reduce declared batch size equally for all compared arms and rerun all matched arms; do not silently change one method. Missing dependency/data → BLOCKED, not random substitute. M loses → SIMPLIFY, do not add a new module automatically.
