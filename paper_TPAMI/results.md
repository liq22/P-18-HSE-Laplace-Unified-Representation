# Results — executed evidence and untested method claims

## 1. Scientific-input corrections

PR10 corrected the two verified review defects before this reference experiment. Invalid Gaussian mean shapes no longer broadcast into a different-dimensional distribution, and nonfinite means fail. Correct [0,0] versus [1,2] under identity covariance still yields 2.5 nats. Generic group statistics now enforce a common condition-wide seed set; `--expected-seeds` additionally detects a seed absent everywhere. The regression fixture's planned mean effect is3.0, whereas the previous incomplete seed mixture could yield1.5. These values demonstrate software semantics, not model gains.

## 2. First real external data/reference slice

Run35227181539, PR11 initial code d7610230, executed the official UCI archive download, native-length conversion, source fit/validation selection, coefficient restoration, predictions and actual CSV figures on CPU. The command was:

```bash
python -m experiments.p19.japanese_vowels --archive "$RUNNER_TEMP/japanese_vowels.zip" --output-dir "$RUNNER_TEMP/vowels-reference"
```

The later public paper entry invokes the same implementation. Source split was fixed before the real run:18/6/6 utterances per speaker. All nine labels are present in each split; original official test membership is unchanged.

| Split | Utterances | Valid frames | Observed length range |
|---|---:|---:|---:|
|Fit|162|2613|7–26|
|Validation|54|828|10–25|
|Reserved calibration|54|833|9–25|
|Official test|370|5687|7–29|

The representation is **time-mean LPC coefficients**, q=12, float64, 96 message bytes. It is not HSE. The consumer has117 fitted coefficient/intercept scalars and solves onehot ridge; outputs are unnormalized class scores, not posterior probabilities. Source validation selected λ=0.0001 from the predeclared three-value grid for every isotropic arm. Matched controls use the same R-selected λ.

### Test results

| Coordinate / penalty | Accuracy | Macro-F1 | Onehot score MSE | Maximum score difference from R |
|---|---:|---:|---:|---:|
|Ordinary / isotropic|0.8594594595|0.8523978638|0.0451129981|0|
|Full-q PCA / isotropic|0.8594594595|0.8523978638|0.0451129981|1.80e-15|
|Random orthogonal / isotropic|0.8594594595|0.8523978638|0.0451129981|4.11e-15|
|Whitened / transported penalty|0.8594594595|0.8523978638|0.0451129981|1.78e-15|
|Whitened / isotropic|0.8594594595|0.8523978638|0.0451666902|0.02625145|

The full seven-model, three-evaluation-split output contains21 rows. All seven models predict the same test labels:318 correct out of370. PCA and orthogonal matched-penalty rows, omitted from the display for brevity, are retained in the source CSV. Every serialized model was reloaded and its evaluation metrics reproduced. The downloaded prediction CSV was also used to recompute classification outcomes.

Source centered feature condition number decreases from16.0680669 to approximately1 after whitening. That improvement did **not** yield a classification gain here. Transporting the regularizer recovers ordinary scores to floating-point precision. Leaving it isotropic changes real-valued scores but not test decisions in this run. Thus coordinate conditioning, changed regularization and improved task risk must not be conflated.

`assets/vowels_affine_reference.csv` retains the numerical summary without variable one-shot CPU fitting times; the complete run artifact includes those descriptive times, source-trial results, predictions and fitted coefficients. They are not a GPU latency or memory Pareto experiment. Figures display validation and test; reserved calibration is retained in CSV and was not used for selection. No confidence interval or iid certificate is asserted from these utterance IDs, whose session dependence is not resolved.

## 3. Method-specific finite witnesses

The existing main-theory Notebook now checks full-q coordinate/penalty equivalence and its failure under an unchanged isotropic whitening penalty. A separate selected-source solver fixture gave matched errors at most1.20e-15 and a whitening/isotropic score change0.47649716. These are algebraic regression values, not a speech or HSE performance result.

The actual shared moment-conditioner tests additionally verify exact R→frozen T composition and collapse of the mean-only affine-consumer path to an affine R consumer. The full covariance message can still be nonlinear; neither check validates a learned superiority claim.

## 4. Earlier general evidence retained

The earlier routing_controls.csv still shows hard routing losing to static fusion in its crossing cell, and failing after target ordering reverses. The selection_summary.csv retains the finite independent-calibration study with explicit target-shift failures. These are known finite controls, not expanded into new routing contributions. Unknown drift bounds remain sensitivity assumptions.

## 5. What has not been measured

This is one real external **reference** and converter, not a conditional-moment, HSE, LLapDiff or SOTA result. Genuine source-trained R/M features, learned linear/MLP bottlenecks, direct task-head comparison, meaningful same-task cost measurements and all five neural benchmark integrations are pending. Four other raw converters remain pending separately. MFPT remains TII-owned reference acceptance, not duplicated as new TPAMI evidence. A negative M/PCA/MLP or direct-head comparison is retained and can complete the scientific question.
