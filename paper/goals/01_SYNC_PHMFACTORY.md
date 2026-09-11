# Goal 01 — PHMFactory accepted-main synchronization

## Scope

Prepare `external/phmfactory/` only after validating the exact current `PHMbench/PHM-Vibench` accepted `main`. This Goal does not modify PHMFactory core.

Current read-only fact: upstream `main` was `9b595f72498621ddb05741ead29d8e7e2b0b7896` when this Goal was written. Re-read it before execution.

## Deliverables

- exact upstream main commit recorded in the run note;
- install/doctor/preflight/Dummy smoke output;
- one real-data configuration with audited labels and independent split;
- selected checkpoint path;
- configured metrics plus independent recomputation from retained predictions/results;
- only after all above pass: parent `.gitmodules` and `external/phmfactory` gitlink update.

## Acceptance

```text
install succeeds
AND phmfactory doctor succeeds
AND phmfactory preflight --config smoke succeeds
AND phmfactory demo succeeds
AND one real-data config uses audited raw data/labels/split
AND a real checkpoint is selected and restored
AND every configured primary metric is finite and independently recomputed
```

Upstream currently states that real-data `baseline_valid` is not requalified. Dummy success alone therefore cannot authorize the gitlink.

## Commands

```bash
git -C /path/to/PHM-Vibench fetch origin
git -C /path/to/PHM-Vibench switch main
git -C /path/to/PHM-Vibench pull --ff-only origin main
python -m pip install -e /path/to/PHM-Vibench
phmfactory doctor
phmfactory preflight --config smoke
phmfactory demo
```

For the real-data config, use the exact local data path and configuration frozen by Goal 03; then recompute the primary metric with the same independent unit/aggregation specified in the paper protocol.

## Failure handling

Stop on any protocol mismatch. Do not patch PHMFactory core, change labels, silently drop samples, switch datasets or add a fallback objective. Report the upstream issue and keep the parent gitlink unchanged.
