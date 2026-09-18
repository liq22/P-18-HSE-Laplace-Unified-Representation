# TII 引言意群（作者用）

一级问题是多源异构工业数据的源支持潜在后验与跨数据集诊断；HSE–LLapDiff是方法主线；R/head_affine/M是其中条件接口的三级归因。TII不加入非工业数据，TPAMI文件不在此轮改写。

| 段 | 唯一逻辑任务 | 主要文献／已知能力 | 必须建立的过渡 |
|---|---|---|---|
| 1 | 解释工业观测支持为何影响跨数据集诊断 | HSE/FISHER已解决异构接口与采样率相关结构 | 统一shape不能决定某个缺失成分能否由源数据推断 |
| 2 | 承认表征与共享／私有学习的已有能力 | TS-TCC/TF-C/DSN；Zhao/DomainBed的条件偏移及选模边界 | 不把独立数据集按标签伪配对，区分工况与采集 |
| 3 | 承认缺失视图、masked diffusion、null-space生成已经存在 | MVAE/MMVAE/CSDI/SSSD/DDRM/DDNM/DPS | 当前测量的null space不等于源训练先验可辨识的空间 |
| 4 | 将gap建立在源联合律可辨识性上 | Ambient/Consistent Ambient/A-DPS；iVAE/Locatello | 配对不是唯一可能路线；源支持不是充分条件，VAE坐标不自动是机械模态 |
| 5 | 引出动机图中的关键歧义 | source-supported missing vs source-global-null；先验相关性边界 | 明确只生成源证据支持且条件可辨识的目标，并保留未估计状态 |
| 6 | 提出三个科学困难 | 跨数据集坐标对应；推断资格与过程约束；后验收益与诊断归因 | 每个困难对应下一段的必要能力，而不是“构建模块” |
| 7 | 自然引出HSE条件锚＋受限LLapDiff | Neural Laplace/LLapDiff与Gaussian diffusion的分工 | Laplace是时间域模态表征；其必要性由ordinary latent diffusion/mixture比较决定 |
| 8 | 形成三项相互连接的贡献 | 问题定义、具体推断设计、理论—实验归因链 | 不预填多源LODO成绩或声称原生支持限制已实现 |

## Challenge → mechanism → observable consequence

| 科学挑战 | 现有能力未直接解决的难点 | 必要机制 | 可观察后果与实验 |
|---|---|---|---|
| C1 识别可比较的观测支持 | 非线性latent未必有物理语义；同频率并不等于同模态 | source-established reference、row-space/块支持、target-common correction | 模态/子空间对应误差、混合坐标反例，E4/E5 |
| C2 只在有依据的空间做概率推断 | source union≠conditional identification；后验可来自未验证的先验相关性 | 资格子空间G、逐步投影、observed-evidence旁路、显式未估计状态 | 禁止方向生成能量、coverage与posterior score，E2/E4 |
| C3 区分统计锚、生成器及诊断效应 | 坐标/容量/评分/测试选择混杂；概率质量不保证F1 | 同头条件消融、同支持生成器对照、固定原始组LODO | 同target ES与每数据集macro-F1分开报告，E1/E2/E3 |

正文没有PR/branch/核验日志。`literature_matrix.md`保存31篇原始工作实际阅读的范围、机制、干预和论证位置；HSE/TF-ProFM的期刊全文访问边界单列，未计入31篇。不得因引用数达标宣称实际工业方法已经验证。
