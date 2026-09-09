# Production Record — PARADOCS10X Short 4: "Moore's Law Was Never About Speed"

- **Rendered:** 2026-09-09
- **video_id:** `25c732d0e2c642e88d83921b22e3b626`
- **Session:** https://app.heygen.com/video-agent/6b3156af39c944dc88b3742c1fd47269
- **Mode:** `generate` (chat mode was down — see below)
- **Orientation:** portrait 9:16
- **Style:** Economist — `e7f9a12679ec426099db7646b70a4639`
- **Voice:** Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad`

## Why this one rendered first
It has **no event-dependent content**. Its central claim is a direct reading of a published
1965 document, so it did not have to wait for the Apple keynote to finish. That was a
deliberate design choice at scripting time — see `SCRIPT.md`.

It is also the most defensible piece of the three: Moore's article title, its subtitle, and
what he actually plotted are all **High** confidence.

## Chat mode was down again — worse than last time

Two chat-mode sessions were accepted, appeared in `list_video_agent_sessions`, then **404'd on
`get_video_agent_session`**:
- `45d7f6d7e2fc4df5a27268cb40d2ee86` (this short)
- `e4921681387942189b20a5aa1ed41734` (Short 3)

**This time the endpoint is broken account-wide, not just for new sessions.** The diagnostic in
`paradocs-short-1/PRODUCTION.md` says to try an older session to confirm endpoint health. The
older session `f3aaa6333ec94c54944814620404ecbb` — which that record says used to read fine —
**also 404s now**. So `get_video_agent_session` is failing for every session, old and new.

Credits were not the cause: 129 premium remaining at fire time.

**Workaround applied:** `mode: generate`, which returned `status: generating` with a real
`video_id` immediately.

⚠️ **Two dead chat sessions exist** (listed above). They produced no video last time this
happened. They could not be stopped because the session endpoint is the thing that is down.

## Cost of the workaround
Generate mode is fire-and-forget — there is no blueprint approval step, so the constraints got
exactly one shot in the initial prompt and could not be restated. `STYLE-GUIDE.md` notes that
the restatement at approval is what makes constraints survive generation.

To compensate, the prompt was hardened before firing:
- **"CAPTIONS MUST BE ENABLED AND BURNED IN"** stated as its own line — captions have failed on
  all four previous renders
- "NEVER typography on an abstract background or plain colour" added to the BASE layer rule
- The palette line made absolute — "nothing else", "reserve red for graphics and type only"
- The banned list extended to match `STYLE-GUIDE.md` exactly (lens flare, exclamation marks)

**Expect this render to hold the brief less tightly than a chat-mode render would.**

## VERIFICATION CHECKLIST — human eyes required

HeyGen CDN egress is blocked from this environment, so this render is **complete, not
verified**. Check each of these by watching it:

| # | Check | Why |
|---|---|---|
| 1 | **Burned-in captions present** | Failed on all 4 previous renders. If `caption.enabled: false`, publish the `captioned_video_url` cut instead |
| 2 | **"Educational only. Not financial advice." in first 4s** | Non-negotiable. `paradocs-longform-1` appears to be missing it |
| 3 | **No human faces** — especially no portrait of Gordon Moore | The prompt bans it explicitly, but a 1965-magazine brief invites one |
| 4 | **No corporate logos** on the magazine, wafers or graphs | House rule |
| 5 | **Imagery-first** — real photographic plates, not type on flat colour | The failure mode `STYLE-GUIDE.md` calls "tried and rejected" |
| 6 | **Palette** — near-black, white, one red. No neon or gradients | |
| 7 | **VO script verbatim**, 148 words, no rewriting | Verify against `SCRIPT.md` |
| 8 | Wafer-price footnote legible on screen | Fact-table requirement |
| 9 | Runtime ~50s | |

## Constraints hit
- HeyGen CDN egress blocked → cannot watch or download; **complete, not verified**
- `get_video_agent_session` 404 account-wide → chat mode unusable, no blueprint approval
- Higgsfield 0 credits, vidIQ 1 credit → no B-roll, no thumbnail generation, no scoring
- HeyGen thumbnail: check the session page for the auto-generated one
