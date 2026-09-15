"""Export an installed native training-time measure, never reverse-sampler steps.

Uniform discrete training times and fixed none/global normalization are explicit.
Batch-normalized objectives are checked using actual batches by native_forward.
"""
import argparse
import csv
import json
from pathlib import Path
import torch
from llapdiffusion.models.llapdiff_utils import NoiseScheduler, _minsnr_weights, _normalize_loss_weights


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--timesteps',type=int,default=1000)
    p.add_argument('--schedule',choices=['cosine','linear'],default='cosine')
    p.add_argument('--prediction',choices=['eps','v','x0'],required=True)
    p.add_argument('--weight',choices=['none','weighted_min_snr'],required=True)
    p.add_argument('--normalization',choices=['none','global'],required=True)
    p.add_argument('--gamma',type=float,default=5.)
    args=p.parse_args()
    if args.timesteps<3: p.error('at least three timesteps are required')
    if args.weight=='none' and args.normalization!='none':
        p.error('use normalization=none for an unweighted declared protocol')
    scheduler=NoiseScheduler(timesteps=args.timesteps,schedule=args.schedule)
    t=torch.arange(1,args.timesteps)
    raw=torch.ones(len(t)) if args.weight=='none' else _minsnr_weights(
        scheduler,t,gamma=args.gamma,predict_type=args.prediction)
    weights=raw if args.normalization=='none' else _normalize_loss_weights(
        raw,scheduler=scheduler,gamma=args.gamma,predict_type=args.prediction,
        normalize='global',exclude_t0=True)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f);writer.writerow(['time_index','alpha_bar','probability','loss_weight','prediction'])
        for step,weight in zip(t,weights):
            writer.writerow([int(step),float(scheduler.alpha_bars[step]),1/len(t),float(weight),args.prediction])
    print(json.dumps({'path':str(args.output),'source':'installed native NoiseScheduler',
                      'time_sampling':'uniform discrete 1..T-1','weight':args.weight,
                      'normalization':args.normalization,'prediction':args.prediction},indent=2))

if __name__=='__main__':main()
