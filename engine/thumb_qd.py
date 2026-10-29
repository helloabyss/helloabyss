# -*- coding: utf-8 -*-
"""Thumbnail for 'The Quiet Depression'. python3 thumb_qd.py && node shoot_thumb.js thumb 1280 720"""
import io, os
from prims import page, t
from zul import zul, R, K, W

os.makedirs('thumb', exist_ok=True)
b = []
TX = 596                      # text + graphic left margin

# Descending step line — the thesis of the video, in the one accent colour.
b.append('<path d="M %d 462 L 736 462 L 736 510 L 876 510 L 876 556 '
         'L 1016 556 L 1016 604 L 1212 604" fill="none" stroke="%s" '
         'stroke-width="15" stroke-linejoin="round" stroke-linecap="round"/>' % (TX, R))

# Zul, cropped at the shoulders by the bottom edge.
b.append(zul(330, 286, 2.85, None, mood='worried'))

b.append(t(TX, 258, 'THE QUIET', 98, anchor='start'))
b.append(t(TX, 374, 'DEPRESSION', 98, anchor='start'))
b.append('<rect x="%d" y="648" width="262" height="46" fill="%s"/>' % (TX, K))
b.append(t(TX + 14, 682, 'PARADOCS10X', 28, anchor='start', fill=W))

io.open('thumb/qd.html', 'w', encoding='utf-8').write(page(''.join(b), 1280, 720))
print('thumb/qd.html')
