# Production Record — PARADOCS10X Roadster pack (5 Shorts + Oct 1 recap)

**Status: NOT YET GENERATED.** Scripts locked and fact-checked 2026-09-21.
Batch scheduled **Sunday 2026-09-27**. Publish before **Oct 1** — the whole pack is a
pre-event pack and Shorts 1–4 lose their point the moment Tesla is on stage.

## Fixed settings (unchanged across the series)
| Setting | Value |
|---|---|
| Style | Economist — `e7f9a12679ec426099db7646b70a4639` |
| Voice | Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad` |
| Mode | `chat` (fall back to `generate` if chat 404s — see `paradocs-short-1/PRODUCTION.md`) |
| Orientation | `portrait` (9:16) |

## Session IDs
| Short | session_id | video_id | Result |
|---|---|---|---|
| 1 — OCT 1 IS A REVEAL | — | — | not started |
| 2 — 2017 NUMBERS | — | — | not started |
| 3 — COLD GAS ≠ TIRE GRIP | — | — | not started |
| 4 — A71 = RUMOR CODE | — | — | not started |
| 5 — TWO CARS, ONE HEADLINE | — | — | not started |
| 6 — Oct 1 recap | — | — | script pending the event |

## Paste-ready brief (per Short)

Build from `STYLE-GUIDE.md` §6. Substitute the VO and the IMAGERY BY BEAT line from
`SCRIPT.md`, and append these pack-specific guardrails to every one:

> **PACK GUARDRAILS (Roadster):**
> - No Tesla badge, no SpaceX logo, no Falcon 9 livery. Plain text name-tags only.
> - **No speedometer sweep and no 0–60 graphic of any kind.** The video's argument is that
>   the numbers are unverified; animating them contradicts it.
> - Every spec number appears with a `CLAIM (2017)` or `CONFIRMED` stamp beside it.
> - Unconfirmed items (A71, nozzle count, rear seats) render as **dashed outline**, not
>   solid fill. Solid = confirmed. Keep that rule consistent across all five.
> - No ticker, no chart, no price. This is a hardware pack.
> - Hero shot: macro of a composite pressure-vessel valve, one red seal ring. Bookend the
>   pack with it — opening on Short 1, sealing on Short 5.
> - "Educational only. Not financial advice." in the first 4 seconds. PARADOCS10X plate on
>   the last frame.

**Restate the guardrails at blueprint approval.** That is what makes them survive
generation (`STYLE-GUIDE.md` §7).

## Verification checklist (CDN egress is blocked — renders are *complete, not verified*)

Machine-checkable from `get_video` / `get_video_scenes`:
- [ ] VO script verbatim in every scene, all five
- [ ] Voice is `0db3abd83c74452fb2460b0dd113daad` on all five
- [ ] 9:16 portrait, 1080p
- [ ] `caption.enabled: true` — if false, publish the `captioned_video_url` cut instead
- [ ] Duration 15–25s per Short

Needs human eyes (watch on app.heygen.com, not from here):
- [ ] Imagery is a real photographic base layer, not a flat plate — `motion_graphics`
      elements report `background: #ffffff` and the API cannot tell these apart
- [ ] Palette is near-black / white / one red. **No cyan** (the outline asked for cyan;
      the house palette overrode it — confirm which one actually rendered)
- [ ] No 0–60 or speedometer animation appeared anyway
- [ ] CLAIM vs CONFIRMED stamps legible and correct
- [ ] No faces, no logos
- [ ] Compliance card readable within the first 4s

## Constraints hit
- **HeyGen CDN egress blocked** (`files2.heygen.ai`, `resource2.heygen.ai`) — cannot download
  or watch. Report as complete, not verified.
- **No detached VO stem** — `create_speech` needs `api` credits the Creator plan lacks.
- **Higgsfield 0 credits** — no external B-roll.
- **vidIQ ~1 credit** — thumbnail generation costs 22. Use the HeyGen session's own
  auto-generated thumbnail instead. Do not chase the vidIQ score; it penalises this
  channel's desaturated palette by design.
- **tesla.com is egress-blocked from this environment.** F4 (the 1.9 / 250+ / 620 figures
  still being on the site) was verified through press sources, not by loading the page.
  **Spot-check tesla.com/roadster by hand before publishing Short 2** — if Tesla quietly
  updates the spec block before Oct 1, that Short is wrong.

## Open decisions
- Short 6 (Oct 1 recap) cannot be written until the event. Hold the slot.
- If the reveal slips, Shorts 1–5 still hold — but re-verify the date before publishing.
