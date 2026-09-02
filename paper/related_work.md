# Related-work and novelty boundary

## Comparison principle

The paper compares methods by the object they represent, the heterogeneity they
model and the information they are permitted to change. Similar module names
are not sufficient evidence of equivalence or novelty.

| Direction | Representation object | Heterogeneity addressed | Observable-support roles | Private preservation | Global-null exclusion |
|---|---|---|---|---|---|
| Latent Laplace Diffusion | generic latent Laplace trajectory | irregular timestamps and forecasting uncertainty | no explicit four-way split | not structural | no |
| Neural Laplace | Laplace-domain trajectory | differential-equation dynamics | no | not applicable | no |
| Flow Matching / OT-CFM | generic data or latent probability path | source-target transport | no | not guaranteed | no |
| Domain Separation Networks | generic shared/private features | domain variation | not acquisition-derived | model-dependent | no |
| irregular-time ODE/CDE models | continuous-time hidden state | timestamps and missingness | no | not explicit | no |
| proposed candidate | fixed physical modal slots | acquisition operators with partial support overlap | shared / observed-private / recoverable-missing / global-null | structural identity | explicit |

## Latent Laplace modeling

Latent Laplace Diffusion supplies stable complex-conjugate modal dynamics,
arbitrary-time queries and a gap-aware irregular-time mechanism. These are
prior contributions. The present project changes the representation semantics:
modal roles are determined by structural acquisition support, and only
source-supported missing modes receive a learned posterior.

Neural Laplace motivates Laplace-domain trajectory modeling. It does not
provide the acquisition-support partition or the Flow/identity/posterior role
assignment.

## Diffusion and probability-flow theory

Score-SDE, probability-flow ODE, Flow Matching and stochastic-interpolant
theories already connect deterministic and stochastic probability paths. The
project therefore does not claim to be the first to combine or unify Flow and
Diffusion.

Diffusion is retained only if the recoverable-missing conditional is
sufficiently non-Gaussian or multimodal that Gaussian and mixture baselines
fail.

## Flow and optimal transport

Flow Matching and OT-CFM motivate learned canonical transport. Ordinary
marginal transport does not decide which physical support should move, and it
can align marginals while permuting class semantics.

Flow is retained only if affine calibration, whitening, CORAL and minibatch OT
cannot achieve the same paired shared-state error and task preservation.

## Shared/private representation learning

Shared/private feature decompositions are established. The proposed difference
is not the existence of shared and private blocks. It is the structural
acquisition rule that assigns fixed Laplace modal slots to:

```text
common support
observed-private support
recoverable-missing support
source-global-null support
```

and assigns different permissible operations to those roles.

## Partial-view and missing-view representation

Partial-view methods motivate recovery from complementary observations.
However, a coordinate being visible in another source domain does not identify
its current-domain conditional without paired events or another coupling
assumption. The project treats this as an explicit identifiability condition,
not an architectural guarantee.

## Exact novelty statement under test

> The candidate novelty is an acquisition-observability-conditioned,
> source-supported modal representation in which common modes are
> canonicalized at the source-population level, observed-private modes are
> preserved, recoverable-missing modes remain probability-valued, and modes
> unsupported by every source are excluded from learned recovery claims.

The claim is rejected or narrowed when:

- source metadata alone matches the method;
- Gaussian or mixture posteriors match Diffusion;
- affine or ordinary OT baselines match Flow;
- the local Laplace representation has no advantage over a matched
  time-domain latent;
- paired source evidence is insufficient to identify the missing conditional.
