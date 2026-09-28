// Renders the PNG app icons from icons/icon.svg (PWA installs need PNGs).
const { chromium } = await import('/opt/node22/lib/node_modules/playwright/index.mjs');
import { readFileSync } from "node:fs";
const svg = readFileSync("public/icons/icon.svg", "utf8");
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage();
for (const [size, name, pad] of [[180, "icon-180.png", 0], [192, "icon-192.png", 0], [512, "icon-512.png", 0], [512, "icon-512-maskable.png", 0.14]]) {
  await p.setViewportSize({ width: size, height: size });
  const inner = Math.round(size * (1 - 2 * pad));
  await p.setContent(`<html><body style="margin:0;background:#0B0B0C;display:grid;place-items:center;width:${size}px;height:${size}px">
    <div style="width:${inner}px;height:${inner}px">${svg.replace("<svg ", `<svg width="${inner}" height="${inner}" `)}</div></body></html>`);
  await p.screenshot({ path: "public/icons/" + name, omitBackground: false });
}
await b.close(); console.log("icons rendered");
