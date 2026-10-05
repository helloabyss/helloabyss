#!/usr/bin/env python3
"""Emit one self-contained animated HTML player from scenes.py.
   python3 player.py [outfile] [limit]"""
import io, sys
from prims import page
from scenes import S

out = sys.argv[1] if len(sys.argv) > 1 else 'player.html'
limit = int(sys.argv[2]) if len(sys.argv) > 2 else len(S)
HOLD = 8.0          # seconds per scene
POP  = 0.28         # entry pop
sel = S[:limit]

frames = []
for i, (n, vo, body) in enumerate(sel):
    svg = page(body)
    svg = svg[svg.index('<svg'):]          # strip the <style> wrapper
    frames.append(f'<div class="sc" id="sc{i}">{svg}</div>')

css = f'''
*{{margin:0;padding:0}}
html,body{{background:#fff;width:1920px;height:1080px;overflow:hidden}}
.sc{{position:absolute;inset:0;width:1920px;height:1080px;background:#fff;
     display:none;transform-origin:50% 50%}}
.sc.on{{display:block;will-change:transform;
        animation:pop {POP}s cubic-bezier(.2,.9,.3,1) both,
        push {HOLD}s linear both}}
@keyframes pop{{from{{transform:scale(.965)}}to{{transform:scale(1)}}}}
@keyframes push{{from{{transform:scale(1)}}to{{transform:scale(1.055)}}}}
svg{{display:block;width:1920px;height:1080px}}
'''

js = f'''
const HOLD={int(HOLD*1000)}, N={len(sel)};
let i=-1;
function step(){{
  if(i>=0){{const p=document.getElementById('sc'+i); p.classList.remove('on');}}
  i++;
  if(i>=N){{document.title='DONE';return;}}
  const e=document.getElementById('sc'+i);
  e.classList.remove('on'); void e.offsetWidth; e.classList.add('on');
  setTimeout(step, HOLD);
}}
window.addEventListener('load', ()=>setTimeout(step, 400));
'''
io.open(out,'w',encoding='utf-8').write(
    f'<!doctype html><meta charset="utf-8"><title>play</title><style>{css}</style>'
    + ''.join(frames) + f'<script>{js}</script>')
print('%s  — %d scenes  — %.1f s runtime' % (out, len(sel), len(sel)*HOLD + 0.4))
