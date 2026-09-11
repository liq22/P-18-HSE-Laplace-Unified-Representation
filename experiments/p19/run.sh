#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
cd "$ROOT"
MODE=${1:-}
shift || true
case "$MODE" in
  theory)
    bash paper/run.sh theory
    ;;
  toy)
    python -m experiments.p19.toy_routing --output outputs/p19/toy_routing.csv
    ;;
  phm)
    : "${PHMFACTORY_ROOT:?set PHMFACTORY_ROOT after paper/goals/01_SYNC_PHMFACTORY.md acceptance}"
    : "${P19_PHM_CONFIG:?set P19_PHM_CONFIG to the accepted real-data config}"
    test -d "$PHMFACTORY_ROOT" || { echo "PHMFACTORY_ROOT not found" >&2; exit 2; }
    (cd "$PHMFACTORY_ROOT" && phmfactory preflight --config "$P19_PHM_CONFIG" && phmfactory --config "$P19_PHM_CONFIG")
    ;;
  external)
    echo "External benchmark training requires Goal 03 data and Goal 06 GPU execution. See paper/goals/06_LOCAL_GPU_8X4090.md." >&2
    exit 3
    ;;
  sota)
    echo "SOTA execution requires official checkouts/data and Goal 06 GPU execution; unavailable methods receive no fabricated score." >&2
    exit 3
    ;;
  ablation)
    echo "Learned ablations start only after the genuine M/B1-aux pilot; see paper/goals/04_EXPERIMENTS.md and 06_LOCAL_GPU_8X4090.md." >&2
    exit 3
    ;;
  statistics)
    python -m experiments.p19.statistics "$@"
    ;;
  plot)
    python -m experiments.p19.plot "$@"
    ;;
  *)
    echo "Usage: bash experiments/p19/run.sh theory|toy|phm|external|sota|ablation|statistics|plot [args]" >&2
    exit 2
    ;;
esac
