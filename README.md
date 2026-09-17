# HSE–Laplace research

Two manuscript workspaces share one implementation:

| Workspace | Scope | Entry |
|---|---|---|
| `paper/` | IEEE TII: industrial data only through PHMFactory | [Manuscript](paper/main.md), [goals](paper/goals/README.md) |
| `paper_TPAMI/` | IEEE TPAMI candidate: representation specificity and five external domains | [Manuscript](paper_TPAMI/main.md), [goals](paper_TPAMI/goals/README.md) |

Read [PAPER_SCOPE.md](PAPER_SCOPE.md) for claim/result ownership. Shared analytical results are not counted twice; adding datasets alone does not create independent novelty.

```bash
python -m pip install -e '.[notebooks,experiments]'
bash experiments/p19/run.sh theory
bash paper_TPAMI/run.sh all-cpu
```

The TPAMI workspace now also runs an actual official Japanese Vowels converter and affine CPU reference via `vowels-reference`; its data SOP supplies the download. This is not an HSE or conditional-moment model result. Four other raw converters and the genuine learned multi-domain comparisons remain pending.

PHMFactory is the sole PHM reader/label/split source. The accepted current-main dependency and real MFPT checkpoint/metric acceptance are unchanged. The Gaussian input and common-recording-seed corrections are applied before numerical evaluation. No paper module changes PHMFactory core.

`src/`, `theory/` and `experiments/` remain shared; historical `experiments/p19/` is not a third paper. Each manuscript has one goal index, protocol and Results location; no new parallel status framework. Real CSV plotters export SVG/PDF/PNG without expected curves. First local learned pilot uses one of8×4090; two-GPU training is prohibited. Master and existing branches are preserved.
