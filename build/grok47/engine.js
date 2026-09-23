// TWiT Shorts engine — spec-driven. seek(t) is pure in t.
const W=1080,H=1920;
const C={BASE:'#0B0B0D',TYPE:'#F2F2F0',ACC:'#FFB020',CAU:'#8A8A86'};
const FONT='"Liberation Sans","DejaVu Sans",sans-serif';
let SPEC=null,PLATES=[],GRAIN=[];

const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const ease=t=>t<0?0:t>1?1:1-Math.pow(1-t,3);
const easeIO=t=>t<0?0:t>1?1:(t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2);
const seg=(t,a,b)=>b<=a?(t>=b?1:0):clamp((t-a)/(b-a),0,1);
const col=k=>C[k]||k;
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}}

function F(x,w,px,ls){x.font=`${w} ${px}px ${FONT}`;x.letterSpacing=(ls||0)+'px';}
function T(x,s,ax,px,y,w,c,ls,al){F(x,w||'bold',px,ls);x.fillStyle=col(c);x.textAlign=ax;x.textBaseline='middle';x.globalAlpha=al===undefined?1:al;x.fillText(s,ax==='center'?W/2:(ax==='left'?arguments[10]:arguments[10]),y);x.globalAlpha=1;}
function ctext(x,s,cx,y,px,w,c,ls,al){F(x,w||'bold',px,ls);x.fillStyle=col(c);x.textAlign='center';x.textBaseline='middle';x.globalAlpha=al==null?1:al;x.fillText(s,cx,y);x.globalAlpha=1;}
function ltext(x,s,cx,y,px,w,c,ls,al){F(x,w||'bold',px,ls);x.fillStyle=col(c);x.textAlign='left';x.textBaseline='middle';x.globalAlpha=al==null?1:al;x.fillText(s,cx,y);x.globalAlpha=1;}
function rtext(x,s,cx,y,px,w,c,ls,al){F(x,w||'bold',px,ls);x.fillStyle=col(c);x.textAlign='right';x.textBaseline='middle';x.globalAlpha=al==null?1:al;x.fillText(s,cx,y);x.globalAlpha=1;}
function wrap(x,s,max){const ws=s.split(' ');let l=[],c='';for(const q of ws){const t=c?c+' '+q:q;if(x.measureText(t).width>max&&c){l.push(c);c=q;}else c=t;}if(c)l.push(c);return l;}
function rule(x,px,y,w,a,c){x.globalAlpha=a;x.strokeStyle=col(c||'ACC');x.lineWidth=5;x.beginPath();x.moveTo(px,y);x.lineTo(px+w,y);x.stroke();x.globalAlpha=1;}

// ---- layer 1: plate ----
function plate(x,i,p,mv){
  const img=PLATES[i]; if(!img){x.fillStyle=C.BASE;x.fillRect(0,0,W,H);}
  else{
    const k=1.08+0.07*easeIO(p);
    const dx=(mv&&mv.x||0)*p*W*0.045, dy=(mv&&mv.y||0)*p*H*0.030;
    x.drawImage(img,(W-W*k)/2+dx,(H-H*k)/2+dy,W*k,H*k);
  }
  const g=x.createLinearGradient(0,0,0,H);
  g.addColorStop(0,'rgba(11,11,13,0.62)');g.addColorStop(0.42,'rgba(11,11,13,0.38)');
  g.addColorStop(0.74,'rgba(11,11,13,0.70)');g.addColorStop(1,'rgba(11,11,13,0.93)');
  x.fillStyle=g;x.fillRect(0,0,W,H);
}
function vignette(x){
  const g=x.createRadialGradient(W/2,H*0.46,H*0.22,W/2,H*0.5,H*0.78);
  g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,0.78)');
  x.fillStyle=g;x.fillRect(0,0,W,H);
}
function initGrain(){GRAIN=[];for(let k=0;k<6;k++){const c=document.createElement('canvas');c.width=270;c.height=480;const x=c.getContext('2d'),d=x.createImageData(270,480),r=mulberry32(77+k*911);for(let i=0;i<d.data.length;i+=4){const v=(r()*255)|0;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=24;}x.putImageData(d,0,0);GRAIN.push(c);}}
function grain(x,t){const g=GRAIN[Math.floor(t*30)%GRAIN.length];x.save();x.globalAlpha=.38;x.imageSmoothingEnabled=false;x.drawImage(g,0,0,270,480,0,0,W,H);x.restore();}

// ---- block primitives ----
const BLOCKS={
 label:(x,b,a)=>ctext(x,b.t,W/2,b.y,b.px||32,'bold','CAU',7,a),
 big:(x,b,a)=>{const ls=(b.track?14:0)-(b.track?12:0)*a;
   ctext(x,b.t,W/2,b.y,b.px||150,'bold',b.col||'TYPE',ls,a);},
 accent:(x,b,a)=>ctext(x,b.t,W/2,b.y,b.px||58,'bold','ACC',b.ls==null?12:b.ls,a),
 sub:(x,b,a)=>ctext(x,b.t,W/2,b.y,b.px||36,'normal',b.col||'CAU',2,a),
 rule:(x,b,a)=>rule(x,W/2-(b.w||300)/2,b.y,(b.w||300)*a,a),
 para:(x,b,a)=>{F(x,'normal',b.px||38);wrap(x,b.t,W-(b.pad||260)).forEach((s,i)=>ctext(x,s,W/2,b.y+i*(b.lh||52),b.px||38,'normal',b.col||'TYPE',0,a*0.94));},
 statpair:(x,b,a,t,t0)=>{
   b.items.forEach((it,i)=>{
     const aa=ease(seg(t,t0+(b.at||0)+i*0.22,t0+(b.at||0)+i*0.22+0.60));
     const cx=W*(i===0?0.29:0.71);
     x.save();x.translate(cx,b.y);x.scale(0.92+0.08*aa,0.92+0.08*aa);x.translate(-cx,-b.y);
     ctext(x,it.v,cx,b.y,b.px||190,'bold','TYPE',-4,aa);x.restore();
     ctext(x,it.l,cx,b.y+122,34,'bold','ACC',8,aa);
   });},
 rows:(x,b,a,t,t0)=>{
   b.items.forEach((it,i)=>{
     const aa=ease(seg(t,t0+(b.at||0)+i*0.18,t0+(b.at||0)+i*0.18+0.50));
     const y=b.y+i*98;
     x.globalAlpha=aa*0.15;x.fillStyle=C.TYPE;x.fillRect(140,y-38,W-280,76);x.globalAlpha=1;
     ltext(x,it.l,172,y,42,'bold',it.hl?'ACC':'TYPE',2,aa);
     rtext(x,it.r,W-172,y,42,'bold',it.hl?'ACC':'TYPE',2,aa);
   });},
 stamp:(x,b,a)=>{x.save();x.translate(W/2,b.y);x.rotate(-0.035);ctext(x,b.t,0,0,b.px||62,'bold','ACC',10,a);x.restore();},
 bars:(x,b,a,t,t0)=>{
   b.items.forEach((r,i)=>{
     const d=(b.at||0)+i*0.36, aa=ease(seg(t,t0+d,t0+d+0.55)), g=ease(seg(t,t0+d+0.22,t0+d+1.30));
     const y=b.y+i*240;
     ltext(x,r.k,140,y,38,'bold','CAU',6,aa);
     rtext(x,r.v,W-140,y,44,'bold','ACC',4,aa);
     const bx=196,bw=W-336,by=y+56;
     x.globalAlpha=aa*0.18;x.fillStyle=C.TYPE;x.fillRect(bx,by,bw,14);x.globalAlpha=1;
     x.globalAlpha=aa*0.55;x.fillStyle=C.CAU;x.fillRect(bx,by,bw*r.a*g,14);x.globalAlpha=1;
     x.globalAlpha=aa;x.fillStyle=C.ACC;x.fillRect(bx,by+26,bw*r.b*g,14);x.globalAlpha=1;
     rtext(x,r.la||'4.6',bx-18,by+7,24,'bold','CAU',1,aa*0.9);
     rtext(x,r.lb||'4.7',bx-18,by+33,24,'bold','ACC',1,aa*0.95);
   });},
 list:(x,b,a,t,t0)=>{
   b.items.forEach((s,i)=>{
     const d=(b.at||0)+i*(b.stagger||0.42), aa=ease(seg(t,t0+d,t0+d+0.45)), y=b.y+i*(b.lh||130);
     x.save();x.translate((1-aa)*-40,0);
     rule(x,150,y,8+58*aa,aa);
     ltext(x,s,240,y,b.px||64,'bold','TYPE',3,aa);
     x.restore();
   });},
 vs:(x,b,a,t,t0)=>{
   [[b.left,0.29,'CAU'],[b.right,0.71,'ACC']].forEach((q,i)=>{
     const aa=ease(seg(t,t0+(b.at||0)+i*0.25,t0+(b.at||0)+i*0.25+0.60));
     const cx=W*q[1];
     ctext(x,q[0].t,cx,b.y,b.px||150,'bold',q[2],-3,aa);
     ctext(x,q[0].l,cx,b.y+104,30,'bold','CAU',4,aa);
   });},
 caveat:(x,b,a)=>{
   const bx=130,by=b.y,bw=W-260,bh=b.h||250;
   x.globalAlpha=a*0.90;x.fillStyle='rgba(11,11,13,0.88)';x.fillRect(bx,by,bw,bh);
   x.globalAlpha=a;x.strokeStyle=C.ACC;x.lineWidth=4;
   x.beginPath();x.moveTo(bx,by);x.lineTo(bx,by+bh);x.stroke();x.globalAlpha=1;
   ltext(x,b.title,bx+38,by+52,30,'bold','ACC',5,a);
   F(x,'normal',34);
   wrap(x,b.t,bw-76).forEach((s,i)=>ltext(x,s,bx+38,by+112+i*46,34,'normal','TYPE',0,a*0.95));
 }
};

function chrome(x,t){
  const a=ease(seg(t,0.10,0.65));
  ltext(x,SPEC.eyebrow,62,86,26,'bold','CAU',6,a*.9);
  rtext(x,SPEC.date,W-62,86,26,'bold','CAU',6,a*.9);
  x.globalAlpha=a*.5;x.strokeStyle=C.CAU;x.lineWidth=2;
  x.beginPath();x.moveTo(62,112);x.lineTo(W-62,112);x.stroke();
  const b=ease(seg(t,0.40,1.05));
  x.globalAlpha=b*.55;x.beginPath();x.moveTo(62,1566);x.lineTo(W-62,1566);x.stroke();x.globalAlpha=1;
  ltext(x,'SOURCE',62,1606,24,'bold','ACC',5,b*.95);
  rtext(x,SPEC.source,W-62,1606,24,'normal','CAU',1,b*.85);
}
function captions(x,t){
  for(const c of SPEC.cues){
    if(t<c.a-0.14||t>c.b+0.10)continue;
    const inp=ease(seg(t,c.a-0.14,c.a+0.09)), out=1-ease(seg(t,c.b-0.05,c.b+0.10));
    const al=Math.min(inp,out); if(al<=0.01)continue;
    F(x,'bold',54);
    const lines=wrap(x,c.t,W-220), y0=1430-(lines.length-1)*33;
    x.save();x.translate(0,(1-inp)*16);
    lines.forEach((s,i)=>{
      const yy=y0+i*66;F(x,'bold',54);const tw=x.measureText(s).width;
      x.globalAlpha=al*.74;x.fillStyle='rgba(11,11,13,1)';x.fillRect(W/2-tw/2-22,yy-38,tw+44,74);x.globalAlpha=1;
      ctext(x,s,W/2,yy,54,'bold','TYPE',0,al);
    });
    x.restore();break;
  }
}
function seek(t){
  const x=document.getElementById('c').getContext('2d');
  x.setTransform(1,0,0,1,0,0);x.globalAlpha=1;
  x.fillStyle=C.BASE;x.fillRect(0,0,W,H);
  let b=SPEC.beats[0];for(const q of SPEC.beats)if(t>=q.a)b=q;
  plate(x,b.plate,clamp((t-b.a)/(b.b-b.a),0,1),b.mv);
  for(const blk of (b.blocks||[])){
    const at=b.a+(blk.at||0), a=ease(seg(t,at,at+(blk.dur||0.65)));
    if(a<=0.001)continue;
    (BLOCKS[blk.k]||(()=>{}))(x,blk,a,t,b.a);
  }
  vignette(x);chrome(x,t);captions(x,t);grain(x,t);
  for(const q of SPEC.beats){
    if(q.a===0)continue;
    if(t>=q.a-0.05&&t<q.a+0.05){x.globalAlpha=0.14*(1-Math.abs(t-q.a)/0.05);x.fillStyle=C.ACC;x.fillRect(0,0,W,H);x.globalAlpha=1;}
  }
}
window.__seek=seek;
window.__init=(spec,imgs)=>{SPEC=spec;PLATES=imgs;initGrain();window.__dur=spec.dur;};
