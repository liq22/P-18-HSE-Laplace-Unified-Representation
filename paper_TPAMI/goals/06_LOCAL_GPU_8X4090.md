# Goal06 — genuine local learned comparison

**Scope:** one real source-trained R/M comparison, not more synthetic features or a compulsory router. Machine:8×RTX4090. First run uses GPU0 only, seeds0/1/2 sequentially. **No two-GPU/world-size2 training.** Four/eight GPUs are later options only for an actually validated distributed implementation.

**Current boundary:** UCI128 raw conversion and ordinary affine CPU reference exist; these do not provide trained HSE or reference-VAE checkpoints. Four other converters remain pending CPU tasks. Identify/train the actual source encoder/reference and record target and extraction before native generation. Classification starts with direct R/M linear/small-MLP heads; the existing native pilot does not automatically implement those classification arms.

**Products:** genuine inputs/targets/splits, selected shared auxiliary checkpoint, simple competing transformations, exact T-composition check, predictions and cost measurements. Freeze primary metric, source checkpoint rule, HPO trials/loss weights, normalizer, q/dtype, consumer/update budget, practical margin and expected seeds before test inspection. The complete message may be invertible: inspect the selected head's replaced-coordinate block rank/minimum singular value, raw diagonal activation range and inverse round-trip error in the actual dtype. Do not infer ideal losslessness from a random float64 fixture or alter the model just to force that subcase.

```bash
bash paper_TPAMI/run.sh setup
bash paper/run.sh setup-neural
export LLAPDIFF_ROOT=/absolute/LLapDiffusion
bash paper/run.sh setup-native
bash paper/run.sh native-acceptance
# Generation only, after actual source-trained HSE/reference exports exist:
CUDA_VISIBLE_DEVICES=0 bash paper_TPAMI/run.sh native-pilot \
 --train /absolute/exports/train.npz --validation /absolute/exports/validation.npz \
 --test /absolute/exports/test.npz --data-note /absolute/exports/export_note.md \
 --device cuda:0 --seeds 0 1 2 --anchor-steps 150 --diffusion-steps 200 \
 --draws 8 --sampler-steps 16 --output-dir outputs/tpami/native_pilot_01
bash paper/run.sh native-figures comparison outputs/tpami/native_pilot_01/event_scores.csv outputs/tpami/native_pilot_01/figures
```

**Acceptance:** original-group separation, identical consumed side/mask/target, shared checkpoint and source-only selections. R→T identity holds. Learned M competes with simple transformations and a matched generic bottleneck before statistical specificity is claimed. Classification metrics remain distinct from denoising diagnostics. Equal bytes are not equal total work; measure actual latency/memory before Pareto plots. No universal 2% effect margin is invented; define the task-specific meaningful threshold before comparison.

**Failure:** absent permission/converter/checkpoint is named; no random replacements. OOM requires a declared paired adjustment, never two GPUs. M tying PCA/MLP or direct heads matching diffusion is a completed negative result. Static fusion is a strong control; route only after these comparisons. No test-set replacement, new model stack to force a win, automatic submission, master edit, force-push, branch deletion or PHMFactory core changes.
