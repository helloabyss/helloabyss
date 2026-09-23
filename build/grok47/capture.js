const {chromium}=require('playwright');const fs=require('fs');
const FPS=30, DUR=17.80, N=Math.round(DUR*FPS);
const OUT=process.env.FRAMES||'/tmp/g47';
(async()=>{
 fs.rmSync(OUT,{recursive:true,force:true});fs.mkdirSync(OUT,{recursive:true});
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
 const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 await p.goto('http://localhost:8941/short.html');
 await p.waitForFunction('window.__ready===true');
 const t0=Date.now();
 for(let i=0;i<N;i++){
   const d=await p.evaluate(t=>{window.__seek(t);return document.getElementById('c').toDataURL('image/jpeg',0.94);}, i/FPS);
   fs.writeFileSync(`${OUT}/${String(i).padStart(5,'0')}.jpg`,Buffer.from(d.split(',')[1],'base64'));
   if(i%120===0)console.log(`${i}/${N}  ${((Date.now()-t0)/1000).toFixed(0)}s`);
 }
 await b.close();
 console.log(`done ${N} frames in ${((Date.now()-t0)/1000).toFixed(0)}s`);
})();
