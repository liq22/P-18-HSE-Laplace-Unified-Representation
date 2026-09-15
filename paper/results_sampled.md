# Sampled-window evidence — 10 September 2026

## Reproducible scope

```
OPENBLAS_NUM_THREADS=1 bash paper/run.sh sampled full
```

The completed local run used 24 acquisition designs and 6,144 independent coefficient events per design (2,048 per simulator seed 0/1/2). Coefficients recur across designs. All methods within a design see the same noisy waveform. Sparse precision/moment headers have 11 stored scalars including layout ID; the full posterior uses 15. Noise standard deviation is 0.5. No network was trained.

The full run produces 336 rows (24 designs x 7 methods x 2 side-input regimes). [sampled_comparison.csv](assets/sampled_comparison.csv) retains every design's point estimates; regenerate `sampled_summary.csv` for full intervals and diagnostics. The downloadable execution package also contains full-precision tables and figures.

## Descriptive results over 24 designs

| Approximate posterior | Mean joint KL, nats | Mean central marginal 90% coverage | Mean coefficient MSE |
|---|---:|---:|---:|
| diagonal precision | 38.1165 | 0.3180 | 0.5380 |
| within-mode precision | 36.9315 | 0.3232 | 0.5203 |
| magnitude-selected precision | 15.2510 | 0.4821 | 0.5843 |
| posterior-risk-selected precision | 15.2510 | 0.4821 | 0.5843 |
| within-mode posterior moments | 0.7824 | 0.8999 | 0.0700 |
| selected posterior moments | 0.2267 | 0.8999 | 0.0700 |
| full posterior, larger header | approximately 0 | 0.8999 | 0.0700 |

These are descriptive design averages, not independent-dataset performance estimates. KL is forward Gaussian posterior KL, not compression mutual information. Moment and full posteriors have the same univariate marginals but different joint laws.

## Results that change the decision

1. Risk and magnitude select identical patterns in all 24 designs. Their paired gain and interval are exactly zero. The additional risk-selector computation is not justified here.
2. Geometry-adaptive precision blocks reduce joint KL relative to fixed within-mode blocks, but coefficient MSE can worsen and coverage remains poor. Lower KL does not improve every task loss.
3. Exact moment headers are a required strong control, not learned HSEs. Their full encoder-side posterior computation cannot be presented as equal-compute training performance.
4. Full actual A,R side input closes all header-induced errors; maximum absolute mean KL is below 2e-15. Do not selectively hide operator information.
5. The SPD perturbation bound held within numerical tolerance. It can be loose for ill-conditioned precision; validity alone does not make a useful certificate.

## Intervals and one illustrative condition

For design 3 (1024 Hz, 0.08 s, 30 Hz separation, regular sampling), within-mode precision had mean KL 6.3959 and magnitude/risk selection 2.0098. Their marginal 95% event-bootstrap intervals were approximately [6.2719,6.5189] and [1.9657,2.0545]. Event-paired differences are separately written to `paired_gains.csv`; overlapping marginal intervals are not a paired-effect test.

## Boundary

Nine new behavior tests and two new theory Notebooks were run locally. Complete repository execution is a separate PR CI result. Existing Task A/B estimates are preserved.

No learned HSE, LLapDiff training, physical anti-alias resampling, real PHM dataset or SOTA comparison was executed. `formal_claim_supported: false`. The next candidate must beat the strongest simple moment/posterior alternative under an explicit compute and actual-information contract, not just a diagonal plug-in.
