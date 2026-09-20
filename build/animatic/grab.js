const {chromium}=require('playwright');const fs=require('fs');
(async()=>{
 const times=process.argv.slice(2).map(Number);
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 await p.goto('http://localhost:8931/animatic.html');await p.waitForFunction('window.__ready===true');
 for(const t of times){
   await p.evaluate(t=>window.__seek(t),t);
   const d=await p.evaluate(()=>document.getElementById('c').toDataURL('image/jpeg',0.9));
   fs.writeFileSync(`/tmp/f_${t.toFixed(1)}.jpg`,Buffer.from(d.split(',')[1],'base64'));
 }
 await b.close();console.log('grabbed',times.length);
})();
