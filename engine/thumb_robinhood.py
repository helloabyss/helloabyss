# -*- coding: utf-8 -*-
"""Thumbnail for the Robinhood agentic-trading tutorial. 1280x720, channel palette.

Both halves of the claim are in FACTS.md: an agent can place real trades, and
Robinhood states it does not supervise third-party agents. No arrow, no circle,
no shock face. Checked downscaled to 320px, which is roughly sidebar size.
"""
import io
from prims import *

W2, H2 = 1280, 720
X = 470                      # type column, clear of Zul
body = (
    zul(230, 330, 1.25, arms='point', view='front', mood='neutral')
    + t(X, 120, 'AN AI CAN TRADE', 68, anchor='start')
    + t(X, 196, 'YOUR ACCOUNT', 68, anchor='start')
    + f'<line x1="{X}" y1="236" x2="1200" y2="236" stroke="{R}" stroke-width="11"/>'
    + t(X, 326, 'NOBODY IS', 72, anchor='start', fill=R)
    + t(X, 406, 'WATCHING', 72, anchor='start', fill=R)
    + toggle(X, 466, False, 132, 64)
    + t(X + 156, 512, 'ONE TOGGLE DECIDES', 36, anchor='start')
    + t(X, 612, 'ROBINHOOD  ·  AGENTIC TRADING', 30, anchor='start', fill=D)
)
io.open('thumb-robinhood.html', 'w', encoding='utf-8').write(page(body, W2, H2))
print('ok')
