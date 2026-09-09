# Production Record — PARADOCS10X Long-Form 1

**Retro-recorded on 2026-09-09.** The render predates the repo's record-keeping rule, so this
file reconstructs it from the HeyGen API rather than from a session log.

| | |
|---|---|
| **video_id** | `5b905bcc1306f5fa70f3f89f56455f30` |
| **Watch** | https://app.heygen.com/videos/5b905bcc1306f5fa70f3f89f56455f30 |
| **Created** | 2026-09-06 (unix `1788762773`) · render took ~8.5 min |
| **Duration** | 666.6s — 11m 07s |
| **Format** | **16:9 landscape**, 1080p, 28 scenes |
| **Voice** | `0db3abd83c74452fb2460b0dd113daad` — Alex Wright, house voice ✅ |
| **Session** | Not recovered — predates session logging |

## Why this file matters

This is the **only long-form PARADOCS10X video that exists**, and it is the proof that the
format is viable on the current plan. Before it was recorded here, nothing in the repo
described it.

---

## VERIFIED FROM SCENE DATA

Read from `get_video_scenes`, **not from watching** — HeyGen CDN egress is blocked.

| Check | Result |
|---|---|
| House voice across all 28 scenes | ✅ **PASS** |
| 1080p | ✅ **PASS** |
| Bookend (scene 0 and scene 25 share a background) | ✅ **PASS** |
| Counter-evidence beat present (scenes 19, 21) | ✅ **PASS** — and unusually well done |
| Actionable close (scene 24, three concrete actions) | ✅ **PASS** |
| **Burned-in captions** | ❌ **FAIL** — `caption.enabled: false` |
| **MID layer — motion graphics** | ❌ **FAIL** — `elements: []` on all 28 scenes |
| **TOP layer — hero typography** | ❌ **FAIL** — no text elements anywhere |
| **Compliance card** ("Educational only. Not financial advice.") | ❌ **FAIL** — no text element exists to carry it |
| Imagery grade / three-colour palette | ❓ **UNKNOWN** — needs human eyes |
| Orientation | ⚠️ 16:9 — correct for long-form, but note the shorts are 9:16 |

**What it actually is:** 28 full-frame background images with voiceover over the top. A
narrated slideshow. The BASE layer is right — real imagery, not abstract texture — but the
MID and TOP layers of the house stack are entirely absent.

---

## DEFECTS TO FIX IN LONG-FORM 2

Ranked. The first is a credibility problem, not a style one.

### 1. ❌ The 1894 claim contradicts the channel's own short
Scene 9 asserts *"a London newspaper famously predicted…"* as fact. `paradocs-short-1` was
**rebuilt specifically to correct this** — the quote is unsourced and The Times refuted the
attribution in 2018.

The channel currently publishes both the myth and its correction. Whichever a viewer sees
second undermines the other, and "this is a debunked myth" is exactly the top comment the
short was rebuilt to prevent.

**Fix:** re-cut scene 9 to the short's framing — *"You've heard this one… no one has ever
found that article. But the crisis underneath it was real."* The Ford payoff is unaffected;
it lands harder. Until it is re-cut, carry the correction in the video description and a
pinned comment.

### 2. ❌ No compliance card
CLAUDE.md requires **"Educational only. Not financial advice."** on screen in the first 4
seconds of every video. This video has no text elements at all, so it cannot be carrying one.
This is the one non-negotiable in the whole guide. Verify by eye; if confirmed absent, add it
to the description immediately and fix on re-cut.

### 3. ❌ Captions disabled
Same defect as both shorts. HeyGen produces a separate captioned cut —
`captioned_video_url` on the video record. **Publish that cut, not the bare one.**

### 4. ❌ Missing MID and TOP layers
No motion graphics and no hero typography across 11 minutes. The script is full of numbers
that the house style says must *count up physically* — 15 million Model Ts, $825 → $260, 12
hours → 93 minutes, 20¢ vs 80¢ vs $2–3 per mile. None of them are visualised.

This is the single largest quality gap and the biggest available win.

### 5. ⚠️ The CTA is follow-bait
Scene 27 — *"hit like… Subscribe, because…"* — is exactly what CLAUDE.md bans: *"No
subscribe animations, no 'what they don't want you to know' CTAs. Close on something the
viewer can act on."*

The video **already has** the compliant close: scene 24's three actions, and scene 26's
*"Watch the cost. Not the car."* Scene 27 is redundant on top of a better ending.
**Recommendation:** cut the like/subscribe sentences, keep the comment question and the
sign-off.

---

## ASSET MANIFEST — 28 backgrounds

**These could not be downloaded from this environment.** `static.heygen.ai`,
`resource2.heygen.ai` and `files2.heygen.ai` all fail the egress proxy with
`CONNECT tunnel failed, response 403`. The URLs are recorded here so the assets can be pulled
from any machine with normal network access.

**Urgency:** the `static.heygen.ai/tmp_resource/…` URLs carry **no signature or expiry** and
are likely durable, but the path segment `tmp_resource` suggests they are not guaranteed to
be. **Pull these to local storage soon** — they are the only copy of this video's imagery.

| Scene | Beat | Asset |
|---|---|---|
| 0 | Cold open · **BOOKEND** | `resource2.heygen.ai/image/ed0593512d86441e8f2a018bc0b1a24b/original.jpg` |
| 1 | The mistake | `static.heygen.ai/tmp_resource/4d7d4503-a52d-467f-9fcb-e50c6aca7c4c` |
| 2 | Thesis | `static.heygen.ai/tmp_resource/e1b46ed5-6198-4d6a-9bb2-badbb3c6bbd9` |
| 3 | Stakes / coal mine | `static.heygen.ai/tmp_resource/42fa9a9e-3767-4b24-bbe9-c6b39c760bf4` |
| 4 | Newcomen | `static.heygen.ai/tmp_resource/63c1dbaa-9ce5-435e-a8a0-f2de30c9882e` |
| 5 | Watt | `static.heygen.ai/tmp_resource/da058423-41bf-4ed0-a1d5-e33bd023d165` |
| 6 | Rainhill / Huskisson | `static.heygen.ai/tmp_resource/91b47b5f-6b28-419a-807f-933182642b6d` |
| 7 | Loud skeptics | `static.heygen.ai/tmp_resource/4aa5f14a-a610-47a6-be25-aa6f63debb8a` |
| 8 | Railway boom | `static.heygen.ai/tmp_resource/ebcadb38-dcd2-471c-b6f2-c5146bdd2389` |
| 9 | Horse crisis ⚠️ | `static.heygen.ai/tmp_resource/98388278-3ed9-463c-9d0d-bdc5df19a18d` |
| 10 | Ford's failures | `static.heygen.ai/tmp_resource/7d2d820f-28a0-47ab-8063-4415d7255ebe` |
| 11 | Model T launch | `static.heygen.ai/tmp_resource/8d5e8beb-d52e-4c9a-af5c-eaf303056a36` |
| 12 | Assembly line | `static.heygen.ai/tmp_resource/3cf41a19-5244-4e68-8052-008c2e344521` |
| 13 | The hinge | `static.heygen.ai/tmp_resource/97eaf89a-1e83-4f3c-b37f-c36d2a2979e9` |
| 14 | Cybercab specs | `static.heygen.ai/tmp_resource/c2497974-561d-40a5-93c7-f3ade0603235` |
| 15 | Price comparison | `static.heygen.ai/tmp_resource/0f7e3a59-2002-4a64-8fcd-eeb2d2e0c2f2` |
| 16 | Utilization / 95% parked | `static.heygen.ai/tmp_resource/8945f886-6150-4a00-8cd8-66817f46813e` |
| 17 | The household | `static.heygen.ai/tmp_resource/cce25b3d-1c61-43ac-946a-0661c4664ea8` |
| 18 | The city | `static.heygen.ai/tmp_resource/2cf6ef1f-4433-4a18-ba56-b8894f8f172a` |
| 19 | Jobs destroyed | `static.heygen.ai/tmp_resource/ba3adcf3-4bf0-41c0-a46b-4823a8ad7e0f` |
| 20 | Jobs created | `static.heygen.ai/tmp_resource/4a8f9c16-c53f-4f6a-a218-a51b2e394b27` |
| 21 | Serious skeptics | `static.heygen.ai/tmp_resource/53575fdb-c606-4a4e-a139-50f16e1ff639` |
| 22 | The rebuttal | `static.heygen.ai/tmp_resource/72f6e402-226d-4786-87f7-e234134e1e21` |
| 23 | Three signals | `static.heygen.ai/tmp_resource/566e27f3-b75a-468a-ba58-a37e4b56059a` |
| 24 | What it means for you | `static.heygen.ai/tmp_resource/163b3716-e8dd-4264-a33f-76079c01f58c` |
| 25 | Claim restated · **BOOKEND** | `resource2.heygen.ai/image/ed0593512d86441e8f2a018bc0b1a24b/original.jpg` |
| 26 | Recap | `static.heygen.ai/tmp_resource/aa071a83-af9e-4e5b-8452-2d19f038f1e1` |
| 27 | CTA | `static.heygen.ai/tmp_resource/226a198f-b56c-4586-bd66-20c58ba5a54b` |

### Expiring URLs — pull before they lapse
The render, caption cut and subtitles are behind **signed** CloudFront URLs:

- `video_url` and `subtitle_url` — signature expired **2026-09-14 06:42 UTC**
- `thumbnail_url` — signature expired **2026-09-16 16:30 UTC**
- `captioned_video_url` — the publishable cut, same signing scheme

Signed links are re-issued each time `list_videos` / `get_video` is called, so they can always
be regenerated from the API. **Nothing is lost** — but they cannot be pasted into a document
and used later.

---

## CONSTRAINTS HIT THIS SESSION

| Constraint | State on 2026-09-09 |
|---|---|
| HeyGen credits | **129 premium**, resets 2026-10-06. This 11-min render is affordable |
| HeyGen CDN egress | ❌ Blocked — `files2`, `resource2` **and `static.heygen.ai`** all 403 at the proxy |
| YouTube egress | ❌ Blocked — `www.youtube.com` and `googleapis.com` both 403 |
| Higgsfield | ❌ **0 credits**, plan `starter`. No B-roll generation |
| vidIQ | ❌ **1 credit** (0 renewable + 1 add-on), resets 2026-10-03. Transcript costs 5, watch costs 25 — **both unaffordable** |

**Net effect:** no video, image or transcript can be fetched into this environment by any
available route. Text-based API metadata is the only channel that works.

---

## THE NEXT VIDEO IS ALREADY PROMISED

Scene 27 commits on camera to a specific follow-up:

> *"the next video breaks down what Tesla's unboxed manufacturing process actually is and why
> it might matter more than the car"*

That is a **published promise to the audience**. If long-form 2 is about something else, this
promise is left dangling. Either make the unboxed-process video next, or drop the promise when
the CTA is re-cut (see defect 5) — but don't leave it unaddressed.
