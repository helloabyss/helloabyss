const load=s=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.onerror=()=>r(null);i.src=s});
// optional moving plates: <name>.webm next to <name>.jpg (kinds.js VID); missing clips fall back to the still
const loadV=s=>new Promise(r=>{const v=document.createElement('video');v.muted=true;v.preload='auto';v.playsInline=true;
  const to=setTimeout(()=>r(null),8000);v.onloadeddata=()=>{clearTimeout(to);r(v)};v.onerror=()=>{clearTimeout(to);r(null)};v.src=s;v.load()});
fetch('words.json').then(r=>r.json()).then(async d=>{const imgs=await Promise.all(IMAGES.map(n=>load(n+'.jpg')));
  const m={};IMAGES.forEach((n,i)=>m[n]=imgs[i]);
  if(typeof VID!=='undefined'){const vs=await Promise.all(IMAGES.map(n=>loadV(n+'.webm')));IMAGES.forEach((n,i)=>{if(vs[i])VID[n]=vs[i]})}
  window.__init(d.words,d.dur+0.9,m);window.__seek(0);window.__ready=true});
