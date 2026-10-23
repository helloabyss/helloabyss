// Cuts transparent character parts out of the CANONICAL artwork.
// The shirt is white on a white page, so the background is removed by a
// flood fill from the border rather than a luminance key -- a key would
// delete the shirt along with the page.
const { chromium } = require('playwright');
const fs = require('fs');

const FIG = { x:142, y:60, w:197, h:638 };     // front figure, art/manifest.json
// Splits from the row profile: head ends 175, neck 176-207, hem 478.
const PARTS = {
  'o-head': { x:0,  y:0,   w:197, h:182, pivot:[97, 176] },  // incl. a little neck
  'o-body': { x:0,  y:168, w:197, h:470, pivot:[97,   8] },  // overlaps 168-182
};

(async () => {
  const b = await chromium.launch({ args:['--no-sandbox'] });
  const p = await b.newPage();
  const b64 = fs.readFileSync('art/zul-sheet.jpg').toString('base64');
  await p.setContent('<img id=i src="data:image/jpeg;base64,' + b64 + '">');
  const out = await p.evaluate(async ({FIG, PARTS}) => {
    const img = document.getElementById('i'); await img.decode();
    const W = img.naturalWidth, H = img.naturalHeight;
    const c = document.createElement('canvas'); c.width=W; c.height=H;
    const g = c.getContext('2d'); g.drawImage(img,0,0);
    const im = g.getImageData(0,0,W,H), d = im.data;
    const lum = i => 0.299*d[i] + 0.587*d[i+1] + 0.114*d[i+2];

    // Flood fill the page from every border pixel through near-white.
    const bg = new Uint8Array(W*H);
    const stack = [];
    for (let x=0;x<W;x++){ stack.push(x, x+(H-1)*W); }
    for (let y=0;y<H;y++){ stack.push(y*W, W-1+y*W); }
    while (stack.length){
      const q = stack.pop();
      if (bg[q]) continue;
      if (lum(q*4) < 238) continue;          // hit ink: stop
      bg[q] = 1;
      const x = q % W, y = (q - x)/W;
      if (x>0)   stack.push(q-1);
      if (x<W-1) stack.push(q+1);
      if (y>0)   stack.push(q-W);
      if (y<H-1) stack.push(q+W);
    }
    // Dilate the background one pixel into anything still near-white. JPEG
    // edges are soft, so pixels just under the fill threshold survive as a
    // pale halo around the figure once it sits on a dark plate.
    const grow = new Uint8Array(bg);
    for (let y=1;y<H-1;y++) for (let x=1;x<W-1;x++){
      const q=y*W+x;
      if (bg[q]) continue;
      if (lum(q*4) < 200) continue;
      if (bg[q-1]||bg[q+1]||bg[q-W]||bg[q+W]) grow[q]=1;
    }
    for (let i=0;i<W*H;i++) if (grow[i]) d[i*4+3] = 0;
    bg.set(grow);
    g.putImageData(im,0,0);

    const res = {};
    for (const [name, P] of Object.entries(PARTS)){
      const o = document.createElement('canvas');
      o.width = P.w*2; o.height = P.h*2;                 // 2x for crispness
      const og = o.getContext('2d');
      og.imageSmoothingQuality = 'high';
      og.drawImage(c, FIG.x+P.x, FIG.y+P.y, P.w, P.h, 0, 0, P.w*2, P.h*2);
      res[name] = { png: o.toDataURL('image/png'), w:P.w, h:P.h, pivot:P.pivot };
    }
    // how much of the page got removed, as a sanity check
    let cleared=0; for (let i=0;i<W*H;i++) if (bg[i]) cleared++;
    res._stats = { cleared, pct: (100*cleared/(W*H)).toFixed(1) };
    return res;
  }, {FIG, PARTS});

  const man = {};
  for (const [name, r] of Object.entries(out)){
    if (name === '_stats') continue;
    fs.writeFileSync('parts/'+name+'.png',
      Buffer.from(r.png.split(',')[1], 'base64'));
    man[name] = { file:name+'.png', w:r.w, h:r.h, pivot:r.pivot };
  }
  fs.writeFileSync('parts/manifest-original.json', JSON.stringify(man, null, 1));
  console.log('background cleared: ' + out._stats.pct + '% of page');
  console.log(Object.keys(man).map(k=>k+' '+man[k].w+'x'+man[k].h+' pivot '+man[k].pivot).join('\n'));
  await b.close();
})();
