# Goal01 — scope and dependency synchronization

**Scope:** create the independent general workspace while retaining industrial TII data/claims in `paper/`. Use current dev, not an old overlay. **Products:** PAPER_SCOPE.md, separate manuscript entries, moved general proof/CSV, updated links and unchanged shared implementation.

```bash
git status --short
git fetch origin
git log -1 --oneline origin/dev
git submodule update --init external/phmfactory
git -C external/phmfactory fetch origin main
git -C external/phmfactory log -1 --oneline origin/main
```

**Acceptance:** current dependency remains a0db97364e6d38a927c3ea30c643ebbb821d54d7, already matching upstream main and real MFPT acceptance. No fictitious fast-forward. A future new main must pass Goal01 in `../../paper/goals/01_SYNC_PHMFACTORY.md` before the parent pointer changes. General and TII Results do not duplicate a new claim/table as independently obtained.

**Failure:** dirty/conflicting branches or changed upstream are inspected, not reset/stashed/force-pushed. Failed upstream acceptance retains the previous pointer. Master and others' branches stay unchanged.
