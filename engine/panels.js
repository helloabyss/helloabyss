// Finds the panel rectangles in a contact sheet by detecting long dark runs.
const { chromium } = require('playwright');
const fs = require('fs');
const file = process.argv[2];
(async () => {
  const b = await chromium.launch({ args:['--no-sandbox'] });
  const p = await b.newPage();
  await p.setContent('<img id=i src="data:image/jpeg;base64,' +
    fs.readFileSync(file).toString('base64') + '">');
  const r = await p.evaluate(async () => {
    const img = document.getElementById('i'); await img.decode();
    const W=img.naturalWidth, H=img.naturalHeight;
    const c=document.createElement('canvas'); c.width=W; c.height=H;
    const g=c.getContext('2d'); g.drawImage(img,0,0);
    const d=g.getImageData(0,0,W,H).data;
    const dark=(x,y)=>{const i=(y*W+x)*4; return (0.299*d[i]+0.587*d[i+1]+0.114*d[i+2])<140;};
    // longest contiguous dark run per row / per column
    const rowRun=[], colRun=[];
    for(let y=0;y<H;y++){let best=0,run=0;for(let x=0;x<W;x++){if(dark(x,y)){run++;if(run>best)best=run;}else run=0;}rowRun.push(best);}
    for(let x=0;x<W;x++){let best=0,run=0;for(let y=0;y<H;y++){if(dark(x,y)){run++;if(run>best)best=run;}else run=0;}colRun.push(best);}
    const pick=(arr,limit)=>{const hits=[];for(let i=0;i<arr.length;i++)if(arr[i]>limit)hits.push(i);
      // collapse adjacent indices into single edges
      const out=[];let s=null,prev=null;
      for(const i of hits){ if(s===null){s=i;} else if(i-prev>3){out.push(Math.round((s+prev)/2)); s=i;} prev=i; }
      if(s!==null) out.push(Math.round((s+prev)/2));
      return out;};
    return {W,H,hEdges:pick(rowRun,W*0.18),vEdges:pick(colRun,H*0.10)};
  });
  console.log(file, JSON.stringify(r));
  await b.close();
})();
