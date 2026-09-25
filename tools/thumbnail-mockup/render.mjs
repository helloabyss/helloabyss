// Free thumbnail mockups: renders concepts from a JSON spec to PNG with the local
// Chromium. No credits are spent. Usage:
//   node tools/thumbnail-mockup/render.mjs <video-dir>
// Reads <video-dir>/thumbnails.json, writes <video-dir>/mockups/<id>.png plus
// mockups/sheet.png (every concept at full size and at Shorts-feed size).
import { createRequire } from 'node:module';
import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { SUBJECTS } from './subjects.mjs';

const require = createRequire(import.meta.url);
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

const here = dirname(fileURLToPath(import.meta.url));
const videoDir = resolve(process.argv[2] ?? '.');
const spec = JSON.parse(readFileSync(join(videoDir, 'thumbnails.json'), 'utf8'));
const outDir = join(videoDir, 'mockups');
mkdirSync(outDir, { recursive: true });

const font = (f) => readFileSync(join(here, 'fonts', f)).toString('base64');
const FONTS = `
@font-face{font-family:Anton;src:url(data:font/woff2;base64,${font('anton-latin-400-normal.woff2')})}
@font-face{font-family:Oswald;src:url(data:font/woff2;base64,${font('oswald-latin-500-normal.woff2')})}`;

// House palette: near-black, white, one red.
const C = { black: '#0b0b0c', white: '#f4f4f2', red: '#d7141e', grey: '#8a8a8a' };

function esc(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
}

function lineHtml(l) {
  const color = C[l.color ?? 'white'] ?? l.color;
  const strike = l.strike
    ? `<span class="strike" style="background:${C.red}"></span>` : '';
  const box = l.box ? `background:${C[l.box] ?? l.box};padding:0 24px;` : '';
  return `<div class="line" style="font-size:${l.size ?? 200}px;color:${color};${box}">
    <span class="t">${esc(l.text)}${strike}</span></div>`;
}

function thumbHtml(c) {
  const subject = SUBJECTS[c.subject] ?? c.subjectSvg ?? '';
  const pos = c.textPosition ?? 'top';
  return `<!doctype html><html><head><style>${FONTS}
  *{margin:0;box-sizing:border-box}
  body{width:1080px;height:1920px;overflow:hidden;background:${C.black}}
  .frame{position:relative;width:1080px;height:1920px;
    background:radial-gradient(ellipse at 50% 62%,#2a2a2c 0%,#141415 45%,${C.black} 80%)}
  .subject{position:absolute;left:0;right:0;${pos === 'top' ? 'bottom:120px' : 'top:120px'};
    height:1100px;display:flex;align-items:center;justify-content:center}
  .subject svg{width:1000px;height:1100px}
  .text{position:absolute;left:50px;right:50px;${pos === 'top' ? 'top:110px' : 'bottom:150px'};
    display:flex;flex-direction:column;align-items:center;gap:6px}
  .line{font-family:Anton,Impact,sans-serif;line-height:1.02;text-transform:uppercase;
    letter-spacing:1px;text-align:center;white-space:nowrap;
    text-shadow:0 6px 0 rgba(0,0,0,.55),0 0 40px rgba(0,0,0,.8)}
  .t{position:relative;display:inline-block}
  .strike{position:absolute;left:-4%;right:-4%;top:52%;height:10%;transform:rotate(-2deg)}
  .tag{position:absolute;top:44px;left:0;right:0;text-align:center;font:500 34px Oswald;
    letter-spacing:6px;color:${C.grey}}
  </style></head><body><div class="frame">
  ${c.tag ? `<div class="tag">${esc(c.tag)}</div>` : ''}
  <div class="subject">${subject}</div>
  <div class="text">${(c.lines ?? []).map(lineHtml).join('')}</div>
  </div></body></html>`;
}

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
const shots = [];
for (const c of spec.concepts) {
  await page.setContent(thumbHtml(c), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  // Shrink any line that overflows the safe width, so text never clips.
  await page.evaluate(() => {
    for (const el of document.querySelectorAll('.line')) {
      const max = 980;
      let size = parseFloat(el.style.fontSize);
      while (el.scrollWidth > max && size > 40) { size -= 4; el.style.fontSize = size + 'px'; }
    }
  });
  const file = join(outDir, `${c.id}.png`);
  await page.screenshot({ path: file });
  shots.push({ c, b64: readFileSync(file).toString('base64') });
  console.log('wrote', file);
}

// Contact sheet: each concept at review size and at real Shorts-feed size (~200px wide).
const cards = shots.map(({ c, b64 }) => `
  <div class="card"><div class="imgs">
    <img class="big" src="data:image/png;base64,${b64}">
    <div class="feed"><img src="data:image/png;base64,${b64}"><span>feed size</span></div>
  </div><h2>${esc(c.id)} — ${esc(c.label ?? '')}</h2>
  ${c.finalImage ? `<p><b>Final image brief:</b> ${esc(c.finalImage)}</p>` : ''}</div>`).join('');
const sheetW = Math.max(1, shots.length) * 700 + 80;
await page.setViewportSize({ width: sheetW, height: 900 });
await page.setContent(`<!doctype html><html><head><style>${FONTS}
  body{margin:0;padding:40px;background:#1b1b1d;color:#eee;font:22px Oswald,sans-serif;display:flex;gap:40px}
  h1{position:absolute;top:0}
  .card{width:660px}.imgs{display:flex;gap:24px;align-items:flex-end}
  .big{width:450px;border:1px solid #333}.feed img{width:180px;display:block;border:1px solid #333}
  .feed span{font-size:16px;color:#999}
  h2{font:28px Anton;letter-spacing:1px;margin:18px 0 6px}p{margin:0;color:#bbb;line-height:1.35}
  </style></head><body>${cards}</body></html>`, { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: join(outDir, 'sheet.png'), fullPage: true });
console.log('wrote', join(outDir, 'sheet.png'));
await browser.close();
