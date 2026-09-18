# Motivation figure: source-supported posterior inference

```bash
python paper/figures/motivation.py --output-dir paper/figures
```

The sole drawing source is `motivation.py`. SVG has real text, semantic object IDs and independent rectangles/paths; no bitmap embedding. PDF and PNG are regenerated locally or by the manuscript workflow, not required as redundant tracked binaries. Output is 180×138 mm, with a 4252×3260 PNG (approximately 600 dpi). The diagram is a proposed scientific mechanism, not empirical evidence.

| Panel/object | Scientific meaning | Text/experiment mapping |
|---|---|---|
| A source support matrix | illustrative aligned reference; source supports need not cover every coordinate | Intro paragraphs 1–4; Method 1–2; E4/E5 |
| B eligibility intersection | current missing + source-supported + conditionally identified | Intro gap/challenge 2; G_e in theory; E4 |
| C HSE and LLapDiff | condition encoder and restricted latent generative mechanism | Method 3–4; E2/E3 |
| C observed path | retain measured evidence/uncertainty, not hard-clamp noisy latent truth | Method 4; private-drift diagnostic |
| C grey exclusion | neither global-null nor unidentified missing output is reported as recovered | Proposition 3/4; emission and coverage checks |
| C amber note | Laplace-domain dynamics differs from Laplace noise; latent support requires alignment | Closest-work boundary; ordinary latent diffusion control |
| D measurement cards | posterior, diagnosis, support compliance and cost are separate | E1–E5 and contribution map |

The displayed source rows do not assert that different datasets contain matching events. The current-view role illustration is an ideal coordinate-separable example, not a calibration of any real sensor. The body caption explains its ambiguity and why eligibility precedes generation. The retained implementation currently provides condition-coordinate ablations; this figure does not claim a native source-support-restricted model has already been trained.
