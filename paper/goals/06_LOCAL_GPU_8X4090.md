# Goal06 — local industrial HSE–LLapDiff

**Scope:** genuine industrial features/targets, not more synthetic smoke. The8×RTX4090 machine first uses GPU0 alone for seeds0/1/2 sequentially. **No two-GPU training/world-size2.** Four/eight GPUs are future options only for verified official distributed implementations, not this pilot.

**Prerequisites/products:** accepted PHMFactory data and splits; real source-trained HSE and reference encoder/checkpoints; exported masks/time/side/targets/original groups; native checkpoints, prediction/score/cost curves and industrial Results. Reference MFPT acceptance does not produce the representation checkpoints.

```bash
bash paper/run.sh setup
bash paper/run.sh setup-neural
export LLAPDIFF_ROOT=/absolute/LLapDiffusion
bash paper/run.sh setup-native
bash paper/run.sh native-acceptance
CUDA_VISIBLE_DEVICES=0 bash paper/run.sh native-pilot \
 --train /absolute/exports/train.npz --validation /absolute/exports/validation.npz \
 --test /absolute/exports/test.npz --data-note /absolute/exports/export_note.md \
 --device cuda:0 --seeds 0 1 2 --anchor-steps 150 --diffusion-steps 200 \
 --draws 8 --sampler-steps 16 --output-dir outputs/tii/native_pilot_01
bash paper/run.sh native-figures comparison outputs/tii/native_pilot_01/event_scores.csv outputs/tii/native_pilot_01/figures
```

**Acceptance:** distinguish synthetic component acceptance from real extraction; preserve shared supervision, actual consumption, target/loss and record-level evaluation. Target domains do not select checkpoints or floors. M need not win for the task to be complete.

**Failure:** absent checkpoints/converter/data are named, not silently replaced. Matched OOM adjustments are explicit, never two GPUs. Negative/equivalent results favor the simpler method. No automatic submission, master edits, force-push, branch deletion or PHMFactory core changes. General-domain runs are specified in the separate TPAMI goal.
