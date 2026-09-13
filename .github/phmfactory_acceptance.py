"""Revision-specific MFPT acceptance, run inside the PHMFactory checkout.

The public CLI performs training. Upstream constructors are used ONLY here to
restore its checkpoints and export its own datasets; paper/P19 never import them.
No raw MAT reader, alternative split, or training algorithm is implemented here.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import numpy as np


def classification_metrics(truth, prediction, classes=3):
    truth, prediction = np.asarray(truth), np.asarray(prediction)
    if truth.shape != prediction.shape or truth.ndim != 1 or not len(truth):
        raise ValueError("paired non-empty label vectors required")
    if not (np.isin(truth, range(classes)).all() and np.isin(prediction, range(classes)).all()):
        raise ValueError("label outside the declared ontology")
    cm = np.bincount(classes * truth.astype(int) + prediction.astype(int),
                     minlength=classes * classes).reshape(classes, classes)
    tp = np.diag(cm)
    denominator = cm.sum(0) + cm.sum(1)
    f1 = np.divide(2 * tp, denominator, out=np.zeros(classes, float), where=denominator > 0)
    return float(tp.sum() / cm.sum()), float(f1.mean())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        acc, f1 = classification_metrics([0, 0, 1, 1, 2, 2], [0, 1, 1, 2, 2, 2])
        np.testing.assert_allclose([acc, f1], [2 / 3, 59 / 90])
        print(f"independent_metric_fixture accuracy={acc:.10f} macro_f1={f1:.10f}")
        return
    if args.data is None or args.output is None:
        parser.error("--data and --output are required for real-data acceptance")
    import torch
    from pytorch_lightning import seed_everything
    from phmfactory.cli import main as public_main
    from phmfactory.config import analyze_config
    from src.configs.config_utils import dict_to_namespace, transfer_namespace
    from src.data_factory import build_data
    from src.model_factory import build_model
    from src.task_factory import build_task

    data_root, output = args.data.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    with (data_root / "metadata_mfpt.csv").open(newline="", encoding="utf-8") as f:
        metadata_rows = list(csv.DictReader(f))
    assert len(metadata_rows) == 20
    assert sum(r["Provider_Split"] == "train" for r in metadata_rows) == 14
    assert sum(r["Provider_Split"] == "test" for r in metadata_rows) == 6
    assert {int(r["Label"]) for r in metadata_rows} == {0, 1, 2}
    assert {int(r["Channels"]) for r in metadata_rows} == {1}
    assert all(float(r["Sample_Rate"]) > 0 for r in metadata_rows)
    config = "configs/baselines/01_mfpt/mfpt_global_average_linear.yaml"
    overrides = [f"data.data_dir={data_root}", f"environment.output_dir={output / 'runs'}",
                 f"data.split.manifest_path={output / 'split_manifest.json'}"]
    cli_args = ["--config", config]
    for item in overrides:
        cli_args += ["--override", item]
    public_main(["preflight", *cli_args])
    result = public_main(cli_args)
    (output / "direct_outputs.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    resolved = analyze_config(config, override_values=overrides).to_resolved_config()
    (output / "resolved_config.json").write_text(json.dumps(resolved, indent=2), encoding="utf-8")
    cfg = dict_to_namespace(resolved)
    env, data_args, model_args, task_args, trainer_args = [
        transfer_namespace(getattr(cfg, key)) for key in ("environment", "data", "model", "task", "trainer")]
    assert env.seed == 17 and env.iterations == 3
    assert trainer_args.num_epochs == 5 and task_args.metrics == ["acc", "f1"]
    assert len(result["best_checkpoints"]) == 3 and len(result["iterations"]) == 3
    split = json.loads((output / "split_manifest.json").read_text())
    groups = {s: set(split["splits"][s]["groups"]) for s in ("train", "val", "test")}
    assert groups["train"] and groups["val"] and groups["test"]
    assert len(groups["train"] | groups["val"]) == 14 and len(groups["test"]) == 6
    assert not (groups["train"] & groups["val"] or groups["train"] & groups["test"] or groups["val"] & groups["test"])
    accepted, predictions = [], []
    for iteration, seed in enumerate((17, 18, 19)):
        seed_everything(seed)
        factory = build_data(data_args, task_args)
        metadata = factory.get_metadata()
        network = build_model(model_args, metadata=metadata)
        task = build_task(args_task=task_args, network=network, args_data=data_args,
                          args_model=model_args, args_trainer=trainer_args,
                          args_environment=env, metadata=metadata)
        checkpoint = Path(result["best_checkpoints"][iteration])
        payload = torch.load(checkpoint, map_location="cpu", weights_only=False)
        task.load_state_dict(payload["state_dict"], strict=True)
        task.eval()
        truth, predicted = [], []
        with torch.no_grad():
            for batch in factory.get_dataloader("test"):
                logits = task(batch)
                target = batch["y"].reshape(-1).cpu().numpy().astype(int)
                pred = logits.argmax(-1).cpu().numpy().astype(int)
                assert logits.shape == (len(target), 3) and np.isfinite(logits.cpu().numpy()).all()
                ids = task._file_id_values(batch["file_id"])
                assert len(ids) == len(target)
                for file_id, y, yp, scores in zip(ids, target, pred, logits.cpu().numpy()):
                    source = metadata[file_id]
                    predictions.append(dict(seed=seed, file_id=file_id, group_id=source["File"],
                                            y_true=int(y), y_pred=int(yp),
                                            logit_0=float(scores[0]), logit_1=float(scores[1]), logit_2=float(scores[2])))
                truth.extend(target.tolist()); predicted.extend(pred.tolist())
        acc, f1 = classification_metrics(truth, predicted)
        reported = result["iterations"][iteration]
        ea = abs(acc - reported["test_acc_RM_007_MFPT"])
        ef = abs(f1 - reported["test_f1_RM_007_MFPT"])
        assert max(ea, ef) < 1e-6, (seed, acc, f1, reported)
        accepted.append(dict(seed=seed, test_windows=len(truth), accuracy=acc, macro_f1=f1,
                             accuracy_abs_error=ea, macro_f1_abs_error=ef, selected_epoch=int(payload["epoch"])))
        if iteration == 0:
            exported_groups = {}
            # Sequential dataset access retains PHMFactory's selected windows and split;
            # it does not inherit a training sampler's dropping/oversampling policy.
            for stage in ("train", "val", "test"):
                dataset = factory.get_dataloader(stage).dataset
                waveforms, labels, file_ids, group_ids, rates = [], [], [], [], []
                for index in range(len(dataset)):
                    sample = dataset[index]
                    ids = task._file_id_values(sample["file_id"])
                    assert len(ids) == 1
                    fid = ids[0]; row = metadata[fid]
                    waveforms.append(torch.as_tensor(sample["x"]).cpu().numpy())
                    labels.append(int(torch.as_tensor(sample["y"]).item()))
                    file_ids.append(str(fid)); group_ids.append(str(row["File"]))
                    rates.append(float(row["Sample_Rate"]))
                assert waveforms and set(group_ids) == groups[stage]
                x = np.stack(waveforms)
                assert x.shape[1:] == (2048, 1) and np.isfinite(x).all()
                np.savez(output / f"{stage}_waveforms.npz", x=x, label=np.asarray(labels),
                         file_id=np.asarray(file_ids), group_id=np.asarray(group_ids),
                         sample_rate_hz=np.asarray(rates), unit_id=np.arange(len(x)),
                         split=np.asarray(stage))
                exported_groups[stage] = {"windows": len(x), "recordings": len(set(group_ids)), "shape": list(x.shape)}
            (output / "export_counts.json").write_text(json.dumps(exported_groups, indent=2))
        close = getattr(factory.data, "close", None)
        if close is not None:
            close()
    summary = json.loads(Path(result["run_summary"]).read_text())
    assert summary["seeds"] == [17, 18, 19] and summary["iterations"] == 3
    for column, metric in (("accuracy", "test_acc_RM_007_MFPT"), ("macro_f1", "test_f1_RM_007_MFPT")):
        values = [r[column] for r in accepted]
        s = summary["metrics"][metric]
        assert s["count"] == 3
        np.testing.assert_allclose([np.mean(values), np.std(values, ddof=1)],
                                   [s["mean"], s["sample_std"]], atol=1e-6, rtol=0)
    for name, rows in (("acceptance", accepted), ("predictions", predictions)):
        with (output / f"{name}.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    print(json.dumps({"scope": "MFPT reference acceptance only; not HSE method evidence", "seeds": accepted,
                      "waveform_export": "created; raw/derived signal arrays are not uploaded by CI"}, indent=2))


if __name__ == "__main__":
    main()
