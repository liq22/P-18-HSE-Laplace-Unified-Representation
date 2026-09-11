# Related Work — TII positioning

The paper is positioned against three different literatures. Missing an abstract or inaccessible full text is never used as evidence that a prior paper did not study an issue; novelty statements below are limited to what the cited primary source or official project explicitly supports.

## 1. Industrial heterogeneous-signal and fault-diagnosis representation

HSE provides a plug-and-play heterogeneous-signal embedding interface for fault-diagnosis foundation models [@li2025hse]. FISHER, accepted by IEEE TII, goes further toward multimodal industrial foundation modeling: its official project states that it handles sound, vibration and voltage, accepts arbitrary sampling rates, and represents sampling-rate increments through STFT sub-bands before a ViT encoder [@fan2026fisher]. TF-ProFM is a recent TII prototype-based time–frequency foundation model for generalizable bearing diagnosis [@pi2026tfprofm]. Recent TII cross-domain diagnosis work such as MSIHAN also shows that target/source relevance and negative transfer remain active industrial concerns [@li2025msihan].

These works rule out claims of being the first industrial foundation representation, the first sampling-rate-aware industrial representation, or the first cross-domain fault-diagnosis model. The remaining question here is narrower: with the same HSE observation access and fixed output budget, does an explicitly supervised statistical reparameterization change what a finite native LLapDiff/diagnostic head can exploit, and does that effect depend on the acquisition condition?

## 2. General and irregular time-series representation

MOMENT [@goswami2024moment] and UniTS [@gao2024units] provide multi-dataset or multi-task time-series foundation-model baselines. PatchTST [@nie2023patchtst] and DLinear [@zeng2023dlinear] are strong simple regular-time references. For irregular observations, Neural CDE [@kidger2020cde], t-PatchGNN [@zhang2024tpatchgnn], ContiFormer [@chen2023contiformer], Hi-Patch [@luo2025hipatch] and HyperIMTS [@li2025hyperimts] address continuous time, transformable patches, hierarchical scales or hypergraph dependencies. Adaptive Time Encoding provides a recent NeurIPS classification baseline for irregular multivariate series [@lee2025ate].

These methods are compared only on task-compatible benchmarks. A point forecaster without a density is not assigned a fabricated NLL; an imputation model is not ranked as if it were a fault classifier. External benchmarks test transfer of the conditioning principle, not industrial validity.

## 3. Conditional generation, compression and goal-oriented statistics

Neural Laplace [@holt2022neurallaplace] and LLapDiff [@you2026llapdiff] motivate the Laplace-domain target and irregular-time trajectory generation. CSDI [@tashiro2021csdi] is a direct conditional diffusion reference for imputation. Alsing and Wandelt [@alsing2018compression] study score compression and Fisher information. Oko et al. [@oko2025sufficiency] connect approximate sufficient representations to downstream conditional generation. Spantini et al. [@spantini2015lowrank; @spantini2017goal] derive prior-aware and goal-oriented posterior approximations. Gneiting and Raftery [@gneiting2007proper] provide the scoring-rule foundation for statistical targets, while Seitzer et al. [@seitzer2022pitfalls] document finite neural optimization pitfalls for heteroscedastic likelihoods.

Accordingly, the generic statements “compression affects conditional generation”, “target moments can be supervised”, and “goal-oriented posterior summaries can be lower dimensional” are antecedents. Our candidate difference is operational: a matched HSE code and its deterministic statistical reparameterization are compared inside the same native generator, and acquisition-conditional risk is used to decide whether global selection or routing is warranted.

## 4. Direct comparison matrix

| Work | Industrial fault task | Heterogeneous acquisition | Probabilistic target | Same-information representation control | Acquisition-conditional selection |
|---|---:|---:|---:|---:|---:|
| HSE | yes | yes | no | not this question | no |
| FISHER | yes | yes, including sampling rate | not the present conditional target | not this question | not claimed here |
| TF-ProFM | yes | multisource/time–frequency | diagnostic prototype | not this question | not claimed here |
| MOMENT / UniTS | broad | multi-domain/task | task dependent | no | no |
| t-PatchGNN / Hi-Patch / HyperIMTS | no PHM-specific claim | irregular sampling | forecasting/classification dependent | no | no |
| LLapDiff | no PHM-specific claim | irregular history | latent trajectory diffusion | inherited reference | no |
| This study | primary PHM + external | explicit acquisition descriptor | frozen-reference latent + downstream diagnosis | yes: B1-aux vs M | only if routing headroom is positive |

The final row is a research contract, not a performance claim. Until the real experiments are complete, `formal_claim_supported=false` remains the correct status.
