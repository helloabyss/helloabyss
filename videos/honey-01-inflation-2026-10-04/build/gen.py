import os, re, subprocess
# "Inflation Explained with Honey" — pilot of the Explained-with-Honey series (The Meticulous Investor).
# Hand-built vector animation (SVG + GSAP), no AI imagery. Narration: ElevenLabs "Brian" (assets/vo.mp3).
# Every cue is pinned to a spoken sentence: segments come from the pauses in the narration
# (silencedetect -38 dB / 0.18 s) and were mapped to the script's 26 sentences by hand.
# Figures: ../SCRIPT.md fact table (US CPI +3.4%, 12 months to Aug 2026, BLS).

GOLD, INK, PAPER, RED, MUTED = "#F2B705", "#0B0B0C", "#F5F5F3", "#D42A2A", "#8A8A8A"

_o = subprocess.run(["ffmpeg", "-hide_banner", "-i", "assets/vo.mp3", "-af", "silencedetect=n=-38dB:d=0.18",
                     "-f", "null", "-"], capture_output=True, text=True).stderr
_gs = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", _o)]
_ge = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", _o)]
GAPS = list(zip(_gs, _ge))[:-1]           # internal pauses; the last silence is the file's tail
SPEECH_END = _gs[-1]
assert len(GAPS) == 27, f"expected 27 pauses, got {len(GAPS)}: re-map sentences before rendering"
SEG = [(0.0, GAPS[0][0])] + [(GAPS[i][1], GAPS[i+1][0]) for i in range(len(GAPS)-1)] + [(GAPS[-1][1], SPEECH_END)]
def S(k): return round(SEG[k-1][0], 3)                 # start of speech segment k (1-based)
def mid(g): return round((GAPS[g-1][0] + GAPS[g-1][1]) / 2, 3)

LINES = [l.strip() for l in open("../../../scripts/2026-10-04-honey-inflation-vo.txt") if l.strip()]
LINE_END_GAP = [1, 4, 5, 6, 8, 10, 12, 14, 18, 22, 24, 26]   # pause that closes each of lines 1-12
EDGE = [0.0] + [mid(g) for g in LINE_END_GAP] + [round(SPEECH_END + 0.35, 3)]
HL = ["honey.", "hundred", "one", "more", "Twice", "richer,", "price", "demand-pull", "sixty", "cost-push.",
      "stings.", "three", "faster"]
VO_END = EDGE[-1]; DISC = 4.5; TOTAL = round(VO_END + DISC, 3)
def L(i): return EDGE[i-1], round(EDGE[i]-EDGE[i-1], 3)          # line i (1-based) start, duration

# ---------------------------------------------------------------- art (hand-built SVG)
def bee(w, cls=""):
    return (f'<svg class="bee {cls}" viewBox="0 0 130 100" width="{w}" height="{w*100//130}">'
            '<path d="M24 60 L8 64 L24 68 Z" fill="#0B0B0C"/>'
            '<ellipse cx="62" cy="62" rx="40" ry="29" fill="#F2B705"/>'
            '<g clip-path="url(#beeBody)"><rect x="46" y="30" width="10" height="64" fill="#0B0B0C"/>'
            '<rect x="66" y="30" width="10" height="64" fill="#0B0B0C"/></g>'
            '<circle cx="104" cy="58" r="19" fill="#3A2C14" stroke="#F2B705" stroke-width="3"/>'
            '<circle cx="110" cy="52" r="6" fill="#F5F5F3"/><circle cx="112" cy="52" r="2.8" fill="#0B0B0C"/>'
            '<path d="M106 40 Q110 22 122 18" stroke="#F2B705" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
            '<circle cx="122" cy="18" r="4" fill="#3A2C14" stroke="#F2B705" stroke-width="2"/>'
            '<g class="wing"><ellipse cx="54" cy="24" rx="19" ry="25" fill="#F5F5F3" fill-opacity=".85" stroke="#0B0B0C" stroke-width="2.5"/></g>'
            '<g class="wing"><ellipse cx="76" cy="22" rx="15" ry="21" fill="#F5F5F3" fill-opacity=".6" stroke="#0B0B0C" stroke-width="2.5"/></g></svg>')

def jar(w):
    return (f'<svg class="jar" viewBox="0 0 60 80" width="{w}" height="{w*80//60}">'
            '<rect x="13" y="2" width="34" height="10" rx="3" fill="#F5F5F3"/>'
            '<rect x="6" y="12" width="48" height="64" rx="11" fill="#F2B705"/>'
            '<rect x="12" y="20" width="8" height="40" rx="4" fill="#F5F5F3" opacity=".35"/>'
            '<rect x="16" y="38" width="30" height="16" rx="3" fill="#0B0B0C" opacity=".85"/></svg>')

def token(w):
    return (f'<svg class="tok" viewBox="0 0 60 60" width="{w}" height="{w}">'
            '<polygon points="30,3 54,16 54,44 30,57 6,44 6,16" fill="#F5F5F3"/>'
            '<polygon points="30,14 44,22 44,38 30,46 16,38 16,22" fill="none" stroke="#0B0B0C" stroke-width="3.5"/>'
            '<rect x="27" y="22" width="6" height="16" fill="#F2B705"/></svg>')

def flower(i):
    return (f'<svg class="flw" id="fl{i}" viewBox="0 0 80 160" width="120" height="240">'
            '<path class="stem" d="M40 158 Q38 110 40 70" stroke="#5E7A3A" stroke-width="6" fill="none"/>'
            '<g class="head"><circle cx="40" cy="44" r="14" fill="#F2B705"/>'
            + "".join(f'<circle cx="{40+26*c:.1f}" cy="{44+26*s:.1f}" r="15" fill="#F5F5F3"/>'
                      for c, s in [(1,0),(0.31,0.95),(-0.81,0.59),(-0.81,-0.59),(0.31,-0.95)]) +
            '<circle cx="40" cy="44" r="13" fill="#F2B705"/></g></svg>')

def caps():
    out = ""
    for i, line in enumerate(LINES, 1):
        st, du = L(i)
        ws = "".join(f'<span class="cw{" hl" if w == HL[i-1] else ""}">{w}</span> ' for w in line.split())
        out += (f'<div class="clip cap" id="cap{i}" data-start="{st}" data-duration="{du}" data-track-index="2">'
                f'<div class="capIn">{ws}</div></div>')
    return out

def scene(i, inner, stamp=""):
    st, du = L(i)
    stp = f'<div class="stamp">{stamp}</div>' if stamp else ""
    return (f'<div id="s{i}" class="clip scene" data-start="{st}" data-duration="{du}" data-track-index="0">'
            f'<div class="slug">EXPLAINED WITH HONEY · No. 1</div>{inner}{stp}</div>')

SC = []
SC.append(scene(1,
    '<div class="mega gold" id="t1" style="top:470px;font-size:168px">'
    + "".join(f'<span class="ch">{c}</span>' for c in "INFLATION") + '</div>'
    '<div class="big" id="t1b" style="top:680px;font-size:64px">explained with <span class="gold">honey</span></div>'
    f'<div class="actor bob" id="b1" style="left:390px;top:900px">{bee(300)}</div>'
    '<div id="compliance">Educational only. Not financial advice.</div>'))
SC.append(scene(2,
    '<svg id="hive" class="abs" viewBox="0 0 300 300" style="left:390px;top:330px;width:300px;height:300px">'
    '<polygon id="hiveP" points="150,8 274,79 274,221 150,292 26,221 26,79" fill="none" stroke="#F2B705" stroke-width="10" stroke-linejoin="round"/>'
    '<text x="150" y="168" text-anchor="middle" font-size="44" font-weight="800" fill="#F5F5F3" font-family="Liberation Sans">HIVE</text></svg>'
    f'<div class="unit" id="u2a" style="left:140px;top:760px">{jar(170)}<div class="num gold">100</div><div class="lbl">JARS OF HONEY</div></div>'
    f'<div class="unit" id="u2b" style="left:600px;top:760px">{token(200)}<div class="num">100</div><div class="lbl">WAX TOKENS</div></div>'))
SC.append(scene(3,
    f'<div class="eq" id="eq3" style="top:560px">{token(190)}<span class="big" style="position:static;font-size:150px">1 = 1</span>{jar(150)}</div>'
    '<div class="big" id="t3" style="top:900px;font-size:66px">ONE TOKEN · ONE JAR</div>'
    f'<div class="actor bob" id="b3" style="left:-260px;top:1060px">{bee(220)}</div>'))
rain = "".join(f'<div class="rain" id="r4{i}" style="left:{120+(i*61)%800}px;top:-120px">{token(86)}</div>' for i in range(14))
SC.append(scene(4,
    '<div class="big gold" id="t4" style="top:340px;font-size:70px">THE HIVE COUNCIL</div>'
    '<div class="podium" id="pod"></div>'
    + "".join(f'<div class="actor bob" id="c4{i}" style="left:{180+i*250}px;top:470px">{bee(190)}</div>' for i in range(3))
    + rain +
    '<div class="flip" id="n4" style="top:1150px"><span id="n4a">100</span><span id="n4b" class="red">200</span></div>'
    '<div class="lbl c" id="l4" style="top:1330px">TOKENS IN THE HIVE</div>'))
SC.append(scene(5,
    f'<div class="unit" id="u5a" style="left:120px;top:520px">{jar(200)}<div class="num">100</div><div class="lbl">SAME HONEY</div></div>'
    f'<div class="unit" id="u5b" style="left:580px;top:500px">{token(240)}<div class="num red">200</div><div class="lbl">2× TOKENS</div></div>'))
SC.append(scene(6,
    '<div class="big" id="t6" style="top:360px;font-size:70px">EVERY BEE FEELS <span class="gold">RICHER</span></div>'
    + "".join(f'<div class="actor bob hop" id="h6{i}" style="left:{x}px;top:{y}px">{bee(170)}{token(64)}</div>'
              for i, (x, y) in enumerate([(90,560),(420,520),(740,580),(230,820),(620,860)]))
    + f'<div class="unit" id="u6" style="left:430px;top:1080px">{jar(150)}</div>'
    '<div class="big red" id="t6b" style="top:1290px;font-size:62px">↑ MORE DEMAND</div>'))
jars7 = "".join(f'<div class="j7" style="left:{110+(i%5)*176}px;top:{480+(i//5)*230}px">{jar(130)}</div>' for i in range(10))
SC.append(scene(7,
    '<div class="big" id="t7" style="top:340px;font-size:66px">STILL <span class="gold">100</span> JARS</div>' + jars7 +
    '<div class="tag" id="tag7"><span id="p7a">PRICE: 1 TOKEN</span><span id="p7b" class="red">PRICE: 2 TOKENS ↑</span></div>'))
chase = "".join(f'<div class="ch8" id="k8{i}" style="left:{-120-i*95}px;top:{960+(i%2)*70}px">{token(90)}</div>' for i in range(6))
SC.append(scene(8,
    '<div class="mega gold" id="t8" style="top:430px;font-size:140px">DEMAND-PULL</div>'
    '<div class="big" id="t8b" style="top:600px;font-size:72px">INFLATION</div>'
    f'<div class="actor" id="j8" style="left:640px;top:930px">{jar(140)}</div>' + chase +
    '<div class="lbl c" id="l8" style="top:1250px">TOO MANY TOKENS · SAME HONEY</div>'))
SC.append(scene(9,
    '<div class="mega" id="t9" style="top:360px;font-size:120px">NOW FLIP IT</div>'
    '<div id="sun9" class="sun"></div>'
    + "".join(f'<div class="fl" style="left:{90+i*190}px;top:820px">{flower(i)}</div>' for i in range(5)) +
    '<div class="flip" id="n9" style="top:1130px"><span id="n9a" class="gold">100</span><span id="n9b" class="red">60</span></div>'
    '<div class="lbl c" id="l9" style="top:1310px">JARS THIS SUMMER</div>'))
SC.append(scene(10,
    f'<div class="unit" id="u10a" style="left:120px;top:420px">{token(200)}<div class="num">200</div><div class="lbl">SAME TOKENS</div></div>'
    f'<div class="unit" id="u10b" style="left:600px;top:440px">{jar(170)}<div class="num red">60</div><div class="lbl">LESS HONEY</div></div>'
    '<div class="tag" id="tag10" style="top:1010px;left:140px;width:800px"><span class="red" style="font-size:54px;white-space:nowrap">PRICE CLIMBS AGAIN ↑</span></div>'
    '<div class="stampbig" id="st10">COST-PUSH</div>'))
bars = [10, 9.67, 9.35, 9.05, 8.75]
SC.append(scene(11,
    f'<div class="actor" id="b11" style="left:250px;top:330px">{bee(560)}</div>'
    '<div class="big" id="t11" style="top:330px;font-size:64px">WHAT 10 TOKENS BUY</div>'
    + "".join(f'<div class="bar" id="bar{i}" style="left:{140+i*170}px;height:{int(v*62)}px;top:{1290-int(v*62)}px">'
              f'<div class="bv">{v:g}</div><div class="bx">YEAR {i+1}</div></div>' for i, v in enumerate(bars)) +
    '<div class="lbl c" id="l11" style="top:1380px">JARS · ILLUSTRATION AT 3.4% A YEAR</div>'))
SC.append(scene(12,
    '<div class="big" id="t12" style="top:420px;font-size:72px">THE <span class="gold">HUMAN</span> HIVE</div>'
    '<div class="lbl c" id="l12" style="top:560px">U.S. CONSUMER PRICES · 12 MONTHS</div>'
    '<div class="mega red c" id="n12" style="top:700px;font-size:280px">+3.4%</div>',
    "CPI-U, 12 months to August 2026 · U.S. Bureau of Labor Statistics"))
SC.append(scene(13,
    '<svg id="ch13" class="abs" viewBox="0 0 880 520" style="left:100px;top:440px;width:880px;height:520px">'
    '<line x1="0" y1="518" x2="880" y2="518" stroke="rgba(245,245,243,.2)" stroke-width="3"/>'
    '<path id="lnP" d="M0,470 C200,430 420,330 620,210 S800,90 880,50" fill="none" stroke="#D42A2A" stroke-width="12" stroke-linecap="round"/>'
    '<path id="lnS" d="M0,470 C220,450 420,400 620,330 S800,250 880,200" fill="none" stroke="#F5F5F3" stroke-width="12" stroke-linecap="round" stroke-dasharray="1 0"/></svg>'
    '<div class="tagl red" id="lp" style="left:640px;top:410px">PRICE OF HONEY</div>'
    '<div class="tagl" id="ls" style="left:610px;top:830px">YOUR SAVINGS ?</div>'
    '<div class="big gold" id="t13" style="top:1080px;font-size:76px">GROWING FASTER?</div>'
    '<div class="lock" id="lock"><div class="mega gold" style="position:static;font-size:120px">INFLATION</div>'
    '<div class="big" style="position:static;font-size:56px;margin-top:40px">explained with honey</div></div>'))

DISC_HTML = (f'<div id="sd" class="clip" data-start="{VO_END}" data-duration="{DISC}" data-track-index="0">'
    '<div id="discCard"><div class="dbar" id="dBar"></div>'
    '<div class="dl1" id="dL1">Educational only.<br>Not financial advice.</div>'
    '<div class="dl2" id="dL2">Not a recommendation to buy or sell any security. Investing involves risk. '
    'Hive figures are illustrations; the 3.4% is U.S. CPI for the 12 months to August 2026 (BLS).</div>'
    '<div class="dl3" id="dL3">THE METICULOUS INVESTOR · EXPLAINED WITH HONEY</div></div></div>')

# ---------------------------------------------------------------- motion
T = []
def a(x): T.append(x)
R = int(TOTAL / 0.07)
a(f'tl.fromTo(".wing",{{scaleY:1}},{{scaleY:.55,duration:.07,repeat:{R},yoyo:true,ease:"none"}},0);')
a(f'tl.fromTo(".bob",{{y:0}},{{y:-16,duration:.55,repeat:{int(TOTAL/.55)},yoyo:true,ease:"sine.inOut"}},0);')
a(f'tl.fromTo("#bg",{{backgroundPosition:"0px 0px"}},{{backgroundPosition:"0px -240px",duration:{TOTAL},ease:"none"}},0);')
a(f'tl.fromTo("#prog",{{scaleX:0}},{{scaleX:1,duration:{TOTAL},ease:"none"}},0);')
for i in range(1, len(LINES)+1):
    a(f'tl.fromTo("#cap{i} .cw",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.2,ease:EO,stagger:.045}},{L(i)[0]+0.02:.3f});')
# 1
a(f'tl.fromTo("#t1 .ch",{{opacity:0,y:60,scale:1.4}},{{opacity:1,y:0,scale:1,duration:.32,ease:E,stagger:.05}},0.05);')
a('rise("#t1b",0.6);')
a('tl.fromTo("#b1",{x:-760,rotation:-12},{x:0,rotation:0,duration:1.1,ease:"power3.out"},0.15);')
a(f'tl.fromTo("#compliance",{{opacity:0}},{{opacity:1,duration:.3}},0.3).to("#compliance",{{opacity:0,duration:.3}},{min(4.0, EDGE[2]-0.2):.3f});')
# 2
a('tl.fromTo("#hiveP",{strokeDasharray:900,strokeDashoffset:900},{strokeDashoffset:0,duration:.8,ease:"power2.inOut"},' + f'{S(2):.3f});')
a(f'pop("#hive",{S(2):.3f});')
a(f'pop("#u2a",{S(3):.3f});'); a(f'pop("#u2b",{S(4):.3f});')
# 3
a(f'pop("#eq3",{S(5):.3f});'); a(f'rise("#t3",{S(5)+0.5:.3f});')
a(f'tl.fromTo("#b3",{{x:0}},{{x:1600,duration:2.0,ease:"none",immediateRender:false}},{S(5)+0.1:.3f});')
# 4
a(f'rise("#t4",{S(6):.3f});')
a(f'tl.fromTo("#pod",{{scaleX:0}},{{scaleX:1,duration:.4,ease:EO}},{S(6)+0.05:.3f});')
for i in range(3): a(f'pop("#c4{i}",{S(6)+0.15+i*0.12:.3f});')
for i in range(14):
    a(f'tl.fromTo("#r4{i}",{{y:0,rotation:0}},{{y:{1150+(i%3)*60},rotation:{(i%2*2-1)*200},duration:1.1,ease:"power2.in",immediateRender:false}},{S(6)+0.9+i*0.09:.3f});')
a(f'pop("#n4",{S(6)+0.4:.3f});'); a(f'rise("#l4",{S(6)+0.5:.3f});')
a(f'tl.to("#n4a",{{yPercent:-100,opacity:0,duration:.35,ease:"power2.in"}},{S(6)+2.0:.3f});')
a(f'tl.fromTo("#n4b",{{yPercent:100,opacity:0}},{{yPercent:0,opacity:1,duration:.35,ease:E}},{S(6)+2.1:.3f});')
# 5
a(f'pop("#u5a",{S(7):.3f});'); a(f'slam("#u5b",{S(8):.3f});'); a(f'flash({S(8):.3f});')
# 6
a(f'rise("#t6",{S(9):.3f});')
for i in range(5): a(f'pop("#h6{i}",{S(9)+0.1+i*0.1:.3f});')
a(f'pop("#u6",{S(10):.3f});')
for i, (x, y) in enumerate([(90,560),(420,520),(740,580),(230,820),(620,860)]):
    a(f'tl.to("#h6{i}",{{x:{(430-x)*0.55:.0f},y:{(1040-y)*0.55:.0f},duration:1.2,ease:"power2.inOut"}},{S(10)+0.1:.3f});')
a(f'slam("#t6b",{S(10)+0.4:.3f});')
# 7
a(f'rise("#t7",{S(11):.3f});')
a(f'tl.fromTo(".j7",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.3,ease:E,stagger:.05}},{S(11)+0.1:.3f});')
a(f'pop("#tag7",{S(11)+1.4:.3f});')
a(f'tl.fromTo("#tag7",{{rotation:0}},{{rotation:4,duration:.07,repeat:7,yoyo:true,ease:"none",immediateRender:false}},{S(12)-0.6:.3f});')
a(f'tl.to("#p7a",{{opacity:0,duration:.15}},{S(12):.3f});')
a(f'tl.fromTo("#p7b",{{opacity:0,scale:1.4}},{{opacity:1,scale:1,duration:.3,ease:E}},{S(12):.3f});'); a(f'flash({S(12):.3f});')
# 8
a(f'slam("#t8",{S(13):.3f});'); a(f'rise("#t8b",{S(13)+0.3:.3f});')
a(f'tl.fromTo("#j8",{{x:0}},{{x:200,duration:1.8,ease:"none"}},{S(14):.3f});')
for i in range(6): a(f'tl.fromTo("#k8{i}",{{x:0}},{{x:{900+i*40},duration:1.9,ease:"power1.in",immediateRender:false}},{S(14)+i*0.05:.3f});')
a(f'rise("#l8",{S(14)+0.3:.3f});')
# 9
a(f'tl.fromTo("#t9",{{opacity:0,x:-500,skewX:-18}},{{opacity:1,x:0,skewX:0,duration:.35,ease:E}},{S(15):.3f});')
a(f'pop("#sun9",{S(16):.3f});')
a(f'tl.fromTo(".fl",{{opacity:0,y:60}},{{opacity:1,y:0,duration:.3,ease:E,stagger:.06}},{S(16)+0.1:.3f});')
a(f'tl.to(".flw .head",{{rotation:75,y:30,transformOrigin:"50% 100%",filter:"grayscale(1) brightness(.6)",duration:.8,ease:"power2.in",stagger:.08}},{S(17):.3f});')
a(f'tl.to(".flw .stem",{{stroke:"#5a5048",duration:.6}},{S(17):.3f});')
a(f'pop("#n9",{S(17)+0.3:.3f});'); a(f'rise("#l9",{S(17)+0.4:.3f});')
a(f'tl.to("#n9a",{{yPercent:-100,opacity:0,duration:.3,ease:"power2.in"}},{S(18):.3f});')
a(f'tl.fromTo("#n9b",{{yPercent:100,opacity:0}},{{yPercent:0,opacity:1,duration:.35,ease:E}},{S(18)+0.1:.3f});')
# 10
a(f'pop("#u10a",{S(19):.3f});'); a(f'pop("#u10b",{S(20):.3f});')
a(f'slam("#tag10",{S(21):.3f});')
a(f'tl.fromTo("#st10",{{opacity:0,scale:2.2,rotation:-14}},{{opacity:1,scale:1,rotation:-8,duration:.3,ease:E}},{S(22):.3f});'); a(f'flash({S(22):.3f});')
# 11
a(f'tl.fromTo("#b11",{{opacity:0,scale:.3,rotation:20}},{{opacity:1,scale:1,rotation:0,duration:.45,ease:E}},{S(23):.3f});')
a(f'tl.to("#b11",{{opacity:0,y:-200,duration:.3,ease:"power2.in"}},{S(24)-0.1:.3f});')
a(f'rise("#t11",{S(24):.3f});')
for i in range(5): a(f'tl.fromTo("#bar{i}",{{scaleY:0,transformOrigin:"50% 100%"}},{{scaleY:1,duration:.35,ease:E}},{S(24)+0.3+i*0.32:.3f});')
a(f'rise("#l11",{S(24)+1.0:.3f});')
# 12
a(f'rise("#t12",{S(25):.3f});'); a(f'rise("#l12",{S(25)+0.3:.3f});')
a(f'slam("#n12",{S(26):.3f});'); a(f'flash({S(26):.3f});')
# 13
a(f'draw("#lnP",{S(27):.3f},1.6);'); a(f'draw("#lnS",{S(27)+0.2:.3f},1.6);')
a(f'rise("#lp",{S(27)+1.2:.3f});'); a(f'rise("#ls",{S(27)+1.4:.3f});')
a(f'slam("#t13",{S(28)+0.6:.3f});')
a(f'out("#ch13, #lp, #ls, #t13",{VO_END-2.4:.3f});'); a(f'pop("#lock",{VO_END-2.2:.3f});')
# disclaimer
d = VO_END
a(f'tl.fromTo("#dBar",{{scaleX:0,transformOrigin:"left"}},{{scaleX:1,duration:.5,ease:EO}},{d+0.2:.3f});')
a(f'tl.fromTo("#dL1",{{opacity:0,y:28}},{{opacity:1,y:0,duration:.5,ease:EO}},{d+0.4:.3f});')
a(f'tl.fromTo("#dL2",{{opacity:0}},{{opacity:1,duration:.5}},{d+1.0:.3f});')
a(f'tl.fromTo("#dL3",{{opacity:0}},{{opacity:1,duration:.5}},{d+1.6:.3f});')

HONEYCOMB = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='208' viewBox='0 0 120 208'>"
             "<path d='M60 4 L112 34 L112 94 L60 124 L8 94 L8 34 Z M60 124 L60 208 M0 0' fill='none' stroke='%23F2B705' stroke-opacity='.07' stroke-width='3'/></svg>")
AUDIO = ('<audio id="vo" class="clip" src="assets/vo-mix.m4a" data-start="0" '
         f'data-duration="{TOTAL}" data-track-index="3" data-volume="1"></audio>') if os.path.exists("assets/vo-mix.m4a") else ""

HTML = f'''<!doctype html>
<!-- Explained with Honey No.1 — Inflation. Hand-built SVG/GSAP, no AI imagery. Generated by gen.py; edit that, not this. -->
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1920">
<script src="vendor/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:{INK}}}
#root{{width:100%;height:100%;position:relative;background:{INK};font-family:"Liberation Sans",Arial,sans-serif;color:{PAPER}}}
#bg{{position:absolute;inset:0;background-image:url("{HONEYCOMB}");background-size:120px 208px}}
.clip{{position:absolute;inset:0}}
.slug{{position:absolute;left:96px;top:150px;color:{MUTED};font-size:22px;letter-spacing:.28em;font-weight:800}}
.stamp{{position:absolute;left:96px;top:1745px;color:{MUTED};font-size:24px}}
.mega{{position:absolute;left:0;right:0;text-align:center;font-weight:800;letter-spacing:-.04em;line-height:.95}}
.big{{position:absolute;left:0;right:0;text-align:center;font-weight:800;letter-spacing:-.02em;line-height:1.05}}
.gold{{color:{GOLD}}} .red{{color:{RED}}}
.c{{left:0;right:0;text-align:center}}
.ch{{display:inline-block}}
.lbl{{position:absolute;color:{MUTED};font-size:30px;letter-spacing:.2em;font-weight:800;text-transform:uppercase}}
.abs,.actor,.rain,.ch8,.fl,.j7{{position:absolute}}
.unit{{position:absolute;width:360px;text-align:center}}
.unit .num{{font-size:120px;font-weight:800;letter-spacing:-.03em;margin-top:6px}}
.unit .lbl{{position:static;margin-top:4px}}
.eq{{position:absolute;left:0;right:0;display:flex;align-items:center;justify-content:center;gap:40px}}
.podium{{position:absolute;left:150px;width:780px;top:680px;height:26px;border-radius:13px;background:{GOLD};transform-origin:center}}
.flip{{position:absolute;left:0;right:0;height:170px;overflow:hidden;text-align:center;font-size:160px;font-weight:800;letter-spacing:-.03em}}
.flip span{{position:absolute;left:0;right:0;top:0}}
.tag{{position:absolute;left:190px;width:700px;top:1040px;height:130px;border-radius:24px;background:{PAPER};color:{INK};
  font-size:62px;font-weight:800;display:flex;align-items:center;justify-content:center}}
.tag span{{position:absolute}}
.tagl{{position:absolute;font-size:34px;font-weight:800;letter-spacing:.08em}}
.sun{{position:absolute;left:770px;top:520px;width:200px;height:200px;border-radius:50%;
  background:radial-gradient(circle,{GOLD} 0 48%,{RED} 49% 52%,transparent 53%)}}
.stampbig{{position:absolute;left:0;right:0;top:1240px;text-align:center}}
#st10{{font-size:130px;font-weight:800;color:{GOLD};letter-spacing:-.02em}}
.bar{{position:absolute;width:130px;background:{GOLD};border-radius:10px 10px 0 0}}
.bar .bv{{position:absolute;top:-56px;left:0;right:0;text-align:center;font-size:40px;font-weight:800}}
.bar .bx{{position:absolute;bottom:-50px;left:0;right:0;text-align:center;font-size:24px;color:{MUTED};font-weight:800}}
.lock{{position:absolute;left:0;right:0;top:640px;text-align:center}}
.wing{{transform-box:fill-box;transform-origin:50% 100%}}
.cap{{pointer-events:none}}
.capIn{{position:absolute;left:96px;right:120px;top:1475px;font-size:46px;line-height:1.24;font-weight:800;
  text-shadow:0 2px 10px rgba(0,0,0,.9)}}
.cw{{display:inline-block}} .cw.hl{{color:{GOLD}}}
#compliance{{position:absolute;left:96px;top:1690px;color:{GOLD};font-size:29px;font-weight:800}}
#flash{{position:absolute;inset:0;background:{PAPER};opacity:0;pointer-events:none;z-index:50}}
#prog{{position:absolute;left:0;bottom:0;height:6px;width:100%;background:{GOLD};transform-origin:left center}}
#discCard{{position:absolute;inset:0;background:{INK};display:flex;flex-direction:column;justify-content:center;padding:0 96px}}
#discCard .dbar{{width:168px;height:6px;background:{GOLD};margin-bottom:46px}}
#discCard .dl1{{font-size:56px;font-weight:800;line-height:1.16}}
#discCard .dl2{{color:{MUTED};font-size:30px;line-height:1.5;margin-top:36px}}
#discCard .dl3{{color:{GOLD};font-size:24px;letter-spacing:.2em;font-weight:800;margin-top:52px}}
</style></head><body>
<svg width="0" height="0" style="position:absolute"><defs><clipPath id="beeBody"><ellipse cx="62" cy="62" rx="40" ry="29"/></clipPath></defs></svg>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
<div id="bg"></div>
{"".join(SC)}
{caps()}
{DISC_HTML}
<div id="flash"></div><div id="prog"></div>
{AUDIO}
</div>
<script>
const tl=gsap.timeline({{paused:true}});
const E="back.out(1.6)", EO="power3.out";
const slam=(s,at,d=.38)=>tl.fromTo(s,{{autoAlpha:0,scale:1.35}},{{autoAlpha:1,scale:1,duration:d,ease:"power4.out"}},at);
const pop=(s,at,d=.4)=>tl.fromTo(s,{{autoAlpha:0,scale:.5}},{{autoAlpha:1,scale:1,duration:d,ease:E}},at);
const rise=(s,at,d=.42,y=40)=>tl.fromTo(s,{{autoAlpha:0,y}},{{autoAlpha:1,y:0,duration:d,ease:EO}},at);
const out=(s,at,d=.28)=>tl.to(s,{{autoAlpha:0,duration:d,ease:"power2.in"}},at);
const flash=(at)=>tl.fromTo("#flash",{{opacity:0}},{{opacity:.45,duration:.04,immediateRender:false}},at).to("#flash",{{opacity:0,duration:.1}},at+.05);
const draw=(s,at,d)=>{{const p=document.querySelector(s);const L=p.getTotalLength();p.style.strokeDasharray=L;
  tl.fromTo(s,{{strokeDashoffset:L}},{{strokeDashoffset:0,duration:d,ease:"power2.inOut"}},at);}};
{chr(10).join(T)}
window.__timelines=window.__timelines||{{}};window.__timelines["main"]=tl;tl.seek(0);
</script></body></html>'''
open("index.html", "w").write(HTML)
print(f"total {TOTAL}s · VO {VO_END}s · {len(LINES)} lines · {len(T)} tweens")
for i in range(1, len(LINES)+1): print(f"  L{i:2d} {L(i)[0]:6.2f} +{L(i)[1]:5.2f}  {LINES[i-1][:50]}")
