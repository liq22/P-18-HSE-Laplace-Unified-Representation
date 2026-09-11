# Goal 01 — PHMFactory accepted-main synchronization and PHM data acceptance

## Scope

PHM data in this paper come through PHMFactory. Do not build a second PHM reader in the parent. Validate the exact current `PHMbench/PHM-Vibench` accepted `main`, then one real PHM dataset through its public configuration/data path. Do not modify PHMFactory core for this paper.

Read-only baseline when this Goal was updated: upstream `main = 9b595f72498621ddb05741ead29d8e7e2b0b7896`. Re-read the ref before local execution.

## Deliverables

- exact upstream main commit;
- public install / doctor / preflight smoke / Dummy demo result;
- PHMFactory dataset source/metadata/config selected for the paper;
- audited label mapping and original recording/bearing/run independent unit;
- verified split-before-windowing or an explicit BLOCKED result if the executed protocol cannot guarantee it;
- selected checkpoint restored for test;
- configured primary metrics and independent recomputation;
- PHMFactory export consumed by the paper without internal imports;
- only after the real-data items pass: add/update parent `.gitmodules` and `external/phmfactory` gitlink.

## Acceptance

```text
public smoke succeeds
AND one PHMFactory real-data config uses the intended raw/metadata source
AND label and original group identity are audited
AND executed train/validation/test split is scientifically acceptable
AND a real checkpoint is selected/restored
AND every declared primary metric is finite and recomputed
AND exported arrays preserve group/split/acquisition metadata
```

PHMFactory's current public documentation states that Dummy is smoke-only and real-data `baseline_valid` is not yet requalified. Therefore the gitlink remains absent until the real-data gate passes.

## Commands

```bash
git -C /absolute/PHM-Vibench fetch origin
git -C /absolute/PHM-Vibench switch main
git -C /absolute/PHM-Vibench pull --ff-only origin main
python -m pip install -e /absolute/PHM-Vibench
phmfactory doctor
phmfactory preflight --config smoke
phmfactory demo
```

Then use the exact real-data config and data root recorded in `PHM_DATA_NOTE.md`. Do not edit a maintained config to hide a protocol mismatch; use visible local overrides or an untracked explicit local config.

## Failure handling

Any silent dataset replacement, sample dropping, group leakage, objective substitution, metric closure failure or checkpoint substitution rejects the slice. Report the mismatch and keep the parent gitlink unchanged. Do not patch PHMFactory core, change labels, silently switch datasets or add a fallback objective.
