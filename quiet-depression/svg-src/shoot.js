const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  for (const f of ['s01','s07','s21']) {
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
    await p.goto('file://' + path.resolve(f + '.html'), { waitUntil: 'networkidle' });
    await p.screenshot({ path: f + '.png', clip: { x:0, y:0, width:1920, height:1080 } });
    await p.close();
    console.log('rendered', f + '.png');
  }
  await b.close();
})();
