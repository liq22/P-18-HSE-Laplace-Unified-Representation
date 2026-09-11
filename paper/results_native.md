# Native acceptance and supporting finite witnesses

## Scope

This file records component acceptance, not a trained-method result. The existing remote source inspected for the native result was `a36f011`, PR #8 targeting dev. No original HSE extraction, reference-VAE export or real-PHM evaluation was performed by that component check.

## Existing native CI evidence

Workflow run 34590958894, native-conditioner job 103235904425, completed 2026-09-11. It installed the original `pixelhero98/LLapDiffusion` component at revision `0631e65cbac59d23822205573ebc7e180ecf0487`. Artifact `native-conditioner-check` contains native_check.json, native_loss_alignment.csv and schedule.csv.

| Check | Actual recorded result |
|---|---:|
| Shared-gradient/frozen/export behavior suite | 14 tests passed |
| Native loss comparison configurations | 24 |
| Per-batch comparison rows | 96 |
| Maximum absolute native/reconstructed loss difference | 1.1920928955e-7 |
| Auxiliary gradient L1 on the consumed trunk | 49.30367923 |
| Ordinary-code maximum change after auxiliary step | 0.01159522310 |
| B1-aux prefix / tail intervention effect | 0.00081454217 / 0.00069965422 |
| M prefix / tail intervention effect | 0.00071845949 / 0.00056587160 |
| Frozen conditioner state after native updates | unchanged |
| Extra cond_summary_raw bypass | absent |
| Native uniform-time schedule export | completed |
| Original HSE/reference executed | false |
| M advantage tested | false |

The effects are from a randomly initialized native component after one update on explicit synthetic fixtures. They show consumption, not trained usefulness. The loss measures cover eps/v/x0 and none/global/batch normalization on the same batch. They do not validate all upstream data trainers or arbitrary time-sampling configurations.

## This revision's Theory 12 witness

The original Gaussian tests remain. Locally, the modified Notebook was executed in an independent kernel with selected inspected source dependencies, not a full repository checkout. Full repository execution belongs to CI on the final commit.

| Finite witness | Result and boundary |
|---|---|
| Gaussian conditional score excess | 0.5114114552, equal to the Gaussian moment KL |
| Same-moment distinct smooth laws | Bayes epsilon gap 0.0224274361995 at alpha=.8, sigma=.6 |
| Grid refinement, 40,001 to 80,001 points | 3.47e-18 difference |
| R versus T(R), both Bayes-sufficient for R squared | affine prediction risks 2/9 and approximately zero |
| Alternative target R, message R squared | irreversible Bayes loss 2/3 |
| Realized batch normalization versus ratio of expectations | 0.7 versus 0.9 |
| V eigenvalues .01 and 2, public floor .1 | closed constrained optimum eigenvalues .1 and 2 |

The affine example illustrates accessibility but does not predict LLapDiff performance. The same-moment result does not favor M over an ordinary message that already retains the law identity. The covariance floor changes the feasible family; positive-definite covariance alone is not a calibration guarantee.

## Updated run and figure entry

`bash paper/run.sh native-acceptance` now resolves the advertised native checks and CSV redraw in one explicit command. `paper/plot_native.py` does no training or simulation. Its M/B1-aux comparison requires exact event/condition/seed pairing, aggregates within original groups and reports intervals conditional on the executed seeds. Missing pairs are rejected; a one-group result has no group-level confidence interval.

The local alignment figure was redrawn from the downloaded existing CI artifact, not a newly generated model comparison. The five plotting behavior tests check pairing and grouping with small fixtures; those fixtures are not empirical method evidence.

## What remains open

Actual HSE/reference checkpoints and genuine exports are required for the two-arm pilot. No sample scores or full SOTA table are filled in before that run. Report M minus B1-aux and its declared cost even if M is worse. `formal_claim_supported: false` remains unchanged.
