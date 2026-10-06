# -*- coding: utf-8 -*-
"""16:9 thumbnail — "Are we in a silent depression?"

Uses the CANONICAL artwork via art.zul_art. Crop and placement come from
art/manifest.json, so a redrawn sheet needs no change here.

    python3 thumb_silent.py && node shoot_at.js thumbsd 1280 720
"""
import io, os
from prims import t
from art import zul_art
from zul import K, W, R

os.makedirs('thumbsd', exist_ok=True)
TX = 586          # type left margin

def build(headline, fname):
    b = ['<rect width="1280" height="720" fill="%s"/>' % W,
         zul_art('face', x=58, y=28, h=676, clip_id='th' + fname[:1])]
    b.append('<path d="M %d 474 L 726 474 L 726 520 L 866 520 L 866 564 '
             'L 1006 564 L 1006 610 L 1206 610" fill="none" stroke="%s" '
             'stroke-width="15" stroke-linejoin="round" stroke-linecap="round"/>' % (TX, R))
    for i, line in enumerate(headline):
        b.append(t(TX, 258 + i * 116, line, 92, anchor='start'))
    b.append('<rect x="%d" y="652" width="424" height="46" fill="%s"/>' % (TX, K))
    b.append(t(TX + 15, 686, 'THE METICULOUS INVESTOR', 27, anchor='start', fill=W))
    io.open('thumbsd/%s.html' % fname, 'w', encoding='utf-8').write(
        '<meta charset="utf-8">'
        '<style>*{margin:0;padding:0}html,body{background:#fff}svg{display:block}</style>'
        '<svg width="1280" height="720" viewBox="0 0 1280 720" '
        'xmlns="http://www.w3.org/2000/svg">' + ''.join(b) + '</svg>')

build(['SILENT', 'DEPRESSION?'], 'a-question')
build(['THE SILENT', 'DEPRESSION'], 'b-declarative')
print('2 variants from canonical art')
