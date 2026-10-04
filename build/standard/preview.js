// Local layout check before any sandbox render. Serve the episode dir (core/boot/short.html copied in,
// placeholder <name>.jpg allowed) on :8959, then:  TS=1,4.5,9 NODE_PATH=$(npm root -g) node preview.js
// Writes prev/t<T>.png per timestamp and prints the scene boundaries.
const {chromium}=require('playwright');const fs=require('fs');const PAGE=process.env.PAGE||'short.html',LAND=PAGE.startsWith('long');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:LAND?{width:1920,height:1080}:{width:1080,height:1920}});
 const errs=[];p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('http://localhost:'+(process.env.PORT||8959)+'/'+PAGE);await p.waitForFunction('window.__ready===true',{timeout:15000});
 fs.mkdirSync('prev',{recursive:true});
 for(const t of process.env.TS.split(',').map(Number)){await p.evaluate(t=>window.__seek(t),t);await p.screenshot({path:`prev/t${t}.png`})}
 console.log(JSON.stringify(await p.evaluate(()=>window.__S.map(s=>s.map(v=>+v.toFixed(2))))));
 console.log('errors',errs.length?errs:'none');console.log('cue errors',await p.evaluate(()=>window.__errs||[]));await b.close()})();
