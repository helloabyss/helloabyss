#!/usr/bin/env python3
"""Validate a beats file before rendering.

Three defects have now shipped from eyeballing layout: a caption across Zul's
legs, a series card over his legs, and a mid-layer rule through the hero
number. Layout collisions get checked by arithmetic here, not by looking.
"""
import json, sys

BEATS = json.load(open(sys.argv[1]))['beats']
AUDIO_LEN = float(sys.argv[2])
CAP_TOP = 1395          # caption band in reel.js
MAXSHOT = 2.0           # STYLE-GUIDE: no shot past 2s
# Some VO lines are genuinely under a second ("Same agent."). That is fast
# cutting, not a fault. Below ~0.85s a frame cannot register at all.
MINSHOT = 0.85
err = []

for i, b in enumerate(BEATS, 1):
    t0, t1 = b['t0'], b['t1']
    d = t1 - t0
    if d > MAXSHOT + 1e-6:
        err.append('beat %d is %.2fs — STYLE-GUIDE allows no shot past %.1fs' % (i, d, MAXSHOT))
    if d < MINSHOT:
        err.append('beat %d is %.2fs — too short to read' % (i, d))
    if not b.get('plate'):
        err.append('beat %d has no photographic plate — imagery is the BASE layer' % i)
    # Hero vertical span, from its baseline and size.
    # #hero is positioned by its TOP with line-height .92 -- not a baseline.
    # Getting this wrong is why the validator first passed a rule drawn
    # straight through the hero number.
    hy, hs = b.get('heroY', 520), b.get('heroSize', 250)
    htop, hbot = hy, hy + hs * 0.92
    if hbot > CAP_TOP:
        err.append('beat %d hero spans to y=%d, inside the caption band (%d)' % (i, hbot, CAP_TOP))
    ss = b.get('subSize', 40)
    sy = hy - ss - 30
    if b.get('sub') and sy < 150:
        err.append('beat %d subtitle at y=%d is above the safe top margin' % (i, sy))
    ny = hy + hs * 0.92 + 26
    if b.get('note') and ny + 36 > CAP_TOP:
        err.append('beat %d note reaches y=%d, inside the caption band' % (i, ny + 36))
    g = b.get('mid')
    if g:
        gy = g['y']
        gh = {'bar': 98, 'grid': 8 * 52, 'rule': 8, 'line_series': 340}[g['type']]
        if not (gy + gh < htop or gy > hbot):
            err.append('beat %d mid-layer %s spans y=%d-%d, overlapping the hero (y=%d-%d)'
                       % (i, g['type'], gy, gy + gh, htop, hbot))
        if gy + gh > CAP_TOP:
            err.append('beat %d mid-layer %s reaches y=%d, inside the caption band'
                       % (i, g['type'], gy + gh))
    if b.get('note') and g:
        if not (g['y'] + {'bar': 98, 'grid': 8*52, 'rule': 8, 'line_series': 340}[g['type']] < ny or g['y'] > ny + 36):
            err.append('beat %d note and mid-layer %s collide at y=%d' % (i, g['type'], ny))

for i in range(len(BEATS) - 1):
    if abs(BEATS[i]['t1'] - BEATS[i + 1]['t0']) > 1e-6:
        err.append('gap or overlap between beat %d and %d' % (i + 1, i + 2))
if abs(BEATS[0]['t0']) > 1e-6:
    err.append('first beat does not start at 0')
if abs(BEATS[-1]['t1'] - AUDIO_LEN) > 0.05:
    err.append('last beat ends %.2f but audio is %.2f' % (BEATS[-1]['t1'], AUDIO_LEN))
if not any(b.get('plate') for b in BEATS):
    err.append('no plates at all')

ds = [b['t1'] - b['t0'] for b in BEATS]
print('%d beats, %.2fs, shots %.2f-%.2fs (mean %.2f)'
      % (len(BEATS), BEATS[-1]['t1'], min(ds), max(ds), sum(ds) / len(ds)))
print('plates used: %d distinct' % len({b.get('plate') for b in BEATS if b.get('plate')}))
if err:
    print('\n'.join('  FAIL ' + e for e in err))
    raise SystemExit('\n%d layout/timing problem(s).' % len(err))
print('beats OK')
