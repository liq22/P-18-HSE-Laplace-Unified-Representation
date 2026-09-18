# TII execution entry

The paper studies source-supported partial posterior inference for source-only cross-dataset industrial diagnosis. Chapter 2 defines the problem; Chapter 3 specifies source-target construction, HSE conditioning, velocity training, the restricted reverse update and coherent diagnostic integration.

```bash
bash paper/build_frontmatter.sh outputs/tii_support
```

This builds Chapters 1–3 and two editable diagrams, executes the original support examples and the new method-equation witnesses. These are analytical/model-interface checks, not new industrial performance results.

## Next substantive implementation

Use the accepted PHMFactory data/split path and actual source reference. Form same-original-recording target/view tuples only after splitting. Validate the common coordinates and acquisition map; identify the joint target under the complete observed condition. A feature reference remains a feature target unless its physical meaning is established. Record source pairing and conditional-transport assumptions separately.

Connect Method Eqs.9–12 to the original native LLapDiff path: velocity target, same time distribution and normalization, basis-projected forward noise, converted predictions and every reverse update. Do not mask a differently trained posterior and call it the new method. Keep the observed-state readout and source-trained diagnostic head fixed for primary mechanism contrasts; each observed draw stays fixed through its conditional reverse trajectory. The old native pilot remains an E3 component control until this actual path exists.

Then execute the E2 family/factorial comparison and E1 LODO on original groups. Use the same admitted targets and side inputs; no clean complementary targets are supplied to the unrestricted control. Report posterior scores only where reference targets exist, separately from diagnosis, admitted coverage and cost. Simple posteriors/direct classifiers matching LLapDiff are decisive findings, not failed execution.

Reuse existing goals for data/sync/GPU commands. First learned pilot uses one of 8×4090; no two-GPU workaround. Preserve master, other branches, prior negative results, TPAMI and PHMFactory core/gitlink. Merge only tested scientific changes into dev.
