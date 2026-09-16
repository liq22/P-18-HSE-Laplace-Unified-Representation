# Method: compare representations, then compare complete policies

## 1. Target and consumer are part of the problem

For each task, declare its observation O, inference-available metadata a, target U (or reference latent Z0), grouping unit and evaluation law. Let F=E(O,a) be one frozen encoder. The general study uses at least two encoder families, initially HSE and a strong ordinary patch/Conv1D encoder, and at least two consumer families. A linear/small nonlinear classifier or regressor and the native LLapDiff provide different finite consumers; they are not scored on incompatible tasks in one table.

Compare message dimensions q under actual parameter/update/inference budgets. A gain at larger q or with extra pretraining is not attributed to statistical structure. Pretraining-data overlap and target access are reported for foundation-model baselines.

## 2. Inherited controlled message construction

The initial concrete instance is the companion TII's global readout. A shared trunk outputs R. One global head computes m(R),S(R) and receives the declared Gaussian conditional score. That score updates the same R path later consumed by B1-aux. Select one checkpoint on source validation, freeze the feature/preprocessing/trunk/head path, and pack M=T(R) as statistical prefix plus retained ordinary coordinates at the same q.

This construction is inherited, not independently new in TPAMI. Gaussian scoring targets moments conditional on the actual input and function class; it neither identifies the complete distribution nor assures target calibration. Input masks/time/side fields are explicitly consumed. Global output summaries have an explicitly all-valid output mask, not fictitious patch-local timestamp semantics. No duplicate unpriced statistical channel bypasses the message.

## 3. Representation utility profile

For a fixed trained consumer, record conditional evaluation risk rho(a;target,consumer,q,cost) for ordinary, statistically supervised ordinary, moment-only, and mixed messages. Estimate differences on identical original groups, targets and randomization. Under a common square target the nested-message decomposition attributes a possible gain to finite-model error reduction exceeding the information penalty. For other proper scores use their measured risk; do not relabel all differences as the squared projection term or mutual information.

The profile is a collection of well-defined comparisons, not a universal scalar ranking. Changing target or consumer can reverse the preferred message. A source target-defined projection must not be selected from the test task's labels. Statistical supervision and inference-side metadata are matched across arms.

## 4. Frozen policy family

Train and select components before policy calibration. Include:

- source-selected best single representation/consumer;
- a source-selected constant prediction mixture;
- a source-fitted acquisition-only hard selector over the same fixed arms;
- a separately declared soft-fusion policy only when trained as its own arm.

Point prediction fusion is a convex combination of points. Class fusion combines normalized probabilities. Distribution fusion is an actual mixture with a fixed total posterior-draw budget, not an average of unrelated generated trajectories. Charge all evaluated arms and gate costs. Hard-selection headroom says nothing by itself about beating static or soft fusion.

## 5. Independent certification where assumptions permit

Set aside original calibration groups not used to choose the policy family, target, model checkpoints, reference policy or loss. Evaluate all policies on those same groups. The bounded-loss routine takes one score per group and computes simultaneous paired lower bounds against the frozen reference. It selects a candidate only when the lower net-gain bound exceeds a declared practical margin; otherwise it returns the reference as an explicit statistical decision.

The proof is `theory/policy_certificate.md`. It is a classical finite-family specialization. Cost differences must be fixed utility penalties or separately justified bounds; measured latency is separately reported. An assumed shift allowance is not estimated from target-test labels. No certificate is claimed for raw Energy Score, unbounded Gaussian NLL, macro-F1, correlated rolling windows or arbitrary target shift. Those comparisons retain empirical intervals with their actual uncertainty unit.

## 6. Minimal implementation and stopping

Reuse `experiments/learned_conditioning/` for the concrete message and native two-arm pilot. `experiments/p19/` contains the fixed-policy simulator, paired statistics and new certificate, without PHMFactory imports. No second trainer/registry is created in this folder. Raw external converters and actual encoder checkpoints are named prerequisites; the native feature launcher does not implement them.

First complete one real ordinary-vs-statistical comparison with matched auxiliary supervision. Extend to multiple consumers/targets and static/dynamic policies only if scientifically informative, retaining adverse results. A generic risk-control corollary plus extra datasets is insufficient to establish a second paper beyond TII.
