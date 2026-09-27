// Opus 5.5 v4, the reference episode for the standard (build/standard/).
const IMAGES=['laptop','chess','track','mag'];
// cut before word index i, lead o seconds: hook|title|date|parity|bench|speed|price|catch|close
const CUTS=[[9,.15],[16,.15],[20,.15],[36,.15],[51,.12],[60,.12],[81,.12],[91,.12]];
const SC=[
// 0 HOOK — laptop B-roll, FASTER / CHEAPER punch-ins
(t,a,b)=>{x.fillStyle=INK;x.fillRect(0,0,W,H);if(IMG.laptop)cover(IMG.laptop,a,t,1);scrim(.5);
  pop(t,at('faster')-.08,540,760,()=>pill('FASTER',0,0,110,ACC,INK));
  pop(t,at('cheaper.')-.08,540,960,()=>pill('CHEAPER',0,0,110,'#FFFFFF',INK));
  const d=cl(1-prog(t,3.7,.3));if(d>0){x.globalAlpha=d;rr(160,150,760,120,16);x.fillStyle='rgba(11,11,13,.72)';x.fill();
    txt('EDUCATIONAL ONLY. NOT FINANCIAL ADVICE.',540,200,30,'#FFFFFF',700,'center',2);txt('MADE WITH CLAUDE OPUS 5.5',540,246,26,ACC,700,'center',3);x.globalAlpha=1}},
// 1 TITLE — slam
(t,a,b)=>{camera(t,a,()=>{x.fillStyle=PAPER;x.fillRect(-200,-200,W+400,H+400);
  x.fillStyle=ACC;x.fillRect(-200,540,(W+400)*eo(prog(t,a,.4)),26);
  [['CLAUDE',at('claude')],['OPUS',at('opus')],['5.5',at('five')]].forEach(([s,ts],i)=>pop(t,ts-.12,540,[720,900,1130][i],()=>txt(s,0,0,i==2?250:170,INK,900,'center',i==2?0:4),.3));})},
// 2 DATE — calendar flip
(t,a,b)=>{camera(t,a,()=>{x.fillStyle=INK;x.fillRect(-200,-200,W+400,H+400);
  txt('LAUNCHED',540,520,56,MUTE,800,'center',8);
  const f=eo(prog(t,at('september')-.1,.45));x.save();x.translate(540,900);x.scale(1,Math.max(.02,f));
  rr(-280,-260,560,520,36);x.fillStyle=PAPER;x.fill();x.fillStyle=RED;rr(-280,-260,560,130,36);x.fill();x.fillRect(-280,-170,560,40);
  txt('SEP',0,-165,72,'#FFFFFF',900,'center',8);txt(String(Math.round(lerp(1,22,eo(prog(t,at('twenty-second.')-.1,.5))))),0,190,300,INK,900);x.restore();
  pop(t,at('twenty-second.')+.3,540,1290,()=>txt('2026 · available now',0,0,46,'#FFFFFF',700))})},
// 3 FABLE PARITY — chess kings B-roll, punch-in mid-scene
(t,a,b)=>{x.fillStyle=INK;x.fillRect(0,0,W,H);const pz=T(28).s-.1;
  if(IMG.chess){if(t<pz)cover(IMG.chess,a,t,-1);else{x.save();x.translate(W/2,H/2);x.scale(1.3,1.3);x.translate(-W/2-60,-H/2+80);cover(IMG.chess,pz,t,1);x.restore()}}
  scrim(.55);
  pop(t,at('matches')-.1,540,330,()=>{txt('OPUS 5.5',-250,0,64,ACC,900);txt('≈',0,4,90,'#FFFFFF',900);txt('FABLE 5.1',250,0,64,'#FFFFFF',900)});
  pop(t,T(28).s-.05,540,440,()=>txt("Anthropic's most powerful public model",250*0+0,0,36,'#E8E8E4',600));
  pop(t,at('work.')-.3,540,1230,()=>pill("ANTHROPIC'S CLAIM",0,0,48,RED,'#FFFFFF'));
  flashIn(t,a);flashIn(t,pz)},
// 4 CODING BENCHMARK — bars
(t,a,b)=>{camera(t,a,()=>{x.fillStyle=INK;x.fillRect(-200,-200,W+400,H+400);
  txt('TOUGH CODING TEST',540,300,62,'#FFFFFF',900,'center',3);txt('Terminal-Bench 4.0 · Anthropic’s results',540,370,34,MUTE,600);
  const base=1280,hmax=720,g0=at('beat')-.1;
  [['OPUS 5.5',66.4,ACC,at('sixty-six')],['FABLE 5.1',55.8,'#FFFFFF',at('fifty-six.')]].forEach(([n,v,col,land],i)=>{
    const p=eio(cl((t-g0)/(land+.5-g0))),val=v*p,h=hmax*(val/70),X=230+i*400;
    rr(X,base-Math.max(h,4),220,Math.max(h,4),14);x.fillStyle=col;x.fill();
    txt(val.toFixed(1)+'%',X+110,base-h-30,64,col,900);txt(n,X+110,base+76,46,'#FFFFFF',800)});
  })},
// 5 SPEED — running track B-roll
(t,a,b)=>{x.fillStyle=INK;x.fillRect(0,0,W,H);if(IMG.track){const p=prog(t,a,b-a);x.save();x.translate(W/2,H*.62);const z=1.05+.5*eio(p);x.scale(z,z);x.translate(-W/2,-H*.62);cover(IMG.track,a,t,0);x.restore()}
  x.strokeStyle='rgba(255,255,255,.28)';x.lineWidth=5;for(let i=0;i<16;i++){const ang=i/16*6.283,r0=((t*1400+i*97)%900)+120;x.beginPath();x.moveTo(540+Math.cos(ang)*r0,900+Math.sin(ang)*r0);x.lineTo(540+Math.cos(ang)*(r0+160),900+Math.sin(ang)*(r0+160));x.stroke()}
  scrim(.5);
  pop(t,at('thirty')-.15,540,720,()=>{txt('+'+Math.round(30*eo(prog(t,at('thirty'),.6)))+'%',0,0,260,'#FFFFFF',900);});
  pop(t,at('faster',20)-.1,540,860,()=>pill('FASTER OUTPUT vs OPUS 5',0,0,46,ACC,INK));
  flashIn(t,a)},
// 6 PRICE — old price struck, new price rolls, −40% claim
(t,a,b)=>{camera(t,a,()=>{x.fillStyle=PAPER;x.fillRect(-200,-200,W+400,H+400);
  txt('PER MILLION TOKENS',540,300,38,MUTE,800,'center',5);
  const s2=at('anthropic',60)-.2,z=t>s2?eo(prog(t,s2,.4)):0;x.save();x.translate(540,700);x.scale(lerp(1,.8,z),lerp(1,.8,z));x.translate(0,lerp(0,-150,z));
  x.globalAlpha=.6;txt('OPUS 5',0,-40,40,INK,800,'center',4);txt('$5 in · $25 out',0,50,70,INK,800);
  const st=eo(prog(t,at('four')-.1,.3));x.strokeStyle=RED;x.lineWidth=12;x.beginPath();x.moveTo(-290,28);x.lineTo(-290+580*st,28);x.stroke();x.globalAlpha=1;
  pop(t,at('four')-.2,0,330,()=>{rr(-460,-150,920,300,26);x.fillStyle=INK;x.fill();txt('OPUS 5.5',0,-60,44,ACC,800,'center',4);
    txt(`$4 in · $${t>at('twenty')-.1?20:25} out`,0,60,96,'#FFFFFF',900)});x.restore();
  pop(t,at('forty')-.2,540,1220,()=>pill('≈ −40% ON TYPICAL JOBS',0,0,54,ACC,INK));
  pop(t,at('says',70)-.1,540,1330,()=>txt("Anthropic's estimate",0,0,36,MUTE,600))})},
// 7 THE CATCH — magnifier B-roll + stamp
(t,a,b)=>{x.fillStyle=INK;x.fillRect(0,0,W,H);if(IMG.mag)cover(IMG.mag,a,t,1);scrim(.6);
  pop(t,at('catch?')-.15,540,380,()=>txt('THE CATCH',0,0,110,'#FFFFFF',900,'center',4));
  const q=prog(t,at('own')-.15,.25);if(q>0){const s=lerp(2.2,1,eo(q));x.save();x.translate(540,760);x.rotate(-0.08);x.scale(s,s);x.globalAlpha=cl(q*2);
    x.strokeStyle=RED;x.lineWidth=12;rr(-400,-110,800,220,12);x.stroke();txt("ANTHROPIC'S",0,-14,64,RED,900,'center',3);txt('OWN NUMBERS',0,66,64,RED,900,'center',3);x.restore();x.globalAlpha=1}
  pop(t,at('not')-.1,540,1010,()=>pill('NOT INDEPENDENT TESTS',0,0,48,'#FFFFFF',INK));
  flashIn(t,a)},
// 8 CLOSE — what to do
(t,a,b)=>{camera(t,a,()=>{x.fillStyle=INK;x.fillRect(-200,-200,W+400,H+400);
  txt('PAY FOR OPUS?',540,480,90,'#FFFFFF',900,'center',3);
  [['Rerun one real job on 5.5',at('rerun')],['Compare the bill',at('compare')]].forEach(([s,ts],i)=>{const p=eo(prog(t,ts-.15,.35));if(p<=0)return;
    const y=720+i*170;x.globalAlpha=p;x.save();x.translate(lerp(-80,0,p),0);rr(110,y-80,860,130,20);x.fillStyle='#1E1E24';x.fill();
    x.beginPath();x.arc(190,y-15,40,0,7);x.fillStyle=ACC;x.fill();txt(String(i+1),190,y+5,48,INK,900);txt(s,260,y+2,48,'#FFFFFF',800,'left');x.restore();x.globalAlpha=1});
  const e=prog(t,b-1.4,.4);if(e>0){x.globalAlpha=e;txt('Sources in the description · Made with Claude Opus 5.5',540,1340,30,'#BDBDB8',600);x.globalAlpha=1}})},
];

