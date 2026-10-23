// Cuts every named pose out of the official sheets.
//
// Panels are kept at FULL uniform size per sheet rather than trimmed to each
// figure's ink. The sheets state "same crop/scale", so the poses are already
// registered to one another; trimming would destroy that and make a pose swap
// jump. Keeping the panel means a swap is a clean cut.
//
// Background: flood fill inward from the panel border through near-white, so
// the white polo stays opaque (a luminance key would delete it), then dilate
// one pixel into anything still near-white to kill the JPEG fringe.
const { chromium } = require('playwright');
const fs = require('fs');

const SHEETS = {
  'glasses': { file:'art/zul-bust-glasses.jpg',
    rows:[[83,482],[521,920],[959,1358]], cols:[[15,414],[429,828],[843,1242]],
    names:[['official','idle-deadpan','point-right'],
           ['point-left','present-palm','shock'],
           ['skeptical','thumbs-up','thinking']] },
  'plain': { file:'art/zul-bust-plain.jpg',
    rows:[[103,502],[547,946],[991,1390]], cols:[[15,414],[429,828],[843,1242]],
    names:[['official','idle-deadpan','point-right'],
           ['point-left','present-palm','shock'],
           ['skeptical','thumbs-up','thinking']] },
  'body': { file:'art/zul-body.jpg',
    rows:[[881,1210],[1247,1576],[1613,1942]],
    cols:[[13,342],[355,684],[697,1026],[1039,1368]],
    names:[['body-front','body-3q-right','body-3q-left','body-back'],
           ['full-point-right','full-point-left','full-present-palm','full-shock'],
           ['full-skeptical','full-thumbs-up','full-shrug',null]],
    extra:{ 'turnaround': [13,61,1368,816] } },
};

(async () => {
  const b = await chromium.launch({ args:['--no-sandbox'] });
  const p = await b.newPage();
  const man = {};
  for (const [set, S] of Object.entries(SHEETS)) {
    await p.setContent('<img id=i src="data:image/jpeg;base64,' +
      fs.readFileSync(S.file).toString('base64') + '">');
    const boxes = [];
    S.rows.forEach((r, ri) => S.cols.forEach((c, ci) => {
      const n = S.names[ri][ci];
      if (n) boxes.push({ name:n, x:c[0]+3, y:r[0]+3, w:c[1]-c[0]-6, h:r[1]-r[0]-6 });
    }));
    for (const [n, e] of Object.entries(S.extra || {}))
      boxes.push({ name:n, x:e[0]+3, y:e[1]+3, w:e[2]-e[0]-6, h:e[3]-e[1]-6 });

    const out = await p.evaluate(async (boxes) => {
      const img = document.getElementById('i'); await img.decode();
      const res = {}; let res_edges = null;
      for (const B of boxes) {
        const c = document.createElement('canvas'); c.width=B.w; c.height=B.h;
        const g = c.getContext('2d');
        g.drawImage(img, B.x, B.y, B.w, B.h, 0, 0, B.w, B.h);
        const im = g.getImageData(0,0,B.w,B.h), d = im.data, W=B.w, H=B.h;
        const lum = i => 0.299*d[i]+0.587*d[i+1]+0.114*d[i+2];
        // Seed the flood only from edges the figure does NOT cross. A bust is
        // cropped at the chest, so the shirt's white interior touches the
        // bottom edge — seeding there lets the fill leak straight into the
        // polo and key it away. Everything outside the figure is still
        // reachable from the remaining edges.
        const edgeInk = { top:0, bottom:0, left:0, right:0 };
        for (let x=0;x<W;x++){
          if (lum((0*W+x)*4) < 238) edgeInk.top++;
          if (lum(((H-1)*W+x)*4) < 238) edgeInk.bottom++;
        }
        for (let y=0;y<H;y++){
          if (lum((y*W)*4) < 238) edgeInk.left++;
          if (lum((y*W+W-1)*4) < 238) edgeInk.right++;
        }
        const openT = edgeInk.top    <= W*0.02, openB = edgeInk.bottom <= W*0.02;
        const openL = edgeInk.left   <= H*0.02, openR = edgeInk.right  <= H*0.02;
        const bg = new Uint8Array(W*H); const st=[];
        for (let x=0;x<W;x++){ if(openT) st.push(x); if(openB) st.push(x+(H-1)*W); }
        for (let y=0;y<H;y++){ if(openL) st.push(y*W); if(openR) st.push(W-1+y*W); }
        res_edges = {openT, openB, openL, openR};
        while (st.length){ const q=st.pop(); if(bg[q])continue;
          if(lum(q*4)<238)continue; bg[q]=1;
          const x=q%W, y=(q-x)/W;
          if(x>0)st.push(q-1); if(x<W-1)st.push(q+1);
          if(y>0)st.push(q-W); if(y<H-1)st.push(q+W); }
        const grow = new Uint8Array(bg);
        for (let y=1;y<H-1;y++) for (let x=1;x<W-1;x++){ const q=y*W+x;
          if(bg[q]||lum(q*4)<200) continue;
          if(bg[q-1]||bg[q+1]||bg[q-W]||bg[q+W]) grow[q]=1; }
        for (let i=0;i<W*H;i++) if(grow[i]) d[i*4+3]=0;
        g.putImageData(im,0,0);
        // ink bounds, reported but NOT cropped to — registration is the point
        let x0=W,y0=H,x1=0,y1=0;
        for(let y=0;y<H;y++)for(let x=0;x<W;x++) if(d[(y*W+x)*4+3]>8){
          if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; }
        const o=document.createElement('canvas'); o.width=W*2; o.height=H*2;
        const og=o.getContext('2d'); og.imageSmoothingQuality='high';
        og.drawImage(c,0,0,W,H,0,0,W*2,H*2);
        res[B.name]={png:o.toDataURL('image/png'),w:W,h:H,ink:[x0,y0,x1-x0+1,y1-y0+1],
                     edges:res_edges};
      }
      return res;
    }, boxes);

    fs.mkdirSync('art/poses/'+set, { recursive:true });
    man[set] = { source:S.file, poses:{} };
    for (const [n,r] of Object.entries(out)){
      fs.writeFileSync(`art/poses/${set}/${n}.png`, Buffer.from(r.png.split(',')[1],'base64'));
      man[set].poses[n] = { file:`${set}/${n}.png`, w:r.w, h:r.h, ink:r.ink };
    }
    console.log(set+': '+Object.keys(out).length+' poses  panel '+
      Object.values(out)[0].w+'x'+Object.values(out)[0].h);
  }
  fs.writeFileSync('art/poses/manifest.json', JSON.stringify(man,null,1));
  await b.close();
})();
