# HSE–LapDiff

## Working title

**Support-Calibrated Latent Laplace Diffusion for Probabilistic Cross-Acquisition Representation**

## Problem

Heterogeneous industrial acquisitions do not merely rescale the same discrete sequence. Sampling rate, anti-alias filtering, sensor response, timestamps, and missingness change how much information is available about a shared physical event. A deterministic embedding can expose a fixed interface, but it does not state how uncertain the unobserved modal content should remain.

## Gap

HSE maps heterogeneous signals to a fixed latent token interface. LLapDiff models irregular targets as stable Laplace-modal latent trajectories and provides probabilistic generation. The unresolved problem is how acquisition information should enter the HSE condition and calibrate a posterior over one canonical Laplace latent state.

## Method under test

For a window-local modal state \(\Theta\in\mathbb R^m\), acquisition domain \(d\) produces

\[
X_d=A_d\Theta+\varepsilon_d,
\qquad
\varepsilon_d\sim\mathcal N(0,R_d)
\]

in the analytic special case. Its fixed-dimensional information statistics are

\[
b_d=A_d^TR_d^{-1}X_d,
\qquad
J_d=A_d^TR_d^{-1}A_d.
\]

HSE is interpreted as a learned fixed-token approximation to slotwise acquisition statistics and physical metadata:

\[
H_d=
\operatorname{HSE}
(X_d,t_d,m_d,a_d)
\in\mathbb R^{K\times D}.
\]

LLapDiff is then conditioned on \(H_d\) to generate

\[
p_\theta(Z^\star\mid H_d),
\]

where \(Z^\star\) is the canonical stable Laplace latent trajectory shared by paired acquisition views of the same event.

The method aligns the coordinate system, not the posterior uncertainty. Higher-information views may have narrower posteriors than lower-information views.

## Candidate contributions

1. **Acquisition-information HSE conditioning.** A fixed physical token interface that represents signal evidence, structural information, physical time, frequency support, and observation reliability.
2. **Support-calibrated canonical posterior.** Heterogeneous paired views condition one LLapDiff posterior family in the same Laplace coordinate system without complete deterministic invariance.
3. **Theory linked to falsification.** Fixed-dimensional sufficiency, closed-form posterior, information monotonicity, paired identifiability, and the task cost of complete invariance yield measurable predictions for the known-pole experiment.

## What is not claimed

- HSE tokens are not yet proved to recover the exact sufficient statistics outside the analytic oracle.
- LLapDiff is not claimed to be necessary until Gaussian and mixture baselines leave proper-score headroom.
- Stable Laplace dynamics and Flow–Diffusion probability-path theory are prior work, not contributions here.
- No learned-model or real-PHM result currently supports the method.

## Future work

After posterior calibration is established, conditional Flow Matching or diffusion distillation may be studied as faster samplers in the same canonical Laplace latent space. They are not part of the current method.
