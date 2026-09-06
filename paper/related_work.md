# Related work and the contribution boundary

## Inherited components

HSE supplies fixed heterogeneous-signal tokenization; fixed input/output shape is not our contribution. LLapDiff supplies latent-trajectory diffusion with stable Laplace modal prediction, arbitrary-time queries and gap-aware conditioning. Its latent target and learned modal parameters must not be treated as the known physical coefficient vector in the analytical oracle.

CSDI is a conditional diffusion baseline. Irregular-time models such as Warpformer, t-PatchGNN and continuous-time encoders are relevant where input, task and budget contracts match. Flow Matching is not an active component.

## Direct analytical predecessors

**Alsing and Wandelt, Generalized massive optimal data compression (2018), arXiv:1712.00012.** Score compression preserves Fisher information under its stated conditions. This motivates acquisition-information summaries, but local Fisher preservation is not a guarantee that an arbitrary diagonal token preserves a full posterior.

**Oko, Lin, Cai and Mei, A Statistical Theory of Contrastive Pre-training and Multimodal Generative AI (2025), arXiv:2501.04641v2.** Definition 1 uses conditional KL to measure approximate sufficiency. Proposition 3 connects encoder sufficiency to conditional denoising error under a bounded-target assumption. Appendix D.5 uses conditional mean differences, total variation, Pinsker and a data-processing bound. Therefore neither “compressed representation controls conditional diffusion” nor the general KL/projection identities in our Theories 9–10 are claimed as first results.

The citation check here covers those sections, not an audit of every proof in the paper. Our Gaussian coefficient oracle is unbounded and must not borrow the bounded-target constant without an added assumption.

## Exact candidate difference

> Under a fixed HSE budget and explicit decoder side information, retain or approximate the acquisition-induced cross-modal coupling needed by the same LLapDiff, and measure the resulting posterior and denoising loss.

| Object | Already available | Still to establish here |
|---|---|---|
| `(b,J)` sufficiency | Gaussian likelihood factorization | Which information the actual token and side inputs preserve |
| score compression | Fisher-information preservation | Posterior-relevant dense or small-block coupling at fixed budget |
| approximate sufficiency | conditional KL and denoising theory | Computable error for a concrete physical conditioner |
| LLapDiff | stable latent-trajectory generation | same-model benefit attributable only to conditioner changes |

If `(H,a)` already reconstructs `J`, absence of off-diagonal entries in `H` is not a novel failure. If Gaussian or finite mixtures perform equivalently under the same condition, retain that negative result. The method claim is unproven until the paired compression and learned experiments are complete.

## Future work

Flow Matching may later accelerate a validated posterior sampler. It is neither an active baseline nor part of the current contribution list.
