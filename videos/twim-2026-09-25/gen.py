import re,json,numpy as np,soundfile as sf
from kokoro_onnx import Kokoro
K=Kokoro("/root/.cache/hyperframes/tts/models/kokoro-v1.0.onnx","/root/.cache/hyperframes/tts/voices/voices-v1.0.bin")
SR=24000;VOICE="am_michael";GS=0.10;GP=0.55
NP=8  # paragraphs == scenes

nw=open("compositions/components/number-wheel.html").read()
WHEEL_CSS=re.search(r'<style[^>]*>(.*?)</style>',nw,re.S).group(1)
WHEEL_JS=re.search(r'<script>(.*?)</script>',nw,re.S).group(1)

paras=[p.strip() for p in open("vo.txt").read().split("\n\n") if p.strip()]
assert len(paras)==NP,len(paras)
audio=[];t=0.0;SC=[];W=[]
for pi,p in enumerate(paras):
    flat=" ".join(p.split());s0=t
    for s in [x.strip() for x in re.findall(r'[^.!?]+[.!?]',flat) if x.strip()]:
        sm,_=K.create(s,voice=VOICE,speed=1.0,lang="en-us");d=len(sm)/SR
        ws=s.split();tot=sum(len(w)+1 for w in ws);acc=0
        for w in ws:
            a0=t+(acc/tot)*d;acc+=len(w)+1;W.append({"w":w,"s":round(a0,3),"e":round(t+(acc/tot)*d,3)})
        audio.append(sm);t+=d;audio.append(np.zeros(int(GS*SR),dtype=sm.dtype));t+=GS
    SC.append({"i":pi,"start":round(s0,3),"end":round(t-GS,3)})
    if pi<NP-1: audio.append(np.zeros(int((GP-GS)*SR),dtype=sm.dtype));t+=GP-GS
full=np.concatenate(audio);ADUR=round(len(full)/SR,3);sf.write("vo.wav",full,SR)
cuts=[0.0]+[round((SC[i]["end"]+SC[i+1]["start"])/2,3) for i in range(NP-1)]+[round(SC[-1]["end"]+0.3,3)]
B=[cuts[i] for i in range(NP)];DISC=4.5;TOTAL=round(cuts[NP]+DISC,3)
S=[(B[i],round(cuts[i+1]-B[i],3)) for i in range(NP)]

def wheel(v,cls=""): return f'<span class="hf-number-wheel {cls}" data-value="{v}"></span>'
def sc(i,num,inner):
    st,du=S[i]
    return (f'<div id="s{i+1}" class="clip" data-start="{st}" data-duration="{du}" data-track-index="0">'
      f'<div class="frame"><div class="fr-t"></div><div class="fr-b"></div>'
      f'<div class="slug">THE 10-YEAR AT 5%</div><div class="num">{num}</div>'
      f'<div class="tick tl"></div><div class="tick tr"></div></div>{inner}</div>')
SVG=lambda body:f'<svg width="1080" height="1920" style="position:absolute;inset:0">{body}</svg>'

# mortgage path 6.71 -> 6.76 -> 6.95 -> 7.03, scaled over 6.65..7.10
MPTS=[6.71,6.76,6.95,7.03]
def my(v): return round(1150-(v-6.65)/0.45*380)
MXY=[(150+i*250,my(v)) for i,v in enumerate(MPTS)]
MPOLY=" ".join(f"{x},{y}" for x,y in MXY)

SCENES=[
 # 1 — the print
 sc(0,"01",'<div class="rulebar" id="r1"></div><div class="kicker" id="k1">The print</div>'
   '<div class="lbl" id="a1" style="position:absolute;left:110px;top:560px">US 10-year Treasury yield</div>'
   f'<div class="big red" id="a2" style="position:absolute;left:110px;top:614px;font-size:200px">{wheel("5.12")}%</div>'
   +SVG('<line id="a3" x1="110" y1="900" x2="970" y2="900" stroke="#242427" stroke-width="3"/>')+
   '<div class="lbl" id="a4" style="position:absolute;left:110px;top:950px">Highest since</div>'
   '<div class="big" id="a5" style="position:absolute;left:110px;top:1000px;font-size:150px">2007</div>'
   '<div class="tag" id="a6" style="position:absolute;left:110px;top:1230px">Most of it in one day</div>'
   '<div class="stamp">Yield as of 2026-09-24 · press convergence</div>'
   '<div id="compliance">Educational only. Not financial advice.</div>'),
 # 2 — what it is
 sc(1,"02",'<div class="rulebar"></div><div class="kicker">What it actually is</div>'
   '<div class="big" id="b1" style="position:absolute;left:110px;top:560px;font-size:86px;width:880px">The price of<br>government money</div>'
   +SVG('<line id="b2" x1="110" y1="880" x2="970" y2="880" stroke="#242427" stroke-width="3"/>')+
   '<div class="lbl" id="b3" style="position:absolute;left:110px;top:930px">Lend to the Treasury for</div>'
   '<div class="big" id="b4" style="position:absolute;left:110px;top:980px;font-size:150px">10 YEARS</div>'
   '<div class="big red" id="b5" style="position:absolute;left:110px;top:1240px;font-size:62px;width:880px">Nearly every other price<br>is set off the back of it.</div>'
   '<div class="stamp">Definitional</div>'),
 # 3 — the trigger
 sc(2,"03",'<div class="rulebar"></div><div class="kicker">The trigger</div>'
   '<div class="lbl" id="c1" style="position:absolute;left:110px;top:560px">Auction of five-year notes</div>'
   f'<div class="big" id="c2" style="position:absolute;left:110px;top:612px;font-size:150px">${wheel("70")}bn</div>'
   +SVG('<line id="c3" x1="110" y1="880" x2="970" y2="880" stroke="#D42A2A" stroke-width="5"/>')+
   '<div class="big red" id="c4" style="position:absolute;left:110px;top:930px;font-size:120px">WEAK<br>DEMAND</div>'
   '<div class="lbl" id="c5" style="position:absolute;left:110px;top:1260px;width:880px">Buyers step back →<br>the government pays up</div>'
   '<div class="stamp">Auction detail per press reports · 2026-09-24</div>'),
 # 4 — risk-free competition
 sc(3,"04",'<div class="rulebar"></div><div class="kicker">Why your portfolio felt it</div>'
   +SVG('<line x1="540" y1="620" x2="540" y2="1240" stroke="#242427" stroke-width="3"/>')+
   '<div class="rowName" id="d1" style="left:110px;top:640px">TREASURY</div>'
   '<div class="rowVal red" id="d2" style="left:110px;top:700px">5%</div>'
   '<div class="lbl" id="d3" style="position:absolute;left:110px;top:800px;width:380px">about as close to<br>risk-free as it gets</div>'
   '<div class="rowName" id="d4" style="left:620px;top:640px">STOCKS</div>'
   '<div class="rowVal" id="d5" style="left:620px;top:700px">MUST BEAT IT</div>'
   '<div class="lbl" id="d6" style="position:absolute;left:620px;top:800px;width:360px">same money,<br>more risk</div>'
   '<div class="big" id="d7" style="position:absolute;left:110px;top:1320px;font-size:62px;width:880px">They compete for<br>the same dollar.</div>'
   '<div class="stamp">Valuation mechanics, not a forecast</div>'),
 # 5 — duration
 sc(4,"05",'<div class="rulebar"></div><div class="kicker">Who it hurts first</div>'
   '<div class="big" id="e1" style="position:absolute;left:110px;top:560px;font-size:76px;width:880px">Profits furthest<br>in the future</div>'
   +SVG('<line id="e2" x1="110" y1="810" x2="970" y2="810" stroke="#242427" stroke-width="3"/>')+
   '<div class="rowName" id="e3" style="left:110px;top:870px">DATA CENTRES</div>'
   '<div class="rowName" id="e4" style="left:110px;top:950px">CHIPS</div>'
   '<div class="rowName" id="e5" style="left:110px;top:1030px">POWER</div>'
   '<div class="big red" id="e6" style="position:absolute;left:110px;top:1160px;font-size:66px;width:880px">All built with<br>borrowed money.</div>'
   '<div class="tag" id="e7" style="position:absolute;left:110px;top:1360px;font-size:32px">A higher rate discounts them harder</div>'
   '<div class="stamp">Duration logic · mechanism, not a recommendation</div>'),
 # 6 — the mortgage
 sc(5,"06",'<div class="rulebar"></div><div class="kicker">It is not only markets</div>'
   '<div class="lbl" id="f1" style="position:absolute;left:110px;top:540px">30-year fixed mortgage</div>'
   f'<div class="big red" id="f2" style="position:absolute;left:110px;top:590px;font-size:170px">{wheel("7.03")}%</div>'
   +SVG('<line x1="110" y1="1150" x2="970" y2="1150" stroke="#242427" stroke-width="3"/>'
        f'<polyline id="f3" points="{MPOLY}" fill="none" stroke="#D42A2A" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/>'
        f'<circle id="f4" cx="{MXY[-1][0]}" cy="{MXY[-1][1]}" r="13" fill="#D42A2A"/>')+
   '<div class="thLabel" id="f5" style="left:110px;top:1170px">Sep 3 · 6.71%</div>'
   '<div class="thLabel" id="f6" style="left:760px;top:1170px;color:#F5F5F3">Sep 24 · 7.03%</div>'
   '<div class="big" id="f7" style="position:absolute;left:110px;top:1270px;font-size:58px;width:880px">Above 7% for the first<br>time in about 20 months.</div>'
   '<div class="stamp">Freddie Mac PMMS weekly survey · 2026-09-24</div>'),
 # 7 — the correction
 sc(6,"07",'<div class="rulebar"></div><div class="kicker">One correction</div>'
   '<div class="lbl" id="n1" style="position:absolute;left:110px;top:540px">The clip going around says</div>'
   '<div class="big" id="n2" style="position:absolute;left:110px;top:592px;font-size:72px;width:880px">"the same thing happened<br>in August 2024"</div>'
   +SVG('<line x1="110" y1="820" x2="970" y2="820" stroke="#D42A2A" stroke-width="5"/>'
        '<path id="n3" d="M 190 900 L 880 1120" stroke="#D42A2A" stroke-width="10" fill="none" stroke-linecap="round"/>'
        '<circle id="n4" cx="190" cy="900" r="13" fill="#F5F5F3"/><circle id="n5" cx="880" cy="1120" r="13" fill="#D42A2A"/>')+
   '<div class="big red" id="n6" style="position:absolute;left:110px;top:860px;font-size:92px">IT FELL</div>'
   '<div class="thLabel" id="n7" style="left:190px;top:1170px">24 Jul 2024 · 4.28%</div>'
   '<div class="thLabel" id="n8" style="left:660px;top:1170px;color:#F5F5F3">5 Aug 2024 · 3.73%</div>'
   '<div class="big" id="n9" style="position:absolute;left:110px;top:1270px;font-size:58px;width:880px">Last real 5% print:<br><span class="red">October 2023.</span></div>'
   '<div class="stamp">Yield path Jul–Aug 2024 · press convergence</div>'),
 # 8 — the close
 sc(7,"08",'<div class="rulebar"></div><div class="kicker">What to actually watch</div>'
   '<div class="big" id="i1" style="position:absolute;left:110px;top:560px;font-size:120px">THE<br>10-YEAR</div>'
   +SVG('<line id="i2" x1="110" y1="880" x2="970" y2="880" stroke="#D42A2A" stroke-width="5"/>')+
   '<div class="lbl" id="i3" style="position:absolute;left:110px;top:940px">It quietly sets</div>'
   '<div class="rowName" id="i4" style="left:110px;top:1010px">YOUR MORTGAGE</div>'
   '<div class="rowName" id="i5" style="left:110px;top:1090px">CORPORATE DEBT</div>'
   '<div class="rowName red" id="i6" style="left:110px;top:1170px">THE PRICE OF GROWTH</div>'
   '<div class="big" id="i7" style="position:absolute;left:110px;top:1300px;font-size:58px;width:880px">Watch the rate,<br>not the reaction.</div>'
   '<div class="stamp">Educational only · not investment advice</div>'),
]
DC=f'<div id="s9" class="clip" data-start="{cuts[NP]}" data-duration="{DISC}" data-track-index="0"><div id="discCard">'\
   '<div class="dbar" id="dbar"></div><div class="dl1" id="dl1">Educational only.<br>Not financial advice.</div>'\
   '<div class="dl2" id="dl2">Market commentary, not a recommendation to buy or sell any security.<br>'\
   'Figures as of the dates shown. Sources in the description.</div></div></div>'

groups=[];cur=[]
for w in W:
    cur.append(w)
    if len(cur)>=5 or w["w"][-1] in ".!?": groups.append(cur);cur=[]
if cur: groups.append(cur)
CAPS=[];CAPTW=[]
for gi,g in enumerate(groups):
    CAPS.append('<div class="capline" id="cg%d">%s</div>'%(gi,"".join(f'<span id="cw{gi}_{wi}">{w["w"]}</span>' for wi,w in enumerate(g))))
    nx=groups[gi+1][0]["s"]-0.05 if gi+1<len(groups) else None
    hide=g[-1]["e"]+0.3 if nx is None else min(g[-1]["e"]+0.3,nx-0.012)
    CAPTW.append(f'tl.to("#cg{gi}",{{autoAlpha:1,duration:.01}},{max(0,g[0]["s"]-0.05):.3f})'
                 f'.to("#cg{gi}",{{autoAlpha:0,duration:.01}},{hide:.3f});')
    for wi,w in enumerate(g):
        CAPTW.append(f'tl.to("#cw{gi}_{wi}",{{color:"#F5F5F3",duration:.01}},{w["s"]:.3f})'
                     f'.to("#cw{gi}_{wi}",{{color:"rgba(245,245,243,.46)",duration:.01}},{w["e"]:.3f});')

WHEEL_SCENES={0,2,5}
TW=[]
for i in range(NP):
    b=B[i]
    TW.append(f'bar("#s{i+1} .rulebar",{b+0.05:.3f},.5); up("#s{i+1} .kicker",{b+0.15:.3f});')
    TW.append(f'tl.fromTo("#s{i+1} .stamp",{{opacity:0}},{{opacity:1,duration:.4}},{b+2.2:.3f});')
    if i in WHEEL_SCENES:
        TW.append(f'tl.fromTo("#s{i+1} .hf-number-wheel-strip",{{y:0}},'
                  f'{{y:(_,s)=>s.style.getPropertyValue("--hf-number-target-y"),'
                  f'duration:1.15,ease:"power3.out",stagger:.055,immediateRender:false}},{b+0.65:.3f});')
ids=[["a1","a2","a4","a5","a6"],["b1","b3","b4","b5"],["c1","c2","c4","c5"],
     ["d1","d2","d3","d4","d5","d6","d7"],["e1","e3","e4","e5","e6","e7"],
     ["f1","f2","f7"],["n1","n2","n6","n9"],["i1","i3","i4","i5","i6","i7"]]
for i,grp in enumerate(ids):
    for j,el in enumerate(grp): TW.append(f'up("#{el}",{B[i]+0.45+j*0.75:.3f},.55,30);')
TW.append(f'tl.fromTo("#compliance",{{opacity:0}},{{opacity:1,duration:.35}},{B[0]+0.3:.3f})'
          f'.to("#compliance",{{opacity:0,duration:.3}},{B[0]+4.4:.3f});')
# scene 6 mortgage line draw
TW.append(f'tl.set("#f3",{{strokeDasharray:1000,strokeDashoffset:1000}},{B[5]:.3f})'
          f'.to("#f3",{{strokeDashoffset:0,duration:1.5,ease:"power2.inOut"}},{B[5]+0.9:.3f});')
TW.append(f'tl.fromTo("#f4",{{scale:0,transformOrigin:"center"}},{{scale:1,duration:.35,ease:"back.out(2.5)"}},{B[5]+2.4:.3f});')
TW.append(f'up("#f5",{B[5]+2.0:.3f});up("#f6",{B[5]+2.6:.3f});')
# scene 7 correction line draw (downward)
TW.append(f'tl.set("#n3",{{strokeDasharray:760,strokeDashoffset:760}},{B[6]:.3f})'
          f'.to("#n3",{{strokeDashoffset:0,duration:1.2,ease:"power2.inOut"}},{B[6]+1.4:.3f});')
TW.append(f'tl.fromTo("#n4",{{scale:0,transformOrigin:"center"}},{{scale:1,duration:.3,ease:"back.out(2)"}},{B[6]+1.4:.3f});')
TW.append(f'tl.fromTo("#n5",{{scale:0,transformOrigin:"center"}},{{scale:1,duration:.35,ease:"back.out(2.5)"}},{B[6]+2.5:.3f});')
TW.append(f'up("#n7",{B[6]+2.2:.3f});up("#n8",{B[6]+2.8:.3f});')
D=TOTAL-DISC
TW.append(f'tl.fromTo("#dbar",{{scaleX:0,transformOrigin:"left"}},{{scaleX:1,duration:.5,ease:E}},{D+0.2:.3f});')
TW.append(f'tl.fromTo("#dl1",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.6,ease:E}},{D+0.4:.3f});')
TW.append(f'tl.fromTo("#dl2",{{opacity:0}},{{opacity:1,duration:.6}},{D+1.0:.3f});')

HTML=open("tpl.tplsrc").read()
HTML=(HTML.replace("__TOTAL__",str(TOTAL)).replace("__ADUR__",str(ADUR))
      .replace("/*WHEELCSS*/",WHEEL_CSS).replace("/*WHEELJS*/",WHEEL_JS)
      .replace("/*SCENES*/","\n".join(SCENES)+"\n"+DC)
      .replace("/*CAPS*/","\n".join(CAPS)).replace("/*TW*/","\n".join(TW)+"\n"+"\n".join(CAPTW))
      .replace("{{","{").replace("}}","}"))
open("index.html","w").write(HTML)
print(f"total {TOTAL}s  audio {ADUR}s")
print("scene starts: "+", ".join(f"{b:.1f}" for b in B))
print(f"caption groups {len(groups)}")
