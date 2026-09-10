# Verified related work and exact gap (10 September 2026)

Primary-source reading includes the LLapDiff paper and released README, Oko et al. Proposition 3 and its proof, Bayesian approximation papers, and the official irregular-time model pages. This is a focused novelty review, not a proof that no equivalent work exists.

| Work | What is already established | What this project must add, or stop claiming |
|---|---|---|
| HSE, Information Fusion 123:103277 (2025) | Temporal-aware patching and fusion for heterogeneous fault-diagnosis signals | Do not reclaim a fixed heterogeneous interface; preserve P,K,D and compare the actual original HSE |
| LLapDiff, arXiv:2605.19805 (2026) | Latent diffusion, stable Laplace-modal prediction, gap-aware conditioning and arbitrary-time synthesis | Changing the history condition, not adding the same modal generator again; no one-step inference claim |
| Alsing–Wandelt, arXiv:1712.00012 | Score-based Fisher-preserving compression | Fisher preservation is not general posterior sufficiency of arbitrary tokens |
| Oko et al., arXiv:2501.04641v2 (2025) | Approximate sufficiency, conditional denoising bounds and a sampling corollary | Generic conditional KL and denoising projection identities are prior analytical machinery |
| Spantini et al., DOI 10.1137/140977308 (2015) | Optimal low-rank Gaussian posterior approximations, including KL-related objectives | Our constrained directly decoded header is a different restriction, not a new general posterior optimality theory |
| Spantini et al., DOI 10.1137/16M1082123 (2017) | Goal-oriented posterior approximation | Do not claim that task-aware Bayesian compression is new |
| ContiFormer, NeurIPS 2023; arXiv:2402.10635 | Continuous-time attention and expressive irregular-series modeling | Strong point-prediction counterpart; it does not itself provide our Gaussian header guarantee |
| t-PatchGNN, ICML 2024/PMLR 235 | Transformable patches and asynchronous multivariate correlations | Required patch-based external baseline where task and inputs match |
| CSDI, arXiv:2107.03502 (2021) | Conditional diffusion for probabilistic imputation | Compare imputation against imputation, not against target-only forecast results |
| Time-IMM, arXiv:2506.10412 (2025) | Cause-driven multimodal irregularity taxonomy and benchmark | Use its irregularity taxonomy as external stress-test context, not PHM evidence or a model row |

## Surviving gap

The reviewed works do not settle the particular deployment question tested here: under the actual side information, what must a finite HSE condition retain about acquisition-induced modal coupling so that the same LLapDiff can represent the correct conditional target, and what is the cost of approximating that condition?

The current answer is deliberately narrower than a new universal tokenizer. We provide a computable Gaussian distortion analysis, an explicit equal-storage header, and strong controls separating likelihood approximation from posterior-moment preservation. The 24-cell study does not support an extra complex risk selector. A learned posterior-aware HSE contribution remains contingent on the fixed-backbone comparison.

## Not admissible as novelty

Stable poles, Laplace synthesis, ordinary Gaussian KL, conditional mutual information decompositions, Gaussian block projection, and taking the minimum of a finite set are not new general results. Source labels, side information and codebook/layout indices must not become uncounted information. A proof of mathematical existence is not a learned-model performance guarantee.

## Primary sources

- HSE: https://doi.org/10.1016/j.inffus.2025.103277
- LLapDiff: https://arxiv.org/abs/2605.19805 ; official code https://github.com/pixelhero98/LLapDiffusion
- Score compression: https://arxiv.org/abs/1712.00012
- Approximate sufficient representations: https://arxiv.org/abs/2501.04641v2
- Bayesian low-rank approximation: https://doi.org/10.1137/140977308
- Goal-oriented approximation: https://doi.org/10.1137/16M1082123
- ContiFormer: https://arxiv.org/abs/2402.10635 (conference year 2023; preprint posted 2024)
- t-PatchGNN: https://proceedings.mlr.press/v235/zhang24bw.html
- CSDI: https://arxiv.org/abs/2107.03502
- Time-IMM: https://arxiv.org/abs/2506.10412
