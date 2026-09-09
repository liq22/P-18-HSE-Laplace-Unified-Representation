# Current results

## Existing linear-Gaussian oracle (retained)

Command:

```bash
python examples/analytic_hse_llapdiff_oracle.py
```

| Quantity | Low | Mid | High |
|---|---:|---:|---:|
| variance, coordinate 1 | 0.500000 | 0.500000 | 0.333333 |
| variance, coordinate 2 | 0.500000 | 0.500000 | 0.333333 |
| variance, coordinate 3 | 1.000000 | 0.800000 | 0.307692 |
| Gaussian entropy | 3.563668 | 3.452097 | 2.568876 |
| token shape | 3 x 8 | 3 x 8 | 3 x 8 |

These posterior values were calculated from the **full** information statistics. Token shape and masks were checked separately. They do not establish inference through diagonal tokens or learned HSE sufficiency.

## Task A: finite theory witnesses, 2026-09-06

```bash
python theory/run_notebooks.py --timeout 180 --output-dir theory/outputs --summary theory/outputs/summary.json
python -m unittest discover -s tests -p 'test_conditioning_information.py' -v
```

| Witness | Numerical result | Interpretation |
|---|---:|---|
| Original dense-J likelihood-ratio spread | 4.44e-16 locally | Full-statistic positive control retained |
| Actual diagonal-token collision: posterior mean distance | 0.5128728388 | Coarse side input can hide coupling |
| Directed KL between two full posteriors | 0.5714285714 nats | Posterior separation, not compression mutual information |
| Full A,R side-input control | agreement within 1e-12 | J can be reconstructed outside the token array |
| Non-Gaussian prior / realized high / average high variance | 0.1 / 1.0 / 0.1 | Eventwise variance decrease is not universal |
| Degraded binary observation posterior | 0.74 versus 0.90 | Averaged posterior consistency, not paired equality |
| Theory 09: total KL | 0.4552409007 | Enumerated binary model |
| Theory 09: compression + fitting | 0.3680642072 + 0.0871766936 | Residual 2.78e-17 |
| Theory 09: full observation side input | compression 0; fitting 0.4552409007 | Better input does not automatically fit the model |
| Theory 09: nonconstant two-token example | 0.2374752379 = 0.2042044257 + 0.0332708123 | Nontrivial coarse conditioning |
| Theory 10: full / compressed denoising risk | 0.2382116886 / 0.4737228680 | Same schedule, noisy full observation |
| Theory 10: projection gap | 0.2355111793 | Equal to Bayes risk difference |
| Theory 10: cross term | -1.24e-12 | Orthogonality witness |
| Theory 10: quadrature refinement | maximum change 1.42e-11 | 160 to 240 nodes |
| Theory 10: score residual | 1.78e-15 | Independent density differentiation |
| Theory 10: alpha=0 | epsilon gap 0; x0 gap 0.64 | One diffusion time cannot certify sufficiency |

The uploaded review used a clean-observation denoising example (full Bayes risk zero, gap about 0.473723). The present witness deliberately uses noisy observations; its gap about 0.235511 is a different experiment. Exact roundoff-sized residuals can vary across NumPy/BLAS versions. The correct dense-J and Gaussian positive controls are retained.

## Task B: exact compressed posterior, 2026-09-08

Command, run from the repository root:

```bash
python -m pip install -e ".[notebooks,experiments]"
OPENBLAS_NUM_THREADS=1 python -m experiments.synthetic_known_pole.run_compression --events-per-seed 2048 --seeds 0 1 2 --bootstrap 1000 --output-dir outputs/task_b
```

[All 60 rows, selected columns and paired intervals](assets/compression_summary.csv). The retained CSV rounds to ten significant digits without clipping small negative values; the command regenerates the full-precision table with additional diagnostics and two figures.

This is a **coefficient-space** acquisition experiment for four coefficients assigned to two fixed damped modes. No sampled-waveform tokenizer, neural model or hardware filter was run. Prior/design probabilities are known, not learned.

Each cell has 6,144 independent held-out events. The same event has four independently noisy acquisition views; all arms receive the same view and declared side input. Views and coefficient dimensions are averaged within event before bootstrap resampling. Corresponding events are reused across coupling cells, so the cells are not independent experiments. Seeds 0,1,2 are simulator replicates.

### True compression loss

Entries are expected conditional KL estimates in nats, with marginal 95% event-paired bootstrap intervals. These are diagnostic intervals, not a simultaneous multiple-comparison guarantee. Individual log-ratio estimates are not clipped. Zero controls below have absolute magnitude below 1e-12.

| Prior | Cross coupling | Diagonal exact conditional | Block exact conditional | Paired gain of block over diagonal |
|---|---:|---:|---:|---:|
| gaussian | 0 | 0.083534 [0.079170, 0.088016] | 0 (analytic control) | 0.083534 [0.079170, 0.088016] |
| gaussian | 0.45 | 0.136693 [0.130889, 0.142697] | 0.059186 [0.055549, 0.062843] | 0.077507 [0.073511, 0.081762] |
| gaussian | 0.8 | 0.091889 [0.087131, 0.096253] | 0.039478 [0.036462, 0.042468] | 0.052411 [0.048737, 0.055937] |
| mixture | 0 | 0.055256 [0.052178, 0.058788] | 0 (analytic control) | 0.055256 [0.052178, 0.058788] |
| mixture | 0.45 | 0.089283 [0.084986, 0.093364] | 0.037205 [0.034546, 0.039723] | 0.052078 [0.048968, 0.055283] |
| mixture | 0.8 | 0.061142 [0.057404, 0.065027] | 0.024326 [0.021822, 0.026732] | 0.036816 [0.034014, 0.039673] |

Full operator side information closes the compression and denoising gap for every arm to numerical precision. A block gain is conditional on missing operator information, not automatic because tokens omit a matrix entry.

The loss is not monotone in cross coupling: changing the design also changes how informative b is about the hidden design. Off-diagonal matrix norm alone is not a sufficient proxy for information loss. The correct conditional mixture remains calibrated while less informative; information loss is not itself miscalibration.

**Compression figure:** `outputs/task_b/compression.svg` plots the exact diagonal/block conditionals for both priors, with event-paired confidence intervals. The non-monotone curves and positive block residuals are retained.

### Plug-in fitting error is not token loss

At cross coupling 0.8:

| Prior / model | Total log-score gap | Compression component | Fitting component | 90% central marginal coverage |
|---|---:|---:|---:|---:|
| gaussian / diag_exact | 0.091889 | 0.091889 | 0.000000 | 0.9017 |
| gaussian / diag_plugin | 0.601327 | 0.091889 | 0.509438 | 0.8371 |
| gaussian / block_exact | 0.039478 | 0.039478 | 0.000000 | 0.9018 |
| gaussian / block_plugin | 0.409752 | 0.039478 | 0.370274 | 0.8548 |
| mixture / diag_exact | 0.061142 | 0.061142 | 0.000000 | 0.9001 |
| mixture / diag_plugin | 0.367740 | 0.061142 | 0.306599 | 0.8589 |
| mixture / block_exact | 0.024326 | 0.024326 | 0.000000 | 0.9005 |
| mixture / block_plugin | 0.238864 | 0.024326 | 0.214538 | 0.8726 |

The plug-in penalty is often larger than the actual compression penalty. A block plug-in can perform worse than the exact diagonal conditional despite retaining more information. This is model mismatch, not a contradiction of information refinement.

Coverage is averaged central marginal coverage, not joint coverage. A prior-only model can also be marginally calibrated. Observation-sensitive endpoints here are joint log-score loss against the full oracle and paired denoising-predictor distance.

**Calibration figure:** `outputs/task_b/calibration.svg` compares 50/80/90% nominal coverage with measured marginal coverage for exact conditionals and plug-ins, separately for each prior at cross coupling 0.8. It is not a learned-posterior calibration claim.

### Decision and remaining scope

- **Retain:** coupling can have information value; exact conditionals marginalize hidden acquisition designs with data-dependent weights.
- **Reject the stronger claim:** within-mode 2x2 blocks are universally sufficient. Hidden cross-mode terms leave positive loss.
- **Retain the null:** full actual operator side input removes the Bayes-information advantage.
- **No learned contribution admitted:** statistics contain 8/10/14 unique layout entries. There is no matched-budget learned HSE comparison. Known Gaussian/finite-mixture oracles represent the true posteriors; Diffusion necessity remains untested.

One theory Markdown/Notebook pair and the behavior tests cover the conditional calculation, its weights, controls, pairing and diffusion-noise boundary. Physical-window compression, learned HSE-LLapDiff and real PHM experiments remain unstarted. `formal_claim_supported: false`.

## Development integration checks, 2026-09-09

The complete Task B command above was rerun with the same 2,048 events per seed, seeds 0/1/2 and 1,000 bootstrap replicates. All 60 rows and 1,500 numeric fields agreed with the supplied full-precision Task B CSV; the maximum absolute difference in this local run was zero. The retained rounded CSV was not overwritten. This is a reproduction check, not additional independent evidence.

The original sign-family determinant is constant across designs. Its observation-space check therefore cannot by itself detect omission of a design-dependent Jacobian. The strengthened same-stem Theory 11 Notebook adds a separate two-design counterexample with unequal determinants:

| Calculation | Design 1 posterior probability | Design 2 posterior probability |
|---|---:|---:|
| Correct score-space likelihood | 0.37678292 | 0.62321708 |
| Observation-space likelihood without Jacobian | 0.54733817 | 0.45266183 |

The maximum weight error is **0.1705552474**. This diagnoses a test-coverage gap; the original score-space implementation already included the correct determinant implicitly and its scientific sweep remains unchanged.

The posterior function now rejects repeated or fractional design indices, inconsistent prior-component counts, nonnormalized weights and nonsymmetric/indefinite covariance inputs. These checks preserve the declared joint distribution instead of silently truncating, reweighting or repairing it. The five added tests cover these cases and verify that plot-only execution never invokes the experiment.

To regenerate figures directly from retained results:

```bash
python -m experiments.synthetic_known_pole.run_compression --plot-only paper/assets/compression_summary.csv --output-dir outputs/task_b_reference
```

Percentile intervals are drawn from their actual endpoints without clipping them to contain the sample estimate. The 8/10/14 layout counts are not Shannon information, minimum storage bits or free parameters of the finite sign family.

Local validation covered the Task B files and the amended Notebook; the complete repository is checked separately by the PR and `dev` push CI. Integrating into `dev` is not novelty approval and does not change `formal_claim_supported: false`.
