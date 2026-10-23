import re

# ---------------------------------------------------------------- beat grid
# Silent piece: nothing to sync to but rhythm, so every beat is placed by hand
# on a 0.5s grid. B(n) converts beats to seconds.
B = 0.5
def b(n): return round(n*B, 3)

SC = [  # (id, kicker, slugnum, start, end)
 ("h","The week that was","01",  0.0,  6.5),
 ("t","The tape",         "02",  6.5, 15.0),
 ("y","Meanwhile",        "03", 15.0, 22.5),
 ("x","The part that doesn't fit","04", 22.5, 29.5),
 ("r","What actually changed","05", 29.5, 37.5),
 ("c","The week ahead",   "06", 37.5, 50.5),
 ("p","How to be ready",  "07", 50.5, 60.0),
 ("z","",                 "08", 60.0, 65.0),
]
DISC_AT, DISC_DUR = 65.0, 4.5
TOTAL = round(DISC_AT + DISC_DUR, 3)
S = {s[0]: (s[3], round(s[4]-s[3],3)) for s in SC}
K = {s[0]: s[3] for s in SC}

nw = open("compositions/components/number-wheel.html").read()
WHEEL_CSS = re.search(r'<style[^>]*>(.*?)</style>', nw, re.S).group(1)
WHEEL_JS  = re.search(r'<script>(.*?)</script>', nw, re.S).group(1)

def wheel(v): return f'<span class="hf-number-wheel" data-value="{v}"></span>'
def words(text, wid):
    """Split into per-word spans so a line can be staggered word by word."""
    return "".join(f'<span class="word" id="{wid}{i}">{w}</span>&nbsp;'
                   for i, w in enumerate(text.split()))

def scene(sid, kicker, num, inner, stamp):
    st, du = S[sid]
    kick = f'<div class="kicker" id="{sid}K">{kicker}</div>' if kicker else ""
    return (f'<div id="s_{sid}" class="clip" data-start="{st}" data-duration="{du}" data-track-index="0">'
      f'<div class="frame"><div class="fr-t"></div><div class="fr-b"></div>'
      f'<div class="slug">THE METICULOUS INVESTOR</div><div class="num">{num}</div></div>'
      f'<div class="rule" id="{sid}R"></div>{kick}{inner}'
      f'<div class="stamp" id="{sid}S">{stamp}</div></div>')

# ---------------------------------------------------------------- scenes
SCENES = []

# 01 — hook. The whole piece earns its watch time here or not at all.
SCENES.append(scene("h","The week that was","01",
  f'<div class="mega" id="hL1" style="top:520px;font-size:140px">{words("THE MARKET","hA")}</div>'
  f'<div class="mega" id="hL2" style="top:668px;font-size:140px">{words("WENT UP.","hB")}</div>'
  '<div class="mega red" id="hL3" style="top:912px;font-size:104px">ALMOST NOTHING</div>'
  '<div class="mega" id="hL4" style="top:1030px;font-size:104px">IN IT DID.</div>'
  '<div class="lbl" id="hL5" style="left:96px;top:1220px">Week of 22–25 September 2026</div>'
  '<div id="compliance">Educational only. Not financial advice.</div>',
  "Index and sector moves as reported for the week ending 2026-09-25"))

# 02 — the tape. A bar race is the fastest way to show dispersion.
bars = [("NASDAQ","+2.1%",0.840,"acc"),("S&P 500","+1.2%",0.480,""),("DOW","+0.3%",0.120,"")]
brows = ""
for i,(nm,val,sx,cls) in enumerate(bars):
    top = 660 + i*168
    brows += (f'<div class="barRow" id="tR{i}" style="top:{top}px">'
      f'<div class="barName">{nm}</div>'
      f'<div class="barTrack"></div>'
      f'<div class="barFill {cls}" id="tF{i}"></div>'
      f'<div class="barVal" id="tV{i}" style="left:812px">{val}</div></div>')
SCENES.append(scene("t","The tape","02",
  f'<div class="big" id="tT1" style="top:400px;font-size:66px;width:888px">{words("Every index rose.","tA")}</div>'
  f'<div class="big red" id="tT2" style="top:478px;font-size:66px;width:888px">{words("Not evenly.","tB")}</div>'
  + brows +
  '<div class="big" id="tP" style="top:1240px;font-size:62px;width:888px">The Nasdaq did <span class="red">seven times</span><br>the Dow\'s week.</div>'
  '<div class="lbl" id="tN" style="left:96px;top:1420px">Dow snapped a three-week losing streak</div>',
  "Weekly index moves to 2026-09-25 · press convergence"))

# 03 — the number the week actually turned on
SCENES.append(scene("y","Meanwhile","03",
  '<div class="lbl" id="yL" style="left:96px;top:560px">US 10-year Treasury yield</div>'
  f'<div class="mega red" id="yN" style="top:614px;font-size:210px">{wheel("5.18")}%</div>'
  '<div class="big" id="yH" style="top:940px;font-size:96px">HIGHEST<br>SINCE 2007</div>'
  '<div class="lbl" id="yS" style="left:96px;top:1220px">A cycle high, set mid-week</div>'
  '<div class="big dim" id="yQ" style="top:1300px;font-size:48px;width:888px">Longer-dated yields are at levels<br>most investors have never traded.</div>',
  "10-year Treasury, week's high 2026-09-24 · press convergence"))

# 04 — name the contradiction plainly; it is the thesis of the piece
SCENES.append(scene("x","The part that doesn't fit","04",
  f'<div class="big" id="xL1" style="top:540px;font-size:72px;width:888px">{words("A higher risk-free rate","xA")}</div>'
  f'<div class="big" id="xL2" style="top:630px;font-size:72px;width:888px">{words("should compress multiples.","xB")}</div>'
  '<div class="rule" id="xRule" style="top:790px;width:888px;height:5px"></div>'
  '<div class="mega red" id="xL3" style="top:860px;font-size:120px">THIS WEEK<br>IT DIDN\'T.</div>'
  '<div class="big dim" id="xL4" style="top:1180px;font-size:50px;width:888px">Stocks rose <span class="red">into</span> the rate,<br>not away from it.</div>',
  "Valuation mechanics · mechanism, not a forecast"))

# 05 — the repricing, shown as two numbers rather than described
SCENES.append(scene("r","What actually changed","05",
  f'<div class="big" id="rT" style="top:470px;font-size:70px;width:888px">{words("The market stopped","rA")}</div>'
  f'<div class="big red" id="rT2" style="top:556px;font-size:70px;width:888px">{words("pricing cuts.","rB")}</div>'
  '<div class="lbl" id="rL" style="left:96px;top:740px">Odds of an October hike</div>'
  '<div class="lbl" id="rO1" style="left:96px;top:830px">One week ago</div>'
  f'<div class="big dim" id="rN1" style="top:876px;font-size:136px">{wheel("42")}%</div>'
  '<div class="lbl" id="rO2" style="left:560px;top:830px">Friday</div>'
  f'<div class="big red" id="rN2" style="top:876px;left:560px;font-size:136px">{wheel("58")}%</div>'
  '<div class="rule" id="rRule" style="top:1090px;width:888px;height:5px"></div>'
  '<div class="big" id="rW" style="top:1150px;font-size:52px;width:888px">Hot activity data. Rising<br>inflation expectations.</div>'
  '<div class="lbl" id="rD" style="left:96px;top:1330px">Market pricing — not a forecast</div>',
  "CME FedWatch, 2026-09-25 vs one week earlier"))

# 06 — the calendar is the payload: what the viewer actually takes into Monday
cal = [("TUE","JOLTS","Job openings · est 7.23m"),
       ("WED","CORE PCE","The Fed's preferred gauge · prev 3.3% y/y"),
       ("WED PM","MICRON","The AI-capex read"),
       ("THU","ISM MFG","Prev 54.6"),
       ("FRI","PAYROLLS","Est +100k · unemployment 4.2%")]
crows = ""
for i,(d,w,n) in enumerate(cal):
    crows += (f'<div class="calRow" id="cR{i}" style="top:{612+i*126}px">'
      f'<div class="calDay">{d}</div><div class="calWhat">{w}</div>'
      f'<div class="calNote">{n}</div></div>')
SCENES.append(scene("c","The week ahead","06",
  '<div class="mega" id="cT" style="top:392px;font-size:88px">FIVE PRINTS.<br>ONE WEEK.</div>'
  + crows +
  '<div class="big dim" id="cF" style="top:1286px;font-size:44px;width:888px">Quarter-end Wednesday. Thin books<br>make every surprise bigger.</div>',
  "Consensus estimates per published previews · estimates, not forecasts"))

# 07 — the plan. Scenarios, never instructions.
ifs = [("IF CORE PCE RUNS HOT","the hike case hardens"),
       ("IF MICRON GUIDES SOFT","the AI-capex trade loses its anchor"),
       ("IF PAYROLLS COME IN WEAK","the growth leg is the one that cracks")]
irows = ""
for i,(c,t) in enumerate(ifs):
    irows += (f'<div class="ifRow" id="pR{i}" style="top:{700+i*180}px">'
      f'<div class="ifCond">{c}</div><div class="ifThen">→ {t}</div></div>')
SCENES.append(scene("p","How to be ready","07",
  f'<div class="big" id="pT1" style="top:450px;font-size:60px;width:888px">{words("Decide what each one means","pA")}</div>'
  f'<div class="big red" id="pT2" style="top:532px;font-size:60px;width:888px">{words("before it prints.","pB")}</div>'
  + irows +
  '<div class="rule" id="pRule" style="top:1300px;width:888px;height:5px"></div>'
  '<div class="mega" id="pC" style="top:1360px;font-size:64px">WRITE THEM DOWN<br>BEFORE MONDAY.</div>',
  "Scenarios, not predictions · educational only"))

# 08 — close
SCENES.append(scene("z","","08",
  '<div class="mega" id="zL1" style="top:700px;font-size:168px">PREPARED</div>'
  '<div class="mega dim" id="zL2" style="top:868px;font-size:168px">BEATS</div>'
  '<div class="mega red" id="zL3" style="top:1036px;font-size:168px">REACTIVE.</div>'
  '<div class="lbl" id="zL4" style="left:96px;top:1290px">The Meticulous Investor · weekly</div>',
  "Figures as of 2026-09-25 · sources in the description"))

DISC = (f'<div id="s_d" class="clip" data-start="{DISC_AT}" data-duration="{DISC_DUR}" data-track-index="0">'
  '<div id="discCard"><div class="dbar" id="dBar"></div>'
  '<div class="dl1" id="dL1">Educational only.<br>Not financial advice.</div>'
  '<div class="dl2" id="dL2">Market commentary, not a recommendation to buy or sell any security.<br>'
  'Estimates are consensus figures, not predictions. Figures as of the dates shown.</div>'
  '<div class="dl3" id="dL3">THE METICULOUS INVESTOR</div></div></div>')

# ---------------------------------------------------------------- choreography
TW = []
for sid,_,_,st,_ in SC:
    TW.append(f'tl.fromTo("#{sid}R",{{scaleX:0}},{{scaleX:1,duration:.45,ease:"power3.inOut"}},{st+0.10:.3f});')
    TW.append(f'tl.fromTo("#{sid}K",{{opacity:0,x:-22}},{{opacity:1,x:0,duration:.4,ease:EO}},{st+0.22:.3f});')
    TW.append(f'tl.fromTo("#{sid}S",{{opacity:0}},{{opacity:1,duration:.4}},{st+1.30:.3f});')

h=K["h"]
TW += [f'wordsIn("#hL1 .word",{h+b(1.4):.3f},.06);',
       f'wordsIn("#hL2 .word",{h+b(2.6):.3f},.06);',
       f'slam("#hL3",{h+b(5.0):.3f},.40);',
       f'slam("#hL4",{h+b(6.2):.3f},.40);',
       f'rise("#hL5",{h+b(8.0):.3f});',
       f'tl.fromTo("#compliance",{{opacity:0}},{{opacity:1,duration:.35}},{h+0.55:.3f})'
       f'.to("#compliance",{{opacity:0,duration:.3}},{h+4.60:.3f});']

t=K["t"]
TW += [f'wordsIn("#tT1 .word",{t+b(0.8):.3f},.05);',
       f'wordsIn("#tT2 .word",{t+b(1.8):.3f},.05);']
for i,(_,_,sx,_) in enumerate(bars):
    at=t+b(3.0+i*1.1)
    TW += [f'rise("#tR{i} .barName",{at:.3f},.34,20);',
           f'tl.fromTo("#tR{i} .barTrack",{{opacity:0}},{{opacity:1,duration:.3}},{at:.3f});',
           # immediateRender:false so the seek-based renderer cannot pre-apply the end state
           f'tl.fromTo("#tF{i}",{{scaleX:0}},{{scaleX:{sx},duration:.80,ease:"power3.inOut",immediateRender:false}},{at+0.18:.3f});',
           f'tl.fromTo("#tV{i}",{{opacity:0,x:-26}},{{opacity:1,x:0,duration:.42,ease:EO}},{at+0.70:.3f});']
TW += [f'slam("#tP",{t+b(11.0):.3f},.46);', f'rise("#tN",{t+b(13.0):.3f});']

y=K["y"]
TW += [f'rise("#yL",{y+b(0.8):.3f},.4,24);',
       f'tl.fromTo("#yN",{{opacity:0,scale:1.18,transformOrigin:"left center"}},'
       f'{{opacity:1,scale:1,duration:.5,ease:E}},{y+b(1.4):.3f});',
       f'tl.fromTo("#yN .hf-number-wheel-strip",{{y:0}},'
       f'{{y:(_,s)=>s.style.getPropertyValue("--hf-number-target-y"),'
       f'duration:1.25,ease:"power3.out",stagger:.06,immediateRender:false}},{y+b(1.7):.3f});',
       f'slam("#yH",{y+b(5.4):.3f},.46);',
       f'rise("#yS",{y+b(7.6):.3f});',
       f'rise("#yQ",{y+b(9.2):.3f});']

x=K["x"]
TW += [f'wordsIn("#xL1 .word",{x+b(0.8):.3f},.05);',
       f'wordsIn("#xL2 .word",{x+b(1.7):.3f},.05);',
       f'tl.fromTo("#xRule",{{scaleX:0}},{{scaleX:1,duration:.5,ease:"power3.inOut",immediateRender:false}},{x+b(3.4):.3f});',
       f'slam("#xL3",{x+b(4.2):.3f},.48);',
       f'rise("#xL4",{x+b(7.4):.3f});']

r=K["r"]
TW += [f'wordsIn("#rT .word",{r+b(0.8):.3f},.05);',
       f'wordsIn("#rT2 .word",{r+b(1.7):.3f},.05);',
       f'rise("#rL",{r+b(3.2):.3f},.4,22);',
       f'rise("#rO1",{r+b(4.0):.3f},.36,18);',
       f'tl.fromTo("#rN1",{{opacity:0,y:28}},{{opacity:1,y:0,duration:.44,ease:E}},{r+b(4.3):.3f});',
       f'rise("#rO2",{r+b(5.6):.3f},.36,18);',
       f'tl.fromTo("#rN2",{{opacity:0,y:28}},{{opacity:1,y:0,duration:.44,ease:E}},{r+b(5.9):.3f});',
       f'tl.fromTo("#rN1 .hf-number-wheel-strip, #rN2 .hf-number-wheel-strip",{{y:0}},'
       f'{{y:(_,s)=>s.style.getPropertyValue("--hf-number-target-y"),'
       f'duration:1.1,ease:"power3.out",stagger:.05,immediateRender:false}},{r+b(4.6):.3f});',
       f'tl.fromTo("#rRule",{{scaleX:0}},{{scaleX:1,duration:.5,ease:"power3.inOut",immediateRender:false}},{r+b(8.0):.3f});',
       f'rise("#rW",{r+b(8.6):.3f});',
       f'rise("#rD",{r+b(11.4):.3f});']

c=K["c"]
TW += [f'slam("#cT",{c+b(0.8):.3f},.48);']
for i in range(len(cal)):
    at=c+b(3.0+i*1.5)
    TW += [f'tl.fromTo("#cR{i}",{{opacity:0,x:-34}},{{opacity:1,x:0,duration:.44,ease:E}},{at:.3f});',
           f'tl.fromTo("#cR{i} .calDay",{{opacity:0}},{{opacity:1,duration:.3}},{at+0.10:.3f});']
TW += [f'rise("#cF",{c+b(12.4):.3f});']

p=K["p"]
TW += [f'wordsIn("#pT1 .word",{p+b(0.8):.3f},.05);',
       f'wordsIn("#pT2 .word",{p+b(1.7):.3f},.05);']
for i in range(len(ifs)):
    at=p+b(3.4+i*1.6)
    TW += [f'tl.fromTo("#pR{i} .ifCond",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.42,ease:E}},{at:.3f});',
           f'tl.fromTo("#pR{i} .ifThen",{{opacity:0,x:30}},{{opacity:1,x:0,duration:.42,ease:E}},{at+0.22:.3f});']
TW += [f'tl.fromTo("#pRule",{{scaleX:0}},{{scaleX:1,duration:.5,ease:"power3.inOut",immediateRender:false}},{p+b(14.0):.3f});',
       f'slam("#pC",{p+b(14.6):.3f},.46);']

z=K["z"]
TW += [f'slam("#zL1",{z+b(0.6):.3f},.42);',
       f'slam("#zL2",{z+b(1.5):.3f},.42);',
       f'slam("#zL3",{z+b(2.4):.3f},.42);',
       f'rise("#zL4",{z+b(4.6):.3f});']

d=DISC_AT
TW += [f'tl.fromTo("#dBar",{{scaleX:0,transformOrigin:"left"}},{{scaleX:1,duration:.5,ease:EO}},{d+0.2:.3f});',
       f'tl.fromTo("#dL1",{{opacity:0,y:28}},{{opacity:1,y:0,duration:.55,ease:EO}},{d+0.4:.3f});',
       f'tl.fromTo("#dL2",{{opacity:0}},{{opacity:1,duration:.55}},{d+1.0:.3f});',
       f'tl.fromTo("#dL3",{{opacity:0}},{{opacity:1,duration:.55}},{d+1.7:.3f});']

HTML = open("tpl.tplsrc").read()
HTML = (HTML.replace("__TOTAL__", str(TOTAL))
        .replace("/*WHEELCSS*/", WHEEL_CSS).replace("/*WHEELJS*/", WHEEL_JS)
        .replace("/*SCENES*/", "\n".join(SCENES) + "\n" + DISC)
        .replace("/*TW*/", "\n".join(TW))
        .replace("{{","{").replace("}}","}"))
open("index.html","w").write(HTML)
print(f"total {TOTAL}s · {len(SC)} scenes + disclaimer · {len(TW)} tweens")
for sid,_,num,st,en in SC: print(f"  {num} {sid:2s} {st:5.1f} → {en:5.1f}")
