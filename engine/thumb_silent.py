# -*- coding: utf-8 -*-
"""16:9 thumbnail — "Are we in a silent depression?"

Uses the SUPPLIED artwork (art/zul-supplied.jpg), not the generated rig.
The source is 1376x768 with the figure sitting at x 506-869, y 104-680
(measured, not estimated — see bounds.js). It is scaled and offset so that
content block lands in the left panel, and clipped so the artwork's own white
background cannot bleed into the type.

    python3 thumb_silent.py && node shoot_at.js thumbsd 1280 720
"""
import base64, io, os
from prims import t
from zul import K, W, R

os.makedirs('thumbsd', exist_ok=True)
SRC = 'art/zul-supplied.jpg'
SW, SH = 1376, 768                 # source size
BX, BY, BW, BH = 506, 104, 363, 576   # measured content box

PANEL = 544                        # artwork panel width
PAD_T, PAD_B = 28, 16
TX = 586                           # type left margin

B64 = base64.b64encode(open(SRC, 'rb').read()).decode()

def art_layer():
    """Scale the content box to the panel height, then offset it into place."""
    target_h = 720 - PAD_T - PAD_B
    k = target_h / float(BH)
    draw_w, draw_h = SW * k, SH * k
    x = (PANEL - BW * k) / 2.0 - BX * k      # centre the content in the panel
    y = PAD_T - BY * k
    return ('<defs><clipPath id="cp"><rect x="0" y="0" width="%d" height="720"/></clipPath></defs>'
            '<g clip-path="url(#cp)">'
            '<image href="data:image/jpeg;base64,%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>'
            '</g>' % (PANEL, B64, x, y, draw_w, draw_h))

def build(headline, fname):
    b = ['<rect width="1280" height="720" fill="%s"/>' % W, art_layer()]
    b.append('<path d="M %d 474 L 726 474 L 726 520 L 866 520 L 866 564 '
             'L 1006 564 L 1006 610 L 1206 610" fill="none" stroke="%s" '
             'stroke-width="15" stroke-linejoin="round" stroke-linecap="round"/>' % (TX, R))
    for i, line in enumerate(headline):
        b.append(t(TX, 258 + i * 116, line, 92, anchor='start'))
    b.append('<rect x="%d" y="652" width="424" height="46" fill="%s"/>' % (TX, K))
    b.append(t(TX + 15, 686, 'THE METICULOUS INVESTOR', 27, anchor='start', fill=W))
    svg = ('<style>*{margin:0;padding:0}html,body{background:#fff}svg{display:block}</style>'
           '<svg width="1280" height="720" viewBox="0 0 1280 720" '
           'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
           + ''.join(b) + '</svg>')
    io.open('thumbsd/%s.html' % fname, 'w', encoding='utf-8').write(svg)

build(['SILENT', 'DEPRESSION?'], 'a-question')
build(['THE SILENT', 'DEPRESSION'], 'b-declarative')
print('2 variants from supplied art')
