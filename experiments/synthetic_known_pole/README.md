# Known-pole paired-acquisition experiment

## Objective

Construct paired heterogeneous observations from the same declared modal event and test whether flow, identity, and diffusion act on the intended subspaces.

## Required latent variables

- `latent_event_id`;
- common damping, frequencies, and residues;
- private damping, frequencies, and residues;
- event time and optional forcing;
- a split assigned before acquisition views are generated.

## Required acquisition operators

- high-rate wide-band;
- anti-aliased low-rate;
- irregular/missing;
- a held-out operator not used for fitting.

## First implementation boundary

Use fixed known modal slots. Do not learn poles, event routing, token allocation, or codebooks in this experiment.

## Primary failure tests

- low-rate observation cannot identify the hidden private realization;
- complete alignment loses private task information when it is conditionally useful;
- shared flow cannot modify private coordinates;
- posterior coverage fails when diffusion uncertainty collapses.
