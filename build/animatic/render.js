const W=1080,H=1920;
const BASE='#0B0B0D',TYPE='#F2F2F0',ACC='#FFB020',CAU='#8A8A86';
const FONT='"Liberation Sans","DejaVu Sans",sans-serif';
let SHOTS=[],CUES=[],HAT=[];
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const ease=t=>t<0?0:t>1?1:1-Math.pow(1-t,3);
const easeIO=t=>t<0?0:t>1?1:(t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2);

function F(ctx,w,px,ls){ctx.font=`${w} ${px}px ${FONT}`;ctx.letterSpacing=(ls||0)+'px';}
function ctext(ctx,s,x,y,px,w,col,ls){F(ctx,w||'bold',px,ls);ctx.fillStyle=col;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(s,x,y);}
function ltext(ctx,s,x,y,px,w,col,ls){F(ctx,w||'bold',px,ls);ctx.fillStyle=col;ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText(s,x,y);}
function wrap(ctx,s,max){const w=s.split(' ');let l=[],c='';for(const x of w){const t=c?c+' '+x:x;if(ctx.measureText(t).width>max&&c){l.push(c);c=x;}else c=t;}if(c)l.push(c);return l;}

// ---------- placeholder plate ----------
function plate(ctx,sh,p){
  ctx.save();
  const k=1+0.05*p; ctx.translate(W/2,H/2); ctx.scale(k,k); ctx.translate(-W/2,-H/2);
  ctx.fillStyle='#141417';ctx.fillRect(0,0,W,H);
  ctx.strokeStyle='#1d1d21';ctx.lineWidth=3;
  for(let i=-H;i<W+H;i+=46){ctx.beginPath();ctx.moveTo(i,0);ctx.lineTo(i+H,H);ctx.stroke();}
  const bx=70,bw=W-140,pad=44;
  F(ctx,'bold',44); const tl=wrap(ctx,sh.title,bw-2*pad);
  F(ctx,'normal',36); const sl=wrap(ctx,sh.src,bw-2*pad);
  const contentH = 86 + tl.length*58 + 56 + 46 + sl.length*48 + 34 + 48 + 66 + 44;
  const bh=contentH+pad, by=Math.max(300, 790-bh/2);
  ctx.fillStyle='rgba(11,11,13,.82)';ctx.fillRect(bx,by,bw,bh);
  ctx.strokeStyle=CAU;ctx.lineWidth=3;ctx.setLineDash([16,12]);ctx.strokeRect(bx,by,bw,bh);ctx.setLineDash([]);
  ltext(ctx,'PLATE '+String(sh.n).padStart(2,'0'),bx+pad,by+72,64,'bold',CAU,4);
  let y=by+150;
  tl.forEach(s=>{ltext(ctx,s,bx+pad,y,44,'bold',TYPE,0);y+=58;});
  y+=40;
  ltext(ctx,'SOURCE',bx+pad,y,30,'bold',CAU,4); y+=46;
  sl.forEach(s=>{ltext(ctx,s,bx+pad,y,36,'normal',TYPE,0);y+=48;});
  y+=30; ltext(ctx,'LICENCE',bx+pad,y,30,'bold',CAU,4); y+=48;
  const need=/needs licence|risky/i.test(sh.lic);
  ltext(ctx,sh.lic.toUpperCase(),bx+pad,y,40,'bold',need?ACC:TYPE,2); y+=62;
  ltext(ctx,'MOTION — '+sh.mo,bx+pad,y,32,'normal',CAU,0);
  ctx.restore();
}

// ---------- builds ----------
function drawHat(ctx,cx,cy,s,rot,refl,fill,stroke,lw){
  ctx.save();ctx.translate(cx,cy);ctx.rotate(rot||0);if(refl)ctx.scale(-1,1);ctx.scale(s,-s);
  ctx.beginPath();HAT.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath();
  ctx.restore();
  if(fill){ctx.fillStyle=fill;ctx.fill();}
  if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=lw||4;ctx.lineJoin='round';ctx.stroke();}
}
function bgGrid(ctx,p){
  ctx.fillStyle=BASE;ctx.fillRect(0,0,W,H);
  ctx.strokeStyle='#17171b';ctx.lineWidth=2;
  const o=(p*40)%80;
  for(let x=-80+o;x<W+80;x+=80){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}
  for(let y=-80+o;y<H+80;y+=80){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
}
function counter(ctx,sh,p){
  plate(ctx,sh,p*0.6);
  ctx.fillStyle='rgba(11,11,13,.86)';ctx.fillRect(0,0,W,H);
  const v=Math.round(sh.cv*ease(clamp(p/0.7,0,1)));
  ctext(ctx,(sh.cpre||'')+v.toLocaleString('en-US')+(sh.cpost||''),W/2,H/2-40,230,'bold',ACC,-6);
  ctext(ctx,sh.clabel,W/2,H/2+120,44,'bold',TYPE,8);
}
function strike(ctx,sh,p){
  plate(ctx,sh,p);
  const w=ease(clamp((p-0.25)/0.5,0,1));
  ctx.save();ctx.translate(W/2,H/2);ctx.rotate(-0.06);
  ctx.fillStyle=ACC;ctx.fillRect(-W*0.44,-12,W*0.88*w,24);ctx.restore();
}
function mapFill(ctx,sh,p){
  bgGrid(ctx,p);
  const w=ease(clamp(p/0.7,0,1));
  ctext(ctx,'US ONLY',W/2,H/2-70,190,'bold','#2a2a2f',-4);
  ctx.save();ctx.beginPath();ctx.rect(W/2-W*0.45,0,W*0.9*w,H);ctx.clip();
  ctext(ctx,'US ONLY',W/2,H/2-70,190,'bold',ACC,-4);ctx.restore();
  ctext(ctx,'EARLY ACCESS',W/2,H/2+90,56,'bold',TYPE,10);
}
function price(ctx,sh,p){
  bgGrid(ctx,p);
  const v=Math.round(2195*ease(clamp(p/0.55,0,1)));
  ctext(ctx,'$'+v.toLocaleString('en-US'),W/2,H/2-60,220,'bold',TYPE,-6);
  const sp=clamp((p-0.6)/0.18,0,1);
  if(sp>0){
    if(sp<0.18){ctx.fillStyle='rgba(255,255,255,'+(0.5*(1-sp/0.18))+')';ctx.fillRect(0,0,W,H);}
    ctx.save();ctx.translate(W/2,H/2+130);ctx.rotate(-0.14);
    const k=1+0.6*(1-ease(sp));ctx.scale(k,k);
    ctx.strokeStyle=ACC;ctx.lineWidth=8;ctx.strokeRect(-330,-72,660,144);
    ctext(ctx,'NOT SHIPPED',0,0,76,'bold',ACC,4);ctx.restore();
  }
}
function stampBeta(ctx,sh,p){
  const sh2=Object.assign({},sh,{n:13,title:'Siri screen recording continues underneath',src:'OWN SCREEN RECORDING — device on iOS 27',lic:'own footage',mo:'BETA stamp lands over it'});
  const q=clamp((p-0.2)/0.1,0,1), shake=p>0.2&&p<0.45?(Math.sin(p*180)*6*(1-q)):0;
  ctx.save();ctx.translate(shake,shake*0.6);plate(ctx,sh2,p*0.5);ctx.restore();
  ctx.fillStyle='rgba(11,11,13,.72)';ctx.fillRect(0,0,W,H);
  const sp=clamp(p/0.22,0,1);
  ctx.save();ctx.translate(W/2,H/2);ctx.rotate(-0.1);
  const k=1+1.4*(1-ease(sp));ctx.scale(k,k);ctx.globalAlpha=ease(sp);
  ctx.fillStyle=ACC;ctx.fillRect(-300,-105,600,210);
  ctext(ctx,'BETA',0,0,150,'bold',BASE,10);ctx.restore();
}
function tiers(ctx,sh,p){
  bgGrid(ctx,p);
  const rows=[['NO SIRI AI','older iPhones'],['BASELINE SIRI AI','A-series'],['A17 PRO — FULL','deepest version']];
  rows.forEach((r,i)=>{
    const a=ease(clamp((p-i*0.18)/0.3,0,1)); if(a<=0)return;
    const y=H/2+230-i*235, top=i===2;
    ctx.save();ctx.globalAlpha=a;ctx.translate(0,(1-a)*60);
    ctx.fillStyle=top?ACC:'#1e1e23';ctx.fillRect(110,y-88,W-220,176);
    if(!top){ctx.strokeStyle=CAU;ctx.lineWidth=3;ctx.strokeRect(110,y-88,W-220,176);}
    ltext(ctx,r[0],160,y-22,52,'bold',top?BASE:TYPE,2);
    ltext(ctx,r[1],160,y+38,34,'normal',top?'rgba(11,11,13,.75)':CAU,0);
    ctx.restore();
  });
}
function hatShot(ctx,sh,p){
  bgGrid(ctx,p);
  const s=Math.min(1,ease(clamp(p/0.35,0,1)));
  const z=118-58*ease(clamp((p-0.45)/0.55,0,1));
  if(p>0.55){
    const n=ease(clamp((p-0.55)/0.45,0,1));
    [[-1,-1,0.9],[1,-1,2.1],[-1,1,3.4],[1,1,5.0]].forEach((o,i)=>{
      const a=clamp(n*1.6-i*0.18,0,1); if(a<=0)return;
      ctx.save();ctx.globalAlpha=a*0.32;
      drawHat(ctx,W/2+o[0]*430*a,H/2+o[1]*430*a,z*0.6,o[2],i%2===1,null,ACC,3);
      ctx.restore();
    });
  }
  ctx.save();ctx.globalAlpha=s;
  drawHat(ctx,W/2,H/2,z,0,false,ACC,null,0);
  ctx.restore();
}
function pinwheel(ctx,sh,p){
  ctx.fillStyle=BASE;ctx.fillRect(0,0,W,H);
  const g=ease(clamp(p/0.6,0,1)), rot=p*0.5;
  ctx.save();ctx.translate(W/2,H/2-30);ctx.rotate(rot);
  for(let arm=0;arm<12;arm++){
    const a0=arm*Math.PI/6;
    for(let k=1;k<=9;k++){
      const r=k*54*g, a=a0+k*0.26;                 // chiral twist: no mirror symmetry
      const x=Math.cos(a)*r,y=Math.sin(a)*r;
      const rad=clamp(22-k*1.7,4,22)*g;
      ctx.globalAlpha=clamp(1.05-k*0.09,0,1)*g;
      ctx.beginPath();ctx.arc(x,y,rad,0,7);ctx.fillStyle=ACC;ctx.fill();
    }
  }
  ctx.globalAlpha=1;ctx.beginPath();ctx.arc(0,0,20*g,0,7);ctx.fillStyle=TYPE;ctx.fill();
  ctx.restore();
  ctext(ctx,'ILLUSTRATIVE — not the paper figure',W/2,200,28,'normal',CAU,2);
}
function closeShot(ctx,sh,p){
  bgGrid(ctx,p*0.4);
  const z=64-10*ease(p);
  drawHat(ctx,W/2,H/2-210,z,0,false,null,ACC,5);
  ctext(ctx,'WHAT ELSE IS',W/2,H/2+190,84,'bold',TYPE,2);
  ctext(ctx,'SITTING IN',W/2,H/2+285,84,'bold',TYPE,2);
  ctext(ctx,'PLAIN SIGHT?',W/2,H/2+380,84,'bold',ACC,2);
}

// ---------- chrome ----------
function lowerThird(ctx,sh,tl,t){
  const p=clamp((t-sh.t0)/0.45,0,1), out=clamp((t-(sh.t0+2.2))/0.35,0,1);
  if(out>=1)return;
  const a=ease(p)*(1-ease(out));
  ctx.save();ctx.globalAlpha=a;ctx.translate(-40*(1-ease(p)),0);
  const y=1214;
  ctx.fillStyle=ACC;ctx.fillRect(80,y-56,Math.round(420*ease(p)),4);
  F(ctx,'bold',50);ltext(ctx,tl[0],80,y,50,'bold',TYPE,1);
  ltext(ctx,tl[1],80,y+52,32,'normal',CAU,1);
  ctx.restore();
}
function overlay(ctx,sh,t){
  const p=clamp((t-sh.t0)/0.3,0,1);
  ctx.save();ctx.globalAlpha=ease(p);
  const y=1332;
  F(ctx,'bold',54);const lines=wrap(ctx,sh.ov,W-200);
  lines.forEach((s,i)=>{
    const yy=y+i*66-(lines.length-1)*33;
    ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.lineWidth=10;ctx.strokeStyle=BASE;ctx.strokeText(s,W/2,yy);
    ctx.fillStyle=ACC;ctx.fillText(s,W/2,yy);
  });
  ctx.restore();
}
function captions(ctx,t){
  const c=CUES.find(c=>t>=c.a&&t<c.b); if(!c)return;
  const words=c.t.split(' ');
  const idx=Math.min(words.length-1,Math.floor((t-c.a)/((c.b-c.a)/words.length)));
  F(ctx,'bold',62);
  const gap=18;let tw=0;const ws=words.map(w=>{const m=ctx.measureText(w).width;tw+=m;return m;});
  tw+=gap*(words.length-1);
  const y=H-470;
  ctx.fillStyle='rgba(11,11,13,.6)';ctx.fillRect(W/2-tw/2-34,y-56,tw+68,112);
  let x=W/2-tw/2;ctx.textAlign='left';ctx.textBaseline='middle';
  words.forEach((w,i)=>{
    ctx.lineWidth=11;ctx.strokeStyle=BASE;ctx.strokeText(w,x,y);
    ctx.fillStyle=i===idx?ACC:TYPE;ctx.fillText(w,x,y);
    x+=ws[i]+gap;
  });
}
function slate(ctx,sh,t){
  ctx.save();ctx.globalAlpha=.75;
  ltext(ctx,'SHOT '+String(sh.n).padStart(2,'0')+' · '+(sh.lic==='build'?'BUILD':sh.lic.toUpperCase()),44,52,26,'bold',CAU,2);
  const tc=(x)=>String(Math.floor(x/60)).padStart(2,'0')+':'+String(Math.floor(x%60)).padStart(2,'0')+':'+String(Math.floor((x%1)*30)).padStart(2,'0');
  ctx.textAlign='right';F(ctx,'bold',26);ctx.letterSpacing='2px';ctx.fillStyle=CAU;ctx.fillText(tc(t),W-44,52);
  ctx.textAlign='center';ctx.fillText('ANIMATIC — PREVIZ, NOT FINAL',W/2,H-38);
  ctx.restore();
}
function wipe(ctx,t){
  for(const s of SHOTS){
    if(s.beat===0)continue;
    const b=s.t0, d=8/30;
    if(t>=b-d&&t<b+d){
      const p=(t-(b-d))/(2*d), x=W-(W+260)*p;
      ctx.fillStyle=ACC;ctx.fillRect(x,0,10,H);
      if(Math.abs(t-b)<1.5/30){ctx.fillStyle=BASE;ctx.fillRect(0,0,W,H);}
      break;
    }
  }
}

function seek(t){
  const ctx=document.getElementById('c').getContext('2d');
  ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,W,H);
  ctx.fillStyle=BASE;ctx.fillRect(0,0,W,H);
  let sh=SHOTS[0];for(const s of SHOTS)if(t>=s.t0)sh=s;
  const p=clamp((t-sh.t0)/(sh.t1-sh.t0),0,1);
  ({plate,counter,strike,map:mapFill,price,stamp:stampBeta,tiers,hat:hatShot,pinwheel,close:closeShot}[sh.kind]||plate)(ctx,sh,p);
  if(sh.lt)lowerThird(ctx,sh,sh.lt,t);
  if(sh.ov&&sh.kind!=='close'&&sh.kind!=='map')overlay(ctx,sh,t);
  captions(ctx,t);
  slate(ctx,sh,t);
  wipe(ctx,t);
}
window.__seek=seek;
window.__init=(s,c,h)=>{SHOTS=s;CUES=c;HAT=h;};
