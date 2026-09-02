# Theorem 6 — Sufficiency of a posterior-valued representation

## Status

**Proved under Axioms A7 and A9.**

## Purpose

A recoverable-missing physical component cannot generally be encoded honestly
by one point. This theorem shows that the exact posterior of a latent physical
state is sufficient for any downstream task that depends on the observation
only through that state. It does not justify a posterior claim for
source-global-null coordinates.

## 1. Setup

Let \(\Theta\) be a latent physical state, \(O\) an observation and \(Y\) a
downstream target. Assume

\[
Y\perp\!\!\!\perp O\mid\Theta.
\tag{6.1}
\]

Define the random probability measure

\[
R(O)
=
\mathbb P(\Theta\in\cdot\mid O).
\]

## 2. Lemma 6.1 — task posterior is an integral over the latent posterior

For every measurable target event \(B\),

\[
\mathbb P(Y\in B\mid O)
=
\int
\mathbb P(Y\in B\mid\Theta=\theta)
R(O)(d\theta)
\quad\text{a.s.}
\tag{6.2}
\]

### Proof

Apply the tower property:

\[
\mathbb P(Y\in B\mid O)
=
\mathbb E[
\mathbb E[
\mathbf 1_{\{Y\in B\}}
\mid
\Theta,O]
\mid
O].
\]

Conditional independence in Equation (6.1) removes \(O\) from the inner
expectation. The outer conditional expectation integrates the resulting
function of \(\Theta\) against the conditional law \(R(O)\). ∎

## 3. Theorem 6 — posterior representation is sufficient

\[
\boxed{
Y\perp\!\!\!\perp O\mid R(O)
}
\]

or, equivalently, the conditional law of \(Y\) given \(O\) is a measurable
function of \(R(O)\) alone.

### Detailed proof

For a measurable target event \(B\), define

\[
F_B(\mu)
=
\int
\mathbb P(Y\in B\mid\Theta=\theta)\mu(d\theta).
\]

Lemma 6.1 gives

\[
\mathbb P(Y\in B\mid O)
=
F_B(R(O)).
\]

The right-hand side is measurable with respect to the sigma-algebra generated
by \(R(O)\). Hence

\[
\mathbb P(Y\in B\mid O,R(O))
=
F_B(R(O))
=
\mathbb P(Y\in B\mid R(O)),
\]

which is the definition of conditional independence. ∎

## 4. Corollary 6.1 — exact posterior loses no Bayes decision information

For an action \(a\) and measurable loss \(L(a,Y)\), the Bayes action given
\(O\) can be written as a function of \(R(O)\). Thus, under Equation (6.1),
the exact posterior-valued representation is sufficient for downstream
decision-making.

## 5. Lemma 6.2 — posterior mean is not sufficient in general

Consider

\[
\Theta\mid O=a
\sim
\frac12\delta_{-1}
+
\frac12\delta_1,
\]

and

\[
\Theta\mid O=b
=
\delta_0.
\]

Both posterior means are zero. Let

\[
Y=\mathbf 1\{|\Theta|>1/2\}.
\]

Then

\[
\mathbb P(Y=1\mid O=a)=1,
\qquad
\mathbb P(Y=1\mid O=b)=0.
\]

The mean cannot distinguish the observations, while the posterior can. ∎

## 6. Relation to the four-block representation

The theorem is used for the source-supported state

\[
\Theta_d^{\mathrm{sup}}
=
(\Theta_c,\Theta_{p,d},\Theta_{m,d}).
\]

The ideal representation is

\[
R_d(O_d)
=
\operatorname{Law}
\left(
T_d\Theta_c,
\Theta_{p,d},
\Theta_{m,d}
\mid
O_d
\right).
\]

The shared and observed-private factors may become nearly deterministic under a
high-information observation. The recoverable-missing factor remains
non-degenerate when the current acquisition cannot identify it.

The global-null coordinate \(\Theta_0\) is excluded from the data-supported
object. Under the exact null condition of Proposition 13.6, the source
likelihood contains no information about it.

## 7. Failure boundaries

1. If the target depends directly on acquisition identity beyond \(\Theta\),
   Equation (6.1) fails.
2. An approximate Diffusion posterior is only approximately sufficient.
3. Finite posterior samples may omit rare modes.
4. Sufficiency does not imply physical identifiability.
5. A downstream model may be unable to consume a distribution-valued input.
6. Recoverable support elsewhere does not identify \(p(\Theta_m\mid O_d)\)
   without paired data or another coupling assumption.
7. The theorem does not convert a global-null prior into data evidence.

## 8. Experimental implication

Compare:

- posterior mean;
- mean plus variance;
- heteroscedastic Gaussian;
- mixture density;
- Monte Carlo posterior samples;
- oracle posterior in the known-pole system.

Include a task whose decision changes with posterior variance or multimodality.
If a Gaussian or mixture model matches Diffusion on CRPS, NLL and coverage,
Diffusion has no demonstrated necessity for that setting.
