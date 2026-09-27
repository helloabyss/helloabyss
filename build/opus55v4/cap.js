// Frame capture for motion.html (sandbox: NODE_PATH=/usr/local/lib/node_modules, cwd = work dir)
const {chromium}=require('playwright');const fs=require('fs');
const FPS=30;(async()=>{fs.rmSync('fr',{recursive:true,force:true});fs.mkdirSync('fr');
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
 const errs=[];p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('http://localhost:8958/motion.html');await p.waitForFunction('window.__ready===true',{timeout:30000});
 fs.writeFileSync('cuts.json',JSON.stringify(await p.evaluate(()=>window.__S.map(s=>s[0]).slice(1))));
 const N=Math.ceil(await p.evaluate(()=>window.__S[window.__S.length-1][1])*FPS);
 for(let i=0;i<N;i++){const d=await p.evaluate(t=>{window.__seek(t);return document.getElementById('c').toDataURL('image/jpeg',0.92)},i/FPS);
  fs.writeFileSync('fr/'+String(i).padStart(5,'0')+'.jpg',Buffer.from(d.split(',')[1],'base64'));if(i%150==0)console.log('frame',i,'/',N)}
 await b.close();if(errs.length)console.log('PAGE ERRORS',errs.slice(0,3));console.log('frames',N)})();
