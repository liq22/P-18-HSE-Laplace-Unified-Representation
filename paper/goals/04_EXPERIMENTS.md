# Goal 04 — Experiment execution

## Scope

Run slices in order: theory/toy → genuine HSE native pilot → PHM → external benchmarks/SOTA → ablation. Each slice must answer one innovation or competing explanation.

## Deliverables

- executable/frozen config;
- actual command and numerical output;
- raw result CSV at independent-unit resolution;
- manuscript Results update and PROMOTE/HOLD/SIMPLIFY/STOP decision.

## Acceptance

1. Reference B1, best single, static fusion and dynamic route are all defined from the same information access.
2. Dynamic route is run as a headline only after positive routing headroom.
3. PHM uses recording/bearing/run-level splits.
4. At least five external benchmark families use task-compatible metrics.
5. No unavailable SOTA receives an invented value.

## Commands

```bash
bash experiments/p19/run.sh theory
bash experiments/p19/run.sh toy
bash experiments/p19/run.sh phm
bash experiments/p19/run.sh external
bash experiments/p19/run.sh sota
bash experiments/p19/run.sh ablation
```

The last four commands require accepted data/dependency configurations and normally reach the local-GPU Goal.

## Failure handling

Do not add modules to rescue a failed central comparison. M ≤ B1-aux → simplify. Static fusion matches route → remove route. Source routing reverses on unseen acquisition → report transportability failure. Gaussian/mixture matches Diffusion → do not claim Diffusion necessity.
