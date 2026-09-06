# Current results

## Existing linear-Gaussian oracle (retained)

Command:

```bash
python examples/analytic_hse_llapdiff_oracle.py
```

The existing three-dimensional oracle reported:

| Quantity | Low | Mid | High |
|---|---:|---:|---:|
| variance, coordinate 1 | 0.500000 | 0.500000 | 0.333333 |
| variance, coordinate 2 | 0.500000 | 0.500000 | 0.333333 |
| variance, coordinate 3 | 1.000000 | 0.800000 | 0.307692 |
| Gaussian entropy | 3.563668 | 3.452097 | 2.568876 |
| token shape | 3 x 8 | 3 x 8 | 3 x 8 |

These posterior values were calculated from the **full** information statistics. Token shape and masks were checked separately. They do not establish that the posterior was reconstructed from diagonal tokens or that a learned HSE preserves the full statistics.

## Task A: finite theory witnesses, 2026-09-06

Reproduce the current theory witnesses with:

```bash
python theory/run_notebooks.py --timeout 180 --output-dir theory/outputs --summary theory/outputs/summary.json
python -m unittest discover -s tests -p 'test_conditioning_information.py' -v
```

The changed/new witnesses are 01, 03, 09 and 10. Their local runs used isolated kernels and the inspected analytical acquisition/token code. Full repository CI is reported separately in the PR; this table is not a claim that a learned model or the complete new benchmark has been run.

| Witness | Numerical result | Interpretation |
|---|---:|---|
| Original dense-J likelihood-ratio spread | 4.44e-16 | Full-statistic sufficiency positive control retained |
| Actual diagonal-token collision: posterior mean distance | 0.5128728388 | Same exposed tokens can hide coupling when side input is coarse |
| Collision: directed KL between full posteriors | 0.5714285714 nats | Posterior separation, not compression mutual information |
| Full A,R side-input control | posterior means/covariances agree within 1e-12 | J can be recovered outside the token array |
| Non-Gaussian prior / realized high / average high variance | 0.1 / 1.0 / 0.1 | Eventwise variance decrease is not universal |
| Degraded binary observation posterior | 0.74 versus high-view 0.90 | Averaged posterior consistency, not pairwise equality |
| Theory 09: total KL | 0.4552409007 nats | One enumerated binary model |
| Theory 09: compression + fitting | 0.3680642072 + 0.0871766936 | Decomposition residual 2.78e-17 |
| Theory 09: side information exposes O | compression 0; fitting 0.4552409007 | Better condition does not automatically fit the decoder |
| Theory 09: nonconstant two-token example | 0.2374752379 = 0.2042044257 + 0.0332708123 | Independently checks nontrivial coarse conditioning |
| Theory 10: full denoising Bayes risk | 0.2382116886 | Full observation is 90%-accurate, not a clean-state teacher |
| Theory 10: compressed denoising Bayes risk | 0.4737228680 | Same schedule and forward noise, H constant |
| Theory 10: projection gap | 0.2355111793 | Equals the Bayes risk difference |
| Theory 10: cross term | -1.24e-12 | Orthogonality check |
| Theory 10: 160-to-240-node refinement | maximum change 1.42e-11 | Numerical integration check |
| Theory 10: score-identity residual | 1.78e-15 | Direct differentiation of Gaussian mixture density |
| Theory 10: alpha=0 control | epsilon gap 0; x0 gap 0.64 | One diffusion time cannot certify sufficiency |

The uploaded review's clean-observation denoising example had full Bayes risk zero and gap about 0.473723. The new witness deliberately uses a noisy full observation, so its gap is about 0.235511. These are different experiments and are not conflicting measurements.

## What passed and what did not get promoted

The finite checks exercise the intended identities and their counterexamples. The original dense-J and Gaussian positive controls remain valid. The two new actual-condition tests check the current tokenizer rather than a replacement implementation.

No experiment here supports the claim that a small-block token is sufficient, that a learned HSE reduces conditional information loss, or that LLapDiff is superior or calibrated. Generic KL/projection results remain analytical support, not newly admitted paper contributions.

`formal_claim_supported: false`. Task B's paired compression experiment, Task C's learned HSE-LLapDiff comparison, and real PHM experiments remain unstarted.
