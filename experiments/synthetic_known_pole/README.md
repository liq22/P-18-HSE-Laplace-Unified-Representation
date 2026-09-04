# Known-pole paired-acquisition experiment

## Objective

Test whether HSE-conditioned LLapDiff recovers a calibrated posterior over the same declared Laplace modal event from heterogeneous paired acquisitions.

## Required generator semantics

```text
latent event is sampled once
train/validation/test split is assigned by latent_event_id
acquisition views are generated only after the split
low-rate views are anti-aliased before sampling
all views retain the same canonical modal target
```

## First implementation

Use fixed known modal slots. Do not learn poles, event boundaries, token allocation, codebooks, or Flow Matching.

## Falsifying comparisons

```text
Gaussian posterior oracle
posterior mean
heteroscedastic Gaussian
finite mixture
original LLapDiff condition
LLapDiff + acquisition metadata
HSE-conditioned LLapDiff
```

The experiment must include an ambiguous conditional for which posterior mean and a single Gaussian are inadequate. If a finite mixture matches Diffusion, the Diffusion claim is stopped or reduced.
