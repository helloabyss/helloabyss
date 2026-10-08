// Render the animated timeline straight to H.264 MP4 with the narration muxed in
// the same pass. Playwright's bundled ffmpeg can only write VP8 webm and has no
// audio codecs at all; imageio-ffmpeg's static build (7.0.2) has libx264, aac and
// an mp3 decoder, so the whole deliverable comes out of one command.
const { chromium } = require('playwright');
const { spawn, execSync } = require('child_process');
const fs = require('fs'), path = require('path');
const FF = execSync("python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'")
            .toString().trim();
const VO = path.resolve('../ai-picks-longform/vo-full.mp3');
const OUT = 'ai-picks-longform.mp4';
const W = 1920, H = 1080;
const D = JSON.parse(fs.readFileSync('aip-durations.json')).durations;
const STILLS = process.argv[2] === 'stills';
const FPS = STILLS ? 12 : +(process.argv[2] || 20);

(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve('aip-anim.html'), { waitUntil: 'load' });
  const n = await p.evaluate(() => window.NSC);
  if (n !== D.length) throw new Error('scene count ' + n + ' != durations ' + D.length);

  if (STILLS) {
    fs.mkdirSync('animstills', { recursive: true });
    for (const s of [0, 3, 7, 14, 15, 17, 22, 24, 28, 31, 32, 37, 41]) {
      for (const t of [0.4, 0.92]) {
        await p.evaluate(([a, c]) => window.setFrame(a, c), [s, t]);
        await p.screenshot({ path: `animstills/${String(s).padStart(2,'0')}-${t*100|0}.png` });
      }
    }
    await b.close(); console.log('animstills/ written'); return;
  }

  const ff = spawn(FF, [
    '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(FPS), '-i', 'pipe:0',
    '-i', VO,
    '-map', '0:v:0', '-map', '1:a:0',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
    '-r', String(FPS), '-c:a', 'aac', '-b:a', '160k',
    '-shortest', '-movflags', '+faststart', OUT,
  ], { stdio: ['pipe', 'ignore', 'pipe'] });
  let err = '';
  ff.stderr.on('data', d => { err += d; if (err.length > 40000) err = err.slice(-20000); });

  const TOTFR = D.reduce((a, d) => a + Math.max(1, Math.round(d * FPS)), 0);
  const t0 = Date.now();
  let total = 0;
  for (let s = 0; s < D.length; s++) {
    const fr = Math.max(1, Math.round(D[s] * FPS));
    for (let f = 0; f < fr; f++) {
      await p.evaluate(([a, c]) => window.setFrame(a, c), [s, fr > 1 ? f / (fr - 1) : 0]);
      const buf = await p.screenshot({ type: 'jpeg', quality: 86,
                                       clip: { x: 0, y: 0, width: W, height: H } });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      total++;
    }
    if (s % 4 === 0 || s === D.length - 1) {
      const el = (Date.now() - t0) / 1000, rate = total / el;
      console.log(`  beat ${s+1}/${D.length}  ${total}/${TOTFR} frames  ${rate.toFixed(1)} fps  ~${((TOTFR-total)/rate/60).toFixed(1)} min left`);
    }
  }
  ff.stdin.end();
  const code = await new Promise(r => ff.on('close', r));
  await b.close();
  if (code !== 0) { console.error(err.slice(-3000)); throw new Error('ffmpeg exit ' + code); }
  console.log(`${OUT} — ${total} frames @ ${FPS}fps = ${(total/FPS).toFixed(2)}s`);
})();
