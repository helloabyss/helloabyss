// Frame-accurate render of poseanim.html to webm. node render_rig.js [secs] [fps]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const FF = '/opt/pw-browsers/ffmpeg-1011/ffmpeg-linux';
const SECS = +(process.argv[2] || 3), FPS = +(process.argv[3] || 24);
const W = 1920, H = 1080, NSC = 4;
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await p.goto('file://' + require('path').resolve('poseanim.html'), { waitUntil: 'load' });
  const ff = spawn(FF, ['-y','-f','image2pipe','-c:v','mjpeg','-framerate',String(FPS),
    '-i','pipe:0','-c:v','libvpx','-b:v','3M','-crf','12','-pix_fmt','yuv420p',
    '-deadline','realtime','-cpu-used','4','pose-demo.webm'], { stdio:['pipe','ignore','ignore'] });
  const per = Math.round(SECS * FPS);
  for (let s = 0; s < NSC; s++) {
    for (let f = 0; f < per; f++) {
      await p.evaluate(([a,b]) => window.setFrame(a,b), [s, f/(per-1)]);
      const buf = await p.screenshot({ type:'jpeg', quality:92, clip:{x:0,y:0,width:W,height:H} });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
  console.log('pose-demo.webm — ' + (NSC*per) + ' frames @ ' + FPS + 'fps');
})();
