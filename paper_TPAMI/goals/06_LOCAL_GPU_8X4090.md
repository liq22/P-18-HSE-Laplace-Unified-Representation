# Goal06 — genuine local models and matched consumers

## Scope and prerequisites

The machine has8×RTX4090. First run uses one GPU, seeds0/1/2 sequentially. **No two-GPU or world-size2 training.** Later supported1/4/8-GPU runs require the official distributed path. Existing code does not require distributed training.

Before claiming native HSE performance obtain source-trained HSE/reference checkpoints, actual masks/side inputs/target map and original-group export files. The completed Japanese Vowels converter and mean-LPC reference are not those checkpoints. Four other external raw converters remain explicit CPU/data prerequisites. Do not fill missing exports with random or analytic features.

## Commands

```bash
bash paper_TPAMI/run.sh setup
bash paper/run.sh setup-neural
export LLAPDIFF_ROOT=/absolute/LLapDiffusion
bash paper/run.sh setup-native
bash paper/run.sh native-acceptance
# The previous command is explicitly synthetic native component/loop validation.
CUDA_VISIBLE_DEVICES=0 bash paper_TPAMI/run.sh native-pilot \
 --train /absolute/exports/train.npz --validation /absolute/exports/validation.npz \
 --test /absolute/exports/test.npz --data-note /absolute/exports/export_note.md \
 --device cuda:0 --seeds 0 1 2 --arms B1_aux M head_affine \
 --anchor-steps 150 --diffusion-steps 200 --draws 8 --sampler-steps 16 \
 --output-dir outputs/tpami/native_control_01
bash paper/run.sh native-figures comparison outputs/tpami/native_control_01/event_scores.csv outputs/tpami/native_control_01/M_vs_R --reference B1_aux --candidate M
bash paper/run.sh native-figures comparison outputs/tpami/native_control_01/event_scores.csv outputs/tpami/native_control_01/M_vs_head --reference head_affine --candidate M
```

## Products and acceptance

A shared selected anchor per seed, three native checkpoints, unchanged actual inputs/targets/loss/sampler, original-group event scores and all costs. `head_affine` reuses the same raw head, not a new fitting stage. Preserve the primary M/R contrast and the nonlinear-specific M/head contrast; do not choose whichever wins after viewing test results. Report both with their source selection and practical margins. Measure selected-head rank and actual dtype behavior before calling the complete message reversible in implementation.

For classification, use direct linear/MLP and same-supervision simple transforms before a generative necessity claim. The native pilot produces Energy Score, not diagnostic macro-F1. A classification model must be explicitly implemented/evaluated; a dataset argument is not such implementation. Static fusion follows the best-single comparison, routing remains secondary.

## Failure handling

Missing data/converter/checkpoint: name it and stop that slice. Native loss mismatch: fix the interface, not the target. OOM: declare a common budget change for all paired arms, not two GPUs. M equals/loses to head_affine or a generic MLP: retain the simpler interpretation and negative result. Do not force method success, change master, force-push, delete branches or claim a full five-domain result from this pilot.
