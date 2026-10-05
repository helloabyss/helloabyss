# -*- coding: utf-8 -*-
"""Reusable flat-line-art primitives. Every scene is composed from these."""
K='#000'; W='#fff'; R='#d81e28'; Y='#f2c200'; G='#2e9e3e'; B='#1f6fb8'; N='#8a5a2b'; D='#5b6670'
SW=8  # standard stroke

def t(x,y,s,size=40,anchor='middle',fill=K,weight=700):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}" font-family="Liberation Sans,Arial,sans-serif">{s}</text>'

def ground(y=950,x1=100,x2=1820):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{K}" stroke-width="9"/>'

def box(x,y,w,h,fill=W,sw=SW,rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{K}" stroke-width="{sw}"/>'

def zul(x,y,sc=1.0,arms=None):
    """arms: None, 'down', 'table' (reaching forward/down), 'up' (holding)"""
    a = {'down':'<line x1="-46" y1="112" x2="-74" y2="168" stroke="#000" stroke-width="7" stroke-linecap="round"/><line x1="46" y1="112" x2="74" y2="168" stroke="#000" stroke-width="7" stroke-linecap="round"/>',
         'table':'<line x1="-44" y1="110" x2="-104" y2="150" stroke="#000" stroke-width="7" stroke-linecap="round"/><line x1="44" y1="110" x2="104" y2="150" stroke="#000" stroke-width="7" stroke-linecap="round"/>',
         'up':'<line x1="-44" y1="110" x2="-92" y2="74" stroke="#000" stroke-width="7" stroke-linecap="round"/><line x1="44" y1="110" x2="92" y2="74" stroke="#000" stroke-width="7" stroke-linecap="round"/>',
         }.get(arms,'')
    return f'''<g transform="translate({x},{y}) scale({sc})">
  <circle cx="0" cy="0" r="46" fill="{W}" stroke="{K}" stroke-width="7"/>
  <g stroke="{K}" stroke-width="6" fill="none">
    <circle cx="-44" cy="-14" r="9"/><circle cx="-34" cy="-30" r="9"/><circle cx="-18" cy="-40" r="9"/>
    <circle cx="0" cy="-44" r="9"/><circle cx="18" cy="-40" r="9"/><circle cx="34" cy="-30" r="9"/><circle cx="44" cy="-14" r="9"/></g>
  <path d="M-50 -34 A 50 42 0 0 1 50 -34 Z" fill="{G}" stroke="{K}" stroke-width="7"/>
  <path d="M-47 -44 A 50 42 0 0 1 47 -44 Z" fill="{Y}" stroke="{K}" stroke-width="7"/>
  <path d="M-40 -56 A 50 42 0 0 1 40 -56 Z" fill="{R}" stroke="{K}" stroke-width="7"/>
  <g stroke="{K}" stroke-width="6" fill="none"><rect x="-36" y="-10" width="30" height="24" rx="4"/>
    <rect x="6" y="-10" width="30" height="24" rx="4"/><line x1="-6" y1="2" x2="6" y2="2"/></g>
  <circle cx="-21" cy="2" r="5" fill="{K}"/><circle cx="21" cy="2" r="5" fill="{K}"/>
  <line x1="-16" y1="28" x2="16" y2="28" stroke="{K}" stroke-width="7" stroke-linecap="round"/>
  <line x1="0" y1="46" x2="0" y2="92" stroke="{K}" stroke-width="7"/>
  <path d="M-52 168 L-40 96 L40 96 L52 168 Z" fill="{W}" stroke="{K}" stroke-width="7" stroke-linejoin="round"/>
  <path d="M-14 96 L0 112 L14 96" fill="none" stroke="{K}" stroke-width="6"/>{a}</g>'''

def fig(x,y,sc=1.0,mood='neutral',arms='down',legs=True):
    m={'neutral':'<line x1="-10" y1="14" x2="10" y2="14" stroke="#000" stroke-width="6" stroke-linecap="round"/>',
       'down':'<path d="M-11 18 Q0 8 11 18" fill="none" stroke="#000" stroke-width="6" stroke-linecap="round"/>',
       'flat':'<line x1="-10" y1="16" x2="10" y2="16" stroke="#000" stroke-width="6" stroke-linecap="round"/>'}[mood]
    A={'down':'<line x1="0" y1="52" x2="-34" y2="94" stroke="#000" stroke-width="7" stroke-linecap="round"/><line x1="0" y1="52" x2="34" y2="94" stroke="#000" stroke-width="7" stroke-linecap="round"/>',
       'fwd':'<line x1="0" y1="52" x2="-46" y2="70" stroke="#000" stroke-width="7" stroke-linecap="round"/><line x1="0" y1="52" x2="46" y2="70" stroke="#000" stroke-width="7" stroke-linecap="round"/>',
       'hold':'<line x1="0" y1="52" x2="-40" y2="40" stroke="#000" stroke-width="7" stroke-linecap="round"/><line x1="0" y1="52" x2="40" y2="40" stroke="#000" stroke-width="7" stroke-linecap="round"/>'}[arms]
    L='<line x1="0" y1="120" x2="-28" y2="182" stroke="#000" stroke-width="7" stroke-linecap="round"/><line x1="0" y1="120" x2="28" y2="182" stroke="#000" stroke-width="7" stroke-linecap="round"/>' if legs else ''
    return f'''<g transform="translate({x},{y}) scale({sc})">
  <circle cx="0" cy="0" r="30" fill="{W}" stroke="{K}" stroke-width="7"/>
  <circle cx="-11" cy="-4" r="4" fill="{K}"/><circle cx="11" cy="-4" r="4" fill="{K}"/>{m}
  <line x1="0" y1="30" x2="0" y2="120" stroke="{K}" stroke-width="7"/>{A}{L}</g>'''

def shop(x, y, lit, w=240, h=260, roof=True, boarded=False):
    win = Y if lit else D
    s = box(x, y, w, h)
    if boarded:
        s += box(x+24, y+42, w-48, 104, N)
        s += f'<line x1="{x+24}" y1="{y+70}" x2="{x+w-24}" y2="{y+70}" stroke="{K}" stroke-width="6"/>'
        s += f'<line x1="{x+24}" y1="{y+118}" x2="{x+w-24}" y2="{y+118}" stroke="{K}" stroke-width="6"/>'
    else:
        s += box(x+24, y+42, w-48, 104, win)
    s += box(x+w//2-38, y+h-92, 76, 92)
    if roof:
        s += f'<path d="M{x-16} {y} L{x+w//2} {y-70} L{x+w+16} {y} Z" fill="{N}" stroke="{K}" stroke-width="{SW}" stroke-linejoin="round"/>'
    return s

def axes(x0=300,y0=880,x1=1680,y1=240,xl='TIME',yl='INDEX'):
    return (f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{K}" stroke-width="9"/>'
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{K}" stroke-width="9"/>'
            + t(x0-34,y0+12,'0',30) + t((x0+x1)//2,y0+76,xl,34)
            + f'<g transform="rotate(-90 {x0-96} {(y0+y1)//2})">'+t(x0-96,(y0+y1)//2,yl,34)+'</g>')

def pile(x,y,n,col,w=140,hh=34):
    return ''.join(box(x,y-i*10,w,hh,col,6) for i in range(n))

def card(x,y,s,w=760,h=84,size=32):
    return box(x,y,w,h) + t(x+w//2, y+h//2+11, s, size)

def page(body,w=1920,h=1080):
    return ('<style>*{margin:0;padding:0}html,body{background:#fff}svg{display:block}</style>'
            f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="{w}" height="{h}" fill="{W}"/>{body}</svg>')

def hand(x, y, sc=1.0, flip=False):
    """Silhouette hand: paddle palm + separate thumb, no interior ruling.
    Interior detail is what fails at this line weight; silhouette reads."""
    f = -1 if flip else 1
    return (f'<g transform="translate({x},{y}) scale({sc*f},{sc})">'
            f'<path d="M-62 -58 Q-14 -76 36 -58 Q62 -48 62 -8 L62 34'
            f' Q62 76 14 76 L-24 76 Q-62 76 -62 36 Z"'
            f' fill="{W}" stroke="{K}" stroke-width="9" stroke-linejoin="round"/>'
            f'<path d="M-62 -14 Q-96 -6 -94 26 Q-92 56 -62 56"'
            f' fill="{W}" stroke="{K}" stroke-width="9"/>'
            f'<line x1="-6" y1="-66" x2="-6" y2="-14" stroke="{K}" stroke-width="6"/>'
            f'<line x1="30" y1="-62" x2="30" y2="-14" stroke="{K}" stroke-width="6"/></g>')

def piggy(x, y, sc=1.0, cracked=True):
    c = (f'<path d="M{-40} {-96} L{-8} {10} L{-56} {96}" fill="none" stroke="{K}" stroke-width="8"/>'
         f'<rect x="-74" y="-66" width="104" height="38" fill="{Y}" stroke="{K}" stroke-width="7" transform="rotate(-20 -22 -47)"/>'
         f'<rect x="-86" y="34" width="104" height="38" fill="{Y}" stroke="{K}" stroke-width="7" transform="rotate(22 -34 53)"/>') if cracked else ''
    return (f'<g transform="translate({x},{y}) scale({sc})">'
            f'<ellipse cx="0" cy="0" rx="210" ry="140" fill="{R}" stroke="{K}" stroke-width="10"/>'
            f'<ellipse cx="196" cy="14" rx="62" ry="52" fill="{R}" stroke="{K}" stroke-width="10"/>'
            f'<circle cx="214" cy="4" r="9" fill="{K}"/><circle cx="238" cy="18" r="9" fill="{K}"/>'
            f'<path d="M60 -120 L104 -142 L116 -92 Z" fill="{R}" stroke="{K}" stroke-width="9" stroke-linejoin="round"/>'
            f'<circle cx="92" cy="-36" r="11" fill="{K}"/>'
            f'<rect x="-70" y="-132" width="140" height="22" rx="11" fill="{K}"/>'
            ''.join(f'<rect x="{-150+i*96}" y="118" width="52" height="56" rx="10" fill="{R}" stroke="{K}" stroke-width="9"/>' for i in range(4))
            + c + '</g>')

def counter(x, y, w, h=34, legs=True):
    s = box(x, y, w, h, N)
    if legs:
        s += (f'<line x1="{x+40}" y1="{y+h}" x2="{x+40}" y2="950" stroke="{K}" stroke-width="8"/>'
              f'<line x1="{x+w-40}" y1="{y+h}" x2="{x+w-40}" y2="950" stroke="{K}" stroke-width="8"/>')
    return s
