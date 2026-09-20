const {chromium}=require('playwright');const fs=require('fs');
const FPS=30, DUR=54.366, N=Math.round(DUR*FPS);
(async()=>{
 fs.rmSync('/tmp/fr',{recursive:true,force:true});fs.mkdirSync('/tmp/fr',{recursive:true});
 const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 await p.goto('http://localhost:8931/animatic.html');
 await p.waitForFunction('window.__ready===true');
 const t0=Date.now();
 for(let i=0;i<N;i++){
   const d=await p.evaluate(t=>{window.__seek(t);return document.getElementById('c').toDataURL('image/jpeg',0.93);}, i/FPS);
   fs.writeFileSync(`/tmp/fr/${String(i).padStart(5,'0')}.jpg`,Buffer.from(d.split(',')[1],'base64'));
   if(i%200===0)console.log(`${i}/${N}  ${((Date.now()-t0)/1000).toFixed(0)}s`);
 }
 await b.close();
 console.log(`done ${N} frames in ${((Date.now()-t0)/1000).toFixed(0)}s`);
})();
