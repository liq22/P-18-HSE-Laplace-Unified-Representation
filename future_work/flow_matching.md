# Future work: Flow Matching

Flow Matching is not part of the active HSE-LapDiff method.

It becomes relevant only after two conditions are met:

1. HSE-conditioned LLapDiff produces a calibrated canonical posterior on paired heterogeneous acquisitions;
2. reverse diffusion sampling is measured as a material inference bottleneck.

A later study may train conditional Flow Matching or distill the diffusion sampler in the same canonical Laplace latent space. That study must preserve the posterior target and compare calibration, likelihood or proper scores, latency, memory, and number of function evaluations. Faster sampling alone does not establish a better representation.
