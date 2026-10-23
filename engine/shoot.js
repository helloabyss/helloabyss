// Renders every .html in a dir to .png at 1920x1080. node shoot.js [dir]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const dir = process.argv[2] || 'out';
(async () => {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  for (const f of files) {
    await p.goto('file://' + path.resolve(dir, f), { waitUntil: 'load' });
    await p.screenshot({ path: path.join(dir, f.replace('.html', '.png')),
                         clip: { x:0, y:0, width:1920, height:1080 } });
  }
  await b.close();
  console.log(files.length + ' PNGs rendered in ' + dir);
})();
