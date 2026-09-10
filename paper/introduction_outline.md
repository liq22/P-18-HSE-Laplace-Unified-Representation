# 引言意群与引用用途

正式英文段落在 `main.md`；这里仅解释写作与核查方式，不复制另一篇引言。

| 段落 | 主旨与论证 | 引用及其用途 | 过渡／不得跳步 |
|---|---|---|---|
| P1 | 工业观测经过采集算子；统一表示必须服务特定任务 | Karniadakis 2021：物理与数据；Bengio 2013：表示的任务因素；HSE 2025：已有异构接口 | 从“接口能接收”转向“接口保留什么”；不说已有 HSE 无效 |
| P2 | fixed patch、连续时间、异步 patch 已改善可用性，仍不等于目标后验充分 | PatchTST；Neural CDE；t-PatchGNN；Time-IMM | 区分采样点预算和物理时长，不能把几何变化全归因于 rate |
| P3 | 条件生成与 Laplace 是已有工具，目标 latent 与真实模态不同 | Neural Laplace；CSDI；Latent Diffusion；LLapDiff | 从模型功能转向条件信息；不把 learned pole 当真实识别参数 |
| P4 | 信息缺失与有限计算不足是不同问题 | Oko 2025：近似充分性；Alsing 2018：Fisher 压缩；Song 2021：训练目标与似然条件 | a 实际重建 J 时，不再声称补回信息；不能借用一般定理认领首创 |
| P5 | 目标导向后验近似已经存在，必须正面比较最强参数化 | Spantini 2015、2017 | 矩块同预算优于精度截断；要证明额外成本约束而非忽略 baseline |
| P6 | 冻结实际信息、目标和成本；在目标空间计算误差 | 本文定义与12/13推导 | 原始系数空间排名不等于 LLapDiff 排名 |
| P7 | 提出具体可检验的目标校准条件器路线，区分已完成与计划 | 方法／实验对应 | 不写“预算最优 tokenizer”“SOTA”“普适统一” |

## 文献来源构成

引言使用16篇不同文献，以下10篇来自用户指定范围内的 Nature 系列、TPAMI 或顶级会议，按唯一文献计为 **10/16=62.5%**。其余6篇是不可省略的领域起点与直接理论近邻；不为提升比例删除它们。

| BibTeX key | 已核验发表来源 | 支撑对象 |
|---|---|---|
| karniadakis2021physics | Nature Reviews Physics 3, 422–440, 2021 | 物理信息融入学习 |
| bengio2013representation | IEEE TPAMI 35(8), 1798–1828, 2013 | 表示与任务相关因素 |
| nie2023patchtst | ICLR 2023 | 时间序列 patch 表示 |
| kidger2020cde | NeurIPS 2020 | 不规则观测 |
| zhang2024tpatchgnn | ICML 2024 | 异步 patch 相关性 |
| chang2025timeimm | NeurIPS 2025 Datasets and Benchmarks | 不规则原因與评价 |
| holt2022neurallaplace | ICML 2022 | Laplace 动力学 |
| tashiro2021csdi | NeurIPS 2021 | 条件时序扩散 |
| rombach2022latent | CVPR 2022 | 冻结参考 latent 的表示代价 |
| song2021maximum | NeurIPS 2021 | 去噪权重与 likelihood |

另外6篇：HSE（Information Fusion）、LLapDiff（按已核验 arXiv 引用）、Oko（arXiv）、Alsing–Wandelt（MNRAS Letters）、Spantini 2015和2017（SIAM Journal on Scientific Computing）。不擅自把 arXiv 标成 TPAMI/ICML 正式发表。

期刊比例是编辑核查，不是科学论证。若后续引言改变，应按实际使用的引用重新计数；禁止添加与目标问题无关的 Nature/Science 论文充数。
