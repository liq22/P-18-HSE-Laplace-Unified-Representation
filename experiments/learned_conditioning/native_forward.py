"""One-batch checks against the installed original LLapDiff, not a mirror.

--component-smoke uses explicitly synthetic features; --batch consumes a real
export and requires its provenance note. Neither mode claims end-to-end HSE
training. A missing native dependency fails, without a replacement denoiser.
"""
import argparse
import copy
import csv
import inspect
import json
from pathlib import Path
import torch
from .moment_conditioner import MatchedConditioner
from .feature_data import load_features, inputs


def independent_parts(model, scheduler, z0, xt, noise, t, condition, query_time,
                      mask, prediction, weighting, normalization, gamma=5.):
    pred = model(xt, t, cond_summary=condition, dt=query_time)
    alpha = scheduler.sqrt_alpha_bars[t].view(-1, 1, 1)
    sigma = scheduler.sqrt_one_minus_alpha_bars[t].view(-1, 1, 1)
    target = {'eps': noise, 'v': alpha*noise-sigma*z0, 'x0': z0}[prediction]
    expanded = mask[..., None].expand_as(pred)
    raw_loss = (((pred-target)**2)*expanded).sum((1, 2))/expanded.sum((1, 2))
    def weight_at(indices):
        abar = scheduler.alpha_bars[indices].clamp(1e-6, 1-1e-6)
        snr = abar/(1-abar)
        clipped = snr.clamp(max=gamma)
        return {'eps': clipped/snr.clamp_min(1e-8), 'v': clipped/(snr+1), 'x0': clipped}[prediction]
    raw_weight = torch.ones_like(raw_loss) if weighting == 'none' else weight_at(t)
    if normalization == 'none':
        denominator = raw_weight.new_tensor(1.)
    elif normalization == 'batch':
        denominator = raw_weight.mean().clamp_min(1e-8)
    elif normalization == 'global':
        denominator = weight_at(torch.arange(1, scheduler.timesteps, device=t.device)).mean().clamp_min(1e-8)
    else:
        raise ValueError('explicit none/batch/global normalization required')
    weights = raw_weight/denominator
    return raw_loss, raw_weight, weights, (raw_loss*weights).mean()


def check_native(data, output, component_only=False):
    from llapdiffusion.models.llapdiff import LLapDiff
    from llapdiffusion.models.llapdiff_utils import diffusion_loss, sample_training_timesteps
    torch.set_num_threads(1); torch.manual_seed(41)
    h, mask, side = inputs(data, slice(0, 4))
    z0 = data['z0'][:4]; target_mask = data['target_mask'][:4]
    dt = data['query_time_s'][:4]
    if h.shape[-1] % 2:
        raise ValueError('native minimal check uses two heads and needs an even width')
    condition = MatchedConditioner(h.shape[1], h.shape[2], data['targets'].shape[1], side.shape[1])
    optimizer = torch.optim.SGD(condition.parameters(), lr=.01)
    before_code = condition.ordinary(h, mask, side).detach().clone()
    condition.score_parts(h, mask, side, data['targets'][:4])['score'].mean().backward()
    aux_grad = sum(float(p.grad.abs().sum()) for p in condition.trunk.parameters())
    if aux_grad <= 0:
        raise AssertionError('auxiliary supervision did not reach the consumed ordinary path')
    optimizer.step(); condition.freeze_for_denoising()
    code_change = float((condition.ordinary(h, mask, side)-before_code).abs().max())
    frozen_state = copy.deepcopy(condition.state_dict())
    config = dict(data_dim=z0.shape[-1], hidden_dim=h.shape[-1], num_layers=1,
                  num_heads=2, laplace_k=4, predict_type='v', timesteps=64,
                  schedule='cosine', dropout=0., attn_dropout=0.,
                  block_summary_adaln=True, analysis_summary_qk=True)
    template = LLapDiff(**config)
    initial = copy.deepcopy(template.state_dict())
    t = sample_training_timesteps(template.scheduler, len(z0), z0.device, sampler='uniform')
    noise = torch.randn_like(z0)
    xt, actual_noise = template.scheduler.q_sample(z0, t, noise=noise)
    torch.testing.assert_close(actual_noise, noise, rtol=0, atol=0)
    rows, effects = [], {}
    for arm in ['B1_aux', 'M']:
        model = LLapDiff(**config); model.load_state_dict(initial); model.eval()
        c = condition(h, mask, side, arm)
        for prediction in ['eps', 'v', 'x0']:
            for weighting, normalization in [('none','none'), ('weighted_min_snr','none'),
                                              ('weighted_min_snr','global'), ('weighted_min_snr','batch')]:
                with torch.no_grad():
                    native, stats = diffusion_loss(model, model.scheduler, z0, t,
                        cond_summary=c, dt=dt, predict_type=prediction,
                        weight_scheme=weighting, minsnr_normalize=normalization,
                        reuse_xt_eps=(xt, noise), target_mask=target_mask, return_stats=True)
                    raw, wr, w, direct = independent_parts(model, model.scheduler, z0, xt, noise, t,
                        c, dt, target_mask, prediction, weighting, normalization)
                for expected, observed in [(raw,stats['per_sample_raw']), (wr,stats['weights_raw']),
                                            (w,stats['weights']), (direct,native)]:
                    torch.testing.assert_close(expected, observed, rtol=3e-5, atol=3e-6)
                for i in range(len(z0)):
                    rows.append({'arm':arm,'prediction':prediction,'weighting':weighting,
                        'normalization':normalization,'batch_item':i,'time_index':int(t[i]),
                        'time_probability':1/(model.scheduler.timesteps-1),
                        'alpha':float(model.scheduler.sqrt_alpha_bars[t[i]]),
                        'sigma':float(model.scheduler.sqrt_one_minus_alpha_bars[t[i]]),
                        'valid_target_elements':int(target_mask[i].sum())*z0.shape[-1],
                        'raw_loss_native':float(stats['per_sample_raw'][i]),'raw_loss_direct':float(raw[i]),
                        'raw_weight':float(wr[i]),'effective_weight':float(w[i]),
                        'batch_loss_native':float(native),'batch_loss_direct':float(direct),
                        'absolute_loss_difference':abs(float(native-direct))})
        # One native update per arm, with equal initialization, target and noise.
        model.train(); opt = torch.optim.Adam(model.parameters(), lr=1e-3)
        parameter = next(model.parameters()); old_parameter = parameter.detach().clone()
        loss = diffusion_loss(model, model.scheduler, z0, t, cond_summary=c, dt=dt,
                              predict_type='v', reuse_xt_eps=(xt,noise), target_mask=target_mask,
                              weight_scheme='none', minsnr_normalize='none')
        opt.zero_grad(set_to_none=True); loss.backward()
        grad = sum(float(p.grad.abs().sum()) for p in model.parameters() if p.grad is not None)
        opt.step(); model.eval()
        with torch.no_grad():
            base = model(xt,t,cond_summary=c,dt=dt)
            changed_stat = c.clone().reshape(len(c),-1); changed_stat[:,:condition.semantic_size] += .1
            changed_tail = c.clone().reshape(len(c),-1); changed_tail[:,condition.semantic_size:] += .1
            stat_effect = float((model(xt,t,cond_summary=changed_stat.reshape_as(c),dt=dt)-base).abs().max())
            tail_effect = float((model(xt,t,cond_summary=changed_tail.reshape_as(c),dt=dt)-base).abs().max())
        if grad <= 0 or stat_effect <= 0 or tail_effect <= 0 or torch.equal(parameter,old_parameter):
            raise AssertionError('native update or field consumption failed')
        for key, value in condition.state_dict().items():
            torch.testing.assert_close(value, frozen_state[key], rtol=0, atol=0)
        if any(p.grad is not None for p in condition.parameters()):
            raise AssertionError('frozen conditioner accumulated denoising gradients')
        effects[arm] = {'denoiser_gradient_l1':grad,'prefix_effect':stat_effect,
                       'tail_effect':tail_effect,'frozen_conditioner_unchanged':True}
    output.mkdir(parents=True,exist_ok=True)
    with (output/'native_loss_alignment.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    result={'scope':'native component on synthetic exported-shape inputs' if component_only else 'native component on supplied frozen-feature export',
        'original_hse_and_reference_encoder_executed':False,
        'native_model_source':inspect.getfile(LLapDiff),'native_loss_source':inspect.getfile(diffusion_loss),
        'actual_native_config':config,'comparisons':24,'batch_rows':len(rows),
        'max_absolute_loss_difference':max(r['absolute_loss_difference'] for r in rows),
        'auxiliary_trunk_gradient_l1':aux_grad,'ordinary_code_changed':code_change,
        'message_scope':'dense global summary; no reused patch padding mask',
        'extra_cond_summary_raw':False,'effects':effects,'model_advantage_tested':False}
    (output/'native_check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--component-smoke',action='store_true');group.add_argument('--batch',type=Path)
    parser.add_argument('--data-note',type=Path);parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    if args.component_smoke:
        from .fit_moment_probe import generate
        data=generate(4,41);torch.manual_seed(43)
        data['z0']=torch.randn(4,8,2);data['query_time_s']=torch.arange(8).float()[None].repeat(4,1)*.01
        data['target_mask']=torch.ones(4,8,dtype=torch.bool);data['target_mask'][1,3:5]=False
        data['targets']=data['z0'][:,0,:].clone()
        data['attention_mask'][:,0]=False
    else:
        if args.data_note is None or not args.data_note.is_file():
            parser.error('a real export requires --data-note with HSE, target and split provenance')
        data=load_features(args.batch,native=True)
        if len(data['tokens'])<4:
            parser.error('native comparison requires at least four events')
    check_native(data,args.output_dir,args.component_smoke)

if __name__=='__main__':
    main()
