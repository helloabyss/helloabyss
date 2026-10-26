#!/usr/bin/env python3
"""Turn a design table + measured cuts into a validated beats.json.

Shared because three videos now need the same thing. Splits any VO beat that
breaches the 2.0s hard limit into punch-ins, and gives each reuse of a plate a
different in-point so the same two seconds never repeat.
"""
import json, math, io, os

HARD, TARGET = 2.0, 1.8


def build(outdir, designs, notice=None, host=None, dur=None):
    cuts = json.load(open(os.path.join(outdir, 'cuts.json')))['cuts']
    # Use the real audio length, not the last word: a read ends with trailing
    # silence and a beat sheet that stops at the last word leaves the tail bare.
    if dur is None:
        dur = max(w['t1'] for w in json.load(open(os.path.join(outdir, 'captions.json')))['words']) + 0.08

    paras = [p.strip() for p in io.open(os.path.join(outdir, 'VO-FINAL.txt'),
                                        encoding='utf-8').read().split('\n\n') if p.strip()]
    assert len(designs) == len(paras), '%d designs for %d beats' % (len(designs), len(paras))
    cuts = list(cuts) + [round(dur, 3)]
    beats, used, poses = [], {}, []
    for i, d in enumerate(designs):
        t0, t1 = cuts[i], cuts[i + 1]
        n = math.ceil((t1 - t0) / TARGET) if (t1 - t0) > HARD else 1
        step = (t1 - t0) / n
        if 'zul' in d:
            poses.append([round(t0, 3), d['zul']])
        for j in range(n):
            b = dict(t0=round(t0 + j * step, 3), t1=round(t0 + (j + 1) * step, 3),
                     plate=d['plate'] + '.webm', heroY=d.get('heroY', 430),
                     heroSize=d.get('size', 220),
                     move=d['move'] if j == 0 else ('push' if d['move'] != 'push' else 'pull'),
                     trans=d.get('trans', 'whip') if j == n - 1 else 'whip')
            for k in ('sub', 'hero', 'note', 'mid'):
                if k in d:
                    b[k] = d[k]
            if d.get('red'):
                b['red'] = True
            if d.get('flash') and j == 0:
                b['flash'] = True
            if 'count' in d:
                c = dict(d['count'])
                b['count'] = {'from': c['from'], 'to': c['to'], 'suf': c.get('suf', ''),
                              'pre': c.get('pre', ''), 'div': c.get('div', 1)}
            b['pt0'] = round((used.get(d['plate'], 0) * 1.7) % 4.0, 2)
            used[d['plate']] = used.get(d['plate'], 0) + 1
            beats.append(b)
    out = {'beats': beats}
    if notice:
        out['notice'] = notice
    if host and poses:
        out['host'] = dict(host, poses=poses)
    json.dump(out, open(os.path.join(outdir, 'beats.json'), 'w'), indent=1)
    ds = [b['t1'] - b['t0'] for b in beats]
    print('%s: %d VO beats -> %d shots, %.2fs, %.2f-%.2fs (mean %.2f)'
          % (outdir, len(designs), len(beats), beats[-1]['t1'], min(ds), max(ds), sum(ds) / len(ds)))
