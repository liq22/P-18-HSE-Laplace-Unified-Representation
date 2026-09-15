# Goal 01 — synchronize and qualify the dependency

## Scope

Read the parent branch/PR and upstream `main` before editing. The initially reviewed parent had no PHMFactory gitlink, so recording the accepted revision is an **initial submodule addition**, not a claimed fast-forward of an existing pointer. Preserve other branches and master.

## Products

`external/phmfactory` at the exact accepted revision, `.gitmodules`, the public acceptance command, numerical reference CSV and dependency scope in Results. No upstream core patch.

## Commands

```bash
git status --short
git fetch origin
git submodule update --init external/phmfactory
git -C external/phmfactory status --short
git -C external/phmfactory fetch origin main
git -C external/phmfactory log -1 --oneline origin/main
# For a later update, require the current pointer to be an ancestor of origin/main.
git -C external/phmfactory merge-base --is-ancestor HEAD origin/main
# In an isolated installed PHMFactory environment:
phmfactory doctor
phmfactory preflight --config smoke
phmfactory demo
bash experiments/p19/run.sh phm-prepare --output /absolute/data/mfpt
bash experiments/p19/run.sh phm --data /absolute/data/mfpt --output /absolute/runs/mfpt-check
```

Do not advance a later pointer before rerunning acceptance at that candidate revision. Run in a temporary/detached candidate checkout if the current parent pointer must remain unchanged during testing.

## Acceptance

Current accepted revision is `a0db97364e6d38a927c3ea30c643ebbb821d54d7`. Run 34765060233 restored three selected checkpoints and independently matched accuracy/F1 within 1e-6; 20 files and disjoint 10/4/6 train/val/test groups were checked. This qualifies only the exact MFPT reference path, not all upstream releases/configurations.

## Failure handling

Dirty worktree or non-descendant upstream: stop synchronization, keep the changes, do not reset/stash/force. Config/reader/split/checkpoint/metric failure: keep the existing pointer and report the actual failing command. A docs-only upstream change still receives the acceptance run before a new pointer is published.
