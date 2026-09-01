---
name: 01-project-brief
description: "Establish or revise the minimum research state needed for the next scientific action: problem boundary, strongest evidence, failure, mechanism, claims, missing experiment, scope, and consequential author decisions."
---

# 01 Project Brief

## Purpose

Create a concise scientific state that makes the next research action obvious.
Initialization is not a metadata-completion or approval workflow.

## Workflow

1. Define the problem as:

   ```text
   Object
   Environment
   Observation
   Task or decision
   Failure or unresolved contradiction
   Desired understanding
   ```

2. Establish the current research state:

   ```text
   Research question
   Current strongest result
   Strongest evidence
   Main failure
   Plausible mechanism
   Strongest competing explanation
   Unverified claim
   Highest-value missing experiment
   Potential contribution
   ```

3. Resolve only contradictions that would change the method, experiment,
   interpretation, or manuscript scope.
4. Update the relevant fields in `project.yaml`, `paper/paper.yaml`, or the intake
   file. Leave unknowns as `TODO` or `unknown`.
5. Record an author decision only when the author actually made one and the
   decision affects direction, formal source transition, or submission.
6. Read the resulting state once for scientific consistency and stop.

## Output Contract

Produce a usable project state with:

- one bounded research question;
- observed failure or unresolved contradiction;
- favored and competing explanations;
- concise hypotheses/claims and their current support type;
- the smallest required experiment or analysis;
- in-scope/out-of-scope boundary;
- one next substantive action.

## Boundaries

- Do not require the title, venue, complete author metadata, all claims, or all
  compliance fields before research can begin.
- Do not create extra status reports, dashboards, ledgers, approval packages, or
  blocker documents.
- Do not turn early hypotheses into approved claims because the template is
  complete.
- Do not polish titles or metadata while the problem, failure, and mechanism are
  unclear.
- Do not run Python for ordinary YAML or prose inspection unless the schema or
  validator itself changed.
- Do not require hashes, receipts, independent-review records, or machine proof of
  human decisions.
