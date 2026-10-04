// Frame capture for the standard engine (sandbox: NODE_PATH=/usr/local/lib/node_modules, cwd = work dir).
// Env: PAGE (short.html | long.html, default short.html), PORT (default 8958),
//      F0/F1 optional frame range so several workers can capture one long video in parallel.
const {chromium}=require('playwright');const fs=require('fs');
const FPS=30,PAGE=process.env.PAGE||'short.html',PORT=process.env.PORT||8958,LAND=PAGE.startsWith('long');
(async()=>{fs.mkdirSync('fr',{recursive:true});
 const b=await chromium.launch();const p=await b.newPage({viewport:LAND?{width:1920,height:1080}:{width:1080,height:1920}});
 const errs=[];p.on('pageerror',e=>errs.push(String(e)));
 await p.goto(`http://localhost:${PORT}/${PAGE}`);await p.waitForFunction('window.__ready===true',{timeout:30000});
 fs.writeFileSync('cuts.json',JSON.stringify(await p.evaluate(()=>window.__S.map(s=>s[0]).slice(1))));
 const N=Math.ceil(await p.evaluate(()=>window.__S[window.__S.length-1][1])*FPS);
 const f0=+(process.env.F0||0),f1=Math.min(N,+(process.env.F1||N));
 for(let i=f0;i<f1;i++){const d=await p.evaluate(async t=>{if(window.__prep)await window.__prep(t);window.__seek(t);return document.getElementById('c').toDataURL('image/jpeg',0.97)},i/FPS);
  fs.writeFileSync('fr/'+String(i).padStart(5,'0')+'.jpg',Buffer.from(d.split(',')[1],'base64'));if((i-f0)%300==0)console.log('frame',i,'/',f1)}
 await b.close();if(errs.length)console.log('PAGE ERRORS',errs.slice(0,3));console.log('frames',f0,f1,'of',N)})();
