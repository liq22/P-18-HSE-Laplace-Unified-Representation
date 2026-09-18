# Results — executed references and actual-message boundaries

## 1. Previously completed scientific corrections

PR10 fixed Gaussian mean-shape/nonfinite handling and condition-wide seed mixtures. The valid Gaussian2.5-nat fixture stays unchanged; invalid broadcast inputs fail. `--expected-seeds` catches a seed missing everywhere. Its planned group-effect fixture is3.0 rather than the old incomplete-mixture1.5. These are computation-semantics checks, not model gains.

## 2. Official Japanese Vowels reference

PR11 runs35227181539,35230324773 and35239616437 executed public UCI128 download, native-length conversion, source-only transform/selection, fitted-coefficient restoration and CSV plots. Reproduce using:

```bash
bash paper_TPAMI/run.sh vowels-reference --archive /absolute/japanese_vowels.zip --output-dir outputs/vowels-reference
bash paper_TPAMI/run.sh reference-plot --csv outputs/vowels-reference/affine_summary.csv --output-dir outputs/vowels-reference/figures
```

Original test370 utterances are unchanged. Source18/6/6 per speaker produces fit162/validation54/reserved-calibration54; valid frame counts are2613/828/833/5687 across fit/validation/calibration/test. Length ranges7–26/10–25/9–25/7–29, all nine classes present. LPC hop is0.0064s, not the raw audio sample interval.

The representation is twelve time-mean LPC values, float64,96 message bytes, not HSE. Onehot ridge has117 fitted coefficient/intercept values. Source validation selects lambda0.0001 from three predeclared choices. Scores are not posterior probabilities.

|Test reference|Accuracy|Macro-F1|Onehot score MSE|Max score difference from R|
|---|---:|---:|---:|---:|
|Ordinary/isotropic|0.8594594595|0.8523978638|0.0451129981|0|
|Full PCA/isotropic|0.8594594595|0.8523978638|0.0451129981|1.80e-15|
|Random orthogonal/isotropic|0.8594594595|0.8523978638|0.0451129981|4.11e-15|
|Whitened/transported|0.8594594595|0.8523978638|0.0451129981|1.78e-15|
|Whitened/isotropic|0.8594594595|0.8523978638|0.0451666902|0.02625145|

All seven models, including the additional equivalent matched rows in `assets/vowels_affine_reference.csv`, give318/370 correct test labels. Full output has21 rows. Source feature condition number16.0680669 becomes approximately1 after whitening, without a classification gain. Restored coefficients reproduce predictions and independently recomputed metrics. Variable one-shot CPU solve times remain descriptive artifact values, not stable latency claims. Calibration did not select the models. Utterance IDs do not justify an iid certificate because session/speaker dependence is unresolved.

## 3. Same-head and precision witnesses

Five actual-conditioner tests now accompany the existing exact-map Notebook. The local same-head affine-consumer collapse residual was4.163336342344337e-17. Existing float64 complete-message recovery was1.7763568394002505e-15 with prefix smallest singular value0.0421791480. These are finite configured-head witnesses, not observations about a trained checkpoint.

A further test sets W_p=I_5, a full-rank head, with raw covariance diagonal coordinates−14 and−15 and the unchanged public floor1e-4. Other code coordinates agree. `MatchedConditioner.moments_from_code` gives:

|dtype|q|message bytes|raw-head max gap|statistical-message max gap|
|---|---:|---:|---:|---:|
|float32|32|128|1.0|0.0|
|float64|32|256|1.0|2.98931626e-11|

The covariance floor plus finite rounding erases the small variance difference in float32. This demonstrates why ideal invertibility does not certify numerical information preservation. It does not justify removing the floor, silently switching dtype or claiming such collisions occur frequently in learned data. `assets/head_coordinate_precision.csv` retains the exact configured values; the native tests reproduce the qualitative equality/difference with the actual implementation.

## 4. Native integration executed, method comparison still pending

Code0aedf0b passed run35239616423. Original native batch reconstruction retained24 comparisons/96 rows and maximum loss difference0 in that run. The new optional `head_affine` loop then ran three actual native denoisers using **four explicitly synthetic events per split**, one anchor update, one denoiser update, two draws and two sampler steps. It checked three restored checkpoints, identical frozen conditioner states,12 finite score rows and128-byte messages. Temporary fixture scores do not enter a method table.

The real-export entry accepts `--arms B1_aux M head_affine`. Costs now distinguish the affine head and statistical factorization actually evaluated, and retain dtype/bytes and parameter/time records. Multi-arm plots require explicit selected pairs and reject draw/sampler or event/seed mismatch. Full current-head validation is recorded in the PR rather than inferred by adding earlier test counts.

## 5. Retained boundaries and missing results

Earlier routing/fusion and independent-calibration CSVs retain static-fusion wins and target-order reversal. They are not new routing contributions. The speech experiment is a real reference/converter, not an HSE/M/LLapDiff/SOTA result. Four other raw converters, genuine source-trained feature/reference checkpoints, learned simple alternatives, direct industrial/general task heads and actual cost-matched M comparisons remain pending. MFPT belongs to the TII reference record, not a duplicated TPAMI method table. Equal or adverse results remain valid completed outcomes.

## Additional replay of the real frozen reference — 2026-09-17

The input is `predictions.csv` from PR11 Actions35230324773, artifact10500548685. It has3346 rows from seven models on54 validation,54 reserved-calibration and370 test utterances. This run does not redownload the raw archive, retrain classifiers, or add independent examples. The prediction-producing modules were unchanged by the subsequently inspected head50e8b1d.

| Split | Utterances | Disagreements across7 models | Minimum common-label margin |
|---|---:|---:|---:|
|Validation|54|0|0.0147057173561|
|Reserved calibration|54|0|0.0131882298621|
|Official test|370|0|0.0007046712398|

The margins are strictly positive on the stored float64 vectors. All hard selectors and convex score mixtures of this fixed bank therefore preserve its classifications on these examples. There is no corresponding population or arbitrary-new-model guarantee, and no iid interval is inferred from utterance IDs with unresolved session dependence.

For a separate exploratory score comparison, fix the pair to ordinary and isotropically whitened ridge. Fit the convex mixture weight by onehot score MSE on validation only. Alpha=1 selects the whitened endpoint rather than a useful interior fusion. The original test results were visible before this replay; the new weight fit does not read calibration/test labels, but this is not a prospective confirmation.

| Split | Ordinary score MSE | Selected-mixture score MSE | Macro-F1 of both |
|---|---:|---:|---:|
|Validation|0.0471501131682|0.0471264083435|0.8126984126984|
|Reserved calibration|0.0479494092798|0.0480499432752|0.7856328856329|
|Official test|0.0451129981094|0.0451666901505|0.8523978638389|

Test score MSE increases by0.0000536920411. Both still classify318/370 test utterances correctly. Identical classifications do not imply identical scores, and none of these scores is described as a calibrated posterior. Nine summary rows and478 per-example agreement rows are retained/generated. Two figures read only the actual summary CSV.

The result stops a classification gate experiment on this observed fixed bank, not the learned conditional-moment comparison. Industrial performance and generalization beyond these saved utterances are not inferred.
