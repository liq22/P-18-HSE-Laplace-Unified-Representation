"""UCI128 variable-length acceptance plus a CPU affine-coordinate control.

Reads the official archive; it never produces or claims HSE/VAE features.
Nine speaker labels follow official sequence blocks. Source train is split into
18/6/6 utterances per speaker for fit/validation/calibration; the official test
set is unchanged. Calibration is reported, never used for fitting or selection.
"""
from __future__ import annotations
import argparse
import csv
import json
import time
from pathlib import Path
from zipfile import ZipFile
import numpy as np
from .affine_controls import fit_coordinates, ridge_fit, predict

TRAIN_COUNTS=[30]*9
TEST_COUNTS=[31,35,88,44,29,24,40,50,29]
RIDGE_GRID=(1e-4,.01,1.)
SOURCE='https://archive.ics.uci.edu/dataset/128/japanese+vowels'


def parse_sequences(text):
    sequences=[];current=[]
    for line in text.splitlines()+['']:
        if line.strip():
            row=np.asarray([float(v) for v in line.split()],dtype=np.float64)
            if row.shape!=(12,) or not np.isfinite(row).all():
                raise ValueError('each observed frame must contain 12 finite LPC coefficients')
            current.append(row)
        elif current:
            if not 7<=len(current)<=29:raise ValueError('utterance length outside official 7..29 range')
            sequences.append(np.stack(current));current=[]
    if not sequences:raise ValueError('no utterances found')
    return sequences


def read_archive(archive):
    with ZipFile(archive) as z:
        def read(name):
            matches=[p for p in z.namelist() if Path(p).name==name]
            if len(matches)!=1:raise ValueError(f'expected exactly one official {name}')
            return z.read(matches[0]).decode('utf-8')
        train=parse_sequences(read('ae.train'));test=parse_sequences(read('ae.test'))
        for name,expected in [('size_ae.train',TRAIN_COUNTS),('size_ae.test',TEST_COUNTS)]:
            observed=[int(v) for v in read(name).split()]
            if observed!=expected:raise ValueError(f'official speaker block counts differ: {name}')
    if len(train)!=270 or len(test)!=370:raise ValueError('official 270/370 split required')
    return train,test


def partition(train,test):
    result={name:[] for name in ('train','validation','calibration','test')}
    for i,seq in enumerate(train):
        label=i//30;local=i%30
        split='train' if local<18 else 'validation' if local<24 else 'calibration'
        result[split].append((f'uci128:train:{i:03d}',label,seq))
    labels=np.repeat(np.arange(9),TEST_COUNTS)
    for i,(seq,label) in enumerate(zip(test,labels)):
        result['test'].append((f'uci128:test:{i:03d}',int(label),seq))
    return result


def class_metrics(y,scores):
    y=np.asarray(y);scores=np.asarray(scores)
    if y.ndim!=1 or scores.shape!=(len(y),9) or len(y)==0 or not np.isfinite(scores).all() or not np.isin(y,range(9)).all():
        raise ValueError('nine-class paired predictions required')
    pred=scores.argmax(1);cm=np.bincount(9*y.astype(int)+pred,minlength=81).reshape(9,9)
    tp=np.diag(cm);den=cm.sum(0)+cm.sum(1)
    f1=np.divide(2*tp,den,out=np.zeros(9),where=den>0)
    return float((pred==y).mean()),float(f1.mean()),float(np.mean((scores-np.eye(9)[y.astype(int)])**2))


def export_partitions(parts,out):
    counts={};arrays={}
    for name,records in parts.items():
        x=np.zeros((len(records),29,12),dtype=np.float64);mask=np.zeros((len(records),29),dtype=bool)
        labels=[];groups=[];pooled=[]
        for i,(gid,label,seq) in enumerate(records):
            x[i,:len(seq)]=seq;mask[i,:len(seq)]=True
            labels.append(label);groups.append(gid);pooled.append(seq.mean(axis=0))
        labels=np.asarray(labels,dtype=np.int64);pooled=np.stack(pooled)
        # Time is relative to the first analysis frame, with the published 6.4ms
        # shift. The raw 10kHz audio rate is NOT the LPC feature sampling rate.
        times=np.where(mask,np.arange(29)[None,:]*.0064,0.)
        np.savez(out/f'{name}_sequences.npz',x=x,attention_mask=mask,time_from_first_frame_s=times,
                 label=labels,group_id=np.asarray(groups),length=mask.sum(1))
        arrays[name]=(pooled,labels,groups)
        counts[name]={'utterances':len(records),'valid_frames':int(mask.sum()),'length_min':int(mask.sum(1).min()),
                      'length_max':int(mask.sum(1).max()),'classes':np.unique(labels).tolist()}
    sets=[set(v[2]) for v in arrays.values()]
    if sum(map(len,sets))!=len(set.union(*sets)):raise ValueError('utterance overlap between splits')
    return counts,arrays


def run(archive,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    train,test=read_archive(archive)
    counts,data=export_partitions(partition(train,test),out)
    x,y,_=data['train'];yv=data['validation'][1]
    center,coordinates,eigenvalues=fit_coordinates(x)
    target=np.eye(9)[y];baseline_scores=[]
    for lam in RIDGE_GRID:
        coef,intercept=ridge_fit(x,target,center,coordinates['R'],lam)
        score=predict(data['validation'][0],center,coordinates['R'],coef,intercept)
        baseline_scores.append(class_metrics(yv,score)[1])
    common_lambda=RIDGE_GRID[int(np.argmax(baseline_scores))]
    rcoef,rint=ridge_fit(x,target,center,coordinates['R'],common_lambda)
    reference={name:predict(values[0],center,coordinates['R'],rcoef,rint) for name,values in data.items()}
    rows=[];predictions=[];trials=[];state={'center':center,'source_covariance_eigenvalues':eigenvalues}
    for name,a in coordinates.items():
        penalties=('isotropic',) if name=='R' else ('isotropic','matched')
        for penalty in penalties:
            model=f'{name}_{penalty}'
            if penalty=='matched':
                lam=common_lambda
            else:
                scores=[]
                for candidate in RIDGE_GRID:
                    coef,intercept=ridge_fit(x,target,center,a,candidate,penalty)
                    metric=class_metrics(yv,predict(data['validation'][0],center,a,coef,intercept))[1]
                    scores.append(metric);trials.append(dict(model=model,regularization=candidate,validation_macro_f1=metric))
                lam=RIDGE_GRID[int(np.argmax(scores))]
            start=time.perf_counter();coef,intercept=ridge_fit(x,target,center,a,lam,penalty);fit_seconds=time.perf_counter()-start
            state[f'{model}_transform']=a;state[f'{model}_coef']=coef;state[f'{model}_intercept']=intercept
            transformed=(x-center)@a
            for split in ('validation','calibration','test'):
                xp,yp,gids=data[split];score=predict(xp,center,a,coef,intercept)
                accuracy,f1,mse=class_metrics(yp,score)
                error=float(np.max(np.abs(score-reference[split])))
                if penalty=='matched' or name in ('R','PCA_R','orthogonal_R'):
                    # Full-rank rotations preserve isotropic ridge too. The source
                    # lambda selection must agree; no target-based tuning allowed.
                    if lam!=common_lambda:raise AssertionError('rotation changed source selection')
                    np.testing.assert_allclose(score,reference[split],rtol=0,atol=1e-8)
                rows.append(dict(model=model,split=split,utterances=len(yp),q=x.shape[1],dtype='float64',
                    message_bytes=x.shape[1]*8,coordinate_parameter_bytes=center.nbytes+a.nbytes,
                    predictor_parameters=coef.size+intercept.size,regularization=lam,
                    accuracy=accuracy,macro_f1=f1,onehot_mse=mse,max_abs_score_delta_from_R=error,
                    source_feature_rank=int(np.linalg.matrix_rank(transformed)),
                    source_feature_condition=float(np.linalg.cond(transformed)),fit_seconds=fit_seconds))
                for i,gid in enumerate(gids):
                    predictions.append(dict(model=model,split=split,group_id=gid,y_true=int(yp[i]),y_pred=int(score[i].argmax()),
                                            **{f'score_{j}':float(score[i,j]) for j in range(9)}))
    np.savez(out/'affine_reference.npz',**state)
    # Restore the actual fitted coefficients and reproduce the retained predictions.
    with np.load(out/'affine_reference.npz',allow_pickle=False) as saved:
        for row in rows:
            model,split=row['model'],row['split']
            pred=predict(data[split][0],saved['center'],saved[model+'_transform'],saved[model+'_coef'],saved[model+'_intercept'])
            acc,f1,_=class_metrics(data[split][1],pred)
            np.testing.assert_allclose([acc,f1],[row['accuracy'],row['macro_f1']],rtol=0,atol=1e-12)
    for name,values in [('affine_summary',rows),('predictions',predictions),('source_trials',trials)]:
        with (out/f'{name}.csv').open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(values[0]));w.writeheader();w.writerows(values)
    report=dict(source=SOURCE,dataset_doi='10.24432/C5NS47',license='CC BY 4.0',
                archive_filename=Path(archive).name,source_fit_rule='first18 per speaker fit; next6 validation; last6 calibration',
                official_test_unchanged=True,frame_hop_s=.0064,raw_audio_sample_rate_hz=10000,
                split_counts=counts,primary_task='speaker classification, not unseen-speaker generalization',
                representation='12-dimensional time-mean LPC coefficients, not HSE',
                consumer='closed-form onehot ridge; outputs are scores, not probabilities',
                independent_group_limitation='utterance IDs unique; session/speaker dependence not resolved; no iid certificate',
                common_lambda=common_lambda,scaling_fit='source-fit utterances only',summary_rows=len(rows))
    (out/'acceptance.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    for r in rows:
        if r['split']=='test':print(r)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True);args=p.parse_args();run(args.archive,args.output_dir)

if __name__=='__main__':main()
