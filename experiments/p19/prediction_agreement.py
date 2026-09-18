"""Replay a frozen multiclass score bank before fitting any classifier router.

Input is the retained Japanese-Vowels prediction CSV, not raw data or HSE
features. Source validation selects a two-score static mixture by onehot MSE.
All-model label agreement bounds *label-changing opportunity*, not proper-score
headroom, calibration, population performance or a jointly retrained fusion.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import numpy as np


def load_bank(path, classes=9):
    if classes < 2:
        raise ValueError('at least two declared classes required')
    with Path(path).open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        required = {'model', 'split', 'group_id', 'y_true', 'y_pred'} | {f'score_{k}' for k in range(classes)}
        if not required <= set(reader.fieldnames or ()):
            raise ValueError('missing identity, label or score columns')
        rows = list(reader)
    if not rows:
        raise ValueError('empty prediction bank')
    models = sorted({r['model'] for r in rows})
    if len(models) < 2:
        raise ValueError('at least two frozen models required')
    by_split = {}
    all_ids = set()
    for split in ('validation', 'calibration', 'test'):
        chosen = [r for r in rows if r['split'] == split]
        ids = sorted({r['group_id'] for r in chosen})
        if not ids or any(not gid.strip() for gid in ids):
            raise ValueError(f'empty split or original ID: {split}')
        if all_ids & set(ids):
            raise ValueError('original IDs cross source-validation/calibration/test')
        all_ids.update(ids)
        keys = [(r['model'], r['group_id']) for r in chosen]
        if len(keys) != len(set(keys)):
            raise ValueError(f'duplicate model/original-ID pair: {split}')
        if set(keys) != {(m, g) for m in models for g in ids}:
            raise ValueError(f'incomplete frozen-model pairing: {split}')
        lookup = dict(zip(keys, chosen))
        y = np.array([int(lookup[models[0], g]['y_true']) for g in ids])
        if not np.isin(y, np.arange(classes)).all():
            raise ValueError('label outside declared ontology')
        score = np.empty((len(models), len(ids), classes), dtype=np.float64)
        for j, model in enumerate(models):
            for i, gid in enumerate(ids):
                row = lookup[model, gid]
                if int(row['y_true']) != y[i]:
                    raise ValueError('truth differs across paired models')
                score[j, i] = [float(row[f'score_{k}']) for k in range(classes)]
                if not np.isfinite(score[j, i]).all():
                    raise ValueError('nonfinite class scores')
                if int(row['y_pred']) != int(score[j, i].argmax()):
                    raise ValueError('stored class decision does not match argmax')
        by_split[split] = (ids, y, score)
    if {r['split'] for r in rows} != set(by_split):
        raise ValueError('unexpected split; do not silently ignore rows')
    return models, by_split


def agreement(scores):
    x = np.asarray(scores, dtype=np.float64)
    if x.ndim != 3 or min(x.shape) < 1 or x.shape[2] < 2 or not np.isfinite(x).all():
        raise ValueError('finite scores[models,examples,classes] required')
    labels = x.argmax(axis=2)
    common = np.all(labels == labels[:1], axis=0)
    first = labels[0]
    competitor = x.copy()
    competitor[:, np.arange(len(first)), first] = -np.inf
    margin = x[:, np.arange(len(first)), first] - competitor.max(axis=2)
    return common, margin.min(axis=0)


def fit_static(first, second, y):
    """Source-validation minimizer of squared *scores*, not Brier probability loss."""
    a, b = np.asarray(first, float), np.asarray(second, float)
    if a.ndim != 2 or a.shape != b.shape or np.asarray(y).shape != (len(a),) or not len(a):
        raise ValueError('paired score matrices and labels required')
    if not np.isfinite(a).all() or not np.isfinite(b).all() or not np.isin(y, range(a.shape[1])).all():
        raise ValueError('invalid scores or labels')
    d = b-a
    denominator = float(np.sum(d*d))
    if denominator == 0:
        return 0.0
    target = np.eye(a.shape[1])[np.asarray(y, dtype=int)]
    return float(np.clip(np.sum(d*(target-a))/denominator, 0., 1.))


def metrics(score, truth):
    pred = score.argmax(axis=1)
    k = score.shape[1]
    cm = np.bincount(k*truth+pred, minlength=k*k).reshape(k,k)
    tp = np.diag(cm); den = cm.sum(0)+cm.sum(1)
    f1 = np.divide(2*tp, den, out=np.zeros(k), where=den > 0)
    return float((pred == truth).mean()), float(f1.mean()), float(np.mean((score-np.eye(k)[truth])**2))


def evaluate(models, bank, reference, candidate):
    if reference == candidate or reference not in models or candidate not in models:
        raise ValueError('two different, present declared models required')
    r, c = models.index(reference), models.index(candidate)
    _, yv, sv = bank['validation']
    alpha = fit_static(sv[r], sv[c], yv)
    summaries = []; examples = []
    for split, (ids, truth, scores) in bank.items():
        same, margins = agreement(scores)
        mixed = (1-alpha)*scores[r]+alpha*scores[c]
        for name, sc in [(reference,scores[r]),(candidate,scores[c]),('source_static_score_mixture',mixed)]:
            acc, f1, mse = metrics(sc,truth)
            summaries.append(dict(split=split,model=name,examples=len(ids),static_alpha=alpha,
                                  accuracy=acc,macro_f1=f1,onehot_score_mse=mse,
                                  differing_from_reference=int(np.sum(sc.argmax(1)!=scores[r].argmax(1))),
                                  bank_models=len(models),bank_disagreement_examples=int(np.sum(~same)),
                                  minimum_bank_label_margin=float(margins.min()),
                                  strict_label_agreement=bool(same.all() and (margins>0).all())))
        for i,gid in enumerate(ids):
            examples.append(dict(split=split,group_id=gid,y_true=int(truth[i]),
                                 reference_label=int(scores[r,i].argmax()),
                                 mixture_label=int(mixed[i].argmax()),all_models_agree=bool(same[i]),
                                 minimum_label_margin=float(margins[i])))
    return summaries, examples


def plot_csv(path, output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    with Path(path).open(newline='',encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError('empty result CSV')
    plt.rcParams.update({'svg.fonttype':'none','pdf.fonttype':42,'font.size':9})
    output = Path(output);output.mkdir(parents=True,exist_ok=True)
    splits = ['validation','calibration','test']
    for key, label, stem in [('minimum_bank_label_margin','Smallest common-label score margin','agreement_margin'),
                            ('onehot_score_mse','Mean squared class-score error','static_score_mse')]:
        fig, ax = plt.subplots(figsize=(6.5,3.4))
        if key == 'minimum_bank_label_margin':
            vals = [float(next(r[key] for r in rows if r['split']==s)) for s in splits]
            ax.scatter(range(3),vals);ax.axhline(0,linewidth=.8)
            for i,value in enumerate(vals):
                ax.annotate(f'{value:.6g}',(i,value),xytext=(0,7),textcoords='offset points',ha='center')
            ax.margins(x=.12,y=.25)
            ax.set_xticks(range(3),splits)
            ax.set_title('Frozen reference models: observed label agreement')
        else:
            for i, name in enumerate(dict.fromkeys(r['model'] for r in rows)):
                vals = [float(next(r[key] for r in rows if r['split']==s and r['model']==name)) for s in splits]
                ax.scatter(np.arange(3)+(i-1)*.12,vals,label={'R_isotropic':'Ordinary ridge',
                    'whitened_R_isotropic':'Whitened ridge',
                    'source_static_score_mixture':'Validation-selected mixture'}.get(name,name))
            ax.set_xticks(range(3),splits);ax.legend(frameon=False,fontsize=7)
            ax.set_title('Score mixture selected on validation only')
        ax.set_ylabel(label);ax.spines[['right','top']].set_visible(False);fig.tight_layout()
        for ext in ('svg','pdf','png'):
            fig.savefig(output/f'{stem}.{ext}',dpi=300)
        plt.close(fig)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--predictions',type=Path);mode.add_argument('--plot-only',type=Path)
    p.add_argument('--reference',default='R_isotropic');p.add_argument('--candidate',default='whitened_R_isotropic')
    p.add_argument('--classes',type=int,default=9);p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args()
    if args.plot_only:
        plot_csv(args.plot_only,args.output_dir);return
    models,bank=load_bank(args.predictions,args.classes)
    summary,examples=evaluate(models,bank,args.reference,args.candidate)
    args.output_dir.mkdir(parents=True,exist_ok=False)
    for name,rows in [('agreement_summary',summary),('agreement_examples',examples)]:
        with (args.output_dir/f'{name}.csv').open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    note={'source_predictions':str(args.predictions),'reference':args.reference,'candidate':args.candidate,
          'models':models,'selection':'validation onehot score MSE, no calibration/test fitting',
          'scope':'descriptive replay of frozen predictions, no model retraining or new independent data',
          'design':'post-hoc analysis of already visible results; the new weight fit reads validation only',
          'boundary':'agreement constrains hard decisions and convex score fusion on these examples only; no proper-score or population claim',
          'independence':'no iid confidence interval; session dependence unresolved in source dataset'}
    (args.output_dir/'interpretation.json').write_text(json.dumps(note,indent=2),encoding='utf-8')
    for row in summary:print(json.dumps(row))

if __name__=='__main__':
    main()
