#!/usr/bin/env python3
"""Fail the build if scene art intrudes on the caption band.

Zul's extent was computed by hand from the proportions in CHARACTER-ZUL.md and
the answer was wrong by ~200px, which put a caption across his legs -- the same
collision the channel has already rejected once. Measure the ink instead.
"""
import sys, glob
from PIL import Image

BAND_TOP = int(sys.argv[2]) if len(sys.argv) > 2 else 1415
bad = []
for f in sorted(glob.glob(sys.argv[1] + '/*.png')):
    im = Image.open(f).convert('L')
    w, h = im.size
    px = im.load()
    low = None
    for y in range(h - 1, BAND_TOP - 1, -1):
        for x in range(0, w, 2):
            if px[x, y] < 200:
                low = y; break
        if low: break
    if low:
        bad.append((f, low))
        print('  COLLISION %s: ink at y=%d (band starts %d)' % (f, low, BAND_TOP))
    else:
        print('  ok        %s' % f)
if bad:
    raise SystemExit('\n%d scene(s) put art inside the caption band.' % len(bad))
print('\nAll scenes clear of the caption band (y>=%d).' % BAND_TOP)
