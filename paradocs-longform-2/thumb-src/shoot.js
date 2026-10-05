const { chromium } = require('playwright');
const path = require('path');
const jobs = [
  ['lf-a.html', 1280, 720,  'thumb-longform-A.png'],
  ['lf-b.html', 1280, 720,  'thumb-longform-B.png'],
  ['s3.html',   1080, 1920, 'thumb-short3.png'],
  ['s4.html',   1080, 1920, 'thumb-short4.png'],
];
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  for (const [f, w, h, out] of jobs) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await p.goto('file://' + path.resolve(f), { waitUntil: 'networkidle' });
    await p.screenshot({ path: out, clip: { x: 0, y: 0, width: w, height: h } });
    await p.close();
    console.log('rendered', out, w + 'x' + h);
  }
  await b.close();
})();
