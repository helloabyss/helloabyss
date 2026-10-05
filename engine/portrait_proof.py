# -*- coding: utf-8 -*-
"""9:16 layout proof for the ONE NUMBER series. The engine is composed for
1920x1080; this checks the primitives reframe to 1080x1920 before anyone plans
a series on the assumption that they do.

Deliberately carries no financial figure. The number shown is 2.6 words/second,
which is measured from this channel's own scripts in STYLE-GUIDE.md SS5A — the
one number on hand that is verified in-repo and is not a market claim.
"""
import io, os
from prims import page, t
from zul import zul, K, W, R

os.makedirs('portrait', exist_ok=True)
Wd, Ht = 1080, 1920
b = []

b.append(t(540, 92, 'LAYOUT PROOF — NOT AN EPISODE', 30, fill='#8a8a8a'))

# HOOK — 13 words, the SS5A ceiling, set as it would really appear.
hook = ['Two point six words', 'a second. That is what', 'five seconds actually', 'buys you.']
for i, line in enumerate(hook):
    b.append(t(70, 236 + i * 82, line, 66, anchor='start'))

# The number, set as the series' main visual device.
b.append(t(540, 780, '2.6', 280))
b.append('<line x1="310" y1="828" x2="770" y2="828" stroke="%s" stroke-width="12"/>' % R)
b.append(t(540, 898, 'WORDS PER SECOND', 44))

b.append(zul(540, 1180, 2.3, 'point', mood='talking', beanie=False, glasses=False))

# Compliance as a thin bottom-edge strip — never a full card (SS5A: it would eat the hook).
b.append('<rect x="0" y="1838" width="%d" height="82" fill="%s"/>' % (Wd, K))
b.append(t(540, 1892, 'EDUCATIONAL ONLY. NOT FINANCIAL ADVICE.', 36, fill=W))

io.open('portrait/proof.html', 'w', encoding='utf-8').write(page(''.join(b), Wd, Ht))
print('portrait/proof.html')
