# -*- coding: utf-8 -*-
"""Scene stills for the Three AI Picks long-form.

White page is the base — Zul is black line on white (CHARACTER-ZUL.md).
Near-black type, one red accent, nothing else. Tickers are always bold,
uppercase, and are the only words allowed the accent colour.

    python3 scenes_aip.py && node shoot_at.js aipscenes 1920 1080
"""
import io, os
from art import zul_pose

K, R, W, GREY = '#111314', '#d81e28', '#ffffff', '#8a9199'
F = 'Liberation Sans,Arial,sans-serif'

def page(body):
    return ('<!doctype html><meta charset="utf-8">'
            f'<style>*{{margin:0;padding:0;box-sizing:border-box}}'
            f'html,body{{background:{W};width:1920px;height:1080px;overflow:hidden;font-family:{F}}}'
            f'.strip{{position:absolute;left:0;top:1006px;width:1920px;height:74px;background:{K};'
            f'color:#fff;font:700 30px {F};text-align:center;line-height:74px;letter-spacing:1px}}'
            f'</style>{body}')

def txt(x, y, s, size, color=K, weight=700, anchor='left', ls=0):
    a = {'left':'left','mid':'center','right':'right'}[anchor]
    tx = {'left':'', 'mid':'transform:translateX(-50%);', 'right':'transform:translateX(-100%);'}[anchor]
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;{tx}'
            f'font:{weight} {size}px {F};color:{color};letter-spacing:{ls}px;'
            f'line-height:1.08;white-space:pre">{s}</div>')

def rule(x, y, w, h=11, color=R):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color}"></div>'

def compliance():
    return '<div class="strip">EDUCATIONAL ONLY. NOT FINANCIAL ADVICE.</div>'

def zul(pset, pose, x, y, h):
    return (f'<svg style="position:absolute;left:0;top:0" width="1920" height="1080">'
            f'{zul_pose(pset, pose, x=x, y=y, h=h)}</svg>')

# ---- scene archetypes -------------------------------------------------------

def s_number(big, label, sub=None, pose=None):
    b = [txt(960, 300, big, 210, anchor='mid'), rule(560, 560, 800),
         txt(960, 600, label, 46, color=GREY, anchor='mid', ls=5)]
    if sub: b.append(txt(960, 700, sub, 40, color=K, anchor='mid', weight=400))
    if pose: b.append(zul(*pose))
    return ''.join(b)

def s_ticker(sym, exch, line, pose):
    return ''.join([zul(*pose),
        txt(980, 250, sym, 150, color=R), txt(980, 420, exch, 34, color=GREY, ls=6),
        rule(980, 480, 780), txt(980, 530, line, 44, weight=400)])

def s_turn(n):
    return ''.join([
        f'<div style="position:absolute;left:0;top:0;width:1920px;height:1080px;background:{K}"></div>',
        txt(960, 420, 'THE NUMBER THE BULL', 72, color='#fff', anchor='mid'),
        txt(960, 505, 'CASE LEAVES OUT', 72, color='#fff', anchor='mid'),
        rule(820, 630, 280), txt(960, 680, n, 34, color=GREY, anchor='mid', ls=6)])

def s_compare(la, a, lb, b_, note=None):
    out = [txt(480, 300, a, 170, anchor='mid'), txt(480, 500, la, 38, color=GREY, anchor='mid', ls=4),
           txt(1440, 300, b_, 170, anchor='mid'), txt(1440, 500, lb, 38, color=GREY, anchor='mid', ls=4),
           rule(955, 280, 10, 260, K)]
    if note: out.append(txt(960, 660, note, 42, anchor='mid', weight=400))
    return ''.join(out)

def s_statement(lines, pose=None, size=64, upto=None):
    n = len(lines) if upto is None else upto
    out = [txt(140, 300 + i*86, l, size) for i, l in enumerate(lines[:n])]
    if pose: out.append(zul(*pose))
    return ''.join(out)

def reveal(lines, pose=None, size=64):
    """A multi-line statement as a progressive reveal — two beats instead of
    one long hold. 32 stills across 8m49s is a 17-second hold; the style guide
    asks for new information every 10-15s."""
    half = max(1, (len(lines) + 1) // 2)
    return [s_statement(lines, pose, size, upto=half),
            s_statement(lines, pose, size)]

# ---- the 32 scenes ----------------------------------------------------------
Z_PT_R  = ('body', 'full-point-right', 120, 150, 760)
Z_PALM  = ('body', 'full-present-palm', 120, 150, 760)
Z_SKEP  = ('body', 'full-skeptical',    120, 150, 760)
Z_SHOCK = ('body', 'full-shock',        120, 150, 760)
Z_SHRUG = ('body', 'full-shrug',        120, 150, 760)
Z_FRONT = ('body', 'body-front',        120, 150, 760)

_S = [
 s_number('−$14,000,000,000', 'SPACEX FREE CASH FLOW, 2025'),
 s_number('$2,100,000,000,000', 'WHAT THE MARKET SAYS IT IS WORTH'),
 reveal(['Both numbers come from','the same filing.','Only one made it','into the videos.'], Z_FRONT),
 s_compare('MICRON GROSS MARGIN FY25','39.8%','FY26','80.7%'),
 reveal(['Three companies.','Three real theses.','Three numbers nobody','mentions.'], Z_PALM),
 s_ticker('SPCX','NASDAQ','Listed 12 June 2026', Z_PT_R),
 s_number('$135 → $161', 'IPO PRICE → DAY-ONE CLOSE'),
 reveal(['Most people file SpaceX','under "rocket company".','The filing disagrees.'], Z_SKEP),
 s_compare('2025 REVENUE','$18.7bn','OF IT, STARLINK','$11.4bn','61% of the company is broadband.'),
 reveal(['Before 2015, the way to end','a launch was to throw the','rocket away.'], Z_SHOCK),
 s_number('2.3m → 12m', 'STARLINK SUBSCRIBERS, 2023 → JUN 2026'),
 s_turn('SPCX'),
 s_compare('SUBSCRIBERS, Q1 2026','+104.7%','REVENUE PER USER','−22.9%','Some of the growth is bought with price cuts.'),
 s_number('−$14.0bn', 'FREE CASH FLOW', '$6.8bn from operations − $20.7bn capex'),
 reveal(['A constellation is a','subscription the company','pays, not one it collects.'], Z_FRONT),
 s_ticker('BE','NYSE','Joined the S&P 500 on 21 Sept 2026', Z_PT_R),
 reveal(['A data centre needs power.','The grid queue is long.','Bloom sells the box that','skips the queue.'], Z_PALM),
 s_number('$751m → $1.07bn', 'QUARTERLY REVENUE, Q1 → Q2 2026', '+130%, then +166% year on year'),
 s_turn('BE'),
 s_number('$20,000,000,000', 'BACKLOG', 'Contracts run 5–20 years — cancellable annually'),
 s_statement(['A backlog is not','a bank balance.'], Z_SKEP, size=78),
 s_ticker('MU','NASDAQ','FY2026 ended 3 September 2026', Z_PT_R),
 s_number('+256%', 'MICRON REVENUE GROWTH, ONE YEAR', '$37.4bn → $133.2bn'),
 reveal(['An AI accelerator is useless','without memory next to it.','Very few companies can','make the high-end kind.'], Z_PALM),
 s_turn('MU'),
 s_compare('GROSS MARGIN','80.7%','NET MARGIN','≈64%','Gross is not what the company keeps.'),
 s_compare('NVIDIA, LAST QUARTER','75.0%','MICRON, FULL YEAR','80.7%','A memory maker out-earning the chips it feeds.'),
 reveal(['Every producer on earth is','building capacity as fast as','it can pour concrete.'], Z_SHOCK),
 reveal(['Eighty percent margins are','not a new normal.','They are what the top of','a cycle looks like.'], Z_SKEP),
 s_number('$61.5bn', 'NEXT-QUARTER GUIDANCE', 'An estimate. Not money earned.'),
 s_statement(['A cash-flow deficit.','A cancellation clause.','A cycle.'], Z_SHRUG, size=74),
 reveal(['Open the last quarterly release','and find the number','nobody quoted.','','If it is not there,','that is your answer.'], None, size=58),
]

# Expand any entry that is a list (a reveal) into its separate beats.
S = []
for e in _S:
    S.extend(e) if isinstance(e, list) else S.append(e)

if __name__ == '__main__':
    os.makedirs('aipscenes', exist_ok=True)
    for i, body in enumerate(S, 1):
        io.open('aipscenes/%02d.html' % i, 'w', encoding='utf-8').write(page(body + compliance()))
    print('%d scenes -> aipscenes/' % len(S))
