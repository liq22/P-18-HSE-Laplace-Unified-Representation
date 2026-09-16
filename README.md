# HSE–Laplace research

Two manuscript workspaces share one implementation:

| Workspace | Scope | Entry |
|---|---|---|
| `paper/` | IEEE TII: industrial fault-diagnosis data only, via PHMFactory | [Industrial manuscript](paper/main.md), [goals](paper/goals/README.md) |
| `paper_TPAMI/` | IEEE TPAMI candidate: target/consumer/budget analysis and five external domains | [General manuscript](paper_TPAMI/main.md), [goals](paper_TPAMI/goals/README.md) |

Read [PAPER_SCOPE.md](PAPER_SCOPE.md) before moving results or changing claims. Adding datasets alone does not make an independent TPAMI contribution. Shared theory/code/reference experiments are attributed rather than counted twice.

```bash
python -m pip install -e '.[notebooks,experiments]'
bash experiments/p19/run.sh theory
bash paper_TPAMI/run.sh all-cpu
```

`src/hse_laplace/`, `theory/`, and `experiments/` remain shared. The historical `experiments/p19/` path is an experiment library, not a third paper. Plot commands consume real CSV and export SVG/PDF/PNG. No duplicate trainer or registry is introduced.

All PHM data enter through the accepted `external/phmfactory` submodule. Its MFPT public baseline, three checkpoint restores and independent metrics passed; no dependency advance exists in the current upstream check. This reference is not a learned HSE advantage. Genuine feature/reference checkpoints, learned method comparisons and five-domain conversions/training remain pending.

Local hardware is8×4090; first run uses one GPU and two-GPU training is forbidden. Flow Matching remains future work. Work is merged normally into dev after validation; master and others' branches are preserved.
