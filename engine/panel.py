# -*- coding: utf-8 -*-
"""Data panels — the capability the benchmark short has and we did not.

Their edge is not pace. It is that a figure arrives as a *dated, labelled,
sourced chart* instead of a big percentage. A reviewer on our own desk read a
set of numbers and attached them to the wrong series; a viewer at thirty
seconds has no chance. So the panel is the honest form, not the decorative one.

Palette is tokenised. The channel is locked to near-black / white / one red,
and the benchmark uses gold — that choice is the owner's, so switching is one
line here and nothing else moves.
"""
INK   = '#0b0d10'   # panel ground
EDGE  = '#9aa3ad'   # panel border
TEXT  = '#ffffff'
MUTE  = '#8d97a3'
UP    = '#ffffff'   # positive series
DOWN  = '#d81e28'   # negative series — the one red accent
GRID  = '#222831'
ACCENT = EDGE       # set to '#d8a62a' to take the benchmark's gold


def _esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def panel(x, y, w, h, label, rows, source=None, kind='candle',
          baseline=None, accent=None):
    """One data card.

    rows   candle: [(date, open, high, low, close), ...]
           line:   [(date, value), ...]
    label  series name, e.g. 'MU · 10 days'
    source printed under the panel, e.g. 'Oct 19 close · Webull'. A panel with
           no source is a panel we cannot stand behind, so it is drawn in red
           as a build-time warning rather than silently omitted.
    """
    a = accent or ACCENT
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{INK}" '
         f'fill-opacity="0.82" stroke="{a}" stroke-width="3"/>']
    pad_l, pad_t, pad_b = 54, 52, 44
    px, py = x + pad_l, y + pad_t
    pw, ph = w - pad_l - 26, h - pad_t - pad_b

    o.append(f'<text x="{x+22}" y="{y+34}" font-size="26" fill="{TEXT}" font-weight="700" '
             f'font-family="Liberation Mono,monospace">{_esc(label)}</text>')
    o.append(f'<text x="{x+w-18}" y="{y+34}" font-size="19" text-anchor="end" '
             f'fill="{MUTE if source else DOWN}" font-family="Liberation Mono,monospace">'
             f'{_esc(source) if source else "UNSOURCED"}</text>')

    if kind == 'candle':
        vals = [v for r in rows for v in r[1:5]]
    else:
        vals = [r[1] for r in rows]
    lo, hi = min(vals), max(vals)
    if baseline is not None:
        lo, hi = min(lo, baseline), max(hi, baseline)
    if hi == lo:
        hi, lo = hi + 1, lo - 1
    pad = (hi - lo) * 0.14
    lo, hi = lo - pad, hi + pad
    sy = lambda v: py + ph - (v - lo) / (hi - lo) * ph

    for i in range(4):
        gy = py + ph * i / 3.0
        o.append(f'<line x1="{px}" y1="{gy:.1f}" x2="{px+pw}" y2="{gy:.1f}" '
                 f'stroke="{GRID}" stroke-width="2"/>')
    if baseline is not None:
        o.append(f'<line x1="{px}" y1="{sy(baseline):.1f}" x2="{px+pw}" y2="{sy(baseline):.1f}" '
                 f'stroke="{MUTE}" stroke-width="2" stroke-dasharray="7 6"/>')

    n = len(rows)
    step = pw / max(1, n)
    if kind == 'candle':
        bw = min(26.0, step * 0.56)
        for i, (d, op, hg, lw, cl) in enumerate(rows):
            cx = px + step * (i + 0.5)
            col = UP if cl >= op else DOWN
            o.append(f'<line x1="{cx:.1f}" y1="{sy(hg):.1f}" x2="{cx:.1f}" y2="{sy(lw):.1f}" '
                     f'stroke="{col}" stroke-width="3"/>')
            top, bot = sy(max(op, cl)), sy(min(op, cl))
            o.append(f'<rect x="{cx-bw/2:.1f}" y="{top:.1f}" width="{bw:.1f}" '
                     f'height="{max(3.0, bot-top):.1f}" fill="{col}"/>')
    else:
        pts = ' '.join(f'{px + step*(i+0.5):.1f},{sy(v):.1f}' for i, (d, v) in enumerate(rows))
        col = DOWN if rows[-1][1] < rows[0][1] else UP
        o.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="5" '
                 f'stroke-linejoin="round" stroke-linecap="round"/>')
        lx, lv = rows[-1]
        o.append(f'<circle cx="{px + step*(n-0.5):.1f}" cy="{sy(lv):.1f}" r="7" fill="{col}"/>')

    # Dated axis. An undated chart is a shape, not evidence.
    for i in (0, n - 1):
        if n:
            o.append(f'<text x="{px + step*(i+0.5):.1f}" y="{y+h-18}" font-size="19" '
                     f'fill="{MUTE}" text-anchor="middle" '
                     f'font-family="Liberation Mono,monospace">{_esc(rows[i][0])}</text>')
    o.append(f'<text x="{px-10}" y="{py+6}" font-size="18" fill="{MUTE}" text-anchor="end" '
             f'font-family="Liberation Mono,monospace">{hi:.0f}</text>')
    o.append(f'<text x="{px-10}" y="{py+ph}" font-size="18" fill="{MUTE}" text-anchor="end" '
             f'font-family="Liberation Mono,monospace">{lo:.0f}</text>')

    return ''.join(o)


def source_strip(x, y, w, text, grade=None):
    """Persistent on-frame sourcing. The benchmark prints this; we buried it in
    the description. `grade` carries our own confidence, which they cannot
    match because they do not grade their claims."""
    g = f'  ·  {grade}' if grade else ''
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="40" fill="{INK}" fill-opacity="0.72"/>'
            f'<rect x="{x}" y="{y}" width="5" height="40" fill="{DOWN}"/>'
            f'<text x="{x+18}" y="{y+27}" font-size="21" fill="{TEXT}" font-weight="700" '
            f'letter-spacing="1.5" font-family="Liberation Mono,monospace">'
            f'{_esc(text + g)}</text></g>')
