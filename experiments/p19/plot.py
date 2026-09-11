"""CSV-only TII comparison figure."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output-dir", required=True)
    args = p.parse_args()
    with Path(args.input).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("summary CSV is empty")
    labels = [f"{r['method']} | {r['condition_id']}" for r in rows]
    effect = np.array([float(r["effect_positive_is_better"]) for r in rows])
    lo = np.array([float(r["ci_low"]) for r in rows])
    hi = np.array([float(r["ci_high"]) for r in rows])
    finite_ci = np.isfinite(lo) & np.isfinite(hi)
    y = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(6.8, max(2.5, .35 * len(rows) + 1.2)))
    ax.axvline(0, linewidth=.8)
    ax.scatter(effect, y, s=24)
    if finite_ci.any():
        err = np.vstack([effect[finite_ci] - lo[finite_ci], hi[finite_ci] - effect[finite_ci]])
        ax.errorbar(effect[finite_ci], y[finite_ci], xerr=err, fmt="none", capsize=2, linewidth=.9)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Paired group-level effect (positive = candidate better)")
    ax.set_ylabel("")
    ax.invert_yaxis()
    ax.grid(axis="x", linewidth=.4, alpha=.35)
    fig.tight_layout()
    out = Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    for suffix in ("svg", "pdf", "png"):
        fig.savefig(out / f"paired_effects.{suffix}", dpi=300 if suffix == "png" else None, bbox_inches="tight")
    plt.close(fig)
    print(f"rows={len(rows)} output_dir={out}")


if __name__ == "__main__":
    main()
