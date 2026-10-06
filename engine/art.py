# -*- coding: utf-8 -*-
"""Canonical Zul artwork.

`art/zul-sheet.jpg` and `art/zul-face.jpg` are the supplied originals and are
the character. Everything else — the vector rig in zul.py, the cut-out parts —
is secondary and must match these, never the other way round.

Place a figure by name and it is scaled and positioned from its measured crop
box, so no composition has to hard-code pixel offsets:

    from art import zul_art
    svg += zul_art('face',  x=60,  y=28, h=680)      # left panel of a thumbnail
    svg += zul_art('front', x=120, y=80, h=900)      # full figure in a scene
"""
import base64, io, json, os

_HERE = os.path.dirname(os.path.abspath(__file__))
_MAN = json.load(open(os.path.join(_HERE, 'art', 'manifest.json')))
_CACHE = {}

# figure name -> source file
WHERE = {'front': 'zul-sheet.jpg', 'three_quarter': 'zul-sheet.jpg',
         'back': 'zul-sheet.jpg', 'face': 'zul-face.jpg'}

def _b64(fname):
    if fname not in _CACHE:
        with open(os.path.join(_HERE, 'art', fname), 'rb') as f:
            _CACHE[fname] = base64.b64encode(f.read()).decode()
    return _CACHE[fname]

def box(figure):
    """The measured crop box for a named figure."""
    fname = WHERE[figure]
    return _MAN[fname]['figures'][figure], _MAN[fname]

def zul_art(figure, x, y, h=None, w=None, clip_id=None):
    """Place a canonical figure with its top-left at (x, y), sized to h or w.

    The whole source image is drawn, scaled, and offset so the figure's crop
    box lands where asked; a clip keeps the rest of the sheet out of frame.
    That is why swapping in a redrawn sheet only needs the manifest updated.
    """
    if figure not in WHERE:
        raise KeyError('unknown figure %r; have %s' % (figure, sorted(WHERE)))
    b, meta = box(figure)
    if h is None and w is None:
        raise ValueError('give h or w')
    k = (h / float(b['h'])) if h else (w / float(b['w']))
    cw, ch = b['w'] * k, b['h'] * k
    cid = clip_id or ('zc%s%d%d' % (figure[:2], x, y))
    return ('<defs><clipPath id="%s"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>'
            '</clipPath></defs>'
            '<g clip-path="url(#%s)"><image href="data:image/jpeg;base64,%s" '
            'x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></g>'
            % (cid, x, y, cw, ch, cid, _b64(WHERE[figure]),
               x - b['x'] * k, y - b['y'] * k, meta['w'] * k, meta['h'] * k))
