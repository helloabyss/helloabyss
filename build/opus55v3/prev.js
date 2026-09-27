const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(async()=>await chromium.launch());
 const p=await b.newPage({viewport:{width:1080,height:1920}});const errs=[];p.on('pageerror',e=>errs.push(String(e)));p.on('console',m=>{if(m.type()=='error')errs.push(m.text())});
 await p.goto('http://localhost:8957/motion.html');await p.waitForFunction('window.__ready===true',{timeout:15000});
 const ts=(process.env.TS||'1,3,4.6,7.5,10.5,15,20.6,23.5,25.5,30.5,35.5,37.9,42.8').split(',').map(Number);
 fs.mkdirSync('prev',{recursive:true});
 for(const t of ts){await p.evaluate(t=>window.__seek(t),t);await p.screenshot({path:`prev/t${t}.png`})}
 console.log(JSON.stringify(await p.evaluate(()=>window.__S)));console.log('errors',errs);await b.close()})();
