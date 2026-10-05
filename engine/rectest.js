const {chromium}=require('playwright');
(async()=>{
  const b=await chromium.launch({args:['--no-sandbox']});
  const ctx=await b.newContext({viewport:{width:1920,height:1080},
    recordVideo:{dir:'rec/',size:{width:1920,height:1080}}});
  const p=await ctx.newPage();
  await p.setContent(`<style>body{margin:0;background:#fff}
   .b{width:200px;height:200px;background:#d81e28;animation:m 2s linear forwards}
   @keyframes m{from{transform:translateX(0)}to{transform:translateX(1400px)}}</style><div class="b"></div>`);
  await p.waitForTimeout(2500);
  await ctx.close(); await b.close();
  console.log('recorded');
})();
