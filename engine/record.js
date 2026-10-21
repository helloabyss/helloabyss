// node record.js <player.html> <outdir> <seconds>
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const [file, dir, secs] = [process.argv[2], process.argv[3], Number(process.argv[4])];
  fs.mkdirSync(dir, { recursive: true });
  const b = await chromium.launch({ args: ['--no-sandbox','--disable-gpu-vsync','--force-device-scale-factor=1'] });
  const ctx = await b.newContext({ viewport:{width:1920,height:1080},
    recordVideo:{ dir, size:{width:1920,height:1080} } });
  const p = await ctx.newPage();
  await p.goto('file://' + path.resolve(file), { waitUntil: 'load' });
  await p.waitForTimeout(secs * 1000);
  await ctx.close(); await b.close();
  const f = fs.readdirSync(dir).filter(x=>x.endsWith('.webm'))[0];
  console.log('recorded', path.join(dir,f), (fs.statSync(path.join(dir,f)).size/1048576).toFixed(1)+' MB');
})();
