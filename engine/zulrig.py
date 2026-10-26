# -*- coding: utf-8 -*-
"""Rig the sheet artwork so it can be animated over footage.

Pose-swapping alone is a slideshow of stills. This cuts each pose at the neck
so the head can bob, tilt and lip-sync against a body that breathes, which is
puppet animation of the owner's own drawing rather than a second rendering of
the character.

Everything is measured off the art: the neck is the narrowest ink span between
head and collar, and the mouth is the enclosed dark shape low in the face.
"""
import os, json
from collections import deque
from PIL import Image
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
POSES = os.path.join(HERE, 'zulsheet', 'poses')
RIG = os.path.join(HERE, 'zulsheet', 'rig')


def _ink(a):
    return (a[:, :, 3] > 40) & (a[:, :, :3].max(2) < 110)


def neck(a):
    """(x_centre, y_top, y_bottom) of the neck column."""
    ink = _ink(a)
    h, w = ink.shape
    widths = []
    for y in range(int(h * 0.25), int(h * 0.75)):
        xs = np.where(ink[y])[0]
        widths.append((y, (xs.max() - xs.min() + 1) if len(xs) else 9999,
                       (xs.min() + xs.max()) / 2 if len(xs) else 0))
    thin = [t for t in widths if t[1] <= 14]
    if not thin:
        return None
    # longest contiguous run of thin rows
    runs, cur = [], [thin[0]]
    for t in thin[1:]:
        if t[0] == cur[-1][0] + 1:
            cur.append(t)
        else:
            runs.append(cur); cur = [t]
    runs.append(cur)
    run = max(runs, key=len)
    return (float(np.mean([t[2] for t in run])), run[0][0], run[-1][0])


def mouth_box(a, face_top_frac=0.12, face_bot_frac=0.46):
    """Bounding box of the drawn mouth, so it can be covered and replaced."""
    ink = _ink(a)
    h, w = ink.shape
    y0, y1 = int(h * face_top_frac), int(h * face_bot_frac)
    band = ink[y0:y1].copy()
    # The mouth is a small blob near the horizontal centre, below the eyes and
    # clear of the outline, so ignore anything touching the band edges.
    lab = np.zeros(band.shape, np.int32)
    best = None
    n = 0
    for yy in range(band.shape[0]):
        for xx in range(band.shape[1]):
            if band[yy, xx] and lab[yy, xx] == 0:
                n += 1
                q, pix = deque([(yy, xx)]), []
                lab[yy, xx] = n
                while q:
                    cy, cx = q.popleft(); pix.append((cy, cx))
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = cy+dy, cx+dx
                        if (0 <= ny < band.shape[0] and 0 <= nx < band.shape[1]
                                and band[ny, nx] and lab[ny, nx] == 0):
                            lab[ny, nx] = n; q.append((ny, nx))
                ys = [p[0] for p in pix]; xs = [p[1] for p in pix]
                if min(ys) == 0 or max(ys) == band.shape[0]-1:
                    continue                      # part of the outline
                cx_ = (min(xs) + max(xs)) / 2
                if abs(cx_ - w/2) > w * 0.16:
                    continue                      # not central: an eye or a curl
                area = len(pix)
                if 12 <= area <= w * h * 0.02:
                    cand = (min(xs), y0+min(ys), max(xs)+1, y0+max(ys)+1, area,
                            (min(ys)+max(ys))/2)
                    if best is None or cand[5] > best[5]:
                        best = cand               # lowest central blob = mouth
    return best[:4] if best else None


def build(name, force=False, warm=False):
    """Split one pose into head + body with a pivot. Cached on disk."""
    os.makedirs(RIG, exist_ok=True)
    suffix = '-warm' if warm else ''
    meta_p = os.path.join(RIG, name + suffix + '.json')
    if os.path.exists(meta_p) and not force:
        return json.load(open(meta_p))
    im = Image.open(os.path.join(POSES, name + '.png')).convert('RGBA')
    cheeks = None
    if warm:
        # The Meticulous Investor runs a warm face. The skin tint is constant
        # so it is baked here; the blush is NOT, because it has to come and go.
        import thumb
        _, cheeks = thumb.face_region(im)
        im = thumb.tint_face(im, cheeks=False)
    a = np.asarray(im)
    nk = neck(a)
    if nk is None:
        raise SystemExit('no neck found in %s — is it a full-body pose?' % name)
    nx, ny0, ny1 = nk
    cut = int((ny0 + ny1) / 2)
    # Overlap by a few pixels so the join never shows a seam when the head
    # rotates a degree or two.
    head = im.crop((0, 0, im.width, min(im.height, cut + 6)))
    body = im.crop((0, max(0, cut - 6), im.width, im.height))
    head.save(os.path.join(RIG, name + suffix + '-head.png'))
    # A head with the drawn mouth painted out, so a driven mouth can take its
    # place. The fill colour is sampled just above the mouth, which is face
    # whether or not the skin tint has been applied.
    mb0 = mouth_box(a)
    if mb0:
        hx0, hy0, hx1, hy1 = mb0
        ha = np.asarray(head).copy()
        samp = ha[max(0, hy0 - 6), (hx0 + hx1) // 2][:3]
        pad = 3
        ha[max(0, hy0-pad):hy1+pad, max(0, hx0-pad):hx1+pad, 0] = samp[0]
        ha[max(0, hy0-pad):hy1+pad, max(0, hx0-pad):hx1+pad, 1] = samp[1]
        ha[max(0, hy0-pad):hy1+pad, max(0, hx0-pad):hx1+pad, 2] = samp[2]
        Image.fromarray(ha, 'RGBA').save(os.path.join(RIG, name + suffix + '-head-nomouth.png'))
    body.save(os.path.join(RIG, name + suffix + '-body.png'))
    mb = mouth_box(a)
    meta = {'w': im.width, 'h': im.height, 'cut': cut,
            'pivot': [round(nx, 1), cut],
            'head': {'file': name + suffix + '-head.png', 'w': head.width, 'h': head.height},
            'body': {'file': name + suffix + '-body.png', 'w': body.width, 'h': body.height,
                     'top': max(0, cut - 6)},
            'cheeks': cheeks,
            'mouth': list(mb) if mb else None,
            'head_nomouth': (name + suffix + '-head-nomouth.png') if mb else None}
    json.dump(meta, open(meta_p, 'w'), indent=1)
    return meta


if __name__ == '__main__':
    import sys
    for n in (sys.argv[1:] or ['nb-bust-idle', 'nb-bust-point-right',
                               'nb-bust-point-left', 'nb-bust-shock',
                               'nb-bust-skeptical']):
        for warm in (False, True):
            m = build(n, force=True, warm=warm)
            print('%-22s %-5s neck@%-5s mouth=%-22s cheeks=%s'
                  % (n, 'warm' if warm else 'line', m['pivot'][0],
                     m['mouth'], m.get('cheeks')))
