# HSE–Laplace Source-Supported Partial Unified Representation

## Working title

**Observability- and Identifiability-Gated Partial Modal Representation for Cross-Acquisition Time Series**

## Problem

Different acquisition operators expose partially overlapping physical modal support. Complete domain invariance can erase task-relevant information available only in a higher-support view, while an unconstrained generator can present prior-driven samples as recovered evidence.

## Representation

\[
\mathcal H
=\mathcal H_c\oplus\mathcal H_{p,d}\oplus\mathcal H_{m,d}\oplus\mathcal H_0.
\]

| Role | Meaning | Permitted operation |
|---|---|---|
| \(\mathcal H_c\) | observable in every declared source domain | anchored canonicalization |
| \(\mathcal H_{p,d}\) | observed now, but not common to every domain | exact preservation |
| \(\mathcal H_{m,d}\) | hidden now, supported by another source | conditional inference only when identified |
| \(\mathcal H_0\) | unsupported by every source | no data-driven recovery claim |

The candidate factorization is

\[
C^*=T_d(C),\qquad P'=P,\qquad
M'\sim q_\theta(M\mid C^*,P,\mathcal O_d,\chi_d).
\]

Flow and Diffusion are not assumed to be necessary. Their inclusion is decided later against affine/OT and Gaussian/mixture alternatives.

## Theory-to-contribution admission rule

A theorem is not listed as a paper contribution merely because it appears in `theory/`.

It must pass all five gates:

1. **Formal completeness:** its Markdown contains explicit assumptions, statement, derivation, and failure boundary.
2. **Executable witness:** the same-stem Notebook passes in a clean kernel.
3. **Mechanism relevance:** the Notebook exercises the central finite implication, not a superficial formula.
4. **Novelty role:** the result is specific to the proposed representation rather than established probability-flow, stability, or decision-theory background.
5. **Empirical prediction:** the result yields a measurable prediction for the known-pole experiment.

Notebook success means only that a finite witness is internally consistent. It does not validate the theorem generally and does not establish empirical usefulness.

## Admitted theoretical contribution candidates

### C1 — Source-supported role decomposition

The four-way decomposition separates common observable, observed-private, source-supported missing, and source-global-null modal coordinates. Its paired Notebook checks the direct sum, empty-block behavior, and global-null separation.

### C2 — Cost of complete invariance

When private information has conditional task value, complete paired invariance has a non-zero Bayes log-risk lower bound. The Notebook realizes the equality case and the task-irrelevant control.

### C3 — Identifiability gate for missing inference

Visibility in another source domain does not identify the current-domain conditional. The Notebook constructs two worlds with equal unpaired marginals and opposite missing conditionals, then shows what pairing resolves.

### C4 — Triangular partial stochastic representation with paired risk control

Anchored shared canonicalization, private identity, and a shared-conditioned missing posterior form one triangular kernel. The paired-risk result controls downstream change only under a same-event coupling. The paired Notebooks check conditional benefit, private invariance, and the semantic-reversal counterexample.

## Results that are not headline contributions

The following remain supporting theory, established background, special cases, null models, or complexity gates even when their Notebooks pass:

- diffusion–flow marginal equivalence;
- posterior sufficiency;
- local modal stability;
- product-case private-preserving OT;
- generator commutation;
- sampling-gap and projector perturbation bounds;
- Diffusion proper-score gate;
- affine Flow gate;
- window-local Laplace adequacy gate.

## Evidence state

```text
formal derivations: present under explicit assumptions
executable finite witnesses: 25 / 25 locally; CI is authoritative
known-pole mechanism evidence: not started
learned Diffusion/Flow evidence: not started
real PHM evidence: not started
formal_claim_supported: false
```

The next scientific step remains the known-pole role, identifiability, and complexity-gate experiment. No new theorem is promoted to an empirical contribution before that experiment.
