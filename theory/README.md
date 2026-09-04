# Theory map

Each numbered Markdown file states one assumption set, result, proof, measurable prediction, and failure condition. Each has one output-free Notebook witness. A witness checks a finite implication; it does not replace the proof or establish empirical usefulness.

| ID | Formal result | Paper role |
|---:|---|---|
| 00 | problem and assumptions | definitions |
| 01 | fixed-dimensional acquisition sufficiency | core analytic foundation |
| 02 | closed-form canonical posterior | strongest simple baseline |
| 03 | acquisition-information monotonicity | core calibration prediction |
| 04 | paired conditional identifiability | core protocol requirement |
| 05 | complete-invariance information loss | core motivation |
| 06 | posterior representation sufficiency | supporting decision-theory result |
| 07 | stable Laplace modal dynamics | inherited supporting property |
| 08 | sampling-gap shift bound | supporting irregular-time result |

## Validity boundary

Theorems 1–3 are exact only for known linear-Gaussian acquisition. Theorems 4–6 are general probability statements under their declared pairing and Markov assumptions. Theorems 7–8 are supporting modal and gap results. None proves that a learned HSE recovers the oracle statistics or that LLapDiff is empirically necessary.

## Execution

```bash
python theory/run_notebooks.py --timeout 180
```

Source Notebooks remain unexecuted and contain no stored outputs.
