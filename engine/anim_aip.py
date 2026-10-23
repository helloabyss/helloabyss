# -*- coding: utf-8 -*-
"""Animated timeline for the Three AI Picks long-form.

Replaces the static-still slideshow. Two things it fixes:

1. ZUL NEVER SITS ON THE TYPE. The bands are enforced by arithmetic, not by
   eye: a body pose at h=700 puts its ink at x 247..453 (measured from
   art/poses/manifest.json), so the type column starts at 620 and a guard
   below raises if any text in a scene with Zul starts left of it. The first
   cut had him straight through the words.

2. THINGS MOVE. Numbers count up, bars grow, rules wipe, lines rise in
   sequence, and Zul CUTS BETWEEN DRAWN POSES mid-beat instead of standing
   still for thirteen seconds.

    python3 anim_aip.py && node render_anim.js
"""
import base64, io, json, os

M = json.load(open('art/poses/manifest.json'))
W, H = 1920, 1080
K, R, GREY, PAPER = '#111314', '#d81e28', '#8a9199', '#ffffff'
TYPE_X = 620          # type column, clear of Zul's ink
FULL_X = 150          # type column when no Zul is present
ZUL_X, ZUL_Y, ZUL_H = 10, 176, 760

# Licensed Adobe Stock plates, graded to the palette by prep_broll.js. Keys are the
# beat index they sit under. Photography is the BASE layer (STYLE-GUIDE.md); the type
# sits on top of it. Never under a beat containing Zul -- his line art needs white.
PLATES = {
    0:  'dish-array',   # SPCX  -- the cash-burn hook, over the ground segment
    15: 'dish-array',   # SPCX  -- Starlink subscriber series
    17: 'dish-array',   # SPCX  -- turn card
    26: 'datacentre',   # BE    -- quarterly revenue, over the demand it serves
    28: 'substation',   # BE    -- turn card, the grid
    29: 'datacentre',   # BE    -- the backlog
    33: 'wafer',        # MU    -- FY26 revenue, over silicon
    38: 'wafer',        # MU    -- turn card
    43: 'wafer',        # MU    -- the margin comparison
    49: 'racks',        # MU    -- next-quarter guidance
    57: 'dish-array',   # close -- back to the opening image, as the script loops back
}

def plate_html(name, i):
    b = base64.b64encode(open('broll/%s-graded.jpg' % name, 'rb').read()).decode()
    d = 1 if i % 2 else -1   # alternate the push so it never feels mechanical
    return (f'<div class="plate" data-a="kb" data-dir="{d}">'
            f'<img src="data:image/jpeg;base64,{b}"></div><div class="scrim"></div><div class="scrimv"></div>')

_cache = {}
def b64(rel):
    if rel not in _cache:
        _cache[rel] = base64.b64encode(open(os.path.join('art/poses', rel), 'rb').read()).decode()
    return _cache[rel]

def zul_imgs(pset, poses):
    m0 = M[pset]['poses'][poses[0]]
    w = ZUL_H * m0['w'] / float(m0['h'])
    out = []
    for i, p in enumerate(poses):
        out.append(f'<img class="zp" data-i="{i}" src="data:image/png;base64,{b64(M[pset]["poses"][p]["file"])}" '
                   f'style="left:{ZUL_X}px;top:{ZUL_Y}px;width:{w:.0f}px;height:{ZUL_H}px">')
    return f'<div class="zul" data-a="pose" data-n="{len(poses)}">' + ''.join(out) + '</div>'

def el(cls, style, inner='', **d):
    at = ''.join(f' data-{k.replace("_","-")}="{v}"' for k, v in d.items())
    return f'<div class="{cls}" style="{style}"{at}>{inner}</div>'

# ---------- beat builders ----------------------------------------------------

def b_num(value, pre='', suf='', dec=1, label='', note='', zul=None):
    x = TYPE_X if zul else FULL_X
    o = [zul_imgs(*zul) if zul else '']
    o.append(el('num', f'left:{x}px;top:300px;font-size:190px', '0',
                a='count', to=value, dec=dec, pre=pre, suf=suf, t0=0.02, t1=0.42))
    o.append(el('rule', f'left:{x}px;top:540px;width:{1840-x if not zul else 1180}px', '',
                a='wipe', t0=0.30, t1=0.55))
    o.append(el('lab', f'left:{x}px;top:586px', label, a='rise', t0=0.42, t1=0.60))
    if note:
        o.append(el('note', f'left:{x}px;top:666px', note, a='rise', t0=0.56, t1=0.74))
    return ''.join(o)

def b_ticker(sym, exch, line, zul, stats=()):
    o = [zul_imgs(*zul)]
    o.append(el('tk', f'left:{TYPE_X}px;top:218px', sym, a='rise', t0=0.03, t1=0.22))
    o.append(el('lab', f'left:{TYPE_X}px;top:398px', exch, a='rise', t0=0.16, t1=0.34))
    o.append(el('rule', f'left:{TYPE_X}px;top:458px;width:1180px', '', a='wipe', t0=0.24, t1=0.52))
    o.append(el('note', f'left:{TYPE_X}px;top:506px', line, a='rise', t0=0.40, t1=0.60))
    for i, (k, v) in enumerate(stats):
        y = 612 + i * 104
        o.append(el('chiprule', f'left:{TYPE_X}px;top:{y+6}px;width:8px;height:74px', '',
                    a='growv', t0=0.52+i*0.12, t1=0.66+i*0.12))
        o.append(el('lab', f'left:{TYPE_X+34}px;top:{y}px;font-size:27px', k,
                    a='rise', t0=0.54+i*0.12, t1=0.70+i*0.12))
        o.append(el('chipv', f'left:{TYPE_X+34}px;top:{y+34}px', v,
                    a='rise', t0=0.58+i*0.12, t1=0.74+i*0.12))
    return ''.join(o)

def b_turn(tag):
    return ''.join([
        el('card', 'left:0;top:0;width:1920px;height:1080px', '', a='none'),
        el('tn', 'left:0;top:400px;width:1920px;text-align:center',
           'THE NUMBER THE BULL CASE LEAVES OUT', a='rise', t0=0.08, t1=0.34),
        el('rule', 'left:820px;top:540px;width:280px', '', a='wipe', t0=0.26, t1=0.52),
        el('lab', 'left:0;top:596px;width:1920px;text-align:center', tag, a='rise', t0=0.40, t1=0.60)])

def b_compare(la, a, lb, b_, note='', dec=1, pre='', suf='%'):
    """Two figures side by side. Bar length is proportional to |value| against the
    larger of the pair — equal-length bars for unequal numbers is a lie."""
    mx = max(abs(a), abs(b_))
    o = []
    for i, (lab, val, cx) in enumerate(((la, a, 480), (lb, b_, 1440))):
        o.append(el('num', f'left:{cx-380}px;top:286px;width:760px;text-align:center;font-size:170px',
                    '0', a='count', to=val, dec=dec, pre=pre, suf=suf, t0=0.04+i*0.16, t1=0.46+i*0.16))
        o.append(el('track', f'left:{cx-300}px;top:500px;width:600px;height:20px'))
        o.append(el('gbar' + (' neg' if val < 0 else ''),
                    f'left:{cx-300}px;top:500px;width:{int(600*abs(val)/mx)}px;height:20px', '',
                    a='grow', t0=0.18+i*0.16, t1=0.56+i*0.16))
        o.append(el('lab', f'left:{cx-380}px;top:546px;width:760px;text-align:center', lab,
                    a='rise', t0=0.30+i*0.16, t1=0.50+i*0.16))
    o.append(el('vdiv', 'left:955px;top:286px;width:10px;height:238px', '', a='growv', t0=0.0, t1=0.30))
    if note:
        o.append(el('note', 'left:150px;top:648px;width:1620px;text-align:center;font-size:50px', note,
                    a='rise', t0=0.60, t1=0.80))
    o.append(el('scale', 'left:150px;top:760px;width:1620px;text-align:center',
                'Bar length is proportional to the figure above it.', a='rise', t0=0.80, t1=0.94))
    return ''.join(o)

def b_lines(lines, zul=None, size=62):
    x = TYPE_X if zul else FULL_X
    o = [zul_imgs(*zul) if zul else '']
    top = 300 if len(lines) <= 4 else 250
    for i, ln in enumerate(lines):
        if not ln: continue
        t0 = 0.04 + i * 0.13
        o.append(el('ln', f'left:{x}px;top:{top+i*92}px;font-size:{size}px', ln,
                    a='rise', t0=round(t0, 3), t1=round(t0 + 0.20, 3)))
    return ''.join(o)

def b_bars(series, label, zul=None, dec=1):
    """A column series that grows. The group is centred and the gap is tied to the
    bar width -- spreading N bars across the full span flung a two-bar chart to the
    frame edges."""
    x = TYPE_X if zul else FULL_X
    span = 1180 if zul else (1840 - x)
    n = len(series)
    bw = int(min(230, span / (n * 1.75)))
    gap = int(bw * 0.62)
    group = n * bw + (n - 1) * gap
    x0 = x + max(0, (span - group) // 2)
    base, top = 620, 300
    mx = max(v for _, v in series)
    o = [zul_imgs(*zul) if zul else '']
    o.append(el('lab', f'left:{x}px;top:{top-74}px;width:{span}px', label, a='rise', t0=0.02, t1=0.20))
    o.append(el('zline', f'left:{x0-30}px;top:{base}px;width:{group+60}px;height:3px', '',
                a='wipe', t0=0.06, t1=0.30))
    for i, (lbl, v) in enumerate(series):
        h = max(6, int((base - top) * v / mx))
        bx = x0 + i * (bw + gap)
        o.append(el('vbar', f'left:{bx}px;top:{base-h}px;width:{bw}px;height:{h}px', '',
                    a='growup', t0=0.14 + i*0.13, t1=0.46 + i*0.13))
        o.append(el('chipv', f'left:{bx-50}px;top:{base-h-82}px;width:{bw+100}px;'
                    f'text-align:center;font-size:46px', '', a='count', to=v,
                    dec=dec, pre='', suf='',
                    t0=0.14 + i*0.13, t1=0.50 + i*0.13))
        o.append(el('lab', f'left:{bx-50}px;top:{base+22}px;width:{bw+100}px;'
                    f'text-align:center;font-size:28px', lbl,
                    a='rise', t0=0.22 + i*0.13, t1=0.42 + i*0.13))
    return ''.join(o)

def b_spark(a, b_, la, lb, label, note, zul):
    """Two REAL observed prices and the move between them. No invented series."""
    x0, y0, w, h = TYPE_X, 600, 1140, 240
    lo, hi = min(a, b_), max(a, b_)
    pad = (hi - lo) * 0.9 or 1
    def yy(v): return y0 + h * (1 - (v - lo + pad*0.25) / (hi - lo + pad*0.5))
    o = [zul_imgs(*zul)]
    o.append(el('tk', f'left:{TYPE_X}px;top:200px', label, a='rise', t0=0.03, t1=0.20))
    o.append(el('note', f'left:{TYPE_X}px;top:386px', note, a='rise', t0=0.16, t1=0.34))
    o.append(f'<svg class="svg" style="left:0;top:0" width="{W}" height="{H}">'
             f'<line x1="{x0}" y1="{y0+h}" x2="{x0+w}" y2="{y0+h}" stroke="{GREY}" stroke-width="2"/>'
             f'<path data-a="dash" data-t0="0.30" data-t1="0.76" '
             f'd="M{x0},{yy(a):.0f} L{x0+w},{yy(b_):.0f}" fill="none" stroke="{R}" '
             f'stroke-width="10" stroke-linecap="round"/>'
             f'<circle cx="{x0}" cy="{yy(a):.0f}" r="11" fill="{R}"/>'
             f'<circle data-a="pop" data-t0="0.74" data-t1="0.86" cx="{x0+w}" cy="{yy(b_):.0f}" '
             f'r="15" fill="{R}"/></svg>')
    o.append(el('wnum', f'left:{x0}px;top:{yy(a)+28:.0f}px;width:320px', '',
                a='count', to=a, dec=0, pre='$', suf='', t0=0.26, t1=0.44))
    o.append(el('lab', f'left:{x0}px;top:{yy(a)+96:.0f}px;width:320px;font-size:26px',
                la, a='rise', t0=0.34, t1=0.50))
    o.append(el('wnum', f'left:{x0+w-180}px;top:{yy(b_)-96:.0f}px;width:360px;text-align:right', '',
                a='count', to=b_, dec=2, pre='$', suf='', t0=0.60, t1=0.84))
    o.append(el('lab', f'left:{x0+w-220}px;top:{yy(b_)-150:.0f}px;width:400px;text-align:right;'
                f'font-size:26px', lb, a='rise', t0=0.70, t1=0.88))
    return ''.join(o)

def b_waterfall(rows, label):
    """Bars off a zero line — positive up in black, negative down in red."""
    ZY, SPAN = 500, 250
    mx = max(abs(v) for _, v in rows)
    o = [el('lab', f'left:{FULL_X}px;top:200px', label, a='rise', t0=0.02, t1=0.18)]
    o.append(el('zline', f'left:{FULL_X}px;top:{ZY}px;width:1620px;height:3px', '',
                a='wipe', t0=0.04, t1=0.26))
    bw, gap = 320, 200
    for i, (lbl, v) in enumerate(rows):
        h = max(4, int(SPAN * abs(v) / mx))
        bx = FULL_X + 170 + i * (bw + gap)
        up = v >= 0
        o.append(el('wbar' + (' pos' if up else ' neg'),
                    f'left:{bx}px;top:{ZY-h if up else ZY}px;width:{bw}px;height:{h}px;'
                    f'transform-origin:{"bottom" if up else "top"} center', '',
                    a='growv', t0=0.18 + i*0.17, t1=0.52 + i*0.17))
        o.append(el('wnum', f'left:{bx-40}px;top:{ZY-h-74 if up else ZY+h+16}px;width:{bw+80}px;'
                    f'text-align:center;color:{K if up else R}', '',
                    a='count', to=v, dec=1, pre='$', suf='bn', t0=0.18+i*0.17, t1=0.56+i*0.17))
        ly = ZY + 22 if up else ZY + h + 92
        o.append(el('lab', f'left:{bx-60}px;top:{ly}px;width:{bw+120}px;'
                    f'text-align:center;font-size:27px', lbl, a='rise', t0=0.34+i*0.17, t1=0.54+i*0.17))
    o.append(el('scale', f'left:{FULL_X}px;top:900px;width:1620px;text-align:center',
                'Operations minus capital expenditure. Both figures from the same filing.',
                a='rise', t0=0.82, t1=0.96))
    return ''.join(o)

def b_dial(pct, label, note, cmp_pct=None, cmp_label=''):
    """An arc that sweeps to a percentage, with the number counting inside it."""
    cx, cy, r = 470, 500, 185
    C = 2 * 3.141592653589793 * r
    o = [f'<svg class="svg" style="left:0;top:0" width="{W}" height="{H}">'
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e4e7ea" stroke-width="40"/>'
         f'<circle data-a="arc" data-t0="0.06" data-t1="0.62" data-c="{C:.1f}" data-pct="{pct}" '
         f'cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{R}" stroke-width="40" '
         f'stroke-linecap="butt" stroke-dasharray="{C:.1f}" stroke-dashoffset="{C:.1f}" '
         f'transform="rotate(-90 {cx} {cy})"/></svg>']
    o.append(el('num', f'left:{cx-240}px;top:{cy-78}px;width:480px;text-align:center;font-size:120px',
                '0', a='count', to=pct, dec=1, pre='', suf='%', t0=0.06, t1=0.62))
    o.append(el('lab', f'left:{cx-300}px;top:{cy+230}px;width:600px;text-align:center', label,
                a='rise', t0=0.30, t1=0.50))
    o.append(el('ln', f'left:900px;top:360px;font-size:62px;width:900px', note,
                a='rise', t0=0.52, t1=0.74))
    if cmp_pct is not None:
        o.append(el('track', 'left:900px;top:600px;width:720px;height:46px'))
        o.append(el('gbar', f'left:900px;top:600px;width:{int(7.2*cmp_pct)}px;height:46px', '',
                    a='grow', t0=0.62, t1=0.88))
        o.append(el('lab', 'left:900px;top:666px', cmp_label, a='rise', t0=0.74, t1=0.90))
    return ''.join(o)

def b_stats(label, rows):
    """Three figures side by side. For a passage that reads out several numbers in a
    row and would otherwise sit on one card for half a minute."""
    o = [el('lab', f'left:{FULL_X}px;top:250px;width:1620px', label, a='rise', t0=0.02, t1=0.18)]
    n = len(rows)
    w = int(1620 / n)
    for i, (k, v) in enumerate(rows):
        x = FULL_X + i * w
        o.append(el('chiprule', f'left:{x}px;top:360px;width:8px;height:150px', '',
                    a='growv', t0=0.10 + i*0.14, t1=0.26 + i*0.14))
        o.append(el('num', f'left:{x+34}px;top:352px;width:{w-60}px;font-size:92px;'
                    f'white-space:nowrap', v,
                    a='rise', t0=0.16 + i*0.14, t1=0.34 + i*0.14))
        o.append(el('lab', f'left:{x+34}px;top:470px;width:{w-60}px;font-size:27px', k,
                    a='rise', t0=0.22 + i*0.14, t1=0.38 + i*0.14))
    return ''.join(o)

# ---------- the beats --------------------------------------------------------
BODY = 'body'
PT  = (BODY, ['body-front', 'full-point-right'])
PALM= (BODY, ['body-front', 'full-present-palm'])
SKEP= (BODY, ['body-front', 'full-skeptical'])
SHOK= (BODY, ['body-front', 'full-shock'])
SHRG= (BODY, ['body-front', 'full-shrug'])
TUP = (BODY, ['body-front', 'full-thumbs-up'])

BEATS = [
 # --- the hook -------------------------------------------------------------
 b_num(14.0, '\u2212$', 'bn', 1, 'SPACEX FREE CASH FLOW, 2025'),
 b_num(2.1, '$', 'tn', 1, 'WHAT THE MARKET SAYS IT IS WORTH'),
 b_lines(['Both numbers come from','the same filing.'], PALM),
 b_lines(['Both numbers come from','the same filing.','Only one made it','into the videos.'], SKEP),
 b_compare('MICRON GROSS MARGIN FY25', 39.8, 'FY26', 80.7),
 b_lines(['Three companies.','Three real theses.'], PT),
 b_lines(['Three companies.','Three real theses.','Three numbers','nobody mentions.'], PALM),
 b_lines(['The bull case,','from the documents.','Then the line underneath it.'], PALM),
 # --- SPCX -----------------------------------------------------------------
 b_spark(135, 160.95, 'IPO PRICE', 'CLOSE, DAY ONE', 'SPCX',
         'Listed on NASDAQ, 12 June 2026', PT),
 b_num(2.1, '$', 'tn', 1, 'VALUATION AT THAT CLOSE', 'Up 19% on the first day of trading.'),
 b_lines(['Most people file SpaceX','under "rocket company".'], SKEP),
 b_lines(['Most people file SpaceX','under "rocket company".','The filing disagrees.'], SHOK),
 b_compare('2025 REVENUE', 18.7, 'OF IT, STARLINK', 11.4,
           note='61% of the company is broadband.', pre='$', suf='bn'),
 b_lines(['Before 2015, the way to','end a launch was to','throw the rocket away.'], SHOK),
 b_lines(['Imagine buying a jet,','flying it to Paris,','and leaving it there.'], SHRG),
 b_bars([('2023', 2.3), ('2024', 4.4), ('2025', 8.9), ('MAR 26', 10.3), ('JUN 26', 12.0)],
        'STARLINK SUBSCRIBERS, MILLIONS'),
 b_num(4.4, '$', 'bn', 1, 'STARLINK OPERATING INCOME, 2025', 'On a 39% margin.'),
 b_turn('SPCX'),
 b_compare('SUBSCRIBERS, Q1 26', 104.7, 'REVENUE PER USER', -22.9,
           note='Growth is real.', pre='', suf='%'),
 b_compare('REVENUE PER USER, 2023', 99, 'MAR 2026', 66,
           note='Some of the growth is being bought with price cuts.',
           dec=0, pre='$', suf=''),
 b_waterfall([('CASH FROM OPERATIONS', 6.8), ('CAPITAL EXPENDITURE', -20.7),
              ('FREE CASH FLOW', -14.0)], 'SPACEX, 2025'),
 b_lines(['Satellites are not','a one-off purchase.','They de-orbit, and they','have to be replaced.'], PALM),
 b_lines(['A constellation is a','subscription the company','pays, not one it collects.'], SKEP),
 # --- BE -------------------------------------------------------------------
 b_ticker('BE', 'NYSE', 'Joined the S&P 500 on 21 Sept 2026', PT,
          [('Q2 2026 REVENUE', '$1.07bn'), ('FY26 GUIDANCE', 'raised three times'),
           ('BACKLOG', 'about $20bn')]),
 b_lines(['A data centre needs power.','The grid queue is long.'], PALM),
 b_lines(['A data centre needs power.','The grid queue is long.','Bloom sells the box','that skips the queue.'], TUP),
 b_bars([('Q1 26', 0.751), ('Q2 26', 1.07)],
        'BLOOM QUARTERLY REVENUE, $BN \u2014 +130%, THEN +166% YEAR ON YEAR', dec=2),
 b_bars([('FEB', 3.2), ('APR', 3.6), ('JUL', 4.05)],
        'FY26 GUIDANCE, $BN \u2014 RAISED THREE TIMES. MIDPOINT OF EACH RANGE', dec=2),
 b_turn('BE'),
 b_num(20.0, '$', 'bn', 1, 'BACKLOG', 'Contracts run 5\u201320 years \u2014 cancellable annually'),
 b_lines(['A backlog is not','a bank balance.'], SKEP, size=76),
 b_lines(['$20bn of intent,','cancellable once a year.','Quoting it without the clause','is quoting half a sentence.'], SKEP),
 # --- MU -------------------------------------------------------------------
 b_ticker('MU', 'NASDAQ', 'FY2026 ended 3 September 2026', PT,
          [('FY2026 REVENUE', '$133.19bn'), ('EARNINGS PER SHARE', '$74.33'),
           ('GROSS MARGIN', '80.7%')]),
 b_compare('FY25 REVENUE', 37.4, 'FY26 REVENUE', 133.2, pre='$', suf='bn'),
 b_num(256, '', '%', 0, 'GROWTH IN A SINGLE YEAR', 'At a company more than forty years old.'),
 b_stats('MICRON, FY2026', [('NET INCOME', '$84.97bn'), ('EARNINGS PER SHARE', '$74.33'),
                            ('GROSS MARGIN, FROM 39.8%', '80.7%')]),
 b_lines(['An AI accelerator is useless','without memory next to it.'], PALM),
 b_lines(['An AI accelerator is useless','without memory next to it.','Very few companies make','the high-end kind.'], SHOK),
 b_turn('MU'),
 b_dial(80.7, 'MICRON GROSS MARGIN FY26', 'Gross margin is not\nwhat the company keeps.',
        cmp_pct=63.8, cmp_label='NET MARGIN 63.8% \u2014 CALCULATED'),
 b_num(63.8, '', '%', 1, 'NET MARGIN \u2014 CALCULATED',
       'Net income \u00f7 revenue. Not a line in the release.'),
 b_lines(['And here is the comparison','that should make you careful','rather than excited.'], SKEP),
 b_compare('NVIDIA, LAST QUARTER', 75.0, 'MICRON, FULL YEAR', 80.7),
 b_compare('NVIDIA, FY2026', 71.1, 'MICRON, FY2026', 80.7,
           note='A year against a quarter \u2014 and it still holds.'),
 b_lines(['A memory maker earning more','per dollar of sales than the','chips it exists to feed.'], SHOK),
 b_lines(['Every producer on earth','is building capacity as fast','as it can pour concrete.'], SHOK),
 b_lines(['Memory is the most reliably','cyclical industry in technology.'], SKEP),
 b_lines(['Eighty percent margins','are not a new normal.'], SKEP),
 b_lines(['Eighty percent margins','are not a new normal.','They are what the top','of a cycle looks like.'], SKEP),
 b_num(61.5, '$', 'bn', 1, 'NEXT-QUARTER GUIDANCE', 'An estimate. Not money earned.'),
 # --- the close ------------------------------------------------------------
 b_lines(['A cash-flow deficit.','A cancellation clause.','A cycle.'], SHRG, size=72),
 b_lines(['None of those make these','bad businesses.'], PALM, size=76),
 b_lines(['The bull case and the risk','come from the same document.','Only one tends to make it','into the video you watched.'], SKEP),
 b_lines(['All three counterweights','are in public filings.'], PALM, size=76),
 b_num(10, '', '', 0, 'MINUTES TO FIND THEM', 'And free to read.'),
 b_lines(['Open the last quarterly','release and find the number','nobody quoted.'], PALM),
 b_lines(['If it is not there,','that is your answer.'], None, size=84),
 b_num(3.0, '', '', 0, 'COMPANIES', 'Every counterweight came from a public filing.'),
]

# ---------- guard: type must never sit on Zul --------------------------------
import re
for i, b in enumerate(BEATS, 1):
    if 'class="zul"' not in b: continue
    for m in re.finditer(r'class="(?:ln|tk|num|lab|note)"[^>]*style="left:(-?\d+)px', b):
        if int(m.group(1)) < TYPE_X:
            raise SystemExit('beat %d puts type at x=%s, inside Zul\'s band (<%d)'
                             % (i, m.group(1), TYPE_X))
print('guard passed: no type inside Zul\'s band in any of %d beats' % len(BEATS))

CSS = f'''*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:{PAPER};width:{W}px;height:{H}px;overflow:hidden;
  font-family:Liberation Sans,Arial,sans-serif;color:{K}}}
.sc{{position:absolute;inset:0;display:none}} .sc.on{{display:block}}
.sc>div,.sc>img{{position:absolute}}
.zul{{position:absolute;inset:0}} .zp{{position:absolute;display:none}} .zp.on{{display:block}}
.num{{font-weight:700;letter-spacing:-2px;line-height:1}}
.tk{{font-weight:700;font-size:160px;color:{R};letter-spacing:1px;line-height:1}}
.lab{{font-weight:700;font-size:34px;color:{GREY};letter-spacing:5px}}
.note{{font-weight:400;font-size:42px}}
.ln{{font-weight:700;line-height:1.15;white-space:pre-line}}
.rule{{height:12px;background:{R};transform-origin:left center}}
.gbar{{background:{K};transform-origin:left center}} .gbar.neg{{background:{R}}}
.track{{background:#e4e7ea}}
.chiprule{{background:{R};transform-origin:top center}}
.chipv{{font-weight:700;font-size:54px;letter-spacing:-1px}}
.scale{{font-size:26px;color:{GREY};font-style:italic}}
.vbar{{background:{K};transform-origin:bottom center}}
.vdiv{{background:{K};transform-origin:top center}}
.card{{background:{K}}} .tn{{font-weight:700;font-size:70px;color:#fff}}
.svg{{position:absolute;pointer-events:none}}
.zline{{background:{K};transform-origin:left center}}
.wbar.pos{{background:{K}}} .wbar.neg{{background:{R}}}
.wnum{{font-weight:700;font-size:56px;letter-spacing:-1px}}
.card~.lab{{color:{GREY}}} .card~.tn{{color:#fff}}
.plate{{position:absolute;inset:0;overflow:hidden}}
.plate img{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;transform-origin:center}}
.scrim{{position:absolute;inset:0;background:linear-gradient(100deg,
  rgba(10,11,12,.74) 0%,rgba(10,11,12,.52) 46%,rgba(10,11,12,.22) 100%)}}
.scrimv{{position:absolute;inset:0;background:linear-gradient(180deg,
  rgba(10,11,12,.62) 0%,rgba(10,11,12,.10) 34%,rgba(10,11,12,.12) 62%,rgba(10,11,12,.66) 100%)}}
.sc.photo .card{{display:none}}
.sc.photo .num,.sc.photo .ln,.sc.photo .tn,.sc.photo .chipv,.sc.photo .wnum,
.sc.photo .note,.sc.photo .lab{{text-shadow:0 2px 18px rgba(0,0,0,.85)}}
body.photo #sec{{color:#e4e9ee;text-shadow:0 2px 14px rgba(0,0,0,.9)}}
.sc.photo .num,.sc.photo .ln,.sc.photo .note,.sc.photo .chipv,.sc.photo .wnum,
.sc.photo .tn{{color:#fff}}
.sc.photo .lab{{color:#dfe4e9}} .sc.photo .scale{{color:#aeb5bc}}
.sc.photo .vbar,.sc.photo .gbar,.sc.photo .vdiv,.sc.photo .zline{{background:#fff}}
.sc.photo .track{{background:rgba(255,255,255,.20)}}
body.photo #rail{{background:#111314;border-top-color:#30353b}}
body.photo #railin{{color:#aeb5bc}}
#prog{{position:absolute;left:0;top:0;height:6px;background:{R};z-index:50}}
#rail{{position:absolute;left:0;top:{H-74-62}px;width:{W}px;height:62px;overflow:hidden;
  border-top:2px solid #e4e7ea;z-index:30;background:{PAPER}}}
#railin{{position:absolute;top:0;white-space:nowrap;line-height:62px;font-size:28px;
  font-weight:700;letter-spacing:2px;color:{GREY}}}
#railin b{{color:{R}}}
#sec{{position:absolute;right:48px;top:40px;font-size:28px;font-weight:700;letter-spacing:6px;
  color:{GREY};z-index:30}}
body.dark #rail,body.dark #sec{{display:none}}
body.dark #strip,body.photo #strip{{border-top:3px solid {R}}}
#strip{{position:absolute;left:0;top:{H-74}px;width:{W}px;height:74px;background:{K};
  color:#fff;font-size:30px;font-weight:700;text-align:center;line-height:74px;letter-spacing:1px;z-index:40}}'''

JS = '''
const ease=t=>t<0?0:t>1?1:(t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2);
const span=(t,a,b)=>ease((t-a)/Math.max(1e-6,b-a));
const SC=[...document.querySelectorAll('.sc')];
window.NSC=SC.length;
const TOT=%s, CUM=%s, SEC=%s;
function fmt(v,dec,pre,suf){
  const s=Math.abs(v).toFixed(dec).replace(/\\B(?=(\\d{3})+(?!\\d))/g,',');
  return (v<0?'\u2212':'')+pre+s+suf;
}
window.setFrame=function(s,t){
  SC.forEach((e,i)=>e.classList.toggle('on',i===s));
  const sc=SC[s];
  sc.querySelectorAll('[data-a]').forEach(e=>{
    const a=e.dataset.a, t0=+(e.dataset.t0||0), t1=+(e.dataset.t1||1), p=span(t,t0,t1);
    if(a==='count'){
      const to=+e.dataset.to, dec=+e.dataset.dec;
      e.textContent=fmt(to*p,dec,e.dataset.pre||'',e.dataset.suf||'');
      e.style.opacity=Math.min(1,p*6);
    } else if(a==='wipe'||a==='grow'){ e.style.transform='scaleX('+p+')';
    } else if(a==='growv'){ e.style.transform='scaleY('+p+')';
    } else if(a==='growup'){ e.style.transform='scaleY('+p+')';
    } else if(a==='rise'){ e.style.opacity=p; e.style.transform='translateY('+(26*(1-p))+'px)';
    } else if(a==='kb'){
      const d=+e.dataset.dir, z=1.06+0.09*t;
      e.firstElementChild.style.transform=
        'scale('+z.toFixed(4)+') translate('+(d*1.6*(t-0.5)).toFixed(3)+'%,'+(-d*0.9*(t-0.5)).toFixed(3)+'%)';
    } else if(a==='pop'){
      e.setAttribute('r', (15*(0.2+0.8*p)).toFixed(1)); e.style.opacity=p;
    } else if(a==='dash'){
      const L=e.getTotalLength(); e.style.strokeDasharray=L; e.style.strokeDashoffset=L*(1-p);
    } else if(a==='arc'){
      const C=+e.dataset.c; e.style.strokeDashoffset=C*(1-p*(+e.dataset.pct)/100);
    } else if(a==='pose'){
      const n=+e.dataset.n, idx=Math.min(n-1,Math.floor(t*n*0.9+0.18));
      e.querySelectorAll('.zp').forEach(z=>z.classList.toggle('on',+z.dataset.i===idx));
      e.style.transform='translateY('+(Math.sin(t*Math.PI*2*0.7)*4).toFixed(2)+'px)';
    }
  });
  const g=CUM[s]+TOT[s]*t, dur=CUM[CUM.length-1];
  document.getElementById('prog').style.width=((g/dur)*1920).toFixed(1)+'px';
  const photo=sc.classList.contains('photo');
  document.body.classList.toggle('photo', photo);
  document.body.classList.toggle('dark', !photo && sc.querySelector('.card')!==null);
  const ri=document.getElementById('railin');
  ri.style.left=(-((g*58)%(ri.scrollWidth/4)))+'px';
  document.getElementById('sec').textContent=SEC[s];
};'''

RAIL = '<b>SPCX</b> \u2212$14.0BN FREE CASH FLOW, 2025 \u00b7 <b>BE</b> $20BN BACKLOG, CANCELLABLE ANNUALLY \u00b7 <b>MU</b> 80.7% GROSS MARGIN, TOP OF A CYCLE \u00b7 '

if __name__ == '__main__':
    # Durations come from align_aip.py, which maps every beat to the script paragraphs
    # it illustrates and places each cut at a real pause in the narration. They are NOT
    # derived from visual weight any more -- that is what made the picture drift.
    import align_aip
    durs, _b, _c, _w = align_aip.build()
    if len(durs) != len(BEATS):
        raise SystemExit('align_aip gives %d durations for %d beats -- SRC and BEATS '
                         'have drifted apart' % (len(durs), len(BEATS)))
    cum = [0.0]
    for d in durs: cum.append(cum[-1] + d)
    body = ''
    for i, b in enumerate(BEATS):
        if i in PLATES:
            if 'class="zul"' in b:
                raise SystemExit('beat %d has both a plate and Zul; his line art '
                                 'disappears on a dark plate' % i)
            body += f'<div class="sc photo" id="sc{i}">{plate_html(PLATES[i], i)}{b}</div>'
        else:
            body += f'<div class="sc" id="sc{i}">{b}</div>'
    print('%d of %d beats carry a photographic plate' % (len(PLATES), len(BEATS)))
    sec = []
    cur = 'THE SETUP'
    for b in BEATS:
        for sym in ('SPCX', 'BE', 'MU'):
            if ('>%s<' % sym) in b: cur = sym
        sec.append(cur)
    sec[-3:] = ['THE ASK'] * 3
    js = (JS.replace('%s', json.dumps([round(d,3) for d in durs]), 1)
            .replace('%s', json.dumps([round(c,3) for c in cum]), 1)
            .replace('%s', json.dumps(sec), 1))
    io.open('aip-anim.html','w',encoding='utf-8').write(
        f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>'
        f'{body}<div id="prog"></div><div id="sec"></div>'
        f'<div id="rail"><div id="railin">{RAIL*4}</div></div>'
        f'<div id="strip">EDUCATIONAL ONLY. NOT FINANCIAL ADVICE.</div>'
        f'<script>{js}</script>')
    print('%d beats · %.1fs total · shortest %.1fs · longest %.1fs · aligned to the narration'
          % (len(BEATS), sum(durs), min(durs), max(durs)))
