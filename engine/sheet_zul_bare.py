# -*- coding: utf-8 -*-
"""Zul, bare-headed variant: no beanie, no glasses.
   python3 sheet_zul_bare.py && node shoot.js zulbare"""
import io, os
from prims import page, t
from zul import zul

os.makedirs('zulbare', exist_ok=True)
BARE = dict(beanie=False, glasses=False)

p1 = [t(960, 68, 'ZUL — BARE-HEADED VARIANT', 46),
      t(960, 106, 'no beanie, no glasses. same rig, same proportions.', 24, weight=400)]
for i, (vw, lbl) in enumerate((('front', 'FRONT'), ('three_quarter', 'THREE-QUARTER'), ('back', 'BACK'))):
    cx = 330 + i * 430
    p1.append(zul(cx, 230, 0.78, 'down', view=vw, legs=True, **BARE))
    p1.append(t(cx, 600, lbl, 24))
p1.append(zul(1660, 230, 0.78, 'down', view='front', legs=True, beanie=False, glasses=True))
p1.append(t(1660, 600, 'GLASSES ON (for reference)', 24))
p1.append('<line x1="80" y1="640" x2="1840" y2="640" stroke="#000" stroke-width="3"/>')
for i, a in enumerate(('down', 'table', 'up', 'point', 'shrug')):
    cx = 250 + i * 355
    p1.append(zul(cx, 760, 0.70, a, **BARE))
    p1.append(t(cx, 1040, a.upper(), 22))

p2 = [t(960, 68, 'ZUL — BARE-HEADED EXPRESSIONS', 46)]
for i, m in enumerate(('neutral', 'worried', 'wry', 'talking', 'flat')):
    cx = 250 + i * 355
    p2.append(zul(cx, 300, 1.35, None, mood=m, **BARE))
    p2.append(t(cx, 560, m.upper(), 24))
p2.append('<line x1="80" y1="620" x2="1840" y2="620" stroke="#000" stroke-width="3"/>')
p2.append(t(960, 690, 'SCALE — positioned by the CENTRE OF HIS HEAD, not his feet', 26))
for i, sc in enumerate((0.6, 0.85, 1.1, 1.4)):
    cx = 330 + i * 430
    p2.append(zul(cx, 760, sc * 0.62, 'down', legs=True, **BARE))
    p2.append(t(cx, 1050, 'sc=%s' % sc, 22))

io.open('zulbare/01.html', 'w', encoding='utf-8').write(page(''.join(p1)))
io.open('zulbare/02.html', 'w', encoding='utf-8').write(page(''.join(p2)))
print('2 sheets')
