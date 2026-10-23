# -*- coding: utf-8 -*-
"""Thumbnail for the AI-picks long-form. Zero credits, deterministic, same palette
as the video so the channel reads as one series.

The claim on it is the hook, which is the most surprising true thing in the fact
table and is also the title: SpaceX burned $14.0bn of cash in 2025 and the market
valued it at ~$2.1tn on day one. Both CONFIRMED in FACTS.md. No clickbait phrasing,
no arrows, no shock face -- the contradiction is the hook.
"""
import base64, io, json

W, H = 1280, 720
K, R, GREY, PAPER = '#111314', '#d81e28', '#8a9199', '#ffffff'
M = json.load(open('art/poses/manifest.json'))

def pose(pset, name, h, x, y):
    m = M[pset]['poses'][name]
    b = base64.b64encode(open('art/poses/' + m['file'], 'rb').read()).decode()
    w = h * m['w'] / float(m['h'])
    return (f'<img src="data:image/png;base64,{b}" style="position:absolute;'
            f'left:{x}px;top:{y}px;width:{w:.0f}px;height:{h}px">')

# Zul bust: the face is far bigger than on a full body, which is what survives
# being shown at 168px wide in a sidebar.
ZH, ZX, ZY = 630, -132, 56
TX = 404   # type column, clear of his ink (ink ends ~x=340 at this scale)

html = f'''<!doctype html><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;background:{PAPER};overflow:hidden;
  font-family:Liberation Sans,Arial,sans-serif;color:{K}}}
div{{position:absolute;white-space:nowrap}}
.n{{font-weight:700;letter-spacing:-5px;font-size:146px;line-height:1}}
.l{{font-weight:700;font-size:30px;letter-spacing:4px;color:{GREY}}}
.rule{{background:{R}}}
.tag{{font-weight:700;font-size:33px;letter-spacing:6px;color:{K}}}
.tag b{{color:{R}}}
</style>
{pose('glasses','skeptical',ZH,ZX,ZY)}
<div class="l" style="left:{TX}px;top:84px">SPACEX BURNED, 2025</div>
<div class="n" style="left:{TX}px;top:124px;color:{R}">&minus;$14.0BN</div>
<div class="rule" style="left:{TX}px;top:318px;width:800px;height:8px"></div>
<div class="l" style="left:{TX}px;top:368px">MARKET SAYS IT&rsquo;S WORTH</div>
<div class="n" style="left:{TX}px;top:408px">$2.1TN</div>
<div class="tag" style="left:{TX}px;top:606px"><b>SPCX</b> &middot; <b>BE</b> &middot; <b>MU</b></div>
'''
io.open('thumb.html', 'w', encoding='utf-8').write(html)
print('thumb.html written')
