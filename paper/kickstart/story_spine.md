# Story Spine

The Story Spine is the paper's shortest scientific argument. It is optional and
should remain shorter than the manuscript section it helps organize.

> 中文说明：先把真实问题、已有能力、failure、科学问题、机制、证据、边界和意义连成一条线。只有承载核心事实或 claim 的位置需要来源/结果指针，不要求每一句话都绑定内部 ID。

## Research state before narrative

```text
Research question:
Observed failure or unresolved contradiction:
Favored mechanism:
Strongest competing explanation:
Current strongest evidence:
Unverified claim:
Highest-value missing experiment:
```

If these items are unresolved, return to research rather than filling the
Introduction with generic prose.

## One-page red thread

| Move | One-sentence content | Scientific basis | Status |
|---|---|---|---|
| Real problem | TODO | verified source / observed need | TODO |
| Current capability | TODO | representative literature | TODO |
| Concrete failure or contradiction | TODO | source / baseline result | TODO |
| Scientific question | TODO | author synthesis | TODO |
| Key mechanism-level idea | TODO | hypothesis / theory | hypothesis |
| Minimal method or intervention | TODO | method/code | planned |
| Decisive evidence | TODO | actual run/analysis | TODO |
| Boundary and alternative explanation | TODO | stress/null/negative result | TODO |
| New understanding | TODO | bounded claim | TODO |

A gap cannot be only “few papers exist.” A method cannot be only a module list. A
main result cannot be written as successful before the actual result exists.

## Central claim

Prefer one central claim and only the supporting claims the paper needs:

```text
Central claim:
Support type: theory-supported / experiment-supported /
              literature-supported / hypothesis-only
Object/environment/task boundary:
Failure condition:
Evidence that would weaken or reject it:
```

Do not create C2/C3 or contribution rows merely to complete a template.

## Section jobs

| Section | Main intellectual job | Avoid |
|---|---|---|
| Abstract | Problem -> gap -> idea -> evidence -> implication | unsupported headline claim |
| Introduction | Define the real problem and specific unresolved question | generic AI background or novelty inflation |
| Related Work | Compare assumptions, mechanisms, failures, and boundaries | paper-by-paper listing |
| Method | Explain assumptions, changed object, mechanism, formulation, algorithm | software architecture that is not the research object |
| Experiments | Define fair comparisons, independent unit, metrics, and boundary tests | protocol detail unrelated to claims |
| Results | Observation -> quantitative evidence -> interpretation | table-by-table victory narration |
| Discussion | Why/when it works, alternatives, failures, literature, implication | repeating Results or hiding null results |
| Limitations | Method/data/experiment/theory/scope limits | generic “more datasets in future” |
| Conclusion | State the bounded knowledge gained | new evidence or universal claims |

## Abstract spine

Write this only after the evidence and claim are stable:

```text
Problem
-> specific gap/failure
-> core mechanism-level idea
-> minimal method/theory
-> main actual evidence
-> scientific implication and boundary
```

## Reader path

A reader should recover the same central claim and boundary from the title,
abstract, Introduction conclusion, key figure/table captions, main Results
finding, Discussion, and Conclusion. Use this as a consistency check, not a
mandatory seven-item drafting order.
