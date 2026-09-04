# Experiment plan

## E0 — closed-form theory oracle

Implemented now. It checks:

- variable observation length with fixed modal statistics;
- exact Gaussian posterior in canonical coordinates;
- posterior covariance and entropy decrease under Loewner-ordered acquisition information;
- fixed `K x D` HSE conditioning tokens;
- likelihood-ratio invariance for observations sharing the same sufficient statistics.

These results validate only the declared linear-Gaussian special case.

## E1 — known-pole paired-acquisition falsification

Generate a latent event before any acquisition view. Split `latent_event_id`, then produce:

```text
high-rate wide-band view
anti-aliased middle-rate view
anti-aliased low-rate view
irregular and block-missing view
```

The canonical target is the same declared Laplace modal trajectory for all paired views.

### Factors

1. complete versus partial frequency support;
2. task-irrelevant versus task-relevant private mode;
3. unimodal versus multimodal conditional ambiguity.

### Baselines

```text
posterior mean regression
heteroscedastic Gaussian
finite conditional mixture
original LLapDiff conditioning
LLapDiff + acquisition metadata
HSE-conditioned LLapDiff
```

Flow Matching and OT are not active baselines in this paper.

### Primary metrics

| Question | Primary metric |
|---|---|
| Does HSE preserve fixed canonical coordinates? | paired modal-mean error |
| Is uncertainty calibrated to acquisition information? | joint Energy Score or declared marginal CRPS |
| Does more information reduce uncertainty? | directional posterior variance order |
| Is private task information lost by full invariance? | paired task log-loss difference |
| Is the posterior calibrated? | 50/80/90% coverage |

### Stop rule for Diffusion

Stop or demote the Diffusion component if the strongest Gaussian or finite-mixture model is equivalent on the predeclared proper score and calibration metrics under the same HSE condition.

## E2 — minimal HSE–LLapDiff integration

Keep the original LLapDiff target VAE, stable modal predictor, diffusion parameterization, and reverse sampler. Replace or augment only the history port tokens with HSE physical tokens. Do not simultaneously add learned poles, event routing, codebooks, domain adversaries, or Flow Matching.

## E3 — real paired-rate pilot

Use one raw high-rate recording source with a clear grouping key.

1. split machines or recordings first;
2. generate high/mid/low views inside each split;
3. use explicit anti-alias filtering;
4. fit normalization and HSE parameters on source splits only;
5. test an unseen intermediate rate or missingness pattern;
6. treat views from one recording as paired observations.

## Statistical contract

The independent unit is `latent_event_id` in E1 and a machine, run, bearing, or recording in E3. Seeds are implementation replicates. Method differences use paired confidence intervals over independent units. Failure and null results remain in the paper.
