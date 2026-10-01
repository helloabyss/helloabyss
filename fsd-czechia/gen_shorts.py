import os,re,json,subprocess,numpy as np,soundfile as sf
from kokoro_onnx import Kokoro
K=Kokoro("/root/.cache/hyperframes/tts/models/kokoro-v1.0.onnx","/root/.cache/hyperframes/tts/voices/voices-v1.0.bin")
SR=24000; VOICE="am_michael"; GAP=0.16

SHORTS=[
 ("01-seventh-country","CZECHIA CLEARS TESLA FSD",
  "Czechia is now the seventh EU country to approve Tesla FSD Supervised. The ministry recognised the Dutch approval on the twenty-first of September. Rollout begins soon.",
  [("Prague · 21 September 2026","7TH","EU COUNTRY"),("Recognised","DUTCH RDW","approval of 10 April 2026"),("Tesla says","ROLLOUT","begins soon")]),
 ("02-the-seven","SEVEN COUNTRIES",
  "Netherlands. Lithuania. Estonia. Denmark. Belgium. Slovenia. And now Czechia. Tesla FSD Supervised keeps expanding, one national recognition at a time.",
  [("One at a time","SEVEN","national recognitions"),("Approved","NL · LT · EE","DK · BE · SI · CZ"),("Not bloc-wide","ONE BY ONE","each state decides")]),
 ("03-october-vote","THE OCTOBER 6 VOTE",
  "Seven countries. Roughly eleven point eight percent of the EU population. The committee vote still needs fifteen states and sixty five percent. Two weeks to go.",
  [("Covered today","11.8%","of EU population"),("Threshold","15 STATES","and 65% of population"),("Expected","6 OCTOBER","committee vote")]),
 ("04-still-supervised","STILL SUPERVISED",
  "FSD Supervised is Level Two. The driver must stay attentive and remains legally responsible. The Czech approval does not change that.",
  [("What it is","LEVEL 2","driver assistance"),("The driver","STAYS LIABLE","and must supervise"),("Approval changes","NOTHING","about that")]),
 ("05-safety-first","CZECHIA ASKED FIRST",
  "Czechia raised safety questions before approving. Traffic lights, speed limits, and whether the driver is really watching. It cleared the system only after more European data.",
  [("Before approving","QUESTIONS","were raised"),("On","LIGHTS · LIMITS","and driver attention"),("Cleared after","MORE DATA","and monitoring")]),
]

def synth(text):
    s=[x.strip() for x in re.findall(r'[^.!?]+[.!?]',text) if x.strip()]
    au=[];t=0.0;words=[]
    for i,sent in enumerate(s):
        sm,_=K.create(sent,voice=VOICE,speed=1.0,lang="en-us"); d=len(sm)/SR
        ws=sent.split(); tot=sum(len(w)+1 for w in ws); acc=0
        for w in ws:
            w0=t+(acc/tot)*d; acc+=len(w)+1; words.append({"w":w,"s":round(w0,3),"e":round(t+(acc/tot)*d,3)})
        au.append(sm); t+=d
        if i<len(s)-1: au.append(np.zeros(int(GAP*SR),dtype=sm.dtype)); t+=GAP
    return np.concatenate(au),t,words

TPL='''<!doctype html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=1080,height=1920"><script src="vendor/gsap.min.js"></script><style>
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#0B1A2E}}
#root{{width:100%;height:100%;position:relative;background:#0B1A2E;font-family:"Liberation Sans",Arial,sans-serif;-webkit-font-smoothing:antialiased}}
.clip{{position:absolute;inset:0}}
.kick{{position:absolute;left:100px;top:300px;color:#8FA6C0;font-size:30px;letter-spacing:.3em;text-transform:uppercase;font-weight:700}}
.hero{{position:absolute;left:100px;top:internalHERO px;color:#FFFFFF;font-weight:800;letter-spacing:-.03em;line-height:.95}}
.sub{{position:absolute;left:100px;top:internalSUB px;color:#C9D6E6;font-size:44px;font-weight:600;letter-spacing:-.01em;width:880px;line-height:1.25}}
.rule{{position:absolute;left:100px;top:370px;width:150px;height:5px;background:#FFFFFF;transform-origin:left center}}
.slug{{position:absolute;right:100px;top:200px;color:#8299B4;font-size:22px;letter-spacing:.22em}}
.capline{{position:absolute;left:90px;top:1500px;width:900px;text-align:center;font-size:42px;font-weight:800;
  opacity:0;line-height:1.24;text-shadow:0 2px 12px rgba(0,0,0,.9)}}
.capline span{{color:rgba(255,255,255,.5);margin:0 .15em}}
#disc{{position:absolute;left:100px;top:1716px;color:#8FA6C0;font-size:27px;font-weight:700;letter-spacing:.02em;line-height:1.4}}
#prog{{position:absolute;left:0;bottom:0;height:4px;width:100%;background:#FFFFFF;transform-origin:left;transform:scaleX(0)}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{CARDS}
<div id="caps">{CAPS}</div>
<div id="disc">Not financial advice.<br>FSD Supervised is supervised.</div>
<div id="prog"></div>
<audio id="vo" src="vo.wav" data-start="0" data-duration="{ADUR}" data-track-index="9" data-volume="1"></audio>
</div><script>
const tl=gsap.timeline({{paused:true}}),E="power3.out";
const up=(s,at,d=.55,y=36)=>tl.fromTo(s,{{opacity:0,y}},{{opacity:1,y:0,duration:d,ease:E}},at);
tl.fromTo("#prog",{{scaleX:0}},{{scaleX:1,duration:{TOTAL},ease:"none"}},0);
{TW}
{CAPTW}
window.__timelines["main"]=tl;tl.seek(0);</script></body></html>'''

for slug,title,vo,cards in SHORTS:
    d=slug; os.makedirs(d,exist_ok=True)
    if not os.path.exists(f"{d}/package.json"):
        subprocess.run(["npx","--yes","hyperframes@0.8.55","init",d,"--non-interactive","--example=blank","--skill=motion-graphics"],
                       check=True,capture_output=True)
    os.makedirs(f"{d}/vendor",exist_ok=True)
    subprocess.run(["cp","../videos/twim-2026-09-20/vendor/gsap.min.js",f"{d}/vendor/gsap.min.js"],check=True)
    au,adur,words=synth(vo); sf.write(f"{d}/vo.wav",au,SR)
    TOTAL=round(adur+1.6,3); n=len(cards); seg=adur/n
    CARDS=[];TW=[]
    for i,(k,h,s) in enumerate(cards):
        st=round(i*seg,3); du=round(seg if i<n-1 else TOTAL-st,3)
        hs=150 if len(h)<=9 else (108 if len(h)<=14 else 86)
        CARDS.append(f'<div id="c{i}" class="clip" data-start="{st}" data-duration="{du}" data-track-index="0">'
          f'<div class="slug">{title}</div><div class="rule" id="r{i}"></div>'
          f'<div class="kick" id="k{i}">{k}</div>'
          f'<div class="hero" id="h{i}" style="top:470px;font-size:{hs}px">{h}</div>'
          f'<div class="sub" id="s{i}" style="top:{470+int(hs*1.25)+40}px">{s}</div></div>')
        TW += [f'tl.fromTo("#r{i}",{{scaleX:0}},{{scaleX:1,duration:.5,ease:E}},{st+.05});',
               f'up("#k{i}",{st+.15});', f'up("#h{i}",{st+.35},.6,46);', f'up("#s{i}",{st+.75});']
    # captions: <=4 words, never crossing a sentence end
    groups=[];cur=[]
    for w in words:
        cur.append(w)
        if len(cur)>=4 or w["w"][-1] in ".!?": groups.append(cur);cur=[]
    if cur: groups.append(cur)
    CAPS=[];CAPTW=[]
    for gi,g in enumerate(groups):
        CAPS.append('<div class="capline" id="g%d">%s</div>'%(gi,"".join(f'<span id="w{gi}_{wi}">{w["w"]}</span>' for wi,w in enumerate(g))))
        nxt=groups[gi+1][0]["s"]-0.05 if gi+1<len(groups) else None
        hide=g[-1]["e"]+0.3 if nxt is None else min(g[-1]["e"]+0.3,nxt-0.012)
        CAPTW.append(f'tl.set("#g{gi}",{{opacity:1}},{max(0,g[0]["s"]-0.05):.3f}).set("#g{gi}",{{opacity:0}},{hide:.3f});')
        for wi,w in enumerate(g):
            CAPTW.append(f'tl.set("#w{gi}_{wi}",{{color:"#FFFFFF"}},{w["s"]:.3f}).set("#w{gi}_{wi}",{{color:"rgba(255,255,255,.5)"}},{w["e"]:.3f});')
    html=(TPL.replace("{TOTAL}",str(TOTAL)).replace("{ADUR}",str(round(adur,3)))
          .replace("{CARDS}","\n".join(CARDS)).replace("{CAPS}","\n".join(CAPS))
          .replace("{TW}","\n".join(TW)).replace("{CAPTW}","\n".join(CAPTW))
          .replace("internalHERO ","470").replace("internalSUB ","700")
          .replace("{{","{").replace("}}","}"))
    open(f"{d}/index.html","w").write(html)
    print(f"{d}: {TOTAL}s ({adur:.1f}s VO, {len(groups)} caption groups)")
