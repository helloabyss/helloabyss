// Grok 4.7 Short — deterministic renderer. seek(t) is a pure function of t.
const W=1080,H=1920;
const BASE='#0B0B0D',TYPE='#F2F2F0',ACC='#FFB020',CAU='#8A8A86';
const FONT='"Liberation Sans","DejaVu Sans",sans-serif';
const DUR=17.80;
let CUES=[],GRAIN=[],PTS=[];

const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const ease=t=>t<0?0:t>1?1:1-Math.pow(1-t,3);
const easeIO=t=>t<0?0:t>1?1:(t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2);
const seg=(t,a,b)=>clamp((t-a)/(b-a),0,1);

function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}}

function F(ctx,w,px,ls){ctx.font=`${w} ${px}px ${FONT}`;ctx.letterSpacing=(ls||0)+'px';}
function ctext(ctx,s,x,y,px,w,col,ls,al){F(ctx,w||'bold',px,ls);ctx.fillStyle=col;ctx.textAlign='center';ctx.textBaseline='middle';ctx.globalAlpha=al===undefined?1:al;ctx.fillText(s,x,y);ctx.globalAlpha=1;}
function ltext(ctx,s,x,y,px,w,col,ls,al){F(ctx,w||'bold',px,ls);ctx.fillStyle=col;ctx.textAlign='left';ctx.textBaseline='middle';ctx.globalAlpha=al===undefined?1:al;ctx.fillText(s,x,y);ctx.globalAlpha=1;}
function rtext(ctx,s,x,y,px,w,col,ls,al){F(ctx,w||'bold',px,ls);ctx.fillStyle=col;ctx.textAlign='right';ctx.textBaseline='middle';ctx.globalAlpha=al===undefined?1:al;ctx.fillText(s,x,y);ctx.globalAlpha=1;}
function wrap(ctx,s,max){const w=s.split(' ');let l=[],c='';for(const x of w){const t=c?c+' '+x:x;if(ctx.measureText(t).width>max&&c){l.push(c);c=x;}else c=t;}if(c)l.push(c);return l;}

// ---------- layer 1: procedural cinematic base ----------
function initParticles(){
  const r=mulberry32(20260921);PTS=[];
  for(let i=0;i<120;i++)PTS.push({x:r(),y:r(),rr:18+r()*190,a:.018+r()*.085,sx:(r()-.5)*.020,sy:-(0.006+r()*0.030),w:r()});
}
function base(ctx,t,drift){
  ctx.fillStyle=BASE;ctx.fillRect(0,0,W,H);
  // soft key light, slowly drifting
  const kx=W*(0.30+0.12*Math.sin(t*0.22)), ky=H*(0.30+0.05*Math.cos(t*0.17));
  let g=ctx.createRadialGradient(kx,ky,0,kx,ky,H*0.78);
  g.addColorStop(0,'rgba(58,52,42,0.60)');g.addColorStop(.45,'rgba(28,26,24,0.30)');g.addColorStop(1,'rgba(11,11,13,0)');
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  // counter fill, cool
  const cx=W*0.82, cy=H*(0.80-0.04*Math.sin(t*0.19));
  g=ctx.createRadialGradient(cx,cy,0,cx,cy,H*0.52);
  g.addColorStop(0,'rgba(30,36,46,0.42)');g.addColorStop(1,'rgba(11,11,13,0)');
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  // drifting bokeh — the depth layer
  ctx.save();ctx.translate(0,drift*-38);
  for(const p of PTS){
    const px=((p.x+p.sx*t)%1+1)%1*W, py=((p.y+p.sy*t)%1+1)%1*H;
    const rr=p.rr*(1+0.06*Math.sin(t*0.5+p.w*9));
    const gg=ctx.createRadialGradient(px,py,0,px,py,rr);
    const amber=p.w>0.80;
    gg.addColorStop(0,amber?`rgba(255,176,32,${p.a*0.85})`:`rgba(150,148,142,${p.a})`);
    gg.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=gg;ctx.beginPath();ctx.arc(px,py,rr,0,7);ctx.fill();
  }
  ctx.restore();
}
function vignette(ctx){
  const g=ctx.createRadialGradient(W/2,H*0.46,H*0.22,W/2,H*0.5,H*0.76);
  g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,0.80)');
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
}
function initGrain(){
  GRAIN=[];
  for(let k=0;k<6;k++){
    const c=document.createElement('canvas');c.width=270;c.height=480;
    const x=c.getContext('2d'),d=x.createImageData(270,480),r=mulberry32(77+k*911);
    for(let i=0;i<d.data.length;i+=4){const v=(r()*255)|0;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=26;}
    x.putImageData(d,0,0);GRAIN.push(c);
  }
}
function grain(ctx,t){
  const g=GRAIN[Math.floor(t*30)%GRAIN.length];
  ctx.save();ctx.globalAlpha=.42;ctx.imageSmoothingEnabled=false;
  ctx.drawImage(g,0,0,270,480,0,0,W,H);ctx.restore();
}

// ---------- shared chrome ----------
function eyebrow(ctx,t){
  const a=ease(seg(t,0.15,0.75));
  ltext(ctx,'FRONTIER AI',62,86,26,'bold',CAU,6,a*.9);
  rtext(ctx,'SEP 21 · 2026',W-62,86,26,'bold',CAU,6,a*.9);
  ctx.globalAlpha=a*.5;ctx.strokeStyle=CAU;ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(62,112);ctx.lineTo(W-62,112);ctx.stroke();ctx.globalAlpha=1;
}
function sourceStrip(ctx,t){
  const a=ease(seg(t,0.5,1.2));
  ctx.globalAlpha=a*.55;ctx.strokeStyle=CAU;ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(62,1566);ctx.lineTo(W-62,1566);ctx.stroke();ctx.globalAlpha=1;
  ltext(ctx,'SOURCE',62,1606,24,'bold',ACC,5,a*.95);
  rtext(ctx,'x.ai/news/grok-4-7 · company-reported',W-62,1606,24,'normal',CAU,1,a*.85);
}
function captions(ctx,t){
  for(const c of CUES){
    if(t<c.a-0.14||t>c.b+0.10)continue;
    const inp=ease(seg(t,c.a-0.14,c.a+0.10)), out=1-ease(seg(t,c.b-0.05,c.b+0.10));
    const al=Math.min(inp,out); if(al<=0.01)continue;
    F(ctx,'bold',54);
    const lines=wrap(ctx,c.t,W-220);
    const y0=1430-(lines.length-1)*33;
    ctx.save();ctx.translate(0,(1-inp)*16);
    lines.forEach((s,i)=>{
      const yy=y0+i*66;
      F(ctx,'bold',54);const tw=ctx.measureText(s).width;
      ctx.globalAlpha=al*.72;ctx.fillStyle='rgba(11,11,13,1)';
      ctx.fillRect(W/2-tw/2-22,yy-38,tw+44,74);ctx.globalAlpha=1;
      ctext(ctx,s,W/2,yy,54,'bold',TYPE,0,al);
    });
    ctx.restore();
    break;
  }
}
function rule(ctx,x,y,w,a,col){ctx.globalAlpha=a;ctx.strokeStyle=col||ACC;ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+w,y);ctx.stroke();ctx.globalAlpha=1;}

// ---------- beats ----------
function hook(ctx,t){
  const p=seg(t,0,3.60);
  const a1=ease(seg(t,0.20,1.05));
  const ls=14-12*ease(seg(t,0.20,1.40));
  ctx.save();const k=1.06-0.06*easeIO(seg(t,0,2.4));
  ctx.translate(W/2,760);ctx.scale(k,k);ctx.translate(-W/2,-760);
  ctext(ctx,'GROK 4.7',W/2,760,168,'bold',TYPE,ls,a1);
  ctx.restore();
  rule(ctx,W/2-150,880,300*ease(seg(t,0.85,1.6)),ease(seg(t,0.85,1.3)));
  const a2=ease(seg(t,1.25,1.95));
  ctext(ctx,'LIVE NOW',W/2,966,58,'bold',ACC,12,a2);
  const a3=ease(seg(t,1.85,2.55));
  ctext(ctx,'SpaceXAI · September 21, 2026',W/2,1052,36,'normal',CAU,2,a3);
}
function price(ctx,t){
  const t0=3.60;
  const a1=ease(seg(t,t0+0.10,t0+0.80));
  ctext(ctx,'PRICE PER MILLION TOKENS',W/2,470,32,'bold',CAU,7,a1);
  const cols=[{x:W*0.29,v:'$2',l:'INPUT',d:0.25},{x:W*0.71,v:'$6',l:'OUTPUT',d:0.50}];
  for(const c of cols){
    const a=ease(seg(t,t0+c.d,t0+c.d+0.70));
    ctx.save();ctx.translate(c.x,640);ctx.scale(0.92+0.08*a,0.92+0.08*a);ctx.translate(-c.x,-640);
    ctext(ctx,c.v,c.x,640,190,'bold',TYPE,-4,a);ctx.restore();
    ctext(ctx,c.l,c.x,762,34,'bold',ACC,8,a);
  }
  // comparison rows
  const rows=[{n:'GROK 4.6',y:960,d:0.95},{n:'GROK 4.7',y:1058,d:1.15}];
  for(const r of rows){
    const a=ease(seg(t,t0+r.d,t0+r.d+0.55));
    ctx.globalAlpha=a*0.13;ctx.fillStyle=TYPE;ctx.fillRect(140,r.y-38,W-280,76);ctx.globalAlpha=1;
    ltext(ctx,r.n,172,r.y,42,'bold',TYPE,2,a);
    rtext(ctx,'$2  /  $6',W-172,r.y,42,'bold',TYPE,2,a);
  }
  const a4=ease(seg(t,t0+1.65,t0+2.25));
  ctx.save();ctx.translate(W/2,1190);ctx.rotate(-0.035);
  ctext(ctx,'UNCHANGED',0,0,62,'bold',ACC,10,a4);
  ctx.restore();
}
function model(ctx,t){
  const t0=7.60;
  const a1=ease(seg(t,t0+0.10,t0+0.75));
  ctext(ctx,'WHAT CHANGED',W/2,470,32,'bold',CAU,7,a1);
  const rows=[
    {k:'BASE MODEL',v:'LARGER',y:640,p6:0.52,p7:0.78,d:0.30},
    {k:'RL RUN',v:'LONGER',y:880,p6:0.44,p7:0.84,d:0.65}
  ];
  for(const r of rows){
    const a=ease(seg(t,t0+r.d,t0+r.d+0.60));
    const g=ease(seg(t,t0+r.d+0.25,t0+r.d+1.35));
    ltext(ctx,r.k,140,r.y,38,'bold',CAU,6,a);
    rtext(ctx,r.v,W-140,r.y,44,'bold',ACC,4,a);
    const bx=196,bw=W-336,by=r.y+56;
    ctx.globalAlpha=a*0.16;ctx.fillStyle=TYPE;ctx.fillRect(bx,by,bw,14);ctx.globalAlpha=1;
    ctx.globalAlpha=a*0.55;ctx.fillStyle=CAU;ctx.fillRect(bx,by,bw*r.p6*g,14);ctx.globalAlpha=1;
    ctx.globalAlpha=a;ctx.fillStyle=ACC;ctx.fillRect(bx,by+26,bw*r.p7*g,14);ctx.globalAlpha=1;
    rtext(ctx,'4.6',bx-18,by+7,24,'bold',CAU,1,a*0.9);
    rtext(ctx,'4.7',bx-18,by+33,24,'bold',ACC,1,a*0.95);
  }
  const a3=ease(seg(t,t0+1.55,t0+2.25));
  F(ctx,'normal',38);
  const ls=wrap(ctx,'Weighted toward problems that take many hours to complete.',W-260);
  ls.forEach((s,i)=>ctext(ctx,s,W/2,1120+i*52,38,'normal',TYPE,0,a3*0.92));
  const a4=ease(seg(t,t0+2.35,t0+2.95));
  ctext(ctx,'BETTER AT VERIFYING ITS OWN WORK',W/2,1268,30,'bold',CAU,5,a4);
}
function avail(ctx,t){
  const t0=11.90;
  const a1=ease(seg(t,t0+0.08,t0+0.65));
  ctext(ctx,'AVAILABLE TODAY',W/2,560,32,'bold',CAU,7,a1);
  const tags=['CURSOR','GROK BUILD','GROK API'];
  tags.forEach((s,i)=>{
    const d=t0+0.28+i*0.26, a=ease(seg(t,d,d+0.50)), y=720+i*130;
    ctx.save();ctx.translate((1-a)*-40,0);
    rule(ctx,150,y,8+58*a,a,ACC);
    ltext(ctx,s,240,y,64,'bold',TYPE,3,a);
    ctx.restore();
  });
  const a4=ease(seg(t,t0+1.30,t0+1.95));
  ctext(ctx,'plus third-party harnesses, routers and cloud platforms',W/2,1170,32,'normal',CAU,1,a4*0.95);
}
function close(ctx,t){
  const t0=14.90;
  const a1=ease(seg(t,t0+0.10,t0+0.80));
  const ls=10-8*ease(seg(t,t0+0.10,t0+1.10));
  ctext(ctx,'A CHEAPER',W/2,620,118,'bold',TYPE,ls,a1);
  ctext(ctx,'OPTION',W/2,748,118,'bold',ACC,ls,a1);
  const a2=ease(seg(t,t0+0.70,t0+1.30));
  ctext(ctx,'for coding and agent work',W/2,868,42,'normal',TYPE,1,a2);
  // the caveat — the channel's differentiator
  const a3=ease(seg(t,t0+1.25,t0+1.95));
  const bx=130,by=980,bw=W-260,bh=250;
  ctx.globalAlpha=a3*0.90;ctx.fillStyle='rgba(11,11,13,0.86)';ctx.fillRect(bx,by,bw,bh);
  ctx.globalAlpha=a3;ctx.strokeStyle=ACC;ctx.lineWidth=4;
  ctx.beginPath();ctx.moveTo(bx,by);ctx.lineTo(bx,by+bh);ctx.stroke();ctx.globalAlpha=1;
  ltext(ctx,'READ THE FINE PRINT',bx+38,by+52,30,'bold',ACC,5,a3);
  F(ctx,'normal',34);
  const cl=wrap(ctx,'Benchmarks are company-reported, and the table compares Grok 4.7 xHigh with Grok 4.6 High. Not like-for-like.',bw-76);
  cl.forEach((s,i)=>ltext(ctx,s,bx+38,by+112+i*46,34,'normal',TYPE,0,a3*0.95));
}

const BEATS=[{a:0,b:3.60,f:hook},{a:3.60,b:7.60,f:price},{a:7.60,b:11.90,f:model},{a:11.90,b:14.90,f:avail},{a:14.90,b:DUR,f:close}];

function seek(t){
  const ctx=document.getElementById('c').getContext('2d');
  ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;
  let b=BEATS[0];for(const x of BEATS)if(t>=x.a)b=x;
  const local=(t-b.a)/(b.b-b.a);
  base(ctx,t,local);
  // slow push-in per beat, camera not decoration
  const k=1.0+0.030*easeIO(local);
  ctx.save();ctx.translate(W/2,H*0.46);ctx.scale(k,k);ctx.translate(-W/2,-H*0.46);
  b.f(ctx,t);
  ctx.restore();
  vignette(ctx);
  eyebrow(ctx,t);
  sourceStrip(ctx,t);
  captions(ctx,t);
  grain(ctx,t);
  // beat cut flash
  for(const x of BEATS){
    if(x.a===0)continue;
    if(t>=x.a-0.05&&t<x.a+0.05){ctx.globalAlpha=0.16*(1-Math.abs(t-x.a)/0.05);ctx.fillStyle=ACC;ctx.fillRect(0,0,W,H);ctx.globalAlpha=1;}
  }
}
window.__seek=seek;
window.__init=(c)=>{CUES=c;initGrain();initParticles();};
window.__dur=DUR;
