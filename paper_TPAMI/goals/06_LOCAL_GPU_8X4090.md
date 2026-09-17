# Goal06 — genuine local learned comparison

**Scope:** one real source-trained R/M comparison, not more synthetic features or a compulsory router. Machine:8×RTX4090. First run uses GPU0 only, seeds0/1/2 sequentially. **No two-GPU/world-size2 training.** Four/eight GPUs are later options only for an actually validated distributed implementation.

**Current boundary:** UCI128 raw conversion and ordinary affine CPU reference exist. They do not provide trained HSE or reference-VAE checkpoints. Four other raw converters are still pending CPU tasks. Identify/train the actual source encoder/reference and record its target and extraction function before invoking native generation. Classification starts with direct R/M linear/small-MLP heads; the existing native pilot does not implement those classification arms automatically.

**Products:** frozen input/target/split, selected shared auxiliary checkpoint, simple competing transformations, exact T-composition check, direct task scores, prediction CSVs and cost measurements. Freeze primary metric, HPO trials, checkpoint rule, loss weights, normalizer, q/dtype, consumer size, update budget, practical margin and expected seeds before test inspection. PCA/whitening/MLP fitting is source-only. Do not impose a speculative 2% effect margin universally; define the task-specific practical threshold before the paired run.

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

**Acceptance:** real feature provenance, original-group separation, identical consumed side/mask/target and same shared checkpoint. Exact R→T consumer identity must hold. Learned M must be compared against the simple transformations and a matched generic bottleneck before statistical specificity is claimed. Diffusion loss is a mechanism diagnostic for a classification task, not its primary outcome. Byte equality is not total-cost equality; measure latency/memory before Pareto plots.

**Failure:** missing permission/converter/checkpoint is named and stops that slice; no random replacement. OOM requires a declared matched change, never two GPUs. M tying PCA/MLP, or direct heads matching diffusion, is a completed negative result. Keep static fusion as a strong control and route only after these contrasts. Do not change target data, retitle the project or add modules to force a win. No automatic submission, master edit, force-push, branch deletion or PHMFactory core modification.
