# Theory and executable witnesses

Every numbered Markdown has one same-stem Notebook under `notebooks/`. Markdown carries assumptions and proofs; Notebook carries finite examples or counterexamples. Passing a Notebook is neither a novelty decision nor evidence of a trained model.

| ID | Result | Current role |
|---:|---|---|
| 00 | Distinct physical coefficients, reference latent and actual condition | Definitions |
| 01 | Full `(b,J)` sufficiency; actual diagonal-token collision and full-side-input control | Analytic baseline and boundary |
| 02 | Closed-form canonical Gaussian posterior | Strong simple baseline |
| 03 | Gaussian covariance order; general posterior coarsening | Supporting result and counterexample |
| 04 | Paired conditional identifiability | Protocol requirement |
| 05 | Complete deterministic invariance information loss | Motivation under exact assumptions |
| 06 | Posterior sufficiency | Established decision-theoretic support |
| 07 | Stable Laplace dynamics | Inherited property |
| 08 | Sampling-gap perturbation | Supporting bound |
| 09 | Posterior error = actual-condition compression + fitting | New project derivation of a standard identity |
| 10 | Optimal denoising projection gap; epsilon/x0/v and score relation | New project derivation of standard projection theory |
| 11 | Exact conditional after discarding a finite acquisition design; nested-summary loss | Computable Task B oracle, not a generic novelty claim |

## Read the current argument

`00 -> 01 -> 09 -> 10 -> 11`, then `03` for the uncertainty boundary. Retain the other correct analytical results without promoting them to new contributions.

## Contribution rule

A candidate needs a checked general argument, a passing same-stem witness, a novelty comparison, and a method-specific prediction. A learned-method claim additionally needs same-information, same-budget experimental support. A formula being stated and its toy example running are not sufficient for admission.

The generic KL, projection, factorization and covariance results are analytical support. **No new learned-method contribution is admitted by this change.** The candidate contribution is a specific acquisition-coupling conditioner, supported only by a finite coefficient-space compression experiment; a physical-window and same-budget learned comparison are still required in `paper/experiments.md`.

## Run

```bash
python theory/run_notebooks.py --timeout 180
```

The existing runner checks pairing and executes each Notebook. It does not check mathematical correctness or originality. Outputs may be kept under ignored `theory/outputs/`; do not build another registry or review-document hierarchy.
