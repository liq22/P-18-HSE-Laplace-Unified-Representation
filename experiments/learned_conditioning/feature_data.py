"""Explicit frozen-feature inputs. No implicit all-valid or missing-metadata path."""
from pathlib import Path
import numpy as np
import torch


def load_features(path, native=False):
    with np.load(Path(path), allow_pickle=False) as f:
        required = ['tokens', 'attention_mask', 'side', 'targets',
                    'event_id', 'group_id', 'condition_id', 'side_names']
        if native:
            required += ['z0', 'target_mask', 'query_time_s', 'target_map']
        missing = [key for key in required if key not in f]
        if missing:
            raise ValueError(f'{path}: missing explicit fields {missing}')
        arrays = {key: f[key].copy() for key in required}
    h, mask, side, y = (arrays[key] for key in required[:4])
    n = len(h)
    if h.ndim != 3 or mask.shape != h.shape[:2] or mask.dtype != np.bool_:
        raise ValueError('expected tokens[N,K,D], attention_mask bool[N,K]')
    if n < 1 or not np.all(mask.any(1)):
        raise ValueError('empty dataset or empty history')
    if side.ndim != 2 or side.shape[0] != n or y.ndim != 2 or len(y) != n:
        raise ValueError('expected side[N,A] and targets[N,d]')
    if not all(np.isfinite(a).all() for a in [h[mask], side, y]):
        raise ValueError('nonfinite observed features or targets')
    if arrays['side_names'].shape != (side.shape[1],) or arrays['side_names'].dtype.kind not in 'US':
        raise ValueError('side_names must declare each fixed-order side column')
    for key in ['event_id', 'group_id', 'condition_id']:
        a = arrays[key]
        if a.shape != (n,) or a.dtype.kind not in 'USiu':
            raise ValueError(f'{key} must be a non-object string or integer vector')
        arrays[key] = a.astype(str)
    if len(set(zip(arrays['event_id'], arrays['condition_id']))) != n:
        raise ValueError('duplicate event/acquisition pair')
    if native:
        z, tm, t, target_map = (arrays[k] for k in ['z0', 'target_mask', 'query_time_s', 'target_map'])
        if z.ndim != 3 or len(z) != n or tm.shape != z.shape[:2] or tm.dtype != np.bool_:
            raise ValueError('expected z0[N,H,Z], target_mask bool[N,H]')
        if not tm.any(1).all() or not np.isfinite(z).all():
            raise ValueError('z0 must be finite; every event needs observed target supervision')
        if t.shape != z.shape[:2] or not np.isfinite(t).all() or np.any(np.diff(t, axis=1) < 0):
            raise ValueError('query_time_s must be finite, nondecreasing [N,H]')
        if target_map.shape != (y.shape[1], z.shape[1]*z.shape[2]):
            raise ValueError('target_map must map flattened z0 to targets')
        used = np.any(np.abs(target_map.reshape(y.shape[1], z.shape[1], z.shape[2])) > 0, axis=(0, 2))
        if not np.all(tm[:, used]):
            raise ValueError('moment target uses missing reference supervision')
        if not np.allclose(y, z.reshape(n, -1) @ target_map.T, atol=1e-5, rtol=1e-5):
            raise ValueError('targets do not equal the declared linear functional of z0')
    result = {}
    for key, a in arrays.items():
        if key.endswith('_id') or key == 'side_names':
            result[key] = a
        else:
            result[key] = torch.from_numpy(a).bool() if a.dtype == np.bool_ else torch.from_numpy(a).float()
    return result


def check_splits(*datasets):
    for i, left in enumerate(datasets):
        for right in datasets[i+1:]:
            for key in ['event_id', 'group_id']:
                if set(left[key]) & set(right[key]):
                    raise ValueError(f'original {key} crosses train/validation/test')
    first = datasets[0]
    for d in datasets[1:]:
        for key in ['tokens', 'side', 'targets']:
            if d[key].shape[1:] != first[key].shape[1:]:
                raise ValueError(f'inconsistent {key} dimensions across splits')
        if not np.array_equal(d['side_names'], first['side_names']):
            raise ValueError('side column meanings/order differ across splits')
        if 'target_map' in first:
            torch.testing.assert_close(d['target_map'], first['target_map'], rtol=0, atol=0)


def inputs(data, index=slice(None), device='cpu'):
    return tuple(data[k][index].to(device) for k in ['tokens', 'attention_mask', 'side'])
