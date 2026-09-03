#!/usr/bin/env python3
"""Validate and execute every theory witness in an isolated kernel."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def numbered_theory_files(theory_dir: Path) -> list[Path]:
    return sorted(path for path in theory_dir.glob("[0-9][0-9]_*.md") if path.is_file())


def validate_source_notebook(path: Path, expected_proof: str) -> nbformat.NotebookNode:
    notebook = nbformat.read(path, as_version=4)
    metadata = notebook.metadata.get("hse_theory", {})
    if metadata.get("proof_file") != expected_proof:
        raise ValueError(f"{path}: proof_file must be {expected_proof!r}")
    if metadata.get("formal_claim_supported") is not False:
        raise ValueError(f"{path}: formal_claim_supported must remain false")
    if metadata.get("evidence_level") != "constructive_or_numerical_witness":
        raise ValueError(f"{path}: invalid evidence_level")
    for cell in notebook.cells:
        if cell.cell_type == "code":
            if cell.get("execution_count") is not None:
                raise ValueError(f"{path}: source notebook must be unexecuted")
            if cell.get("outputs"):
                raise ValueError(f"{path}: source notebook must not store outputs")
    return notebook


def execute_notebook(
    source: Path,
    destination: Path,
    *,
    timeout: int,
    kernel_name: str,
) -> dict[str, object]:
    notebook = nbformat.read(source, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=timeout,
        kernel_name=kernel_name,
        allow_errors=False,
        resources={"metadata": {"path": str(source.parents[2])}},
    )
    executed = client.execute()
    sentinel = f"THEORY_DEMO_PASS::{source.stem}"
    text_outputs: list[str] = []
    for cell in executed.cells:
        if cell.cell_type != "code":
            continue
        for output in cell.get("outputs", []):
            if output.output_type == "stream":
                text_outputs.append(output.get("text", ""))
            elif output.output_type in {"execute_result", "display_data"}:
                text = output.get("data", {}).get("text/plain", "")
                if isinstance(text, list):
                    text = "".join(text)
                text_outputs.append(str(text))
    if sentinel not in "\n".join(text_outputs):
        raise RuntimeError(f"{source}: completion sentinel missing")
    destination.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(executed, destination)
    return {"theory_id": source.stem[:2], "notebook": str(source), "status": "passed"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--kernel-name", default="python3")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    theory_dir = repo_root / "theory"
    notebook_dir = theory_dir / "notebooks"
    proofs = numbered_theory_files(theory_dir)
    expected = {path.stem for path in proofs}
    actual = {path.stem for path in notebook_dir.glob("*.ipynb")}
    if expected != actual:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise RuntimeError(f"proof/notebook mismatch: missing={missing}, extra={extra}")

    temporary_output = args.output_dir is None
    output_dir = args.output_dir or Path(tempfile.mkdtemp(prefix="hse-theory-notebooks-"))
    results: list[dict[str, object]] = []
    try:
        for proof in proofs:
            source = notebook_dir / f"{proof.stem}.ipynb"
            validate_source_notebook(source, f"theory/{proof.name}")
            result = execute_notebook(
                source,
                output_dir / source.name,
                timeout=args.timeout,
                kernel_name=args.kernel_name,
            )
            results.append(result)
            print(f"PASS {proof.stem}")
        summary = {
            "status": "passed",
            "proof_count": len(proofs),
            "notebook_count": len(results),
            "formal_claim_supported": False,
            "evidence_level": "constructive_or_numerical_witness",
            "results": results,
        }
        if args.summary:
            args.summary.parent.mkdir(parents=True, exist_ok=True)
            args.summary.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(json.dumps({key: summary[key] for key in summary if key != "results"}, indent=2))
    finally:
        if temporary_output:
            shutil.rmtree(output_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
