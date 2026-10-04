import re,json,numpy as np,soundfile as sf
from kokoro_onnx import Kokoro
K=Kokoro("/root/.cache/hyperframes/tts/models/kokoro-v1.0.onnx","/root/.cache/hyperframes/tts/voices/voices-v1.0.bin")
SR=24000;VOICE="am_michael";GS=0.10;GP=0.55

# pull the registry number-wheel snippet in verbatim
nw=open("compositions/components/number-wheel.html").read()
WHEEL_CSS=re.search(r'<style[^>]*>(.*?)</style>',nw,re.S).group(1)
WHEEL_JS=re.search(r'<script>(.*?)</script>',nw,re.S).group(1)

paras=[p.strip() for p in open("vo.txt").read().split("\n\n") if p.strip()]
assert len(paras)==9,len(paras)
audio=[];t=0.0;SC=[];W=[]
for pi,p in enumerate(paras):
    flat=" ".join(p.split());s0=t
    for si,s in enumerate([x.strip() for x in re.findall(r'[^.!?]+[.!?]',flat) if x.strip()]):
        sm,_=K.create(s,voice=VOICE,speed=1.0,lang="en-us");d=len(sm)/SR
        ws=s.split();tot=sum(len(w)+1 for w in ws);acc=0
        for w in ws:
            a0=t+(acc/tot)*d;acc+=len(w)+1;W.append({"w":w,"s":round(a0,3),"e":round(t+(acc/tot)*d,3)})
        audio.append(sm);t+=d;audio.append(np.zeros(int(GS*SR),dtype=sm.dtype));t+=GS
    SC.append({"i":pi,"start":round(s0,3),"end":round(t-GS,3)})
    if pi<8: audio.append(np.zeros(int((GP-GS)*SR),dtype=sm.dtype));t+=GP-GS
full=np.concatenate(audio);ADUR=round(len(full)/SR,3);sf.write("vo.wav",full,SR)
cuts=[0.0]+[round((SC[i]["end"]+SC[i+1]["start"])/2,3) for i in range(8)]+[round(SC[-1]["end"]+0.3,3)]
B=[cuts[i] for i in range(9)];DISC=4.5;TOTAL=round(cuts[9]+DISC,3)
S=[(B[i],round(cuts[i+1]-B[i],3)) for i in range(9)]

def wheel(v,cls=""): return f'<span class="hf-number-wheel {cls}" data-value="{v}"></span>'
def sc(i,num,inner):
    st,du=S[i]
    return (f'<div id="s{i+1}" class="clip" data-start="{st}" data-duration="{du}" data-track-index="0">'
      f'<div class="frame"><div class="fr-t"></div><div class="fr-b"></div>'
      f'<div class="slug">$MSTR · BITCOIN MATH</div><div class="num">{num}</div>'
      f'<div class="tick tl"></div><div class="tick tr"></div></div>{inner}</div>')

SCENES=[
 sc(0,"01",'<div class="rulebar" id="r1"></div><div class="kicker" id="k1">The divergence</div>'
   '<div class="lbl" id="a1" style="position:absolute;left:110px;top:560px">Bitcoin</div>'
   '<div class="big" id="a2" style="position:absolute;left:110px;top:606px;font-size:130px">HIGHEST<br>SINCE JAN</div>'
   '<svg width="1080" height="1920" style="position:absolute;inset:0"><line id="a3" x1="110" y1="960" x2="970" y2="960" stroke="#242427" stroke-width="3"/></svg>'
   '<div class="lbl" id="a4" style="position:absolute;left:110px;top:1010px">Strategy stock · 12 months</div>'
   '<div class="big red" id="a5" style="position:absolute;left:110px;top:1056px;font-size:150px">−79%</div>'
   '<div class="stamp">Prices as of 2026-09-21</div>'
   '<div id="compliance">Educational only. Not financial advice.</div>'),
 sc(1,"02",'<div class="rulebar"></div><div class="kicker">What it owns</div>'
   '<div class="lbl" id="b1" style="position:absolute;left:110px;top:560px">Bitcoin held</div>'
   f'<div class="big" id="b2" style="position:absolute;left:110px;top:612px;font-size:132px">{wheel("845,256")}</div>'
   '<svg width="1080" height="1920" style="position:absolute;inset:0"><line id="b3" x1="110" y1="860" x2="970" y2="860" stroke="#242427" stroke-width="3"/></svg>'
   '<div class="lbl" id="b4" style="position:absolute;left:110px;top:910px">Average cost per coin</div>'
   '<div class="big" id="b5" style="position:absolute;left:110px;top:956px;font-size:108px">$75,400</div>'
   '<div class="lbl" id="b6" style="position:absolute;left:110px;top:1150px">Bitcoin this week</div>'
   f'<div class="big" id="b7" style="position:absolute;left:110px;top:1196px;font-size:108px">${wheel("86,000")}</div>'
   '<div class="tag" id="b8" style="position:absolute;left:110px;top:1350px">Coins above cost</div>'
   '<div class="stamp">Holdings per bitcointreasuries · price 2026-09-21</div>'),
 sc(2,"03",'<div class="rulebar"></div><div class="kicker">But the stock</div>'
   '<div class="big red" id="c1" style="position:absolute;left:110px;top:600px;font-size:190px">−38%</div>'
   '<div class="lbl" id="c2" style="position:absolute;left:110px;top:840px">Year to date</div>'
   '<svg width="1080" height="1920" style="position:absolute;inset:0"><line id="c3" x1="110" y1="960" x2="970" y2="960" stroke="#D42A2A" stroke-width="5"/></svg>'
   '<div class="big" id="c4" style="position:absolute;left:110px;top:1010px;font-size:76px;width:880px">The coins are up.<br>The equity is not.</div>'
   '<div class="stamp">As of 2026-09-21</div>'),
 sc(3,"04",'<div class="rulebar"></div><div class="kicker">The number that matters</div>'
   '<div class="lbl" id="d1" style="position:absolute;left:110px;top:600px">Market value</div>'
   '<div class="big" id="d2" style="position:absolute;left:110px;top:660px;font-size:96px">÷ BITCOIN HELD</div>'
   '<svg width="1080" height="1920" style="position:absolute;inset:0"><line id="d3" x1="110" y1="820" x2="970" y2="820" stroke="#242427" stroke-width="3"/></svg>'
   '<div class="big red" id="d4" style="position:absolute;left:110px;top:870px;font-size:180px">mNAV</div>'
   '<div class="lbl" id="d5" style="position:absolute;left:110px;top:1100px;width:880px">What the market pays<br>for each coin it owns</div>'
   '<div class="stamp">Definition per public mNAV trackers</div>'),
 sc(4,"05",'<div class="rulebar"></div><div class="kicker">The collapse</div>'
   '<svg width="1080" height="1920" style="position:absolute;inset:0">'
   '<line x1="110" y1="1180" x2="970" y2="1180" stroke="#6E6E6E" stroke-width="3" stroke-dasharray="10 10"/>'
   '<polyline id="e1" points="150,700 400,830 650,1090 900,1210" fill="none" stroke="#D42A2A" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/>'
   '<circle id="e2" cx="150" cy="700" r="13" fill="#F5F5F3"/><circle id="e3" cx="900" cy="1210" r="13" fill="#D42A2A"/></svg>'
   '<div class="thLabel" id="e4" style="left:110px;top:640px">2024 · 3.4×</div>'
   '<div class="thLabel" id="e5" style="left:700px;top:1238px;color:#F5F5F3">now · 1.16×</div>'
   '<div class="thLabel" id="e6" style="left:110px;top:1200px">1.0× — parity with the coins</div>'
   '<div class="big" id="e7" style="position:absolute;left:110px;top:1296px;font-size:56px;width:880px">Fully diluted, some trackers<br>put it <span class="red">under one</span>.</div>'
   '<div class="stamp">Multiples per public mNAV trackers · 2026-09-21</div>'),
 sc(5,"06",'<div class="rulebar"></div><div class="kicker">Why the premium was the engine</div>'
   '<div class="lbl" id="f1" style="position:absolute;left:110px;top:580px">Above 1.0×</div>'
   '<div class="big" id="f2" style="position:absolute;left:110px;top:626px;font-size:82px;width:880px">Issue shares → buy coins →<br>bitcoin per share rises</div>'
   '<svg width="1080" height="1920" style="position:absolute;inset:0"><line id="f3" x1="110" y1="900" x2="970" y2="900" stroke="#242427" stroke-width="3"/></svg>'
   '<div class="lbl" id="f4" style="position:absolute;left:110px;top:950px;color:#D42A2A">Below 1.0×</div>'
   '<div class="big red" id="f5" style="position:absolute;left:110px;top:996px;font-size:82px;width:880px">The same move<br>works in reverse</div>'
   '<div class="tag" id="f6" style="position:absolute;left:110px;top:1260px;font-size:34px">The flywheel ran on the premium</div>'
   '<div class="stamp">Mechanism, not a forecast</div>'),
 sc(6,"07",'<div class="rulebar"></div><div class="kicker">So it started selling</div>'
   '<div class="lbl" id="n1" style="position:absolute;left:110px;top:580px">Reported in a July filing</div>'
   f'<div class="big red" id="n2" style="position:absolute;left:110px;top:632px;font-size:150px">{wheel("3,588")}</div>'
   '<div class="lbl" id="n3" style="position:absolute;left:110px;top:840px">coins sold · about $216 million</div>'
   '<svg width="1080" height="1920" style="position:absolute;inset:0"><line id="n4" x1="110" y1="960" x2="970" y2="960" stroke="#242427" stroke-width="3"/></svg>'
   '<div class="lbl" id="n5" style="position:absolute;left:110px;top:1010px">Across 2026</div>'
   '<div class="big" id="n6" style="position:absolute;left:110px;top:1056px;font-size:104px">~6,900 coins</div>'
   '<div class="tag" id="n7" style="position:absolute;left:110px;top:1240px;font-size:32px">Most of it below average cost</div>'
   '<div class="stamp">Per company 8-K, 2026-07-06</div>'),
 sc(7,"08",'<div class="rulebar"></div><div class="kicker">The part people miss</div>'
   '<svg width="1080" height="1920" style="position:absolute;inset:0">'
   '<line x1="110" y1="1040" x2="970" y2="1040" stroke="#242427" stroke-width="3"/>'
   '<path id="h1" d="M 180 1040 L 430 720" stroke="#F5F5F3" stroke-width="10" fill="none" stroke-linecap="round"/>'
   '<path id="h2" d="M 640 1120 L 900 1120" stroke="#D42A2A" stroke-width="10" fill="none" stroke-linecap="round"/></svg>'
   '<div class="rowName" id="h3" style="left:180px;top:620px">BITCOIN</div>'
   '<div class="rowVal" id="h4" style="left:180px;top:666px">RALLIED</div>'
   '<div class="rowName" id="h5" style="left:640px;top:1180px">THE PREMIUM</div>'
   '<div class="rowVal red" id="h6" style="left:640px;top:1226px">DID NOT</div>'
   '<div class="stamp">Weekly move to 2026-09-21</div>'),
 sc(8,"09",'<div class="rulebar"></div><div class="kicker">What to actually watch</div>'
   '<div class="big" id="i1" style="position:absolute;left:110px;top:600px;font-size:92px">BITCOIN<br>PER SHARE</div>'
   '<div class="lbl" id="i2" style="position:absolute;left:110px;top:840px">what they own</div>'
   '<svg width="1080" height="1920" style="position:absolute;inset:0"><line id="i3" x1="110" y1="940" x2="970" y2="940" stroke="#D42A2A" stroke-width="5"/></svg>'
   '<div class="big red" id="i4" style="position:absolute;left:110px;top:990px;font-size:92px">THE<br>MULTIPLE</div>'
   '<div class="lbl" id="i5" style="position:absolute;left:110px;top:1230px">what you pay for it</div>'
   '<div class="stamp">Educational only · not investment advice</div>'),
]
DC=f'<div id="s10" class="clip" data-start="{cuts[9]}" data-duration="{DISC}" data-track-index="0"><div id="discCard">'\
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
    CAPS.append('<div class="capline" id="g%d">%s</div>'%(gi,"".join(f'<span id="w{gi}_{wi}">{w["w"]}</span>' for wi,w in enumerate(g))))
    nx=groups[gi+1][0]["s"]-0.05 if gi+1<len(groups) else None
    hide=g[-1]["e"]+0.3 if nx is None else min(g[-1]["e"]+0.3,nx-0.012)
    # tl.set() is a zero-duration tween: GSAP renders those immediately and they do not
    # re-evaluate reliably under the renderer's per-frame seek, which left several caption
    # lines stacked on screen at once. Tiny-duration .to() tweens are seek-safe.
    CAPTW.append(f'tl.to("#g{gi}",{{autoAlpha:1,duration:.01}},{max(0,g[0]["s"]-0.05):.3f})'
                 f'.to("#g{gi}",{{autoAlpha:0,duration:.01}},{hide:.3f});')
    for wi,w in enumerate(g):
        CAPTW.append(f'tl.to("#w{gi}_{wi}",{{color:"#F5F5F3",duration:.01}},{w["s"]:.3f})'
                     f'.to("#w{gi}_{wi}",{{color:"rgba(245,245,243,.46)",duration:.01}},{w["e"]:.3f});')

TW=[]
for i in range(9):
    b=B[i]
    TW.append(f'bar("#s{i+1} .rulebar",{b+0.05:.3f},.5); up("#s{i+1} .kicker",{b+0.15:.3f});')
    TW.append(f'tl.fromTo("#s{i+1} .stamp",{{opacity:0}},{{opacity:1,duration:.4}},{b+2.2:.3f});')
    if i in (1,6):   # only scenes that actually contain wheels
        # fromTo, not to: the strip carries a CSS transform and GSAP must own the full state
        TW.append(f'tl.fromTo("#s{i+1} .hf-number-wheel-strip",{{y:0}},'
                  f'{{y:(_,s)=>s.style.getPropertyValue("--hf-number-target-y"),'
                  f'duration:1.15,ease:"power3.out",stagger:.055,immediateRender:false}},{b+0.65:.3f});')
ids=[["a1","a2","a4","a5"],["b1","b2","b4","b5","b6","b7","b8"],["c1","c2","c4"],["d1","d2","d4","d5"],
     ["e4","e7"],["f1","f2","f4","f5","f6"],["n1","n2","n3","n5","n6","n7"],["h3","h4","h5","h6"],["i1","i2","i4","i5"]]
for i,grp in enumerate(ids):
    for j,el in enumerate(grp): TW.append(f'up("#{el}",{B[i]+0.45+j*0.75:.3f},.55,30);')
TW.append(f'tl.fromTo("#compliance",{{opacity:0}},{{opacity:1,duration:.35}},{B[0]+0.3:.3f}).to("#compliance",{{opacity:0,duration:.3}},{B[0]+4.4:.3f});')
# scene 5 line draw + scene 8 paths
TW.append(f'tl.set("#e1",{{strokeDasharray:1000,strokeDashoffset:1000}},{B[4]:.3f}).to("#e1",{{strokeDashoffset:0,duration:1.6,ease:"power2.inOut"}},{B[4]+0.7:.3f});')
TW.append(f'tl.fromTo("#e2",{{scale:0,transformOrigin:"center"}},{{scale:1,duration:.3,ease:"back.out(2)"}},{B[4]+0.7:.3f});')
TW.append(f'tl.fromTo("#e3",{{scale:0,transformOrigin:"center"}},{{scale:1,duration:.35,ease:"back.out(2.5)"}},{B[4]+2.3:.3f});')
TW.append(f'up("#e5",{B[4]+2.5:.3f});up("#e6",{B[4]+3.1:.3f});')
for pid,at in [("h1",B[7]+0.8),("h2",B[7]+2.4)]:
    TW.append(f'tl.set("#{pid}",{{strokeDasharray:420,strokeDashoffset:420}},{at:.3f}).to("#{pid}",{{strokeDashoffset:0,duration:.85,ease:"power2.out"}},{at+0.1:.3f});')
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
print(f"total {TOTAL}s  audio {ADUR}s  scenes at "+", ".join(f"{b:.1f}" for b in B))
print(f"caption groups {len(groups)}")
