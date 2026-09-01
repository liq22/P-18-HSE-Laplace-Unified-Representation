# Experiment plan

## Rule

Each experiment must distinguish the unified representation from a named simpler explanation. A completed run records command, configuration, data/split version, seed, environment, terminal state, metrics, and interpretation boundary. No custom hash or ledger is required.

## E0 — analytic contract

### Question

Do the code objects implement the proved block structure?

### Checks

- observable projectors are symmetric, idempotent, orthogonal, and sum to identity;
- private coordinates do not change under transport;
- stable modal transitions obey the exact norm bound;
- compensated Gaussian SDE moments match the prescribed flow path.

### Command

```bash
python examples/analytic_unified_representation.py
python -m unittest discover -s tests -v
```

### Decision

Failure blocks all learned experiments.

## E1 — known-pole paired-acquisition falsification

### Latent system

Generate one latent event with:

- at least two common damped modes;
- one high-support private mode;
- declared damping, frequency, residues, and event time;
- optional bounded forcing.

Produce paired acquisition views from the same event:

```text
high-rate wide-band view
mid-rate view
anti-aliased low-rate narrow-band view
irregular/missing view
```

Split latent event identities before generating acquisition views.

### Methods

1. no alignment;
2. complete paired invariance;
3. metadata-conditioned generic latent diffusion;
4. shared flow only;
5. unobserved diffusion only;
6. full unified representation.

### Primary estimands

- shared modal estimation error;
- canonical shared Wasserstein distance;
- observed-private pre/post distance;
- unobserved-private 90% interval coverage;
- CRPS or NLL;
- acquisition-space reconstruction error;
- downstream log-loss with and without private modes.

### Go/no-go

Continue only if the full representation simultaneously:

- improves unobserved-private calibration over point and metadata-conditioned baselines;
- preserves observed-private coordinates;
- reduces common-mode domain discrepancy without degrading shared task utility;
- retains task-relevant private information that complete invariance removes.

## E2 — source-only canonical-anchor headroom

Before training a neural flow, compare source-only canonical targets:

- identity/no alignment;
- mean/whitening alignment;
- CORAL;
- MMD optimization;
- minibatch optimal transport;
- Wasserstein barycenter in modal coordinates.

Hold out one acquisition operator completely. If a simple linear map matches the barycenter and task results, do not build a complex flow model.

## E3 — learned unobserved posterior

Freeze modal slots and observable projectors. Train only the unobserved score or velocity head.

Compare:

- posterior mean regression;
- heteroscedastic Gaussian;
- generic latent diffusion;
- support-masked modal diffusion.

Primary outcome: calibration on modes known to be hidden by the low-support operator.

## E4 — learned shared flow

Freeze the modal encoder and private identity path. Train only the shared conditional flow.

Compare:

- CORAL;
- MMD;
- DANN;
- domain-separation baseline;
- minibatch OT;
- generic latent flow matching;
- OT conditional flow matching;
- support-constrained shared flow.

Report number of function evaluations, latency, and domain/fault probes. Flow must reduce acquisition identity without class permutation or private loss.

## E5 — real recording-level paired-rate pilot

Select raw high-rate PHM recordings with clear license and recording or machine grouping keys.

Protocol:

1. split machines/recordings first;
2. create high/mid/low rate views inside each split;
3. use explicit anti-alias filtering;
4. freeze support thresholds, normalization, HPO, and canonical anchors on source data;
5. evaluate an unseen intermediate rate or sensor response.

Do not treat windows from the same original recording as independent units.

## Statistics

For empirical papers, predeclare:

- independent unit: machine, bearing, run, or recording;
- one primary comparison;
- one primary metric;
- paired confidence intervals at the independent-unit level;
- all dataset-level and worst-domain results;
- fixed tuning trials and compute budget;
- exploratory versus confirmatory results.

## Stop conditions

Stop or simplify when:

- the common observable subspace is consistently empty;
- metadata conditioning matches support-aware posterior calibration;
- ordinary OT matches the shared flow;
- private modes contain only acquisition identity;
- the local modal residual is too large for the target window;
- the learned score is not calibrated on hidden modes.
