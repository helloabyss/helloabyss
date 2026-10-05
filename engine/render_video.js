// node render_video.js <player.html> <out.webm> <scenes> [fps] [hold]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const FF = '/opt/pw-browsers/ffmpeg-1011/ffmpeg-linux';
(async () => {
  const file = process.argv[2], outf = process.argv[3];
  const NSC = Number(process.argv[4]);
  const FPS = Number(process.argv[5] || 12), HOLD = Number(process.argv[6] || 8);
  const per = Math.round(FPS * HOLD), total = per * NSC;
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(file), { waitUntil: 'load' });
  const ff = spawn(FF, ['-y','-f','image2pipe','-c:v','mjpeg','-framerate',String(FPS),
    '-i','pipe:0','-c:v','libvpx','-b:v','4M','-crf','10','-pix_fmt','yuv420p',
    '-deadline','realtime','-cpu-used','4', outf], { stdio:['pipe','ignore','ignore'] });
  const t0 = Date.now();
  for (let i = 0; i < total; i++) {
    const s = Math.floor(i / per), t = (i % per) / per;
    await p.evaluate(([s, t]) => window.setFrame(s, t), [s, t]);
    const buf = await p.screenshot({ type:'jpeg', quality:88, clip:{x:0,y:0,width:1920,height:1080} });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 200 === 0) process.stdout.write(`  ${i}/${total}  ${((Date.now()-t0)/1000).toFixed(0)}s\n`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
  console.log(`done ${total} frames in ${((Date.now()-t0)/1000).toFixed(0)}s -> ${outf}`);
})();
