# Production Record — The Meticulous Investor, LONG: Tesla's two dates

**Status: NOT YET GENERATED. This is the week's one Tesla long.**
`money-fsd-czechia-long/` is on HOLD as the Oct 6 recap.

Scripts locked and fact-checked 2026-09-21. Target runtime ~8:30.
Publish before **Oct 1** — beats 0:45 through 3:20 are pre-event.

## Fixed settings
| Setting | Value |
|---|---|
| Style | Economist — `e7f9a12679ec426099db7646b70a4639` |
| Voice | Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad` |
| Mode | `chat` — **required here.** An 8-minute piece has too many constraints to survive `generate` mode's single shot |
| Orientation | `portrait` (9:16) |

## Session
| session_id | video_id | Result |
|---|---|---|
| — | — | not started |

## Production note — length
Every prior record in this repo is a Short (42–72s). This is the channel's **first
long-form piece**, and nothing here has been proven at that length:
- HeyGen chat mode has only been exercised on ~60s briefs from this account.
- The `STYLE-GUIDE.md` motion rules ("cut or punch in every 1.2–1.8s, no shot past 2s")
  were written for Shorts. Held literally across 8:30 that is ~300 cuts and will read as
  frantic rather than dramatic. **Proposed adaptation:** keep the 1.2–1.8s cadence inside
  each beat's opening 10–15 seconds, then allow 3–4s shots through the body of a beat.
  This is a deviation from a locked rule — confirm before shooting.
- If the long cannot be produced in one pass, cut it as **nine beat-sized segments** and
  assemble. The beat sheet in `SCRIPT.md` is already segmented for this.

## Paste-ready brief

Build from `STYLE-GUIDE.md` §6 with the beat sheet from `SCRIPT.md`, and append:

> **GUARDRAILS (two-dates long):**
> - `$TSLA` as plain text only. **No candles, no chart, no price line.**
> - No Tesla logo, no EU flag, no national flags. Plain text name-tags.
> - Oct 1 stamps `CONFIRMED`; Oct 6 stamps `EXPECTED`. Never assert the committee date.
> - Spec figures always carry `CLAIM (2017)`.
> - The 4.1× safety figure, if shown, stamps `TESLA-MEASURED · 5 COUNTRIES · DATA THROUGH 2025`.
> - Threshold bars must visibly fail to reach the line. Never let one complete.
> - Say "Waco" (as the invite does). **No map** — the flight restriction names McGregor,
>   ~20 miles away, and a map would assert a single site the sources do not agree on.
> - Hero shot: the dim committee tally board. Bookend: a stage light striking an empty
>   floor at 0:00, the same light cutting out at 8:00.
> - Compliance card in the first 4 seconds.
> - **No subscribe animation and no subscribe CTA.** Close on the next dated thing.

**Restate the guardrails at blueprint approval** — especially the no-chart and no-subscribe
rules, which are the two most likely to be helpfully added back by the generator.

## Verification checklist (renders are *complete, not verified* — CDN egress blocked)

Machine-checkable:
- [ ] VO verbatim across all scenes, including the added 5:00 beat
- [ ] Voice `0db3abd83c74452fb2460b0dd113daad`
- [ ] 9:16 portrait, 1080p
- [ ] `caption.enabled: true` — else publish the `captioned_video_url` cut
- [ ] Runtime 8:00–9:00
- [ ] Scene count matches the nine beats

Needs human eyes:
- [ ] Photographic base layer throughout — not flat plates (`motion_graphics` elements
      report `background: #ffffff` and the API cannot distinguish the two)
- [ ] Near-black / white / one red. No navy, no cyan
- [ ] **No chart, candle or price line anywhere**
- [ ] **No subscribe animation** on the end card
- [ ] Counter-evidence beat at 5:00 is actually present and not trimmed
- [ ] No map of Texas; "Waco" spoken, no site asserted visually
- [ ] Cut rhythm is dramatic, not frantic, at this length
- [ ] No faces, no logos, no flags
- [ ] Compliance card in the first 4s

## Constraints hit
- HeyGen CDN egress blocked — complete, not verified.
- No detached VO stem.
- Higgsfield 0 credits. vidIQ ~1 credit — HeyGen session thumbnail; do not chase the score.
- tesla.com egress-blocked: the 2:00 spec claim was verified via press, not the live page.

## Re-verify the morning of publish
- [ ] Oct 1 event still on, still Waco, still 8:30pm ET
- [ ] Oct 6 TCMV date still expected
- [ ] Still 7 states / ~11.8%; France still ~15.3%
- [ ] Sweden's objection unchanged (the 5:00 beat depends on it)
- [ ] tesla.com/roadster spec block unchanged — **check by hand**

## Packaging
- Title: `Tesla Has Two Dates: October 1 Roadster, October 6 FSD. Don't Trade Them as One.`
- HeyGen auto-titles renders off-script — ignore the returned `title`, use the one above.
- Pinned comment:
  > Oct 1 is a reveal. Oct 6 is the vote. Which date is in your thesis?
