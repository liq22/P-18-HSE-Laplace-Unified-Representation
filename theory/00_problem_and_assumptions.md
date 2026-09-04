# Theory 0 — Problem, variables, and assumptions

## Status

Definitions and assumptions. No empirical claim.

## 1. Canonical local state

A window-local physical event is represented by a finite vector

\[
\Theta\in\mathbb R^m.
\]

The coordinate system is fixed across the acquisition operators considered in one experiment. In the intended implementation, coordinates are stable Laplace modal slots with declared damping and frequency semantics.

This is a local approximation. It does not claim that an entire machine is globally finite-dimensional or globally linear.

## 2. Heterogeneous acquisition

Acquisition domain \(d\) observes

\[
X_d=A_d\Theta+\varepsilon_d,
\qquad
\varepsilon_d\sim\mathcal N(0,R_d)
\]

in the analytic oracle, where:

- \(A_d\in\mathbb R^{n_d\times m}\) contains sensor response, filtering, timestamps, channel selection, and sampling support;
- \(n_d\) may vary with acquisition rate and missingness;
- \(R_d\succ0\) is a declared noise covariance.

The learned method may be nonlinear and non-Gaussian. The linear-Gaussian model is used only to prove a tractable special case and define testable targets.

## 3. Canonical prior and posterior

The oracle prior is

\[
\Theta\sim\mathcal N(\mu_0,\Sigma_0),
\qquad
\Sigma_0\succ0.
\]

Every acquisition produces a posterior in the same \(\Theta\) coordinate system:

\[
p(\Theta\mid X_d,A_d,R_d).
\]

Uniform coordinates do not imply uniform uncertainty.

## 4. HSE conditioning contract

HSE outputs a fixed token sequence

\[
H_d\in\mathbb R^{K\times D}
\]

with:

- a Boolean attention mask;
- physical time support in seconds;
- frequency support in hertz;
- signal evidence;
- acquisition information;
- observation reliability.

In the analytic oracle, one token corresponds to one declared modal slot. A learned HSE is expected to approximate the same information semantics without access to the hidden target state.

## 5. LLapDiff contract

LLapDiff is conditioned on \(H_d\) and predicts a posterior over a canonical stable Laplace latent trajectory \(Z^\star\). Paired acquisition views of one `latent_event_id` share the same canonical target.

The active method does not contain Flow Matching. Flow Matching is future work for sampling acceleration only after posterior validity is established.

## 6. Core assumptions

### A1 — shared event

Paired views are generated from the same latent event, not from samples matched only by class.

### A2 — known acquisition specification in the oracle

\(A_d\) and \(R_d\) are known in the theoretical oracle. Learned or misspecified operators require separate error analysis.

### A3 — positive-definite noise and prior covariance

\[
R_d\succ0,
\qquad
\Sigma_0\succ0.
\]

### A4 — stable local Laplace chart

For each oscillatory mode,

\[
s_k=-\rho_k+i\omega_k,
\qquad
\rho_k>0.
\]

### A5 — paired conditional evidence

Claims about \(p(Z^\star\mid X_d)\) require paired observations and targets, a known simulator, or an equivalent physical coupling. Unpaired marginals alone are insufficient.

### A6 — task Markov condition

For posterior-sufficiency results,

\[
Y\perp\!\!\!\perp X_d\mid\Theta.
\]

## 7. Claims not made

The theory does not establish that:

- all heterogeneous time series share one latent state;
- higher sampling rate always means higher information;
- a learned HSE exactly recovers the oracle statistics;
- LLapDiff is always necessary;
- an unobserved high-frequency realization is deterministically recoverable;
- analytic or synthetic evidence proves real PHM performance.
