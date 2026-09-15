# Results and execution boundary

## 1. What the repository currently demonstrates

The retained results cover analytical posterior studies, native LLapDiff **component** checks, fixed-predictor routing counterexamples, and one real PHMFactory reference acceptance. They do not yet include trained HSE–LLapDiff on real frozen HSE features, learned static/dynamic routing, or the five external-domain method comparisons.

The original native loss/consumption measurements remain attributable to their recorded CI run, not a fresh real-data experiment. Native synthetic components and genuine feature extraction are explicitly different stages.

## 2. Real MFPT reference acceptance

Exact PHMFactory revision: `a0db97364e6d38a927c3ea30c643ebbb821d54d7`. Original accepted config: `configs/baselines/01_mfpt/mfpt_global_average_linear.yaml`, seeds 17/18/19, five CPU epochs. Actions run **34765060233**, job **103744444769**, executed the public install/doctor/smoke/preflight/data preparation/train path, then independently restored all checkpoints and recomputed metrics.

| Seed | Test windows | Accuracy | Pooled-window macro-F1 | Selected epoch |
|---:|---:|---:|---:|---:|
| 17 | 96 | 0.500000 | 0.2222222222 | 4 |
| 18 | 96 | 0.3333333333 | 0.1666666667 | 4 |
| 19 | 96 | 0.1666666667 | 0.0952380952 | 4 |

Mean accuracy is 0.3333333 (sample standard deviation 0.1666667); mean F1 is 0.1613757 (sample standard deviation 0.0636572). This six-parameter reference is intentionally weak; its scores are not HSE method performance. Maximum independent accuracy difference from the framework was 9.94e-9 and maximum F1 difference 4.97e-9. Each test recording has 16 windows, so the independently recomputed recording-balanced pooled metric coincides here; that equivalence does not hold with unequal window counts.

Exported dataset shapes were train `[160,2048,1]` from 10 files, validation `[64,2048,1]` from 4 files, and test `[96,2048,1]` from 6 files. The split is disjoint by original File, not an assertion of independent machines/bearings. Raw and derived waveform arrays are excluded from CI uploads. Numeric diagnostics/predictions are retained in the run artifact; `paper/assets/mfpt_reference_recomputed.csv` records independent recomputation.

The first acceptance run **34764636902** completed all three public trainings but then failed in the parent-side serialization of `ResolvedConfig`. Using the documented `runtime_config()` fixed that integration error. No upstream model, split, epochs or seed was changed to obtain a pass.

## 3. Fixed-predictor routing and fusion controls

Reproduction:

```bash
bash experiments/p19/run.sh toy --events 1024 --seed 0 --output outputs/p19/toy_routing.csv
```

Four scenarios each contain 1,024 independent source events and 1,024 independent test events, with two acquisition views per event. Six methods yield 24 summary rows and 49,152 test-score rows. Repeated methods/views are paired, not additional independent events. Source estimates select arms/weights; only the selected rules are evaluated on test.

| Scenario | Best source-selected single | Static prediction fusion | Hard source route | Conditional soft control |
|---|---:|---:|---:|---:|
| No hard headroom | 0.25190793 | 0.13178764 | 0.25190793 | 0.13179010 |
| Conditional crossing | 0.25037478 | 0.12711208 | 0.17848866 | 0.11676041 |
| Fusion without hard crossing | 0.11125000 | 0.00562500 | 0.11125000 | approximately 0 |
| Target ordering reversal | 0.25439336 | 0.12748929 | 0.32789204 | 0.16534586 |

Entries are observed test MSEs in a declared simulation, not trained industrial models. The exact algebraic hard headroom is 0.075 in the crossing reference law and zero in the dominance law. The soft-control example proves that zero hard headroom cannot eliminate fusion. In the stochastic crossing cell the hard route improves over a source-selected single arm but loses to static fusion. Under target reversal it becomes worse than the selected single. These negative controls constrain the method claim and remain in the paper.

## 4. Manuscript result slots awaiting GPU/data

**Primary learned contrast:** M versus B1-aux with the same checkpoint, supervision, target and total cost. **Secondary contrasts:** B1 reference, best single, static prediction fusion, then justified hard routing. **Industrial table:** recording-balanced pooled-confusion macro-F1, conventional pooled metrics, Energy Score and costs. **External tables:** one task-compatible table per domain, never an average of incompatible metrics.

No values are entered for unrun models. A null/worse M result, static fusion matching routing, or source-to-target reversal completes the corresponding question and leads to simplification. CI acceptance cannot promote these empty method claims.
