# -*- coding: utf-8 -*-
"""Renders the Zul model sheet. python3 sheet_zul.py && node shoot.js zulsheet"""
import io, os
from prims import page, t
from zul import zul

os.makedirs('zulsheet', exist_ok=True)

p1 = []
p1.append(t(960, 70, 'ZUL — MODEL SHEET', 46))
p1.append(t(960, 108, 'locked design. views and poses.', 24, weight=400))
for i, (vw, lbl) in enumerate((('front', 'FRONT'), ('three_quarter', 'THREE-QUARTER'), ('back', 'BACK'))):
    cx = 330 + i * 430
    p1.append(zul(cx, 230, 0.78, 'down', view=vw, legs=True))
    p1.append(t(cx, 600, lbl, 24))
p1.append(zul(1660, 230, 0.78, 'down', glasses=False, legs=True))
p1.append(t(1660, 600, 'NO GLASSES (variant)', 24))
p1.append('<line x1="80" y1="640" x2="1840" y2="640" stroke="#000" stroke-width="3"/>')
for i, a in enumerate(('down', 'table', 'up', 'point', 'shrug')):
    cx = 250 + i * 355
    p1.append(zul(cx, 760, 0.70, a))
    p1.append(t(cx, 1040, a.upper(), 22))

p2 = []
p2.append(t(960, 70, 'ZUL — EXPRESSIONS', 46))
for i, m in enumerate(('neutral', 'worried', 'wry', 'talking', 'flat')):
    cx = 250 + i * 355
    p2.append(zul(cx, 300, 1.35, None))
    p2.append(t(cx, 560, m.upper(), 24))
p2 = [p2[0]] + [x for x in p2[1:]]
# redo with moods actually applied
p2 = [t(960, 70, 'ZUL — EXPRESSIONS', 46)]
for i, m in enumerate(('neutral', 'worried', 'wry', 'talking', 'flat')):
    cx = 250 + i * 355
    p2.append(zul(cx, 300, 1.35, None, mood=m))
    p2.append(t(cx, 560, m.upper(), 24))
p2.append('<line x1="80" y1="620" x2="1840" y2="620" stroke="#000" stroke-width="3"/>')
p2.append(t(960, 690, 'SCALE — he is positioned by the CENTRE OF HIS HEAD, not his feet', 26))
for i, s in enumerate((0.6, 0.85, 1.1, 1.4)):
    cx = 330 + i * 430
    p2.append(zul(cx, 760, s*0.62, 'down', legs=True))
    p2.append(t(cx, 1050, 'sc=%s' % s, 22))

io.open('zulsheet/01.html', 'w', encoding='utf-8').write(page(''.join(p1)))
io.open('zulsheet/02.html', 'w', encoding='utf-8').write(page(''.join(p2)))
print('2 sheets')
