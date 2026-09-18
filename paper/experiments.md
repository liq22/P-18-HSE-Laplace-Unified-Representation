# Five experiments for the source-supported posterior claim

## E1 — source-only cross-dataset industrial diagnosis

Use multiple accepted industrial source datasets and hold out one complete target dataset at a time. PHMFactory alone owns raw preparation, labels, source splits and grouping keys. A shared fault ontology, documented mechanical correspondence and deployment acquisition descriptors are prerequisites, not assumptions inferred from matching dataset names. Source labels are permitted; target labels are used only for final scoring. No target normalization, representation fitting, covariance threshold selection or checkpoint choice. Unsupported target classes require a separate open-set protocol, not a randomly initialized target classifier.

Split original recording/bearing/machine groups before constructing paired views. Pairings for posterior supervision are within the same source event/recording or declared simulator; unrelated source datasets are not class-sorted into paired samples. Compare the complete proposed model with observed-only HSE/direct diagnosis, strongest same-input single model and static prediction fusion. Report each target's recording-balanced pooled-confusion macro-F1 and balanced accuracy, then dataset-macro differences. Latent windows, training seeds and posterior draws are not independent datasets. Predeclare practical/equivalence margins and model-selection budgets. MFPT's existing six-parameter reference is data-path acceptance only and cannot alone support this experiment.

## E2 — the conditional generative mechanism

Fix the same source data, admitted target, observed condition and side inputs. Compare deterministic imputation, Gaussian posterior, finite mixture, ordinary latent diffusion and LLapDiff. The ordinary latent denoiser must match target coordinates, support restriction, network/update/sampling budgets as closely as feasible; report residual cost differences rather than calling equal token width equal computation. A generic masked conditional diffusion/SSSD-style temporal model and appropriate inverse-posterior formulation are direct mechanism references; FISHER/HSE remain industrial representation references.

Primary posterior score: joint Energy Score on held-out eligible targets. Report conditional/marginal coverage, sharpness, target error and coherent-sample diagnostics separately. Exact posterior KL and exact NLL are limited to known-law or tractable-density settings; approximate diffusion likelihood is not ranked against exact Gaussian likelihood without matching conventions. A deterministic point has a valid point/Dirac scoring interpretation but not a finite continuous-density NLL by default. Report diagnosis separately. A better posterior score without a diagnostic gain is a mechanism result, not a successful E1 claim.

## E3 — HSE and conditional-anchor attribution

Within the same eligible posterior process compare existing R, same-head raw H_A (`head_affine`), statistical H_M, full-q PCA/whitening/orthogonal coordinates and a matched nonlinear MLP conditioner. Use the same auxiliary-supervised source checkpoint when isolating the coordinate map; retain ordinary B1 without auxiliary supervision to isolate training effects. Transport regularization when claiming affine equivalence, and record dtype/bytes, rank, scale, factorization cost and all learned parameters.

In the known linear oracle compare full (b,J), compact (b,diag J) and declared blocks. Coarse versus full operator side-information regimes must be explicit and equal across methods. Full a=(A,R_noise) can restore J even when tokens omit it. Distinguish true conditional compression loss from a mismatched Gaussian plug-in. These are mechanism ablations within HSE–LLapDiff, not the paper's top-level objective.

## E4 — permitted inference versus unsupported output

Hold the source reference and posterior family fixed. Compare no support restriction, source support only, support plus conditional-identification restriction, and a reject-all missing baseline. Include all-missing generation, observed-branch update and source-global-null negative controls. Known simulators provide exact support and identifiable/nonidentifiable joint laws; real support labels require independently justified acquisition metadata/reference calibration.

Report (i) generated energy outside the admitted subspace, (ii) the fraction of unsupported coordinates emitted as recovered values, (iii) admitted target coverage, (iv) proper score on the common admitted target, and (v) whole-task diagnosis. The first two are structural compliance/unsupported-emission measures, not a general detector of factual hallucinations. Reject-all cannot win simply by deleting every difficult target; conditional scores require the same target set, and coverage/utility are always reported. Wrong or uncertain support maps are explicit failure cells.

## E5 — reversible acquisition change and irreversible loss

Use same-original-recording controls, formed after splitting: gain/known invertible sensor transforms, time grids, phase reference, bandwidth restriction and complete deletion of a task-relevant band. Separate fixed point count from fixed physical duration; anti-alias before downsampling. A finite-window damped sinusoid is not exactly band-limited, so measure filter response/leakage rather than assign physical nullity from the nominal Nyquist rate alone. Unknown sensor mixing, shifted machine dynamics and source–target conditional reversal are failure conditions, not mere nuisance metadata.

Measure source-common/target-missing role reassignment, posterior sensitivity, private-evidence drift, uncertainty and diagnosis. Ordinary latent versus Laplace dynamics comparisons use matched support/targets and include local modal residual or dynamics mismatch. Sparse excitation or spikes alone are not evidence for Laplace-distributed diffusion noise. Expected outcomes are not plotted; source/simulator controls can fail or produce no improvement.
