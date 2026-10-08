# -*- coding: utf-8 -*-
"""Pose-to-pose animation from the official Zul pose library.

The sheets are drawn at one crop and scale, so the poses are registered to
each other: swapping one for another is a clean cut with no jump. That is why
this does NOT bend limbs — the poses are drawn, so the animation cuts between
them and adds only a float and a settle. Limited animation, done the way it is
actually done.

    python3 pose_anim.py && node render_pose.js
"""
import base64, io, json, os

M = json.load(open('art/poses/manifest.json'))
W, H = 1920, 1080
R, K = '#d81e28', '#000'

# (set, pose) per beat. Real drawn poses, in the order the VO needs them.
BEATS = [
    ('body', 'body-front',        0),   # settle, no card yet
    ('body', 'full-point-right',  1),   # SPCX lands
    ('body', 'full-present-palm', 2),   # BE lands
    ('body', 'full-skeptical',    3),   # MU lands — the counter-evidence face
]
TICKERS = [('SPCX', 'NASDAQ'), ('BE', 'NYSE'), ('MU', 'NASDAQ')]

def b64(rel):
    with open(os.path.join('art/poses', rel), 'rb') as f:
        return base64.b64encode(f.read()).decode()

FIG_H = 820                      # on-screen height of the panel, px
layers = []
for i, (st, pose, _) in enumerate(BEATS):
    m = M[st]['poses'][pose]
    w = FIG_H * m['w'] / float(m['h'])
    layers.append(
        f'<img class="pz" id="pz{i}" src="data:image/png;base64,{b64(m["file"])}" '
        f'style="left:{430 - w/2:.1f}px;top:{140}px;width:{w:.1f}px;height:{FIG_H}px">')

cards = ''.join(
    f'<div class="tk" id="tk{i}" style="top:{250 + i*198}px">'
    f'<span class="sym">{s}</span><span class="ex">{e}</span></div>'
    for i, (s, e) in enumerate(TICKERS))

CSS = f'''*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#0b0d0e;width:{W}px;height:{H}px;overflow:hidden;
  font-family:Liberation Sans,Arial,sans-serif}}
.pz{{position:absolute;opacity:0}}
.tk{{position:absolute;left:940px;width:800px;padding:20px 34px;background:#fff;
  display:flex;align-items:baseline;gap:30px;opacity:0;border-left:14px solid {R}}}
.sym{{font-size:108px;font-weight:700;letter-spacing:2px;color:{R}}}
.ex{{font-size:32px;font-weight:700;color:#5b6670;letter-spacing:4px}}
#strip{{position:absolute;left:0;top:{H-74}px;width:{W}px;height:74px;background:#000;
  color:#fff;font-size:30px;font-weight:700;text-align:center;line-height:74px;letter-spacing:1px}}'''

JS = '''
const $=id=>document.getElementById(id);
const ease=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
const CARDS=[0,1,2,3];
window.NSC=%d;
window.setFrame=function(s,t){
  // Hard cut between drawn poses; only the active one is visible.
  for(let i=0;i<window.NSC;i++) $('pz'+i).style.opacity = (i===s)?1:0;
  // Float + a settle on entry, so a held pose still breathes.
  const settle = 1 - 0.012*Math.exp(-t*9)*Math.cos(t*26);
  const float  = Math.sin(t*Math.PI*2*0.8)*5;
  $('pz'+s).style.transform='translateY('+float.toFixed(2)+'px) scale('+settle.toFixed(4)+')';
  const n=CARDS[s];
  for(let i=0;i<3;i++){
    const el=$('tk'+i); let o=0,dx=70;
    if(i<n){ o=1; dx=0; }
    else if(i===n){ const k=Math.min(1,t/0.3); o=ease(k); dx=70*(1-ease(k)); }
    el.style.opacity=o; el.style.transform='translateX('+dx+'px)';
  }
};''' % len(BEATS)

io.open('poseanim.html','w',encoding='utf-8').write(
    '<!doctype html><meta charset="utf-8">' + f'<style>{CSS}</style>'
    + ''.join(layers) + cards
    + '<div id="strip">EDUCATIONAL ONLY. NOT FINANCIAL ADVICE.</div>'
    + f'<script>{JS}</script>')
print('poseanim.html — %d drawn poses, %d ticker cards' % (len(BEATS), len(TICKERS)))
