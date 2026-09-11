# P19 experiment entry

This directory contains paper-level experiment entry points only. It does not import PHMFactory internals and does not vendor external SOTA code.

CPU-ready now:

```bash
bash experiments/p19/run.sh theory
bash experiments/p19/run.sh toy
bash experiments/p19/run.sh statistics --input /path/result.csv --reference B1_aux --output outputs/p19/summary.csv
bash experiments/p19/run.sh plot --input outputs/p19/summary.csv --output-dir outputs/p19/figures
```

Data/GPU-dependent entries are still explicit commands:

```bash
bash experiments/p19/run.sh phm
bash experiments/p19/run.sh external
bash experiments/p19/run.sh sota
bash experiments/p19/run.sh ablation
```

They fail fast until their Goal requirements are supplied. This is intentional: a runnable placeholder using random data would be worse than an explicit blocked slice.

Result CSV for `statistics` must contain:

```text
method,condition_id,group_id,seed,unit_id,value
```

`unit_id` is the paired event/window identifier inside an original independent group. `group_id` is recording/bearing/run/subject/station according to the protocol. Candidate/reference key sets must match exactly.
