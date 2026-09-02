# Theorem 16 — Source support is not conditional identifiability

## Status

**Necessary-condition theorem, non-identifiability counterexample, and a
population sufficient condition under paired events.**

## Purpose

A modal coordinate can be hidden in the current domain and observable in another
source domain. This makes it source-supported, but it does not by itself
identify the conditional law needed to infer that coordinate for the current
sample.

For this reason, \(\mathcal H_{m,d}\) should be read as
**source-supported missing**, not as an automatic guarantee of recovery.

## 1. Setup

Let \(C\) denote observed common information and \(M\) a modal coordinate hidden
in domain \(d\) but observed in another source domain. The desired object is

\[
p(M\mid C,P,\mathcal O_d).
\]

Define a recoverability certificate

\[
\chi_{d,k}\in\{0,1\}
\]

for slot \(k\). The certificate is one only when the experiment supplies a
declared mechanism that identifies the relevant conditional, such as paired
latent events, a known simulator, or an injective physical coupling model.

## 2. Lemma 16.1 — source support is necessary for source-likelihood learning

If no source acquisition has non-zero sensitivity to modal direction \(u_k\),
then that direction belongs to the source-global-null block and cannot receive
direct likelihood information. Therefore source support is necessary before a
data-supported missing posterior can be claimed.

The stronger global-null statement is proved in Theory 17.

## 3. Theorem 16.1 — unpaired marginals do not identify a missing conditional

### Statement

Knowing the marginal laws of \(C\) and \(M\) from separate unpaired source
datasets does not identify \(p(M\mid C)\).

### Construction and detailed proof

Let \(C,M\in\{0,1\}\). Consider two joint laws.

Under model \(P_+\),

\[
P_+(C=0,M=0)=P_+(C=1,M=1)=\frac12.
\]

Thus

\[
M=C
\quad\text{almost surely}.
\]

Under model \(P_-\),

\[
P_-(C=0,M=1)=P_-(C=1,M=0)=\frac12.
\]

Thus

\[
M=1-C
\quad\text{almost surely}.
\]

Both models have the same marginals:

\[
C\sim\mathrm{Bernoulli}(1/2),
\qquad
M\sim\mathrm{Bernoulli}(1/2).
\]

Hence any unpaired dataset that observes only \(C\) in one source and only
\(M\) in another has the same population distribution under \(P_+\) and
\(P_-\). Nevertheless,

\[
P_+(M=1\mid C=1)=1,
\]

whereas

\[
P_-(M=1\mid C=1)=0.
\]

Therefore the missing conditional is not identified by unpaired marginals. ∎

## 4. Theorem 16.2 — paired population data identify the conditional law

Assume paired latent events provide draws from the joint law
\(P_{C,P,M}\) on standard Borel spaces. Then a regular conditional law

\[
P(M\in\cdot\mid C,P)
\]

is identified \(P_{C,P}\)-almost surely by the joint distribution.

### Proof

The joint distribution determines all integrals

\[
P(M\in B,(C,P)\in A)
\]

for measurable \(A,B\). By disintegration on standard Borel spaces, there is a
regular conditional kernel \(K(B\mid c,p)\), unique
\(P_{C,P}\)-almost surely, satisfying

\[
P(M\in B,(C,P)\in A)
=
\int_A K(B\mid c,p)\,P_{C,P}(dc,dp).
\]

Thus the population joint law identifies the conditional kernel up to the usual
null-set ambiguity. ∎

## 5. Observation-operator condition

Paired raw observations identify the latent joint only if their acquisition
operators or encoders recover the relevant coordinates up to the declared
equivalence. Pairing alone does not repair a non-injective observation map.

A practical certificate therefore requires:

```text
source support
+ paired or physically anchored correspondence
+ identifiable observation map on the target modal slots
+ train/test separation by latent event
```

## 6. Consequence for the representation

The representation may attach a learned posterior to slot \(k\in\mathcal
H_{m,d}\) only when \(\chi_{d,k}=1\). If \(\chi_{d,k}=0\), the output must say
one of:

```text
unidentified
partially identified
prior-driven
unsupported by the declared coupling
```

It must not call the result a recovered physical mode.

## 7. Failure boundaries

1. Finite paired samples do not guarantee accurate estimation.
2. Pairing errors destroy the joint law.
3. Conditional shift between source and target can invalidate the learned
   kernel.
4. A simulator identifies only its own data-generating assumptions.
5. A semantic label is not necessarily an injective modal anchor.

## 8. Experimental implication

Include two datasets with identical unpaired marginals but opposite
\(p(M\mid C)\). An unpaired method should fail to distinguish them. A paired
method may succeed. The independent unit must be the latent event, not an
acquisition view.
