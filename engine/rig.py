# -*- coding: utf-8 -*-
"""Cut-out rig: composites the part PNGs and animates them per frame.

Parts are ordinary transparent PNGs. It makes no difference whether they came
out of zul.py or out of Procreate — if a part matches the canvas size and
pivot in parts/manifest.json, the rig animates it identically.

Assembly is done in ZUL'S OWN coordinate space, not in canvas pixels: each
part declares where its pivot sits in that space, and the rig pins that pivot
to a joint. Guessing per-canvas offsets is how the first attempt ended up with
a floating head.

    python3 rig.py && node render_rig.js
"""
import io, json

M = json.load(open('parts/manifest.json'))
W, H = 1080, 1920
SCALE = 2.4
NECK_FRAME = (540, 780)      # where zul-local (0, 104) lands in the frame

# Joints, in zul-local coordinates (see zul.py).
NECK   = (0, 104)
SHO_L, SHO_R = (-66, 156), (66, 156)
HIP_L, HIP_R = (-20, 244), (20, 244)

def place(name, joint, elem_id, z, flip=False):
    """Pin this part's pivot to a joint in zul-local space."""
    m = M[name]
    plx, ply = m['pivot_local']
    fx = NECK_FRAME[0] + (joint[0] - NECK[0]) * SCALE
    fy = NECK_FRAME[1] + (joint[1] - NECK[1]) * SCALE
    px, py = m['pivot'][0] * SCALE, m['pivot'][1] * SCALE
    return (f'<img id="{elem_id}" src="parts/{m["file"]}" '
            f'style="position:absolute;left:{fx - px:.1f}px;top:{fy - py:.1f}px;'
            f'width:{m["w"] * SCALE:.1f}px;height:{m["h"] * SCALE:.1f}px;'
            f'transform-origin:{px:.1f}px {py:.1f}px;z-index:{z};'
            f'{"transform:scaleX(-1);" if flip else ""}">')

parts = [
    place('leg',   HIP_L, 'legL',  1),
    place('leg',   HIP_R, 'legR',  1, flip=True),
    place('torso', NECK,  'torso', 2),
    place('arm',   SHO_L, 'armL',  3),
    place('arm',   SHO_R, 'armR',  3, flip=True),
    place('head',  NECK,  'head',  4),
]

JS = '''
const $ = id => document.getElementById(id);
const lerp = (a,b,t) => a + (b-a)*t;
const ease = t => t<.5 ? 4*t*t*t : 1-Math.pow(-2*t+2,3)/2;

// A scene is a pair of poses; the rig eases between them. Angles are degrees
// about each part's pivot. Arms hang at 0 and swing out positive-outward.
const SCENES = [
  { armL:[ 4,  6], armR:[  4,  52], head:[0,-3], bob:1.0 },  // raise to point
  { armL:[ 4, 18], armR:[ 52,  44], head:[-3,2], bob:1.6 },  // gesture while talking
  { armL:[18,  4], armR:[ 44,   4], head:[2, 0], bob:0.8 },  // settle
];
window.NSC = SCENES.length;

window.setFrame = function(s, t){
  const S = SCENES[s], e = ease(t);
  const bob = Math.sin(t * Math.PI * 2 * S.bob) * 4;
  $('armL').style.transform  = 'rotate(' + lerp(S.armL[0], S.armL[1], e) + 'deg)';
  $('armR').style.transform  = 'scaleX(-1) rotate(' + lerp(S.armR[0], S.armR[1], e) + 'deg)';
  $('head').style.transform  = 'translateY(' + bob + 'px) rotate(' + lerp(S.head[0], S.head[1], e) + 'deg)';
  $('torso').style.transform = 'translateY(' + (bob * 0.35) + 'px)';
  $('legL').style.transform  = 'rotate(' + ( bob * 0.25) + 'deg)';
  $('legR').style.transform  = 'scaleX(-1) rotate(' + (bob * 0.25) + 'deg)';
};'''

CSS = f'''*{{margin:0;padding:0}}
html,body{{background:#fff;width:{W}px;height:{H}px;overflow:hidden}}
img{{position:absolute}}
#strip{{position:absolute;left:0;top:{H-82}px;width:{W}px;height:82px;background:#000;
  color:#fff;font:700 36px Liberation Sans,Arial,sans-serif;text-align:center;line-height:82px}}'''

io.open('rig.html', 'w', encoding='utf-8').write(
    '<!doctype html><meta charset="utf-8">' + f'<style>{CSS}</style>' + ''.join(parts)
    + '<div id="strip">EDUCATIONAL ONLY. NOT FINANCIAL ADVICE.</div>'
    + f'<script>{JS}</script>')
print('rig.html — %d parts' % len(parts))
