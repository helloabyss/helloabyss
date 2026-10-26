# -*- coding: utf-8 -*-
"""Thumbnail treatment for Zul.

The model sheets are pure line art with a white face. The owner's reference
thumbnail adds three things on top, and none of them are in the artwork:
a skin fill, rosy cheeks, and a rim glow that lifts him off a busy photo.
All three are applied here so the sheet stays untouched.
"""
from collections import deque
from PIL import Image, ImageFilter, ImageDraw
import numpy as np

SKIN   = (236, 200, 164)
CHEEK  = (240, 160, 150)


def _regions(alpha, rgb, seeds, light=232):
    """Flood the enclosed light areas reachable from `seeds`."""
    h, w = alpha.shape
    ok = (rgb[:, :, 0] >= light) & (rgb[:, :, 1] >= light) & (rgb[:, :, 2] >= light) & (alpha > 0)
    out = np.zeros((h, w), bool)
    q = deque()
    for (sx, sy) in seeds:
        if 0 <= sx < w and 0 <= sy < h and ok[sy, sx] and not out[sy, sx]:
            out[sy, sx] = True; q.append((sy, sx))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny, nx = y+dy, x+dx
            if 0 <= ny < h and 0 <= nx < w and ok[ny, nx] and not out[ny, nx]:
                out[ny, nx] = True; q.append((ny, nx))
    return out


def _components(mask):
    """Label 4-connected regions of a boolean mask."""
    h, w = mask.shape
    lab = np.zeros((h, w), np.int32)
    out, n = [], 0
    for y in range(h):
        for x in range(w):
            if mask[y, x] and lab[y, x] == 0:
                n += 1
                q, pix = deque([(y, x)]), []
                lab[y, x] = n
                while q:
                    cy, cx = q.popleft(); pix.append((cy, cx))
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = n; q.append((ny, nx))
                out.append(pix)
    return out


def face_region(img, head_frac=0.40):
    """The face mask and the two cheek centres, measured off the art.

    Returned so an animated blush can be drawn at the right place every frame.
    Baking cheeks into the head PNG would freeze them, and a blush that never
    changes reads as painted on rather than as a person.
    """
    im = img.convert('RGBA')
    a = np.asarray(im)
    h, w, _ = a.shape
    alpha, rgb = a[:, :, 3], a[:, :, :3]
    light = ((rgb[:, :, 0] >= 232) & (rgb[:, :, 1] >= 232) & (rgb[:, :, 2] >= 232)
             & (alpha > 0))
    face = np.zeros((h, w), bool)
    for pix in _components(light):
        if len(pix) < 25:
            continue
        if sum(p[0] for p in pix) / len(pix) < h * head_frac:
            for (y, x) in pix:
                face[y, x] = True
    if face.sum() < 40:
        return None, None
    ys, xs = np.where(face)
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    cy = int(y0 + (y1 - y0) * 0.78)
    r = max(4, int((x1 - x0) * 0.13))
    return face, [[int(x0 + (x1-x0) * 0.20), cy, r],
                  [int(x0 + (x1-x0) * 0.80), cy, r]]


def tint_face(img, skin=SKIN, cheeks=True, head_frac=0.40):
    """Fill the face with skin tone.

    Seeded coordinates were guessed from head-height fractions and landed on
    the curls instead of the face. This finds the regions instead: light areas
    that are enclosed by his outline (so not the transparent surround), whose
    centroid sits in the top `head_frac` of the figure. The glasses split the
    face into forehead and cheek, so both get picked up without naming either.
    """
    im = img.convert('RGBA')
    a = np.asarray(im).copy()
    h, w, _ = a.shape
    alpha, rgb = a[:, :, 3], a[:, :, :3]
    light = ((rgb[:, :, 0] >= 232) & (rgb[:, :, 1] >= 232) & (rgb[:, :, 2] >= 232)
             & (alpha > 0))
    face = np.zeros((h, w), bool)
    for pix in _components(light):
        if len(pix) < 25:
            continue
        cy = sum(p[0] for p in pix) / len(pix)
        if cy < h * head_frac:
            for (y, x) in pix:
                face[y, x] = True
    if face.sum() < 40:
        return im
    for i, v in enumerate(skin):
        a[:, :, i] = np.where(face, v, a[:, :, i])
    out = Image.fromarray(a, 'RGBA')
    if cheeks:
        ys, xs = np.where(face)
        cy = int(ys.min() + (ys.max() - ys.min()) * 0.78)
        x0, x1 = xs.min(), xs.max()
        r = max(4, int((x1 - x0) * 0.13))
        blob = Image.new('RGBA', out.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(blob)
        for cx in (int(x0 + (x1-x0) * 0.20), int(x0 + (x1-x0) * 0.80)):
            d.ellipse([cx-r, cy-int(r*0.7), cx+r, cy+int(r*0.7)], fill=CHEEK + (165,))
        blob = blob.filter(ImageFilter.GaussianBlur(r * 0.45))
        bm = np.asarray(blob).copy()
        bm[:, :, 3] = np.where(face, bm[:, :, 3], 0)
        out.alpha_composite(Image.fromarray(bm, 'RGBA'))
    return out


def rim(img, colour=(255, 214, 102), px=14, passes=3):
    """Glow behind the figure so he separates from a busy plate."""
    im = img.convert('RGBA')
    pad = px * 3
    big = Image.new('RGBA', (im.width + pad*2, im.height + pad*2), (0, 0, 0, 0))
    big.alpha_composite(im, (pad, pad))
    a = np.asarray(big)[:, :, 3]
    glow = Image.new('RGBA', big.size, colour + (0,))
    g = np.asarray(glow).copy()
    mask = Image.fromarray(a, 'L').filter(ImageFilter.MaxFilter(3))
    for _ in range(passes):
        mask = mask.filter(ImageFilter.MaxFilter(5))
    mask = mask.filter(ImageFilter.GaussianBlur(px * 0.6))
    g[:, :, 3] = np.asarray(mask)
    out = Image.fromarray(g, 'RGBA')
    out.alpha_composite(big)
    return out
