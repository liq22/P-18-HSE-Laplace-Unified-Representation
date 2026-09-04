# Theory 6 — Posterior-valued representation sufficiency

## Status

Proved under the latent Markov condition.

## Assumption

Let \(O\) denote an acquisition observation, \(\Theta\) the canonical latent state, and \(Y\) a downstream target. Assume

\[
Y\perp\!\!\!\perp O\mid\Theta.
\]

Define the representation

\[
R(O)=p(\Theta\mid O).
\]

## Lemma 6.1 — downstream posterior is a posterior functional

For every measurable target event \(B\),

\[
p(Y\in B\mid O)
=
\int p(Y\in B\mid\theta)R(O)(d\theta).
\]

### Proof

Apply the tower property to \(\mathbf1_{Y\in B}\), then use the conditional independence assumption to remove \(O\) from the inner conditional. ∎

## Theorem 6 — sufficiency

\[
\boxed{
Y\perp\!\!\!\perp O\mid R(O).
}
\]

### Proof

By Lemma 6.1, the conditional distribution of \(Y\) given \(O\) is a measurable functional of \(R(O)\). Therefore conditioning additionally on \(O\) after conditioning on \(R(O)\) does not change that distribution. ∎

## Lemma 6.2 — posterior mean is not sufficient in general

Consider

\[
\Theta\mid O=a
\sim\tfrac12\delta_{-1}+\tfrac12\delta_1,
\]

and

\[
\Theta\mid O=b=\delta_0.
\]

Both means are zero. For

\[
Y=\mathbf1\{|\Theta|>1/2\},
\]

we have

\[
p(Y=1\mid O=a)=1,
\qquad
p(Y=1\mid O=b)=0.
\]

Thus a mean-only embedding can discard task-relevant posterior structure. ∎

## HSE–LLapDiff implication

Posterior samples or an equivalent distributional representation are scientifically meaningful only when downstream decisions depend on uncertainty or multimodality. A Gaussian or finite mixture remains a required simpler baseline.

## Failure conditions

- If \(Y\) depends directly on acquisition identity beyond \(\Theta\), the Markov condition fails.
- An approximate diffusion posterior is only approximately sufficient.
- Finite Monte Carlo samples can miss rare posterior modes.
