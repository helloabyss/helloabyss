# ONE NUMBER — series brief

**Status: prepared, not approved.** §6 holds one decision only Sheldon can make.
Written 2026-10-05.

---

## 1. What it is

**One number that was in the news this week. Where it actually comes from. Where it
is weaker than it looks.**

60–90 seconds. The arithmetic is drawn on screen as it is spoken. Hosted by Zul
(`CHARACTER-ZUL.md`), bare-headed variant. Every episode ends on the counter-evidence
beat the channel already mandates — here it is not an obligation bolted on, it is the
last act of the format.

The channel is called The Meticulous Investor. This series is that word as a format:
showing the working is the entire product.

## 2. Why this series, and not a different one

Three things in `GROWTH-PLAN.md` point at it, and they are the plan's own findings,
not new claims:

- **§2 — "The constraint is cadence and news-latency."** Not quality. The three shorts
  in the repo are well-built; the channel published 5 videos in 30 days and gained 0
  subscribers while a competitor's 82-second Fed short, up within hours, took 286,270
  views. A format that can ship the day a number prints attacks the stated constraint.
- **§3 — "narrow and frequent."** The breakout channels in this niche are two years
  old and topically disciplined. ONE NUMBER is maximally narrow: a single, repeatable
  question asked of a different number each time.
- **§3 — flat declarative titles, 60–90s.** The format is already the shape of the
  things that win here. The title writes itself from the number.

A number is also the one subject where **drawn beats photographed**. Cinematic B-roll
cannot show a calculation; it can only gesture at one while a voice asserts the result.
A stick figure at a board can show the division happening. That is an argument for the
format on the merits, not just on cost.

## 3. What it costs — and why that matters this week

**Zero credits per episode.** The engine (`engine/`) renders a full set of scene stills
in about 7 seconds on this machine, deterministically, with no API call.

Measured 2026-10-05: **HeyGen 0** (resets 10-06 12:57 UTC), **Higgsfield 0.35**. The
house-style pipeline cannot render anything today, and cannot buy a hero plate at all.
A zero-credit format is not a nice-to-have this week.

The sane split, if the series runs:

| Slot | Format | Cost |
|---|---|---|
| 3 × weekly cadence episodes | ONE NUMBER, engine | 0 |
| Friday reactive slot (§6 — "where the outliers come from") | House style, HeyGen | ~1 credit |

That reserves the credit budget for the slot the plan says generates outliers, and
stops cadence depending on a balance that just hit zero.

## 4. Episode architecture

Conforms to `STYLE-GUIDE.md` §5A. **≈2.6 words/second; the 5-second hook ceiling is 13
words with no tolerance.** Budgets below are computed, not copied.

| Beat | Window | Words | Job |
|---|---|---|---|
| **HOOK** | 0:00–0:05 | **≤13** | The number, stated flat. Most surprising true thing in the fact table. Must work as the title. |
| **SOURCE** | 0:05–0:25 | ≈52 | Who published it, when, and what it literally measures. Named, not "studies say". |
| **THE WORKING** | 0:25–0:55 | ≈78 | The arithmetic, drawn as spoken. The spine of the episode. |
| **THE TURN** | 0:55–1:15 | ≈52 | Signposted aloud. Where the number is weaker than it looks. |
| **CLOSE** | 1:15–1:30 | ≈39 | One thing the viewer can check or do. Loops back to the hook number. |

**Total ≈234 words ≈ 90s.** A 60s cut is the same spine at ≈156 words, trimming SOURCE
and CLOSE, never THE TURN.

Rules inherited and non-negotiable: no question openers, no dates before the claim,
compliance as a thin bottom-edge strip in the first 4 seconds (never a full card —
it would eat the hook), faceless, no real logos, no clickbait.

**Caption rule carried over from finding #13:** shot-list row labels must be verbatim
substrings of the VO, re-checked after every VO edit. Captions burn in word-by-word.

## 5. Packaging

- **Title: the number, flat and declarative.** No series prefix, no "EP 4" — those cost
  CTR and the brand is carried by the look, not by a tag in the title.
- **Thumbnail: the number itself, set huge, with Zul.** Locked palette — near-black,
  white, one red accent. Built in the engine, so it costs nothing and cannot drift from
  the character. This is the strongest brand-forming surface the series has: a viewer
  should recognise an episode from the thumbnail alone at 320px.
- Per `CLAUDE.md`: **do not chase the vidIQ thumbnail score.** It rewards saturation and
  will fight the palette.

## 6. The decision — T8, and the honest case against

**Running two visual formats on a 6-subscriber channel splits the visual signal.**
`GROWTH-PLAN.md` §1 argues topical discipline is the whole strategy at this size, on the
grounds that every video is a meaningful fraction of the classification evidence. That
argument is about *topic*, and the lane here stays finance — but the same logic applies
at least partly to *look*. A viewer who meets the channel twice should meet the same
channel twice.

`STYLE-GUIDE.md` is explicit that photographic imagery is the base layer and that
typography on abstract backgrounds "was tried and rejected". **A white-ground stickman
short does not comply with the house style as written.** This brief does not pretend
otherwise and does not quietly amend it.

So there are three honest options, and this is the call to make:

1. **ONE NUMBER becomes the channel's cadence format** for 90 days. House style is kept
   for the Friday reactive slot. `STYLE-GUIDE.md` gains a section saying so. Best answer
   to the §2 cadence constraint and to a zero credit balance; costs visual uniformity.
2. **Stay house-style only.** Park this brief. Cadence stays hostage to the HeyGen
   balance, and nothing ships today.
3. **Run one ONE NUMBER episode as a test** against the existing three shorts and compare
   retention before committing. Slowest, but it is the only option that produces evidence
   rather than an opinion — and this repo's whole discipline is evidence over assertion.

**Recommended: 3, then 1 if it holds up.** The channel has been burned by confident
unverified calls fifteen times (`PROVENANCE.md`); a format change on a cold-start channel
is exactly the kind of decision that should produce evidence first. One episode costs
zero credits and about a day.

## 7. Candidate angles — UNRESEARCHED

**None of these are claims. Every one is a question to point `scout` and `fact-checker`
at, and several may not survive contact with a source.** Recurring, calendar-pegged
numbers are listed first because they make cadence predictable — the series should not
depend on something surprising happening each week.

| # | The number | Why it may carry an episode | Pegged to |
|---|---|---|---|
| 1 | The Social Security COLA | A single published figure, derived by a formula most people have never seen worked through | Annual, autumn |
| 2 | The CPI headline vs the core print | Two numbers from one release that routinely disagree; the gap is the episode | Monthly |
| 3 | The headline unemployment rate vs U-6 | Same data, two definitions, very different number | Monthly |
| 4 | A mortgage rate's true lifetime cost | Pure arithmetic, highly drawable, and the result is usually a surprise | Continuous |
| 5 | An index's "record high" in nominal vs real terms | A record that may not be one once deflated | Continuous |
| 6 | A fund's expense ratio over a holding period | Small number, large compounding; the whole point is the working | Continuous |
| 7 | The FOMC dot-plot median vs the market-implied path | Two forecasts of one thing; already channel territory via `fed-dot-short` | 8×/year |

Each needs a fact table with confidence levels before a word of VO is written, per
`CLAUDE.md`. Rows 1–3 and 7 are calendar events and can be scheduled in advance —
`GROWTH-PLAN.md` §5 link 3 proposes exactly this.

## 8. What is NOT built yet

Honest gaps, so none of this reads as further along than it is:

- **The engine renders 1920×1080 landscape. The channel is portrait 9:16.** A portrait
  composition pass is required — the primitives are positionable, but every scene in
  `engine/` is composed for a landscape frame. Proof render: `engine/portrait-proof.png`.
- **No episode exists.** No fact table, no VO, no shot list for any of §7.
- **No scene primitives for arithmetic** — the thing the series is actually about. The
  kit has figures, shops, piles and charts; it has no "working shown step by step on a
  board" primitive. That is the main build if §6 goes ahead.
- **Zul has never appeared on this channel.** He was designed for PARADOCS10X, which
  `GROWTH-PLAN.md` §1 parks. Reusing him here is a deliberate transfer, not continuity.
- **No retention evidence** that a drawn format performs in this niche. §3's research
  covers titles, length and timing — not illustration style.
