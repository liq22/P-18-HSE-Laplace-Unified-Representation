# Experiment plan

## Rule

Each experiment changes one scientific decision. The independent unit is a
`latent_event_id` in synthetic work and a machine, bearing, run or recording in
real work. Multiple acquisition views of one unit are paired observations, not
independent samples.

Every completed run records command, configuration, data and split version,
seed, environment, terminal state, metrics and interpretation boundary. No
custom hash, receipt or ledger is required.

## E0 — analytic contract

Check:

- four structural projectors are orthogonal and sum to identity;
- source-supported missing and source-global null are distinct;
- indefinite covariance is rejected;
- observed-private and global-null coordinates remain unchanged;
- structural observability and instance reliability are separate;
- soft slot weights obey monotonicity and threshold behavior;
- stable Laplace transitions satisfy the analytic norm bound.

Failure blocks all empirical work.

## E1 — known-pole mechanism factorial

Use paired acquisition views generated from the same latent event. Split
`latent_event_id` before creating views.

### Main 2 x 2 x 2 factors

```text
full / partial structural support overlap
x
private task-irrelevant / task-relevant
x
unimodal / multimodal source-supported missing conditional
```

### Mandatory identification control

Construct two populations with identical unpaired \(C\) and \(M\) marginals but
opposite \(p(M\mid C)\). Compare:

```text
paired evidence
unpaired evidence
```

The unpaired model must not be credited with identifying the conditional.

### Mandatory Flow headroom control

Use:

```text
invertible affine shared distortion
nonlinear but invertible shared distortion
```

A paired affine map must solve the affine cell. Learned Flow is considered only
in the nonlinear cell.

### Global-null control

Add a coordinate in \(\mathcal H_0\), independent of all supported
coordinates. Correct behavior is:

```text
unsupported / prior-only
```

not recovered.

### Physical-scope controls

Compare:

```text
event-local damped transient
transient + bounded forced component
single switching event
```

These cells measure Laplace model residual and determine whether the physical
scope must be narrowed.

## E2 — observable-role screen

Compare:

```text
no decomposition
complete invariance
hard fixed-slot support
soft fixed-slot support
```

Primary outcome:

\[
\text{paired slot-role error}.
\]

Secondary outcomes:

- shared paired modal error;
- private drift;
- threshold sensitivity;
- acquisition-ID leakage.

## E3 — source-supported missing identifiability screen

Use oracle modal states.

Compare:

```text
unpaired marginal model
paired conditional model
known-simulator conditional
class-only pseudo-pairing
```

Primary outcome:

\[
\text{conditional proper score on held-out latent events}.
\]

A missing posterior may be called data-supported only when the declared
identifiability certificate is present and train/test latent events are
disjoint.

## E4 — posterior-complexity screen

Compare under the same information and split:

```text
posterior mean
heteroscedastic Gaussian
finite mixture
generic latent Diffusion
support-aware modal Diffusion
```

Primary metric: one predeclared proper score, CRPS or NLL.

Secondary metrics:

- interval coverage;
- calibration error;
- task loss for a variance- or multimodality-sensitive target;
- sampling cost.

### Diffusion stop rule

Stop Diffusion development when the strongest Gaussian or mixture model is
equivalent within the paired confidence interval on the primary proper score
and calibration metric.

## E5 — canonicalizer-complexity screen

Use source-only anchors and completely hold out one acquisition operator.

Compare:

```text
identity
paired affine regression
whitening / CORAL
minibatch OT
generic Flow Matching / OT-CFM
support-constrained shared Flow
```

Primary metric:

\[
\text{paired shared modal MSE}.
\]

Secondary metrics:

- task-sufficient semantic statistic preservation;
- class-conditional retrieval;
- source-population discrepancy;
- acquisition-ID probe;
- NFE, latency and memory.

### Flow stop rule

Stop learned Flow when paired affine, CORAL or ordinary OT is equivalent on the
primary error and semantic-preservation metrics.

## E6 — Laplace adequacy screen

Compare equal-dimensional representations:

```text
window-local Laplace modal state
direct time-domain latent
Laplace + bounded forced baseline
```

Primary metric:

\[
\eta_{\mathrm{modal}}
=
\|s-\Phi\Theta\|/(\|s\|+\epsilon).
\]

Also report acquisition-space residual and cross-acquisition task utility.

### Laplace stop rule

Remove Laplace as the main representation when a matched direct time-domain
latent simultaneously improves the primary reconstruction and
cross-acquisition metrics.

## E7 — learned triangular model

Only after E3–E6 show headroom:

```text
shared canonicalizer
-> exact observed-private path
-> source-supported missing posterior conditioned on canonical shared/private
```

Do not jointly add learned poles, event routing, VQ codebooks or foundation
pretraining.

## E8 — real recording-level paired-rate pilot

Protocol:

1. select raw high-rate data with a clear license and grouping key;
2. split machines or recordings first;
3. create anti-aliased high/mid/low-rate views inside each split;
4. freeze support thresholds, normalization, anchors and HPO on source data;
5. evaluate an unseen intermediate rate or sensor response;
6. keep acquisition views of one recording paired.

## Statistical contract

For each mechanism freeze one primary comparison and one primary metric.

| Mechanism | Primary metric |
|---|---|
| role assignment | paired slot-role error |
| shared canonicalization | paired shared modal MSE |
| private preservation | private drift |
| missing posterior | CRPS or NLL |
| complete-invariance harm | paired task log-loss difference |
| Laplace adequacy | modal residual ratio |

Use paired confidence intervals over independent latent events or recordings.
Seeds are implementation replicates, not a substitute for independent units.

## Final stop condition

Stop the combined method when only one block has measurable value or when all
complex mechanisms are matched by simpler baselines. A smaller valid method is
preferred to an unexplained Flow–Diffusion stack.
