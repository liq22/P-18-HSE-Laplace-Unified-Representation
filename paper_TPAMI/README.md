# General representation study — TPAMI candidate

Read [scope](../PAPER_SCOPE.md), [manuscript](main.md), [Method](method.md), [actual results](results.md) and [the sole task index](goals/README.md). TII `paper/` remains industrial-only.

The immediate question is whether a conditional-moment message has an advantage beyond equally supervised ordinary code and simple coordinate/learned transformations. General projection and routing theory are supporting background; a mean-only affine head does not enlarge an affine consumer family. More datasets alone do not establish a second independent paper.

```bash
bash paper_TPAMI/run.sh setup
bash paper_TPAMI/run.sh theory
# First actual external reference; official download command is in the SOP.
bash paper_TPAMI/run.sh vowels-reference --archive /absolute/vowels.zip --output-dir outputs/tpami/vowels-reference-01
bash paper_TPAMI/run.sh reference-plot --csv outputs/tpami/vowels-reference-01/affine_summary.csv --output-dir outputs/tpami/vowels-reference-01/figures
```

Japanese Vowels now has real native-length conversion, source-fitted same-dimensional affine controls, saved/restored coefficients and prediction metrics. The features are mean LPC, not HSE. Four other raw converters and genuine learned feature/reference checkpoints remain pending. The existing `all-cpu` command only executes mathematical studies and their figures; it does not claim all external benchmarks are integrated.

Reuse the shared code and bibliography, not copied trainers. First genuine local neural pilot uses one of8×4090; two-GPU training is forbidden. The existing local GPU goal names actual dependencies rather than substituting synthetic inputs.
