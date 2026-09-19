# Goal 04 — Gate 1–3: minimal sufficient industrial experiments

## Scientific chain

```text
Contribution
→ Hypothesis
→ Estimand
→ Controlled contrast
→ PHMFactory config
→ Local execution
→ Raw artifact
→ Analysis
→ Claim or claim removal
```

The old Stage-I DCT/MFPT batch is an implementation witness only. Do not rerun the 14 support + 13 method finite witnesses unless a changed implementation invalidates them.

## Gate 1 — one real source batch through the final path

Before an effect experiment, implement the paper method in PHMFactory and pass one real **source-only** batch:

```text
Data Factory record/view
→ source reference + qualification
→ HSE condition
→ eligible basis B_e
→ native velocity loss
→ parameter update
→ intrinsic reverse path
→ shared diagnostic readout
→ checkpoint reload
→ reproduced predictions/metrics
```

Required checks: true parameter gradient/update, non-diagonal basis, empty eligibility, observed-condition consumption, no target/reference leakage into deployment inputs, every-step forbidden energy, checkpoint reload, finite normalized class probabilities.

Gate 1 establishes executability, not superiority.

## Gate 2 — one LODO target × one seed × all decisive configurations

Use one predeclared target dataset only after configs/hyperparameters were fixed from source data. Run every decisive cell once to detect degenerate comparisons, shape/ontology errors, OOM and artifact omissions. Do not use this target result to redesign the method.

Only after Gate 2 has complete artifacts may Gate 3 launch the registered folds/seeds.

## Gate 3 — frozen full experiment

Run qualified LODO folds and preregistered seeds without changing target/condition definitions, HPO spaces, loss weighting, sampler or reader. Independent seeds measure optimization variation; they do not multiply the number of target environments.

---

## E1 — net diagnostic value

### Scientific question

Does the complete source-qualified conditional inference method provide useful diagnostic information beyond the strongest source-selected observed-only method on unseen industrial datasets?

### Primary estimand

For target dataset $e$:

$$
\Delta_{net,e}=U_e(S\!\!\!-\!L)-U_e(B_{obs}^{*}),
$$

where $U_e$ is group-balanced macro-F1 from the target's pooled weighted confusion matrix. Report every $\Delta_{net,e}$; dataset-macro mean is descriptive only.

### Treatment / controls

Minimum retained set:

1. strongest source-selected observed-only HSE/direct classifier;
2. one strong conventional observed-only baseline available in PHMFactory;
3. deterministic conditional predictor;
4. joint Gaussian conditional model;
5. ordinary temporal conditional diffusion `S-T`;
6. complete `S-L`;
7. one external conditional-imputation diffusion baseline (CSDI or SSSD) only if protocol-compatible;
8. Mixture4 only if the non-Gaussian-posterior claim is retained.

Reported literature scores are context only. Any executable row in the main table must be a same-protocol reproduction/adaptation with its actual data access stated.

### Two evaluation tracks

- **M / mechanism track:** fixed source front-end, observed readout and diagnostic consumer.
- **P / performance track:** each method may train/select its own same-grade source-only reader under the same total budget and ontology.

E1's performance conclusion uses P. M does not substitute for a fair whole-method comparison.

---

## E2 — support process × physical-time parameterization

### Scientific question

What part of any effect is associated with the defined eligible-state process, what part with the Laplace-domain physical-time parameterization, and is there an interaction?

### Four cells

| State process | Generic temporal T | Laplace-domain temporal L |
|---|---:|---:|
| Ambient A | A-T | A-L |
| Eligible intrinsic S | S-T | S-L |

Gaussian forward kernel, prediction target, noise-level sampling, loss weighting, reverse sampler/steps, conditioner, source supervision and scored target must be fixed.

### Fairness control

Before interpreting S−A, run an **ambient-clamped C** equivalence check: keep ambient tensor/backbone/parameterization but deterministically clamp the complementary state every step. If S and C are numerically equivalent under the declared mapping, record equivalence and do not manufacture another performance curve.

A may not use complementary ground truth, receive arbitrary high-variance nuisance noise, or allow an untrained complement to alter deployment outputs without an explicit declared process. Without those controls, call S−A only the difference between the two stated processes, not a universal causal effect of support restriction.

### Registered estimands

For larger-is-better utility $U$:

$$
\Delta_{support}=\tfrac12[(U_{S,T}-U_{A,T})+(U_{S,L}-U_{A,L})],
$$

$$
\Delta_{Laplace}=\tfrac12[(U_{A,L}-U_{A,T})+(U_{S,L}-U_{S,T})],
$$

$$
\Delta_{int}=(U_{S,L}-U_{A,L})-(U_{S,T}-U_{A,T}).
$$

Compute them separately for macro-F1 and $U_{ES}=-ES$. The raw table always reports Energy Score in its natural lower-is-better direction.

---

## E3 — conditioner specificity and conditional dependence

### Conditioner question

Does the statistical coordinate transform add value beyond the same auxiliary supervision, the affine head output, and a generic same-budget nonlinearity?

Compare, with the generator/target fixed:

```text
R_aux
H_A
H_M
MLP_budget(H_A)
```

The key specificity estimand is:

$$
\Delta_{coord}=U(H_M)-\max\{U(H_A),U(MLP_{budget}(H_A))\}.
$$

If $H_M\approx MLP_{budget}$, retain a generic-nonlinearity conclusion and remove a statistics-specific performance claim.

### Dependence question

Where a non-degenerate observed posterior or repeated matched references exist, compare conditional paired draws with within-condition re-pairing that preserves empirical marginals. If only one target exists per distinct condition, do not claim true conditional covariance recovery; report proper joint score and aggregate coverage instead.

---

## E4 — qualification, acquisition and failure boundary

This combines the old identification and acquisition-boundary experiments.

### Qualification controls

Use a controlled paired-view setting with known qualification truth when natural datasets do not expose it. Compare:

```text
qualified
geometry-only
wrong qualification
empty/reject
```

Wrong qualification must have a predefined error scale, e.g. set-overlap/Jaccard distance across fixed levels, not an arbitrary random mask. Empty/reject is evaluated jointly with coverage and utility; zero unsupported output alone is never a win.

Report:

$$
Coverage,\quad QualifiedRisk,\quad OverallUtility,\quad UnsupportedEmissionRate.
$$

### Acquisition controls

Use same-recording controlled views to distinguish reversible coordinate/sampling changes from irreversible information loss:

- fixed physical duration vs fixed point count;
- anti-aliased sampling-rate change;
- irregular timestamps;
- long missing intervals;
- bandwidth restriction and deletion of task-relevant support.

Compare the Laplace physical-time branch to matched Fourier/zero-damping and time-MLP alternatives. If Laplace benefit appears only under irregular/long-gap acquisition, restrict the paper claim to that regime.

---

## Statistics and cost

- Statistical unit: machine / acquisition run / raw recording, whichever is the highest trustworthy independent key.
- Within-target uncertainty: paired group bootstrap.
- Optimization variability: seed SD reported separately.
- Do not treat three targets × five seeds as 15 independent environments.
- Record actual parameters, state dimension, NFE, posterior draws, wall time and peak memory.
- Cost Pareto reuses trained checkpoints; do not retrain every draw/step point.

## Failure handling

A zero or negative effect is a completed experiment. If a scientific object is unavailable, record `NA` with the missing assumption instead of substituting a toy score. Do not repeat runs until the sign changes, hide failed seeds, or change folds after target results are visible.
