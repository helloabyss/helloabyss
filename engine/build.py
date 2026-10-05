#!/usr/bin/env python3
"""One command -> every still for a video. python3 build.py [outdir]"""
import io, os, sys, json
from prims import page
from scenes import S

out = sys.argv[1] if len(sys.argv) > 1 else 'out'
os.makedirs(out, exist_ok=True)
manifest = []
for n, vo, body in S:
    f = os.path.join(out, '%02d.html' % n)
    io.open(f, 'w', encoding='utf-8').write(page(body))
    manifest.append({'n': n, 'png': '%02d.png' % n, 'vo': vo, 'seconds': 8})
io.open(os.path.join(out, 'manifest.json'), 'w', encoding='utf-8').write(
    json.dumps(manifest, indent=1, ensure_ascii=False))
# CapCut/Premiere-friendly SRT so the VO lines up without eyeballing
def ts(total):
    h = int(total // 3600); mi = int(total % 3600 // 60); sec = total % 60
    return ('%02d:%02d:%06.3f' % (h, mi, sec)).replace('.', ',')
srt = []
for i, item in enumerate(manifest):
    a, b = i * 8, (i + 1) * 8
    srt.append('%d\n%s --> %s\n%s\n' % (i + 1, ts(a), ts(b), item['vo']))
io.open(os.path.join(out, 'timing.srt'), 'w', encoding='utf-8').write('\n'.join(srt))
print('%d scenes -> %s/  (+ manifest.json, timing.srt)' % (len(S), out))
