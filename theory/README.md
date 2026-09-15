# Theory index

Each numbered Markdown has one same-stem Notebook in `notebooks/`. Markdown states assumptions and proof; Notebook supplies finite constructive or counterexample checks. Successful execution is not general proof verification or novelty approval.

| ID | Result | Role |
|---:|---|---|
| 00 | Targets, acquisition assumptions and actual condition | Definitions |
| 01 | Full-statistic sufficiency and diagonal-token boundary | Analytic baseline |
| 02 | Closed-form Gaussian posterior | Strong simple baseline |
| 03 | Gaussian information order and general posterior coarsening | Supporting result |
| 04 | Paired conditional identifiability | Protocol requirement |
| 05 | Complete invariance information loss | Motivation under exact assumptions |
| 06 | Posterior sufficiency | Established decision-theoretic support |
| 07 | Stable Laplace dynamics | Inherited property |
| 08 | Sampling-gap perturbation | Supporting bound |
| 09 | Compression versus model fitting | Standard identity applied to actual condition |
| 10 | Conditional denoising projection | Established projection analysis |
| 11 | Exact compressed posterior over finite designs | Computable oracle, not arbitrary plug-in |
| 12 | Normalized precision/natural-parameter error to posterior KL | New project derivation; Gaussian support, not generic novelty |
| 13 | Design-only budget choice and strong moment-matching control | Restricted oracle and complexity/parameterization boundary |

Read 00 -> 01 -> 09 -> 10 for the current condition argument. Read 11 to distinguish exact compressed inference from plug-ins. Read 12 -> 13 with `paper/results_sampled.md` for the fixed-storage sampled experiment.

```
python theory/run_notebooks.py --timeout 180
```

A contribution requires a correct general argument, a passing witness, an explicit closest-work difference and a method-specific prediction. A learned-method contribution also needs the same-information, declared-budget experiment. The generic identities and simple finite-set optimum do not become original contributions because they have files. No learned contribution is admitted by the current sampled oracle.
