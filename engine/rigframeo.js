const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport:{width:1920,height:1080}, deviceScaleFactor:1 });
  await p.goto('file://' + require('path').resolve('rigo.html'), { waitUntil:'load' });
  for (const [s,t,n] of [[1,0.9,'a'],[3,0.9,'b']]) {
    await p.evaluate(([x,y]) => window.setFrame(x,y), [s,t]);
    await p.screenshot({ path:'rigochk_'+n+'.png', clip:{x:0,y:0,width:1920,height:1080} });
  }
  await b.close(); console.log('2 frames');
})();
