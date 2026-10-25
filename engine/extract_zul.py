#!/usr/bin/env python3
"""Cut the poses out of the owner's model sheets.

Re-deriving Zul in SVG was an approximation of artwork we already have. These
are the sheets themselves, cut to transparent PNGs and used as-is.

Background removal is a flood fill from the panel edge, NOT a white-to-alpha
threshold: his polo and face are white too, and thresholding would punch holes
straight through him.
"""
import os, sys, json
from collections import deque
from PIL import Image
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SHEETS = os.path.join(HERE, 'zulsheet')
OUT = os.path.join(SHEETS, 'poses')

NAMES = {
 'bust-kit-2026-10-06.jpg': [
   'official', 'idle-deadpan', 'point-right',
   'point-left', 'present-palm', 'shock',
   'skeptical', 'thumbs-up', 'thinking'],
 'body-profile-2026-10-06.jpg': [
   '_turnaround',
   'body-front', 'body-3q-right', 'body-3q-left', 'body-back',
   'full-point-right', 'full-point-left', 'full-present-palm', 'full-shock',
   'full-skeptical', 'full-thumbs-up', 'full-shrug'],
 'no-beanie-2026-10-06.jpg': [
   'beanie-full-front', 'nobeanie-full-front',
   'nb-body-front', 'nb-body-3q-right', 'nb-body-3q-left', 'nb-body-back',
   'nb-bust-idle', 'nb-bust-point-right', 'nb-bust-shock', 'nb-bust-skeptical'],
}


def find_cells(a, minw=120, minh=120):
    white = (a[:, :, 0] >= 248) & (a[:, :, 1] >= 248) & (a[:, :, 2] >= 248)
    H, W = white.shape
    rows = white.sum(1) > W * 0.25
    bands, s = [], None
    for y in range(H):
        if rows[y] and s is None: s = y
        elif not rows[y] and s is not None:
            if y - s >= minh: bands.append((s, y))
            s = None
    if s is not None and H - s >= minh: bands.append((s, H))
    out = []
    for (y0, y1) in bands:
        cols = white[y0:y1].sum(0) > (y1 - y0) * 0.4
        runs, s = [], None
        for x in range(W):
            if cols[x] and s is None: s = x
            elif not cols[x] and s is not None:
                runs.append((s, x)); s = None
        if s is not None: runs.append((s, W))
        # A tall figure can break one panel into slivers; rejoin them.
        merged = []
        for r in runs:
            if merged and r[0] - merged[-1][1] <= 4:
                merged[-1] = (merged[-1][0], r[1])
            else:
                merged.append(list(r) if False else (r[0], r[1]))
            merged[-1] = tuple(merged[-1])
        for (x0, x1) in merged:
            if x1 - x0 >= minw:
                out.append((x0, y0, x1, y1))
    return out


def cut(a, box, pad=3):
    x0, y0, x1, y1 = box
    sub = a[y0 + pad:y1 - pad, x0 + pad:x1 - pad]
    h, w, _ = sub.shape
    light = (sub[:, :, 0] >= 236) & (sub[:, :, 1] >= 236) & (sub[:, :, 2] >= 236)
    # Flood from the border through light pixels only: that is the ground and
    # the air around him, never the polo, which is enclosed by his outline.
    outside = np.zeros((h, w), bool)
    q = deque()

    def seed(y, x):
        if light[y, x] and not outside[y, x]:
            outside[y, x] = True; q.append((y, x))

    # Seed the top, left and right edges in full. The BOTTOM edge is seeded
    # only at the outer quarters: a bust pose is cropped at the chest, so its
    # white polo touches the bottom border, and flooding from there walks up
    # inside him and erases the shirt. The outer corners are always ground.
    for x in range(w):
        seed(0, x)
    for y in range(h):
        seed(y, 0); seed(y, w - 1)
    edge = max(1, w // 4)
    for x in list(range(edge)) + list(range(w - edge, w)):
        seed(h - 1, x)
    while q:
        y, x = q.popleft()
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny, nx = y+dy, x+dx
            if 0 <= ny < h and 0 <= nx < w and light[ny, nx] and not outside[ny, nx]:
                outside[ny, nx] = True; q.append((ny, nx))
    # JPEG leaves a light fringe between ink and ground that the >=236 test
    # keeps, so every figure came out with a halo on a dark plate. Grow the
    # outside into that fringe a couple of pixels, under a looser threshold.
    # The polo cannot be reached: it is enclosed by his black outline.
    fringe = (sub[:, :, 0] >= 206) & (sub[:, :, 1] >= 206) & (sub[:, :, 2] >= 206)
    for _ in range(2):
        nb = np.zeros_like(outside)
        nb[1:, :] |= outside[:-1, :]
        nb[:-1, :] |= outside[1:, :]
        nb[:, 1:] |= outside[:, :-1]
        nb[:, :-1] |= outside[:, 1:]
        outside |= (nb & fringe)
    rgba = np.dstack([sub.astype(np.uint8), np.where(outside, 0, 255).astype(np.uint8)])
    ys, xs = np.where(~outside)
    if len(ys) == 0:
        return None
    m = 2
    t, b = max(0, ys.min()-m), min(h, ys.max()+1+m)
    l, r = max(0, xs.min()-m), min(w, xs.max()+1+m)
    return Image.fromarray(rgba[t:b, l:r], 'RGBA')


def main():
    os.makedirs(OUT, exist_ok=True)
    index = {}
    for fn, names in NAMES.items():
        a = np.asarray(Image.open(os.path.join(SHEETS, fn)).convert('RGB')).astype(int)
        boxes = find_cells(a)
        if len(boxes) != len(names):
            print('!! %s: %d cells but %d names' % (fn, len(boxes), len(names)))
            for b in boxes: print('     ', b)
            continue
        for box, name in zip(boxes, names):
            if name.startswith('_'):
                continue
            img = cut(a, box)
            if img is None:
                print('!! %s/%s empty' % (fn, name)); continue
            p = os.path.join(OUT, name + '.png')
            img.save(p)
            index[name] = {'file': 'poses/%s.png' % name, 'w': img.width, 'h': img.height,
                           'sheet': fn}
            print('  %-22s %4dx%-4d' % (name, img.width, img.height))
    json.dump(index, open(os.path.join(SHEETS, 'poses.json'), 'w'), indent=1, sort_keys=True)
    print('\n%d poses -> %s' % (len(index), OUT))


if __name__ == '__main__':
    main()
