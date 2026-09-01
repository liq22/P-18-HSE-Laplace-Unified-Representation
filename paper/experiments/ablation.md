# Ablation and Sensitivity Plan

## Design Questions

- 哪个组件对主结果必要？
- 性能变化来自结构、数据、训练预算还是调参？
- 结论对关键超参数、seed 和数据子集是否稳定？

## Ablation Matrix

| Ablation ID | Claim | Changed factor | Controlled factors | Expected diagnostic value | Runs | Status |
|---|---|---|---|---|---|---|
| A1 | C1 | TODO | TODO | TODO | TODO | planned |

## Sensitivity Matrix

| Parameter/condition | Range | Selection rule | Metric | Result artifact | Interpretation |
|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO | TODO |

## Guardrails

- 不将无效消融隐藏。
- 一次只改变可解释的因素，或使用明确的因子设计。
- 调参预算对 baseline 和 proposed method 公平。
