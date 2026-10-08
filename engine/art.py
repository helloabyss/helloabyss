# -*- coding: utf-8 -*-
"""Canonical Zul artwork — the official pose library.

`art/zul-*.jpg` are the supplied sheets and they ARE the character. Everything
generated (zul.py, the old cut-out parts) is secondary and must match them.

`extract_poses.js` cuts every named pose off the sheets into `art/poses/`,
keyed to transparency. Panels are kept at their full uniform size because the
sheets are drawn at one crop and scale: the poses are registered to each
other, so swapping one for another is a clean cut rather than a jump. Do not
trim them.

    from art import zul_pose, POSES
    svg += zul_pose('body', 'full-point-right', x=120, y=80, h=900)
    svg += zul_pose('glasses', 'skeptical',     x=60,  y=28, h=676)

Sets:
  glasses  bust, Meta Ray-Ban black Wayfarer   9 poses
  plain    bust, no glasses                    9 poses
  body     full figure + turnaround           12 poses
"""
import base64, io, json, os

_HERE = os.path.dirname(os.path.abspath(__file__))
_M = json.load(open(os.path.join(_HERE, 'art', 'poses', 'manifest.json')))
_CACHE = {}

POSES = {s: sorted(_M[s]['poses']) for s in _M}

# Legacy names used before the pose library existed, mapped onto it so older
# callers keep working and silently pick up the latest art.
_LEGACY = {
    'front':         ('body', 'body-front'),
    'three_quarter': ('body', 'body-3q-right'),
    'back':          ('body', 'body-back'),
    'face':          ('plain', 'official'),
}

def _b64(rel):
    if rel not in _CACHE:
        with open(os.path.join(_HERE, 'art', 'poses', rel), 'rb') as f:
            _CACHE[rel] = base64.b64encode(f.read()).decode()
    return _CACHE[rel]

def pose_box(pset, name):
    if pset not in _M:
        raise KeyError('no set %r; have %s' % (pset, sorted(_M)))
    if name not in _M[pset]['poses']:
        raise KeyError('no pose %r in %r; have %s' % (name, pset, POSES[pset]))
    return _M[pset]['poses'][name]

def zul_pose(pset, name, x, y, h=None, w=None):
    """Place a named pose with its PANEL's top-left at (x, y), sized to h or w.

    Sizing by the panel rather than by the ink keeps every pose in register —
    size by ink and the figure jumps between cuts.
    """
    m = pose_box(pset, name)
    if h is None and w is None:
        raise ValueError('give h or w')
    k = (h / float(m['h'])) if h else (w / float(m['w']))
    return ('<image href="data:image/png;base64,%s" x="%.1f" y="%.1f" '
            'width="%.1f" height="%.1f"/>'
            % (_b64(m['file']), x, y, m['w'] * k, m['h'] * k))

def zul_art(figure, x, y, h=None, w=None, clip_id=None):
    """Legacy entry point. Resolves old figure names onto the pose library."""
    if figure in _LEGACY:
        return zul_pose(*_LEGACY[figure], x=x, y=y, h=h, w=w)
    raise KeyError('unknown figure %r; use zul_pose() — sets %s'
                   % (figure, {s: POSES[s] for s in POSES}))
