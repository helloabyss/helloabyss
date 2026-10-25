# -*- coding: utf-8 -*-
"""Zul from the owner's model sheets, not re-derived in code.

`zul.py` draws him from scratch and is still what the stickman scene engine
uses. For composites over footage the artwork itself is the asset: these are
the sheet cells, cut to transparent PNGs by `extract_zul.py`.

When the two disagree the sheet wins, so prefer these for anything the viewer
will actually see.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, 'zulsheet')
INDEX = json.load(open(os.path.join(DIR, 'poses.json')))

# Reference measurement: the corner host occupies ~22% of frame height.
CORNER_FRAC = 0.22


def path(name):
    if name not in INDEX:
        raise KeyError('no pose %r. have: %s' % (name, ', '.join(sorted(INDEX))))
    return os.path.join(DIR, INDEX[name]['file'].split('/')[-1] and INDEX[name]['file'])


def size(name):
    e = INDEX[name]
    return e['w'], e['h']


def place(name, frame_h=1920, frac=CORNER_FRAC):
    """Pixel height and width for a pose at a given share of frame height."""
    w, h = size(name)
    ph = frame_h * frac
    return int(round(w * ph / h)), int(round(ph))


def img_tag(name, x, y, frame_h=1920, frac=CORNER_FRAC, anchor='bottom-left', extra=''):
    """An <img> for the HTML compositor, positioned by a corner."""
    w, h = place(name, frame_h, frac)
    left = x if 'left' in anchor else x - w
    top = y - h if 'bottom' in anchor else y
    src = 'file://' + os.path.join(DIR, 'poses', name + '.png')
    return ('<img class="zul" src="%s" style="position:absolute;left:%dpx;top:%dpx;'
            'width:%dpx;height:%dpx;%s">' % (src, left, top, w, h, extra))


def names():
    return sorted(INDEX)
