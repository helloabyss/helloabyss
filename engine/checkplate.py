#!/usr/bin/env python3
"""Reject a plate that is crushed to black, or so bright that type cannot sit
on it.

The ceiling used to be 120, which encoded the near-black look the owner
rejected on 2026-10-26. Bright plates are now the point. What has NOT changed
is the reason a ceiling exists: cream type laid straight onto a 180-luma frame
is unreadable. So the window is wider, and the rule is that anything above
SCRIM_AT must carry its type on chrome -- a card, a panel, a band -- or inside
the scrim at the foot of the frame, never bare over the picture.

Pure black is still a missing plate that renders anyway. Sampled across the
clip, not at one frame.
"""
import subprocess, sys, os, tempfile
from PIL import Image, ImageStat

FF = '/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
f = sys.argv[1]
lo, hi = 8.0, 200.0           # mean luma window for a usable plate
SCRIM_AT = 120.0              # above this, type needs chrome or the foot scrim
means = []
with tempfile.TemporaryDirectory() as td:
    for t in (0.5, 2.0, 3.5, 5.0):
        o = os.path.join(td, 't.png')
        subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', str(t), '-i', f,
                        '-frames:v', '1', '-vf', 'scale=240:-1', o], check=False)
        if not os.path.exists(o):
            continue
        means.append(ImageStat.Stat(Image.open(o).convert('L')).mean[0])
if not means:
    raise SystemExit('PLATE REJECTED %s: no frames decoded' % f)
m = sum(means) / len(means)
print('   luma mean %.1f  (samples %s)' % (m, ' '.join('%.0f' % x for x in means)))
if m < lo:
    raise SystemExit('PLATE REJECTED %s: mean luma %.1f is below %.1f — crushed to black' % (f, m, lo))
if m > hi:
    raise SystemExit('PLATE REJECTED %s: mean luma %.1f is above %.1f — blown out' % (f, m, hi))
if m > SCRIM_AT:
    print('   note: %.1f is bright — type must sit on chrome or in the foot scrim' % m)
