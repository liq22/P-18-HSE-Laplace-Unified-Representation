# Goal04 — implement and test the admitted posterior target

## Scope

This goal now concerns the actual source-supported HSE–LLapDiff inference path, not only a fixed-head coordinate comparison. Use the accepted PHMFactory industrial reader/labels/splits and original groups. The five scientific contrasts are in `paper/experiments.md`.

## Available commands and present boundary

```bash
bash paper/build_frontmatter.sh outputs/tii_support
bash experiments/p19/run.sh phm --data /absolute/data/mfpt --output /absolute/runs/mfpt-reference
# Existing coordinate-interface mechanism control only, not the new restricted posterior:
CUDA_VISIBLE_DEVICES=0 bash paper/run.sh native-pilot \
 --train /absolute/exports/train.npz --validation /absolute/exports/validation.npz \
 --test /absolute/exports/test.npz --data-note /absolute/exports/export_note.md \
 --device cuda:0 --seeds 0 1 2 --arms B1_aux M head_affine \
 --output-dir outputs/tii/conditioner_control
```

The support-restricted native training entry does not yet exist. Its next implementation must use source-established modal/latent blocks, a source-identified joint eligible target and the actual native objective. Do not rename the above unrestricted coordinate pilot as completion of that task.

## Required implementation products and acceptance

Retain observed evidence and uncertainty; project every missing-state update onto the fixed eligible subspace; do not emit unsupported coordinates as recovered; handle empty eligibility without a sampler. Check block-decoder support consistency, same-source noise dependence and actual conditioning inputs. Then freeze same-support/target comparisons across point, Gaussian, mixture, ordinary latent diffusion and LLapDiff. Keep R/head_affine/M, simple nonlinear conditioners and direct observed-only diagnosis as controls. Deliver actual per-original-group outputs, costs and the corresponding Results, with target data untouched by fitting.

## Failure handling

Unknown latent-to-mode map or unidentified joint conditional blocks that physical recovery claim, rather than allowing a guessed mask. Missing data/checkpoints remain named prerequisites. Reject-all requires admitted-coverage/utility reporting. Equal or worse LLapDiff/F1 results are completed negative outcomes. No two-card workaround, upstream PHMFactory core edits or test-set replacement.
