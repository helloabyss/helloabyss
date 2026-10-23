const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.goto('file://' + require('path').resolve('_prof.html'), { waitUntil:'load' });
  const r = await p.evaluate(async () => {
    const img = document.getElementById('i'); await img.decode();
    const c = document.createElement('canvas');
    c.width = img.naturalWidth; c.height = img.naturalHeight;
    const g = c.getContext('2d'); g.drawImage(img,0,0);
    const d = g.getImageData(0,0,c.width,c.height).data;
    const ink=(x,y)=>{const i=(y*c.width+x)*4; return d[i]<235||d[i+1]<235||d[i+2]<235;};
    // front figure box from art/manifest.json
    const X0=142,Y0=60,W=197,H=638;
    const rows=[];
    for (let y=Y0; y<Y0+H; y++){
      let lo=1e9, hi=-1, n=0, runs=0, prev=false;
      for (let x=X0; x<X0+W; x++){
        const on=ink(x,y);
        if(on){ if(x<lo)lo=x; if(x>hi)hi=x; n++; }
        if(on&&!prev) runs++;
        prev=on;
      }
      rows.push({y, lo:lo===1e9?null:lo-X0, hi:hi<0?null:hi-X0, n, runs});
    }
    return {X0,Y0,W,H,rows};
  });
  // print a compact profile every 8px: width span and number of separate ink runs
  const out=[];
  for (let i=0;i<r.rows.length;i+=8){
    const q=r.rows[i];
    out.push(`y=${String(q.y).padStart(3)} rel=${String(q.y-r.Y0).padStart(3)} x[${q.lo}..${q.hi}] runs=${q.runs} ink=${q.n}`);
  }
  console.log(out.join('\n'));
  await b.close();
})();
