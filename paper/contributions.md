# Contribution–mechanism–evidence map (author material)

The main question is source-supported latent posterior inference for unseen industrial datasets. Conditional-moment coordinates are a conditioner ablation. LLapDiff is the proposed core generative mechanism; its necessity remains testable rather than assumed.

| Contribution | Literature-derived gap | New element proposed here | Figure | Method / estimand / experiment | Current evidence |
|---|---|---|---|---|---|
| C1: source-referenced partially observable formulation | Shared/private features, measurement-null generation and corrupted-data identification are established separately; source union alone does not determine which industrial conditional is identified. | Four source-relative roles plus an explicit source-identified missing target, with a target-common-support correction. | A–B | Method 1–2; support assignment, eligible coverage and known-joint conditional error; E4–E5. | Finite subspace and nonidentifiability witnesses. No physical source reference established on multiple real datasets. |
| C2: support-restricted HSE–LLapDiff design | Existing masked diffusion does not by itself validate a mask on arbitrary learned physical coordinates or its source evidence. | Acquisition-aware HSE/statistical anchor, a source-justified eligible latent subspace, and stable Laplace temporal prediction restricted to that target while retaining observed evidence. | B–C | Method 3–4; projected-update leakage, posterior Energy Score and generator cost; E2–E4. | Projection theorem and finite update witness; actual source-restricted native implementation pending. |
| C3: posterior-to-diagnosis attribution | Better posterior or denoising scores do not imply cross-dataset diagnostic benefit; ordinary nonlinear coordinates and extra supervision can confound the claim. | A joint evidence chain with fixed-condition generator contrasts, fixed-generator conditioner contrasts and untouched target-dataset diagnosis. | D | Method 5; per-target group-balanced macro-F1, same-target posterior score and cost; E1–E3. | Existing coordinate/native component controls remain valid; no learned LODO method result yet. |

## Claim language

Use “we formulate”, “we specify/propose” and “we derive” for the actual formulation, proposed mechanism and proved scope properties. Do not write that the support-restricted LLapDiff was implemented/trained or that industrial diagnosis improved before it occurs. General subspace algebra, KL decomposition, Bayes denoising projection and prior-mediated null inference are attributed supporting theory, not independently new principles.

The current three contribution statements are therefore not three verified empirical findings. A paper-level method contribution requires C2's actual native mechanism and C3's new industrial evidence. If Gaussian/mixture or ordinary diffusion matches it, report that result and narrow the LLapDiff claim. If only the conditioner improves, retain the coordinate result as a component finding rather than pretending it demonstrates the full posterior program.

## Changes accepted from the supplied comments

Promote cross-dataset posterior inference above coordinate attribution. Keep four observational roles and conditional identifiability distinct. Retain the same-head controls. Correct Laplace-noise motivation to Laplace-domain modal dynamics; separate dataset family from same-event pairing; qualify arbitrary learned-coordinate support; retain the correlated-prior null counterexample. Explicitly test reject-all rather than using zero unsupported emissions as sufficient success.
