# Experiment plan

## Rule

Every experiment must distinguish one proposed mechanism from a named simpler
explanation. The independent unit is a latent event in synthetic work and a
machine, bearing, run or recording in real work. Windows or multiple
acquisition views of one unit are not independent samples.

A completed run records command, configuration, data and split version, seed,
environment, terminal state, metrics and interpretation boundary. No custom
hash, checksum or ledger is required.

## E0 — analytic contract

### Question

Does the implementation match the corrected scientific object?

### Checks

- four projectors are symmetric, idempotent, orthogonal and sum to identity;
- recoverable-missing and global-null support are different;
- indefinite noise covariance is rejected;
- observed-private and global-null coordinates remain unchanged;
- the missing update may condition on canonical shared state;
- stable modal transitions obey the exact decay bound;
- compensated Gaussian SDE moments match the declared probability path.

### Command

```bash
python examples/analytic_unified_representation.py
python -m unittest discover -s tests -v
```

Failure blocks all empirical work.

## E1 — known-pole 2×2×2 oracle falsification

No neural network is trained in E1. Ground-truth modal states and acquisition
operators are available.

### Factor A — support overlap

```text
full overlap
partial overlap
```

### Factor B — private task value

```text
I(Y; P | C) = 0
I(Y; P | C) > 0
```

### Factor C — recoverable-missing posterior shape

```text
unimodal
multimodal
```

The design yields eight cells. Every cell contains paired acquisition views
generated from the same latent event. Split `latent_event_id` before generating
views.

### Global-null negative control

Add one modal coordinate satisfying

\[
A_d\Theta_0=0
\]

for every source domain. The correct method output is `unsupported` or
`prior-only`, not a reconstruction score presented as evidence.

### Signal regimes

Run three declared regimes:

```text
damped transient only
damped transient + bounded forced component
one switching event as a misspecification control
```

The first paper remains focused on event-local transients unless the forced
baseline shows systematic residual failure.

### Oracle methods

1. no role decomposition;
2. complete invariance;
3. hard four-way support;
4. soft slot observability;
5. posterior mean for missing modes;
6. oracle Gaussian posterior;
7. oracle mixture posterior;
8. oracle full conditional posterior;
9. identity shared coordinates;
10. affine shared calibration;
11. oracle nonlinear canonical map.

### Primary metrics

| Mechanism | One primary metric |
|---|---|
| support decomposition | true-versus-estimated modal role error |
| complete-invariance harm | paired task log-loss difference |
| observed-private preservation | maximum private drift |
| missing posterior | CRPS or NLL |
| shared canonicalization | paired shared modal MSE |
| global-null behavior | false recovery rate, target zero |
| modal adequacy | event-level reconstruction residual |

Secondary metrics may include coverage, conditional retrieval, CKA and
acquisition-ID probes. They are not averaged into one score.

### Go/no-go

Proceed only when E1 shows independent headroom:

```text
support decomposition needed:
partial-overlap cells fail under no decomposition

private identity needed:
task-relevant private cells degrade under complete invariance

probability-valued missing state needed:
mean regression fails when posterior shape matters

Diffusion headroom:
Gaussian and mixture baselines fail on multimodal cells

Flow headroom:
affine mapping fails on a semantic-preserving nonlinear distortion

Laplace headroom:
matched direct time-domain latent is not uniformly better
```

## E2 — learned missing posterior

Run only if E1 establishes posterior headroom. Freeze modal slots and support.

Compare:

- posterior mean;
- heteroscedastic Gaussian;
- mixture-density network;
- generic latent Diffusion;
- support-aware modal Diffusion.

The missing posterior conditions on canonical shared state, observed-private
state, acquisition metadata and the current observation:

\[
q_\theta(
\Theta_{m,d}\mid
\Theta_c^*,\Theta_{p,d},\mathcal O_d).
\]

Primary outcome: paired CRPS or NLL on the recoverable-missing modal state.
Use paired bootstrap intervals over latent events.

### Diffusion stop rule

Stop the Diffusion branch when a Gaussian or mixture model is statistically
equivalent on the primary metric, calibration and downstream decision.

## E3 — source-only canonicalization headroom

Before neural Flow, compare:

- identity;
- affine calibration;
- whitening;
- CORAL;
- MMD;
- minibatch OT;
- paired physical-anchor mapping.

Hold out one acquisition operator. The canonical target must be source-only and
physically anchored by known modal slots or paired events. A population
barycenter is not interpreted as per-observation posterior equality.

### Flow stop rule

Do not train Flow when affine calibration, CORAL or minibatch OT matches paired
shared-state error and task preservation.

## E4 — learned shared Flow

Run only if E3 reveals nonlinear headroom. Freeze the modal encoder, role
assignment and private path.

Compare:

- generic latent Flow Matching;
- OT-CFM on the same modal state;
- support-constrained modal Flow.

Primary metric: paired shared modal MSE on a held-out acquisition operator.
Report task log-loss, class-conditional retrieval, acquisition-ID probe,
number of function evaluations, latency and memory as secondary results.

## E5 — triangular combined model

Combine only the mechanisms that passed E1--E4:

```text
shared canonical Flow
→ unchanged observed-private state
→ missing posterior conditioned on canonical shared and private state
→ global-null unsupported marker
```

The commuting-generator theorem is a decoupled null baseline, not a claim about
the final conditional model.

## E6 — real paired-rate PHM pilot

Select raw high-rate recordings with a clear license and machine or recording
group key.

Protocol:

1. split machines or recordings first;
2. generate high, intermediate and anti-aliased low-rate views inside each
   split;
3. keep paired view identity;
4. freeze support threshold, normalization, HPO and canonical anchor using
   source data only;
5. evaluate an unseen rate or sensor response;
6. use event-local windows appropriate for the declared transient model.

## Statistics

Predeclare:

- one primary comparison per mechanism;
- one primary metric per mechanism;
- paired differences at the independent-unit level;
- paired bootstrap confidence intervals;
- all source, held-out and worst-condition results;
- fixed tuning trials and compute budget;
- confirmatory versus exploratory outcomes.

## Stop conditions

Simplify or stop when:

- common support is consistently empty;
- global-null recovery is presented as source evidence;
- unpaired source data cannot identify the missing conditional;
- metadata conditioning matches role-aware recovery;
- Gaussian or mixture posterior matches Diffusion;
- affine/CORAL/ordinary OT matches Flow;
- the local modal residual is too large;
- private modes contain only acquisition identity;
- only one of the three active mechanisms has measurable value.
