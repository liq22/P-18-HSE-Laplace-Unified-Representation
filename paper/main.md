# HSE–LapDiff

## Working title

**Acquisition-Information Conditioning for Probabilistic Cross-Acquisition Representation**

## Problem and exact gap

The same local event can produce different information under different sampling rates, timestamps, masks and sensor responses. A fixed embedding interface does not establish that a conditional generator receives the same physical evidence or should return the same uncertainty.

HSE supplies heterogeneous-signal tokenization. LLapDiff supplies stable modal prediction in a latent-trajectory diffusion model. Neither component is claimed here as new. The remaining question is whether an actual finite-budget HSE condition retains the cross-modal acquisition information required by that fixed generator.

Statistical compression and approximate sufficient-representation theory already connect compressed conditions to conditional generation; see Alsing and Wandelt and Oko et al. in `related_work.md`. Our candidate difference must be a concrete, budgeted acquisition-information mechanism and its measurable effect, not a new name for those identities.

## Three objects, one controlled comparison

The analytical target is a known-pole coefficient vector `beta` with `s(t)=Phi_Lambda(t) beta`. Under known linear-Gaussian acquisition,

\[
x=A\beta+\epsilon,\quad b=A^TR^{-1}x,\quad J=A^TR^{-1}A.
\]

The learned target is instead `Z0=E_ref(X_ref)` from a source-trained frozen reference encoder. Its coordinates are not automatically the physical coefficients. LLapDiff's predicted modal parameters are a third object, not an assumed ground-truth physical state.

The actual condition is

\[
H=T_\psi(O,a),\qquad C=(H,a).
\]

`O` includes all current-acquisition information visible to the conditioner encoder; `a` includes only the side input actually consumed by the generator. Teacher and student see the same underlying acquisition. A reference target is supervision, not extra input granted only to the teacher.

## Analysis that guides the candidate method

Theory 1 preserves the complete `(b,J)` sufficiency result. It also gives a collision through the existing diagonal tokenizer, with a positive control showing that full acquisition side information can reconstruct `J`. Therefore a missing matrix entry inside `tokens` is not by itself proof of complete-condition information loss.

Theory 9 separates

\[
\mathbb E\operatorname{KL}(p(Z_0\mid O,a)\|q_\phi(Z_0\mid H,a))
=I(Z_0;O\mid H,a)
+\mathbb E\operatorname{KL}(p(Z_0\mid H,a)\|q_\phi(Z_0\mid H,a)).
\]

Theory 10 separates full-information Bayes error, the conditioning projection gap, and denoiser approximation error. The same result is converted explicitly between epsilon, x0 and v under a fixed schedule. These are established analytical tools applied to our interface, not standalone novelty claims.

## Coefficient-space falsification and candidate method

Theory 11 computes the true compressed conditional by mixing compatible acquisition designs with their posterior probabilities. In Task B, a Gaussian prior can therefore yield a non-Gaussian compressed posterior. Replacing J by its diagonal is a different, approximate probability model.

The 6,144-event coefficient-space experiment supports a limited conclusion: within-mode blocks reduce information loss relative to diagonal summaries when the decoder lacks the distinguishing operator information. They are exactly sufficient in the no-cross-coupling control, but not when cross-mode coupling is hidden. Full operator side input removes the information gap in all arms. Scalar budgets are 8/10/14, so this is not a same-budget method win.

Compare the original HSE against the smallest coupling feature supported by an actual sampled-window follow-up, initially a declared within-mode cosine/sine information block. Preserve the original patch/token budget and the LLapDiff target VAE, denoiser, training schedule and sampler. Report the real scalar storage and computation: a full `(b,J)` oracle is not a same-budget deployed baseline.

Do not assume that `2x2` blocks suffice when cross-mode coupling is strong. If actual side information already recovers all of `J`, study genuine patch/compression or finite-capacity loss rather than hiding metadata to manufacture an advantage.

## Contribution admission

No new learned-method contribution is admitted yet. Candidates are:

1. a concrete acquisition-coupling condition that improves the same LLapDiff at declared equal information and budget;
2. analysis of that specific condition's posterior and denoising loss, using rather than reclaiming generic KL/projection theory;
3. paired evidence that separates compression, fitting, correlated noise and reference-target uncertainty, including negative results.

The finite witnesses and coefficient-space Monte Carlo experiment in `results.md` support only their stated constructions. They do not show learned sufficiency, calibration, superiority over mixtures, or PHM generalization.

## Future work

Flow Matching remains outside the active method. Consider sampler acceleration only after learned posterior validity is established and sampling latency is a measured bottleneck.
