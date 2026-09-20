# Animatic renderer

Deterministic previz renderer for This Week in Tech. Chromium + Playwright frame capture,
encoded with ffmpeg. Needs no render credits.

| File | Role |
|---|---|
| `shots.json` | The 20 shots: timing, kind, description, exact source, licence, overlay, motion |
| `cues.json` | Caption cues, **generated from the episode SRT** — never hand-edited |
| `hat_vertices.json` | Verified hat monotile geometry (13 vertices) |
| `render.js` | Canvas renderer — `seek(t)` is a pure function of `t`, so frames are reproducible |
| `animatic.html` | Host page, 1080×1920 canvas |
| `capture.js` | Frame capture loop |

`kind` selects the draw routine: `plate` (placeholder for footage), `counter`, `strike`,
`map`, `price`, `stamp`, `tiers`, `hat`, `pinwheel`, `close`.

Regenerate `cues.json` after any script change:

```bash
python3 - <<'PY'
import json
cues=[]
for blk in open('../../scripts/2026-09-20.srt').read().strip().split('\n\n'):
    L=blk.split('\n'); a,b=L[1].split(' --> ')
    f=lambda x:(lambda h,m,s:int(h)*3600+int(m)*60+float(s.replace(',','.')))(*x.split(':'))
    cues.append({"a":f(a),"b":f(b),"t":L[2]})
json.dump(cues, open('cues.json','w'))
PY
```

See `scripts/2026-09-20-PRODUCTION.md` for the render command and what still has to be shot.
