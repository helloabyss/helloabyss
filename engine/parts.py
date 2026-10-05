# -*- coding: utf-8 -*-
"""Part templates for the cut-out rig.

Each part is a transparent PNG on a FIXED canvas with a FIXED pivot. That is
the whole trick: hand-drawn art only animates cleanly if every redraw lands in
the same place, so the canvas size and pivot are the contract. Redraw the
artwork in Procreate at the same pixel dimensions and the rig keeps working.

    python3 parts.py && node shoot_alpha.js parts
"""
import io, os, json
from zul import (HEAD_PATH, _beanie, _curls, _beard, _face, _body, _hand,
                 K, W, LW, LW_FINE)

# name -> (canvas w, h, pivot x, y, local-origin x, y)
SPEC = {
    'head':  (300, 300, 150, 196, 150, 150),   # pivot = base of skull
    'torso': (380, 200, 190,  14, 190, -90),   # pivot = neck joint at top
    'arm':   (110, 210,  55,  22,  55,  22),   # pivot = shoulder end
    'leg':   (110, 250,  55,  18,  55,  18),
}

def _wrap(name, inner):
    w, h, px, py, ox, oy = SPEC[name]
    return ('<style>*{margin:0;padding:0}html,body{background:transparent}'
            'svg{display:block}</style>'
            f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            'xmlns="http://www.w3.org/2000/svg">'
            f'<g transform="translate({ox},{oy})">{inner}</g></svg>')

def head_svg(beanie=False, glasses=False, beard=True, mood='neutral'):
    return (f'<path d="{HEAD_PATH}" fill="{W}" stroke="{K}" stroke-width="{LW}" '
            'stroke-linejoin="round"/>'
            + (_beanie() if beanie else '')
            + _curls('front', beanie)
            + (_beard() if beard else '')
            + _face('front', mood, glasses))

def torso_svg():
    # Body without arms or legs — those are their own parts.
    return _body('front', None, False)

def arm_svg():
    return (f'<line x1="0" y1="0" x2="0" y2="150" stroke="{K}" stroke-width="{LW}" '
            'stroke-linecap="round"/>' + _hand(0, 150, 1))

def leg_svg():
    return (f'<path d="M 0 0 L 2 150 L -12 156" fill="none" stroke="{K}" '
            f'stroke-width="{LW}" stroke-linecap="round" stroke-linejoin="round"/>')

if __name__ == '__main__':
    os.makedirs('parts', exist_ok=True)
    build = {'head': head_svg(), 'torso': torso_svg(), 'arm': arm_svg(), 'leg': leg_svg()}
    man = {}
    for name, inner in build.items():
        io.open(f'parts/{name}.html', 'w', encoding='utf-8').write(_wrap(name, inner))
        w, h, px, py, ox, oy = SPEC[name]
        # pivot_local is the pivot in ZUL's own coordinate space, which is what
        # the rig assembles against. Canvas pixels differ per part; local does not.
        man[name] = {'file': f'{name}.png', 'w': w, 'h': h, 'pivot': [px, py],
                     'pivot_local': [px - ox, py - oy]}
    io.open('parts/manifest.json', 'w', encoding='utf-8').write(json.dumps(man, indent=1))
    print('%d part templates -> parts/' % len(build))
