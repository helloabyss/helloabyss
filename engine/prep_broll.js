// Downscale + grade the licensed stock plates to the channel palette.
// Near-monochrome, dark, contrasty: the three-colour rule means imagery carries
// no colour of its own -- the only colour in frame is the red accent in the type.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const W = 1920, H = 1080;
const SRC = ['dish-array', 'datacentre', 'substation', 'wafer', 'racks'];
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: W, height: H } });
  for (const name of SRC) {
    const raw = fs.readFileSync(path.join('broll', name + '.jpg')).toString('base64');
    const out = await p.evaluate(async ([data, W, H]) => {
      const img = new Image();
      await new Promise(r => { img.onload = r; img.src = 'data:image/jpeg;base64,' + data; });
      const c = document.createElement('canvas');
      c.width = W; c.height = H;
      const x = c.getContext('2d');
      // grade, then cover-crop so no plate is ever stretched
      x.filter = 'grayscale(1) contrast(1.10) brightness(0.72)';
      const s = Math.max(W / img.width, H / img.height);
      const dw = img.width * s, dh = img.height * s;
      x.drawImage(img, (W - dw) / 2, (H - dh) / 2, dw, dh);
      return c.toDataURL('image/jpeg', 0.82).split(',')[1];
    }, [raw, W, H]);
    fs.writeFileSync(path.join('broll', name + '-graded.jpg'), Buffer.from(out, 'base64'));
    console.log(name, '->', (Buffer.from(out, 'base64').length / 1024).toFixed(0) + 'KB');
  }
  await b.close();
})();
