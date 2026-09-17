# Candidate contribution and decisive comparisons

The candidate is a conditional-moment reparameterization whose value depends on target, finite consumer and explicit cost. The industrial message itself comes from the TII companion; extra datasets do not make an independent TPAMI contribution. A general claim requires method-specific findings beyond generic projection or routing identities and actual evidence across encoder/consumer families.

## What the current code implies

M=T(R) cannot contain new observation information. Its mean head is affine, so a mean-only message followed by an affine consumer cannot enlarge the original affine prediction family. Full covariance/Cholesky fields are nonlinear, but **nonlinear does not imply lossy**: for the complete message, the same-stem theory gives an explicit inverse when the head block on the replaced coordinates is nonsingular, under exact-arithmetic/diagonal-map conditions. Then the raw-message Bayes information penalty is zero. Rank deficiency, finite precision or restricted message variants require separate analysis; no unconditional lossless implementation is claimed.

Thus possible benefit must be tested against generic nonlinear coordinates, changed regularization, auxiliary supervision and conditioning of the computation. The actual selected checkpoint must report the replaced-block singular values and numerical inverse behavior in its working dtype before the ideal inverse interpretation is used. Classical invertible coupling work is acknowledged; this is not a new normalizing flow or Flow Matching branch.

| Contrast | Explanation tested | Current status |
|---|---|---|
| R→same frozen T→same consumer vs M | interface/packing rather than predictive advantage | implemented exact-identity test |
| complete-M inverse and singular-head collision | whether this concrete message actually loses raw-code information | conditional proof and actual float64 component tests |
| R vs full-q PCA/random orthogonal | pure rotation | actual CPU reference implemented |
| R vs whitening, isotropic and transported penalties | scale/regularization rather than information | actual CPU reference implemented |
| M vs mean-only/covariance field shuffles | which nonlinear statistical field matters | learned comparison pending |
| M vs same-supervision linear/small-MLP transformation | generic finite transformation | pending genuine R and matching training budget |
| direct task heads vs diffusion consumers | generator necessity | task-specific learned experiment pending |
| source-selected single vs static fusion, then optional hard policy | ensembling versus routing | finite controls exist; learned comparison pending |

The primary outcome is task-specific. Native diffusion loss or statistical diagnostics do not imply macro-F1 improvements. Conditional moments are not automatically a calibrated complete posterior. Unknown drift is a sensitivity parameter, not an observable deployment guarantee. The real external result currently validates one converter and an affine reference, not HSE superiority or all five domains. Equal/worse M outcomes complete the experiment and favor simplification.
