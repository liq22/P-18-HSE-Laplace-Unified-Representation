# HSE–LLapDiff：原生集成与最小比较 Goal

## 当前范围

沿用 PR #8 的 `agent/paper-sampled-posterior-study`，目标 `dev`。开始前检查工作区和新提交；不 reset、不强推、不自动合并。HSE＋LLapDiff 是唯一当前方法，Flow Matching 保持 future work。

现在只做：**代码集成 → 原生接口验收 → M 对 B1-aux 的小规模配对训练**。B1 保留为参考，B0 用于检查原模型入口。M0、完整五臂、全部 SOTA 和真实 PHM 扩展在主路径有效后再做。不再先进行纯理论审阅，也不要求 M 必须获胜。

本文是唯一执行计划。读 AGENTS.md、本文、Method 和实际 forward，更新一次短清单后执行。保留正确推导与负结果，不新增 reviewer 目录、Goal Registry、完整性链或理论编号。

## 问题与唯一贡献候选

在相同冻结输入、统计监督、消息预算和 LLapDiff 下，**显式全局统计读出是否比受同一监督的普通代码更容易被有限去噪器利用？**

LLapDiff、近似充分表示、Gaussian 评分、矩投影和目标导向 Bayesian 近似均有直接先例。候选贡献是具体条件器及其有效原生比较，不是通用定理、CI 或脚本数量。

当前强控制采用 `R=trunk(C_F)`，矩头读取 R；B1-aux 发送全部 R，M 发送由 R 算出的矩和剩余坐标。因此此处 M 是 R 的确定性函数，不可能增加相对 R 的 Bayes 信息。若 M 更好，应检验有限计算/优化的可利用性。这个结论不适用于任意两个互不嵌套的压缩器。

## C1–C7 的处理

| 评论 | 实施要求 |
|---|---|
| C1 同监督 | 辅助 score 更新实际发送普通代码的 trunk；两臂使用同一源验证 checkpoint，第二阶段冻结全部 conditioner |
| C2 信息解释 | 分清完整输入、R 与 M；不把额外监督、参数或成本解释成信息恢复 |
| C3 条件和分组 | mask、side、side_names 显式提供；event_id 和原始 group_id 均隔离；source/unseen 分开报告且不重拟合目标 |
| C4 消费和冻结 | 历史 mask 在打包前消费；输出是 dense global summary，不复用 patch mask；干预矩前缀/普通尾部并检查原生输出 |
| C5 优化 | 保存 score、logdet、Mahalanobis 和最小特征值；显式 covariance floor；比较 constant/ridge 读出；正定不等于校准 |
| C6 原生 loss | 同 batch 核对 eps/v/x0、目标有效维度、时间和 none/global/batch 权重；公式镜像不代替原生执行 |
| C7 完成定义 | 实现正确、比较有效、可复现、解释准确即完成；负结果不触发自动加模块 |

## 参数共享与冻结

```text
冻结 HSE、源预处理、历史 mask 和实际侧信息 C_F
    ↓
共享可训练 trunk → R[K D] → B1-aux 普通消息
    ↓
全局矩头 → Gaussian score → 梯度回到同一个 trunk
    ↓ source validation 选择一个 checkpoint
冻结 trunk、矩头和输入路径
    ├─ B1-aux = R
    └─ M = [m(R), vech(chol S(R)), R 的剩余坐标]
第二阶段只训练各自同构、同初始化策略的 LLapDiff
```

选定后矩头的条件是固定的 R。有限函数类不保证达到真实 `E[U|R]`、`Cov(U|R)`，更不保证条件于原始波形的完整后验或目标域校准。第一阶段 R 可学习，第二阶段固定。

例：K=4、D=8、二维 U，M 使用5个矩字段＋27个普通字段；B1-aux 发送32个普通字段。矩只出现一次。输出槽是全局 summary，不再一一对应原 patch。统计值在原始读出处验证，原生模型可再投影/归一化。默认不增加 cond_summary_raw 旁路。

## A：全仓集成验收

```bash
bash paper/run.sh setup
bash paper/run.sh theory
bash paper/run.sh setup-neural
bash paper/run.sh conditioner-tests
```

报告同一最终提交的测试，不累加旧版本数量。解析环境不需要 PHMFactory。保留 detached auxiliary branch 负测试，确保能识别无效同监督控制。

## B：原生组件和真实输入

原版 LLapDiff 独立安装，记录实际 revision。组件检查参考 `pixelhero98/LLapDiffusion` 的已读版本 `0631e65`；更换版本先核对接口，不换成模拟去噪器。组件依赖与完整官方数据 trainer 依赖不同。

```bash
# 显式合成输入的原生组件检查，不是 HSE/VAE 实验
bash paper/run.sh native-component
bash paper/run.sh native-schedule --output outputs/native_schedule.csv \
  --prediction v --weight none --normalization none
```

原生 forward 没有 attention_mask 参数。当前实现先屏蔽历史无效值，再输出全局 dense summary；target_mask 控制目标 loss，与历史 mask 不混用。batch 权重用实际 batch 重算，uniform CSV 不冒充 Karras 或随机比值的期望。

真实 train/validation/test NPZ 必须包含：

```text
tokens[N,K,D]；attention_mask bool[N,K]（True=有效）
side[N,A]；side_names[A]（没有侧信息也明确提供 A=0）
targets[N,d]；event_id[N]；group_id[N]；condition_id[N]
原生比较另需 z0[N,H,Z]；target_mask bool[N,H]
query_time_s[N,H]；target_map[d,H*Z]
验证 targets = flatten(z0) @ target_map.T
```

一份短 export note 记录实际 HSE 类/checkpoint、eval patch、dropout/归一化状态、源预处理、侧信息列及单位、参考编码器/latent 标准化、原 recording 分组和 split 命令。文件检查不能代替原记录来源检查，不用人工窗口 ID 掩盖同一 recording 跨集合。

```bash
bash paper/run.sh native-batch --batch /absolute/source_train.npz \
  --data-note /absolute/export_note.md
```

本地 agent 必须真实运行 HSE 与参考编码器导出。仅消费已有特征，只能报告“原生模型消费导出特征”。缺 checkpoint/导出数据时停止这个片段，不用随机输入补齐后宣布真实训练完成。

## C：小规模两臂训练

```bash
bash paper/run.sh native-pilot \
  --train /absolute/train.npz --validation /absolute/validation.npz \
  --test /absolute/test.npz --data-note /absolute/export_note.md \
  --device cuda:0 --seeds 0 1 2 --anchor-steps 150 \
  --diffusion-steps 200 --draws 8 --sampler-steps 16 \
  --output-dir outputs/native_pilot_01
```

这是预声明的小配置，不是已完成证据。先一个真实 batch，再执行。验证只含 source 条件；测试中 source holdout 与 unseen acquisition 分开报告。原始 event/recording 在生成视图/窗口之前分割。

入口训练原版 LLapDiff 和共享读出，不内部替换 HSE/VAE。两臂共享输入、target_map、统计监督、选模规则、初始 denoiser、样本/t/噪声策略、优化次数、mask 和 schedule。B1/B0 参考入口保留，不用随机投影冒充原 HSE。

主指标是标准化 reference latent 的 joint Energy Score，按有效维度平方根缩放。波形/PHM 主张另需同一 decoder 和任务评价。保存逐 event/condition/seed 分数、选模步数、曲线、draw 数和实际成本。训练 seed 与 posterior draw 不是独立设备。区间条件于已运行 seeds；不以 p>0.05 宣布等价。

GO：比较有效且目标收益可重复，再扩五臂。SIMPLIFY：M 无增益或更差，保留 B1-aux。BLOCKED：真实依赖缺失，只标对应片段未完成。结果不自动触发合并或全部 SOTA。

## 后续消融和强方法

五臂 B0/B1/B1-aux/M0/M；oracle 真矩替换、去/打乱残余、显式协方差约束、同 teacher、source/unseen、两个同维且至少一个跨组目标、固定点数/时长。Gaussian/finite-mixture 概率头继续作为强控制。

外部候选按任务适配：LLapDiff；CSDI（插补）；t-PatchGNN、ContiFormer、Neural CDE（不规则预测）；PatchTST/DLinear（点预测）。解析控制保留矩块、自然参数、先验/目标低秩和完整侧输入。未运行项不填分数，不以点预测 MSE 排名代替概率评分。

## 文档、图和解耦

main.md 是摘要/英文引言；introduction_outline.md 是意群/引用用途；method.md 是计算定义；experiments.md 是协议；理论12及同名Notebook支撑矩语义和嵌套信息边界。保留历史正确定理和负结果。

引言以相关 Nature-family、TPAMI 和顶会顶刊为多数，同时保留 Oko、Alsing、Spantini、Gneiting、Seitzer 等直接先例，不凑无关名刊引用。

```bash
# 只读 CSV，不训练、不生成模拟事件
bash paper/run.sh native-figures scores outputs/readout/score_parts.csv outputs/readout_figures
bash paper/run.sh native-figures alignment outputs/paper/native-component/native_loss_alignment.csv outputs/native_figures
bash paper/run.sh native-figures comparison outputs/native_pilot_01/event_scores.csv outputs/pilot_figures
```

论文只消费导出数组/原始分组，不导入 PHMFactory 内部、不改 submodule/factory、不注入路径。没有 PHMFactory gitlink 时不人为添加。图参考指定 nature-figure 的结论优先、数据独立和可编辑矢量文字，一图一个问题，不复制治理框架。

完成：正确原生路径＋有效比较＋可复现产物＋准确正文。formal_claim_supported=false，直到真实学习式证据和独立创新判断成立。
