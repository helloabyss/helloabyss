import re
# "93% of Pros Lost to the S&P 500" — The Meticulous Investor, 2026-10-01.
# VO-paced: beat lengths come from the script's word counts, so Sheldon's narration can be
# dropped in later (audio element below) without re-timing. Until then the caption rail
# carries every spoken line, so the piece reads with the sound off.
# Figures: ../SCRIPT.md fact table (SPIVA YE2025, Persistence YE2025, SPIVA mid-2026).

BEATS = [  # (caption line, highlighted word, seconds)
 ("Ninety-three percent.", "Ninety-three", 2.4),
 ("That's how many large-cap fund managers lost to the plain S&P 500.", "lost", 3.6),
 ("Over twenty years.", "twenty", 1.8),
 ("Not financial advice, so do your own research.", "own", 2.4),
 ("These are pros. Research teams. Data terminals. Big salaries.", "pros.", 3.0),
 ("And in 2025 alone, seventy-nine percent of them still trailed the index.", "seventy-nine", 3.8),
 ("So why not just pick the winners?", "winners?", 2.6),
 ("Because the winners don't stay winners.", "don't", 2.6),
 ("Take the top-quarter funds of 2021.", "2021.", 2.4),
 ("By the end of 2025, less than half a percent were still there.", "half", 3.4),
 ("Fewer than one in two hundred.", "two", 2.4),
 ("To be fair, active funds had a better start to 2026.", "fair,", 3.0),
 ("Only sixty-seven percent lagged in the first half.", "sixty-seven", 2.8),
 ("Still two in three.", "two", 1.8),
 ("And an index fund won't save you in a crash. It falls with the market.", "falls", 4.2),
 ("What it does is take the fees out of the fight.", "fees", 3.0),
 ("Tonight, look up one number on every fund you own: the expense ratio.", "expense", 4.0),
 ("It's the one part of your return you know in advance.", "advance.", 3.6),
]
T = []; acc = 0.0
# Narration: ElevenLabs "Brian" (premade, eleven_multilingual_v2), 57.5 s. Beat edges sit in the middle of the
# pause after each line (silencedetect -38 dB / 0.18 s), mapped to sentences by hand: 1-based gap index per line end.
import os, re, subprocess
VO_FILE = "assets/vo-brian.mp3"
if os.path.exists(VO_FILE):
    _o = subprocess.run(["ffmpeg","-hide_banner","-i",VO_FILE,"-af","silencedetect=n=-38dB:d=0.18","-f","null","-"],
                        capture_output=True, text=True).stderr
    _st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", _o)]
    _en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", _o)]
    _g = list(zip(_st, _en))
    LINE_END_GAP = [1,2,3,4,7,9,10,11,12,14,15,16,17,18,20,21,23]
    _edges = [0.0] + [(_g[i-1][0]+_g[i-1][1])/2 for i in LINE_END_GAP] + [_st[-1] + 0.35]
    BEATS = [(c, h, round(_edges[i+1]-_edges[i], 3)) for i,(c,h,_) in enumerate(BEATS)]
for _,_,d in BEATS: T.append(round(acc,3)); acc += d
VO_END = round(acc,3)
DISC_AT, DISC_DUR = VO_END, 4.5
TOTAL = round(DISC_AT + DISC_DUR, 3)
def t(i, off=0.0): return round(T[i-1] + off, 3)   # beat i (1-based) start + offset

# scenes = groups of beats: (id, first beat, last beat, kicker, stamp)
SC = [("a",1,3,"The scorecard","Large-cap funds vs S&P 500 · 20 yrs · SPIVA U.S. Year-End 2025"),
      ("b",4,6,"The pros","SPIVA U.S. Year-End 2025 · calendar 2025"),
      ("c",7,8,"The obvious fix",""),
      ("d",9,11,"Persistence","U.S. Persistence Scorecard Year-End 2025 · domestic equity funds"),
      ("e",12,15,"The other side","SPIVA U.S. Mid-Year 2026 · H1 2026"),
      ("f",16,18,"What you control","Illustration · no specific fund shown")]
def span(sc):
    a,b0 = sc[1], sc[2]; st = T[a-1]; en = (T[b0] if b0 < len(T) else VO_END)
    return round(st,3), round(en-st,3)

nw = open("compositions/components/number-wheel.html").read()
WHEEL_CSS = re.search(r'<style[^>]*>(.*?)</style>', nw, re.S).group(1)
WHEEL_JS  = re.search(r'<script>(.*?)</script>', nw, re.S).group(1)
def wheel(v): return f'<span class="hf-number-wheel" data-value="{v}"></span>'

def scene(sid, kicker, inner, stamp):
    st, du = span([s for s in SC if s[0]==sid][0])
    kick = f'<div class="kicker" id="{sid}K">{kicker}</div>' if kicker else ""
    stp = f'<div class="stamp" id="{sid}S">{stamp}</div>' if stamp else ""
    return (f'<div id="s_{sid}" class="clip" data-start="{st}" data-duration="{du}" data-track-index="0">'
      f'<div class="frame"><div class="fr-t"></div>'
      f'<div class="slug">THE METICULOUS INVESTOR</div></div>'
      f'<div class="rule" id="{sid}R"></div>{kick}{inner}{stp}</div>')

def dots(gid, n=100, cols=10, size=50, gap=18, top=0):
    out = ""
    for i in range(n):
        r, c = divmod(i, cols)
        out += (f'<div class="dot" id="{gid}{i}" style="left:{c*(size+gap)}px;top:{r*(size+gap)}px;'
                f'width:{size}px;height:{size}px"></div>')
    return f'<div class="dotGrid" id="{gid}" style="top:{top}px">{out}</div>'

S = []
# A — hook: 93% → lost to the S&P 500 → over 20 years (line race)
S.append(scene("a","The scorecard",
  f'<div class="mega red" id="aN" style="top:430px;font-size:300px">{wheel("93")}%</div>'
  '<div class="big" id="aL" style="top:760px;font-size:76px;width:888px">LOST TO THE<br><span class="red">S&amp;P 500</span></div>'
  '<svg id="aChart" class="chart" viewBox="0 0 888 360" style="top:1000px">'
  '<line x1="0" y1="359" x2="888" y2="359" class="axis"/>'
  '<path id="aIdx" class="ln paper" d="M0,300 C120,270 220,250 330,215 S560,140 660,110 S820,50 888,30"/>'
  '<path id="aAct" class="ln accent" d="M0,300 C120,282 220,272 330,250 S560,205 660,190 S820,160 888,150"/>'
  '</svg>'
  '<div class="lbl" id="aY0" style="left:96px;top:1372px">2006</div>'
  '<div class="lbl" id="aY1" style="left:860px;top:1372px">2025</div>'
  '<div class="tag" id="aT1" style="left:800px;top:990px">INDEX</div>'
  '<div class="tag red" id="aT2" style="left:800px;top:1130px">AVG FUND</div>'
  '<div class="mega" id="a20" style="top:430px;font-size:300px">20<span class="unit">YRS</span></div>'
  '<div id="compliance">Educational only. Not financial advice.</div>',
  [s for s in SC if s[0]=="a"][0][4]))

# B — not advice / the pros / 79 of 100
S.append(scene("b","The pros",
  '<div class="big dim" id="bNA" style="top:520px;font-size:64px;width:888px">Not financial advice.<br>Do your own research.</div>'
  '<div class="mega" id="bP1" style="top:470px;font-size:150px">PROS.</div>'
  '<div class="mega dim" id="bP2" style="top:660px;font-size:110px">TEAMS.</div>'
  '<div class="mega dim" id="bP3" style="top:790px;font-size:110px">TERMINALS.</div>'
  '<div class="mega dim" id="bP4" style="top:920px;font-size:110px">SALARIES.</div>'
  + dots("bG", top=430) +
  f'<div class="mega red" id="bN" style="top:1180px;font-size:140px">{wheel("79")}%</div>'
  '<div class="big" id="bNL" style="top:1210px;left:430px;font-size:54px;width:560px">TRAILED<br>THE INDEX · 2025</div>',
  [s for s in SC if s[0]=="b"][0][4]))

# C — pick the winners? / winners don't stay
S.append(scene("c","The obvious fix",
  '<div class="mega" id="cQ" style="top:560px;font-size:130px">PICK THE<br><span class="red">WINNERS?</span></div>'
  '<div class="mega" id="cA1" style="top:560px;font-size:130px">WINNERS</div>'
  '<div class="mega" id="cA2" style="top:700px;font-size:130px">DON\'T</div>'
  '<div class="mega red" id="cA3" style="top:840px;font-size:130px">STAY.</div>'
  '<div class="strike" id="cX" style="top:905px;width:470px"></div>',
  ""))

# D — top quartile 2021 → 0.46% left
rows = ""
for i in range(12):
    rows += f'<div class="lbRow" id="dR{i}" style="top:{560+i*58}px"><span class="lbN">#{i+1}</span><span class="lbBar"></span></div>'
S.append(scene("d","Persistence",
  '<div class="big" id="dH" style="top:400px;font-size:62px;width:888px">TOP QUARTER · <span class="red">2021</span></div>'
  + rows +
  f'<div class="mega" id="dYr" style="top:400px;font-size:62px">{wheel("2025")}</div>'
  '<div class="mega red" id="dN" style="top:1240px;font-size:150px">0.46%</div>'
  '<div class="big" id="dNL" style="top:1250px;left:640px;font-size:50px;width:360px">STILL<br>THERE</div>'
  '<div class="mega" id="d200" style="top:1240px;font-size:150px">1 IN <span class="red">200+</span></div>',
  [s for s in SC if s[0]=="d"][0][4]))

# E — to be fair: 67 of 100 / still 2 in 3 / index funds fall too
S.append(scene("e","The other side",
  '<div class="big" id="eF" style="top:400px;font-size:62px;width:888px">TO BE FAIR · <span class="red">2026 H1</span></div>'
  + dots("eG", top=520) +
  f'<div class="mega red" id="eN" style="top:1240px;font-size:140px">{wheel("67")}%</div>'
  '<div class="big" id="eNL" style="top:1290px;left:430px;font-size:54px;width:560px">LAGGED</div>'
  '<div class="mega" id="e23" style="top:1250px;left:430px;font-size:110px">2 IN 3</div>'
  '<svg id="eChart" class="chart" viewBox="0 0 888 520" style="top:560px">'
  '<line x1="0" y1="519" x2="888" y2="519" class="axis"/>'
  '<path id="eLn" class="ln paper" d="M0,120 L140,100 L260,130 L360,90 L430,110 L480,360 L540,430 L600,330 L700,260 L800,200 L888,170"/>'
  '</svg>'
  '<div class="mega" id="eFall" style="top:1160px;font-size:96px">INDEX FUNDS<br><span class="red">FALL TOO.</span></div>',
  [s for s in SC if s[0]=="e"][0][4]))

# F — fees out of the fight / expense ratio / known in advance
S.append(scene("f","What you control",
  '<div class="colLbl" id="fL1" style="left:180px;top:1158px">ACTIVE</div>'
  '<div class="colLbl" id="fL2" style="left:620px;top:1158px">INDEX</div>'
  '<div class="col" id="fC1" style="left:150px;top:560px;height:580px"></div>'
  '<div class="colFee" id="fFee1" style="left:150px;top:560px;height:150px"></div>'
  '<div class="col" id="fC2" style="left:590px;top:560px;height:580px"></div>'
  '<div class="colFee" id="fFee2" style="left:590px;top:560px;height:12px"></div>'
  '<div class="tag red" id="fFT" style="left:150px;top:500px">FEES</div>'
  '<div class="mega" id="fH" style="top:1240px;font-size:78px">FEES OUT OF<br>THE <span class="red">FIGHT.</span></div>'
  '<div id="fPage">'
  '<div class="pgHead">FUND DETAILS</div>'
  '<div class="pgRow"><span>Category</span><span>Large blend</span></div>'
  '<div class="pgRow"><span>Holdings</span><span>— —</span></div>'
  '<div class="pgRow" id="fER"><span>Expense ratio</span><span class="erVal">0.__%</span><i id="fHL"></i></div>'
  '<div class="pgRow"><span>Inception</span><span>— —</span></div>'
  '</div>'
  '<div class="mega" id="fKnown" style="top:1240px;font-size:78px">KNOWN IN<br><span class="red">ADVANCE.</span></div>',
  [s for s in SC if s[0]=="f"][0][4]))

# caption rail: one line per beat, highlighted word in red
CAPS = ""
for i,(line,hl,d) in enumerate(BEATS, 1):
    ws = "".join(f'<span class="cw{" hl" if w==hl else ""}">{w}</span> ' for w in line.split())
    CAPS += (f'<div class="clip cap" id="cap{i}" data-start="{t(i)}" data-duration="{d}" data-track-index="2">'
             f'<div class="capIn">{ws}</div></div>')

DISC = (f'<div id="s_disc" class="clip" data-start="{DISC_AT}" data-duration="{DISC_DUR}" data-track-index="0">'
  '<div id="discCard"><div class="dbar" id="dBar"></div>'
  '<div class="dl1" id="dL1">Educational only.<br>Not financial advice.</div>'
  '<div class="dl2" id="dL2">Not a recommendation to buy or sell any security. Past performance does not '
  'indicate future results. Figures from S&amp;P Dow Jones Indices SPIVA reports, as of the dates shown.</div>'
  '<div class="dl3" id="dL3">THE METICULOUS INVESTOR</div></div></div>')


# ---------------------------------------------------------------- B-roll plates (base layer)
# (file, first beat, last beat, opacity). AI stills from Higgsfield, graded dark/desaturated in CSS,
# moved with slow push-ins so they play as B-roll. Skipped silently if the file isn't on disk yet.
import os
PLATES = [("b02-screen-wall.png",1,1,.55),("b03-lobby.png",2,4,.45),("b02-screen-wall.png",5,5,.50),
          ("b03-lobby.png",9,11,.26),("b08-coins.png",16,16,.45),("b02-screen-wall.png",17,18,.32)]
# Only 3 stills exist (ElevenLabs FLUX.2 Pro; the free plan's daily image cap stopped the other 7), so beats 6-8 and 12-15,
# which carry dot grids, the leaderboard and the crash line, stay on the plain dark ground.
PL = ""; PTW = []
for n,(f,a,z,op) in enumerate(PLATES):
    if not os.path.exists(f"assets/broll/{f}"):
        print("  (plate missing, skipped)", f); continue
    st = T[a-1]; en = T[z] if z < len(T) else VO_END; du = round(en-st,3)
    PL += (f'<div class="clip plate" id="pl{n}" data-start="{st}" data-duration="{du}" data-track-index="1">'
           f'<img src="assets/broll/{f}" alt=""><div class="scrim"></div></div>')
    PTW.append(f'tl.fromTo("#pl{n} img",{{scale:1.06,y:0}},{{scale:1.20,y:-40,duration:{du},ease:"none"}},{st:.3f});')
    PTW.append(f'tl.fromTo("#pl{n} img",{{opacity:0}},{{opacity:{op},duration:.35,ease:"power2.out",immediateRender:false}},{st:.3f});')
    if f == "b04-trophy.png":   # the trophy falls with "STAY."
        PTW.append(f'tl.to("#pl{n} img",{{y:260,rotation:6,opacity:0,duration:.7,ease:"power2.in"}},{t(8,1.9):.3f});')

# ---------------------------------------------------------------- choreography
TW = []
for sid,a,_,_,_ in SC:
    st = T[a-1]
    TW.append(f'tl.fromTo("#{sid}R",{{scaleX:0}},{{scaleX:1,duration:.45,ease:"power3.inOut"}},{st+0.08:.3f});')
    TW.append(f'tl.fromTo("#{sid}K",{{opacity:0,x:-22}},{{opacity:1,x:0,duration:.4,ease:EO}},{st+0.18:.3f});')
    if [s for s in SC if s[0]==sid][0][4]: TW.append(f'tl.fromTo("#{sid}S",{{opacity:0}},{{opacity:1,duration:.4,immediateRender:false}},{st+1.0:.3f});')
for i in range(1, len(BEATS)+1):
    TW.append(f'tl.fromTo("#cap{i} .cw",{{opacity:0,y:18}},{{opacity:1,y:0,duration:.22,ease:EO,stagger:.045}},{t(i,0.02):.3f});')

# A
TW += [f'slam("#aN",{t(1,0.05):.3f},.40);', 'flash(' + f'{t(1,0.05):.3f}' + ');',
       f'roll("#aN",{t(1,0.10):.3f},1.2);',
       f'tl.fromTo("#compliance",{{opacity:0}},{{opacity:1,duration:.3}},{0.4:.3f}).to("#compliance",{{opacity:0,duration:.3}},{4.1:.3f});',
       f'tl.to("#aN",{{scale:.42,y:-40,transformOrigin:"left top",duration:.5,ease:"power3.inOut"}},{t(2,0.0):.3f});',
       f'rise("#aL",{t(2,0.25):.3f});',
       f'tl.fromTo("#aChart",{{opacity:0}},{{opacity:1,duration:.25}},{t(2,0.62):.3f});', f'draw("#aIdx",{t(2,0.7):.3f},2.4);', f'draw("#aAct",{t(2,0.7):.3f},2.4);',
       f'rise("#aY0",{t(2,0.7):.3f},.3,10);', f'rise("#aY1",{t(2,0.7):.3f},.3,10);',
       f'rise("#aT1",{t(2,2.6):.3f},.3,10);', f'rise("#aT2",{t(2,2.8):.3f},.3,10);',
       f'out("#aN",{t(3,0.0):.3f});', f'out("#aL",{t(3,0.0):.3f});',
       f'slam("#a20",{t(3,0.08):.3f},.38);', f'flash({t(3,0.08):.3f});']
# B
TW += [f'rise("#bNA",{t(4,0.1):.3f});', f'out("#bNA",{t(5,-0.1):.3f});',
       f'slam("#bP1",{t(5,0.25):.3f},.32);', f'slam("#bP2",{t(5,1.30):.3f},.30);',
       f'slam("#bP3",{t(5,2.65):.3f},.30);', f'slam("#bP4",{t(5,3.80):.3f},.30);',
       f'out("#bP1, #bP2, #bP3, #bP4",{t(6,-0.05):.3f});',
       f'tl.fromTo("#bG .dot",{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.25,ease:EO,stagger:{{each:.006,from:"start"}}}},{t(6,0.05):.3f});',
       f'tl.fromTo("#bG .dot:nth-child(-n+79)",{{backgroundColor:"#3A3A3C"}},{{backgroundColor:"#D42A2A",duration:.2,stagger:.016,immediateRender:false}},{t(6,0.9):.3f});',
       f'rise("#bN",{t(6,0.9):.3f});', f'roll("#bN",{t(6,1.0):.3f},1.3);', f'rise("#bNL",{t(6,1.2):.3f});']
# C
TW += [f'slam("#cQ",{t(7,0.05):.3f},.40);', f'out("#cQ",{t(8,-0.08):.3f});',
       f'slam("#cA1",{t(8,0.02):.3f},.30);', f'slam("#cA2",{t(8,0.42):.3f},.30);',
       f'slam("#cA3",{t(8,0.82):.3f},.30);', f'flash({t(8,0.82):.3f});',
       f'tl.fromTo("#cX",{{scaleX:0}},{{scaleX:1,duration:.35,ease:"power3.inOut",immediateRender:false}},{t(8,1.4):.3f});',
       f'tl.to("#cA3",{{y:220,rotation:8,opacity:0,duration:.7,ease:"power2.in"}},{t(8,1.9):.3f});']
# D
TW += [f'rise("#dH",{t(9,0.05):.3f});',
       f'tl.fromTo(".lbRow",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:.3,ease:EO,stagger:.05,immediateRender:false}},{t(9,0.4):.3f});',
       f'out("#dH",{t(10,-0.05):.3f});', f'rise("#dYr",{t(10,0.05):.3f},.3,12);', f'roll("#dYr",{t(10,0.05):.3f},2.4);']
for k,i in enumerate([3,9,0,6,11,2,8,5,10,1,7]):   # 11 of 12 rows drop out across the four years
    TW.append(f'tl.to("#dR{i}",{{opacity:.06,x:30,duration:.22,ease:"power2.in"}},{t(10,0.25+k*0.2):.3f});')
TW += [f'tl.to("#dR4 .lbBar",{{backgroundColor:"#D42A2A",duration:.2}},{t(10,2.6):.3f});',
       f'slam("#dN",{t(10,2.4):.3f},.36);', f'rise("#dNL",{t(10,2.6):.3f});',
       f'out("#dN, #dNL",{t(11,-0.05):.3f});', f'slam("#d200",{t(11,0.05):.3f},.36);', f'flash({t(11,0.05):.3f});']
# E
TW += [f'rise("#eF",{t(12,0.05):.3f});',
       f'tl.fromTo("#eG .dot",{{opacity:0,scale:.3}},{{opacity:1,scale:1,duration:.25,ease:EO,stagger:{{each:.006}}}},{t(12,0.3):.3f});',
       f'tl.fromTo("#eG .dot:nth-child(-n+67)",{{backgroundColor:"#3A3A3C"}},{{backgroundColor:"#D42A2A",duration:.2,stagger:.02,immediateRender:false}},{t(13,0.05):.3f});',
       f'rise("#eN",{t(13,0.1):.3f});', f'roll("#eN",{t(13,0.15):.3f},1.2);', f'rise("#eNL",{t(13,0.3):.3f});',
       f'out("#eNL",{t(14,-0.05):.3f});', f'slam("#e23",{t(14,0.02):.3f},.32);', f'flash({t(14,0.02):.3f});',
       f'out("#eG, #eN, #e23",{t(15,-0.05):.3f});', f'tl.to("#eF",{{opacity:0,duration:.25}},{t(15,-0.05):.3f});',
       f'tl.fromTo("#eChart",{{opacity:0}},{{opacity:1,duration:.2}},{t(15,0.1):.3f});', f'draw("#eLn",{t(15,0.15):.3f},2.0);', f'shake({t(15,1.05):.3f});',
       f'rise("#eFall",{t(15,1.6):.3f});']
# F
TW += [f'tl.fromTo("#fC1, #fC2",{{scaleY:0,transformOrigin:"center bottom"}},{{scaleY:1,duration:.55,ease:EO,immediateRender:false}},{t(16,0.05):.3f});',
       f'rise("#fL1",{t(16,0.3):.3f},.3,10);', f'rise("#fL2",{t(16,0.3):.3f},.3,10);',
       f'tl.fromTo("#fFee1, #fFee2",{{scaleY:0,transformOrigin:"center top"}},{{scaleY:1,duration:.5,ease:EO,immediateRender:false}},{t(16,0.8):.3f});',
       f'rise("#fFT",{t(16,1.0):.3f},.3,10);', f'slam("#fH",{t(16,1.5):.3f},.36);',
       f'out("#fC1, #fC2, #fFee1, #fFee2, #fL1, #fL2, #fFT, #fH",{t(17,-0.05):.3f});',
       f'tl.fromTo("#fPage",{{opacity:0,y:80}},{{opacity:1,y:0,duration:.5,ease:EO}},{t(17,0.05):.3f});',
       f'tl.fromTo("#fPage",{{y:0}},{{y:-140,duration:1.6,ease:"power2.inOut",immediateRender:false}},{t(17,0.7):.3f});',
       f'tl.fromTo("#fHL",{{scaleX:0}},{{scaleX:1,duration:.45,ease:"power3.inOut",immediateRender:false}},{t(17,2.3):.3f});',
       f'tl.to("#fPage",{{scale:1.12,transformOrigin:"center 60%",duration:3.0,ease:"none"}},{t(18,0.0):.3f});',
       f'slam("#fKnown",{t(18,0.4):.3f},.40);']
# disclaimer
d = DISC_AT
TW += [f'tl.fromTo("#dBar",{{scaleX:0,transformOrigin:"left"}},{{scaleX:1,duration:.5,ease:EO}},{d+0.2:.3f});',
       f'tl.fromTo("#dL1",{{opacity:0,y:28}},{{opacity:1,y:0,duration:.55,ease:EO}},{d+0.4:.3f});',
       f'tl.fromTo("#dL2",{{opacity:0}},{{opacity:1,duration:.55}},{d+1.0:.3f});',
       f'tl.fromTo("#dL3",{{opacity:0}},{{opacity:1,duration:.55}},{d+1.7:.3f});']

EXTRA_CSS = """
.unit{font-size:.30em;letter-spacing:.08em;margin-left:18px;color:#8A8A8A;vertical-align:.95em}
.chart{position:absolute;left:96px;width:888px;overflow:visible}
.axis{stroke:rgba(245,245,243,.18);stroke-width:2}
.ln{fill:none;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
.ln.paper{stroke:#F5F5F3}.ln.accent{stroke:#D42A2A}
.tag{position:absolute;color:#F5F5F3;font-size:26px;font-weight:800;letter-spacing:.18em}
.tag.red{color:#D42A2A}
.dotGrid{position:absolute;left:150px;width:780px;height:780px}
.dot{position:absolute;border-radius:50%;background:#3A3A3C}
.strike{position:absolute;left:96px;height:14px;background:#D42A2A;transform-origin:left center}
.lbRow{position:absolute;left:96px;width:888px;height:46px}
.lbN{position:absolute;left:0;top:4px;color:#8A8A8A;font-size:30px;font-weight:800;width:80px}
.lbBar{position:absolute;left:90px;top:8px;height:30px;width:760px;background:#F5F5F3}
.col{position:absolute;width:340px;background:#F5F5F3}
.colFee{position:absolute;width:340px;background:#D42A2A}
.colLbl{position:absolute;color:#F5F5F3;font-size:40px;font-weight:800;letter-spacing:.16em}
#fPage{position:absolute;left:96px;top:520px;width:888px;background:#161618;border:1px solid rgba(245,245,243,.14);padding:34px 40px 18px}
.pgHead{color:#8A8A8A;font-size:26px;letter-spacing:.28em;font-weight:800;margin-bottom:18px}
.pgRow{position:relative;display:flex;justify-content:space-between;color:#F5F5F3;font-size:42px;padding:26px 0;border-top:1px solid rgba(245,245,243,.10)}
.pgRow span:first-child{color:#B9B9B9}
.erVal{font-weight:800}
#fHL{position:absolute;left:-16px;right:-16px;top:12px;bottom:12px;background:rgba(212,42,42,.32);transform-origin:left center;z-index:-1}
#fER{z-index:1}
.cap{pointer-events:none}
.capIn{position:absolute;left:96px;right:120px;top:1470px;font-size:46px;line-height:1.24;font-weight:800;color:#F5F5F3;
  letter-spacing:-.01em;text-shadow:0 2px 10px rgba(0,0,0,.85)}
.cw{display:inline-block}.cw.hl{color:#D42A2A}
#flash{position:absolute;inset:0;background:#F5F5F3;opacity:0;pointer-events:none;z-index:50}
#compliance{top:1680px}
.plate{overflow:hidden}
.plate img{position:absolute;left:-60px;top:-110px;width:1200px;height:2140px;object-fit:cover;
  filter:grayscale(.7) contrast(1.1) brightness(.78);transform-origin:50% 45%}
.plate .scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,11,12,.85) 0%,rgba(11,11,12,.25) 30%,rgba(11,11,12,.35) 62%,rgba(11,11,12,.92) 100%)}
"""
HELPERS = """
const flash=(at)=>tl.fromTo("#flash",{opacity:.0},{opacity:.55,duration:.04,immediateRender:false},at).to("#flash",{opacity:0,duration:.08},at+.05);
const shake=(at)=>tl.fromTo("#root",{x:0},{x:14,duration:.04,yoyo:true,repeat:5,ease:"none",immediateRender:false},at).to("#root",{x:0,duration:.02},at+.25);
const draw=(s,at,d)=>{const p=document.querySelector(s);const L=p.getTotalLength();
  p.style.strokeDasharray=L;tl.fromTo(s,{strokeDashoffset:L},{strokeDashoffset:0,duration:d,ease:"power2.inOut"},at);};
const roll=(s,at,d)=>tl.fromTo(s+" .hf-number-wheel-strip",{y:0},{y:(_,el)=>el.style.getPropertyValue("--hf-number-target-y"),
  duration:d,ease:"power3.out",stagger:.06,immediateRender:false},at);
"""
HTML = open("tpl.tplsrc").read().replace("{{","{").replace("}}","}")
HTML = HTML.replace("Every figure traceable to ../../research/2026-09-27.md", "Every figure traceable to ../SCRIPT.md (fact table)")
HTML = HTML.replace("kinetic weekly. Type IS the motion. Silent by design:", "93% of pros lost to the S&P 500. VO-paced; captions carry the script:")
HTML = (HTML.replace("__TOTAL__", str(TOTAL))
        .replace("/*WHEELCSS*/", WHEEL_CSS + EXTRA_CSS).replace("/*WHEELJS*/", WHEEL_JS)
        .replace("/*SCENES*/", PL + "\n" + "\n".join(S) + "\n" + CAPS + "\n" + DISC + '\n<div id="flash"></div>\n' + ((f'<audio id="vo" class="clip" src="assets/vo-mix.m4a" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-volume="1"></audio>') if os.path.exists("assets/vo-mix.m4a") else (f'<audio id="vo" class="clip" src="{VO_FILE}" data-start="0" data-duration="{VO_END}" data-track-index="3" data-volume="1"></audio>' if os.path.exists(VO_FILE) else '')))
        .replace("const out=", HELPERS + "const out=")
        .replace("/*TW*/", "\n".join(PTW + TW)))
# autoAlpha: hidden beats get visibility:hidden, so they never count as on-screen
HTML = HTML.replace("{opacity:0,","{autoAlpha:0,").replace("{opacity:1,","{autoAlpha:1,").replace("to(s,{opacity:0,","to(s,{autoAlpha:0,")
open("index.html","w").write(HTML)
print(f"total {TOTAL}s · VO {VO_END}s · {len(BEATS)} beats · {len(TW)} tweens")
for sid,a,b0,_,_ in SC: st,du = span((sid,a,b0)); print(f"  {sid} beats {a}-{b0}  {st:5.2f} → {st+du:5.2f}")
