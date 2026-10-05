# Production Record — PARADOCS10X Short 3: "The $30,000 Wafer"

- **Rendered:** 2026-09-09
- **video_id:** `c9ac94a803bd4b37b8f9d885c4e797d2`
- **Session:** https://app.heygen.com/video-agent/d1420bda678d44d1b69201e3effa677b
- **Mode:** `generate` (chat mode 404 — see `../paradocs-short-4/PRODUCTION.md`)
- **Orientation:** portrait 9:16
- **Style:** Economist — `e7f9a12679ec426099db7646b70a4639`
- **Voice:** Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad`

## Why this rendered before the keynote finished
The script was checked line by line for event dependencies before firing. It has **none**:

- The hook — *"a number Apple didn't put on a slide today"* — asserts only that Apple did not
  present TSMC wafer costs. Safe under any outcome.
- The body is entirely wafer economics, all verified pre-event.
- The close — *"If prices went up and margin held, you paid for it"* — is phrased
  **conditionally** and stays true whether prices rose or held.

The `[[SLOT]]` noted in `SCRIPT.md` was a *consider-revising* flag on the close, not a blank.
On review the conditional phrasing needed no change, so the short was cleared to render.

⚠️ **This is the one to re-check against the actual keynote.** If Apple did something that makes
the hook read oddly — say, a slide that *did* discuss manufacturing cost — the hook is worth a
re-cut. Watch it before publishing.

## Fact-safety notes
The `$30,000` figure is **industry reporting, not an audited disclosure**, and the VO says so
out loud rather than burying it in the description. The prompt also requires an on-screen
footnote carrying the same caveat. Do not let either be lost — a confident-sounding unaudited
number on a finance channel is exactly what `CLAUDE.md` forbids.

The script names Apple and TSMC in narration. That is fine — `STYLE-GUIDE.md` bans **logos and
badges**, not names. The prompt explicitly forbids the Apple and TSMC marks and any device
resembling a real product.

## VERIFICATION CHECKLIST — human eyes required

**Complete, not verified** — HeyGen CDN egress is blocked here.

| # | Check | Why |
|---|---|---|
| 1 | **Burned-in captions present** | Failed on all 4 previous renders |
| 2 | **"Educational only. Not financial advice." in first 4s** | Non-negotiable; this short names a listed company |
| 3 | **NO Apple logo, NO TSMC logo** anywhere | House rule, and the brief invites them |
| 4 | **No device resembling a real phone** | Prompt bans it; generation may drift |
| 5 | **Wafer-price footnote on screen and legible** | Fact-table requirement — the caveat must be visible, not just spoken |
| 6 | **$30,000 and $25,000–27,000 count up**, not just appear | House rule for numbers; long-form 1 visualised none |
| 7 | **No human faces** — no technicians, no stage, no audience | |
| 8 | **Palette** — near-black, white, one red | |
| 9 | **VO verbatim**, 152 words | Verify against `SCRIPT.md` |
| 10 | **Hook still lands** given what Apple actually announced | See warning above |
| 11 | Runtime ~52s | |

## Publishing order
`LONGFORM-GUIDE.md` §5 says long-form first, shorts as feeders. The long-form is blocked on the
keynote, so if these ship first they run as standalone pieces. Short 4 is the safer lead — it
carries no event dependency and no unaudited number in its hook.

## Constraints hit
- HeyGen CDN egress blocked → **complete, not verified**
- `get_video_agent_session` 404 account-wide → generate mode, no blueprint approval
- Higgsfield 0 credits, vidIQ 1 credit → no B-roll, no thumbnail, no scoring

---

## RENDER COMPLETE — 2026-09-09

- **Watch:** https://app.heygen.com/videos/c9ac94a803bd4b37b8f9d885c4e797d2
- **HeyGen auto-title:** "Paradocs 10X: The $30,000 Chip Wafer" — **ignore it**, upload as
  *"The $30,000 Wafer"* per `SCRIPT.md`
- **Duration:** 55.8s (target ~52s) · 9:16 · 1080p · 9 scenes

### Verified from scene data (not from watching — CDN egress blocked)
| Check | Result |
|---|---|
| VO script **verbatim** across all 9 scenes | ✅ **PASS** — matches `SCRIPT.md` word for word |
| Series voice `0db3abd8…` on every scene | ✅ **PASS** |
| 9:16 portrait, 1080p | ✅ **PASS** |
| The audited-disclosure caveat survived into the VO | ✅ **PASS** — scenes 6 and 7 carry it intact |
| **Burned-in captions** | ❌ **FAIL — `caption.enabled: false`** |
| Imagery / palette / no Apple or TSMC logo | ❓ **UNKNOWN** — needs human eyes |

The caveat surviving matters: it is what keeps an unaudited number on a finance channel
compliant. Confirm the **on-screen footnote** is present too — that was in the brief but
cannot be verified from scene data.

### The caption defect — no re-render needed
`captioned_video_url` → `caption_c9ac94a803bd4b37b8f9d885c4e797d2.mp4`

### Same imagery ambiguity as Short 4
All scenes report `background: {color: '#ffffff'}` plus one `motion_graphics` b-roll element.
See `../paradocs-short-4/PRODUCTION.md` for why this is UNKNOWN rather than FAIL.
