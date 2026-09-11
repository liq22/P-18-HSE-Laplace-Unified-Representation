# HSE–LLapDiff：原生集成与最小比较 Goal

## 唯一目标与权限

沿用 PR #8 的 `agent/paper-sampled-posterior-study`，目标 `dev`。先读 `AGENTS.md` 和实际分支；不 reset、不强推、不自动合并，不用旧 ZIP 覆盖已经新增的共享监督和原生组件。更新一次短执行清单后进入实现，不再先做纯理论审阅。

本轮只完成 **A 集成验收 → B 原生计算闭环 → C 小规模有效比较**。没有真实 HSE/reference 导出时只阻塞 B 的真实输入片段和 C，不用随机替代组件冒充完成。M 不必获胜；负结果可交付。Flow Matching、全量五臂、全部 SOTA 和真实 PHM 大实验不在第一轮。

## 研究问题与贡献边界

在同样的冻结特征、目标、统计监督、消息预算和 LLapDiff 下，显式全局统计读出能否降低有限去噪器的拟合代价？

当前强控制定义 `R=g_theta(C_F)`；矩头读取 R，Gaussian score 的梯度回到 g_theta；B1-aux 发送 R，M 发送由 R 算出的矩字段和剩余坐标。因此 **M=T(R)**，不能增加相对 R 的 Bayes 信息。可能的收益是信息更容易被有限模型利用，而不是“创造信息”。这不代表任意两个独立学习的压缩器都有这种信息序。

保留一个贡献候选：**经过统计监督的具体 HSE 条件器改动及其同模型增量**。KL、Gaussian 评分、条件期望投影和数据处理是支撑工具，不是重新认领的一般理论创新。参考 LLapDiff、Oko、Alsing、Spantini、Gneiting–Raftery、Seitzer 等直接先例；新近 Hi-Patch/HyperIMTS 用于异构建模比较，不替代 B1-aux。

## C1–C7 落实规则

| 评论 | 实际验收 |
|---|---|
| C1 同监督 | 辅助评分更新最终普通代码的 trunk；保留 detached-head 负测试；两臂使用同一 checkpoint 与冻结边界 |
| C2 信息解释 | 主比较是嵌套消息；若 M 改善，解释有限拟合/计算，而不直接宣称降低 Bayes 压缩损失 |
| C3 条件和分组 | tokens、mask、side 及列名全部明确；原 event 和 recording/group 都隔离；源域与未见采集分开报告 |
| C4 字段消费 | 历史 mask 在全局编码前消费；输出是 dense global summary；分别干预矩前缀和普通尾部；无额外 raw-summary 旁路 |
| C5 数值学习 | score、logdet、Mahalanobis、最小特征值及 near-floor 比例；公开 covariance floor；constant/ridge 强控制；不得把验证恶化直接归因为一种原因 |
| C6 原生 loss | 同 batch、同噪声、同 t，对齐 eps/v/x0、mask reduction、none/global/batch 权重；真实 batch 分母不能换成期望 |
| C7 完成定义 | 实现正确、比较有效、结果可复现、解释准确即完成；等价或更差不触发自动加模块 |

## 两阶段计算定义

```text
冻结 HSE / 源归一化 / patch 选择 → C_F=(tokens, history_mask, side)
    ↓ 可训练 trunk
R[ K D ] → 全局矩头 → Gaussian score，梯度更新 trunk 和矩头
    ↓ 一个 source-validation checkpoint
冻结全部 conditioner 和其输入路径
    ├─ B1-aux：完整 R
    └─ M：[mean(R), vech(chol S(R)), R 的剩余坐标]
    ↓ 两个同构、同初始化策略的原版 LLapDiff
只更新各自 denoiser
```

矩语义针对选定后固定的 R；不保证条件于全部原始波形，更不保证目标采集域校准。第一阶段联合训练 R 不等于无限函数族优化。S=BBᵀ+λI 中 λ 是公开模型约束，不是隐藏 jitter。原始读出可以被下游再投影；读出处的解释与真实消费路径必须一致。

## A：接收补丁和完整仓库验收

```bash
bash paper/run.sh setup
bash paper/run.sh theory
bash paper/run.sh setup-neural
bash paper/run.sh conditioner-tests
```

报告一个最终提交的结果，不累加不同版本测试数。旧精度扰动与形状反例保留，新增内容进入既有理论12及同名Notebook，不创建新编号或审阅目录。

## B：原生组件，然后真实特征

原版 LLapDiff 独立安装。当前组件接口核对版本为 `0631e65cbac59d23822205573ebc7e180ecf0487`；不要强制重置用户已有 checkout。换版本需重新检查实际接口。

```bash
export LLAPDIFF_ROOT=/absolute/path/to/LLapDiffusion
bash paper/run.sh setup-native
# 原生组件、共享梯度、loss、schedule、字段消费和CSV重绘
bash paper/run.sh native-acceptance
```

`native-acceptance` 使用显式合成特征夹具；它不执行 HSE/VAE 导出，不构成方法优势。输出到 `outputs/paper/native-component/`。原生 uniform schedule 已在此步骤实际导出；batch-normalized loss 仍按实际 batch 检查。

真实 NPZ 字段：

```text
tokens[N,K,D], attention_mask bool[N,K]（True=有效）
side[N,A], side_names[A]（不存在时明确 A=0）
targets[N,d], event_id[N], group_id[N], condition_id[N]
z0[N,H,Z], target_mask bool[N,H], query_time_s[N,H]
target_map[d,H*Z]，且 targets=flatten(z0)@target_map.T
```

原始 group 应在 window/view 生成前划分。短 export note 写清真实 HSE 类/checkpoint、eval patch、dropout/归一化状态、侧信息列/单位、参考编码器/latent 标准化、target_map 和原 recording 分组。字串无重叠不代替来源核实。禁止从随机特征反推“真实 HSE 已运行”。

```bash
bash paper/run.sh native-batch --batch /absolute/train.npz \
  --data-note /absolute/export_note.md
```

本地 agent 必须用实际 HSE 和冻结参考编码器生成/核验这些文件。数据或 checkpoint 缺失时，报告具体缺失依赖，不自动换数据或 encoder。

## C：最小配对训练

先真实 batch 通过，再用冻结小配置：

```bash
bash paper/run.sh native-pilot \
  --train /absolute/train.npz --validation /absolute/validation.npz \
  --test /absolute/test.npz --data-note /absolute/export_note.md \
  --device cuda:0 --seeds 0 1 2 --anchor-steps 150 \
  --diffusion-steps 200 --draws 8 --sampler-steps 16 \
  --output-dir outputs/native_pilot_01
```

当前脚本执行 M/B1-aux 两臂；B1 原始参考在真实 HSE 路径上保留，不能用随机投影代替。B0 可先验证上游入口；M0 在主要路径有效后加入，不为凑五臂提前扩大规模。

两臂同一个 source checkpoint、相同初始 denoiser、数据/t/噪声策略、监督和优化预算。只在源验证集选模。主指标是标准化 reference latent 上按有效维数平方根归一的 joint Energy Score；另报告源/未见条件评分、成本和训练曲线。requested sampler steps 与真正函数调用数不混称。checkpoint 只能支持所声明的导出特征管线。

统计：在 condition/event/seed 层精确配对；先平均已执行 seeds，再在原始 recording/group 内平均事件，最后组等权。区间条件于实际训练 seeds，posterior draws 不当独立设备。只有一组不输出伪置信区间；缺失配对必须修复或明确停止，不静默删除。

CONTINUE：正确比较下 M 有可重复且实际有意义的目标收益，再扩展。SIMPLIFY：同监督普通代码等价或更好，保留简单方法。BLOCKED：缺少真实依赖，仅相应片段未完成。不以 p>0.05 宣布等价，不要求 M 必须获胜。

## 后续论文实验，不在首次 pilot 自动执行

五臂 B0/B1/B1-aux/M0/M；oracle 真矩替换、残余去除/打乱、公开 covariance floor、不同同维目标、原生 schedule/噪声参数化、固定点数/固定时长、源域/未见采集。Gaussian 与 finite mixture 使用同条件作概率头控制。

外部强候选按任务：CSDI 用于插补；t-PatchGNN、ContiFormer、Neural CDE、Hi-Patch、HyperIMTS 用于兼容的不规则预测；PatchTST/DLinear 为点预测参考。没有概率头的不输出虚构NLL；没有运行的不填分数。不把“列出 SOTA”当成“已完成 SOTA”。

## 论文与绘图唯一入口

`main.md` 为摘要/英文引言；`introduction_outline.md` 为意群与引用用途；`method.md` 为实际计算；`experiments.md` 为协议；`results_native.md` 为已有原生组件证据及新推导见证；理论12的完整证明和Notebook保持配对。

```bash
# 所有绘图只读CSV，不调用训练/模拟函数
bash paper/run.sh native-figures scores outputs/paper/conditioner-full/score_parts.csv outputs/readout_figures
bash paper/run.sh native-figures alignment outputs/paper/native-component/native_loss_alignment.csv outputs/alignment_figures
bash paper/run.sh native-figures comparison outputs/native_pilot_01/event_scores.csv outputs/pilot_figures
```

图参考指定 nature-figure 的数据优先、物理尺寸、可编辑 SVG/PDF 文字与结论清晰原则；不复制完整治理工具，不宣称期刊认证。引言多数引用相关 Nature-family、TPAMI 和顶会，同时保留必要统计近邻，不凑无关名刊。

论文实验不依赖 PHMFactory 内部、不注入 submodule 路径、不改变 factory 或子模块版本。只通过导出数组、原始分组与记录级split交换数据。维持 `formal_claim_supported=false`；原生组件和有限证明通过不自动授权合并或论文投稿。
