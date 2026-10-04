// Scene-type library for the standard engine. Loaded after core.js, before the episode's scenes.js.
// An episode defines BEATS = [{cue:'first words of the beat', ...K.kind(opts)}]; cues are phrases from the
// script, resolved against words.json at init, so the cut list follows whatever voice is dropped in.
const U=Math.min(W,H)/1080*(W>H?1.2:1), LAND=W>H, CX=W/2, CY=LAND?H*0.42:H*0.40, BLUE='#3DA9FC', GREEN='#35C46A';
window.__errs=[];
function findPhrase(ph,from=0){const q=ph.split(/\s+/).map(nrm).filter(Boolean);
  for(let i=Math.max(0,from);i<=WORDS.length-q.length;i++){let ok=true;for(let k=0;k<q.length;k++)if(nrm(WORDS[i+k].w)!==q[k]){ok=false;break}if(ok)return i}
  window.__errs.push('phrase not found: "'+ph+'" after word '+from);return -1}
// time of a phrase inside beat b (searches from the beat's first word)
function A(b,ph){b._c=b._c||{};if(!(ph in b._c)){const i=findPhrase(ph,b.i0);b._c[ph]=i<0?b.t0+0.5:WORDS[i].s}return b._c[ph]}
let BEATS=[];
const CUTS=()=>{let p=0;let ch='';BEATS.forEach((b,k)=>{const i=findPhrase(b.cue,p);b.skip=i<0;if(i<0)return;b.i0=i;p=i+1;if(b.tag)ch=b.tag;b.chap=ch});
  BEATS=BEATS.filter(b=>!b.skip); // a cue missing from this narration drops its beat (logged in __errs)
  BEATS.forEach(b=>b.t0=WORDS[b.i0].s);return BEATS.slice(1).map(b=>[b.i0,.12])};
const SC=new Proxy([],{get:(o,k)=>k==='length'?BEATS.length:(isNaN(k)?o[k]:((t,a,e)=>{BEATS[+k].draw(t,a,e,BEATS[+k]);disclosure(t)}))});
// compliance card, first 4 s of every video (CLAUDE.md)
function disclosure(t){const d=cl(1-prog(t,3.7,.3));if(d<=0)return;x.globalAlpha=d;font(28*U,700);const w=x.measureText('EDUCATIONAL ONLY. NOT FINANCIAL ADVICE.').width+60*U;
  rr(CX-w/2,(LAND?H-260:150)*U,w,64*U,14*U);x.fillStyle='rgba(11,11,13,.75)';x.fill();txt('EDUCATIONAL ONLY. NOT FINANCIAL ADVICE.',CX,(LAND?H-260:150)*U+42*U,28*U,'#FFFFFF',700,'center',2);x.globalAlpha=1}

// ---------- shared chrome ----------
function srcTag(s){if(!s)return;font(24*U,800);const w=x.measureText(s).width+36*U;const X=W-w-40*U,Y=40*U;
  rr(X,Y,w,44*U,22*U);x.fillStyle='rgba(11,11,13,.72)';x.fill();x.strokeStyle=s==='OPINION'?ACC:(s.startsWith('REPORTED')||s==='COMPANY CLAIM'?RED:'rgba(255,255,255,.35)');x.lineWidth=2;x.stroke();
  txt(s,X+w/2,Y+31*U,24*U,'#FFFFFF',800,'center',2)}
function chapterTag(c){if(!c)return;font(24*U,800);const w=x.measureText(c).width+36*U;rr(40*U,40*U,w,44*U,22*U);x.fillStyle=ACC;x.fill();txt(c,40*U+w/2,40*U+31*U,24*U,INK,900,'center',2)}
function chrome(b){chapterTag(b.chap);srcTag(b.src)}
function tagAt(t,b,o){ // pill popping in on a phrase: {at,text,y,bg,fg,size}
  pop(t,A(b,o.at)-.08,o.x??CX,o.y??CY,()=>pill(o.text,0,0,(o.size||64)*U,o.bg||ACC,o.fg||INK))}
function stampAt(t,b,o){const q=prog(t,A(b,o.at)-.1,.25);if(q<=0)return;const s=lerp(2.2,1,eo(q));x.save();x.translate(o.x??CX,o.y??CY);x.rotate(-0.07);x.scale(s,s);x.globalAlpha=cl(q*2);
  font((o.size||84)*U,900);const w=x.measureText(o.text).width+70*U,h=(o.size||84)*1.7*U;x.strokeStyle=o.color||RED;x.lineWidth=10*U;rr(-w/2,-h/2,w,h,10*U);x.stroke();
  txt(o.text,0,(o.size||84)*.36*U,(o.size||84)*U,o.color||RED,900,'center',4);x.restore();x.globalAlpha=1}
function pillW(s,sz,padX=44){font(sz,900);return x.measureText(s).width+padX*2}
// lay out pills in centred rows that fit maxW; returns [{x,y}] centres
function rowLayout(texts,sz,maxW,gap,y0,rowH){const ws=texts.map(s=>pillW(s,sz));const rows=[[]];let cur=0;
  ws.forEach((w,i)=>{if(rows[rows.length-1].length&&cur+gap+w>maxW){rows.push([]);cur=0}rows[rows.length-1].push(i);cur+=(cur?gap:0)+w});
  const pos=[];rows.forEach((r,ri)=>{const tot=r.reduce((a,i)=>a+ws[i],0)+gap*(r.length-1);let X=CX-tot/2;r.forEach(i=>{pos[i]={x:X+ws[i]/2,y:y0+ri*rowH};X+=ws[i]+gap})});return pos}
function bg(c){x.fillStyle=c;x.fillRect(-200,-200,W+400,H+400)}
// ---------- moving plates: a video clip (<name>.webm) when present, else the still with a camera move ----------
let VID={};const RATE=0.85;
function clipTime(v,s){const D=Math.max(.2,(v.duration||4)-.06),u=Math.max(0,s)*RATE,m=u%(2*D);return m<D?m:2*D-m}
function media(nm,t,a,dir){const v=VID[nm];if(v&&v.readyState>=2){cover(v,a,t,dir||1);return true}const im=IMG[nm];if(im){cover(im,a,t,dir||1);return true}return false}
// graphic scenes sit on a tinted moving plate: 'ink' = dark tint, 'paper' = frosted light tint
function plate(b,t,a,mode){bg(mode==='paper'?PAPER:INK);const nm=b.plate;if(!nm||!media(nm,t,a,b.pdir||1))return;
  x.fillStyle=mode==='paper'?'rgba(244,243,239,.74)':'rgba(11,11,13,.44)';x.fillRect(-200,-200,W+400,H+400)}
// capture hook: seek the clip the scene at time t is showing, then draw
window.__prep=async t=>{const S=window.__S;if(!S)return;let k=S.length-1;for(let i=0;i<S.length;i++)if(t<S[i][1]){k=i;break}
  const b=BEATS[k];if(!b)return;const nm=b.img||b.plate,v=VID[nm];if(!v)return;const ct=clipTime(v,t-S[k][0]);
  if(Math.abs(v.currentTime-ct)<1e-3)return;await new Promise(r=>{const to=setTimeout(r,3000);v.onseeked=()=>{clearTimeout(to);r()};v.currentTime=ct})};
function counter(t,t0,to,d=0.9){return to*eo(prog(t,t0,d))}
function fmtNum(v,dec=0){return v.toLocaleString('en-US',{minimumFractionDigits:dec,maximumFractionDigits:dec})}

// ---------- scene kinds ----------
const K={
// B-roll photo with continuous camera move; optional tags / stamp / big stat
broll:o=>({src:o.src,img:o.img,draw:(t,a,e,b)=>{bg(INK);
  if(o.punch&&t>A(b,o.punch)){x.save();x.translate(W/2,H/2);x.scale(1.28,1.28);x.translate(-W/2+(o.px||0)*U,-H/2+(o.py||0)*U);media(o.img,A(b,o.punch),t,-(o.dir||1));x.restore()}else media(o.img,a,t,o.dir||1);
  scrim(.45);(o.tags||[]).forEach(g=>tagAt(t,b,g));if(o.stat){const s=o.stat;pop(t,A(b,s.at)-.1,CX,s.y??CY,()=>{
    txt((s.prefix||'')+fmtNum(counter(t,A(b,s.at),s.value,s.d||0.8),s.dec||0)+(s.suffix||''),0,0,(s.size||220)*U,s.color||'#FFFFFF',900);
    if(s.label)txt(s.label,0,70*U,44*U,s.color||ACC,800,'center',6)})}
  if(o.stamp)stampAt(t,b,o.stamp);flashIn(t,a);chrome(b)}}),
// chapter card on paper: number + title
chapter:o=>({tag:o.tag,draw:(t,a,e,b)=>{camera(t,a,()=>{plate(b,t,a,'paper');x.fillStyle=ACC;x.fillRect(-200,CY+120*U,(W+400)*eo(prog(t,a,.45)),18*U);
  pop(t,a+.05,CX,CY-150*U,()=>txt(o.n,0,0,120*U,ACC,900,'center',4));
  pop(t,a+.18,CX,CY+60*U,()=>txt(o.title,0,0,(LAND?150:120)*U,INK,900,'center',3))});chapterTag(b.chap)}}),
// calendar flip for a date
date:o=>({src:o.src,draw:(t,a,e,b)=>{camera(t,a,()=>{plate(b,t,a,'ink');txt(o.label,CX,CY-(LAND?290:330)*U,(LAND?44:52)*U,MUTE,800,'center',8);
  const f=eo(prog(t,A(b,o.at)-.1,.45));x.save();x.translate(CX,CY+20*U);x.scale(1,Math.max(.02,f));
  rr(-260*U,-250*U,520*U,500*U,34*U);x.fillStyle=PAPER;x.fill();x.fillStyle=o.color||RED;rr(-260*U,-250*U,520*U,125*U,34*U);x.fill();x.fillRect(-260*U,-165*U,520*U,40*U);
  txt(o.month,0,-162*U,68*U,'#FFFFFF',900,'center',8);txt(String(Math.round(lerp(1,o.day,eo(prog(t,A(b,o.at),.5))))),0,175*U,280*U,INK,900);x.restore();
  if(o.sub)pop(t,A(b,o.at)+.4,CX,CY+330*U,()=>txt(o.sub,0,0,48*U,'#FFFFFF',800,'center',4))});chrome(b)}}),
// big text lines slammed onto paper (or ink)
slam:o=>({src:o.src,draw:(t,a,e,b)=>{camera(t,a,()=>{plate(b,t,a,o.dark?'ink':'paper');const n=o.lines.length;
  o.lines.forEach((l,k)=>pop(t,A(b,l.at)-.1,CX,CY+(k-(n-1)/2)*(l.gap||170)*U,()=>txt(l.text,0,(l.size||130)*.35*U,(l.size||130)*U,l.color||(o.dark?'#FFFFFF':INK),900,'center',3)))});chrome(b)}}),
// row of chips popping in (optional photo behind)
chips:o=>({src:o.src,img:o.img,draw:(t,a,e,b)=>{if(o.img){bg(INK);media(o.img,a,t,o.dir||1);scrim(.7)}else camera(t,a,()=>plate(b,t,a,'ink'));
  if(o.title)pop(t,a+.05,CX,CY-(LAND?190:260)*U,()=>txt(o.title,0,0,(o.tsize||76)*U,'#FFFFFF',900,'center',3));
  const sz=(o.size||52)*U,pos=rowLayout(o.items.map(i=>i.text),sz,W-240*U,34*U,CY+40*U,150*U);
  o.items.forEach((it,k)=>pop(t,A(b,it.at)-.08,pos[k].x,pos[k].y,()=>pill(it.text,0,0,sz,it.bg||ACC,it.fg||INK)));flashIn(t,a);chrome(b)}}),
// step flow A → B → C keyed to words
steps:o=>({src:o.src,img:o.img,draw:(t,a,e,b)=>{if(o.img){bg(INK);media(o.img,a,t,1);scrim(.72)}else camera(t,a,()=>plate(b,t,a,'ink'));
  if(o.title)pop(t,a+.05,CX,CY-(LAND?220:330)*U,()=>txt(o.title,0,0,66*U,'#FFFFFF',900,'center',3));
  const n=o.items.length;let sz=(o.size||(n>3?42:50))*U,gap=90*U,ws=o.items.map(i=>pillW(i.text,sz)),tot=ws.reduce((a,v)=>a+v,0)+gap*(n-1);
  if(LAND&&tot>W-160*U){const k=(W-160*U)/tot;sz*=k;gap*=k;ws=o.items.map(i=>pillW(i.text,sz));tot=ws.reduce((a,v)=>a+v,0)+gap*(n-1)}
  const fit=LAND;let X0=CX-tot/2;const P=o.items.map((it,k)=>{const p=fit?{x:X0+ws[k]/2,y:CY+30*U}:{x:CX,y:CY-(n-1)*95*U+k*190*U};X0+=ws[k]+gap;return p});
  o.items.forEach((it,k)=>{const p=back(prog(t,A(b,it.at)-.08,.3));if(p<=0)return;const {x:X,y:Y}=P[k];
    if(k>0){const q=eo(prog(t,A(b,it.at)-.25,.25)),pv=P[k-1];x.strokeStyle=ACC;x.lineWidth=8*U;x.beginPath();
      if(fit){const x1=pv.x+ws[k-1]/2+10*U,x2=X-ws[k]/2-10*U;x.moveTo(x1,Y);x.lineTo(x1+(x2-x1)*q,Y)}else{x.moveTo(X,pv.y+50*U);x.lineTo(X,pv.y+50*U+(Y-pv.y-100*U)*q)}x.stroke()}
    x.save();x.translate(X,Y);x.scale(p,p);pill(it.text,0,0,sz,it.bg||(k===n-1?ACC:'#FFFFFF'),INK);x.restore()});chrome(b)}}),
// app ecosystem: dot in the middle, app tiles orbit, counter to 4,000+
apps:o=>({src:o.src,draw:(t,a,e,b)=>{camera(t,a,()=>{plate(b,t,a,'ink');const t0=A(b,o.at),R=330*U;
  const names=['EMAIL','CALENDAR','DOCS','CRM','SHEETS','TICKETS','CHAT','DRIVE','CODE','NOTES','BILLING','DESIGN'];
  names.forEach((nm,k)=>{const p=eo(prog(t,t0+k*.06,.4));if(p<=0)return;const ang=k/names.length*6.283+t*.25;
    const X=CX+Math.cos(ang)*R*p*(LAND?1.6:1),Y=CY+Math.sin(ang)*R*p*.8;x.globalAlpha=p;pill(nm,X,Y,26*U,'#1E1E24','#BDBDB8',22*U);x.globalAlpha=1});
  const g=x.createRadialGradient(CX,CY,0,CX,CY,150*U);g.addColorStop(0,'#FFE3A0');g.addColorStop(.35,ACC);g.addColorStop(1,'rgba(255,176,32,0)');x.fillStyle=g;x.beginPath();x.arc(CX,CY,(150+8*Math.sin(t*3))*U,0,7);x.fill();
  pop(t,t0+.2,CX,CY+10*U,()=>txt(fmtNum(Math.round(counter(t,t0+.2,4000,1.2)))+'+',0,30*U,96*U,INK,900));
  pop(t,t0+.6,CX,CY+(LAND?300:470)*U,()=>txt(o.label||'APPS VIA PLUGINS',0,0,48*U,'#FFFFFF',800,'center',6))});chrome(b)}}),
// computers: 'separate' (one isolated box per dot) or 'shared' (many bots, one box, blast radius)
machine:o=>({src:o.src,draw:(t,a,e,b)=>{camera(t,a,()=>{plate(b,t,a,'ink');
  if(o.title)pop(t,a+.05,CX,CY-(LAND?285:520)*U,()=>txt(o.title,0,0,(LAND?54:62)*U,'#FFFFFF',900,'center',3));
  if(o.mode==='separate'){[-1,0,1].forEach((k,i)=>{const p=back(prog(t,a+.15+i*.15,.35));if(p<=0)return;const X=CX+k*(LAND?520:330)*U,Y=CY+40*U;
      x.save();x.translate(X,Y);x.scale(p,p);rr(-180*U,-150*U,360*U,300*U,22*U);x.fillStyle='#16161A';x.fill();x.strokeStyle=ACC;x.lineWidth=5*U;x.stroke();
      x.beginPath();x.arc(0,-20*U,48*U+4*Math.sin(t*3+i),0,7);x.fillStyle=ACC;x.fill();txt('USER '+(i+1),0,100*U,30*U,'#BDBDB8',800,'center',4);x.restore()});
    if(o.lockAt)pop(t,A(b,o.lockAt)-.1,CX,CY+(LAND?270:300)*U,()=>pill('ISOLATED',0,0,46*U,'#FFFFFF',INK));
    if(o.laptopAt)pop(t,A(b,o.laptopAt)-.1,CX,CY+(LAND?380:420)*U,()=>pill('YOUR LAPTOP: OFF',0,0,40*U,'#1E1E24','#FFFFFF'))}
  else{const p=back(prog(t,a+.1,.35));x.save();x.translate(CX,CY+40*U);x.scale(p,p);rr(-(LAND?560:420)*U,-200*U,(LAND?1120:840)*U,400*U,26*U);x.fillStyle='#14161C';x.fill();x.strokeStyle=BLUE;x.lineWidth=6*U;x.stroke();
      const nb=o.bots||4;for(let i=0;i<nb;i++){const q=back(prog(t,a+.3+i*.15,.3));const X=(i-(nb-1)/2)*(LAND?220:170)*U;x.save();x.translate(X,-50*U);x.scale(q,q);x.beginPath();x.arc(0,0,44*U+3*Math.sin(t*4+i),0,7);x.fillStyle=BLUE;x.fill();txt('BOT '+String.fromCharCode(65+i),0,90*U,26*U,'#BDBDB8',800,'center',3);x.restore()}
      const s=eo(prog(t,a+.9,.4));x.globalAlpha=s;pill('SHARED FILES',-(LAND?220:170)*U,135*U,30*U,'#2A2E38','#FFFFFF',20*U);pill('SHARED LOGINS',(LAND?220:170)*U,135*U,30*U,'#2A2E38','#FFFFFF',20*U);x.globalAlpha=1;x.restore();
    if(o.blastAt){const q=prog(t,A(b,o.blastAt)-.1,1.2);if(q>0){for(let r=0;r<3;r++){const rr2=((q*1.2+r*.33)%1);x.strokeStyle=`rgba(255,74,61,${(1-rr2)*.8})`;x.lineWidth=8*U;x.beginPath();x.ellipse(CX,CY+40*U,(300+rr2*700)*U,(160+rr2*380)*U,0,0,7);x.stroke()}
      pop(t,A(b,o.blastAt),CX,CY-(LAND?250:300)*U,()=>pill('BLAST RADIUS',0,0,54*U,RED,'#FFFFFF'))}}}});chrome(b)}}),
// group chat between bots (illustration)
chat:o=>({src:o.src||'ILLUSTRATION',draw:(t,a,e,b)=>{camera(t,a,()=>{plate(b,t,a,'ink');const pw=LAND?900*U:860*U,X0=CX-pw/2;
  rr(X0,90*U,pw,(LAND?600:1200)*U,26*U);x.fillStyle='#181B22';x.fill();txt(o.title||'# group-chat',X0+40*U,150*U,34*U,'#8FA3BF',800,'left');
  let y=230*U;o.msgs.forEach((m,k)=>{const p=back(prog(t,A(b,m.at)-.1,.3));if(p<=0)return;const col=[BLUE,'#B07CFF',GREEN,ACC][k%4];
    x.save();x.translate(X0+60*U,y);x.scale(p,p);x.beginPath();x.arc(24*U,24*U,24*U,0,7);x.fillStyle=col;x.fill();txt(m.who,64*U,20*U,26*U,col,900,'left',2);
    font(34*U,700);const w=x.measureText(m.text).width+40*U;rr(64*U,32*U,w,58*U,18*U);x.fillStyle='#252A35';x.fill();txt(m.text,84*U,72*U,34*U,'#FFFFFF',700,'left');x.restore();y+=(LAND?104:118)*U})});chrome(b)}}),
// rules panel / toggle switches; o.rows=[{at,label,state:'ON'|'OFF'|'ASK',danger}]
toggles:o=>({src:o.src,draw:(t,a,e,b)=>{camera(t,a,()=>{plate(b,t,a,'ink');if(o.title)pop(t,a+.05,CX,CY-(LAND?300:420)*U,()=>txt(o.title,0,0,62*U,'#FFFFFF',900,'center',3));
  const n=o.rows.length;o.rows.forEach((r,k)=>{const p=eo(prog(t,A(b,r.at)-.15,.3));if(p<=0)return;const Y=CY-((n-1)/2-k)*150*U+20*U,w=(LAND?980:900)*U;
    x.globalAlpha=p;rr(CX-w/2,Y-55*U,w,110*U,20*U);x.fillStyle='#1A1C22';x.fill();txt(r.label,CX-w/2+40*U,Y+16*U,44*U,'#FFFFFF',800,'left',2);
    const on=t>A(b,r.flip||r.at)+.25,sw=eo(prog(t,A(b,r.flip||r.at)+.1,.25));const col=r.danger?RED:(r.state==='ASK'?ACC:GREEN);
    rr(CX+w/2-200*U,Y-32*U,140*U,64*U,32*U);x.fillStyle=on?col:'#3A3D45';x.fill();x.beginPath();x.arc(CX+w/2-168*U+76*U*sw,Y,26*U,0,7);x.fillStyle='#FFFFFF';x.fill();
    if(r.state)txt(r.state,CX+w/2-230*U,Y+14*U,30*U,on?col:MUTE,900,'right',2);x.globalAlpha=1})});chrome(b)}}),
// vertical bars with counters; items=[{label,value,color,at,fmt:(v)=>str}]
bars:o=>({src:o.src,draw:(t,a,e,b)=>{camera(t,a,()=>{plate(b,t,a,o.paper?'paper':'ink');const fg=o.paper?INK:'#FFFFFF';
  if(o.title)pop(t,a+.05,CX,(LAND?110:300)*U,()=>txt(o.title,0,0,(LAND?54:64)*U,fg,900,'center',3));
  const n=o.items.length,base=LAND?H-300*U:CY+420*U,hmax=LAND?base-(o.note?360:270)*U:760*U,mx=Math.max(...o.items.map(i=>Math.abs(i.value))),bw=(LAND?260:240)*U;
  o.items.forEach((it,k)=>{const p=eio(prog(t,A(b,it.at)-.1,.9)),v=it.value*p,h=hmax*Math.abs(v)/mx,X=CX+(k-(n-1)/2)*(LAND?560:360)*U;
    rr(X-bw/2,base-Math.max(h,4),bw,Math.max(h,4),14*U);x.fillStyle=it.color||ACC;x.fill();
    txt(it.fmt?it.fmt(v):fmtNum(v),X,base-h-28*U,(it.vsize||64)*U,it.color||ACC,900);txt(it.label,X,base+52*U,(LAND?34:40)*U,fg,800,'center',3)});
  if(o.note)pop(t,A(b,o.note.at),LAND?CX:CX,LAND?200*U:base+170*U,()=>pill(o.note.text,0,0,44*U,o.note.bg||ACC,INK))});chrome(b)}}),
// checklist of a side; rows=[{at,text,good}]
check:o=>({src:o.src,img:o.img,draw:(t,a,e,b)=>{bg(INK);media(o.img,a,t,o.dir||1);x.fillStyle='rgba(11,11,13,.62)';x.fillRect(0,0,W,H);
  pop(t,a+.05,CX,(LAND?150:330)*U,()=>pill(o.title,0,0,66*U,o.color||ACC,INK));
  o.rows.forEach((r,k)=>{const p=eo(prog(t,A(b,r.at)-.12,.3));if(p<=0)return;const Y=(LAND?290:520)*U+k*(LAND?130:150)*U,X=CX-(LAND?420:400)*U;
    x.globalAlpha=p;x.save();x.translate(lerp(-60,0,p)*U,0);x.beginPath();x.arc(X,Y,30*U,0,7);x.fillStyle=r.good?GREEN:RED;x.fill();
    txt(r.good?'✓':'✕',X,Y+12*U,34*U,'#FFFFFF',900);txt(r.text,X+60*U,Y+16*U,(LAND?52:46)*U,'#FFFFFF',800,'left',1);x.restore();x.globalAlpha=1});flashIn(t,a);chrome(b)}}),
// scorecard rows: [{at,label,winner:'DOTS'|'GROK BOT'|'NEITHER'}]
score:o=>({src:o.src||'OPINION',draw:(t,a,e,b)=>{camera(t,a,()=>{plate(b,t,a,'paper');pop(t,a+.05,CX,(LAND?140:300)*U,()=>txt(o.title||'OUR SCORECARD',0,0,70*U,INK,900,'center',4));
  o.rows.forEach((r,k)=>{const p=eo(prog(t,A(b,r.at)-.12,.3));if(p<=0)return;const Y=(LAND?290:500)*U+k*(LAND?140:170)*U,w=(LAND?1300:940)*U;
    x.globalAlpha=p;rr(CX-w/2,Y-55*U,w,110*U,16*U);x.fillStyle='#FFFFFF';x.fill();txt(r.label,CX-w/2+40*U,Y+16*U,(LAND?46:40)*U,INK,800,'left',2);
    const col=r.winner==='DOTS'?ACC:(r.winner==='NEITHER'?MUTE:BLUE);pill(r.winner,CX+w/2-(LAND?190:160)*U,Y,(LAND?40:34)*U,col,r.winner==='NEITHER'?'#FFFFFF':INK);x.globalAlpha=1})});chrome(b)}}),
// quote card
quote:o=>({src:o.src,draw:(t,a,e,b)=>{camera(t,a,()=>{plate(b,t,a,'ink');x.fillStyle='rgba(11,11,13,.25)';x.fillRect(-200,-200,W+400,H+400);
  const words=o.text.split(' '),t0=A(b,o.at);let line='',lines=[];font(70*U,800);words.forEach(w=>{const tl=line?line+' '+w:w;if(x.measureText(tl).width>(LAND?1400:900)*U){lines.push(line);line=w}else line=tl});lines.push(line);
  txt('“',CX-(LAND?720:460)*U,CY-150*U,200*U,ACC,900,'center');lines.forEach((l,k)=>{const p=eo(prog(t,t0+k*.25,.35));x.globalAlpha=p;txt(l,CX,CY-60*U+k*95*U,70*U,'#FFFFFF',800,'center');x.globalAlpha=1});
  pop(t,t0+.6,CX,CY+lines.length*95*U+20*U,()=>txt('— '+o.who,0,0,40*U,ACC,800,'center',4))});chrome(b)}}),
// timeline A → B with bracket
timeline:o=>({src:o.src,draw:(t,a,e,b)=>{camera(t,a,()=>{plate(b,t,a,'ink');const L=CX-(LAND?600:330)*U,R=CX+(LAND?600:330)*U,Y=CY+20*U,q=eio(prog(t,a+.1,.9));
  x.strokeStyle='#3A3D45';x.lineWidth=10*U;x.beginPath();x.moveTo(L,Y);x.lineTo(R,Y);x.stroke();x.strokeStyle=ACC;x.beginPath();x.moveTo(L,Y);x.lineTo(lerp(L,R,q),Y);x.stroke();
  [[L,o.a,BLUE,a+.05],[R,o.b,ACC,a+.8]].forEach(([X,p,col,ts])=>pop(t,ts,X,Y,()=>{x.beginPath();x.arc(0,0,26*U,0,7);x.fillStyle=col;x.fill();txt(p.date,0,-60*U,60*U,'#FFFFFF',900);txt(p.label,0,90*U,40*U,col,800,'center',3)}));
  if(o.span)pop(t,A(b,o.span.at)-.1,CX,Y-190*U,()=>pill(o.span.text,0,0,60*U,ACC,INK))});chrome(b)}}),
// closing call to comment: two sides + question
cta:o=>({src:o.src,img:o.img,draw:(t,a,e,b)=>{bg(INK);media(o.img,a,t,1);scrim(.55);
  const sz=(LAND?60:72)*U,wl=pillW(o.left,sz),wr=pillW(o.right,sz),gap=80*U;
  pop(t,A(b,o.atA)-.1,LAND?CX-(wr+gap)/2:CX,LAND?CY:CY-160*U,()=>pill(o.left,0,0,sz,ACC,INK));
  pop(t,A(b,o.atB)-.1,LAND?CX+(wl+gap)/2:CX,LAND?CY:CY+20*U,()=>pill(o.right,0,0,sz,BLUE,INK));
  pop(t,A(b,o.atC)-.1,CX,LAND?CY+200*U:CY+220*U,()=>pill('COMMENT BELOW',0,0,54*U,'#FFFFFF',INK));chrome(b)}}),
};
