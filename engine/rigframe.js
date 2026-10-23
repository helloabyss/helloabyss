const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport:{width:1080,height:1920}, deviceScaleFactor:1 });
  await p.goto('file://' + require('path').resolve('rig.html'), { waitUntil:'load' });
  for (const [s,t,name] of [[0,0,'a'],[0,1,'b'],[1,0.5,'c']]) {
    await p.evaluate(([a,b]) => window.setFrame(a,b), [s,t]);
    await p.screenshot({ path:'rigchk_'+name+'.png', clip:{x:0,y:0,width:1080,height:1920} });
  }
  await b.close(); console.log('3 frames');
})();
