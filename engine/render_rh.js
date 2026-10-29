// Render a stills folder to a finished H.264 MP4 with narration muxed, in one pass.
//
// Differs from render_video.js in two ways that matter:
//   1. Per-scene durations read from durations.json, not a flat seconds-per-scene.
//      A uniform hold is what makes picture drift against voice over a long runtime.
//   2. imageio-ffmpeg's full ffmpeg, so the output is H.264 + AAC MP4 with the audio
//      already in it. Playwright's stripped build could only write silent VP8.
const { chromium } = require('playwright');
const { spawn, execSync } = require('child_process');
const fs = require('fs'), path = require('path');

const DIR = process.argv[2], AUDIO = process.argv[3], OUT = process.argv[4];
const FPS = +(process.argv[5] || 12);
const FF = execSync("python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'")
            .toString().trim();
const man = JSON.parse(fs.readFileSync(path.join(DIR, 'manifest.json')));
const W = 1920, H = 1080;

// entry pop then slow push — the channel's established scene motion
const page = `<!doctype html><meta charset="utf-8"><style>
*{margin:0;padding:0}html,body{width:${W}px;height:${H}px;background:#fff;overflow:hidden}
img{position:absolute;left:0;top:0;width:${W}px;height:${H}px;display:none;
    transform-origin:50% 50%}
img.on{display:block}</style>
${man.map((m,i)=>`<img id="s${i}" src="file://${path.resolve(DIR)}/${m.png}">`).join('')}
<script>
window.setFrame=function(s,t){
  const im=document.querySelectorAll('img');
  im.forEach((e,i)=>e.classList.toggle('on',i===s));
  const pop = t<0.04 ? (t/0.04)*3.5 : 3.5;      // fast entry pop
  const push = 2.0*t;                            // slow linear push
  im[s].style.transform='scale('+(1+(pop+push)/100).toFixed(5)+')';
};</script>`;
fs.writeFileSync(path.join(DIR, '_player.html'), page);

(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(DIR, '_player.html'), { waitUntil: 'load' });
  const ff = spawn(FF, [
    '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(FPS), '-i', 'pipe:0',
    '-i', path.resolve(AUDIO),
    '-map', '0:v:0', '-map', '1:a:0',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
    '-r', String(FPS), '-c:a', 'aac', '-b:a', '192k', '-ac', '2',
    '-movflags', '+faststart', OUT,
  ], { stdio: ['pipe', 'ignore', 'pipe'] });
  let err = ''; ff.stderr.on('data', d => { err = (err + d).slice(-4000); });

  const total = man.reduce((a, m) => a + Math.max(1, Math.round(m.seconds * FPS)), 0);
  const t0 = Date.now(); let n = 0;
  for (let s = 0; s < man.length; s++) {
    const fr = Math.max(1, Math.round(man[s].seconds * FPS));
    for (let f = 0; f < fr; f++) {
      await p.evaluate(([a, c]) => window.setFrame(a, c), [s, fr > 1 ? f / (fr - 1) : 0]);
      const buf = await p.screenshot({ type: 'jpeg', quality: 88 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      n++;
    }
    const el = (Date.now() - t0) / 1000, rate = n / el;
    console.log(`  scene ${s+1}/${man.length}  ${n}/${total}  ${rate.toFixed(1)} fps  ~${((total-n)/rate/60).toFixed(1)} min left`);
  }
  ff.stdin.end();
  const code = await new Promise(r => ff.on('close', r));
  await b.close();
  if (code !== 0) { console.error(err); throw new Error('ffmpeg exit ' + code); }
  console.log(`${OUT} — ${n} frames @ ${FPS}fps = ${(n/FPS).toFixed(2)}s`);
})();
