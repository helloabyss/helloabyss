# -*- coding: utf-8 -*-
"""PARADOCS10X short 5 — "82% / 25%". Portrait 9:16.

The VO lines are read out of ../paradocs-short-5/VO-FINAL.txt rather than
retyped here. Picture and script then cannot drift apart, which is how the
long-form lost sync the first time.
"""
import io, os
from prims import K, W, R, t, box
from zul import zul

SIZE = (1080, 1920)
CW = 1080

# YouTube Shorts overlays the bottom ~250px and the right edge. Everything
# that must be read lives inside this band.
SAFE_TOP, SAFE_BOT = 150, 1520

VOF = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', 'paradocs-short-5', 'VO-FINAL.txt')
LINES = [p.strip() for p in io.open(VOF, encoding='utf-8').read().split('\n\n') if p.strip()]


def hero(y, s, size=300, fill=K):
    return t(CW // 2, y, s, size, fill=fill, weight=800)


def label(y, s, size=46, fill=K):
    return t(CW // 2, y, s, size, fill=fill)


def rule(y, w=560, col=K, sw=9):
    return (f'<line x1="{CW//2-w//2}" y1="{y}" x2="{CW//2+w//2}" y2="{y}" '
            f'stroke="{col}" stroke-width="{sw}"/>')


def bar(x, y, w, h, fill=W, sw=8):
    return box(x, y, w, h, fill, sw)


C = []

# 1 — the benchmark score. The claim as the industry states it.
C.append(
    label(330, 'TERMINAL-BENCH', 52)
    + rule(372, 420)
    + hero(640, '82%', 330)
    + label(730, 'CODING BENCHMARK', 44)
    + zul(250, 975, 0.95, arms='point', view='three_quarter', mood='wry', legs=True)
    + box(560, 930, 420, 150, W, 8)
    + t(770, 995, 'PASSED', 62, weight=800)
    + t(770, 1050, 'THE TEST', 44)
)

# 2 — the same agent, real work. Red is the channel's one accent; it lands here.
C.append(
    label(300, 'SAME AGENT — REAL WORK', 50)
    + rule(342, 560)
    + t(300, 560, '82%', 150, fill='#c9c9c9', weight=800)
    + t(300, 620, 'BENCHMARK', 36, fill='#c9c9c9')
    + t(540, 600, '→', 90)
    + t(790, 600, '25%', 190, fill=R, weight=800)
    + t(790, 672, 'REAL WORK', 40, fill=R)
    + rule(820, 700)
    + label(930, "BERKELEY'S AGENTS' LAST EXAM", 46)
    + bar(170, 1030, 740, 300, W, 9)
    + t(540, 1150, 'A 57-POINT DROP', 74, weight=800)
    + t(540, 1240, 'ON THE SAME MODEL', 46)
)

# 3 — what the benchmark actually is. 1,400 squares would not read; 140 do,
# tagged with the real figure rather than implying one square per task.
grid = ''.join(
    box(150 + (i % 20) * 39, 760 + (i // 20) * 39, 30, 30, W, 4)
    for i in range(140))
C.append(
    label(250, "AGENTS' LAST EXAM", 66)
    + rule(298, 620)
    + t(540, 500, '1,400+', 180, weight=800)
    + label(600, 'REAL TASKS', 48)
    + label(672, 'from 300 working professionals', 42)
    + label(726, '1,490 instances \u00b7 960 workflows \u00b7 55 fields', 34)
    + grid
    + t(540, 1100, 'UC BERKELEY RDI · SNORKEL AI', 36)
    + zul(880, 1180, 0.8, arms='down', view='front', mood='neutral')
)

# 4 — the grading method is the benchmark's whole claim to realism.
C.append(
    label(290, 'HOW IT IS GRADED', 52)
    + rule(332, 480)
    + bar(110, 420, 380, 500)
    + t(300, 490, 'HUMAN', 54, weight=800)
    + ''.join(f'<line x1="150" y1="{560+i*52}" x2="450" y2="{560+i*52}" stroke="{K}" stroke-width="7"/>'
              for i in range(6))
    + bar(590, 420, 380, 500)
    + t(780, 490, 'AGENT', 54, weight=800)
    + ''.join(f'<line x1="630" y1="{560+i*52}" x2="{930 if i%2 else 820}" y2="{560+i*52}" stroke="{K}" stroke-width="7"/>'
              for i in range(6))
    + t(540, 1020, 'GRADED AGAINST', 50)
    + t(540, 1090, "THE EXPERT'S OWN", 62, weight=800)
    + t(540, 1160, 'DELIVERABLE', 62, weight=800)
    + rule(1210, 560, R)
    + t(540, 1290, 'Deterministic scripts. No partial credit.', 38)
)

# 5 — the hardest tier. The number is the shot.
C.append(
    label(330, 'THE HARDEST TIER', 54, R)
    + rule(374, 480, R)
    + hero(720, '0.0%', 360, R)
    + rule(800, 700)
    + t(540, 920, 'THE LEADING AGENTS', 54)
    + t(540, 1000, 'SCORED NOTHING', 66, weight=800)
    + zul(540, 1120, 0.95, arms='shrug', view='front', mood='worried')
)

# 6 — the payoff. Why it fails is more interesting than that it fails.
C.append(
    label(300, 'WHY THEY FAIL', 54)
    + rule(342, 420)
    + bar(110, 430, 860, 130, R, 9)
    + t(540, 515, "DIDN'T KNOW THE JOB", 58, fill=W, weight=800)
    + t(540, 615, '~75% of failures', 48, fill=R)
    + bar(110, 700, 290, 130, W, 9)
    + t(255, 785, 'TOOLS', 54, weight=800)
    + t(255, 880, 'the rest', 44)
    + rule(960, 700)
    + t(540, 1080, 'The tools worked.', 58)
    + t(540, 1170, 'It did not know', 66, weight=800)
    + t(540, 1250, 'the work.', 66, weight=800)
)

# 7 — the mandatory counter-evidence. Same weight of frame as the thesis.
_pts = [(200, 1120, 'JUN', '24%'), (540, 950, 'AUG', '38%'), (880, 680, 'OCT', '59%')]
_line = ('<polyline points="200,1120 540,950 880,680" fill="none" '
         f'stroke="{R}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>')
C.append(
    label(290, 'BUT — THE OTHER SIDE', 54)
    + rule(332, 520)
    + f'<line x1="140" y1="1240" x2="960" y2="1240" stroke="{K}" stroke-width="9"/>'
    + _line
    + ''.join(f'<circle cx="{x}" cy="{y}" r="22" fill="{W}" stroke="{K}" stroke-width="9"/>'
              + t(x, y - 50, v, 64, weight=800) + t(x, 1300, m, 44)
              for x, y, m, v in _pts)
    + t(540, 480, 'SCORES ARE CLIMBING', 56, weight=800)
    + t(540, 550, 'FAST', 80, fill=R, weight=800)
    + t(540, 1380, 'Different boards, different scoring.', 34)
)

# 8 — close on the gap, not on a CTA. House rule: no subscribe animation.
C.append(
    bar(130, 400, 360, 180, W, 9)
    + t(310, 500, '82%', 110, weight=800)
    + t(310, 560, 'BENCHMARK', 34)
    + bar(590, 400, 360, 180, W, 9)
    + t(770, 500, '25%', 110, fill=R, weight=800)
    + t(770, 560, 'REAL WORK', 34, fill=R)
    + t(540, 720, 'THE GAP IS REAL', 70, weight=800)
    + t(540, 820, 'AND IT IS CLOSING', 62, fill=R, weight=800)
    + rule(880, 620)
    + zul(540, 1010, 0.72, arms='down', view='front', mood='wry', legs=True)
    + t(540, 1380, 'PARADOCS 10X', 56, weight=800)
)

assert len(C) == len(LINES), '%d compositions for %d VO paragraphs' % (len(C), len(LINES))
S = [(i + 1, LINES[i], C[i]) for i in range(len(C))]
