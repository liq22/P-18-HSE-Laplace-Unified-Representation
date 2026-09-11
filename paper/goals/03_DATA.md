# Goal 03 — Data authority

## Scope

PHM datasets are acquired, parsed and split through PHMFactory's accepted public data path. External non-PHM benchmark families follow `paper/experiments/DATA_DOWNLOAD_SOP.md` official sources.

## PHM deliverables

- `PHM_DATA_NOTE.md` with exact PHMFactory revision, data root/metadata, source/license note, label map, original independent group and split rule;
- exact public PHMFactory config + visible overrides;
- one parsed real batch and split audit;
- exported arrays containing paper-required fields plus original group/split/acquisition condition;
- no paper-side PHM reader.

## External deliverables

For each non-PHM dataset: local `DATA_NOTE.md`, official source, version/license, independent unit, split and one parsed smoke batch.

## Acceptance

- PHM data enter the paper only through PHMFactory public interfaces/exports;
- original group identity cannot cross train/validation/test;
- target/test statistics do not fit normalization, representation selection or routing;
- data availability does not imply benchmark validity;
- external official source/license is frozen before a training job.

## Commands

Follow Goal 01 for PHMFactory and dataset-specific commands in `DATA_DOWNLOAD_SOP.md` for non-PHM external benchmarks.

## Failure handling

If PHMFactory cannot expose an auditable valid split/label protocol, HOLD the PHM dataset or open an upstream scientific issue; do not duplicate the reader in the paper repo. If an external source/license is ambiguous, HOLD that external dataset rather than use a mirror after seeing performance.
