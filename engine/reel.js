// Imagery-first portrait reel. STYLE-GUIDE.md section 1-3, which the first
// attempt at this short ignored: it put type on white and held each frame for
// 3-6s. Here the photographic plate is the BASE of every beat, graphics sit
// over it, type and captions sit on top, and nothing is ever at rest.
//
//   node reel.js <beats.json> <plates-dir> <audio.wav> <captions.json> <out.mp4> [fps]
const { chromium } = require('playwright');
const { spawn, execSync } = require('child_process');
const fs = require('fs'), path = require('path');

const [BEATS_F, PLATES, AUDIO, CAPS_F, OUT] = process.argv.slice(2);
const FPS = +(process.argv[7] || 30);
const FF = execSync("python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'")
            .toString().trim();
const beats = JSON.parse(fs.readFileSync(BEATS_F)).beats;
const words = JSON.parse(fs.readFileSync(CAPS_F)).words;
// Per-channel notice. The money channel needs the legal card; a PARADOCS10X
// video with no financial claim needs a sourcing line, not a disclaimer.
const NOTICE = JSON.parse(fs.readFileSync(BEATS_F)).notice || '';
// Host rig: the owner's sheet artwork, cut at the neck so the head can bob,
// tilt and lip-sync over a body that breathes. Pose swaps happen on beats.
const HOST = JSON.parse(fs.readFileSync(BEATS_F)).host || null;
const RIGDIR = path.join(__dirname, 'zulsheet', 'rig');
let RIG = null;
if (HOST) {
  RIG = {};
  const sfx = HOST.warm ? '-warm' : '';
  for (const p of HOST.poses.map(p => p[1])) {
    if (!RIG[p]) RIG[p] = JSON.parse(fs.readFileSync(path.join(RIGDIR, p + sfx + '.json')));
  }
}
const rigUrl = f => 'file://' + path.join(RIGDIR, f);
const W = 1080, H = 1920;
// Palette. The three-colour near-black + red scheme was rejected by the owner
// on 2026-10-26 ("makes me sick"), so the look is a named token set chosen per
// video in beats.json rather than hex literals scattered through the CSS.
const LOOKS = {
  warmdark:  { ground:'#141118', ink:'#f7f3ec', mute:'#9b9186', accent:'#e0a008',
               card:'#221d26', vig:'rgba(20,17,24,' },
  light:     { ground:'#f4f1ea', ink:'#15171a', mute:'#6b7280', accent:'#c8102e',
               card:'#ffffff', vig:'rgba(244,241,234,' },
  editorial: { ground:'#0e1a2b', ink:'#f2f6fb', mute:'#8fa3bd', accent:'#ffb020',
               card:'#16263d', vig:'rgba(14,26,43,' },
};
const LOOK = LOOKS[JSON.parse(fs.readFileSync(BEATS_F)).look || 'warmdark'];
const DUR = beats[beats.length - 1].t1;
const abs = p => 'file://' + path.resolve(PLATES, p);
const plates = [...new Set(beats.map(b => b.plate).filter(Boolean))];

// Plates are decoded to frames on disk BEFORE the browser starts.
//
// Profiled 2026-10-27: a per-frame <video> seek cost 481ms of a 561ms frame --
// 85% of the entire render, and the reason a 38s short took nine minutes. The
// seek is unavoidable while the plate is a <video>, because every output frame
// lands at a different source timestamp. So the plate stops being a video: one
// ffmpeg pass per plate writes the frames out, and the page shows an <img>.
// Swapping an <img> src costs a JPEG decode instead of a seek.
//
// (An <img> pointed at an .mp4 is what produced an entirely black render once
// before. This points it at real JPEGs.)
const CACHE = path.join(PLATES, '.frames');
const plateFrames = {};
for (const pl of plates) {
  const dir = path.join(CACHE, pl.replace(/\W/g, '_'));
  const src = path.resolve(PLATES, pl);
  const stamp = path.join(dir, '.ok');
  if (!fs.existsSync(stamp) || fs.statSync(stamp).mtimeMs < fs.statSync(src).mtimeMs) {
    fs.rmSync(dir, { recursive: true, force: true });
    fs.mkdirSync(dir, { recursive: true });
    execSync(`${FF} -nostdin -v error -y -i ${JSON.stringify(src)} ` +
             `-vf fps=${FPS} -q:v 3 ${JSON.stringify(path.join(dir, '%05d.jpg'))}`);
    fs.writeFileSync(stamp, '');
  }
  const n = fs.readdirSync(dir).filter(f => f.endsWith('.jpg')).length;
  if (!n) throw new Error('no frames decoded for plate ' + pl);
  plateFrames[pl] = { dir, n };
}
console.log('  plates cached: ' + plates.map(p => p + '=' + plateFrames[p].n + 'f').join(' '));

const html = `<!doctype html><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${W}px;height:${H}px;background:${LOOK.ground};overflow:hidden;
  font-family:"Liberation Sans Narrow","Liberation Sans",Arial,sans-serif}
#stage{position:absolute;inset:0;overflow:hidden}
/* BASE -- live photographic footage, graded on ingest by getplate.sh. The
   first version of this file used <img> and silently rendered black plates. */
.plate{position:absolute;left:-10%;top:-10%;width:120%;height:120%;
  object-fit:cover;display:none;will-change:transform}
.plate.on{display:block}
/* Near-black vignette so type always has something to sit on */
#vig{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(ellipse at 50% 42%,${LOOK.vig}.10) 0%,${LOOK.vig}.52) 58%,${LOOK.vig}.90) 100%)}
#grain{position:absolute;inset:0;opacity:.055;pointer-events:none;mix-blend-mode:overlay}
/* MID -- motion graphics over the imagery */
#mid{position:absolute;inset:0}
/* LAYOUT -- the furniture a composition needs: a flat ground panel, a floating
   card, an accent band, comparison columns. Previously every beat was the same
   full-bleed plate with a centred word at y=430, 28 times in a row, which read
   as a slide deck. */
#chrome{position:absolute;inset:0}
#chrome .pane{position:absolute;background:${LOOK.ground}}
#chrome .cardbox{position:absolute;background:${LOOK.card};border-radius:20px;
  box-shadow:0 24px 70px rgba(0,0,0,.34)}
#chrome .band{position:absolute;background:${LOOK.accent}}
#chrome .lab{position:absolute;font-weight:700;letter-spacing:5px;
  text-transform:uppercase;color:${LOOK.mute}}
#chrome .big{position:absolute;font-weight:800;letter-spacing:-2px;
  line-height:.9;color:${LOOK.ink}}
#chrome .qt{position:absolute;font-weight:800;line-height:1.08;color:${LOOK.ink}}
.bar{position:absolute;height:26px;background:${LOOK.accent}}
.barbg{position:absolute;height:26px;border:4px solid rgba(255,255,255,.65)}
.tick{position:absolute;width:3px;background:rgba(255,255,255,.30)}
.rule{position:absolute;height:8px;background:#fff}
.rule.r{background:${LOOK.accent}}
/* TOP -- hero type and captions */
#hero{position:absolute;left:40px;width:${W - 80}px;text-align:center;color:${LOOK.ink};
  font-weight:800;letter-spacing:-2px;line-height:.92;white-space:nowrap;
  text-shadow:0 10px 60px rgba(0,0,0,.85)}
#hero .fit{display:inline-block;white-space:nowrap}
#hero .l{display:inline-block;will-change:transform,opacity}
#hero.red{color:${LOOK.accent}}
/* #sub was LOOK.mute on plates running 115-178 mean luma -- effectively
   invisible. Ink-coloured with a real shadow instead. */
#sub{position:absolute;left:0;width:${W}px;text-align:center;color:${LOOK.ink};
  font-weight:700;letter-spacing:5px;text-transform:uppercase;
  text-shadow:0 2px 6px rgba(0,0,0,.95),0 4px 24px rgba(0,0,0,.85)}
#note{position:absolute;left:0;width:${W}px;text-align:center;color:rgba(255,255,255,.72);
  font-weight:700;font-size:30px;letter-spacing:1px;text-shadow:0 3px 14px rgba(0,0,0,.9)}
/* Captions sat at y1395-1595. The bottom of a Shorts frame is covered by the
   title, channel row and action buttons, and the playbook puts every text
   element above y~1535. The lower stack is lifted to clear it. */
#cap{position:absolute;left:60px;top:1316px;width:${W - 120}px;height:180px;
  display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:0 15px;
  font-size:58px;font-weight:800;line-height:1.1;text-align:center}
#cap span{color:#fff;-webkit-text-stroke:9px #000;paint-order:stroke fill;
  text-shadow:0 5px 18px rgba(0,0,0,.95)}
#cap span.now{color:${LOOK.accent}}
/* Host rig. Each pose is a stack: body, then head on its own transform. */
#host{position:absolute;left:0;top:0;transform-origin:0 0}
.zp{position:absolute;left:0;top:0;display:none}
.zp.on{display:block}
.zp img{position:absolute;left:0;top:0;display:block}
.zp .zh{position:absolute;left:0;top:0;will-change:transform}
.zp .zm{position:absolute;left:0;top:0;pointer-events:none}
#flash{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none}
#card{position:absolute;left:0;top:118px;width:${W}px;text-align:center}
#card b{display:inline-block;font-size:27px;font-weight:700;color:rgba(255,255,255,.93);
  padding:7px 20px;letter-spacing:2px;background:rgba(7,8,10,.62);
  border-left:4px solid ${LOOK.accent}}
/* type-as-mask wipe: a giant word reveals the next beat through its counters */
#mask{position:absolute;inset:0;background:#07080a;display:none;
  -webkit-mask-repeat:no-repeat;-webkit-mask-position:center;mask-repeat:no-repeat;mask-position:center}
</style>
<div id="stage">
  ${plates.map((p, i) => `<img class="plate" id="p${i}">`).join('')}
  <div id="vig"></div><div id="chrome"></div><div id="mid"></div>
  <div id="sub"></div><div id="hero"></div><div id="note"></div>
  <div id="mask"></div>
  <div id="flash"></div></div>  ${HOST ? `<div id="host">${Object.entries(RIG).map(([k, m]) => `
    <div class="zp" id="zp-${k}">
      <img class="zb" src="${rigUrl(m.body.file)}" style="top:${m.body.top}px">
      <div class="zh" style="transform-origin:${m.pivot[0]}px ${m.pivot[1]}px">
        <img src="${rigUrl(m.head_nomouth || m.head.file)}">
        ${m.mouth ? `<svg class="zm" width="${m.w}" height="${m.h}">
          <defs><filter id="bl-${k}" x="-60%" y="-60%" width="220%" height="220%">
            <feGaussianBlur stdDeviation="${Math.max(2, (m.cheeks ? m.cheeks[0][2] : 10) * 0.42)}"/>
          </filter></defs>
          ${m.cheeks ? `<g class="zc" filter="url(#bl-${k})" opacity="0">
            ${m.cheeks.map(c => `<ellipse cx="${c[0]}" cy="${c[1]}" rx="${c[2]}" ry="${(c[2]*0.7).toFixed(1)}" fill="#f0a096"/>`).join('')}
          </g>` : ''}
          <path/></svg>` : ''}
      </div>
    </div>`).join('')}</div>` : ''}<div id="cap"></div><div id="card"></div>
<script>
const LOOK  = ${JSON.stringify(LOOK)};
const BEATS = ${JSON.stringify(beats)};
const WORDS = ${JSON.stringify(words)};
const NOTICE = ${JSON.stringify(NOTICE)};
const HOST = ${JSON.stringify(HOST)};
const RIG  = ${JSON.stringify(RIG)};
const PLATES = ${JSON.stringify(plates)};
const FRAMES = ${JSON.stringify(plateFrames)};
const FPS = ${FPS};
const CARD = 4.0;
const ease = t => 1 - Math.pow(1 - t, 3);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

function setMid(b, u) {
  const m = document.getElementById('mid');
  if (!b.mid) { m.innerHTML = ''; return; }
  const g = b.mid; let h = '';
  if (g.type === 'bar') {
    // Proportional, always -- and on a FIXED scale across the whole sequence.
    // Normalising to each beat's own max pinned the white bar at full width and
    // made the amber bar SHRINK from 482px to 341px while the number it stands
    // for grew from 0.17 to 0.24. A chart that animates the opposite of the
    // narration is worse than no chart. g.max is the scale for every beat.
    const mx = g.max || Math.max(g.a, g.b), wA = 820 * (g.a / mx), wB = 820 * (g.b / mx);
    const gw = ease(clamp(u / .55, 0, 1));
    h += '<div class="barbg" style="left:130px;top:' + g.y + 'px;width:820px"></div>';
    h += '<div class="bar" style="left:130px;top:' + g.y + 'px;width:' + (wA * gw) + 'px;background:#fff"></div>';
    h += '<div class="barbg" style="left:130px;top:' + (g.y + 72) + 'px;width:820px"></div>';
    h += '<div class="bar" style="left:130px;top:' + (g.y + 72) + 'px;width:' + (wB * gw) + 'px"></div>';
    // Unlabelled bars are unreadable: the viewer cannot recover which is which.
    const lab = (txt, y) => '<div style="position:absolute;left:130px;top:' + y +
      'px;font-size:26px;font-weight:700;letter-spacing:3px;color:' + LOOK.ink +
      ';text-shadow:0 3px 14px rgba(0,0,0,.9)">' + txt + '</div>';
    h += lab(g.la || '', g.y - 36) + lab(g.lb || '', g.y + 72 - 36);
  } else if (g.type === 'grid') {
    // 1,400+ tasks -- a readable sample, not one square per task.
    const n = 120, lit = Math.floor(n * clamp(u / .7, 0, 1));
    for (let i = 0; i < n; i++) {
      const x = 150 + (i % 15) * 52, y = g.y + Math.floor(i / 15) * 52;
      h += '<div style="position:absolute;left:' + x + 'px;top:' + y + 'px;width:36px;height:36px;border:3px solid '
        + (i < lit ? 'rgba(255,255,255,.9)' : 'rgba(255,255,255,.18)') + '"></div>';
    }
  } else if (g.type === 'line_series') {
    // A decay curve drawn from real numbers, not a swoosh. Draws itself in.
    const rows = g.rows, n = rows.length;
    const vs = rows.map(r => r[1]), lo = Math.min(...vs), hi = Math.max(...vs);
    const W0 = 820, H0 = 300, x0 = 130, y0 = g.y;
    const sx = i => x0 + W0 * i / (n - 1);
    const sy = v => y0 + H0 - (v - lo) / Math.max(1e-6, hi - lo) * H0;
    const shown = Math.max(2, Math.round(n * Math.min(1, u / 0.72)));
    h += '<div style="position:absolute;left:' + x0 + 'px;top:' + y0 + 'px;width:' + W0 +
         'px;height:' + H0 + 'px;border-left:3px solid rgba(255,255,255,.5);' +
         'border-bottom:3px solid rgba(255,255,255,.5)"></div>';
    let d = '';
    for (let i = 0; i < shown; i++) d += (i ? ' L ' : 'M ') + sx(i).toFixed(1) + ' ' + sy(vs[i]).toFixed(1);
    h += '<svg style="position:absolute;left:0;top:0" width="1080" height="1920">' +
         '<path d="' + d + '" fill="none" stroke="' + LOOK.accent + '" stroke-width="6" ' +
         'stroke-linejoin="round" stroke-linecap="round"/>' +
         '<line x1="' + x0 + '" y1="' + sy(100) + '" x2="' + (x0 + W0) + '" y2="' + sy(100) +
         '" stroke="rgba(255,255,255,.45)" stroke-width="3" stroke-dasharray="8 7"/></svg>';
    h += '<div style="position:absolute;left:' + x0 + 'px;top:' + (y0 + H0 + 10) +
         'px;font-size:21px;color:#8d97a3;font-family:Liberation Mono,monospace">' +
         (g.label || '') + '</div>';
    h += '<div style="position:absolute;left:' + (x0 + W0 - 220) + 'px;top:' + (y0 + H0 + 10) +
         'px;width:220px;text-align:right;font-size:21px;color:#8d97a3;' +
         'font-family:Liberation Mono,monospace">' + (g.src || '') + '</div>';
  } else if (g.type === 'rule') {
    const w = 700 * ease(clamp(u / .4, 0, 1));
    h += '<div class="rule' + (g.red ? ' r' : '') + '" style="left:' + (540 - w / 2) + 'px;top:' + g.y + 'px;width:' + w + 'px"></div>';
  }
  m.innerHTML = h;
}

function fitHero(el, want, boxW) {
  // Shrink the hero until the laid-out LETTERS fit the box.
  //
  // Two earlier versions got this wrong. The first compared el.scrollWidth
  // against a width smaller than the element's own box, so every hero bottomed
  // out at the 28px floor. The second measured the string with a probe span --
  // but the hero renders as one inline-block per letter, which loses kerning
  // and rounds each box up, so the real line is wider than any probe of it and
  // "DREW THE LINE" still lost its last letter off the frame.
  //
  // So measure what is actually on screen: the union of the letter rects.
  const span = () => {
    const ls = el.children;
    if (!ls.length) return 0;
    let lo = Infinity, hi = -Infinity;
    for (const l of ls) {
      const r = l.getBoundingClientRect();
      if (r.width === 0) continue;
      if (r.left < lo) lo = r.left;
      if (r.right > hi) hi = r.right;
    }
    return hi > lo ? hi - lo : 0;
  };
  let size = want;
  el.style.fontSize = size + 'px';
  let w = span();
  if (w > boxW) size = Math.max(28, Math.floor(size * boxW / w));
  el.style.fontSize = size + 'px';
  // #hero is nowrap, so the line can never break mid-word -- an earlier fix
  // let it wrap and produced "DREW TH / E LINE". The estimate is close but not
  // exact (rounding moves with the size), so step down until it really fits.
  let guard = 0;
  while (span() > boxW && size > 28 && guard++ < 40) {
    size -= Math.max(1, Math.round(size * 0.03));
    el.style.fontSize = size + 'px';
  }
}

// Composition templates. A beat names one in "layout"; it draws its own
// furniture into #chrome and returns where the hero type goes, so the frame
// changes shape between beats instead of only changing content.
//   full   -- full-bleed plate, stat low (the original, kept for hooks)
//   split  -- plate top, flat ground panel below, type left-aligned in it
//   card   -- plate behind, the number on a floating card
//   quote  -- vox-pop caption card; b.quote + b.who carry it, hero unused
//   versus -- two columns from b.vs = (la, va, lb, vb); hero unused
//   band   -- one word reversed out of a full-width accent band
const LAY = {
  // The plates are bright now, so the foot scrim is what makes type readable
  // over bare picture -- and the type sits IN it rather than up at y=520 over
  // the lit part of the frame, where cream on 170-luma footage disappears.
  full: (b, u) => ({ chrome:
      '<div class="pane" style="left:0;top:0;width:1080px;height:1920px;background:' +
      'linear-gradient(transparent 26%,' + LOOK.ground + '66 46%,' + LOOK.ground +
      'ee 62%,' + LOOK.ground + ' 76%)"></div>',
    heroTop: b.heroY || 1035, align: 'left', left: 70, width: 940 }),

  // Two layouts that put the eye somewhere other than the bottom third.
  // A QC gate measured 68% of runtime in one arrangement -- muted label, left
  // hero, lower third -- which is what "still PowerPoint-like" meant. A
  // seventh variation of the same shape would not have fixed it.
  //
  //   topper     -- scrim and type at the TOP, picture owning the frame below
  //   fullbleed  -- type alone on the picture, no panel, no card, no band
  topper: (b, u) => ({ chrome:
      '<div class="pane" style="left:0;top:0;width:1080px;height:1920px;background:' +
      'linear-gradient(' + LOOK.ground + ' 0%,' + LOOK.ground + 'ee 22%,' +
      LOOK.ground + '55 36%,transparent 52%)"></div>' +
      '<div class="band" style="left:70px;top:' + (150 + (1 - ease(clamp(u / .3, 0, 1))) * 14).toFixed(0) +
        'px;width:' + (110 * ease(clamp(u / .3, 0, 1))).toFixed(0) + 'px;height:7px"></div>',
    heroTop: 250, align: 'left', left: 70, width: 940, subTop: 196 }),

  fullbleed: (b, u) => ({ chrome:
      // Light touch only. The first version scrimmed at 73-96% and left the
      // type floating on near-black, which is the "typography on an abstract
      // background" STYLE-GUIDE.md section 1 forbids. The picture has to stay
      // the base layer; the type earns its legibility from its own shadow.
      '<div class="pane" style="left:0;top:0;width:1080px;height:1920px;background:' +
      'radial-gradient(ellipse at 50% 46%,' + LOOK.ground + '26 0%,' +
      LOOK.ground + '70 58%,' + LOOK.ground + 'b0 100%)"></div>',
    heroTop: b.heroY || 760, align: 'center', left: 40, width: 1000, subTop: 660,
    heroShadow: '0 6px 18px rgba(0,0,0,.95),0 14px 70px rgba(0,0,0,.9)' }),

  split: (b, u) => ({ chrome:
      '<div class="pane" style="left:0;top:1020px;width:1080px;height:900px"></div>' +
      '<div class="band" style="left:0;top:1014px;width:' +
        (1080 * ease(clamp(u / .35, 0, 1))).toFixed(0) + 'px;height:6px"></div>',
    heroTop: 1070, align: 'left', left: 70, width: 940 }),

  card: (b, u) => {
    const g = ease(clamp(u / .3, 0, 1));
    return { chrome:
      '<div class="cardbox" style="left:70px;top:' + (640 + (1 - g) * 40).toFixed(0) +
        'px;width:940px;height:600px;opacity:' + g.toFixed(3) + '"></div>',
      heroTop: 760, align: 'left', left: 130, width: 820 };
  },

  quote: (b, u, t) => {
    const g = ease(clamp(u / .3, 0, 1));
    const n = (b.quote || '').length;
    // Reveal across the whole quote GROUP, in absolute time. Keyed to u it
    // restarted on every beat, so a two-beat quote typed out, cut, and typed
    // again -- the thesis line read "never one numb" for half its screen time.
    const q0 = b.qt0 !== undefined ? b.qt0 : b.t0;
    const q1 = b.qt1 !== undefined ? b.qt1 : b.t1;
    const qu = clamp((t - q0) / Math.max(0.1, q1 - q0), 0, 1);
    const shown = (b.quote || '').slice(0, Math.ceil(n * clamp((qu - .04) / .26, 0, 1)));
    return { chrome:
      '<div class="cardbox" style="left:60px;top:' + (700 + (1 - g) * 40).toFixed(0) +
        'px;width:960px;height:' + (b.quoteH || 420) + 'px;opacity:' + g.toFixed(3) + '"></div>' +
      // A statement card, NOT a quotation. It previously set the script's own
      // paraphrase in quote marks under an attribution rule, inventing a sourced
      // quote -- on a channel whose whole pitch is accuracy, in a video about
      // people misreading a published number. The primary source is DNS-blocked
      // here, so a real verbatim quote is not available either.
      '<div style="position:absolute;left:118px;top:' + (742 + (1 - g) * 40).toFixed(0) +
        'px;width:92px;height:7px;background:' + LOOK.accent + ';opacity:' + g.toFixed(3) + '"></div>' +
      '<div class="qt" style="left:118px;top:' + (790 + (1 - g) * 40).toFixed(0) +
        'px;width:844px;font-size:' + (b.quoteSize || 72) + 'px">' + shown + '</div>' +
      (b.who ? '<div class="lab" style="left:118px;top:' + (700 + (b.quoteH || 420) - 70) +
        'px;font-size:30px;opacity:' + ease(clamp((qu - .5) / .3, 0, 1)).toFixed(3) +
        '">' + b.who + '</div>' : ''),
      heroTop: -9999, align: 'center', left: 40, width: 1000 };
  },

  versus: (b, u) => {
    const v = b.vs || {}, g = ease(clamp(u / .3, 0, 1)), g2 = ease(clamp((u - .25) / .3, 0, 1));
    const col = (x, lab, val, hot, o) =>
      '<div class="cardbox" style="left:' + x + 'px;top:' + (660 + (1 - o) * 36).toFixed(0) +
        'px;width:452px;height:540px;opacity:' + o.toFixed(3) +
        (hot ? ';border:5px solid ' + LOOK.accent : '') + '"></div>' +
      '<div class="lab" style="left:' + (x + 48) + 'px;top:' + (708 + (1 - o) * 36).toFixed(0) +
        'px;font-size:30px;opacity:' + o.toFixed(3) + (hot ? ';color:' + LOOK.accent : '') + '">' + lab + '</div>' +
      '<div class="big" style="left:' + (x + 48) + 'px;top:' + (766 + (1 - o) * 36).toFixed(0) +
        'px;font-size:140px;opacity:' + o.toFixed(3) + (hot ? ';color:' + LOOK.accent : '') + '">' + val + '</div>';
    return { chrome: col(56, v.la || '', v.va || '', false, g) + col(572, v.lb || '', v.vb || '', true, g2),
      heroTop: -9999, align: 'center', left: 40, width: 1000 };
  },

  band: (b, u) => {
    // The hero is near-black by design, reversed out of the amber band. While
    // the band wiped in, the uncovered part of the word was near-black type on
    // a 170-luma plate -- about 2.2s of unreadable hero across five beats. The
    // wipe is quicker now and the hero waits for it.
    const w = 1080 * ease(clamp(u / .16, 0, 1));
    return { chrome: '<div class="band" style="left:0;top:' + (b.bandY || 780) +
        'px;width:' + w.toFixed(0) + 'px;height:330px"></div>',
      heroTop: (b.bandY || 780) + 42, align: 'center', left: 40, width: 1000,
      subTop: (b.bandY || 780) - 96, color: LOOK.ground,
      heroOpacity: ease(clamp((u - 0.14) / 0.10, 0, 1)) };
  },
};

// Resolve only after the browser has actually painted. Without this the first
// frame of a render captures an unpainted stage: a white blank, which on a
// Short is the thumbnail the whole feed sees.
window.painted = () => new Promise(r =>
  requestAnimationFrame(() => requestAnimationFrame(r)));

window.setFrame = async function (t) {
  let bi = 0;
  for (let i = 0; i < BEATS.length; i++) if (t >= BEATS[i].t0) bi = i;
  const b = BEATS[bi], len = b.t1 - b.t0, u = clamp((t - b.t0) / len, 0, 1);

  // BASE: every beat moves. Push/pull/drift with parallax against the type.
  document.querySelectorAll('.plate').forEach((e, i) =>
    e.classList.toggle('on', PLATES[i] === b.plate));
  const el = document.querySelector('.plate.on');
  if (el) {
    // Point the plate at the right pre-decoded frame. The clip loops if the
    // beat outruns it, which is what the old modulo on currentTime did.
    const f = FRAMES[b.plate];
    const idx = Math.round(((b.pt0 || 0) + (t - b.t0)) * FPS) % f.n;
    const src = f.dir + '/' + String(idx + 1).padStart(5, '0') + '.jpg';
    if (el.getAttribute('src') !== src) {
      el.src = src;
      try { await el.decode(); } catch (e) { /* first paint can race; next frame covers it */ }
    }
    const amp = b.move === 'pull' ? -1 : 1;
    const sc = 1.0 + (b.move === 'pull' ? 0.14 - 0.14 * u : 0.14 * u);
    const dx = (b.move === 'driftL' ? -40 : b.move === 'driftR' ? 40 : 0) * u;
    const dy = (b.move === 'up' ? -34 : b.move === 'down' ? 34 : 0) * u * amp;
    el.style.transform = 'scale(' + (1.06 + sc * .9).toFixed(4) + ') translate(' + dx + 'px,' + dy + 'px)';
  }
  const lay = (LAY[b.layout] || LAY.full)(b, u, t);
  document.getElementById('chrome').innerHTML = lay.chrome;
  setMid(b, u);

  // TOP: hero letters arrive individually with overshoot. Never a whole-word fade.
  const hero = document.getElementById('hero');
  let txt;
  if (b.count) {
    const dv = b.count.div || 1;
    const raw = (b.count.from + (b.count.to - b.count.from) * ease(clamp(u / .55, 0, 1))) / dv;
    const dp = dv >= 100 ? 2 : (dv >= 10 ? 1 : 0);
    txt = (b.count.pre || '') + (raw >= 0 ? '' : '\u2212') +
          Math.abs(raw).toFixed(dp) + (b.count.suf || '');
  } else {
    txt = b.hero || '';
  }
  hero.className = b.red ? 'red' : '';
  hero.style.fontSize = (b.heroSize || 250) + 'px';
  hero.style.top = lay.heroTop + 'px';
  hero.style.left = lay.left + 'px';
  hero.style.width = lay.width + 'px';
  hero.style.textAlign = lay.align;
  hero.style.color = lay.color || '';
  hero.style.opacity = lay.heroOpacity !== undefined ? lay.heroOpacity : 1;
  hero.style.textShadow = lay.heroShadow || '';
  if (b.count) {
    hero.innerHTML = '<span class="l">' + txt + '</span>';
  } else {
    hero.innerHTML = [...txt].map((c, i) => {
      const s = b.heroInstant ? 1 : clamp((u - i * 0.022) / 0.16, 0, 1), o = ease(s);
      const over = 1 + 0.16 * Math.sin(Math.PI * s) * (1 - s);
      return '<span class="l" style="opacity:' + o.toFixed(3) +
        ';transform:translateY(' + ((1 - o) * 46).toFixed(1) + 'px) scale(' + over.toFixed(3) + ')">' +
        (c === ' ' ? '&nbsp;' : c) + '</span>';
    }).join('');
  }
  // Fit check. Words running off the frame is the single worst defect this
  // renderer has shipped, so the size is measured, never trusted.
  fitHero(hero, b.heroSize || 250, lay.width - 16);

  const sub = document.getElementById('sub');
  sub.textContent = b.sub || '';
  sub.style.fontSize = (b.subSize || 40) + 'px';
  sub.style.top = (lay.subTop !== undefined ? lay.subTop
                   : lay.heroTop - (b.subSize || 40) - 30) + 'px';
  sub.style.left = lay.left + 'px';
  sub.style.width = lay.width + 'px';
  sub.style.textAlign = lay.align;
  sub.style.opacity = b.heroInstant ? 1 : ease(clamp(u / .18, 0, 1));
  const note = document.getElementById('note');
  note.textContent = b.note || '';
  note.style.top = (lay.heroTop + (b.heroSize || 250) * 0.92 + 26) + 'px';
  note.style.left = lay.left + 'px';
  note.style.width = lay.width + 'px';
  note.style.textAlign = lay.align;
  note.style.opacity = ease(clamp((u - .18) / .25, 0, 1));

  // Transitions. No plain cuts: whip out, or a giant word wipes the frame.
  const st = document.getElementById('stage');
  const tail = clamp((u - 0.88) / 0.12, 0, 1);
  if (b.trans === 'whip' && tail > 0) {
    st.style.transform = 'translateX(' + (-tail * 190).toFixed(1) + 'px)';
    st.style.filter = 'blur(' + (tail * 16).toFixed(1) + 'px)';
  } else if (b.trans === 'whipUp' && tail > 0) {
    st.style.transform = 'translateY(' + (-tail * 190).toFixed(1) + 'px)';
    st.style.filter = 'blur(' + (tail * 16).toFixed(1) + 'px)';
  } else { st.style.transform = ''; st.style.filter = ''; }
  const head = clamp(u / 0.10, 0, 1);
  if (bi > 0 && BEATS[bi - 1].trans && BEATS[bi - 1].trans.startsWith('whip')) {
    const d = (1 - ease(head)) * 190;
    st.style.transform = BEATS[bi - 1].trans === 'whipUp'
      ? 'translateY(' + d + 'px)' : 'translateX(' + d + 'px)';
    st.style.filter = 'blur(' + ((1 - ease(head)) * 14).toFixed(1) + 'px)';
  }
  // 1-2 frame white impact flash on the biggest landings
  // The impact flash is a cut accent -- it needs something to cut FROM. On the
  // opening beat it fired at t=0 and made frame 0 an 82%-white blank, which on
  // a Short is the thumbnail the entire feed sees.
  document.getElementById('flash').style.opacity =
    (b.flash && u < 0.035 && bi > 0) ? 0.82 : 0;
  const card = document.getElementById('card');
  // The sourcing strip is what a PARADOCS10X video carries INSTEAD of a
  // disclaimer, so it runs the whole way. It previously died at the first plate
  // change 3.9s in -- on screen for 10% of the runtime, which is worse than a
  // considered decision not to have it.
  if (NOTICE) { card.innerHTML = '<b>' + NOTICE + '</b>'; card.style.display = 'block'; }
  else { card.style.display = 'none'; }

  // ---- host -------------------------------------------------------------
  if (HOST) {
    let pose = HOST.poses[0][1];
    for (const [pt, pn] of HOST.poses) if (t >= pt) pose = pn;
    const m = RIG[pose];
    document.querySelectorAll('.zp').forEach(e =>
      e.classList.toggle('on', e.id === 'zp-' + pose));
    const host = document.getElementById('host');
    const sc = (HOST.h || 420) / m.h;
    host.style.transform = 'translate(' + (HOST.x - (HOST.anchor === 'right' ? m.w * sc : 0))
      + 'px,' + (HOST.y - m.h * sc) + 'px) scale(' + sc.toFixed(4) + ')';
    const el = document.getElementById('zp-' + pose);
    // Breathe, and let the head lead it slightly so the neck reads as a joint.
    const br = Math.sin(t * 2.0) * 1.6 + Math.sin(t * 3.7) * 0.6;
    const tilt = Math.sin(t * 1.15) * 1.6;
    el.querySelector('.zb').style.transform = 'translateY(' + (br * 0.45).toFixed(2) + 'px)';
    el.querySelector('.zh').style.transform =
      'translateY(' + br.toFixed(2) + 'px) rotate(' + tilt.toFixed(2) + 'deg)';
    // Blush comes and goes rather than sitting there: a constant flush reads
    // as a painted doll. A cubed slow sine spends most of its ~15s cycle near
    // zero and swells once, and emphatic poses add to it.
    const zc = el.querySelector('.zc');
    if (zc) {
      const sw = Math.max(0, Math.sin(t * 0.42 + 1.1));
      let bl = Math.pow(sw, 3) * 0.5;
      if (pose.indexOf('shock') >= 0) bl += 0.45;
      else if (pose.indexOf('skeptical') >= 0) bl += 0.18;
      zc.setAttribute('opacity', Math.min(0.8, bl).toFixed(3));
    }
    const sv = el.querySelector('.zm');
    if (sv && m.mouth) {
      // Lip-flap off the measured word timings, drawn where the sheet's own
      // mouth was. Closed is the flat line; open is a lens.
      let o = 0;
      for (const wd of WORDS) {
        if (t >= wd.t0 && t < wd.t1) {
          const u = (t - wd.t0) / Math.max(0.08, wd.t1 - wd.t0);
          o = Math.pow(Math.sin(Math.PI * Math.min(1, u)), 0.6) *
              (0.72 + 0.28 * Math.abs(Math.sin(t * 27)));
          break;
        }
        if (wd.t0 > t) break;
      }
      const [mx0, my0, mx1, my1] = m.mouth;
      const cx = (mx0 + mx1) / 2, cy = (my0 + my1) / 2;
      const hw = Math.max(7, (mx1 - mx0) * 0.42);
      const hh = 1.4 + o * (my1 - my0) * 0.95;
      sv.querySelector('path').setAttribute('d',
        'M ' + (cx - hw) + ' ' + cy + ' Q ' + cx + ' ' + (cy + hh) + ' ' + (cx + hw) + ' ' + cy +
        ' Q ' + cx + ' ' + (cy - hh * 0.55) + ' ' + (cx - hw) + ' ' + cy + ' Z');
      sv.querySelector('path').setAttribute('fill', o > 0.12 ? '#111' : 'none');
      sv.querySelector('path').setAttribute('stroke', '#111');
      sv.querySelector('path').setAttribute('stroke-width', '5');
      sv.querySelector('path').setAttribute('stroke-linecap', 'round');
    }
  }

  // Captions: the sentence the current word is in, white with heavy black stroke.
  let cur = -1;
  for (let i = 0; i < WORDS.length; i++) {
    if (t >= WORDS[i].t0 && t < WORDS[i].t1) { cur = i; break; }
    if (WORDS[i].t0 > t) break;
    cur = i;
  }
  const cap = document.getElementById('cap');
  if (cur < 0) { cap.innerHTML = ''; return; }
  let a = cur, z = cur;
  while (a > 0 && !/[.!?]$/.test(WORDS[a - 1].w)) a--;
  while (z < WORDS.length - 1 && !/[.!?]$/.test(WORDS[z].w)) z++;
  let out = '';
  for (let i = a; i <= z; i++) out += '<span class="' + (i === cur ? 'now' : '') + '">' + WORDS[i].w + '</span>';
  cap.innerHTML = out;
};
</script>`;
const page = path.join(path.dirname(OUT), '_reel.html');
fs.writeFileSync(page, html);

(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(page), { waitUntil: 'load' });
  // Every plate must have real pixels before a single frame is captured.
  await p.waitForFunction("document.querySelectorAll('img.plate').length > 0",
                          { timeout: 30000 });
  // PROBE=t1,t2,... dumps stills at those times and exits. A layout change can
  // then be checked in seconds rather than by sitting through a full render.
  if (process.env.PROBE) {
    const dir = path.join(path.dirname(OUT), 'qc');
    fs.mkdirSync(dir, { recursive: true });
    for (const t of process.env.PROBE.split(',').map(Number)) {
      await p.evaluate(async tt => { await window.setFrame(tt); await window.painted(); }, t);
      await p.screenshot({ path: path.join(dir, 'probe-' + t.toFixed(2) + '.png') });
    }
    await b.close();
    console.log('probe stills in ' + dir);
    return;
  }
  const ff = spawn(FF, [
    '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(FPS), '-i', 'pipe:0',
    '-i', path.resolve(AUDIO), '-map', '0:v:0', '-map', '1:a:0',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p',
    '-r', String(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
    '-movflags', '+faststart', OUT,
  ], { stdio: ['pipe', 'ignore', 'pipe'] });
  let err = ''; ff.stderr.on('data', d => { err = (err + d).slice(-4000); });
  // Capture in parallel. One page is bounded by the screenshot encode (~84ms),
  // so a single sequential pass can never beat ~12fps however cheap the frame
  // is to build. Each worker owns a contiguous slice, writes numbered JPEGs,
  // and ffmpeg assembles them in order afterwards -- which keeps the output
  // byte-identical to the sequential path.
  const total = Math.round(DUR * FPS), t0 = Date.now();
  const WORKERS = Math.max(1, Math.min(+(process.env.WORKERS || 4), 8));
  const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'reel-'));
  let done = 0;
  const slice = Math.ceil(total / WORKERS);

  const worker = async (w, pg) => {
    const lo = w * slice, hi = Math.min(total, lo + slice);
    for (let n = lo; n < hi; n++) {
      await pg.evaluate(async t => { await window.setFrame(t); await window.painted(); }, n / FPS);
      await pg.screenshot({ path: path.join(tmp, String(n).padStart(6, '0') + '.jpg'),
                            type: 'jpeg', quality: 90 });
      if (++done % 60 === 0)
        console.log(`  ${done}/${total}  ${(done / ((Date.now() - t0) / 1000)).toFixed(1)} fps`);
    }
  };

  // Separate BROWSERS, not separate tabs. Four pages in one browser only
  // reached 0.7 of a core: screenshot capture serialises on the shared
  // compositor, so the extra pages mostly waited.
  const browsers = [], pages = [p];
  for (let w = 1; w < WORKERS; w++) {
    const bb = await chromium.launch({ args: ['--no-sandbox'] });
    const pg = await bb.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
    await pg.goto('file://' + path.resolve(page), { waitUntil: 'load' });
    browsers.push(bb); pages.push(pg);
  }
  await Promise.all(pages.map((pg, w) => worker(w, pg)));
  for (const bb of browsers) await bb.close();

  for (let n = 0; n < total; n++) {
    const buf = fs.readFileSync(path.join(tmp, String(n).padStart(6, '0') + '.jpg'));
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  fs.rmSync(tmp, { recursive: true, force: true });
  ff.stdin.end();
  const code = await new Promise(r => ff.on('close', r));
  await b.close();
  if (code !== 0) { console.error(err); throw new Error('ffmpeg exit ' + code); }
  console.log(`${OUT} — ${total} frames @ ${FPS}fps = ${(total / FPS).toFixed(2)}s`);
})();
