"""Paired group-level paper statistics from retained CSV results."""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

REQUIRED = {"method", "condition_id", "group_id", "seed", "unit_id", "value"}


def read_rows(path):
    with Path(path).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("input CSV is empty")
    missing = REQUIRED - set(rows[0])
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    for r in rows:
        r["value"] = float(r["value"])
        if not np.isfinite(r["value"]):
            raise ValueError("non-finite metric value")
    return rows


def reduce_method(rows, method, condition):
    selected = [r for r in rows if r["method"] == method and r["condition_id"] == condition]
    unit = defaultdict(list)
    for r in selected:
        unit[(r["group_id"], r["seed"], r["unit_id"])].append(r["value"])
    unit_mean = {k: float(np.mean(v)) for k, v in unit.items()}
    group_seed = defaultdict(list)
    for (group, seed, _), value in unit_mean.items():
        group_seed[(group, seed)].append(value)
    gs_mean = {k: float(np.mean(v)) for k, v in group_seed.items()}
    groups = defaultdict(list)
    for (group, _seed), value in gs_mean.items():
        groups[group].append(value)
    return unit_mean, {g: float(np.mean(v)) for g, v in groups.items()}


def interval(values, draws=2000):
    arr = np.asarray(values, dtype=float)
    if len(arr) < 2:
        return float("nan"), float("nan")
    rng = np.random.default_rng(0)
    means = np.empty(draws)
    for i in range(draws):
        means[i] = np.mean(rng.choice(arr, size=len(arr), replace=True))
    return float(np.quantile(means, .025)), float(np.quantile(means, .975))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--reference", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--direction", choices=["lower", "higher"], default="lower")
    args = p.parse_args()
    rows = read_rows(args.input)
    methods = sorted({r["method"] for r in rows})
    if args.reference not in methods:
        raise ValueError("reference method not present")
    conditions = sorted({r["condition_id"] for r in rows})
    output = []
    for condition in conditions:
        ref_units, ref_groups = reduce_method(rows, args.reference, condition)
        for method in methods:
            if method == args.reference:
                continue
            cur_units, cur_groups = reduce_method(rows, method, condition)
            if set(cur_units) != set(ref_units):
                missing = sorted(set(ref_units) - set(cur_units))[:5]
                extra = sorted(set(cur_units) - set(ref_units))[:5]
                raise ValueError(f"unpaired rows for {method}/{condition}: missing={missing}, extra={extra}")
            if set(cur_groups) != set(ref_groups):
                raise ValueError(f"group mismatch for {method}/{condition}")
            diffs = []
            for g in sorted(ref_groups):
                raw = cur_groups[g] - ref_groups[g]
                diffs.append(-raw if args.direction == "lower" else raw)
            lo, hi = interval(diffs)
            output.append({
                "condition_id": condition,
                "reference": args.reference,
                "method": method,
                "groups": len(diffs),
                "effect_positive_is_better": float(np.mean(diffs)),
                "ci_low": lo,
                "ci_high": hi,
            })
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = ["condition_id", "reference", "method", "groups", "effect_positive_is_better", "ci_low", "ci_high"]
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(output)
    print(f"comparisons={len(output)} output={out}")


if __name__ == "__main__":
    main()
