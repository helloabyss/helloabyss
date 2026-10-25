# -*- coding: utf-8 -*-
"""Thumbnail for the Agents' Last Exam short. 1080x1920, channel palette.

The whole claim is the two numbers and the fact that they belong to the SAME
model, so the thumbnail is those three things and nothing else. No arrow
clutter, no shock face. Checked downscaled to 180px wide.
"""
import io
from prims import page, t, K, W, R
from zul import zul

CW = 1080
body = (
    t(CW // 2, 250, 'SAME AI MODEL', 74, weight=800)
    + f'<line x1="240" y1="300" x2="840" y2="300" stroke="{K}" stroke-width="12"/>'
    + t(CW // 2, 640, '82%', 330, weight=800)
    + t(CW // 2, 730, 'ON THE BENCHMARK', 62)
    + t(CW // 2, 880, '▼', 90, fill=R)
    + t(CW // 2, 1220, '25%', 330, fill=R, weight=800)
    + t(CW // 2, 1310, 'ON REAL WORK', 62, fill=R)
    + f'<line x1="240" y1="1400" x2="840" y2="1400" stroke="{K}" stroke-width="12"/>'
    + t(CW // 2, 1500, 'BERKELEY TESTED IT', 58, weight=800)
    + t(CW // 2, 1570, 'ON 1,400 REAL JOBS', 58, weight=800)
    + zul(880, 1660, 0.72, arms='down', view='three_quarter', mood='wry')
)
io.open('thumb-ale.html', 'w', encoding='utf-8').write(page(body, CW, 1920))
print('thumb-ale.html written')
