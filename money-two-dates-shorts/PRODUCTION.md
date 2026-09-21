# Production Record — The Meticulous Investor, two-dates pack (5 Shorts + 1 added)

**Status: NOT YET GENERATED.** Scripts locked and fact-checked 2026-09-21.
Batch scheduled **Sunday 2026-09-27**.

**Hard expiry.** Shorts 1–4 are pre-event and die on **Oct 1**. Short 5 and the added
Short 6 die on **Oct 6**. Publish the whole pack in the window Sept 27 – Sept 30.

## Fixed settings
| Setting | Value |
|---|---|
| Style | Economist — `e7f9a12679ec426099db7646b70a4639` |
| Voice | Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad` |
| Mode | `chat` (fall back to `generate` if chat 404s) |
| Orientation | `portrait` (9:16) |

## Session IDs
| Short | session_id | video_id | Result |
|---|---|---|---|
| 1 — TWO DATES | — | — | not started |
| 2 — REVEAL ≠ REVENUE | — | — | not started |
| 3 — 2017 SPECS ARE STILL CLAIMS | — | — | not started |
| 4 — DON'T PAY TWICE | — | — | not started |
| 5 — WHICH ROW DO YOU OWN? | — | — | not started |
| 6 — SWEDEN SAYS NO *(added)* | — | — | not started |

## Paste-ready brief (per Short)

Build from `STYLE-GUIDE.md` §6, substitute the VO and imagery beats from `SCRIPT.md`, and
append:

> **PACK GUARDRAILS (two dates):**
> - `$TSLA` appears as **plain text only.** No candlesticks, no chart, no price line, no
>   invented price action of any kind. A ticker on screen with a moving line is a fabricated
>   market claim.
> - No Tesla logo, no EU flag, no national flags. Plain text name-tags for all 27 states.
> - Population and country counts animate as **bars that visibly fail to reach the
>   threshold line.** The gap is the point; do not let a bar fill to 100%.
> - Every date carries a state stamp: `CONFIRMED` (Oct 1) or `EXPECTED` (Oct 6). The
>   committee date can move and the video must not assert it as fixed.
> - Short 4's valuation line carries a `FRAMING, NOT A PRICE CALL` stamp.
> - Hero shot: a dim committee tally board, rows half-lit. Bookend the pack with it.
> - "Educational only. Not financial advice." in the first 4 seconds **and** on the last frame.

**Restate the guardrails at blueprint approval.**

## Verification checklist (renders are *complete, not verified* — CDN egress blocked)

Machine-checkable:
- [ ] VO verbatim in every scene, all six
- [ ] Voice `0db3abd83c74452fb2460b0dd113daad`
- [ ] 9:16 portrait, 1080p
- [ ] `caption.enabled: true` — else publish the `captioned_video_url` cut
- [ ] Duration 15–25s each

Needs human eyes:
- [ ] Photographic base layer present, not a flat navy plate. **The outline asked for "dark
      navy, big white text"; the house palette overrode it.** Confirm what rendered
- [ ] Palette near-black / white / one red — no navy, no cyan
- [ ] **No chart, candle or price line anywhere near `$TSLA`**
- [ ] Threshold bars stop short of the line (they must not complete)
- [ ] `EXPECTED` stamp present on every Oct 6 mention
- [ ] No faces, no logos, no flags
- [ ] Compliance card readable in the first 4s

## Constraints hit
- HeyGen CDN egress blocked — complete, not verified.
- No detached VO stem (`create_speech` needs `api` credits).
- Higgsfield 0 credits. vidIQ ~1 credit — use HeyGen's session thumbnail; do not chase the
  vidIQ score against this palette.

## Re-verify before publishing
These facts move. Check each one the morning of publish:
- [ ] **Oct 6 TCMV date still stands** — committee dates slip. Source: fsd-eu-tracker.de
- [ ] **Still seven approved states, still ~11.8%** — an eighth approval before publish
      breaks Shorts 5 and 6 and the "about 12%" figure
- [ ] **Sweden's position unchanged** — Short 6 is built on it. If Tesla removes or gates
      the speed-offset feature, that Short is dead
- [ ] **tesla.com/roadster spec block unchanged** (Short 3). tesla.com is egress-blocked
      from this environment; check by hand
- [ ] **Oct 1 event still on** for Shorts 1–4

## Open decisions
- Pack is six Shorts, not five. If it must stay at five, cut Short 4 (`DON'T PAY TWICE`) —
  it is the only beat carrying no verifiable fact. Do **not** cut Short 6; it is the
  counter-evidence beat `STYLE-GUIDE.md` §5 requires.
