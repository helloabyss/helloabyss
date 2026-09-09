# Production Record — PARADOCS10X Short 1 rebuild

- **Session:** https://app.heygen.com/video-agent/f3aaa6333ec94c54944814620404ecbb
- **video_id:** `5f10618bb45c4c5cb74669aa40ba5dee`
- **Mode:** generate (chat mode was failing — see below)
- **Style:** Economist — `e7f9a12679ec426099db7646b70a4639`
- **Voice:** Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad`

## Rebuilding
Original: `7e996157645fe8fac15f961a759556d7` — "SHORT 1 - Nine Feet of Manure - PARADOCS10X",
42.5s, 9:16, 1080p. Three static background images, no elements, **captions disabled**.
The original already used this same voice, so the series voice is unchanged.

Sibling in the series: `5106846e12b3f3d8b8c238cc71937017` — "SHORT 2 - 95 Percent Parked".
Worth rebuilding to match once Short 1 is approved.

## Changes
- Imagery-first three-layer stack and dramatic motion, per `STYLE-GUIDE.md`.
- **Captions turned ON** (original had them disabled) — house style requires burned-in
  word-by-word captions.
- One factual correction (below). Arc, payload and the "This is Paradocs 10X" sign-off kept.

## The factual correction — do not revert
The original asserts as fact: *"In 1894, a London newspaper made a prediction…"*
No such article has been located; the quote traces to a 2004 essay and The Times refuted
the attribution in 2018.

The rebuild keeps the hook verbatim as a **familiar claim** and immediately sources it:
"No one has ever found that article. But the crisis underneath it was real." An on-screen
footnote carries the correction. Everything after is documented, so the Ford punchline is
unaffected — and the video stops being vulnerable to a "this is a debunked myth" top comment.

## Prompt guardrails
- No real newspaper masthead (the script makes a claim about a real publication).
- The autonomous pod is generic and unbadged — no Tesla branding.
- Archival cold grade, not warm sepia.
- Street bookend shot from an identical camera position at both ends.

## Constraints
- Higgsfield 0 credits; vidIQ ~1 credit. Check the HeyGen session for its auto-generated thumbnail.
- HeyGen CDN egress blocked — render will be **complete, not verified**.

## Note on an earlier misread
Before finding the existing PARADOCS10X series, a standalone manure short was scripted and
sent to session `34e1666e89274d309417fac5667fda54`. That session now returns 404 and no video
from it appears in the account, so it produced nothing. Its directory was removed; the useful
research carried into this rebuild.

## HeyGen chat mode was failing — workaround used
Two chat-mode sessions created after a container restart were accepted, appeared in
`list_video_agent_sessions`, but then **404'd on `get_video_agent_session` and produced no
video at all**:
- `34e1666e89274d309417fac5667fda54` (dead 7.5+ hours, no video)
- `eae1d23393a14cac9a261206d182b653` (dead, no video)

Diagnostics that ruled out the obvious causes:
- The same endpoint returns full detail for **older** sessions (`b48693558189…` reads fine),
  so the endpoint itself is healthy.
- Credits are fine — 330 premium remaining.
- Same tool, same parameters that worked earlier in the day.

**Workaround: use `mode: generate`.** It returned `status: generating` with a real `video_id`
immediately, and the video record is trackable via `get_video`.

**Cost of the workaround:** generate mode is fire-and-forget. There is no blueprint approval
step, so the constraints cannot be restated at approval — which `STYLE-GUIDE.md` notes is
what makes them survive generation. Expect this render to hold the brief less tightly than
the PDT and moat rebuilds did. If chat mode recovers, prefer it.

---

## RENDER COMPLETE — with one confirmed defect

- **Watch:** https://app.heygen.com/videos/5f10618bb45c4c5cb74669aa40ba5dee
- **video_id:** `5f10618bb45c4c5cb74669aa40ba5dee`
- **Duration:** 45.6s (original was 42.5s) · 9:16 · 1080p

### Verified from scene data (not from watching — CDN egress is blocked)
| Check | Result |
|---|---|
| VO script verbatim across all 10 scenes | **PASS** |
| Series voice (`0db3abd8…`) | **PASS** |
| 9:16 portrait, 1080p | **PASS** |
| **Burned-in captions** | **FAIL — `caption.enabled: false`** |
| Imagery-first base layer | **UNKNOWN** — see below |
| Palette / grade | **UNKNOWN** — needs human eyes |

### The caption defect and its fix
House style requires burned-in word-by-word captions; this render has them disabled, the
same gap the original had. **No re-render is needed** — HeyGen produced a separate captioned
cut. Publish that one:

`captioned_video_url` → `caption_5f10618bb45c4c5cb74669aa40ba5dee.mp4` (linked from the video
page above). Check its caption styling matches house style before publishing.

### Why the imagery is UNKNOWN, not FAIL
Every scene reports `background: {color: '#ffffff'}` with a single element of type
`motion_graphics`, id-prefixed `b_roll_*`. Read literally that is a white background, which
would fail both the imagery-first rule and the near-black palette. But `get_video_scenes`
only describes `avatar`, `image` and `video` elements in full — a `motion_graphics` element
carries just an id and a type, so a full-frame b-roll plate would be invisible to this API
and the white background never seen. **Cannot be resolved without watching it.** If the video
does read white and flat, the imagery instruction did not land and it needs a re-run.

### Conclusion
Generate mode preserved the script perfectly and lost at least one style constraint. Prefer
chat mode once it recovers, so the brief can be restated at blueprint approval.
