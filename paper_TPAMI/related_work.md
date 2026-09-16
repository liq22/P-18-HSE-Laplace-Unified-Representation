# Primary-source comparison and reading scope

## Direct general predecessors

**Predictive V-information, ICLR 2020** [@xu2020usable]: full paper Definitions 1–3 and Proposition 1 inspected. Restricted observer families can make computation useful despite Shannon data processing. Our risk profiles therefore cannot be advertised as the first notion of finite-model usable information.

**Multi-expert deferral, ICML 2024/2025** [@mao2024regression; @mao2025routing]: official PMLR records and the 2025 full Section 2 distinguish fixed and jointly learned experts, costs and learning guarantees. Our fixed-arm headroom and plug-in inequality are simpler supporting tools. They do not give H-consistency for our neural architecture.

**Learn then Test** [@angelopoulos2025ltt]: inspected arXiv:2110.01052 Sections 2.1–2.3 and Theorem 1, including simultaneous testing and calibration. Final publication is Annals of Applied Statistics (2025), DOI 10.1214/24-AOAS1998. The paired Hoeffding/Bonferroni rule here is a transparent specialization, not a new generic risk-control framework. No raw unbounded proper score is silently inserted into a bounded-loss theorem.

**Moirai-MoE, ICML 2025** [@liu2025moiraimoe]: official PMLR 267:38940–38962 verifies the final venue. The accessible full arXiv v1 Sections 3.1–3.2 describes single input projection, decoder-only processing, sparse experts and cluster-informed gating. This reading is distinguished from the inaccessible final PDF, not substituted for an audit of all final-paper claims. It is a direct forecasting/routing baseline where data and compute access can be matched.

**AME-TS, 2026 preprint** [@wang2026amets]: full HTML Sections 3.1–3.4 inspected. A separately trained regime predictor supplies forecastability, seasonality, trend and sparsity; a training-time KL prior aligns expert usage, and inference uses the learned router. Consequently, explicitly supervised structural routing is already a close idea. Our global posterior-moment semantics, fixed-policy comparison and independent certification differ in objective and execution, but a small toy certificate does not establish an empirical advantage. The preprint says code will be released upon publication; do not report an executed reproduction without an actual implementation.

## Representation and conditional generation

MOMENT/UniTS, Neural CDE, t-PatchGNN, Hi-Patch/HyperIMTS establish strong multi-task and irregular-time references. Neural Laplace, CSDI and LLapDiff supply model/target precedents. LLapDiff full v2 Sections 3–5 and Appendices E–H distinguish latent targets, modal prediction and iterative generation; we retain this distinction. Alsing, Spantini, Oko, Gneiting and Seitzer remain mandatory statistical antecedents even when outside the requested venue majority.

The companion industrial manuscript is an internal predecessor, not an unseen competing dataset. Its method or results will not be reintroduced as independent TPAMI contributions. The general manuscript needs target/consumer/budget analysis and genuinely additional cross-domain evidence; five datasets alone do not establish that distinction.

## Verified reading locations

- https://arxiv.org/pdf/2002.10689 — V-information definitions/properties.
- https://proceedings.mlr.press/v267/mao25c.html and https://arxiv.org/pdf/2506.20650 — fixed/joint expert setting.
- https://arxiv.org/pdf/2110.01052 — risk-control testing framework.
- https://proceedings.mlr.press/v267/liu25an.html and https://arxiv.org/pdf/2410.10469 — final bibliographic record plus inspected preprint methodology.
- https://arxiv.org/html/2605.25166v1 — AME-TS methodology and release status.
- https://arxiv.org/html/2605.19805v2 — LLapDiff full methodology/appendices.

No missing abstract, missing code or inaccessible final text is treated as proof that a work omits a mechanism. Empirical SOTA status is not inferred from a paper's own abstract.
