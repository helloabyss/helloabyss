const {chromium}=require('playwright');const fs=require('fs');
const S=process.env.SHORT, N=parseInt(process.env.NFRAMES,10), FPS=30;
const OUT='/home/user/ep/fr'+S;
(async()=>{
 fs.rmSync(OUT,{recursive:true,force:true});fs.mkdirSync(OUT,{recursive:true});
 const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 const errs=[];p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('http://localhost:8956/short_gen.html?s='+S);
 await p.waitForFunction('window.__ready===true');
 for(let i=0;i<N;i++){
  const d=await p.evaluate(t=>{window.__seek(t);return document.getElementById('c').toDataURL('image/jpeg',0.94);}, i/FPS);
  fs.writeFileSync(OUT+'/'+String(i).padStart(5,'0')+'.jpg',Buffer.from(d.split(',')[1],'base64'));
 }
 await b.close();
 if(errs.length)console.log('PAGE ERRORS',errs.slice(0,3));
 console.log('  frames '+N);
})();
