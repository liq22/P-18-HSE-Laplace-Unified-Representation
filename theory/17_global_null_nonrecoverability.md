# Theorem 17 — Source-global-null non-recoverability

## Status

**Proved for an additive acquisition model.**

## Purpose

A source-global-null coordinate is absent from every declared source
likelihood. A generative model may still emit samples due to a prior, but those
samples are not source-data-supported recoveries.

## 1. Setup

Decompose

\[
\Theta=\Theta_{\mathrm{sup}}+\Theta_0,
\]

where \(\Theta_0=P_0\Theta\) and

\[
A_dP_0=0
\qquad
\text{for every source domain }d.
\]

The source observations satisfy

\[
Y_d=A_d\Theta_{\mathrm{sup}}+\varepsilon_d.
\]

Assume the noise law does not depend on \(\Theta_0\).

## 2. Lemma 17.1 — likelihood invariance

For every value of \(\theta_0\),

\[
p(\{Y_d\}_d\mid\Theta_{\mathrm{sup}},\Theta_0=\theta_0)
=
p(\{Y_d\}_d\mid\Theta_{\mathrm{sup}}).
\]

### Proof

Because \(A_dP_0=0\),

\[
A_d(\Theta_{\mathrm{sup}}+\Theta_0)
=
A_d\Theta_{\mathrm{sup}}.
\]

The conditional distribution of each observation, and hence their joint
likelihood, is unchanged by \(\theta_0\). ∎

## 3. Theorem 17.1 — zero direct likelihood information

The source likelihood score in a global-null direction is zero:

\[
\nabla_{\theta_0}
\log p(\{Y_d\}_d\mid\Theta_{\mathrm{sup}},\theta_0)
=0.
\]

Consequently the conditional Fisher information supplied by the source
likelihood is

\[
\boxed{
\mathcal I_{\mathrm{source}}(\theta_0\mid\Theta_{\mathrm{sup}})=0.
}
\]

### Proof

Differentiate the likelihood invariance of Lemma 17.1. The score is identically
zero, so its squared expectation is zero. ∎

## 4. Corollary 17.1 — posterior equals prior under prior independence

If

\[
\Theta_0\perp\!\!\!\perp\Theta_{\mathrm{sup}},
\]

then

\[
\boxed{
p(\Theta_0\mid\{Y_d\}_d)=p(\Theta_0).
}
\]

### Proof

By Lemma 17.1,

\[
p(y\mid\theta_{\mathrm{sup}},\theta_0)
=
p(y\mid\theta_{\mathrm{sup}}).
\]

With the factorized prior,

\[
p(\theta_0,\theta_{\mathrm{sup}})
=
p(\theta_0)p(\theta_{\mathrm{sup}}).
\]

Bayes' rule gives

\[
p(\theta_0\mid y)
\propto
p(\theta_0)
\int
p(y\mid\theta_{\mathrm{sup}})
p(\theta_{\mathrm{sup}})\,d\theta_{\mathrm{sup}},
\]

and the integral is constant in \(\theta_0\). Normalize to obtain the result. ∎

## 5. Prior-mediated information is not direct observability

If \(\Theta_0\) is correlated with supported coordinates, observations can
change its posterior indirectly through the prior dependence. This does not
contradict zero likelihood information. The recovered content then comes from a
declared structural prior, not from direct source observability.

## 6. Failure boundaries

1. Adding a new sensor changes the declared source union and may remove a
   coordinate from \(\mathcal H_0\).
2. A nonlinear acquisition can couple nominally null and supported modes.
3. A learned encoder can leak global-null labels through metadata.
4. Prior correlation must not be reported as direct measurement evidence.
5. The theorem is protocol-relative, not an absolute physical impossibility.

## 7. Experimental implication

Randomize a global-null coordinate independently of all supported coordinates.
No source-only estimator should exceed chance or the prior baseline. Report any
posterior output as prior-driven and exclude it from reconstruction or recovery
metrics.
