# Theory 4 — Paired evidence and conditional identifiability

## Status

Proved as a non-identifiability counterexample for unpaired marginals and a standard conditional-existence statement for paired joint data.

## Theorem 4.1 — separate marginals do not identify a conditional

Knowing \(p(X)\) and \(p(Z)\) does not in general identify \(p(Z\mid X)\).

### Proof by construction

Let

\[
X\sim\operatorname{Bernoulli}(1/2),
\qquad
Z\sim\operatorname{Bernoulli}(1/2).
\]

Consider two joint worlds:

\[
P_+: Z=X,
\]

\[
P_-: Z=1-X.
\]

Both worlds have exactly the same marginals for \(X\) and \(Z\). However,

\[
P_+(Z=1\mid X=1)=1,
\]

while

\[
P_-(Z=1\mid X=1)=0.
\]

Therefore the conditional is not determined by the separate marginals. ∎

## Theorem 4.2 — paired joint law determines a regular conditional up to null sets

If \((X,Z)\) takes values in standard Borel spaces and its joint law is known, then a regular conditional distribution

\[
p(Z\in B\mid X=x)
\]

exists and is unique for \(p_X\)-almost every \(x\).

### Justification

This is the standard disintegration result for probability measures on standard Borel spaces. The joint measure determines the conditional kernel outside an \(X\)-null set.

## HSE–LLapDiff implication

Training a canonical posterior requires one of:

- paired acquisition and reference latent data for the same `latent_event_id`;
- a known simulator;
- a physical model that identifies the joint coupling.

Class matching or distribution alignment is not a substitute for event pairing.

## Executable prediction

A finite witness must show two data-generating worlds with identical unpaired marginals and opposite conditionals. A paired sample reveals which world generated the data.

## Failure conditions

- Finite paired samples do not guarantee accurate conditional estimation.
- Pairing does not repair a non-injective observation map without further structure.
- Target-domain conditional mechanisms may shift; source pairing alone does not prove target transportability.
