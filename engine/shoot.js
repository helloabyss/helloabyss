// Renders every .html in a dir to .png. Canvas comes from canvas.json when the
// build wrote one (portrait shorts), else 1920x1080. node shoot.js [dir]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const dir = process.argv[2] || 'out';
(async () => {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const _cv = require('fs').existsSync(path.join(dir,'canvas.json'))
    ? JSON.parse(require('fs').readFileSync(path.join(dir,'canvas.json')))
    : { w: 1920, h: 1080 };
  const p = await b.newPage({ viewport: { width: _cv.w, height: _cv.h }, deviceScaleFactor: 1 });
  for (const f of files) {
    await p.goto('file://' + path.resolve(dir, f), { waitUntil: 'load' });
    await p.screenshot({ path: path.join(dir, f.replace('.html', '.png')),
                         clip: { x:0, y:0, width:_cv.w, height:_cv.h } });
  }
  await b.close();
  console.log(files.length + ' PNGs rendered in ' + dir);
})();
