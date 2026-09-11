# Introduction paragraph map — IEEE TII

This is an author-facing logic map. Manuscript prose lives in `main.md`.

| ¶ | Job | Key sources | Required transition / boundary |
|---:|---|---|---|
| 1 | Establish industrial acquisition heterogeneity and state that HSE already provides a heterogeneous interface. Introduce current industrial foundation-model competition. | Nature Reviews Physics for physics-informed framing; HSE; FISHER; TF-ProFM. | The gap is not “first unified industrial representation”; it is target-relevant accessibility under a fixed condition budget. |
| 2 | Separate our question from irregular-time modeling and generic time-series foundation models. | Neural CDE, t-PatchGNN, ContiFormer, Hi-Patch, HyperIMTS, MOMENT, UniTS. | Handling timestamps/sampling scale does not imply equal accessibility to one finite downstream generator. |
| 3 | Introduce the probabilistic target and retain LLapDiff rather than reinventing it. Distinguish physical oracle coefficients, frozen reference latent and learned Laplace parameters. | Neural Laplace, CSDI, LLapDiff. | Better analytical posterior approximation is not automatically better reference-latent generation. |
| 4 | Close generic theoretical novelty. | Alsing–Wandelt; Oko; Spantini 2015/2017; Gneiting–Raftery; Seitzer. | The paper must contribute a concrete industrial intervention and falsifiable estimand, not generic information identities. |
| 5 | Define the matched intervention R versus M. State `M=T(R)` and same-supervision/same-budget control. | Current method; Theory 12 antecedents. | A gain cannot be attributed to new Bayes information; it must come from finite accessibility/fitting. |
| 6 | Introduce acquisition-conditional accessibility and routing headroom. | New mathematical object for this manuscript; generic routing/MoE is not claimed as new. | Router is activated only if the conditional risk profiles cross beyond a practical margin. |
| 7 | State TII evidence contract: recording-level PHM first, external benchmark second, empty Results cells until executed. | PHMFactory protocol; industrial baselines. | Contributions are conditional candidates until real experiments promote them. |

## Citation discipline

Most Introduction citations should come from Nature/Science-family reviews, IEEE TPAMI, ICML, NeurIPS, ICLR, CVPR and directly relevant IEEE TII work. Direct predecessors outside those venues remain mandatory when they define the actual theoretical boundary. Venue prestige never replaces relevance.

Do not write “prior work does not study X” from a missing abstract or inaccessible full text. Use only a positive, source-supported statement about what the original work establishes, followed by the narrower object tested here.
