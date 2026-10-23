# -*- coding: utf-8 -*-
"""Timeline + deterministic player for the Three AI Picks long-form.

Durations are weighted, not uniform: the black "number the bull case leaves
out" cards are punctuation and run short, everything else shares the rest.
Total is pinned to the MEASURED voiceover length, so picture and sound cannot
drift — the quiet-depression video needed a re-render because the VO came in
longer than the planned runtime.
"""
import base64, io, json, os, sys
from scenes_aip import S

VO_SECS = float(sys.argv[1]) if len(sys.argv) > 1 else 529.40
DIR = 'aipscenes'

# turn cards carry the near-black full-bleed div
w = [0.42 if 'width:1920px;height:1080px;background:#111314' in b else 1.0 for b in S]
tot = sum(w)
durs = [VO_SECS * x / tot for x in w]
json.dump({'durations': [round(d, 3) for d in durs], 'total': round(sum(durs), 3)},
          open('aip-durations.json', 'w'), indent=1)

def b64(p):
    with open(p, 'rb') as f: return base64.b64encode(f.read()).decode()

frames = ''.join(
    f'<div class="sc" id="sc{i}"><img src="data:image/png;base64,{b64(os.path.join(DIR, "%02d.png" % (i+1)))}"></div>'
    for i in range(len(S)))

CSS = '''*{margin:0;padding:0}html,body{background:#fff;width:1920px;height:1080px;overflow:hidden}
.sc{position:absolute;inset:0;width:1920px;height:1080px;display:none;transform-origin:50% 50%}
.sc.on{display:block}img{display:block;width:1920px;height:1080px}'''

JS = '''
window.NSC=%d;
window.setFrame=function(s,t){
  for(let k=0;k<window.NSC;k++){const e=document.getElementById('sc'+k);
    if(e.classList.contains('on')&&k!==s) e.classList.remove('on');}
  const e=document.getElementById('sc'+s);
  if(!e.classList.contains('on')) e.classList.add('on');
  // settle on entry, then a slow push so a 12s hold still moves
  const pop=t<.05?(1-0.03*(1-t/.05)):1, push=1+0.045*t;
  e.style.transform='scale('+(pop*push).toFixed(5)+')';
};''' % len(S)

io.open('aip-player.html','w',encoding='utf-8').write(
    f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>{frames}<script>{JS}</script>')
print('%d scenes · total %.2fs · turn cards %.1fs · others %.1fs'
      % (len(S), sum(durs), min(durs), max(durs)))
