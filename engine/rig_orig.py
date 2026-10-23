# -*- coding: utf-8 -*-
"""16:9 animated beat using the CANONICAL artwork.

Parts are cut from art/zul-sheet.jpg by cutparts.js, not regenerated from
zul.py — this is the actual supplied character, not an approximation of it.

Only the head is separated. The row profile shows a clean neck at rel 176-207
with nothing behind it, so head-on-neck is a safe cut. The arms overlap the
torso silhouette and are NOT separated: mangling the supplied art to get an
elbow would be a worse trade than a head bob.

    python3 rig_orig.py && node render_rigo.js
"""
import io, json

M = json.load(open('parts/manifest-original.json'))
W, H = 1920, 1080
SCALE = 1.25
NECK = (430, 400)          # where the shared neck pivot lands in frame
K, R = '#000', '#d81e28'

def place(name, eid, z):
    m = M[name]
    px, py = m['pivot'][0] * SCALE, m['pivot'][1] * SCALE
    return (f'<img id="{eid}" src="parts/{m["file"]}" '
            f'style="position:absolute;left:{NECK[0]-px:.1f}px;top:{NECK[1]-py:.1f}px;'
            f'width:{m["w"]*SCALE:.1f}px;height:{m["h"]*SCALE:.1f}px;'
            f'transform-origin:{px:.1f}px {py:.1f}px;z-index:{z}">')

TICKERS = [('SPCX', 'NASDAQ'), ('BE', 'NYSE'), ('MU', 'NASDAQ')]
cards = ''.join(
    f'<div class="tk" id="tk{i}" style="top:{246 + i*198}px">'
    f'<span class="sym">{s}</span><span class="ex">{e}</span></div>'
    for i, (s, e) in enumerate(TICKERS))

CSS = f'''*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#0b0d0e;width:{W}px;height:{H}px;overflow:hidden;
  font-family:Liberation Sans,Arial,sans-serif}}
img{{position:absolute}}
.tk{{position:absolute;left:940px;width:800px;padding:20px 34px;background:#fff;
  display:flex;align-items:baseline;gap:30px;opacity:0;border-left:14px solid {R}}}
.sym{{font-size:108px;font-weight:700;letter-spacing:2px;color:{R}}}
.ex{{font-size:32px;font-weight:700;color:#5b6670;letter-spacing:4px}}
#strip{{position:absolute;left:0;top:{H-74}px;width:{W}px;height:74px;background:#000;
  color:#fff;font-size:30px;font-weight:700;text-align:center;line-height:74px;letter-spacing:1px}}'''

JS = '''
const $=id=>document.getElementById(id), lerp=(a,b,t)=>a+(b-a)*t;
const ease=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
// Head tilt in degrees about the neck; body breathes against it.
const SCENES=[
  {head:[0,-2.5], bob:1.0, cards:0},
  {head:[-2.5,2], bob:1.5, cards:1},
  {head:[2,-1.5], bob:1.2, cards:2},
  {head:[-1.5,0], bob:0.8, cards:3},
];
window.NSC=SCENES.length;
window.setFrame=function(s,t){
  const S=SCENES[s], e=ease(t), bob=Math.sin(t*Math.PI*2*S.bob)*4;
  $('head').style.transform='translateY('+bob+'px) rotate('+lerp(S.head[0],S.head[1],e)+'deg)';
  $('body').style.transform='translateY('+(bob*0.3)+'px) scaleY('+(1+bob*0.0012)+')';
  for(let i=0;i<3;i++){
    const el=$('tk'+i); let o=0,dx=70;
    if(i<S.cards){ o=1; dx=0; }
    else if(i===S.cards){ const k=Math.min(1,t/0.35); o=ease(k); dx=70*(1-ease(k)); }
    el.style.opacity=o; el.style.transform='translateX('+dx+'px)';
  }
};'''

io.open('rigo.html','w',encoding='utf-8').write(
    '<!doctype html><meta charset="utf-8">' + f'<style>{CSS}</style>'
    + place('o-body','body',2) + place('o-head','head',3) + cards
    + '<div id="strip">EDUCATIONAL ONLY. NOT FINANCIAL ADVICE.</div>'
    + f'<script>{JS}</script>')
print('rigo.html — canonical parts, 3 ticker cards, 4 beats')
