# -*- coding: utf-8 -*-
"""Composition templates.

The first three shorts used ONE layout for every beat -- plate, centred word,
optional bar -- repeated 28 times. That reads as a slide deck however good the
footage is, which is exactly what the owner called it. These are distinct
compositions a beat can be assigned, so the frame changes shape, not just
content.

Palette is a dict so a look can be swapped whole.
"""

LIGHT = dict(
    ground='#f4f1ea', ink='#15171a', mute='#6b7280',
    accent='#c8102e', accent2='#1b6b4a', warm='#e0a008',
    card='#ffffff', plate_op=0.92, grade='saturate(0.75) contrast(1.05) brightness(1.02)')

WARM_DARK = dict(
    ground='#141118', ink='#f7f3ec', mute='#9b9186',
    accent='#e0a008', accent2='#4ea36f', warm='#e0a008',
    card='#221d26', plate_op=0.72, grade='saturate(0.62) contrast(1.12) brightness(0.72)')

EDITORIAL = dict(
    ground='#0e1a2b', ink='#f2f6fb', mute='#8fa3bd',
    accent='#ffb020', accent2='#43c59e', warm='#ffb020',
    card='#16263d', plate_op=0.66, grade='saturate(0.7) contrast(1.1) brightness(0.8)')


def css(p):
    return f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:{p['ground']};
 font-family:"Liberation Sans Narrow","Liberation Sans",Arial,sans-serif;color:{p['ink']}}}
.plate{{position:absolute;object-fit:cover;filter:{p['grade']}}}
.card{{position:absolute;background:{p['card']};border-radius:20px;
 box-shadow:0 24px 70px rgba(0,0,0,.28)}}
.k{{font-weight:800;letter-spacing:-2px;line-height:.9}}
.lab{{font-weight:700;letter-spacing:5px;text-transform:uppercase;color:{p['mute']}}}
.acc{{color:{p['accent']}}}
.acc2{{color:{p['accent2']}}}
.rule{{position:absolute;height:6px;background:{p['ink']}}}
"""


def full_stat(p, plate, lab, big, sub=None):
    """A — full-bleed footage, stat anchored low. The one we had."""
    return (f'<img class="plate" src="{plate}" style="left:0;top:0;width:1080px;height:1920px;opacity:{p["plate_op"]}">'
            f'<div style="position:absolute;left:0;top:0;width:1080px;height:1920px;'
            f'background:linear-gradient(transparent 38%,{p["ground"]}ee 72%,{p["ground"]} 100%)"></div>'
            f'<div class="lab" style="position:absolute;left:70px;top:1160px;font-size:36px">{lab}</div>'
            f'<div class="k" style="position:absolute;left:70px;top:1210px;font-size:210px">{big}</div>'
            + (f'<div style="position:absolute;left:74px;top:1450px;font-size:44px;font-weight:700;color:{p["mute"]}">{sub}</div>' if sub else ''))


def split(p, plate, lab, big, note=None):
    """B — footage top, flat panel bottom. Hard horizon, very different shape."""
    return (f'<img class="plate" src="{plate}" style="left:0;top:0;width:1080px;height:1020px">'
            f'<div style="position:absolute;left:0;top:1020px;width:1080px;height:900px;background:{p["ground"]}"></div>'
            f'<div class="rule" style="left:0;top:1014px;width:1080px;background:{p["accent"]}"></div>'
            f'<div class="lab" style="position:absolute;left:70px;top:1100px;font-size:38px">{lab}</div>'
            f'<div class="k" style="position:absolute;left:70px;top:1160px;font-size:230px">{big}</div>'
            + (f'<div style="position:absolute;left:74px;top:1430px;width:940px;font-size:46px;font-weight:700">{note}</div>' if note else ''))


def card_stat(p, plate, lab, big, note=None):
    """C — footage behind, a floating card carries the number."""
    return (f'<img class="plate" src="{plate}" style="left:0;top:0;width:1080px;height:1920px;opacity:{p["plate_op"]}">'
            f'<div class="card" style="left:70px;top:620px;width:940px;height:620px;padding:60px">'
            f'<div class="lab" style="font-size:36px">{lab}</div>'
            f'<div class="k" style="margin-top:28px;font-size:230px">{big}</div>'
            + (f'<div style="margin-top:30px;font-size:46px;font-weight:700;color:{p["mute"]}">{note}</div>' if note else '')
            + '</div>')


def quote(p, plate, line, who):
    """D — vox-pop card. A line in quotes with an attribution, like a street
    interview caption. Breaks the stat rhythm completely."""
    return (f'<img class="plate" src="{plate}" style="left:0;top:0;width:1080px;height:1920px;opacity:{p["plate_op"]}">'
            f'<div style="position:absolute;left:0;top:0;width:1080px;height:1920px;'
            f'background:linear-gradient({p["ground"]}cc,transparent 40%,{p["ground"]}dd)"></div>'
            f'<div class="card" style="left:60px;top:700px;width:960px;padding:60px 58px">'
            f'<div style="font-size:120px;line-height:.5;color:{p["accent"]};font-weight:800">&ldquo;</div>'
            f'<div style="font-size:72px;font-weight:800;line-height:1.08;margin-top:10px">{line}</div>'
            f'<div class="lab" style="margin-top:34px;font-size:30px">&mdash; {who}</div></div>')


def versus(p, plate, la, va, lb, vb):
    """E — two columns, the comparison the data actually is."""
    return (f'<img class="plate" src="{plate}" style="left:0;top:0;width:1080px;height:1920px;opacity:{p["plate_op"]}">'
            f'<div class="card" style="left:56px;top:620px;width:452px;height:560px;padding:48px">'
            f'<div class="lab" style="font-size:30px">{la}</div>'
            f'<div class="k" style="margin-top:24px;font-size:150px">{va}</div></div>'
            f'<div class="card" style="left:572px;top:620px;width:452px;height:560px;padding:48px;'
            f'border:5px solid {p["accent"]}">'
            f'<div class="lab" style="font-size:30px;color:{p["accent"]}">{lb}</div>'
            f'<div class="k acc" style="margin-top:24px;font-size:150px">{vb}</div></div>')


def band(p, plate, word):
    """F — a single word in a full-width band, footage above and below."""
    return (f'<img class="plate" src="{plate}" style="left:0;top:0;width:1080px;height:1920px;opacity:{p["plate_op"]}">'
            f'<div style="position:absolute;left:0;top:760px;width:1080px;height:330px;background:{p["accent"]}"></div>'
            f'<div class="k" style="position:absolute;left:0;top:800px;width:1080px;text-align:center;'
            f'font-size:190px;color:{p["ground"]}">{word}</div>')
