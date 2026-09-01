# Related-work boundary

## Latent Laplace modeling

Latent Laplace Diffusion models irregular targets as low-dimensional latent trajectories, imposes stable complex-conjugate modal poles, evaluates trajectories directly at arbitrary timestamps, and analyzes random sampling gaps through renewal averaging. The present project does not claim these elements as new. Its proposed difference is to condition the modal state space on acquisition observability and assign flow, identity, or diffusion to different observable blocks.

Neural Laplace motivates solver-free Laplace-domain representations of differential-equation trajectories. It is relevant to the modal coordinate system, not to the shared/private/unobserved split.

## Diffusion and probability-flow methods

Score-based SDE theory establishes reverse-time diffusion and an equivalent probability-flow ODE with the same marginal densities. Stochastic interpolants provide a broader framework connecting deterministic flows and stochastic diffusions. Therefore the project does not claim to be the first to unify diffusion and flow.

The proposed narrow distinction is an observability-projector-conditioned block process in a stable physical modal space.

## Flow matching and optimal transport

Flow Matching trains continuous normalizing flows by vector-field regression along prescribed probability paths. Conditional and OT flow matching provide practical source-target couplings. These works motivate the shared canonical transport but do not by themselves protect acquisition-private coordinates or determine the transported subspace from physical observability.

## Irregular time-series baselines

The empirical plan must compare observation-space diffusion, Latent ODE/CDE models, continuous-time Transformers, and graph/patch approaches when their tasks and inputs are compatible. A baseline is included in the main table only when it can use the same observed information and evaluation protocol.

## Shared/private representation learning

Domain-separation methods already split shared and private features. The current research cannot claim that decomposition alone as novel. Its candidate contribution is to define the split through acquisition-dependent modal observability and to leave unobserved private modes distribution-valued.

## Exact novelty statement under test

> Heterogeneous acquisition should be represented by a stable Laplace-modal posterior whose common observable coordinates are transported to a source-only canonical space, whose observed-private coordinates are structurally unchanged, and whose unobserved coordinates remain probabilistic.

This statement remains a hypothesis until the known-pole and real paired-acquisition experiments exclude simpler metadata-conditioned diffusion and ordinary transport explanations.
