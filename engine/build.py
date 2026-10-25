#!/usr/bin/env python3
"""One command -> every still for a video. python3 build.py [outdir]"""
import io, os, sys, json, importlib.util
from prims import page

# python3 build.py [outdir] [scenes_module.py] [durations.json]
# Defaults keep the original behaviour: scenes.py at a flat 8s per scene.
out = sys.argv[1] if len(sys.argv) > 1 else 'out'
mod = sys.argv[2] if len(sys.argv) > 2 else 'scenes.py'
durf = sys.argv[3] if len(sys.argv) > 3 else None
_sp = importlib.util.spec_from_file_location('_scenes', mod)
_m = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_m)
S = _m.S
# Portrait shorts and landscape long-form share this runner; a scenes module
# declares its own canvas via SIZE and landscape stays the default.
SIZE = getattr(_m, 'SIZE', (1920, 1080))
# Per-scene durations measured from the narration beat the flat 8s, which is what
# makes picture drift against voice over a long runtime.
DUR = json.load(open(durf))['durations'] if durf else [8] * len(S)
if len(DUR) != len(S):
    raise SystemExit('%d durations for %d scenes' % (len(DUR), len(S)))
os.makedirs(out, exist_ok=True)
manifest = []
for n, vo, body in S:
    f = os.path.join(out, '%02d.html' % n)
    io.open(f, 'w', encoding='utf-8').write(page(body, SIZE[0], SIZE[1]))
    manifest.append({'n': n, 'png': '%02d.png' % n, 'vo': vo,
                     'seconds': round(DUR[n - 1], 3)})
io.open(os.path.join(out, 'manifest.json'), 'w', encoding='utf-8').write(
    json.dumps(manifest, indent=1, ensure_ascii=False))
# The renderers used to hardcode 1920x1080 and silently cropped portrait builds.
io.open(os.path.join(out, 'canvas.json'), 'w', encoding='utf-8').write(
    json.dumps({'w': SIZE[0], 'h': SIZE[1]}))
# CapCut/Premiere-friendly SRT so the VO lines up without eyeballing
def ts(total):
    h = int(total // 3600); mi = int(total % 3600 // 60); sec = total % 60
    return ('%02d:%02d:%06.3f' % (h, mi, sec)).replace('.', ',')
srt = []
_t = 0.0
for i, item in enumerate(manifest):
    a = _t; _t += item['seconds']; b = _t
    srt.append('%d\n%s --> %s\n%s\n' % (i + 1, ts(a), ts(b), item['vo']))
io.open(os.path.join(out, 'timing.srt'), 'w', encoding='utf-8').write('\n'.join(srt))
print('%d scenes -> %s/  (+ manifest.json, timing.srt)' % (len(S), out))
