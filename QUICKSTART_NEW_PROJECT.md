# PaperTrace 快速使用

## 1. 初始化

```bash
python scripts/setup_papertrace.py --non-interactive
```

Core 模式足以处理研究状态、方法、代码、实验设计、统计、图表规划和论文写作。只有任务确实需要额外外部能力时才启用 `--profile execution`。

## 2. 选择入口

### 已有项目

把已经确认的事实写入 `paper/paper.yaml`，未知项保留 `TODO`，然后使用：

```text
读取 paper/paper.yaml 和与当前任务直接相关的文件。
找出最影响当前 claim 的一个问题，直接修改主要产物并做一次最近验证。
```

不需要重新填写 intake，也不需要补齐未使用的 lifecycle 文件。

### 新方向或核心创新尚未收敛

```text
@初始化入口
从研究对象、环境、观测、任务、已知失败或未决矛盾出发，生成 3–5 个机制不同的候选。
淘汰只增加模块、损失、规模、数据集或命名的候选；核验最强近邻，保留一个暂定方向，
给出可观察预测、拒绝条件、决定性实验和边界。未知事实不得补写。
```

初始化结果仍是暂定研究判断；作者批准只记录在 `paper/paper.yaml -> idea_selection`。

## 3. 直接推进任务

### 修复代码

```text
复现 sampling-rate metadata 的传播错误。语义不一致时 fail fast；
修改源码和最近的 regression test，不添加 wrapper、fallback 或无关重构。
```

### 设计实验

```text
为 claim C2 设计区分机制解释与 capacity-only 解释的最小公平实验。
明确 independent unit、信息公平、主指标、机制指标、可能结果及其决策含义。
```

### 执行实验

```text
执行已确定的 matched comparison。检查真实输出、重复运行和不确定性；
保存结果并更新 claim decision，不能只写 run record。
```

### 修改正文

```text
依据当前已验证结果重写 Introduction 的目标段落。
保持 claim 强度、数字、引用和适用边界，不输出段落评分或写作审计。
```

### 避免防御性写作

```text
去掉已经稳定文本中的重复 caveat、免责声明、想象中的审稿人反驳和叠加 hedge；
将必要边界写成正向 scope，保留真实不确定性、局限、null result、数字和引用。
```

### 图表与投稿

```text
基于指定结果生成实际图表和 caption。
```

```text
核验目标期刊最新官方要求并生成实际投稿文件；不执行正式提交。
```

## 4. 文件何时创建

默认只维护当前状态和 active source。下列文件在产生真实内容时再创建或填写：

```text
paper/kickstart/idea_candidates.yaml
paper/method/method_spec.yaml
paper/refs/reading_matrix.md
paper/experiments/run_ledger.md
paper/experiments/evidence_matrix.md
paper/assets/figures/figure_manifest.md
paper/assets/tables/table_manifest.md
paper/tex/
paper/reviews/
paper/submission/
```

不要创建占位 claim、run、reference、figure、review 或 submission 文件来表示进度。

## 5. 最近验证

| 修改 | 最近验证 |
|---|---|
| 论文段落 | 重读目标段及相邻逻辑，核对改变的数字和引用 |
| 文献结论 | 核验承担结论的原文和最强近邻 |
| 方法或理论 | 检查 failure、竞争解释、假设、预测、拒绝条件和边界 |
| 代码 | 运行最近的针对性测试或 smoke path |
| 实验或统计 | 检查 independent unit、协议、公平性、指标、不确定性和结果解释 |
| 图表 | 打开资产，核对数据、单位、标签、caption 和正文调用 |
| TeX | 编译一次 |
| 投稿文件 | 确认目标文件存在、可打开且符合官方要求 |

完整仓库测试只在最终 PR 检查时运行一次。
