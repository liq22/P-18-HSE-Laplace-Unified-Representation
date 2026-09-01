# Experiment Execution Contract

Use this template before `06-experiment-ops` starts any real experiment run. Keep this file as agent guidance; the canonical experiment facts remain `paper/experiments/run_ledger.md` and `paper/experiments/evidence_matrix.md`.

```yaml
contract_id: TODO
contract_mode: review_only  # review_only | executable
hypothesis: TODO
single_change: TODO
baseline:
  run_required: true
  command: TODO
  expected_signal: TODO
execution:
  repo_path: TODO
  editable_paths: []
  run_command: TODO
  config_path: TODO
  data_version: TODO
  seed: TODO
metric:
  primary: TODO
  parser: TODO
  direction: maximize  # maximize | minimize | target
  keep_rule: TODO
  discard_rule: TODO
budget:
  max_wall_time: TODO
  max_runs: TODO
  hardware: TODO
outputs:
  artifact_path: TODO
  log_path: TODO
  ledger_run_id: TODO
claim_impact:
  claim_ids: []
  expected_decision: TODO
stop_conditions:
  - baseline_failed
  - metric_parser_untrusted
  - budget_exhausted
  - artifact_missing
```

Rules:

- `review_only` means no real experiment execution.
- `executable` requires baseline, metric parser, budget, artifact path and log path.
- One run may change only one conceptual factor.
- A completed run is not claim evidence until ledger, artifact/log, metric result, decision and claim impact are recorded.
