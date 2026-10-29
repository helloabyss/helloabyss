# -*- coding: utf-8 -*-
"""PARADOCS10X long-form: setting up agentic trading on Robinhood.

Narration lines are READ FROM the script rather than retyped here, so the picture
and the voiceover cannot drift apart. One scene per paragraph of VO-FINAL.txt; the
build asserts the counts match.
"""
import io, re
from prims import *

VO = '../robinhood-agent-longform/VO-FINAL.txt'
LINES = [p.strip().replace('\n', ' ')
         for p in re.split(r'\n\s*\n', io.open(VO, encoding='utf-8').read()) if p.strip()]

CARD = card(140, 980, 'EDUCATIONAL ONLY.  NOT FINANCIAL ADVICE.', 860, 80, 34)

def head(s, y=150, size=58):
    return t(960, y, s, size)

C = []   # compositions, one per VO paragraph

# 1 — cold open: the three facts, stated flat
C.append(zul(330, 430, 1.25, arms='present', mood='neutral')
         + panel(740, 250, 1040, [('Reads every account you own', '', True),
                                  ('Trades in one of them', '', True),
                                  ('Robinhood does not supervise it', '', False)],
                 'AN AI IN YOUR BROKERAGE')
         + CARD)

# 2 — what it is: you out of the loop, agent in
C.append(phone(260, 230) + t(440, 980, 'YOU', 38)
         + arrow(660, 560, 880, 560, D)
         + box(900, 440, 420, 240, W, 8, 16) + t(1110, 540, 'AGENT', 46)
         + t(1110, 610, 'MCP SERVER', 30, fill=D)
         + arrow(1340, 560, 1560, 560, R)
         + box(1580, 440, 240, 240, W, 8, 16) + t(1700, 580, 'ORDER', 36, fill=R))

# 3 — not a bot: a connection, not a strategy
C.append(head('IT IS NOT A BOT. IT IS A CONNECTION.')
         + box(240, 320, 620, 380, W, 8, 16) + t(550, 420, 'TRADING BOT', 44)
         + t(550, 500, 'strategy baked in', 34, fill=D) + t(550, 580, 'does one thing', 34, fill=D)
         + xmark(550, 650)
         + box(1060, 320, 620, 380, W, 8, 16) + t(1370, 420, 'AN AGENT', 44, fill=R)
         + t(1370, 500, 'decides for itself', 34, fill=D)
         + t(1370, 580, 'inside your account', 34, fill=D))

# 4 — beta scope
C.append(panel(400, 300, 1120, [('Stocks — at beta launch', 'YES', True),
                                ('Options, supported crypto', 'LATER', True),
                                ('Margin borrowing', 'NOT ENABLED', False)],
               'WHAT IT CAN TRADE')
         + t(960, 800, 'Rollout moved during the beta. Check your own account.', 32, fill=D))

# 5 — step one: name it
C.append(zul(330, 430, 1.25, arms='point', mood='neutral')
         + t(1180, 240, 'STEP 1', 44, fill=R)
         + panel(740, 300, 1040, [('Agent name', 'REQUIRED', True)], 'NAME THE AGENT')
         + t(1260, 640, 'It is how that agent’s orders are', 34, fill=D)
         + t(1260, 690, 'identified later. Name it anyway.', 34, fill=D))

# 6 — step two: a separate account
C.append(t(960, 150, 'STEP 2', 44, fill=R) + head('OPEN A DEDICATED ACCOUNT', 230, 58)
         + acctbox(300, 340, 560, 300, 'YOUR MAIN ACCOUNT', 'NOT THIS ONE')
         + acctbox(1060, 340, 560, 300, 'AGENTIC ACCOUNT', 'THIS ONE', True)
         + t(960, 760, 'The real safety boundary of the whole system.', 36))

# 7 — the boundary, precisely
C.append(head('WHAT A CONNECTED AGENT CAN REACH', 150, 44)
         + acctbox(170, 260, 500, 250, 'MAIN', 'READ')
         + acctbox(710, 260, 500, 250, 'RETIREMENT', 'READ')
         + acctbox(1250, 260, 500, 250, 'AGENTIC', 'READ + TRADE', True)
         + t(960, 640, 'It caps what the agent can TRADE.', 46)
         + t(960, 710, 'Not what the agent can SEE.', 46, fill=R))

# 8 — funding it
C.append(zul(380, 420, 1.2, arms='down', mood='wry')
         + piggy(1250, 560, 1.5)
         + t(1250, 300, 'FUND IT WITH WHAT YOU', 42)
         + t(1250, 360, 'COULD LOSE OUTRIGHT', 42, fill=R)
         + t(1250, 860, 'Ring-fencing the money does not', 32, fill=D)
         + t(1250, 905, 'ring-fence the information.', 32, fill=D))

# 9 — step three: connect the model
C.append(t(960, 150, 'STEP 3', 44, fill=R) + head('CONNECT THE MODEL', 230, 58)
         + box(260, 360, 480, 260, W, 8, 16) + t(500, 460, 'IN-APP AGENT', 40)
         + t(500, 530, 'Robinhood’s own', 32, fill=D)
         + box(1180, 360, 480, 260, W, 8, 16) + t(1420, 460, 'OUTSIDE AGENT', 40, fill=R)
         + t(1420, 530, 'via the MCP server', 32, fill=D)
         + t(960, 800, 'The difference is who wrote the thing deciding.', 36))

# 10 — approvals ON
C.append(panel(400, 320, 1120, [('Trade approvals', 'ON', True)], 'AGENT SETTINGS')
         + tick(560, 700) + t(960, 715, 'It proposes. You place the order.', 44, anchor='middle')
         + CARD)

# 11 — approvals OFF
C.append(panel(400, 320, 1120, [('Trade approvals', 'OFF', False)], 'AGENT SETTINGS')
         + xmark(560, 700) + t(980, 715, 'It decides. The order goes.', 44)
         + t(960, 850, 'Nothing between the model and your money.', 34, fill=R))

# 12 — sources disagree
C.append(head('SOURCES DISAGREE', 160, 44)
         + box(200, 250, 680, 300, W, 8, 16)
         + t(540, 350, 'One report:', 34, fill=D) + t(540, 420, 'OFF by default', 44)
         + t(540, 480, 'for outside agents', 32, fill=D)
         + t(960, 420, '?', 120, fill=R)
         + box(1040, 250, 680, 300, W, 8, 16)
         + t(1380, 350, 'Another:', 34, fill=D) + t(1380, 420, 'confirmation', 44)
         + t(1380, 480, 'described as optional', 32, fill=D)
         + t(960, 680, 'So this video will not tell you what your default is.', 40))

# 13 — could not open the docs
C.append(zul(420, 430, 1.3, arms='shrug', mood='wry')
         + t(1260, 380, 'I could not open', 48)
         + t(1260, 450, 'Robinhood’s own docs', 48)
         + t(1260, 520, 'to settle it.', 48)
         + t(1260, 650, 'So I am not going to guess at it', 34, fill=D)
         + t(1260, 700, 'and neither should a thumbnail.', 34, fill=D))

# 14 — go and look
C.append(panel(400, 300, 1120, [('Trade approvals', 'CHECK IT', False)], 'AGENT SETTINGS')
         + arrow(1150, 700, 1290, 530, R, 11)
         + t(960, 800, 'A default you have not verified is not a setting.', 44)
         + t(960, 870, 'It is a guess you are funding.', 44, fill=R))

# 15 — the disclaimer
C.append(box(220, 260, 1480, 420, W, 8, 20)
         + t(960, 370, '“Does not control, supervise,', 54)
         + t(960, 450, 'monitor, recommend or audit', 54)
         + t(960, 530, 'third-party agents.”', 54)
         + t(960, 620, 'Robinhood’s own wording, as reported', 30, fill=D)
         + CARD)

# 16 — no vetting layer
C.append(box(220, 400, 420, 240, W, 8, 16) + t(430, 540, 'ROBINHOOD', 40)
         + arrow(660, 520, 840, 520, D)
         + box(860, 400, 200, 240, W, 8, 16) + xmark(960, 520, 48)
         + t(960, 720, 'NO VETTING LAYER', 36, fill=R)
         + arrow(1080, 520, 1260, 520, D)
         + box(1280, 400, 420, 240, W, 8, 16) + t(1490, 540, 'YOUR AGENT', 40, fill=R)
         + t(960, 880, 'Connect something bad and the loss is yours.', 36))

# 17 — not a scandal
C.append(zul(380, 430, 1.25, arms='present', mood='neutral')
         + t(1260, 360, 'That is not a scandal.', 52)
         + t(1260, 440, 'It is stated up front.', 52)
         + t(1260, 580, 'But it inverts what people expect', 36, fill=D)
         + t(1260, 635, 'of a regulated brokerage:', 36, fill=D)
         + t(1260, 740, 'that somebody is checking.', 44, fill=R)
         + t(1260, 820, 'For this feature, nobody is.', 44, fill=R))

# 18 — checklist, first two
C.append(head('BEFORE THE FIRST SESSION', 170, 50)
         + box(300, 280, 90, 90, W, 7, 10) + t(345, 345, '1', 50, fill=R)
         + t(440, 325, 'Fund it with money you could lose', 42, anchor='start')
         + t(440, 385, 'outright — not money you need', 34, anchor='start', fill=D)
         + box(300, 480, 90, 90, W, 7, 10) + t(345, 545, '2', 50, fill=R)
         + t(440, 525, 'Confirm the approvals toggle', 42, anchor='start')
         + t(440, 585, 'with your own eyes', 34, anchor='start', fill=D)
         + CARD)

# 19 — checklist, last two
C.append(head('BEFORE THE FIRST SESSION', 170, 50)
         + box(300, 280, 90, 90, W, 7, 10) + t(345, 345, '3', 50, fill=R)
         + t(440, 325, 'Know what it is allowed to trade', 42, anchor='start')
         + t(440, 385, 'the list moved during the beta', 34, anchor='start', fill=D)
         + box(300, 480, 90, 90, W, 7, 10) + t(345, 545, '4', 50, fill=R)
         + t(440, 525, 'Know how you disconnect it', 42, anchor='start')
         + t(440, 585, 'and how fast you can do it', 34, anchor='start', fill=D)
         + CARD)

# 20 — close
C.append(zul(400, 430, 1.3, arms='point', mood='neutral')
         + panel(880, 330, 900, [('Trade approvals', '?', False)], 'ONE TOGGLE')
         + t(1330, 700, 'Go and look at the toggle.', 52, fill=R)
         + CARD)

assert len(C) == len(LINES), 'picture has %d scenes, script has %d paragraphs' % (len(C), len(LINES))
S = [(i + 1, LINES[i], C[i]) for i in range(len(C))]
