# Results — current evidence and empty slots that must remain empty

## R0. Remote native acceptance at current PR head

The current PR head before this TII-writing commit was `d8ea36fc8b3274dc007ccb40af6064f45fe87f14`. GitHub Actions run `34602707154` completed both `analytic-oracle` and `native-conditioner` jobs successfully. The native job installed the original `pixelhero98/LLapDiffusion` component at revision `0631e65cbac59d23822205573ebc7e180ecf0487` and executed the advertised `bash paper/run.sh native-acceptance` entry.

Actual native-component values from that run:

| Check | Value |
|---|---:|
| shared-gradient/export behavior tests | 14 passed |
| native loss comparison configurations | 24 |
| comparison rows | 96 |
| maximum absolute native/reconstructed loss difference | 2.3841857910e-7 |
| auxiliary gradient L1 reaching the ordinary trunk | 49.30367953 |
| ordinary-code maximum change after auxiliary step | 0.01159522310 |
| B1-aux prefix intervention effect | 0.00081458688 |
| B1-aux tail intervention effect | 0.00069965422 |
| M prefix intervention effect | 0.00071845204 |
| M tail intervention effect | 0.00056588650 |
| frozen conditioner changed by denoiser update | false |
| extra raw-summary bypass | false |
| genuine HSE/reference extraction executed | false |
| method advantage tested | false |

These numbers establish component consumption and loss consistency only. They are **not** a learned HSE–LLapDiff result, PHM result or evidence that M is better than B1-aux.

## R1. Existing finite theory witnesses

Retain the prior analytical records: actual-token collision/full-side-input control, conditional KL decomposition, denoising projection, same-moment non-Gaussian collision, Gaussian posterior parameterization controls and the source-supervised shared-code checks. They delimit possible mechanisms; none authorizes an industrial performance claim.

The new TII main-theory estimand is routing headroom. `experiments/p19/toy_routing.py` supplies only a finite algebraic witness. A positive toy headroom is not empirical evidence of acquisition routing in real data.

## R2. PHM main table — intentionally empty

Required rows: reference B1, B1-aux, M, source-selected best single, static fusion, dynamic acquisition route, plus compatible industrial baselines. Required columns include recording-macro macro-F1, worst-acquisition F1, reference-latent Energy Score, parameters, latency and memory.

**No values are inserted until the exact PHMFactory real-data protocol is accepted and executed.** Dummy smoke cannot fill this table.

## R3. External benchmark table — intentionally empty

Benchmark families and compatible metrics are defined in `experiments.md` and `experiments/DATA_DOWNLOAD_SOP.md`. Download links or successful parsing do not count as integrated benchmark results.

## R4. Ablation and routing table — intentionally empty

The routing row is admitted only after group-level source estimates show practical headroom. If the best single representation dominates, the correct result is `routing_not_justified` and the simpler method is retained.

## R5. Negative-result policy

A result may change the final paper identity:

- M ≤ B1-aux at comparable cost → simplify to the ordinary supervised code;
- static fusion matches dynamic routing → remove the router;
- dynamic source gain reverses on unseen acquisition → report transportability failure;
- Gaussian/mixture probability head matches Diffusion → do not claim Diffusion necessity;
- PHM gains disappear under recording-level splits → reject the window-level claim.

No failed central hypothesis is repaired by adding a new model or changing the test set after seeing results.
