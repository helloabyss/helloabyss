#!/usr/bin/env python3
"""Reject a plate that the grade has crushed to black or left too bright.

Dark and desaturated is the look; pure black is a missing plate that still
renders. Sampled across the clip, not at one frame.
"""
import subprocess, sys, os, tempfile
from PIL import Image, ImageStat

FF = '/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
f = sys.argv[1]
lo, hi = 8.0, 120.0           # mean luma window for a gradeable plate
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
    raise SystemExit('PLATE REJECTED %s: mean luma %.1f is above %.1f — too bright for the grade' % (f, m, hi))
