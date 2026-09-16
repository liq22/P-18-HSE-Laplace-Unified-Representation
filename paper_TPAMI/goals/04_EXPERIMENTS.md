# Goal04 — execute the smallest generalizable comparison

**Scope:** one real M/B1-aux comparison first, then alternate target/encoder/consumer, then single/static/dynamic policies. **Products:** selected source checkpoints, group predictions, native score/cost curves and actual Results updates; no prefilled SOTA scores.

```bash
bash paper_TPAMI/run.sh toy
bash paper_TPAMI/run.sh ablation parameterization smoke
bash paper_TPAMI/run.sh native-pilot \
  --train /absolute/train.npz --validation /absolute/validation.npz \
  --test /absolute/test.npz --data-note /absolute/export_note.md \
  --device cuda:0 --seeds 0 1 2 --output-dir outputs/tpami/native
bash paper_TPAMI/run.sh sota --help
```

**Acceptance:** reference, strongest source-selected single, source-selected static mixture and fixed acquisition policy use actual identical task access. At least two encoder/consumer families and five task-compatible domains are needed before a broad conclusion. Official model APIs and raw conversion are verified before an external run; native-pilot implements only the existing two-arm generation task.

**Failure:** M loses or the static reference wins: report and simplify. Target order reverses: retain failure, do not refit on target. Unsupported SOTA task remains pending, not randomly initialized under the same name. No combinatorial search to rescue the central hypothesis.
