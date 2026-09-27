const load=s=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.onerror=()=>r(null);i.src=s});
fetch('words.json').then(r=>r.json()).then(async d=>{const imgs=await Promise.all(IMAGES.map(n=>load(n+'.jpg')));
  const m={};IMAGES.forEach((n,i)=>m[n]=imgs[i]);window.__init(d.words,d.dur+0.9,m);window.__seek(0);window.__ready=true});
