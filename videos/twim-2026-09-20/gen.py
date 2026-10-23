import json
T=json.load(open("vo_timing.json")); SC=T["scenes"]; W=T["words"]
# visual cut points = midpoint of each inter-beat silence
cuts=[0.0]
for i in range(len(SC)-1): cuts.append(round((SC[i]["end"]+SC[i+1]["start"])/2,3))
cuts.append(round(SC[-1]["end"]+0.30,3))
DISC=4.5; TOTAL=round(cuts[-1]+DISC,3)
S=[(round(cuts[i],3), round(cuts[i+1]-cuts[i],3)) for i in range(9)]
A=[(s["start"],s["end"]) for s in SC]          # audio windows per beat

# ---- caption groups: <=5 words, never crossing a sentence end ----
groups=[];cur=[]
for w in W:
    cur.append(w)
    if len(cur)>=5 or w["w"][-1] in ".!?":
        groups.append(cur); cur=[]
if cur: groups.append(cur)

capHTML=[];capTW=[]
for gi,g in enumerate(groups):
    spans="".join(f'<span id="w{gi}_{wi}">{w["w"]}</span>' for wi,w in enumerate(g))
    capHTML.append(f'<div class="capline" id="g{gi}">{spans}</div>')
    g0,g1=g[0]["s"],g[-1]["e"]
    show=max(0.0,g0-0.05)
    # never let two caption lines be on screen at once
    nxt=groups[gi+1][0]["s"]-0.05 if gi+1<len(groups) else None
    hide=g1+0.28 if nxt is None else min(g1+0.28,nxt-0.012)
    capTW.append(f'  tl.set("#g{gi}",{{opacity:1}},{show:.3f}).set("#g{gi}",{{opacity:0}},{hide:.3f});')
    for wi,w in enumerate(g):
        capTW.append(f'  tl.set("#w{gi}_{wi}",{{color:"#F5F5F3"}},{w["s"]:.3f}).set("#w{gi}_{wi}",{{color:"rgba(245,245,243,.42)"}},{w["e"]:.3f});')

def base(i): return S[i][0]
CAPS="\n".join(capHTML); CAPTW="\n".join(capTW)

# ---------------- scene bodies ----------------
def sc(i,inner,num):
    st,du=S[i]
    return f'''      <div id="s{i+1}" class="clip" data-start="{st}" data-duration="{du}" data-track-index="0">
        <div class="frame"><div class="fr-t"></div><div class="fr-b"></div>
          <div class="slug">TWIM · 20 SEP 2026</div><div class="num">{num}</div>
          <div class="tick tl"></div><div class="tick tr"></div></div>
{inner}
      </div>'''

s1=sc(0,'''        <div class="rulebar" id="s1bar"></div>
        <div class="kicker" id="s1k">This Week in the Market</div>
        <div class="lbl" id="s1lbl" style="position:absolute;left:110px;top:560px">US 10-Year Treasury Yield</div>
        <svg width="1080" height="1920" style="position:absolute;inset:0">
          <line id="s1th" x1="110" y1="1120" x2="970" y2="1120" stroke="#6E6E6E" stroke-width="3" stroke-dasharray="10 10"/>
          <line id="s1drop" x1="820" y1="996" x2="820" y2="1120" stroke="#D42A2A" stroke-width="3"/>
          <circle id="s1dot" cx="820" cy="980" r="16" fill="#D42A2A"/>
        </svg>
        <div class="thLabel" id="s1thl" style="left:110px;top:1140px">5.00% threshold</div>
        <div class="sweepwrap" style="left:110px;top:680px"><div class="big" id="s1num" style="font-size:190px">0.000%</div><div class="sweep" id="s1sw"></div></div>
        <div class="tag" id="s1tag" style="position:absolute;left:110px;top:965px">Above five percent</div>
        <div class="stamp" id="s1st">US 10-year Treasury · close 2026-09-18</div>
        <div id="compliance">Educational only. Not financial advice.</div>''','01')

s2=sc(1,'''        <div class="rulebar"></div>
        <div class="kicker">The week · three ways</div>
        <svg width="1080" height="1920" style="position:absolute;inset:0">
          <line x1="540" y1="620" x2="540" y2="1320" stroke="#242427" stroke-width="3"/>
        </svg>
        <div class="rowName" id="n1" style="left:110px;top:660px">DOW</div>
        <div class="bar neg" id="b1" style="left:170px;top:726px;width:370px"></div>
        <div class="rowVal red" id="v1" style="left:110px;top:770px">−733 PTS</div>
        <div class="tag" id="t1" style="position:absolute;left:110px;top:845px;font-size:26px">Worst week since March</div>
        <div class="rowName" id="n2" style="left:110px;top:960px">NASDAQ</div>
        <div class="bar pos" id="b2" style="left:540px;top:1026px;width:390px"></div>
        <div class="rowVal" id="v2" style="left:560px;top:1070px">+2.6%</div>
        <div class="rowName" id="n3" style="left:110px;top:1200px">S&amp;P 500</div>
        <div class="bar pos" id="b3" style="left:540px;top:1266px;width:130px"></div>
        <div class="rowVal" id="v3" style="left:560px;top:1310px">+0.7%</div>
        <div class="stamp">Weekly change · 14–18 Sep 2026</div>''','02')

s3=sc(2,'''        <div class="rulebar"></div>
        <div class="kicker">Friday's close</div>
        <div class="tileL" id="c1l" style="left:110px;top:640px">S&amp;P 500</div>
        <div class="tileV" id="c1v" style="left:110px;top:686px">0.00</div>
        <div class="tileL" id="c2l" style="left:110px;top:960px">Nasdaq Composite</div>
        <div class="tileV" id="c2v" style="left:110px;top:1006px">0.00</div>
        <div class="tileL" id="c3l" style="left:110px;top:1280px">Dow Jones Industrial Average</div>
        <div class="tileV" id="c3v" style="left:110px;top:1326px">0.00</div>
        <div class="stamp">Closing levels · 2026-09-18</div>''','03')

s4=sc(3,'''        <div class="rulebar"></div>
        <div class="kicker">Wednesday 16 September</div>
        <div class="big" id="s4bp" style="position:absolute;left:110px;top:560px;font-size:250px">+25</div>
        <div class="lbl" id="s4bpl" style="position:absolute;left:118px;top:872px">basis points</div>
        <svg width="1080" height="1920" style="position:absolute;inset:0">
          <line x1="110" y1="1120" x2="970" y2="1120" stroke="#242427" stroke-width="3"/>
          <rect id="s4old" x="110" y="1090" width="430" height="60" fill="#242427"/>
          <rect id="s4new" x="540" y="1090" width="430" height="60" fill="#D42A2A"/>
        </svg>
        <div class="thLabel" id="s4o" style="left:110px;top:1170px">from 3.50–3.75%</div>
        <div class="thLabel" id="s4n" style="left:540px;top:1170px;color:#F5F5F3">to 3.75–4.00%</div>
        <div class="tag" id="s4tag" style="position:absolute;left:110px;top:1300px;font-size:34px">First increase since 2023</div>
        <div class="stamp">FOMC decision · 2026-09-16</div>''','04')

s5=sc(4,'''        <div class="rulebar"></div>
        <div class="kicker">The vote</div>
        <div class="sweepwrap" style="left:110px;top:540px"><div class="big" id="s5v" style="font-size:255px">12–0</div><div class="sweep" id="s5sw"></div></div>
        <div class="lbl" id="s5u" style="position:absolute;left:110px;top:930px;color:#F5F5F3">Unanimous · not one dissent</div>
        <svg width="1080" height="1920" style="position:absolute;inset:0">
          <line id="s5rule" x1="110" y1="1040" x2="970" y2="1040" stroke="#242427" stroke-width="3"/>
        </svg>
        <div class="lbl" id="s5n" style="position:absolute;left:110px;top:1090px">Kevin Warsh · Chair, Federal Reserve</div>
        <div id="s5q" style="position:absolute;left:110px;top:1180px;width:860px;color:#D42A2A;font-size:54px;font-weight:800;letter-spacing:-.02em;line-height:1.22">“A timelier return to two percent.”</div>
        <div class="stamp">FOMC · 2026-09-16</div>''','05')

s6=sc(5,'''        <div class="rulebar"></div>
        <div class="kicker">The complication</div>
        <div class="lbl" id="s6l" style="position:absolute;left:110px;top:560px">US consumer prices · year on year</div>
        <svg width="1080" height="1920" style="position:absolute;inset:0">
          <line x1="110" y1="900" x2="970" y2="900" stroke="#242427" stroke-width="2" stroke-dasharray="8 8"/>
          <line id="s6line" x1="240" y1="900" x2="840" y2="900" stroke="#F5F5F3" stroke-width="8" stroke-linecap="round"/>
          <circle id="s6d1" cx="240" cy="900" r="14" fill="#F5F5F3"/>
          <circle id="s6d2" cx="840" cy="900" r="14" fill="#F5F5F3"/>
        </svg>
        <div class="thLabel" id="s6a" style="left:190px;top:940px">JUL · 3.4%</div>
        <div class="thLabel" id="s6b" style="left:780px;top:940px">AUG · 3.4%</div>
        <div class="thLabel" id="s6c" style="left:110px;top:820px;color:#6E6E6E">Consensus 3.4% — in line</div>
        <div class="big red" id="s6slam" style="position:absolute;left:110px;top:1120px;font-size:92px;line-height:1.1;width:880px">They hiked<br/>anyway.</div>
        <div class="stamp">CPI, August 2026 · released 2026-09-11</div>''','06')

s7=sc(6,'''        <div class="rulebar"></div>
        <div class="kicker">One week · two directions</div>
        <svg width="1080" height="1920" style="position:absolute;inset:0">
          <line x1="110" y1="1080" x2="970" y2="1080" stroke="#242427" stroke-width="3"/>
          <path id="s7up" d="M 200 1080 L 430 760" stroke="#F5F5F3" stroke-width="10" fill="none" stroke-linecap="round"/>
          <path id="s7dn" d="M 650 1080 L 880 1300" stroke="#D42A2A" stroke-width="10" fill="none" stroke-linecap="round"/>
        </svg>
        <div class="rowName" id="s7ul" style="left:200px;top:660px">NASDAQ</div>
        <div class="rowVal" id="s7uv" style="left:200px;top:706px">+2.6%</div>
        <div class="rowName" id="s7dl" style="left:650px;top:1322px">DOW</div>
        <div class="rowVal red" id="s7dv" style="left:650px;top:1368px">−733 PTS</div>
        <div class="tag" id="s7c" style="position:absolute;left:110px;top:1104px;font-size:26px;color:#6E6E6E">Same week</div>
        <div class="stamp">Weekly change · 14–18 Sep 2026</div>''','07')

s8=sc(7,'''        <div class="rulebar"></div>
        <div class="kicker">The week ahead</div>
        <div class="big" id="s8d" style="position:absolute;left:110px;top:600px;font-size:200px">SEP 30</div>
        <svg width="1080" height="1920" style="position:absolute;inset:0">
          <line id="s8r" x1="110" y1="900" x2="970" y2="900" stroke="#D42A2A" stroke-width="5"/>
        </svg>
        <div class="rowName" id="s8n" style="left:110px;top:950px;font-size:60px">MICRON · FISCAL Q4</div>
        <div class="lbl" id="s8s" style="position:absolute;left:110px;top:1060px">Memory pricing · AI capital spending</div>
        <div class="stamp">Date per company IR</div>''','08')

s9=sc(8,'''        <div class="rulebar"></div>
        <div class="kicker">The number to watch</div>
        <svg width="1080" height="1920" style="position:absolute;inset:0">
          <line x1="110" y1="1120" x2="970" y2="1120" stroke="#6E6E6E" stroke-width="3" stroke-dasharray="10 10"/>
          <line id="s9drop" x1="820" y1="996" x2="820" y2="1120" stroke="#D42A2A" stroke-width="3"/>
          <circle id="s9dot" cx="820" cy="980" r="16" fill="#D42A2A"/>
        </svg>
        <div class="thLabel" style="left:110px;top:1140px">5.00% threshold</div>
        <div class="big" id="s9num" style="position:absolute;left:110px;top:680px;font-size:190px">5.006%</div>
        <div class="big red" id="s9slam" style="position:absolute;left:110px;top:1260px;font-size:78px;width:880px">The hurdle moved.</div>
        <div class="stamp">US 10-year Treasury · close 2026-09-18</div>''','09')

s10=f'''      <div id="s10" class="clip" data-start="{cuts[-1]}" data-duration="{DISC}" data-track-index="0">
        <div id="discCard"><div class="dbar" id="dbar"></div>
          <div class="dl1" id="dl1">Educational only.<br/>Not financial advice.</div>
          <div class="dl2" id="dl2">Market commentary, not a recommendation to buy or sell any security.<br/>Figures as of the dates shown. Sources in the description.</div>
        </div>
      </div>'''

TPL=open("tpl.tplsrc").read()
out=(TPL.replace("/*SCENES*/", "\n".join([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10]))
        .replace("/*CAPS*/", CAPS).replace("/*CAPTW*/", CAPTW)
        .replace("__TOTAL__", str(TOTAL)).replace("__AUDIODUR__", str(T["total"])))
for i,(st,du) in enumerate(S): out=out.replace(f"__B{i+1}__", f"{st:.3f}")
open("index.html","w").write(out)
print(f"scenes: "+", ".join(f"{i+1}@{s:.2f}" for i,(s,d) in enumerate(S)))
print(f"caption groups: {len(groups)}  total {TOTAL}s  audio {T['total']}s")
