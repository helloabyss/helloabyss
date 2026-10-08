// Renders each .html in a dir to a TRANSPARENT png at its own svg size.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const dir = process.argv[2] || 'parts';
(async () => {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 800, height: 800 }, deviceScaleFactor: 2 });
  for (const f of files) {
    await p.goto('file://' + path.resolve(dir, f), { waitUntil: 'load' });
    const el = await p.$('svg');
    await el.screenshot({ path: path.join(dir, f.replace('.html', '.png')), omitBackground: true });
  }
  await b.close(); console.log(files.length + ' transparent parts');
})();
