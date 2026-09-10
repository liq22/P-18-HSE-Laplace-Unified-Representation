# HSE–LLapDiff：目标与成本明确的后验条件器 Goal 包

## 目标与当前分支

只推进 `HSE + LLapDiff`。Flow Matching 留在 Future Work。沿用当前 PR #8 的 `agent/paper-sampled-posterior-study`，目标 `dev`；不要再建重复论文目录，不修改 `master`，不覆盖其他人在该分支的新提交。开始前先用本地 plan 模式读取 `AGENTS.md`、本文和当前代码，只更新一次不超过20行的实际执行清单，然后进入实验。

当前工作名：**Target-Aware Posterior Conditioning for Heterogeneous Time Series**。

核心问题不是“块比对角多保留信息”，而是：在同一观测、实际侧信息、冻结目标和明确总成本下，应传输哪一种后验条件，才真正改善同一个 LLapDiff？

## 择优吸收本轮评论

| 评论 | 本轮处理 |
|---|---|
| C1、C2 | 保留已存在的后验矩块强基线，补完整均值＋精度块以分离均值误差；加入 product-KL 恒等式和 Schur 方差解释 |
| C3 | 将信息受限与有限计算两种解释写入主问题；完整 a 已能重建 J 时，不声称找回信息 |
| C4、C8 | 冻结目标后计算目标 KL／去噪差；把 Spantini 2017 goal-oriented 作为直接理论和数值控制 |
| C5、C6 | 保留正确 Gaussian 恒等式，收紧上界；演示界的松紧、排序及自然参数误差抵消／放大 |
| C7 | 相位变换包含先验；补廉价 trace-isotropic、矩块控制；任意坐标配对不冒充完整物理模态组 |
| C9、C10 | 相同 partition 的相同计算不称统计等效；分别报告设置数、方法数、事件数 |
| C11、C12 | 固定点数与固定时长分开；已知极点诊断不声称覆盖抗混叠／私有频带；下一轮只增加一个非频率因素与一个极点失配检查 |

不吸收旧治理材料中的 hash、checksum、manifest、receipt、ledger、Goal Registry 或多层 reviewer 文档。现有正确定理和负结果保留。每个论证仍使用一份 Markdown＋同名 Notebook，本轮修改12、13，不增加编号。

## 当前真实状态

PR #8 已有四维系数、11标量可解码头和24个采集设置；这与上一份离线六维19标量增量包不同。禁止机械覆盖。已有336行表是24设计×7方法×2侧输入，并不是336个独立机制。

本轮新控制是一个六维固定分组反例，加4个固定点数／固定时长设计；代码可生成30行表。它没有训练 HSE 或 LLapDiff，不是实机数据。完整参考条件、精度／矩块和低秩都属于解析控制。当前最强新结论是：先明确后验参数化、目标和成本，再决定是否开发耦合条件器。

## 核心文件与阅读顺序

`main.md` 是英文摘要和完整引言；`introduction_outline.md` 给出逐段意群及引用用途；`method.md` 定义实际输入、目标和候选方法；`experiments.md` 保留原实验并记录后续协议。完整证明为 `theory/12_posterior_precision_distortion.md` 和 `13_acquisition_only_budget_choice.md`，同名 Notebook 在 `theory/notebooks/`。

引言16篇不同文献中10篇来自 Nature Reviews Physics、IEEE TPAMI、ICML、NeurIPS、ICLR、CVPR（62.5%）。保留HSE、LLapDiff、Oko、Alsing和两篇Spantini这些直接近邻，不用无关名刊论文凑比例。文献题目、出处和引用键见 `literature/references.bib`；详细统计见引言意群文件。

## G1：同预算参数化与目标控制（本轮可执行）

运行相同观测／先验／分组的 full、natural blocks、full mean + precision blocks、marginal moment blocks、trace-isotropic、prior-aware low-rank。目标只取冻结的最后模态；再加入目标专用的低秩和完整目标矩基线。明确目标专用头不能重建所有物理变量。

主输出：系数 KL、目标 KL、目标去噪差；三种块表示的统计数一致。编码计算、是否需完整后验、是否可缓存、是否可换先验单独说明。不得把低秩因子自由度当传输位数；变动分组必须计入编号。

完成条件：product-KL 恒等式、Schur 次序、目标排名反转、相位含先验变换和廉价等变基线全部通过；报告上界／精确值而不是仅断言上界有效。若精度块没有目标精度或真实计算优势，默认矩块／低秩为后续强参考，不继续寻找它能赢的频率排列。

## G2：实际 HSE 接口与目标相关收益（下一唯一实现目标）

先读真实 HSE 和 LLapDiff 前向路径，记录 O、H、a 和 Z0 的来源。高率参考只能作为各臂共同监督。用同一批样本验证每个字段是否被实际消费、eval patch 是否确定、1/2/3通道 shape 及梯度是否正确。不要把记录在对象上但未被 forward 消费的 metadata 计为已知条件。

固定一套源训练 reference encoder 和 target grid。先用冻结线性目标 L 做能精确求解的控制，再转向真实 Z0；不得由 beta 后验排名推断 learned Z0 排名。保持频率不变，只改变一个缺失位置或阻尼因素，另检查小幅极点失配。固定 P,K 的部署表与固定物理局部时长表分开报告，后者观测数随率变化。

两种定位必须由测量决定：
- 实际条件存在碰撞：测试新增字段是否降低条件信息损失。
- a 已重建 J 且 b 完整：只测试有限计算下是否更易利用，比较 metadata MLP、显式求解器及容量匹配网络。

编码预算逐项记录传输数值／位宽、HSE K,D、所有侧流、encoder延迟、decoder延迟、峰值内存、缓存和训练时间。小矩阵的计时不代表嵌入式设备性能。

## G3：同一个 LLapDiff 的三臂学习式对照（尚未实现）

三臂为 B0原 history conditioner、B1原 HSE、M目标校准 HSE；共享原始观测和a。冻结同一个target VAE权重，统一denoiser架构、v/epsilon/x0参数化、schedule、sampler、optimizer steps、source-validation搜索空间与trial预算。不要只冻结某一臂的denoiser。

M先从最简单的目标均值／协方差特征开始，位于现有D内；不附加未计价的token流。若用蒸馏，必须加入同teacher、同loss的B1控制。把Gaussian与finite-mixture概率头放在同条件下比较。未推导过的残差损失不进入主训练。

主指标：目标联合Energy Score；另报marginal CRPS、条件分层coverage和width、联合相关性、观测依赖性、prior-only负控制、任务macro-F1／检索，以及posterior samples和成本。选择主指标和实际等价阈值后才看测试结果。统计独立单位为latent event，后续是recording；训练seed和后验draw不是独立设备。

GO：在相同信息与实际预算下，超过最强简单条件且目标/任务非劣。HOLD：只改善beta或全局coverage。STOP该复杂模块：Gaussian/mixture或简单条件进入预声明等价区间。不能以p>0.05宣布等价。

## 外部强基线与SOTA候选

“SOTA候选”表示需在冻结任务上重跑的强公开方法，不预先宣称本文超过它们。

| 类别 | 必跑／条件适配 |
|---|---|
| 直接继承 | 原LLapDiff；原HSE；相同a的HSE |
| 后验近似 | 精度块；完整均值＋精度块；边缘矩块；trace-isotropic；Spantini prior-aware与goal-oriented控制 |
| 物理表示 | 同窗口STFT、小波、Prony／matrix pencil、维度匹配直接时域表示 |
| 条件生成 | 同条件Gaussian、finite mixture；CSDI仅进入对应插补协议 |
| 不规则预测 | t-PatchGNN、ContiFormer、Neural CDE；须匹配输入、时间、mask与预测目标 |
| 序列基线 | PatchTST、DLinear；不把点预测MSE排名替代后验proper-score排名 |

现有 `run_official_baselines.sh` 是原模型入口，不是本文HSE接入已完成的证明。先检查外部版本和数据许可，再运行。不可调用的模型保留“未运行／原因”，不伪造分数或静默替换实现。

## 必须消融

固定分组下分别更换自然／均值修正／边缘矩参数化；粗a与完整a；实际目标与全系数指标；有无相位参考变换且先验同步；对角／trace／完整模态组；无蒸馏／同teacher蒸馏；固定点数／固定时长；exact／轻微失配极点。分阶段做，不交叉成巨大基准。

## 与PHMFactory充分解耦

当前基线没有PHMFactory gitlink。不得为了满足文字要求新增submodule或修改外部仓库。论文代码只消费明确导出的数组和记录级split信息；禁止从submodule内部动态导入、改sys.path或复用会静默变更科学协议的factory。将来若用户已有外部PHMFactory，用独立导出步骤产生 waveform、timestamp、mask、sampling_rate_hz、units、recording_id、split；父仓记录版本与命令即可，不建完整性链。

## 一键执行与单独绘图

从仓库根或任意目录使用脚本绝对路径：

```bash
bash paper/run.sh setup
bash paper/run.sh theory
bash paper/run.sh parameterization smoke
bash paper/run.sh parameterization full
bash paper/run.sh sampled full
bash paper/run.sh all smoke
```

纯CSV绘图不重新实验：

```bash
bash paper/run.sh parameterization-figures paper/assets/parameterization_controls.csv outputs/parameterization_figures
bash paper/run.sh figures outputs/paper/sampled-full/sampled_summary.csv outputs/sampled_figures
```

图形参考指定nature-figure的“科学问题优先、可编辑文字、源数据与绘图分离”原则；Python matplotlib，单图一个问题，SVG/PDF/PNG输出。没有复制其整套审计/manifest基础设施，也不声称通过Nature投稿审查。当前脚本只绘制真实CSV，不为未运行的G3/G4生成SOTA表。

## G4：真实PHM后续条件

G3通过后才选择一个许可明确、有raw recording和group key的数据源。先按machine/bearing/recording分割，再做抗混叠采样率视图；source-only预处理与HPO，测试未见中间采样率。异步／传感器失配另作外部效度，不以同记录重采样冒充跨硬件验证。

## 贡献准入与完成交付

理论正确不等于首创，Notebook通过不等于实证。正文中的通用KL、Schur、Gaussian投影、相位协变和低秩先例作为支撑。候选贡献只保留：实际固定预算的目标相关HSE条件器、对其具体目标误差的分析、同信息同模型的可重复训练证据。缺任何一项，不写“已改善LLapDiff”。

每个执行片段留下代码、实际命令、数值CSV、图及正文修改；不新建永久review目录。保留当前PR到dev的单一工作线；GitHub CI和本地验证分别记录。`formal_claim_supported: false` 在真实学习式证据和独立理论/创新审阅前保持。
