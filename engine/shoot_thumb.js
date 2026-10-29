const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const dir = process.argv[2] || 'thumb';
const W = +(process.argv[3] || 1280), H = +(process.argv[4] || 720);
(async () => {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  for (const f of files) {
    await p.goto('file://' + path.resolve(dir, f), { waitUntil: 'load' });
    await p.screenshot({ path: path.join(dir, f.replace('.html', '.png')), clip: { x:0, y:0, width:W, height:H } });
  }
  await b.close(); console.log(files.length + ' @ ' + W + 'x' + H);
})();
