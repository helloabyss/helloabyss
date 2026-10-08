# -*- coding: utf-8 -*-
"""16:9 animated beat for the Three AI Picks long-form.

Zul is driven by the cut-out rig (he moves, so the rig is correct here; held
frames use the canonical art — see CHARACTER-ZUL.md). The background is a
near-black plate so the Higgsfield b-roll can be dropped behind him in the
edit without relighting anything.

    python3 rig_16x9.py && node render_rig16.js
"""
import io, json

M = json.load(open('parts/manifest.json'))
W, H = 1920, 1080
SCALE = 1.55
NECK_FRAME = (430, 430)          # zul-local (0,104) lands here

NECK = (0, 104)
SHO_L, SHO_R = (-66, 156), (66, 156)
HIP_L, HIP_R = (-20, 244), (20, 244)

K, W_, R = '#000', '#fff', '#d81e28'

def place(name, joint, eid, z, flip=False):
    m = M[name]
    fx = NECK_FRAME[0] + (joint[0] - NECK[0]) * SCALE
    fy = NECK_FRAME[1] + (joint[1] - NECK[1]) * SCALE
    px, py = m['pivot'][0] * SCALE, m['pivot'][1] * SCALE
    return (f'<img id="{eid}" src="parts/{m["file"]}" '
            f'style="position:absolute;left:{fx-px:.1f}px;top:{fy-py:.1f}px;'
            f'width:{m["w"]*SCALE:.1f}px;height:{m["h"]*SCALE:.1f}px;'
            f'transform-origin:{px:.1f}px {py:.1f}px;z-index:{z};'
            f'{"transform:scaleX(-1);" if flip else ""}">')

parts = [place('leg', HIP_L, 'legL', 1), place('leg', HIP_R, 'legR', 1, True),
         place('torso', NECK, 'torso', 2),
         place('arm', SHO_L, 'armL', 3), place('arm', SHO_R, 'armR', 3, True),
         place('head', NECK, 'head', 4)]

# Ticker cards. Bold, uppercase, accent red — the only words allowed the accent.
TICKERS = [('SPCX', 'Nasdaq'), ('BE', 'NYSE'), ('MU', 'Nasdaq')]
cards = []
for i, (sym, ex) in enumerate(TICKERS):
    cards.append(
        f'<div class="tk" id="tk{i}" style="top:{250 + i*196}px">'
        f'<span class="sym">{sym}</span><span class="ex">{ex}</span></div>')

CSS = f'''*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#0b0d0e;width:{W}px;height:{H}px;overflow:hidden;
  font-family:Liberation Sans,Arial,sans-serif}}
img{{position:absolute}}
.tk{{position:absolute;left:980px;width:760px;padding:22px 34px;
  background:#fff;display:flex;align-items:baseline;gap:28px;opacity:0;
  border-left:14px solid {R}}}
.sym{{font-size:104px;font-weight:700;letter-spacing:2px;color:{R}}}
.ex{{font-size:34px;font-weight:700;color:#5b6670;text-transform:uppercase;letter-spacing:3px}}
#strip{{position:absolute;left:0;top:{H-74}px;width:{W}px;height:74px;
  background:#000;color:#fff;font-size:30px;font-weight:700;
  text-align:center;line-height:74px;letter-spacing:1px}}'''

JS = '''
const $=id=>document.getElementById(id), lerp=(a,b,t)=>a+(b-a)*t;
const ease=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
const SCENES=[
  {armL:[4,6],   armR:[4,54],  head:[0,-3], bob:1.0, cards:0},
  {armL:[4,16],  armR:[54,48], head:[-3,2], bob:1.5, cards:1},
  {armL:[16,10], armR:[48,52], head:[2,-2], bob:1.2, cards:2},
  {armL:[10,4],  armR:[52,4],  head:[-2,0], bob:0.8, cards:3},
];
window.NSC=SCENES.length;
window.setFrame=function(s,t){
  const S=SCENES[s], e=ease(t), bob=Math.sin(t*Math.PI*2*S.bob)*3;
  $('armL').style.transform='rotate('+lerp(S.armL[0],S.armL[1],e)+'deg)';
  $('armR').style.transform='scaleX(-1) rotate('+lerp(S.armR[0],S.armR[1],e)+'deg)';
  $('head').style.transform='translateY('+bob+'px) rotate('+lerp(S.head[0],S.head[1],e)+'deg)';
  $('torso').style.transform='translateY('+(bob*0.35)+'px)';
  $('legL').style.transform='rotate('+(bob*0.2)+'deg)';
  $('legR').style.transform='scaleX(-1) rotate('+(bob*0.2)+'deg)';
  // Cards land one per scene, each sliding in over the first 35% of its beat.
  for(let i=0;i<3;i++){
    const el=$('tk'+i); let o=0,dx=70;
    if(i<S.cards){ o=1; dx=0; }
    else if(i===S.cards){ const k=Math.min(1,t/0.35); o=ease(k); dx=70*(1-ease(k)); }
    el.style.opacity=o; el.style.transform='translateX('+dx+'px)';
  }
};'''

io.open('rig16.html','w',encoding='utf-8').write(
    '<!doctype html><meta charset="utf-8">' + f'<style>{CSS}</style>'
    + ''.join(parts) + ''.join(cards)
    + '<div id="strip">EDUCATIONAL ONLY. NOT FINANCIAL ADVICE.</div>'
    + f'<script>{JS}</script>')
print('rig16.html — %d parts, 3 ticker cards, 4 beats' % len(parts))
