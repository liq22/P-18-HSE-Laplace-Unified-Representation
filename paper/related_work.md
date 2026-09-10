# Related work and the exact unresolved gap

Primary-source check: 10 September 2026. This is a focused comparison, not an assertion that no equivalent work exists. The Introduction uses 16 distinct references, 10 from Nature Reviews Physics, IEEE TPAMI, ICML, NeurIPS, ICLR or CVPR. The six direct specialist/preprint references remain because relevance takes priority over venue counts. See `introduction_outline.md` and `../literature/references.bib`.

| Predecessor | What is already established | What remains to test here |
|---|---|---|
| HSE, Information Fusion 2025 | Heterogeneous signal patching and a common embedding interface | Preserve original P,K,D and test the actual consumed condition, not a replacement oracle |
| LLapDiff, arXiv:2605.19805 | Latent-trajectory diffusion, stable modal prediction, gap-aware conditioning, arbitrary-time evaluation | Does a target-aware condition improve this same generator? No inherited modal or one-step claim |
| Alsing–Wandelt, MNRAS Letters 2018 | Fisher-preserving score compression under stated assumptions | Complete posterior preservation cannot be inferred for arbitrary diagonal tokens |
| Oko et al., arXiv:2501.04641 | Approximate sufficient representations connected to conditional diffusion | A specific conditioner and measurable loss under its actual side inputs, not a new generic sufficiency principle |
| Spantini et al., SIAM JSC 2015 | Prior- and likelihood-informed low-rank posterior approximation | Mandatory prior-whitened low-rank numerical control with actual encoder/storage costs |
| Spantini et al., SIAM JSC 2017 | Goal-oriented posterior covariance and mean approximation | Target-aware inference is not new; compare on the frozen target, not only all physical coefficients |
| Neural Laplace, ICML 2022 | Learning dynamics through Laplace-domain representations | Inherited coordinate machinery, not proof that learned latent poles are physical |
| Neural CDE, NeurIPS 2020; ContiFormer, NeurIPS 2023 | Continuous-time irregular-sequence modeling | Task-compatible external models; no invented predictive density for a point predictor |
| t-PatchGNN, ICML 2024 | Transformable temporal patches and asynchronous multivariate dependence | Relevant learned patch baseline after matching observations, task and budget |
| CSDI, NeurIPS 2021 | Conditional probabilistic imputation | Compare imputation to imputation; do not import its results into forecast ranking |
| Time-IMM, NeurIPS 2025 Datasets and Benchmarks | Cause-driven irregular multimodal time-series evaluation | Protocol context, not PHM evidence or a model row |
| Latent diffusion, CVPR 2022; likelihood-weighted score training, NeurIPS 2021 | Learned latent generation and qualified links from objectives to likelihood | Freeze the actual target and schedule; arbitrary denoising MSE is not an endpoint guarantee |

## The gap after incorporating the strongest controls

A likelihood header is not necessarily the best posterior message for a fixed prior and target. At a fixed Gaussian partition, exact posterior moments give the forward-KL-optimal product approximation. The current natural blocks may be useful for prior reuse or independent-evidence accumulation, but those algebraic properties require a deployment use case and measured cost benefit. They do not defeat moment matching on its own objective.

The candidate research question is therefore: **under equal current-acquisition information, a frozen generation target and explicit encoder/transmission/decoder budgets, can an amortized HSE expose target-relevant posterior structure that the same finite LLapDiff otherwise uses inefficiently?** If actual conditions collide, study compression. If the side input already reconstructs full information, study computation. Do not claim both explanations from the same result without separating them.

The proposed target-calibrated mean/covariance feature remains a candidate. Generic KL identities, Gaussian product projection, Schur complements, coordinate covariance and low-rank optimality are supporting tools. The new numerical controls falsify pure-accuracy preference for natural blocks; they do not yet establish learned superiority.

## Exact primary sources

HSE: https://doi.org/10.1016/j.inffus.2025.103277

LLapDiff: https://arxiv.org/abs/2605.19805 ; official code https://github.com/pixelhero98/LLapDiffusion

Approximate sufficiency: https://arxiv.org/abs/2501.04641v2

Score compression: https://doi.org/10.1093/mnrasl/sly029

Prior-aware approximation: https://doi.org/10.1137/140977308

Goal-oriented approximation: https://doi.org/10.1137/16M1082123

Irregular patching: https://proceedings.mlr.press/v235/zhang24bw.html

The bibliography also provides exact DOI/proceedings links for the Introduction's high-venue background papers. No acceptance status is invented for LLapDiff or Oko et al. Flow Matching remains future work.
