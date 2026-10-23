const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.goto('file://' + require('path').resolve('bounds.html'), { waitUntil:'load' });
  const r = await p.evaluate(async () => {
    const img = document.getElementById('i');
    await img.decode();
    const c = document.createElement('canvas');
    c.width = img.naturalWidth; c.height = img.naturalHeight;
    const x = c.getContext('2d'); x.drawImage(img, 0, 0);
    const d = x.getImageData(0, 0, c.width, c.height).data;
    let x0=c.width, y0=c.height, x1=0, y1=0;
    for (let yy=0; yy<c.height; yy++) for (let xx=0; xx<c.width; xx++) {
      const i=(yy*c.width+xx)*4;
      if (d[i]<235 || d[i+1]<235 || d[i+2]<235) {
        if(xx<x0)x0=xx; if(xx>x1)x1=xx; if(yy<y0)y0=yy; if(yy>y1)y1=yy;
      }
    }
    return {w:c.width,h:c.height,x0,y0,x1,y1,cw:x1-x0,ch:y1-y0};
  });
  console.log(JSON.stringify(r));
  await b.close();
})();
