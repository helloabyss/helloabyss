// Portrait short -> finished H.264 + AAC MP4, one pass.
//
// Differs from render_rh.js: canvas comes from canvas.json (so portrait stops
// being cropped to 1920x1080), captions are burned in word by word from
// captions.json, and the compliance card is held over the first 4 seconds.
//
//   node render_short.js <stills-dir> <audio.wav> <out.mp4> <captions.json> [fps]
const { chromium } = require('playwright');
const { spawn, execSync } = require('child_process');
const fs = require('fs'), path = require('path');

const DIR = process.argv[2], AUDIO = process.argv[3], OUT = process.argv[4];
const CAPS = process.argv[5];
const FPS = +(process.argv[6] || 24);
const FF = execSync("python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'")
            .toString().trim();
const man = JSON.parse(fs.readFileSync(path.join(DIR, 'manifest.json')));
const cv = JSON.parse(fs.readFileSync(path.join(DIR, 'canvas.json')));
const words = JSON.parse(fs.readFileSync(CAPS)).words;
const W = cv.w, H = cv.h;
const CARD = 4.0;   // compliance card, seconds

const html = `<!doctype html><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${W}px;height:${H}px;background:#fff;overflow:hidden;
  font-family:"Liberation Sans",Arial,sans-serif}
#st{position:absolute;inset:0}
#st img{position:absolute;left:0;top:0;width:${W}px;height:${H}px;display:none;
  transform-origin:50% 50%}
#st img.on{display:block}
/* Caption band. Art is kept clear of 1440-1600 by scenes-ale.py. */
#cap{position:absolute;left:50px;top:1430px;width:${W - 100}px;height:190px;
  display:flex;align-items:center;justify-content:center;flex-wrap:wrap;
  gap:0 16px;font-size:60px;font-weight:800;line-height:1.12;text-align:center}
#cap span{color:#111}
#cap span.now{color:#d81e28}
#card{position:absolute;left:0;top:118px;width:${W}px;text-align:center;
  font-size:34px;font-weight:700;color:#111;letter-spacing:.4px}
#card b{border:4px solid #111;padding:12px 26px;display:inline-block;font-weight:700}
</style>
<div id="st">${man.map((m, i) => `<img id="s${i}" src="file://${path.resolve(DIR)}/${m.png}">`).join('')}</div>
<div id="cap"></div><div id="card"><b>Educational only. Not financial advice.</b></div>
<script>
const WORDS = ${JSON.stringify(words)};
const CARD = ${CARD};
window.setFrame = function (s, t, abs) {
  const im = document.querySelectorAll('#st img');
  im.forEach((e, i) => e.classList.toggle('on', i === s));
  const pop = t < 0.04 ? (t / 0.04) * 3.5 : 3.5;   // house entry pop
  const push = 2.0 * t;                             // house slow push
  im[s].style.transform = 'scale(' + (1 + (pop + push) / 100).toFixed(5) + ')';
  document.getElementById('card').style.display = abs < CARD ? 'block' : 'none';
  // Caption shows the sentence the current word belongs to.
  let cur = -1;
  for (let i = 0; i < WORDS.length; i++) {
    if (abs >= WORDS[i].t0 && abs < WORDS[i].t1) { cur = i; break; }
    if (WORDS[i].t0 > abs) break;
    cur = i;
  }
  const cap = document.getElementById('cap');
  if (cur < 0) { cap.innerHTML = ''; return; }
  let a = cur, b = cur;
  while (a > 0 && !/[.!?]$/.test(WORDS[a - 1].w)) a--;
  while (b < WORDS.length - 1 && !/[.!?]$/.test(WORDS[b].w)) b++;
  let out = '';
  for (let i = a; i <= b; i++) out += '<span class="' + (i === cur ? 'now' : '') + '">' + WORDS[i].w + '</span>';
  cap.innerHTML = out;
};
</script>`;
fs.writeFileSync(path.join(DIR, '_short.html'), html);

(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(DIR, '_short.html'), { waitUntil: 'load' });
  const ff = spawn(FF, [
    '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(FPS), '-i', 'pipe:0',
    '-i', path.resolve(AUDIO),
    '-map', '0:v:0', '-map', '1:a:0',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p',
    '-r', String(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
    '-movflags', '+faststart', OUT,
  ], { stdio: ['pipe', 'ignore', 'pipe'] });
  let err = ''; ff.stderr.on('data', d => { err = (err + d).slice(-4000); });

  const total = man.reduce((a, m) => a + Math.max(1, Math.round(m.seconds * FPS)), 0);
  const t0 = Date.now(); let n = 0, abs = 0;
  for (let s = 0; s < man.length; s++) {
    const fr = Math.max(1, Math.round(man[s].seconds * FPS));
    for (let f = 0; f < fr; f++) {
      await p.evaluate(([a, c, d]) => window.setFrame(a, c, d),
                       [s, fr > 1 ? f / (fr - 1) : 0, abs]);
      const buf = await p.screenshot({ type: 'jpeg', quality: 90 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      n++; abs = n / FPS;
    }
    const el = (Date.now() - t0) / 1000;
    console.log(`  scene ${s + 1}/${man.length}  ${n}/${total}  ${(n / el).toFixed(1)} fps`);
  }
  ff.stdin.end();
  const code = await new Promise(r => ff.on('close', r));
  await b.close();
  if (code !== 0) { console.error(err); throw new Error('ffmpeg exit ' + code); }
  console.log(`${OUT} — ${n} frames @ ${FPS}fps = ${(n / FPS).toFixed(2)}s`);
})();
