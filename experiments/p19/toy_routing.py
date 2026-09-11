"""Finite witnesses for routing-headroom definitions; not PHM evidence."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def headroom(rows):
    conditions = sorted({r["condition"] for r in rows})
    arms = sorted({r["arm"] for r in rows})
    by = {(r["condition"], r["arm"]): r["risk"] for r in rows}
    global_risks = {arm: sum(by[(c, arm)] for c in conditions) / len(conditions) for arm in arms}
    best_global = min(global_risks.values())
    oracle = sum(min(by[(c, arm)] for arm in arms) for c in conditions) / len(conditions)
    return best_global - oracle


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="outputs/p19/toy_routing.csv")
    args = p.parse_args()
    scenarios = {
        "no_headroom": [
            {"condition": "low_missing", "arm": "R", "risk": 0.20, "estimate": 0.205},
            {"condition": "low_missing", "arm": "M", "risk": 0.25, "estimate": 0.245},
            {"condition": "high_missing", "arm": "R", "risk": 0.30, "estimate": 0.304},
            {"condition": "high_missing", "arm": "M", "risk": 0.35, "estimate": 0.346},
        ],
        "positive_headroom": [
            {"condition": "low_missing", "arm": "R", "risk": 0.15, "estimate": 0.158},
            {"condition": "low_missing", "arm": "M", "risk": 0.30, "estimate": 0.294},
            {"condition": "high_missing", "arm": "R", "risk": 0.35, "estimate": 0.343},
            {"condition": "high_missing", "arm": "M", "risk": 0.20, "estimate": 0.207},
        ],
    }
    assert abs(headroom(scenarios["no_headroom"])) < 1e-12
    assert abs(headroom(scenarios["positive_headroom"]) - 0.075) < 1e-12

    # Plug-in selector regret <= 2 epsilon for the declared uniform error bound.
    for rows in scenarios.values():
        eps = max(abs(r["estimate"] - r["risk"]) for r in rows)
        conditions = sorted({r["condition"] for r in rows})
        for c in conditions:
            sub = [r for r in rows if r["condition"] == c]
            chosen = min(sub, key=lambda r: r["estimate"])
            oracle = min(sub, key=lambda r: r["risk"])
            assert chosen["risk"] - oracle["risk"] <= 2 * eps + 1e-12

    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["scenario", "condition", "arm", "risk", "estimated_risk"])
        w.writeheader()
        for scenario, rows in scenarios.items():
            for r in rows:
                w.writerow({"scenario": scenario, "condition": r["condition"], "arm": r["arm"], "risk": r["risk"], "estimated_risk": r["estimate"]})
    print(f"no_headroom={headroom(scenarios['no_headroom']):.6f}")
    print(f"positive_headroom={headroom(scenarios['positive_headroom']):.6f}")
    print(f"output={path}")


if __name__ == "__main__":
    main()
