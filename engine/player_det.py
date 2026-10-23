#!/usr/bin/env python3
"""Deterministic player: exposes window.setFrame(scene, progress 0..1)."""
import io, sys
from prims import page
from scenes import S
out = sys.argv[1] if len(sys.argv) > 1 else 'player.html'
limit = int(sys.argv[2]) if len(sys.argv) > 2 else len(S)
sel = S[:limit]
frames = []
for i, (n, vo, body) in enumerate(sel):
    svg = page(body); svg = svg[svg.index('<svg'):]
    frames.append(f'<div class="sc" id="sc{i}">{svg}</div>')
css = '''*{margin:0;padding:0}html,body{background:#fff;width:1920px;height:1080px;overflow:hidden}
.sc{position:absolute;inset:0;width:1920px;height:1080px;background:#fff;display:none;
    transform-origin:50% 50%}
.sc.on{display:block}
svg{display:block;width:1920px;height:1080px}'''
js = '''
window.NSC = %d;
window.setFrame = function(s, t){
  for(let k=0;k<window.NSC;k++){const e=document.getElementById('sc'+k);
    if(e.classList.contains('on') && k!==s) e.classList.remove('on');}
  const e=document.getElementById('sc'+s);
  if(!e.classList.contains('on')) e.classList.add('on');
  // entry pop over first 4%% of the hold, then slow linear push
  const pop = t < .04 ? (1 - 0.035*(1 - t/.04)) : 1;
  const push = 1 + 0.055*t;
  e.style.transform = 'scale(' + (pop*push).toFixed(5) + ')';
};''' % len(sel)
io.open(out,'w',encoding='utf-8').write(
    f'<!doctype html><meta charset="utf-8"><style>{css}</style>'+''.join(frames)+f'<script>{js}</script>')
print('%s — %d scenes' % (out, len(sel)))
