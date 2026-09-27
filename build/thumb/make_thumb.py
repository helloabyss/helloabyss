#!/usr/bin/env python3
"""make_thumb.py <manifest.json> <thumb_copy.json> — grade plates, render 1280x720 + 1080x1920 thumbnails."""
import json, subprocess, sys
from PIL import Image, ImageOps, ImageEnhance, ImageStat

def grade(src, dst, W, H, T=42.0):
    im = Image.open(src).convert("RGB")
    k = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * k) + 1, int(im.height * k) + 1), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    im = ImageOps.autocontrast(im.crop((l, t, l + W, t + H)), cutoff=(1, 1))
    im = im.point([int(min(255, (v/255 if v/255 < 0.62 else 0.62 + (v/255 - 0.62) * 0.42) * 255)) for v in range(256)] * 3)
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(0.40)).enhance(1.15)
    lo, hi = 0.35, 3.2
    for _ in range(18):
        g = (lo + hi) / 2
        if ImageStat.Stat(im.point([int(255 * ((v/255) ** g)) for v in range(256)] * 3).convert("L")).mean[0] > T: lo = g
        else: hi = g
    im = im.point([int(255 * ((v/255) ** ((lo + hi) / 2))) for v in range(256)] * 3)
    r, g2, b = im.split()
    Image.merge("RGB", (r, g2.point(lambda v: int(v * .975)), b.point(lambda v: int(v * .90)))).save(dst, quality=93)

m = json.load(open(sys.argv[1]))["episodes"][0]
copy = json.load(open(sys.argv[2]))
subprocess.run(["curl", "-sSf", "-o", "pl.png", m["thumb_plate_land"]], check=True)
subprocess.run(["curl", "-sSf", "-o", "pp.png", m["thumb_plate_port"]], check=True)
grade("pl.png", "tl.jpg", 1280, 720); grade("pp.png", "tp.jpg", 1080, 1920)
for plate, name in (("tl.jpg", "tl.json"), ("tp.jpg", "tp.json")):
    c = dict(copy); c["plate"] = plate; json.dump(c, open(name, "w"))
js = """const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();
for(const [w,h,sp,o] of [[1280,720,'tl.json','thumb_1280x720.jpg'],[1080,1920,'tp.json','thumb_1080x1920.jpg']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 await p.goto('http://localhost:8971/thumb.html?w='+w+'&h='+h+'&spec='+sp);
 await p.waitForFunction('window.__ready===true');
 fs.writeFileSync(o,Buffer.from((await p.evaluate(()=>document.getElementById('c').toDataURL('image/jpeg',0.95))).split(',')[1],'base64'));
 await p.close();}
await b.close();console.log('thumbs rendered');})();"""
open("r.js", "w").write(js)
