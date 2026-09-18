# Goal06 — local industrial comparison on8×4090

## Scope

Industrial data only. First run uses GPU0 with paired seeds0/1/2 sequentially. Two-GPU/world-size2 execution is prohibited. Genuine source-trained HSE/reference checkpoints and exported original-recording splits are prerequisites; MFPT's reference model does not provide them.

The primary scientific decision is direct industrial diagnosis: same linear/MLP consumer on R, M and same-head affine control, then PCA/whitening/generic MLP and static fusion. The native script below is a **secondary generation comparison**, not an implementation of the diagnosis table.

## Actual available commands

```bash
bash paper/run.sh setup
bash paper/run.sh setup-neural
export LLAPDIFF_ROOT=/absolute/LLapDiffusion
bash paper/run.sh setup-native
bash paper/run.sh native-acceptance
CUDA_VISIBLE_DEVICES=0 bash paper/run.sh native-pilot \
 --train /absolute/exports/train.npz --validation /absolute/exports/validation.npz \
 --test /absolute/exports/test.npz --data-note /absolute/exports/export_note.md \
 --device cuda:0 --seeds 0 1 2 --arms B1_aux M head_affine \
 --anchor-steps 150 --diffusion-steps 200 --draws 8 --sampler-steps 16 \
 --output-dir outputs/tii/native_control_01
bash paper/run.sh native-figures comparison outputs/tii/native_control_01/event_scores.csv outputs/tii/native_control_01/M_vs_R --reference B1_aux --candidate M
bash paper/run.sh native-figures comparison outputs/tii/native_control_01/event_scores.csv outputs/tii/native_control_01/M_vs_head --reference head_affine --candidate M
```

## Products and acceptance

Real source-trained feature/target exports with original group IDs; selected shared conditioner and native checkpoints; score/logdet/Mahalanobis/eigenvalue diagnostics; paired event scores; q/dtype/bytes, head/trunk/consumer parameters and measured cost. Native acceptance includes explicitly synthetic fixtures and never proves genuine feature extraction.

The industrial classifier still needs actual label-probe training on these genuine features and recording-balanced pooled-confusion macro-F1. At least two industrial data sources or sufficient independently identified machines/bearings are required for a broad method conclusion. Do not invent independent bearings from six MFPT filenames. Acquire/parse/split PHM only through accepted PHMFactory, without a second reader.

## Failure handling

Missing checkpoint/export/classifier implementation is reported explicitly rather than called completed. A null/worse M result, no advantage over the same affine head or generic MLP, or a direct classifier matching diffusion favors simplification. OOM adjustments must be matched and recorded; no two-GPU workaround. Do not change test groups, tune on target, edit PHMFactory core, force-push, modify master or delete branches.
