# Current results

## Linear-Gaussian analytic oracle

Command:

```bash
python examples/analytic_hse_llapdiff_oracle.py
```

The oracle used one three-dimensional canonical modal state and three nested acquisition operators.

| Quantity | Low | Mid | High |
|---|---:|---:|---:|
| posterior variance, mode 1 | 0.500000 | 0.500000 | 0.333333 |
| posterior variance, mode 2 | 0.500000 | 0.500000 | 0.333333 |
| posterior variance, mode 3 | 1.000000 | 0.800000 | 0.307692 |
| posterior entropy | 3.563668 | 3.452097 | 2.568876 |
| HSE token shape | 3 × 8 | 3 × 8 | 3 × 8 |

The low-rate operator did not observe the third modal slot, so its attention mask was `[true, true, false]`; the mid- and high-information operators used all three slots.

Two observations that differed only along the likelihood null space had identical \((b,J)\). Across four latent test points, the spread of their log-likelihood difference was

\[
1.11\times10^{-15},
\]

consistent with floating-point roundoff.

## Interpretation

These numbers support three finite statements in the analytic model:

1. observation length can change while the sufficient-statistic and token dimensions remain fixed;
2. ordered acquisition information produces ordered posterior covariance and entropy;
3. \((b,J)\) preserves the latent-dependent part of the Gaussian likelihood.

They do not show that a learned HSE recovers these statistics, that LLapDiff is necessary, or that the method improves a PHM task. `formal_claim_supported` remains `false`.
