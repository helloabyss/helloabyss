// Segments a white-background art sheet into its figures and prints crop boxes.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage();
  const out = {};
  for (const [key, file] of Object.entries({ sheet:'art/zul-sheet.jpg', face:'art/zul-face.jpg' })) {
    const b64 = fs.readFileSync(file).toString('base64');
    await p.setContent('<img id=i src="data:image/jpeg;base64,' + b64 + '">');
    out[key] = await p.evaluate(async () => {
      const img = document.getElementById('i'); await img.decode();
      const c = document.createElement('canvas');
      c.width = img.naturalWidth; c.height = img.naturalHeight;
      const g = c.getContext('2d'); g.drawImage(img, 0, 0);
      const d = g.getImageData(0,0,c.width,c.height).data;
      const ink = (x,y) => { const i=(y*c.width+x)*4; return d[i]<235||d[i+1]<235||d[i+2]<235; };
      // column occupancy -> split on runs of empty columns
      const col = []; for (let x=0;x<c.width;x++){ let n=0; for(let y=0;y<c.height;y++) if(ink(x,y)) n++; col.push(n); }
      const groups = []; let s = -1;
      for (let x=0;x<c.width;x++){
        if (col[x]>0 && s<0) s = x;
        if ((col[x]===0 || x===c.width-1) && s>=0){ if (x-s > 40) groups.push([s, x]); s = -1; }
      }
      const boxes = groups.map(([x0,x1]) => {
        let y0=c.height, y1=0;
        for (let y=0;y<c.height;y++) for (let x=x0;x<=x1;x++) if (ink(x,y)){ if(y<y0)y0=y; if(y>y1)y1=y; break; }
        for (let y=c.height-1;y>=0;y--){ let hit=false; for (let x=x0;x<=x1;x++) if(ink(x,y)){hit=true;break;} if(hit){y1=y;break;} }
        return { x: x0, y: y0, w: x1-x0+1, h: y1-y0+1 };
      });
      return { w: c.width, h: c.height, figures: boxes };
    });
  }
  console.log(JSON.stringify(out, null, 1));
  await b.close();
})();
