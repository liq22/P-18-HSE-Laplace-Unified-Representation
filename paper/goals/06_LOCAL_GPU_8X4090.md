# Goal06 — local support-qualified HSE–LLapDiff on 8×4090

## Scope and prerequisites

Industrial data only. First run uses GPU0 and seeds0/1/2 sequentially. Two-GPU/world-size2 execution is prohibited. Genuine source-trained HSE/reference checkpoints, original-recording splits and compatible mechanical/latent coordinates are prerequisites; the MFPT reference does not supply them.

The new main method needs an actual source-qualified missing target and restricted reverse process. The existing native pilot is an available E3 conditioner ablation, not that new model. Complete Goal04's source-reference, identification and projected-batch implementation before starting E2's generator comparison or E1's industrial LODO.

## Existing command, with its limited scope

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
 --output-dir outputs/tii/conditioner_control_01
bash paper/run.sh native-figures comparison outputs/tii/conditioner_control_01/event_scores.csv outputs/tii/conditioner_control_01/M_vs_head --reference head_affine --candidate M
```

## Products and acceptance

For the new restricted path, retain actual source-frozen support/eligibility descriptors, validated coordinate correspondence, projected native forward/backward/reverse checks and observed-evidence preservation. Then use the same admitted target and condition for point/Gaussian/mixture/ordinary diffusion/LLapDiff. Use source-only training and original-group target evaluation. Posterior scores do not replace diagnosis; unsupported emission rate is paired with eligible coverage and utility. Record all parameters, dtype/bytes, total cost and posterior draws.

## Failure handling

Missing identification, physical support correspondence, native code or data is named as a prerequisite, not silently filled by a mask or random feature. Unknown target conditional shift precludes a transfer guarantee. OOM changes must be declared and matched, with no two-card workaround. If LLapDiff or the full posterior does not improve the defined outcome, preserve that result and simplify. No automatic submission, master edits, force-push, branch deletion or PHMFactory core changes.
