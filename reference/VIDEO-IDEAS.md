# Video ideas — 2026-10-25

Six ideas. Four for **The Meticulous Investor** (the channel the owner's benchmark short is
aimed at), two for **PARADOCS10X**. Nothing here is scripted, sourced or rendered, and no
generation credit was spent producing it.

Desk traffic behind every line is in `reference/AGENT-LOG.md`.

**Built to one shape**, the only one with evidence behind it on these channels — *a named
thing, one hard number, and the cost that number hides* — and to the benchmark measured in
`reference/GROK-BOT-TEARDOWN.md`: **real B-roll as the base layer**, data **charted on dated
panels rather than announced**, sourcing **printed on the frame**, evidence shown **two-sided
as a card pair**, and Zul as a **small persistent corner host at ~15% frame height, re-posed
per shot, never the subject**.

---

## A standing honesty note — read before costing any of these

**Nothing below can be graded CONFIRMED, and nothing will be.** Verified again today:
`WebFetch` returns `getaddrinfo ENOTFOUND` for primary sources. Only server-side web search
works. Every figure here is **corroborated secondary reporting**, and each block says which
ones rest on a single source.

Three specific limits, and they are in the blocks because they change what can be said:

- **No market price can be re-verified from here.** No idea below uses one. That is a
  filter that was applied, not a coincidence.
- **No live rate or yield can go on screen** (M1).
- **Two ideas rest entirely on a figure the publishing party chose, compiled and audited
  itself** (P1, P2), and the attribution must sit in the sentence carrying the number, not in
  the description.

---

# The Meticulous Investor

All four: **Zul appears** as a small corner host per the teardown. He is furniture, not the
scene, and he is **not in any thumbnail** — at 320px he would be unreadable. Built by
`engine/zul.py`, never drawn by hand (`CHARACTER-ZUL.md`).

---

## M1 — The daily reset

**Working title:** `Flat Index, 3x Fund Down 1.6%: The Daily Reset` (47 chars)

**Hard number:** the index ends **exactly flat**; the 3x fund ends **1.6% down**.
**The cost it hides:** "3x" is three times the *daily move*, never three times the *return*.
The reset is a cost you pay for holding, and nobody quotes it.

Worked example, illustrative, labelled on-frame as not any real fund:

```
index   0.95 × (1 / 0.95)         = 1.000000   exactly flat
3x fund 0.85 × (1 + 3 × 0.052632) = 0.984211   −1.58%
```

**Checkable from here?** **This is the only one of the six whose hard number we do not have
to source — we derive it.** The arithmetic was recomputed in-session and is reproducible by
anyone with a calculator. The *mechanism* is graded **HIGH** against the SEC investor
bulletin, FINRA Notice 09-31 and an SLCG paper; none was opened and the exact wording of all
three is **not established**, so none may be quoted. Nothing needs to be quoted — the maths
is the claim.

**Not checkable, and therefore excluded:** any real fund's tracking history, any fee or
borrowing cost, any ticker. The markets desk refuses all three and I am not appealing.

**Counter-evidence beat:** decay is **path-dependent, not a law**. In a steady trend,
compounding runs the other way and a 3x fund can *beat* 3x the index's return. The video must
never say "they always decay." Shown as a card pair, benchmark-style: `choppy → you lose` /
`trending → you gain`.

**Runtime:** 30–34s. **Zul:** yes, corner host.

**Hook:** *"The index is flat. The 3x fund is down 1.6%."*
**social-packager: PASSED** — "the strongest hook of the six. It is a paradox, it needs no
setup, and it works unchanged as the title." Conditions attached: `Illustrative · not a real
fund` on frame; compliance as a **bottom strip** in the first 4s, not a full card ahead of the
hook; and because 1.6% sounds small, beat two must show the swing repeating and the gap
widening — **computed before scripting, never asserted from memory**.

**First frame, silent:** two stacked panels — index `100 → 100` in white, fund `100 → 98.4`
in red. The benchmark's two-panel layout exactly.
**Thumbnail:** `INDEX 100 → 100` over `3x FUND 100 → 98.4`, with 98.4 in red.

**Confidence: high.** **What kills it:** nothing external — the maths cannot rot and there is
no counterparty to contradict us. The only failure mode is internal: if the two series are
*announced* instead of *charted as two labelled panels*, viewers will attach the numbers to
the wrong series. We know this because a senior reviewer did exactly that this session
(`AGENT-LOG.md` §2, Disagreement 2). **Charted panels are a build requirement, not a style
preference.**

---

## M2 — The brokerage cash sweep

**Working title:** `Cash Sweep: $250,000 Per Bank, and SIPC Doesn't Apply` (53 chars)

**Hard number:** **$250,000** per bank.
**The cost it hides:** your idle cash is not *at* the brokerage. It has been swept out to
partner banks, so FDIC rules apply and **SIPC does not** — and the rate on it comes from a
contract between your broker and those banks that you are not a party to.

**Checkable from here?** Structure graded **HIGH**, anchored on the SEC investor bulletin,
but the corroboration is mostly **broker documentation**, which is a weak form of
independence — flagged, not hidden.

**NOT CHECKABLE, and this one shapes the whole video:** **no sweep rate and no money-market
yield may appear anywhere.** The markets desk refuses it outright — unverifiable from here
and stale within days. Also not checkable: any broker's current program-bank list (it
changes, so no bank is named) and whether any named broker's default is opt-out today.

This is why the hard number is the **insurance limit**, not the yield. The desk's own ranking
argued for leading on yield and then banned every yield figure in the same memo; I overruled
the lead and kept the ban (`AGENT-LOG.md` §2, Disagreement 1). The yield point survives as
beat two, reframed from *what the rate is* to **who sets it** — true regardless of where rates
go, and needing no figure.

**Counter-evidence beat, two-sided card pair:** multi-bank networks raise the cap well past
$250,000, so most viewers never reach it — and **many brokers sweep to money market funds
instead, which SIPC does cover**, so the claim does not generalise to every account. The
packager caught that second one and it is the honest half of the video.

One grading note to carry into `FACTS.md`: *"the rate is not set by competition for your
deposit"* is an **inference**, and must be graded as analysis, not as reported fact.

**Runtime:** 32–36s. **Zul:** yes, corner host.

**Hook:** *"Your cash isn't at your brokerage. It's at banks your brokerage picked."*
**social-packager: REWRITTEN.** My draft was *"a bank you never chose"* — vetoed as
**arguable**, because the customer enrolled in the program, and as over-generalising to every
broker. Rewrite accepted. Condition: `If your cash sweeps to a bank program` on frame.

**First frame, silent:** a plain-text brokerage name-tag, a cash block sliding out to three
plain-text bank name-tags. No logos (`STYLE-GUIDE.md` §4).
**Thumbnail:** `$250,000 PER BANK` white, `SIPC: NOT HERE` red.

**Confidence: medium-high.** **What kills it:** if re-checking shows the money-market-sweep
default is now the industry norm rather than the exception, the premise inverts and the video
becomes a correction of itself. Gate that before scripting.
**Close:** "find your sweep program's disclosure and read the bank list yourself" — actionable,
and not a call, per `DISCLAIMER.md`.

---

## M3 — The $150,000 Roth catch-up

**Working title:** `401(k) Catch-Up: Over $150,000, It Goes In as Roth` (49 chars)

**Hard number:** **$150,000** in prior-year FICA wages.
**The cost it hides:** if you are 50+ and over it, your catch-up contribution **must** go in
as Roth — the pre-tax deduction on that slice disappears.

**Checkable from here?** **HIGH**, and *better* than the researcher brought it. The markets
desk corrected the threshold from $145,000 to **$150,000** (IRS Notice 2025-67 indexed it up)
and closed the effective-date conflict: effective 2026, good-faith compliance through 2026,
strict enforcement from 2027. Rule itself is HIGH across four law and benefits firms.

**The number must never be presented as "income."** It is **2025 FICA wages, W-2 box 3,
sponsoring employer only** — that qualifier goes on the frame. The wage base is the trap and
it is where most coverage goes wrong.

**Not checkable:** whether the boundary is "more than" or "at or above" $150,000 (sources
split — say **over**); the final-regulation detail, still moving; whether any specific plan
has implemented it; the 2027 threshold.

**Counter-evidence beat:** **Roth is not a penalty.** The money grows and comes out tax-free,
so the cost is only the deduction — and whether that is a net loss depends on a future tax
rate **nobody can verify**, which the video says out loud. Most coverage frames this as a
punishment; that framing is the error.

**Runtime:** 30–34s. **Zul:** yes, corner host.

**Hook:** *"At 50, over $150,000, your 401(k) catch-up can't be pre-tax."*
**social-packager: REWRITTEN.** My draft — *"Over $150,000 last year? Your catch-up deduction
is gone."* — was vetoed on three counts: it **opens as a question** (worst-testing opener on
these channels), *"deduction is gone"* **overstates** (only the pre-tax treatment of that
slice goes; you can still contribute), and it **omits "50+"**, which is who the video is for.

**Thumbnail:** `$150,000` large in white, `CATCH-UP = ROTH ONLY` with ROTH in red.

**Confidence: medium-high on the rule, medium on timing.** **What kills it:** final
regulations landing differently, or the 2027 threshold being indexed before publication.
Re-verify the number on the day. **Narrow audience by design** — the packager would not open
the channel with it, and nor would I.

---

## M4 — The overtime deduction ⚠ flagged off-lane

**Working title:** `Overtime Deduction: $12,500 Max, Only the Extra Half Counts` (58 chars)

**Hard number:** **$12,500** ($25,000 filing jointly — and you must file jointly to claim it).
**The cost it hides:** it is a **deduction, not an exemption**. Only the *premium half* of
time-and-a-half qualifies, **payroll tax still applies** (it does not touch Social Security
or Medicare), and only FLSA-required overtime counts — not state-law, union or policy
overtime.

The packager derived the figure that makes this a video rather than a tax note: the premium
is **one third of overtime pay**, so reaching the $12,500 cap takes roughly **$37,500 of
overtime pay**. **That is calculated, not reported**, and must be labelled as such on frame
and in the description — the house rule, applied unprompted.

**Checkable from here?** **HIGH** on the rules, four independent sources. The married-cap
dispute the researcher flagged is **resolved**: $12,500, $25,000 joint, must file jointly;
Paychex's "per person regardless of filing status" appears wrong.
**Not checkable:** whether the sunset is exactly tax year 2028 (verify the end year before
scripting); whether premium-only qualification has been softened — one source flags
ambiguity; the 2026 W-2 box 12 reporting detail, which comes from a single tax-prep source.

**Counter-evidence beat:** it phases out above **$150,000 MAGI / $300,000 joint**, needs a
valid SSN, and it **sunsets** — so for many viewers the answer is "this is smaller than the
headline and it expires."

**Runtime:** 32–36s. **Zul:** yes, corner host.

**Hook:** *"Only the extra half of time-and-a-half is deductible. The cap is $12,500."*
**social-packager: REWRITTEN, and held back in the running order.** My draft spelled the
number out — *"Twelve thousand five hundred dollars…"* — which **fails the silent test**,
because a spelled-out number is not a picture.

**Thumbnail:** `$12,500 MAX` white, `ONLY THE ½ IN TIME-AND-A-HALF` with ½ in red.

**⚠ LANE FLAG — the packager's call, unhedged:** *"It is off-lane for a channel called The
Meticulous Investor. It's a tax topic for hourly workers, not for people holding brokerage
accounts."* A cold-start channel learns who its audience is from its first handful of videos,
so this belongs **fourth or later**, after M1, M2 and M3 have set the lane. Refused to invent
evidence either way: vidIQ cannot see this channel.

**Confidence: high on facts, medium on fit.** **What kills it:** the lane, not the facts. Also
the widest reach of the four, which is the argument for keeping it — just not first.

---

# PARADOCS10X

Neither carries Zul. No host, no stickman, imagery-first (`CHARACTER-ZUL.md`, `CLAUDE.md`).
Neither takes a financial disclaimer — no ticker, no valuation, no buy/sell/hold — but both
take an **on-frame sourcing strip**, which is the stronger requirement here.

---

## P1 — Google's 0.24 Wh prompt

**Working title:** `Gemini Prompt: 0.24 Wh. Or 0.10, Depending on the Boundary` (58 chars)

**Hard number:** **0.24 Wh** per median text prompt (with 0.03 g CO₂e and 0.26 mL water).
**The cost it hides:** **the same prompt measures 0.10 Wh under the narrow boundary.** The
difference is idle capacity, host CPU/RAM and data-centre overhead. The hidden cost is itself
a number, which is the cleanest version of this shape in the set.

**Checkable from here?** **HIGH that Google published it** — the figures and the 0.10/0.24 gap
are consistently reported. But **every figure traces to Google's own report**, so every
sentence carrying one takes **"Google says"** in the sentence, not in the description.
The criticism (Shaolei Ren, UC Riverside) is **MEDIUM**; "excludes training and indirect
water" is **single-source** and must be attributed as *"critics say."*

**Not checkable:** Google's paper itself; any update; whether other labs have published
comparable figures.

**The staleness line is a trap and the desk caught me on it.** I asked whether "nobody has
updated it in 14 months" was the story. It is not sayable: *"I can say I found none, not that
none exists."* Approved wording: **"the only disclosure we have dates from August 2025."**

**BANNED:** Google's own "less than nine seconds of TV" comparison — *"It's Google's, and it
flatters."*

**Counter-evidence beat:** the honest one cuts **toward** Google — its figure is far below the
public estimates that were circulating, and it is a real disclosure nobody else matched. Set
against: it is a **median** (so heavy prompts are excluded from the headline), **text only**
(no image, video or voice), and the boundary is Google's to draw.

**Runtime:** 28–32s. **Zul:** no.

**Hook:** *"The same prompt. 0.10 watt-hours, or 0.24."*
**social-packager: PASSED.** Conditions: `Google's own figures · median text prompt · Aug 2025
disclosure` on the frame. One weakness noted, and it is real: **"it has no named adversary."**

**First frame, silent:** `0.10 Wh | 0.24 Wh` side by side.
**Thumbnail:** `0.10 Wh` white next to `0.24 Wh` red, labelled `SAME PROMPT · GOOGLE'S OWN
FIGURES`.

**Confidence: medium-high.** **What kills it:** Google publishing an update between now and
upload, which would make a 14-month-old figure the wrong lead — **re-search on the day**.
Secondary risk: at 30 seconds a methodology gap can read as dry. It works only if the imagery
is physical — chips, cooling, idle racks — never a diagram of a boundary.

---

## P2 — Waymo's own benchmark

**Working title:** `Waymo's 0.01 vs 0.21 Crash Rate, Scored by Waymo Itself` (54 chars)

**Hard number:** **0.01** serious-injury-or-worse crashes **per million miles** against a
**0.21** human benchmark — about **95% fewer**, across **271.3M rider-only miles** through
June 2026.
**The cost it hides:** the comparison is **constructed by the party being measured**. Five
metros only (LA, SF Bay Area, Phoenix, Austin, Atlanta), rider-only miles **exclude the
conditions Waymo does not drive in**, and Waymo compiles, chooses and publishes the human
benchmark it is scored against.

**Checkable from here?** **MEDIUM.** Figures are consistently reported but all originate with
Waymo's Safety Impact hub, which cannot be opened. The headline has moved — **92% at 170M
miles → 94% at 220M → 95%** — so it is a **rising trend, and the date must be on screen**.
Cite the hub's figure and date, never a news rounding. Autonomy wording must be exact:
**rider-only, no human driver** — not "self-driving."

**⚠ GATE BEFORE SCRIPTING — booked, not noted.** The packager sent a fact-check back up the
line on its own pick: *"'No independent verification' is a negative claim and easy to get
wrong. The Swiss Re claims study and the peer-reviewed Waymo papers are the first things to
rule out."* If either counts as independent, the line softens to **"the benchmark Waymo
built"** and the video still works. **If that check is skipped, the video's whole thesis is
an unverified negative.**

**Counter-evidence beat:** 271 million miles is a genuinely large sample and the direction has
held across three successive updates — this is **not** a video saying the safety claim is
false. It is a video about **who built the exam**. That distinction is the whole piece and it
must be unmistakable, or it becomes a cheap-shot debunk.

**Runtime:** 32–36s. **Zul:** no.

**Hook:** *"Waymo: 0.01 serious-injury crashes per million miles. Humans: 0.21. Waymo built
that benchmark."*
**social-packager: REWRITTEN, lightly.** My draft — *"0.01 against 0.21. Waymo grades its own
exam."* — lost on two points: **0.01 has no unit** (meaningless on a silent first frame), and
*"grades its own exam"* is **editorial**, which this channel does not do.

**Thumbnail:** `0.01 vs 0.21` white, `SCORED BY WAYMO` red, small `THRU JUN 2026`.

**Confidence: medium.** **What kills it:** the independence gate above, or Waymo publishing a
fresh figure that moves the headline again mid-build.

**Why this and not SWE-bench.** The technical desk ranked SWE-bench Verified second and Waymo
as a fallback; **I promoted Waymo.** SWE-bench's headline, 59.4%, is 59.4% *of the 138 hardest
tasks of 500* and the desk ruled it **may never appear separated from that denominator** — a
number that cannot go on a thumbnail cannot carry a short built on this shape. It also
overlaps `paradocs-short-5`'s benchmarks-vs-real-work ground. Waymo is the **only idea in
either channel** that honestly carries the frame behind this channel's one long-form breakout:
**a named head-to-head with a trust question attached.** SWE-bench is parked, not killed.

---

# Recommendation — build M1 first

**M1, The Daily Reset.**

Everything in this repo's recent history says the binding risk is a number that turns out to
be wrong or stale. M1 is **the only one of the six whose hard number we derive rather than
source** — the index ends flat, the fund ends 1.6% down, and that is arithmetic anyone can
reproduce. It has no ticker, no price, no date, no counterparty and no decay; it is as true in
March as today, which is exactly what you want from the first video on a cold-start channel
that may sit unwatched for weeks.

It also forces the right build. The benchmark's real advantage is **charted two-panel data
with sourcing on the frame**, and we proved this session that announcing these two series
instead of drawing them makes even a careful reader attach the numbers to the wrong line. So
M1 cannot be made cheaply or wrongly — it makes us build the panel rig, which M2, M3 and P2
all then inherit.

And the packager passed its hook outright, the only money idea it did. Independently, it also
picked M1 to open the channel.

**Order after that:** M2 → M3 → P2 (gated on the independence check) → P1 → M4 last, off-lane.

---

# ⚠ For the owner — a palette decision, not resolved here

The benchmark short runs **near-black + gold/amber + red**, with headlines in a serif display
face and red reserved for the negative. `STYLE-GUIDE.md` locks this channel to **near-black +
white + ONE red accent**, heavy condensed sans, "nothing else."

Theirs reads warmer and more *financial broadsheet*. Ours reads colder and more *editorial*.

**This is an identity choice and it is yours.** Every thumbnail and first-frame concept above
is costed in **our** palette, and the packager deliberately kept them there rather than drift
toward the reference. Nothing will move on this until you say so.

Two smaller production conflicts, flagged not taken:

- **Cut rate.** `STYLE-GUIDE.md` §2 mandates a cut every 1.2–1.8s, no shot past 2s. The
  benchmark holds **3.3s** and reads as *higher* production, because the motion lives inside
  the footage rather than in the cutting. A sub-40s short at benchmark pace is ~11 shots, not
  ~30. That is a style-guide amendment, not a per-video choice.
- **On-frame sourcing.** The packager recommends adopting it (*"few Shorts viewers open the
  description"*), thumbnails unchanged. Nothing in `engine/` renders a persistent source strip
  today, so it is new build work.
