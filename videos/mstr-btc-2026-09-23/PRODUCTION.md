# Production — $MSTR bitcoin math

Two cuts of the same script exist. Both verified as far as this environment allows.

## A. HeyGen cut — **the real channel voice** ✅ APPROVED
- **Watch:** https://app.heygen.com/videos/07ec91817c45421993a4eaa90c802b78
- **video_id:** `07ec91817c45421993a4eaa90c802b78` · **110.07s** · 9:16 · 1080p
- **Title (auto):** "Bitcoin Up. Strategy Down." — HeyGen's own, and good enough to keep
- **Cost:** **74 premium credits** (361 → 287) = **40.3 cr/min**, matching the rate measured
  in `RENDERING.md`

### Verified from `get_video_scenes` (25 scenes)
| Check | Result |
|---|---|
| Voice `0db3abd8…` on every scene | **PASS** |
| Script verbatim, no rewrites | **PASS** |
| Brand glossary `c9064148…` applied | **PASS** |
| 9:16, 1080p | **PASS** |
| voice_settings | pitch 0 · speed 1.0 · volume 1.0 |
| **Captions** | **FAIL — `caption.enabled: false`** |

**Caption fix, no re-render needed:** publish `captioned_video_url` →
`caption_07ec91817c45421993a4eaa90c802b78.mp4` from the video page. An SRT is also exposed
via `subtitle_url`.

**UNKNOWN — needs eyes.** Every scene reports `background:#ffffff` with one
`motion_graphics` element. `get_video_scenes` returns only an id and type for
`motion_graphics`, so a full-frame dark plate is invisible to this API and the white
background may never be seen. Whether the three-colour palette and the mNAV decline chart
landed **cannot be resolved without watching it** — CDN egress is blocked here.

## B. HyperFrames cut — exact charts, working captions
`mstr-btc-math.mp4` — 117.6s, built locally, **0 credits**, `check` passed 56/56 WCAG AA,
frames inspected. Placeholder Kokoro voice. Keep as the data-accurate reference.

---

## THE WORKING RECIPE — reuse this

```jsonc
// mcp__heygen__create_video_agent
{
  "mode": "generate",                                    // NOT chat — see below
  "orientation": "portrait",
  "styleId": "e7f9a12679ec426099db7646b70a4639",         // Economist
  "voiceId": "0db3abd83c74452fb2460b0dd113daad",         // Alex Wright – Informative
  "brandGlossaryId": "c906414830134497906c72eecf054153"  // TWIM lexicon, 36 terms
}
```

1. **Chat mode stalled again.** Session `2a34bf9a…` sat at `status:thinking, progress:0`
   with `video_id:null` for 7+ minutes — the same failure as `paradocs-short-1`. It
   **consumed zero credits**, so abandoning it is free. Do not wait on chat mode; give it
   ~5 minutes, then switch.
2. **`generate` returns a real `video_id` immediately** and is trackable via `get_video`.
   `pending` → `processing` → `completed`; the title changing from the prompt text to a real
   headline is the signal it has parsed the script.
3. **Generate mode disables captions even when the prompt demands them.** Instructing
   "captions must be ENABLED" did **not** work. Assume `caption.enabled:false` every time and
   plan on the `captioned_video_url` cut.
4. **Put every constraint in the initial prompt.** Generate mode has no blueprint approval,
   so there is no second chance to restate the palette, the no-faces rule or the key chart.
5. Budget ~40 cr/min. A 2-minute short is ~75–80 credits.
