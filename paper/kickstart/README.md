# Paper Kickstart

`kickstart/` 是一次性探索区，不是持续同步的项目状态系统。

| File | Use |
|---|---|
| `new_project_intake.yaml` | 首次记录研究对象、failure、已有结果、竞争解释和下一动作 |
| `idea_candidates.yaml` | 仅在方向仍开放时比较候选；已有明确问题时可保持空列表 |
| `core_innovation.md` | 人可读的 provisional front-runner、最近邻差异、可证伪预测与 kill test |
| `story_spine.md` | 可选的论文最短论证线 |
| `minimum_viable_paper_plan.md` | 可选的 research-to-paper 参考，不是固定 SOP |

完成首次整理后，将当前事实写入 `paper/paper.yaml.research_state`。之后：

```text
paper.yaml = 当前态
intake = 原始输入
idea_candidates = 开放方向的候选空间
core_innovation = 尚未获批的前沿候选综合
logs = 历史决策
```

不要维护多份同步状态。`core_innovation.md` 不是 novelty 证明，也不会自动成为论文 authority；方向批准只记录在 `paper.yaml.idea_selection`。

## @初始化入口

方向尚未收敛时，可直接使用根目录 README 中的 `@初始化入口`，或读取：

```text
.agent/references/initialize_core_innovation_prompt.md
```

它会从真实 failure 或未决矛盾出发，使用 M1–M5 搜索结构不同的候选，再用 P01–P15 标记最深层变化，最终形成一个 provisional front-runner。模式是设计镜头，不是覆盖配额或新颖性证据。

## Idea 规则

候选只有在 `retained`、`revised`、成为 provisional front-runner 或准备批准时，才需要完整说明：

- 研究对象、before→after 和 changed object；
- favored/competing mechanism；
- observable prediction 与 rejection condition；
- strongest verified neighbor 或未决检索问题；
- confound-isolating decisive kill test；
- claim boundary 与禁止声称。

`proposed` 候选可以非常简短。探索不需要审批；成为论文 authority 的方向由作者确认，并只记录在 `paper.yaml.idea_selection`。

未知内容保持 `TODO/unknown/unverified`。不要为模板完整制造 claim、reference、experiment、figure、gate、hash、receipt 或审计材料。
