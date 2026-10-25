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
const W = 1080, H = 1920;
const DUR = beats[beats.length - 1].t1;
const abs = p => 'file://' + path.resolve(PLATES, p);
const plates = [...new Set(beats.map(b => b.plate).filter(Boolean))];

const html = `<!doctype html><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${W}px;height:${H}px;background:#07080a;overflow:hidden;
  font-family:"Liberation Sans Narrow","Liberation Sans",Arial,sans-serif}
#stage{position:absolute;inset:0;overflow:hidden}
/* BASE -- live photographic footage, graded on ingest by getplate.sh. The
   first version of this file used <img> and silently rendered black plates. */
.plate{position:absolute;left:-10%;top:-10%;width:120%;height:120%;
  object-fit:cover;display:none;will-change:transform}
.plate.on{display:block}
/* Near-black vignette so type always has something to sit on */
#vig{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(ellipse at 50% 42%,rgba(7,8,10,.12) 0%,rgba(7,8,10,.62) 58%,rgba(7,8,10,.93) 100%)}
#grain{position:absolute;inset:0;opacity:.055;pointer-events:none;mix-blend-mode:overlay}
/* MID -- motion graphics over the imagery */
#mid{position:absolute;inset:0}
.bar{position:absolute;height:26px;background:#d81e28}
.barbg{position:absolute;height:26px;border:4px solid rgba(255,255,255,.65)}
.tick{position:absolute;width:3px;background:rgba(255,255,255,.30)}
.rule{position:absolute;height:8px;background:#fff}
.rule.r{background:#d81e28}
/* TOP -- hero type and captions */
#hero{position:absolute;left:0;width:${W}px;text-align:center;color:#fff;
  font-weight:800;letter-spacing:-2px;line-height:.92;white-space:nowrap;
  text-shadow:0 10px 60px rgba(0,0,0,.85)}
#hero .l{display:inline-block;will-change:transform,opacity}
#hero.red{color:#d81e28}
#sub{position:absolute;left:0;width:${W}px;text-align:center;color:#fff;
  font-weight:700;letter-spacing:5px;text-transform:uppercase;
  text-shadow:0 4px 24px rgba(0,0,0,.9)}
#note{position:absolute;left:0;width:${W}px;text-align:center;color:rgba(255,255,255,.72);
  font-weight:700;font-size:30px;letter-spacing:1px;text-shadow:0 3px 14px rgba(0,0,0,.9)}
#cap{position:absolute;left:60px;top:1395px;width:${W - 120}px;height:200px;
  display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:0 15px;
  font-size:58px;font-weight:800;line-height:1.1;text-align:center}
#cap span{color:#fff;-webkit-text-stroke:9px #000;paint-order:stroke fill;
  text-shadow:0 5px 18px rgba(0,0,0,.95)}
#cap span.now{color:#d81e28}
#flash{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none}
#card{position:absolute;left:0;top:118px;width:${W}px;text-align:center}
#card b{display:inline-block;font-size:27px;font-weight:700;color:rgba(255,255,255,.93);
  padding:7px 20px;letter-spacing:2px;background:rgba(7,8,10,.62);
  border-left:4px solid #d81e28}
/* type-as-mask wipe: a giant word reveals the next beat through its counters */
#mask{position:absolute;inset:0;background:#07080a;display:none;
  -webkit-mask-repeat:no-repeat;-webkit-mask-position:center;mask-repeat:no-repeat;mask-position:center}
</style>
<div id="stage">
  ${plates.map((p, i) => `<video class="plate" id="p${i}" src="${abs(p)}" muted preload="auto" playsinline></video>`).join('')}
  <div id="vig"></div><div id="mid"></div>
  <div id="sub"></div><div id="hero"></div><div id="note"></div>
  <div id="mask"></div><div id="flash"></div><div id="cap"></div><div id="card"></div>
</div>
<script>
const BEATS = ${JSON.stringify(beats)};
const WORDS = ${JSON.stringify(words)};
const NOTICE = ${JSON.stringify(NOTICE)};
const PLATES = ${JSON.stringify(plates)};
const CARD = 4.0;
const ease = t => 1 - Math.pow(1 - t, 3);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

function setMid(b, u) {
  const m = document.getElementById('mid');
  if (!b.mid) { m.innerHTML = ''; return; }
  const g = b.mid; let h = '';
  if (g.type === 'bar') {
    // Proportional, always. Equal bars for unequal values is a lie this repo has told once.
    const mx = Math.max(g.a, g.b), wA = 820 * (g.a / mx), wB = 820 * (g.b / mx);
    const gw = ease(clamp(u / .55, 0, 1));
    h += '<div class="barbg" style="left:130px;top:' + g.y + 'px;width:820px"></div>';
    h += '<div class="bar" style="left:130px;top:' + g.y + 'px;width:' + (wA * gw) + 'px;background:#fff"></div>';
    h += '<div class="barbg" style="left:130px;top:' + (g.y + 72) + 'px;width:820px"></div>';
    h += '<div class="bar" style="left:130px;top:' + (g.y + 72) + 'px;width:' + (wB * gw) + 'px"></div>';
  } else if (g.type === 'grid') {
    // 1,400+ tasks -- a readable sample, not one square per task.
    const n = 120, lit = Math.floor(n * clamp(u / .7, 0, 1));
    for (let i = 0; i < n; i++) {
      const x = 150 + (i % 15) * 52, y = g.y + Math.floor(i / 15) * 52;
      h += '<div style="position:absolute;left:' + x + 'px;top:' + y + 'px;width:36px;height:36px;border:3px solid '
        + (i < lit ? 'rgba(255,255,255,.9)' : 'rgba(255,255,255,.18)') + '"></div>';
    }
  } else if (g.type === 'rule') {
    const w = 700 * ease(clamp(u / .4, 0, 1));
    h += '<div class="rule' + (g.red ? ' r' : '') + '" style="left:' + (540 - w / 2) + 'px;top:' + g.y + 'px;width:' + w + 'px"></div>';
  }
  m.innerHTML = h;
}

window.setFrame = async function (t) {
  let bi = 0;
  for (let i = 0; i < BEATS.length; i++) if (t >= BEATS[i].t0) bi = i;
  const b = BEATS[bi], len = b.t1 - b.t0, u = clamp((t - b.t0) / len, 0, 1);

  // BASE: every beat moves. Push/pull/drift with parallax against the type.
  document.querySelectorAll('.plate').forEach((e, i) =>
    e.classList.toggle('on', PLATES[i] === b.plate));
  const el = document.querySelector('.plate.on');
  if (el) {
    // Seek the plate to this beat's in-point plus elapsed, and WAIT for it.
    const want = Math.min(((b.pt0 || 0) + (t - b.t0)) % Math.max(0.1, el.duration || 6),
                          (el.duration || 6) - 0.05);
    if (Math.abs(el.currentTime - want) > 0.008) {
      el.currentTime = want;
      await new Promise(r => {
        let done = false;
        const fin = () => { if (!done) { done = true; el.removeEventListener('seeked', fin); r(); } };
        el.addEventListener('seeked', fin);
        setTimeout(fin, 400);
      });
    }
    const amp = b.move === 'pull' ? -1 : 1;
    const sc = 1.0 + (b.move === 'pull' ? 0.14 - 0.14 * u : 0.14 * u);
    const dx = (b.move === 'driftL' ? -40 : b.move === 'driftR' ? 40 : 0) * u;
    const dy = (b.move === 'up' ? -34 : b.move === 'down' ? 34 : 0) * u * amp;
    el.style.transform = 'scale(' + (1.06 + sc * .9).toFixed(4) + ') translate(' + dx + 'px,' + dy + 'px)';
  }
  setMid(b, u);

  // TOP: hero letters arrive individually with overshoot. Never a whole-word fade.
  const hero = document.getElementById('hero');
  const txt = b.count ? (b.count.pre || '') +
      Math.round(b.count.from + (b.count.to - b.count.from) * ease(clamp(u / .55, 0, 1))) +
      (b.count.suf || '') : (b.hero || '');
  hero.className = b.red ? 'red' : '';
  hero.style.fontSize = (b.heroSize || 250) + 'px';
  hero.style.top = (b.heroY || 520) + 'px';
  if (b.count) {
    hero.innerHTML = '<span class="l">' + txt + '</span>';
  } else {
    hero.innerHTML = [...txt].map((c, i) => {
      const s = clamp((u - i * 0.022) / 0.16, 0, 1), o = ease(s);
      const over = 1 + 0.16 * Math.sin(Math.PI * s) * (1 - s);
      return '<span class="l" style="opacity:' + o.toFixed(3) +
        ';transform:translateY(' + ((1 - o) * 46).toFixed(1) + 'px) scale(' + over.toFixed(3) + ')">' +
        (c === ' ' ? '&nbsp;' : c) + '</span>';
    }).join('');
  }
  const sub = document.getElementById('sub');
  sub.textContent = b.sub || '';
  sub.style.fontSize = (b.subSize || 40) + 'px';
  sub.style.top = ((b.heroY || 520) - (b.subSize || 40) - 30) + 'px';
  sub.style.opacity = ease(clamp(u / .18, 0, 1));
  const note = document.getElementById('note');
  note.textContent = b.note || '';
  note.style.top = ((b.heroY || 520) + (b.heroSize || 250) * 0.92 + 26) + 'px';
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
  document.getElementById('flash').style.opacity = (b.flash && u < 0.035) ? 0.82 : 0;
  const card = document.getElementById('card');
  if (NOTICE && t < CARD) { card.innerHTML = '<b>' + NOTICE + '</b>'; card.style.display = 'block'; }
  else { card.style.display = 'none'; }

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
  await p.waitForFunction(`Array.from(document.querySelectorAll('video'))
      .every(v => v.readyState >= 2 && v.videoWidth > 0)`, { timeout: 60000 });
  const ff = spawn(FF, [
    '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(FPS), '-i', 'pipe:0',
    '-i', path.resolve(AUDIO), '-map', '0:v:0', '-map', '1:a:0',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p',
    '-r', String(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
    '-movflags', '+faststart', OUT,
  ], { stdio: ['pipe', 'ignore', 'pipe'] });
  let err = ''; ff.stderr.on('data', d => { err = (err + d).slice(-4000); });
  const total = Math.round(DUR * FPS), t0 = Date.now();
  for (let n = 0; n < total; n++) {
    await p.evaluate(async t => await window.setFrame(t), n / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 90 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (n % 60 === 0) console.log(`  ${n}/${total}  ${(n / ((Date.now() - t0) / 1000)).toFixed(1)} fps`);
  }
  ff.stdin.end();
  const code = await new Promise(r => ff.on('close', r));
  await b.close();
  if (code !== 0) { console.error(err); throw new Error('ffmpeg exit ' + code); }
  console.log(`${OUT} — ${total} frames @ ${FPS}fps = ${(total / FPS).toFixed(2)}s`);
})();
