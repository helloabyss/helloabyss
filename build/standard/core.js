// Standard Shorts engine (owner-approved 2026-09-27, reference: Opus 5.5 v4).
// Per-video scenes.js must define: IMAGES (names of <name>.jpg), CUTS ([wordIndex, leadSeconds] per cut),
// SC (one draw function per scene, len(CUTS)+1). Captions, grain, progress bar and camera helpers live here.

// Timing comes from HeyGen create_speech word timestamps (words.json).
const c=document.getElementById('c'),W=c.width,H=c.height,x=c.getContext('2d');
// Caption geometry: portrait Shorts (1080x1920) or landscape long-form (1920x1080).
const CAP=W>H?{y:H-130,max:1500,fs:66}:{y:1500,max:900,fs:80};
const INK='#0B0B0D',PAPER='#F4F3EF',ACC='#FFB020',RED='#FF4A3D',MUTE='#8A8A86';
const F='"Montserrat","Liberation Sans","Helvetica Neue",Arial,sans-serif';
const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)), lerp=(a,b,t)=>a+(b-a)*t;
const eo=t=>1-Math.pow(1-cl(t),3), eio=t=>{t=cl(t);return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2};
const back=t=>{t=cl(t);const s=1.9;return 1+(s+1)*Math.pow(t-1,3)+s*Math.pow(t-1,2)};
const prog=(t,a,d)=>cl((t-a)/d);
let WORDS=[],DUR=44,IMG={},ONV=false,NOSH=false; // ONV: this frame's background is footage (text gets a shadow)
function font(sz,w=800){x.font=`${w} ${sz}px ${F}`}
function txt(s,X,Y,sz,col,w=800,al='center',ls=0){font(sz,w);if(ONV&&!NOSH){if(col===INK)col='#FFFFFF';else if(col===MUTE)col='#D9D9D3'}x.fillStyle=col;x.textAlign=al;x.textBaseline='alphabetic';
  if(ONV&&!NOSH){x.shadowColor='rgba(0,0,0,.7)';x.shadowBlur=Math.max(8,sz*.35);x.shadowOffsetY=sz*.04}
  if(ls){x.letterSpacing=ls+'px'}x.fillText(s,X,Y);if(ls)x.letterSpacing='0px';x.shadowColor='transparent';x.shadowBlur=0;x.shadowOffsetY=0}
function rr(X,Y,w,h,r){x.beginPath();x.roundRect(X,Y,w,h,r)}
function T(i){return WORDS[i]}             // word by index
const nrm=s=>s.toLowerCase().replace(/[^a-z0-9'-]/g,'');
function at(word,from=0){const q=nrm(word);for(let i=from;i<WORDS.length;i++)if(nrm(WORDS[i].w)===q)return WORDS[i].s;return 0}

// ---------- scene boundaries (set in init from word times) ----------
let S=[];
function cover(img,t0,t,dir){ // image with strong continuous camera move
  const p=prog(t,t0,6),k=1.12+0.22*eio(p);const iw=img.videoWidth||img.width,ih=img.videoHeight||img.height,s=Math.max(W/iw,H/ih)*k;
  const dw=iw*s,dh=ih*s;x.drawImage(img,(W-dw)/2+dir*lerp(60,-60,p),(H-dh)/2+lerp(30,-40,p),dw,dh)}
function flashIn(t,t0){const a=1-prog(t,t0,.22);if(a>0){x.fillStyle=`rgba(255,255,255,${.55*a})`;x.fillRect(0,0,W,H)}}
function camera(t,t0,fn){ // whip-in: scale + slide at scene start
  const p=eo(prog(t,t0,.35));x.save();x.translate(W/2,H/2);x.scale(lerp(1.18,1,p)+0.012*Math.sin(t*1.3),lerp(1.18,1,p)+0.012*Math.sin(t*1.3));
  x.rotate(lerp(-0.035,0,p));x.translate(-W/2+lerp(140,0,p),-H/2);fn();x.restore()}

// ---------- scene helpers ----------
function scrim(a=.55){const g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,`rgba(11,11,13,${a*.7})`);g.addColorStop(.45,'rgba(11,11,13,0)');g.addColorStop(.7,'rgba(11,11,13,.15)');g.addColorStop(1,`rgba(11,11,13,${a+.2})`);x.fillStyle=g;x.fillRect(0,0,W,H)}
function pop(t,t0,X,Y,fn,d=.32){const p=back(prog(t,t0,d));if(p<=0)return;x.save();x.translate(X,Y);x.scale(p,p);fn();x.restore()}
function pill(s,X,Y,sz,bg,fg,padX=44){font(sz,900);const w=x.measureText(s).width+padX*2;rr(X-w/2,Y-sz*.95,w,sz*1.55,sz*.78);
  if(ONV){x.shadowColor='rgba(0,0,0,.5)';x.shadowBlur=sz*.6;x.shadowOffsetY=sz*.12}x.fillStyle=bg;x.fill();x.shadowColor='transparent';x.shadowBlur=0;x.shadowOffsetY=0;
  NOSH=true;txt(s,X,Y+sz*.08,sz,fg,900,'center',2);NOSH=false}
// ---------- word-by-word captions: 1–3 word groups, current word amber ----------
let GROUPS=[];
function buildGroups(){GROUPS=[];let g=[];WORDS.forEach((w,i)=>{g.push(i);const end=/[.,?!:]$/.test(w.w);
  const gap=i+1<WORDS.length?WORDS[i+1].s-w.e:9;const ch=g.reduce((a,j)=>a+WORDS[j].w.length,0);if(end||g.length>=3||gap>.35||ch>15){GROUPS.push(g);g=[]}});if(g.length)GROUPS.push(g)}
function captions(t){ONV=false;if(window.NOCAP)return;let G=null;for(const g of GROUPS){const s=WORDS[g[0]].s-.05,e=WORDS[g[g.length-1]].e+.25;if(t>=s&&t<e){G=g}}
  if(!G)return;const parts=G.map(i=>WORDS[i].w.toUpperCase().replace(/[,.:]$/,''));
  let fs=CAP.fs;font(fs,900);let ws=parts.map(p=>x.measureText(p).width),sp=30,tot=ws.reduce((a,b)=>a+b,0)+sp*(parts.length-1);
  if(tot>CAP.max){fs=Math.floor(fs*CAP.max/tot);font(fs,900);ws=parts.map(p=>x.measureText(p).width);sp=26;tot=ws.reduce((a,b)=>a+b,0)+sp*(parts.length-1)}
  let X=(W-tot)/2;const Y=CAP.y;
  rr(X-34,Y-fs-8,tot+68,fs+44,20);x.fillStyle='rgba(11,11,13,.78)';x.fill();
  G.forEach((wi,k)=>{const w=WORDS[wi],on=t>=w.s-.03&&t<(k<G.length-1?WORDS[G[k+1]].s-.03:1e9),p=back(prog(t,w.s-.03,.16));
    x.save();x.translate(X+ws[k]/2,Y);const s=on?Math.min(1.05,lerp(.85,1.05,p)):1;x.scale(s,s);
    txt(parts[k],0,0,fs,on?ACC:(t>=w.s?'#FFFFFF':'rgba(255,255,255,.55)'),900,'center');x.restore();X+=ws[k]+sp})}

function grain(){if(!grain.t){grain.t=[];for(let k=0;k<4;k++){const g=document.createElement('canvas');g.width=W/4;g.height=H/4;const gx=g.getContext('2d'),d=gx.createImageData(W/4,H/4);
  for(let i=0;i<d.data.length;i+=4){const v=Math.random()*255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=18}gx.putImageData(d,0,0);grain.t.push(g)}}
  x.globalAlpha=.5;x.drawImage(grain.t[Math.floor(performance.now()/40)%4],0,0,W,H);x.globalAlpha=1}

window.__seek=t=>{let k=S.length-1;for(let i=0;i<S.length;i++)if(t<S[i][1]){k=i;break}
  x.setTransform(1,0,0,1,0,0);SC[k](t,S[k][0],S[k][1]);x.setTransform(1,0,0,1,0,0);
  // progress bar (retention cue)
  x.fillStyle='rgba(255,255,255,.18)';x.fillRect(0,0,W,8);x.fillStyle=ACC;x.fillRect(0,0,W*cl(t/DUR),8);
  captions(t);grain()};
window.__init=(words,dur,imgs)=>{WORDS=words;DUR=dur;IMG=imgs;buildGroups();
  const st=w=>at(w)-.18;const cuts=typeof CUTS==='function'?CUTS():CUTS;const b=[0,...cuts.map(([i,o])=>T(i).s-o),dur];
  S=[];for(let i=0;i<b.length-1;i++)S.push([b[i],b[i+1]]);window.__S=S};
