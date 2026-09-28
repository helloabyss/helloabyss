const {chromium} = await import('/opt/node22/lib/node_modules/playwright/index.mjs');
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p = await b.newPage({viewport:{width:1280,height:720}});
for (const n of ['A','B']) {
  await p.goto('file://'+process.cwd()+`/thumb_${n}.html`);
  await p.waitForTimeout(300);
  await p.screenshot({path:`thumbnail-${n}.png`});
}
await b.close(); console.log('shot');
