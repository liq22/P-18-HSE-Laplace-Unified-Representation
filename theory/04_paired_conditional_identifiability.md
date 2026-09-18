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

The source observation design must identify the required joint conditional under the declared assumptions. Possible routes include:

- paired acquisition and reference latent data for the same `latent_event_id`, with an identifiable observation model;
- a known simulator or physical model that identifies the joint coupling;
- an identifiable corruption ensemble, as in Ambient Diffusion and related corrupted-data learning.

Pairing is not universally necessary. Class matching or distribution alignment alone does not establish the missing joint relationship. See the current TII Related Work for the corrupted-data predecessors.

Qualify the target together with the complete condition actually consumed. The stronger construction in `../paper/theory_main.md` uses source A observing (C,P) and source B observing (C,M): both observed pair laws can coincide across two worlds while p(M given C,P) differs. Shared C does not establish a conditional-independence separator. A common-view conditional cannot be silently extended with private evidence.

## Executable prediction

A finite witness must show source-compatible joint worlds with opposite required conditionals. The same-stem TII Notebook now verifies the overlapping-source construction; no duplicate experiment is needed here.

## Failure conditions

- Finite paired samples do not guarantee accurate conditional estimation.
- Pairing does not repair a non-injective observation map without further structure.
- Target-domain conditional mechanisms may shift; source pairing alone does not prove target transportability.
