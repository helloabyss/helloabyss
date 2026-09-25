# Production Record — PARADOCS10X "The Headset Disappears" (Meta VR Glasses)

- **Session:** https://app.heygen.com/video-agent/07bdf30108254e5292557bc560dc7dfc
- **Mode:** chat (session is alive and readable, unlike the 404s hit on Short 1)
- **Style:** Economist — `e7f9a12679ec426099db7646b70a4639`
- **Voice:** Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad`
- **Orientation:** portrait 9:16
- **Credits at start:** 275 premium

## Source material — none from meta.com
Asked to reuse images and clips from meta.com/vr-glasses. Not used:
- `www.meta.com` is blocked by the egress proxy (curl 403, WebFetch EGRESS_BLOCKED).
- Flipping or remixing Meta's copyrighted ad material to get past Content ID was declined.
- It would also break the no-faces and no-logos rules in the style guide.
All imagery is generated as generic, unbadged hardware. If real footage is wanted, Meta's
newsroom press assets can be added in the edit under their terms, unaltered.

## Research constraints
roadtovr.com and engadget.com are also egress-blocked, so the facts come from search-result
summaries of several outlets that agree with each other (UploadVR, VR.org, Hardware
Busters, CNBC, Meta 10-Q). The FOV figure differs between sources (70°×66° vs 84°), so the
script says only "narrower than a Quest 3".

## Prompt guardrails
- Generic, unbadged glasses and headset — no Meta/Apple/Ray-Ban/Oakley likeness or logos.
- Puck-in-pocket shot cropped at the shoulder — no face.
- Bookend: same desk, same camera position — headset at the open, only glasses at the close.
- Captions explicitly required (Short 1 rendered with `caption.enabled: false`).

## Brief change
The user removed the "Educational only. Not financial advice." card because PARADOCS10X is a tech
channel. The change was sent into the session before the blueprint was approved.

## Status
- **13:56 UTC — blueprint `blueprint_904s7t` approved** with all constraints restated (imagery
  base layer, grade, same-desk bookend, hero shot, captions, no faces/logos, no disclaimer
  card, footnotes kept). Rendering.
- HeyGen estimates **~66s** with the verbatim script at this voice's pace (target was ~58s).
  Kept as is: Shorts allow up to 3 min and the style guide says not to cut facts for length.

## RENDER COMPLETE — not verified

- **Watch:** https://app.heygen.com/videos/26c914fb455c440ab5a4704d665678e6
- **video_id:** `26c914fb455c440ab5a4704d665678e6`
- **Duration:** 58.7s (the blueprint estimated 66s, but the render came in on the ~58s target) · 9:16 · 1080p · 13 scenes
- HeyGen auto-title "The Headset That Disappeared" — use a title from `SCRIPT.md`.

### Checked from scene data (not from watching — CDN egress blocked)
| Check | Result |
|---|---|
| VO verbatim (13 scenes joined, compared to the brief exactly) | **PASS** |
| House voice `0db3abd8…`, speed 1.0 | **PASS** |
| 9:16, 1080p | **PASS** |
| No disclaimer card | Agent confirms; no scene script/element suggests one — **eyes needed** |
| Captions | **AMBIGUOUS** — `caption.enabled: false` at video level (same as Short 1), but the agent says it built **custom karaoke captions** (white on dark scrim, active word red) as on-screen graphics. If the main render shows no captions, publish the `captioned_video_url` cut (`caption_26c914fb….mp4`, linked from the video page). **Do not publish both caption layers stacked.** |
| Imagery base layer | **UNKNOWN** — every scene reports `background: #ffffff` + one `motion_graphics` b-roll element; this API doesn't describe those, same as Short 1. Must be watched. |

## Verification checklist (a human has to watch it — CDN egress is blocked)
- [ ] **No** "Not financial advice" card (removed by user; tech channel)
- [ ] VO verbatim, ends "This is Paradocs 10X."
- [ ] Burned-in word-by-word captions present
- [ ] Imagery base layer on every scene — not flat white or abstract
- [ ] No faces, no real logos, no recognisable Meta/Apple product design
- [ ] Near-black / white / red only; imagery desaturated
- [ ] Footnotes on battery (Meta's figure) and Reality Labs (Q2 2026, 10-Q)
- [ ] Bookend: same desk at open and close

## Thumbnail — 4 candidates generated (Higgsfield, GPT Image 2.5, 9:16, 2K)
Higgsfield now has credits (540 at the time, ~11 used). vidIQ has 1 credit, so generating costs 22
and scoring costs 5, and scoring also needs an uploaded YouTube video ID. **No CTR score available.**
Images are hosted on cloudfront, which the egress proxy blocks, so they could not be pulled
into the repo or looked at from here.

| # | Concept | Job ID |
|---|---|---|
| A1 | "100 GRAMS" / red "THE HEADSET IS GONE", cracked headset + floating glasses | `0b3fdcc4-bd62-4da1-a098-c8fe27389658` |
| A2 | same prompt, second variant | `d5df1d54-7407-4fb6-a962-6d99a7d44670` |
| **B1** | **"VR HEADSET" struck through in red / "$1,299 GLASSES", glasses on a scale reading 100g** | `5327b1ca-f6cb-48b8-893e-bf70922e6bcb` |
| B2 | same prompt, second variant | `434ea87d-6ff3-410f-a70d-eb557daa8ef8` |

**Recommendation: concept B.** The struck-through "before" next to the "after" states the whole
video in three words, reads at phone size, and uses the same red-strike layout as the PDT
thumbnail (`pdt-short/thumbnail-pdt.png`). Before picking, check the AI-rendered text for spelling
and that there are no logos or brand-like marks on the hardware.

### Thumbnail v2 — product likeness + "META" name (user request)
The user flagged that the A/B options looked generic, with nothing tying them to Meta's device.
One image generated (~1.4 credits), `0e43a6ee-788e-494b-aaa2-d22504dde303`:
https://d8j0ntlcm91z4.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/hf_20260925_013656_0e43a6ee-788e-494b-aaa2-d22504dde303.png

The hardware follows reported descriptions (UploadVR, VR.org): chunky glasses-like frame,
magnesium alloy, opaque front, sensors on the temple undersides, nose pads, no strap, thin cable
to a ~two-phone-sized puck. No Meta imagery used. Text: "META" / ~~VR HEADSET~~ / "$1,299 GLASSES".
Name in plain text only, no logo. Credit rule from now on: **generate one image at a time and ask before any more.**
