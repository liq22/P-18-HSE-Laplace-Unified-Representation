# Related work and exact gap

## HSE

HSE provides a plug-and-play fixed latent interface for heterogeneous signal types, sampling rates, lengths, and channels through temporal-aware patching and cross-dimensional fusion. The present work does not claim fixed-shape heterogeneous embedding as new. Its question is how HSE conditions a probability distribution over one canonical physical latent state.

## Latent Laplace Diffusion

LLapDiff models irregular multivariate targets as compact latent trajectories with stable complex-conjugate Laplace modes, arbitrary-time evaluation, and gap-aware history conditioning. The present work keeps those principles. It targets the preliminary history representation by replacing generic acquisition conditioning with fixed physical HSE tokens and paired cross-acquisition posterior calibration.

## Conditional time-series diffusion

CSDI and related models establish conditional score-based diffusion for probabilistic imputation. They motivate strong probabilistic baselines, but do not by themselves define a common physical latent coordinate system across sampling rates and sensor supports.

## Irregular and multi-rate encoders

Warpformer, t-PatchGNN, continuous-time models, and related approaches handle irregular timestamps, asynchronous variables, or sampling-rate discrepancies. They must be compared when their input and task contracts match. The narrow gap here is posterior calibration to acquisition information in fixed Laplace modal coordinates.

## Exact novelty statement under test

> HSE tokens approximate acquisition evidence and information for fixed Laplace modal slots, and condition LLapDiff to generate one support-calibrated canonical posterior across paired heterogeneous acquisitions.

The novelty is not “HSE plus Diffusion” by itself. It survives only if the HSE condition improves posterior calibration and cross-acquisition representation beyond acquisition metadata, generic LLapDiff conditioning, Gaussian, and finite-mixture alternatives.

## Flow Matching boundary

Flow Matching is established probability-path methodology. It is retained only as future work for sampling acceleration after the HSE-LLapDiff posterior has been validated.
