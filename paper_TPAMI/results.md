# Results — general study

## 1. Shared earlier evidence

`assets/routing_controls.csv` retains the earlier fixed-predictor study: the hard source route loses to static fusion in the crossing cell (MSE 0.178489 vs 0.127112) and fails after target-order reversal (0.327892 vs 0.254393 for the selected single). Moving it out of the industrial manuscript did not create new evidence.

`assets/selection_summary.csv` retains the independent finite-policy calibration study: four scenarios, calibration groups 64/2048, three simulator seeds, 512 source-fit events and 4096 test events per run. At n=64 no candidate passes the simultaneous bound. At n=2048 complementary hard-policy net gains are 0.10231250/0.10158008/0.09908984; under target reversal and a false zero-shift assumption they are -0.25305859/-0.25628125/-0.26331250. The identical reversed observations with a declared 0.4 shift allowance retain the reference. Binary Brier loss and toy cost utilities are not GPU latency or native HSE results. The guarantee remains a classical finite-family specialization, not an independent TPAMI novelty claim.

## 2. Scientific-input corrections (2026-09-17)

The supplied review identified two errors that remained in dev after the manuscript split. The exact pre-fix Gaussian calculation accepted mean `[0]` against a 2-dimensional covariance and other mean `[1,2]`, yielding a misleading finite KL of 2.5 through broadcasting. A nonfinite mean returned NaN. The shared `gaussian_kl` now requires two finite mean vectors matching the same nonempty covariance dimension; invalid inputs fail before evaluation. Valid inputs `[0,0]` and `[1,2]` with identity covariances still give exactly 2.5 nats.

The generic group-statistics entry formerly allowed the same missing seed in both arms of one recording. A regression fixture with common-seed effect 3.0 could report 1.5 after that omission. Each condition now requires the same seed set for every method/group. `--expected-seeds 0 1 2` additionally detects a seed absent from every group; inference from observed rows alone cannot detect that global omission. Existing native plotting checks are retained, not duplicated or replaced.

Actual local command on the inspected two-module slice:

```bash
python -m unittest discover -s tests -p 'test_scientific_input_contract.py' -v
```

Ten new tests passed, including wrong-length/scalar/column/nonfinite means and jointly missing/global missing seeds. These are software regression values, not changes to retained experimental scores. Full combined-checkout CI is recorded in the corresponding PR. No preexisting method result is declared invalid solely from the existence of these bugs; retained scripts are rerun rather than assumed affected.

## 3. Unfinished empirical claims

No genuine multi-domain HSE/reference checkpoint, learned M/B1-aux comparison, external SOTA run or TPAMI method advantage is established. MFPT remains the TII-owned reference acceptance. Each general task still needs genuine input preparation and matched controls against PCA/whitening, orthogonal and learned reparameterizations before statistical-message specificity can be asserted. Source-test shift allowances are sensitivity assumptions, not observable deployment certificates.
