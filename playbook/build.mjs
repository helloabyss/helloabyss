// Build the playbook PDF from src/book.html
// Usage: node build.mjs        (expects `npm i playwright-core` and a Chromium binary)
import { chromium } from 'playwright-core';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.join(here, 'src', 'book.html');
const out = path.join(here, 'dist', 'The-Faceless-Channel-Playbook.pdf');

const EXECUTABLE = process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium';

fs.mkdirSync(path.dirname(out), { recursive: true });

const browser = await chromium.launch({ executablePath: EXECUTABLE });
const page = await browser.newPage();
await page.goto('file://' + src, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

// Report any element that overflows its page width — catches broken tables early.
const wide = await page.evaluate(() => {
  const bad = [];
  document.querySelectorAll('table, pre, .worksheet').forEach((el, i) => {
    if (el.scrollWidth > el.clientWidth + 1) bad.push(`${el.tagName}#${i} ${el.scrollWidth}>${el.clientWidth}`);
  });
  return bad;
});
if (wide.length) console.warn('overflowing elements:', wide);

await page.pdf({
  path: out,
  preferCSSPageSize: true,
  printBackground: true,
  displayHeaderFooter: false,   // running feet are stamped by stamp.py instead:
                                // Chromium reserves a band for them even on
                                // zero-margin pages, which breaks full-bleed art.
});

await browser.close();
const kb = Math.round(fs.statSync(out).size / 1024);
console.log(`built ${out} (${kb} KB)`);
