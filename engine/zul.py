# -*- coding: utf-8 -*-
"""
ZUL — the channel's recurring host.

Locked design. Read CHARACTER-ZUL.md before changing anything in here; the
whole point of this module is that he looks identical in every video.

Geometry is defined around a head centred on (0,0) with radius 46, so a call
site positions him by his FACE, not by his feet. Everything else hangs off
that. Scale with `sc`.

    zul(960, 400)                      # bust, front, arms down
    zul(960, 300, 1.2, 'up', legs=True)
    zul(300, 400, view='three_quarter', mood='worried')
    zul(300, 400, view='back')
"""
from math import cos, sin, pi

K = '#000'      # line
W = '#fff'      # fill / paper
R = '#d81e28'   # beanie red
Y = '#f2c200'   # beanie yellow
G = '#2e9e3e'   # beanie green
LENS = '#b9c7d0'  # glass tint

HEAD_R = 46
LW     = 7      # main line weight
LW_FINE = 5     # curls, collar, small detail

_uid = [0]
def _nid(p):
    _uid[0] += 1
    return '%s%d' % (p, _uid[0])


def _curl(cx, cy, r=9.5, turns=1.55, rot=0.0, pts=26):
    """One hair coil, as an Archimedean spiral. Tight at the centre, open at
    the rim — this is what reads as 'curl' rather than 'circle' at 1080p."""
    d = []
    for i in range(pts):
        t = i / (pts - 1.0)
        ang = rot + t * turns * 2 * pi
        rad = r * (0.16 + 0.84 * t)
        d.append('%s%.1f %.1f' % ('M' if i == 0 else 'L', cx + rad * cos(ang), cy + rad * sin(ang)))
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%d" '
            'stroke-linecap="round" stroke-linejoin="round"/>' % (' '.join(d), K, LW_FINE))


# Curls sit on an arc just outside the head edge, from under the brim down to
# the cheek. Measured off the reference: each coil is ~0.14 x head radius, which
# is roughly half the size that "looks right" when guessed.
_CURL_R = 6.5
_CURLS_SIDE = [(-47.0, -17.1), (-49.7, -5.2), (-49.5, 7.0), (-46.4, 18.7), (-40.5, 29.4)]

def _curls(view):
    out = []
    if view == 'back':
        # Seen from behind the coils ring the whole brim.
        # Fringe across the brim, plus the same side coils as the front, so the
        # back of the head reads as hair rather than a dotted line.
        for i in range(7):
            x = -40 + i * 13.3
            out.append(_curl(x, -3 + 5 * cos(x / 40.0 * 1.4), 7.0, rot=0.4 * i))
        for (cx, cy) in _CURLS_SIDE[:4]:
            out.append(_curl(cx, cy, _CURL_R, rot=0.9))
            out.append(_curl(-cx, cy, _CURL_R, rot=pi - 0.9))
        return ''.join(out)
    for i, (cx, cy) in enumerate(_CURLS_SIDE):
        out.append(_curl(cx, cy, _CURL_R, rot=0.5 + 0.4 * i))
        out.append(_curl(-cx, cy, _CURL_R, rot=pi - 0.5 - 0.4 * i))   # mirrored
    if view == 'three_quarter':
        out.append(_curl(-54, -14, _CURL_R, rot=1.2))   # more hair on the far side
        out.append(_curl(-53, 26, _CURL_R, rot=2.0))
    return ''.join(out)


def _beanie():
    """Three-band knit cap. Bands are clipped to one dome so the edges stay
    crisp and the stripes follow the curve instead of sitting flat."""
    cid = _nid('bn')
    dome = 'M -51 -16 A 53 58 0 0 1 51 -16 Q 0 -4 -51 -16 Z'
    return (
        '<defs><clipPath id="%s"><path d="%s"/></clipPath></defs>'
        '<g clip-path="url(#%s)">'
        '<rect x="-60" y="-62" width="120" height="25" fill="%s"/>'      # red crown
        '<rect x="-60" y="-37" width="120" height="9" fill="%s"/>'       # yellow
        '<rect x="-60" y="-28" width="120" height="34" fill="%s"/>'      # green brim
        # Dividers live INSIDE the clip: at these heights the dome is only
        # ~41 and ~46 wide, so unclipped lines poke out as tabs at the sides.
        '<path d="M -56 -37 Q 0 -32 56 -37" fill="none" stroke="%s" stroke-width="4"/>'
        '<path d="M -56 -28 Q 0 -23 56 -28" fill="none" stroke="%s" stroke-width="4"/>'
        '</g>'
        '<path d="%s" fill="none" stroke="%s" stroke-width="%d" stroke-linejoin="round"/>'
        % (cid, dome, cid, R, Y, G, K, K, dome, K, LW))


_MOUTHS = {
    'neutral': 'M -16 23 L 16 23',
    'worried': 'M -16 27 Q 0 16 16 27',
    'wry':     'M -16 24 Q 0 29 13 19',
    'talking': 'M -13 20 Q 0 34 13 20 Q 0 27 -13 20',
    'flat':    'M -12 23 L 12 23',
}

def _face(view, mood, glasses):
    if view == 'back':
        return ''
    dx = 9 if view == 'three_quarter' else 0      # features shift toward camera
    g = []
    if glasses:
        g.append('<g stroke="%s" stroke-width="6" stroke-linejoin="round">' % K)
        if view == 'three_quarter':
            g.append('<rect x="%d" y="-12" width="30" height="24" rx="5" fill="%s"/>' % (-38 + dx, LENS))
            g.append('<rect x="%d" y="-12" width="34" height="24" rx="5" fill="%s"/>' % (-2 + dx, LENS))
            g.append('<line x1="%d" y1="0" x2="%d" y2="0"/>' % (-8 + dx, -2 + dx))
            g.append('<line x1="%d" y1="-6" x2="-45" y2="-8"/>' % (-38 + dx))
        else:
            g.append('<rect x="-40" y="-12" width="36" height="24" rx="5" fill="%s"/>' % LENS)
            g.append('<rect x="4" y="-12" width="36" height="24" rx="5" fill="%s"/>' % LENS)
            g.append('<line x1="-4" y1="0" x2="4" y2="0"/>')
            g.append('<line x1="-40" y1="-6" x2="-46" y2="-8"/><line x1="40" y1="-6" x2="46" y2="-8"/>')
        g.append('</g>')
    g.append('<circle cx="%d" cy="0" r="5" fill="%s"/>' % (-22 + dx, K))
    g.append('<circle cx="%d" cy="0" r="5" fill="%s"/>' % ((12 if view == 'three_quarter' else 22) + dx, K))
    m = _MOUTHS.get(mood, _MOUTHS['neutral'])
    if dx:
        for a in ('M -16', 'M -13', 'M -12'):
            m = m.replace(a, 'M %d' % (int(a.split()[1]) + dx))
    g.append('<path d="%s" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round"/>' % (m, K, LW))
    return ''.join(g)


def _hand(x, y, flip=1):
    """Three short strokes. Deliberately minimal — a drawn hand at this line
    weight reads as a blob, which is why earlier mitten/glove attempts failed."""
    return ('<g stroke="%s" stroke-width="%d" stroke-linecap="round" fill="none">'
            '<path d="M %.0f %.0f q %.0f 7 %.0f 12"/>'
            '<path d="M %.0f %.0f q %.0f 8 %.0f 10"/>'
            '<path d="M %.0f %.0f q %.0f 6 %.0f 7"/></g>'
            % (K, LW_FINE,
               x, y, 6 * flip, 3 * flip,
               x + 4 * flip, y - 1, 6 * flip, 1 * flip,
               x + 7 * flip, y - 3, 4 * flip, -2 * flip))


_ARMS = {
    'down':  ((-57, 152, -65, 230), (57, 152, 65, 230)),
    'table': ((-57, 150, -116, 196), (57, 150, 116, 196)),
    'up':    ((-56, 148, -102, 86),  (56, 148, 102, 86)),
    'point': ((-57, 152, -65, 230),  (56, 148, 124, 124)),
    'shrug': ((-57, 150, -98, 118),  (57, 150, 98, 118)),
}

# Shoulders y=104, hem y=244 (torso 140 = 1.5 head-diameters), feet y=400.
_SIL_FRONT = ('M -38 104 L -68 124 L -57 154 L -45 146 L -50 244 '
              'L 50 244 L 45 146 L 57 154 L 68 124 L 38 104 Z')
_SIL_34    = ('M -32 104 L -60 124 L -50 154 L -40 146 L -44 244 '
              'L 46 244 L 42 146 L 52 154 L 62 124 L 34 104 Z')

def _body(view, arms, legs):
    out = []
    out.append('<line x1="0" y1="%d" x2="0" y2="110" stroke="%s" stroke-width="%d"/>' % (HEAD_R, K, LW))
    out.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%d" stroke-linejoin="round"/>'
               % (_SIL_34 if view == 'three_quarter' else _SIL_FRONT, W, K, LW))
    if view == 'back':
        out.append('<path d="M -20 105 Q 0 117 20 105" fill="none" stroke="%s" stroke-width="%d"/>' % (K, LW_FINE))
    else:
        c = 7 if view == 'three_quarter' else 0
        # One V-shaped collar band, drawn as a single closed path. Two separate
        # flaps plus a placket converge into an unreadable dark wedge once the
        # head is scaled up for a thumbnail, so the band is drawn as one shape.
        out.append('<path d="M %d 102 L %d 143 L %d 102 L %d 102 L %d 123 L %d 102 Z" '
                   'fill="%s" stroke="%s" stroke-width="%d" stroke-linejoin="round"/>'
                   % (-32 + c, c, 32 + c, 15 + c, c, -15 + c, W, K, LW_FINE))
        out.append('<line x1="%d" y1="143" x2="%d" y2="173" stroke="%s" stroke-width="4"/>' % (c, c, K))
        out.append('<circle cx="%d" cy="152" r="3.6" fill="none" stroke="%s" stroke-width="3"/>' % (c, K))
        out.append('<circle cx="%d" cy="166" r="3.6" fill="none" stroke="%s" stroke-width="3"/>' % (c, K))
    if arms in _ARMS:
        (lx1, ly1, lx2, ly2), (rx1, ry1, rx2, ry2) = _ARMS[arms]
        for (x1, y1, x2, y2, f) in ((lx1, ly1, lx2, ly2, -1), (rx1, ry1, rx2, ry2, 1)):
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%d" stroke-linecap="round"/>'
                       % (x1, y1, x2, y2, K, LW))
            out.append(_hand(x2, y2, f))
    if legs:
        out.append('<g stroke="%s" stroke-width="%d" stroke-linecap="round" fill="none">'
                   '<path d="M -20 244 L -22 394 L -36 399"/>'
                   '<path d="M 20 244 L 22 394 L 36 399"/></g>' % (K, LW))
    return ''.join(out)


def zul(x, y, sc=1.0, arms='down', view='front', mood='neutral',
        glasses=True, legs=False):
    """Zul, positioned by the centre of his head.

    arms    None | 'down' | 'table' | 'up' | 'point' | 'shrug'
    view    'front' | 'three_quarter' | 'back'
    mood    'neutral' | 'worried' | 'wry' | 'talking' | 'flat'
    """
    return ('<g transform="translate(%s,%s) scale(%s)">'
            '<circle cx="0" cy="0" r="%d" fill="%s" stroke="%s" stroke-width="%d"/>'
            '%s%s%s%s</g>'
            % (x, y, sc, HEAD_R, W, K, LW,
               _body(view, arms, legs), _beanie(), _curls(view), _face(view, mood, glasses)))
