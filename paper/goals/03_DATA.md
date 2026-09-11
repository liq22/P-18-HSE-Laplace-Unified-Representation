# Goal 03 — Data acquisition and split authority

## Scope

Follow `paper/experiments/DATA_DOWNLOAD_SOP.md`. Freeze official source, version, license, label mapping, independent unit and split before training.

## Deliverables

For each selected dataset: local `DATA_NOTE.md`; raw source path; label map; independent group key; split-before-windowing rule; conversion command; one parsed smoke batch.

## Acceptance

- official source is used;
- license is known or explicitly marked human-verification-required before redistribution;
- original group identity cannot cross train/validation/test;
- target/test statistics do not fit normalization or routing;
- download success is not marked as integration success.

## Commands

Use the dataset-specific commands in `DATA_DOWNLOAD_SOP.md`, then run the parser/converter required by the reproduced baseline. For PHM data, finish Goal 01 acceptance before the parent gitlink is committed.

## Failure handling

If official data, license, labels or group identity are ambiguous, HOLD that dataset. Do not replace it with a mirror or a different dataset after seeing performance.
