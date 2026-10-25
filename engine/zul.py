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
LENS = '#ffffff'  # clear. Sheet 2026-10-06: black Wayfarer, lenses not tinted

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
# Coils start BELOW the beanie brim. Pushed any higher they climb over the
# red crown and the hat stops reading as three bands.
_CURLS_SIDE = [(-46.5, -13.0), (-49.8, -2.0), (-50.2, 9.5), (-47.6, 20.0),
               (-42.4, 29.5), (-34.5, 36.8)]

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

def _face(view, mood, glasses, mouth=None):
    if view == 'back':
        return ''
    dx = 9 if view == 'three_quarter' else 0      # features shift toward camera
    g = []
    if glasses:
        g.append('<g stroke="%s" stroke-width="7" stroke-linejoin="round">' % K)
        if view == 'three_quarter':
            g.append('<rect x="%d" y="-13" width="32" height="26" rx="6" fill="%s"/>' % (-39 + dx, LENS))
            g.append('<rect x="%d" y="-13" width="36" height="26" rx="6" fill="%s"/>' % (-2 + dx, LENS))
            g.append('<line x1="%d" y1="0" x2="%d" y2="0"/>' % (-8 + dx, -2 + dx))
            g.append('<line x1="%d" y1="-6" x2="-45" y2="-8"/>' % (-38 + dx))
        else:
            g.append('<rect x="-43" y="-13" width="39" height="26" rx="6" fill="%s"/>' % LENS)
            g.append('<rect x="4" y="-13" width="39" height="26" rx="6" fill="%s"/>' % LENS)
            g.append('<line x1="-4" y1="-4" x2="4" y2="-4"/>')
            g.append('<line x1="-43" y1="-8" x2="-50" y2="-10"/><line x1="43" y1="-8" x2="50" y2="-10"/>')
        g.append('</g>')
    g.append('<circle cx="%d" cy="0" r="5" fill="%s"/>' % (-22 + dx, K))
    g.append('<circle cx="%d" cy="0" r="5" fill="%s"/>' % ((12 if view == 'three_quarter' else 22) + dx, K))
    if mouth is None:
        m = _MOUTHS.get(mood, _MOUTHS['neutral'])
    else:
        # Driven mouth for lip-flap: 0 is the flat neutral line, 1 is the open
        # lens. Interpolating the control points keeps the line weight and the
        # corner positions identical to the hand-drawn mouths.
        o = max(0.0, min(1.0, mouth))
        # Narrow. A mouth spanning the full ±13 of the 'talking' pose reads as a
        # grin at thumbnail scale, not as speech.
        w = 8.0 + 1.5 * o
        top, bot = 22.0, 22.0 + 8.5 * o
        m = 'M %.1f %.1f Q 0 %.1f %.1f %.1f Q 0 %.1f %.1f %.1f' % (
            -w, top, bot, w, top, top - 3.2 * o, -w, top)
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
_SIL_FRONT = ('M -34 104 L -62 126 L -53 155 L -42 147 L -41 246 '
              'L 41 246 L 42 147 L 53 155 L 62 126 L 34 104 Z')
_SIL_34    = ('M -29 104 L -55 126 L -47 155 L -37 147 L -37 246 '
              'L 39 246 L 39 147 L 49 155 L 57 126 L 31 104 Z')

def _body(view, arms, legs, arm_xy=None):
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
        out.append('<path d="M %d 103 L %d 108 L %d 141 Z" fill="%s" stroke="%s" '
                   'stroke-width="%d" stroke-linejoin="round"/>'
                   % (-6 + c, -31 + c, -2 + c, W, K, LW_FINE))
        out.append('<path d="M %d 103 L %d 108 L %d 141 Z" fill="%s" stroke="%s" '
                   'stroke-width="%d" stroke-linejoin="round"/>'
                   % (6 + c, 31 + c, 2 + c, W, K, LW_FINE))
        out.append('<line x1="%d" y1="141" x2="%d" y2="176" stroke="%s" stroke-width="%d" '
                   'stroke-linecap="round"/>' % (c, c, K, LW_FINE - 1))
        # Buttons sit ON the placket line, as drawn on the sheet.
        out.append('<circle cx="%d" cy="152" r="3.4" fill="%s" stroke="%s" stroke-width="3"/>' % (c, W, K))
        out.append('<circle cx="%d" cy="168" r="3.4" fill="%s" stroke="%s" stroke-width="3"/>' % (c, W, K))
    pair = arm_xy if arm_xy is not None else _ARMS.get(arms)
    if pair:
        (lx1, ly1, lx2, ly2), (rx1, ry1, rx2, ry2) = pair
        for (x1, y1, x2, y2, f) in ((lx1, ly1, lx2, ly2, -1), (rx1, ry1, rx2, ry2, 1)):
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%d" stroke-linecap="round"/>'
                       % (x1, y1, x2, y2, K, LW))
            out.append(_hand(x2, y2, f))
    if legs:
        out.append('<g stroke="%s" stroke-width="%d" stroke-linecap="round" fill="none">'
                   '<path d="M -20 244 L -22 394 L -36 399"/>'
                   '<path d="M 20 244 L 22 394 L 36 399"/></g>' % (K, LW))
    return ''.join(out)


def zul(x, y, sc=1.0, arms='down', view='front', mood='neutral',
        glasses=True, legs=False, arm_xy=None, mouth=None, tilt=0.0):
    """Zul, positioned by the centre of his head.

    arms    None | 'down' | 'table' | 'up' | 'point' | 'shrug'
    view    'front' | 'three_quarter' | 'back'
    mood    'neutral' | 'worried' | 'wry' | 'talking' | 'flat'
    """
    # Head group is rotated separately from the body so a tilt reads as a neck
    # movement rather than the whole figure leaning.
    head = ('<g transform="rotate(%.2f)">'
            '<circle cx="0" cy="0" r="%d" fill="%s" stroke="%s" stroke-width="%d"/>'
            '%s%s%s</g>'
            % (tilt, HEAD_R, W, K, LW,
               _beanie(), _curls(view), _face(view, mood, glasses, mouth)))
    return ('<g transform="translate(%s,%s) scale(%s)">%s%s</g>'
            % (x, y, sc, _body(view, arms, legs, arm_xy), head))
