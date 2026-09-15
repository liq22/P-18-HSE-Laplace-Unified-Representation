"""Small M/B1-aux comparison on actual exported frozen HSE/reference features.

There is deliberately no synthetic fallback. This script trains the installed
LLapDiff, not the HSE or reference encoder. The export note defines that boundary.
"""
import argparse
import copy
import csv
import json
import time
from pathlib import Path
import numpy as np
import torch
from .feature_data import load_features, check_splits, inputs
from .fit_moment_probe import fit_shared, diagnostics


def energy_score(draws, truth, mask):
    """Unbiased sample Energy Score, Euclidean norm divided by sqrt(valid size)."""
    if draws.shape[0] < 2:
        raise ValueError('Energy Score needs at least two independent draws')
    result=[]
    for i in range(len(truth)):
        d=draws[:,i,mask[i]].flatten(1)
        y=truth[i,mask[i]].flatten()
        distance_to_y=torch.linalg.vector_norm(d-y,dim=-1).mean()
        pairwise=torch.cdist(d,d).sum()/(len(d)*(len(d)-1))
        result.append((distance_to_y-.5*pairwise)/np.sqrt(len(y)))
    return torch.stack(result)


def native_model(data, device):
    from llapdiffusion.models.llapdiff import LLapDiff
    width=data['tokens'].shape[-1]
    if width%2:
        raise ValueError('this minimal configuration needs an even condition width')
    return LLapDiff(data_dim=data['z0'].shape[-1],hidden_dim=width,num_layers=1,num_heads=2,
        laplace_k=4,predict_type='v',timesteps=64,schedule='cosine',dropout=0.,attn_dropout=0.,
        block_summary_adaln=True,analysis_summary_qk=True).to(device)


def pilot(train, val, test, seeds, anchor_steps, diffusion_steps, draws, sample_steps, device, output):
    from llapdiffusion.models.llapdiff_utils import diffusion_loss
    records=[]; history=[]; costs=[]; anchor_scores=[]
    for seed in seeds:
        start=time.perf_counter()
        anchor, anchor_rows, anchor_step=fit_shared(train,val,anchor_steps,seed)
        anchor_seconds=time.perf_counter()-start
        for split_name,split in [('validation',val),('test',test)]:
            for condition_id in np.unique(split['condition_id']):
                idx=np.flatnonzero(split['condition_id']==condition_id)
                anchor_scores.append({'seed':seed,'split':split_name,'condition_id':condition_id,
                    **diagnostics(anchor,split,idx)})
        with (output/f'anchor_seed{seed}.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(anchor_rows[0]));w.writeheader();w.writerows(anchor_rows)
        # This same fitted checkpoint supervises and freezes both arms.
        anchor.to(device)
        frozen=copy.deepcopy(anchor.state_dict())
        torch.manual_seed(seed+1000)
        initial=native_model(train,device).state_dict()
        for arm in ['B1_aux','M']:
            torch.manual_seed(seed+2000)
            if str(device).startswith('cuda'):
                torch.cuda.manual_seed_all(seed+2000)
                torch.cuda.synchronize()
            start=time.perf_counter()
            model=native_model(train,device);model.load_state_dict(initial)
            optimizer=torch.optim.Adam(model.parameters(),lr=1e-3)
            # Equal predeclared validation subset; no target-domain selection.
            nv=min(64,len(val['tokens']))
            with torch.no_grad():
                cv=anchor(*inputs(val,slice(0,nv),device),arm)
            zv=val['z0'][:nv].to(device);mv=val['target_mask'][:nv].to(device)
            tv=torch.arange(nv,device=device)%63+1
            ev=torch.randn(zv.shape,generator=torch.Generator(device=device).manual_seed(seed+3000),device=device)
            xv,_=model.scheduler.q_sample(zv,tv,ev)
            best=float('inf');selected=0;state=None
            for step in range(1,diffusion_steps+1):
                model.train()
                index=torch.randint(len(train['tokens']),(min(16,len(train['tokens'])),))
                with torch.no_grad(): c=anchor(*inputs(train,index,device),arm)
                z=train['z0'][index].to(device);m=train['target_mask'][index].to(device)
                dt=train['query_time_s'][index].to(device)
                t=torch.randint(1,64,(len(z),),device=device);noise=torch.randn_like(z)
                xt,_=model.scheduler.q_sample(z,t,noise)
                optimizer.zero_grad(set_to_none=True)
                loss=diffusion_loss(model,model.scheduler,z,t,cond_summary=c,dt=dt,
                    predict_type='v',weight_scheme='none',minsnr_normalize='none',
                    target_mask=m,reuse_xt_eps=(xt,noise))
                if not torch.isfinite(loss): raise FloatingPointError('nonfinite native loss')
                loss.backward();optimizer.step()
                if step%25==0 or step==diffusion_steps:
                    model.eval()
                    with torch.no_grad():
                        vl=diffusion_loss(model,model.scheduler,zv,tv,cond_summary=cv,
                            dt=val['query_time_s'][:nv].to(device),predict_type='v',weight_scheme='none',
                            minsnr_normalize='none',target_mask=mv,reuse_xt_eps=(xv,ev))
                    history.append({'seed':seed,'arm':arm,'step':step,'train_loss':float(loss.detach()),'validation_loss':float(vl)})
                    if float(vl)<best: best=float(vl);selected=step;state=copy.deepcopy(model.state_dict())
            model.load_state_dict(state);model.eval()
            if str(device).startswith('cuda'): torch.cuda.synchronize()
            train_seconds=time.perf_counter()-start
            torch.save({'model':state,'conditioner':anchor.state_dict(),'conditioner_config':anchor.config(),
                        'seed':seed,'arm':arm,'selected_step':selected,'anchor_selected_step':anchor_step},
                       output/f'{arm}_seed{seed}.pt')
            start=time.perf_counter()
            for begin in range(0,len(test['tokens']),8):
                end=min(begin+8,len(test['tokens']));index=slice(begin,end)
                with torch.no_grad():
                    c=anchor(*inputs(test,index,device),arm)
                    dt=test['query_time_s'][index].to(device)
                    rng=torch.Generator(device=device).manual_seed(seed+4000+begin)
                    samples=torch.stack([model.generate(tuple(test['z0'][index].shape),steps=sample_steps,
                        guidance_strength=1.,cfg_rescale=False,eta=0.,cond_summary=c,dt=dt,generator=rng)
                        for _ in range(draws)])
                    es=energy_score(samples,test['z0'][index].to(device),test['target_mask'][index].to(device))
                for i,value in enumerate(es):
                    row=begin+i
                    records.append({'seed':seed,'arm':arm,'event_id':test['event_id'][row],
                        'group_id':test['group_id'][row],'condition_id':test['condition_id'][row],
                        'energy_score':float(value),'posterior_draws':draws,'sampler_steps':sample_steps})
            if str(device).startswith('cuda'): torch.cuda.synchronize()
            for key,value in anchor.state_dict().items():
                torch.testing.assert_close(value,frozen[key],rtol=0,atol=0)
            costs.append({'seed':seed,'arm':arm,'anchor_cpu_seconds':anchor_seconds,
                          'denoiser_training_seconds':train_seconds,'sampling_seconds':time.perf_counter()-start,
                          'conditioner_parameters':sum(p.numel() for p in anchor.parameters()),
                          'denoiser_parameters':sum(p.numel() for p in model.parameters()),
                          'message_scalars':anchor.budget,'anchor_selected_step':anchor_step,
                          'denoiser_selected_step':selected})
    for name,rows in [('event_scores',records),('training_curve',history),('costs',costs),('anchor_scores',anchor_scores)]:
        with (output/f'{name}.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['train','validation','test','data-note','output-dir']:
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--device',required=True)
    p.add_argument('--seeds',type=int,nargs='+',default=[0,1,2])
    p.add_argument('--anchor-steps',type=int,default=150)
    p.add_argument('--diffusion-steps',type=int,default=200)
    p.add_argument('--draws',type=int,default=8);p.add_argument('--sampler-steps',type=int,default=16)
    args=p.parse_args()
    if not args.data_note.is_file(): p.error('actual HSE/reference export note is required')
    if len(set(args.seeds))!=len(args.seeds): p.error('training seeds must be distinct')
    if min(args.anchor_steps,args.diffusion_steps,args.sampler_steps)<1 or args.draws<2:
        p.error('positive update counts and at least two draws are required')
    if args.sampler_steps>64: p.error('sampler steps cannot exceed the declared 64-step schedule')
    device=torch.device(args.device)
    if device.type not in ('cpu','cuda'): p.error('select cpu or an explicit CUDA device')
    if device.type=='cuda' and not torch.cuda.is_available(): p.error('requested CUDA is unavailable')
    data=[load_features(path,native=True) for path in [args.train,args.validation,args.test]]
    check_splits(*data)
    if not set(data[1]['condition_id'])<=set(data[0]['condition_id']):
        p.error('validation contains unseen acquisition conditions; reserve these for test')
    args.output_dir.mkdir(parents=True,exist_ok=False)
    torch.set_num_threads(1)
    pilot(*data,args.seeds,args.anchor_steps,args.diffusion_steps,args.draws,args.sampler_steps,device,args.output_dir)
    settings={key:str(value) if isinstance(value,Path) else value for key,value in vars(args).items()}
    settings['scope']='native LLapDiff on supplied frozen exports, not on-the-fly HSE/VAE execution'
    settings['decision']='report M minus B1_aux; no automatic promotion or full experiment launch'
    (args.output_dir/'settings.json').write_text(json.dumps(settings,indent=2),encoding='utf-8')
    print('Completed the declared comparison; both favorable and unfavorable rows are retained.')

if __name__=='__main__':main()
