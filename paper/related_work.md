# Related-work and novelty boundary

## Comparison principle

The comparison is organized by the represented object, the source of
heterogeneity, the support semantics and the evidence required for missing
inference.

| Direction | Representation object | Support roles | Missing identifiability | Private preservation | Global-null exclusion |
|---|---|---|---|---|---|
| Latent Laplace Diffusion | generic latent Laplace trajectory | no four-way partition | learned from its forecasting setup | not structural | no |
| Neural Laplace | Laplace-domain trajectory | no | not addressed | not applicable | no |
| Flow Matching / OT-CFM | generic probability path | no | not addressed | not guaranteed | no |
| Domain Separation Networks | generic shared/private features | not acquisition-derived | not addressed | model-dependent | no |
| partial-view representation | shared latent factors | view-dependent | often assumed through pairing or objectives | method-dependent | rarely explicit |
| proposed candidate | fixed physical modal slots | common / observed-private / source-supported-missing / source-global-null | explicit certificate required | structural identity | explicit |

## What is already established

The project does not claim as new:

- stable Laplace latent dynamics;
- arbitrary-time modal synthesis;
- the probability-path relation between Flow and Diffusion;
- shared/private feature decomposition;
- generic missing-view generation;
- optimal transport or Flow Matching.

## Exact unresolved gap

Existing components do not jointly answer:

1. which modal coordinates may be aligned under partially overlapping
   acquisition support;
2. which observed coordinates must remain unchanged;
3. when a current-domain missing coordinate is identifiable from other sources;
4. when a generated coordinate is only prior-driven;
5. when the complexity of Flow or Diffusion is actually necessary.

## Narrow novelty statement under test

> The candidate novelty is a role- and identifiability-gated physical
> representation: acquisition observability assigns fixed Laplace modal slots to
> common, observed-private, source-supported-missing or source-global-null
> roles; paired or physical evidence determines whether missing inference is
> identifiable; and nested model classes determine whether affine/Gaussian
> realizations are sufficient before Flow or Diffusion is used.

## Closest-work questions

### Relative to LLapDiff

LLapDiff supplies stable latent Laplace dynamics and probabilistic irregular-time
prediction. The proposed difference is not another generic latent conditioner.
It is the explicit acquisition-support role assignment, identifiability gate and
global-null exclusion.

### Relative to Flow Matching and OT

Flow methods supply trainable transport. They do not by themselves select the
physically admissible transported block or prevent semantic permutation. The
paper therefore requires paired or task-sufficient anchors.

### Relative to shared/private learning

Shared/private decompositions already exist. The proposed split is fixed by
acquisition observability and adds two missing-data categories:
source-supported missing and source-global null.

### Relative to partial-view methods

Complementary views can support a missing conditional only when their joint
coupling is identified. Separate unpaired marginals are insufficient; Theory 16
gives an explicit counterexample.

## Rejection conditions

Narrow or reject the novelty claim when:

- metadata and a hard support mask match the method;
- unpaired source evidence cannot identify the missing conditional;
- Gaussian or mixture models match Diffusion under a proper score;
- paired affine calibration or ordinary OT matches Flow;
- a direct time-domain latent matches Laplace coordinates;
- private information is only acquisition identity;
- semantic anchors do not prevent class permutation.
