# RENDERING — how TWIM episodes get made

**Decision record, 2026-09-20.** Which connected resource renders this series, and why.

---

## The problem the choice has to solve

TWIM is a **data show**. A beat is "core PCE came in at two point six percent" over a chart
whose axis is labelled, whose line is in the right place, and whose source stamp reads
`as of 2026-09-18 close`. `COMPLIANCE.md §7` requires the as-of on screen; `§7` also forbids
an unlabelled axis crop that exaggerates a move.

**A generative video tool cannot do this.** HeyGen's video agent, AgentOpus, Higgsfield and
vidIQ all *invent* imagery from a prompt. Ask any of them for a chart and you get something
chart-shaped, with plausible-looking numbers. For this channel that is not an aesthetic
problem, it is a **compliance failure** — a hallucinated axis label is a false statement of
fact on screen.

So the requirement is **deterministic rendering**: pixels I specify, not pixels a model
imagines.

## Live status of every candidate (checked 2026-09-20)

| Resource | Credits / state | Deterministic? | Verdict |
|---|---|---|---|
| **HyperFrames (local skills)** | free, renders locally | **Yes — HTML/SVG** | **Chosen for visuals** |
| HeyGen video agent | 0 premium, resets 2026-10-06 | No — prompt-driven | Voice only (see below) |
| HeyGen HyperFrames (hosted MCP) | n/a | No — prompt-driven agent | **Blocked for this client** |
| AgentOpus | PRO, **385 credits** | No | Only generator with capacity; wrong voice |
| vidIQ | 21 credits | No | Scoring (5) yes; thumbnail (22) no |
| Higgsfield | **0 credits** | No | Unusable |
| Adobe | gen-AI unavailable here | Partially | Fonts/images/PDF only, not video |

The hosted HyperFrames MCP rejects `compose`/`render_video` from CLI/IDE clients:
> *"Hosted HyperFrames compose/render is disabled for local CLI/IDE agents… author
> HyperFrames with the local HyperFrames skills instead."*

That pointer is the answer — the **local** skills are better for this job anyway, because
they produce hand-authored HTML rather than prompting an agent.

## The choice: split the job

### Visuals → HyperFrames, locally

HyperFrames renders video **from HTML**. A composition is an HTML file with `data-*` timing
attributes and a paused GSAP timeline. That means charts are SVG with coordinates I compute
— exact values, exact labels, exact palette, every time.

**Proven end to end on 2026-09-20** (`videos/twim-probe/`): 1080×1920, 9.0s, 270 frames,
h264, rendered locally in **8 seconds**. See `videos/twim-probe/frame-chart.png` — axis
labels, FOMC marker, source stamp and the three-colour palette all landed exactly as
authored.

**It also fixes the repo's oldest constraint.** Every HeyGen render in this repo is filed
*complete, not verified*, because CDN egress is blocked and the MP4 can never be watched
from here. A local render lands on local disk — so it can be probed with `ffprobe`, have
frames extracted, and be **actually looked at** before publishing. "Complete, not verified"
stops being the default.

Other fits:
- `/faceless-explainer` skill is literally this format.
- Compositions are text files → diffable, reviewable, committable. `CLAUDE.md` says the repo
  is the durable record; this makes the *visuals* part of that record, not just a session ID.
- `npx hyperframes check` gates on runtime errors, layout and **WCAG contrast** — a real QA
  step before render.
- The renderer **refuses to ship silently-broken output**: the first probe render captured
  all 270 frames then failed because GSAP hadn't loaded, rather than emitting a static video.

### Voice → still HeyGen

The locked channel voice (`VO_PROFILE.md §1`) is Alex Wright – Informative, used by all four
existing videos. **HyperFrames cannot reproduce it.** `npx hyperframes tts` is local
**Kokoro-82M** only — 12 fixed voices (`af_heart`, `am_adam`, …), not the HeyGen library.

So the voice stays where it is, and the standing blocks still apply: 0 premium credits until
**2026-10-06**, and no detached VO stem (`create_speech` needs separate `api` credits).

## The one open question worth testing

`hyperframes auth status` reports:
> *"Not signed in to HeyGen — voice & music will use local engines (free, offline)."*

Signing in with `npx hyperframes auth login` may route voice sourcing through HeyGen
instead of Kokoro. **If that exposes the HeyGen voice library, it would solve two problems
at once** — the locked voice *and* a real detached VO stem, which the MCP `create_speech`
path cannot provide on the Creator plan.

**Unverified.** It needs Sheldon's OAuth, and it may still bill `api` credits. Worth one
test before 2026-10-06. Until then, treat the voice as blocked.

## Setup (reproducible)

```bash
npx skills add heygen-com/hyperframes     # 21 skills → .agents/ (gitignored, 19MB)
sudo apt-get install -y ffmpeg            # encoder + ffprobe
npx hyperframes browser ensure            # headless Chrome for rendering
npx hyperframes doctor                    # expect all-green except optional Kokoro/MusicGen
```

Then per episode:
```bash
npx hyperframes init "videos/<project>" --non-interactive --example=blank --skill=faceless-explainer
npx hyperframes lint      # fast loop while authoring
npx hyperframes check     # full gate: runtime, layout, contrast
npx hyperframes render --quality draft   # `looks` / `delivery` for real encodes
ffprobe -v error -show_format <out>.mp4  # verify
```

### Gotcha: no CDN inside the renderer
The agent proxy blocks `cdn.jsdelivr.net`, so a scaffold's CDN `<script>` tag fails inside
headless Chrome and **blocks the render**. Vendor libraries from npm instead:

```bash
npm install gsap@3.14.2 && cp node_modules/gsap/dist/gsap.min.js vendor/gsap.min.js
```
then reference `vendor/gsap.min.js`. This is better practice regardless — it pins the
library so renders stay reproducible.

## What this means for `/twim`

Phase 8 of `.claude/commands/twim.md` currently sends the whole episode to
`create_video_agent`. Under this decision it splits: **HyperFrames builds the picture,
HeyGen supplies the voice.** That rewrite is deliberately *not* applied yet — it depends on
the auth test above, and on whether the voice is worth waiting for credits. Sheldon's call.

---

## What a week actually costs (measured 2026-09-20)

### HeyGen — derived from this account's own burn, not a pricing page

Two credit checkpoints are recorded in the repo: **501** premium credits at the PDT session
start, and **330** at the paradocs session. Ten renders sit between them and zero.

| Window | Credits spent | Output rendered | Rate |
|---|---|---|---|
| 501 → 330 | 171 | 4 renders · 4.24 min | **40.3 cr/min** |
| 330 → 0 | 330 | 6 renders · 6.82 min | **48.4 cr/min** |
| **All ten** | **501** | **11.06 min** | **45.3 cr/min** |

HeyGen's published rate for Avatar IV/V studio video is **20 credits/min** (Avatar III is 3).
The observed rate is **more than double** that, because `create_video_agent` is a pricier
product than a plain avatar render — it generates scenes, B-roll and motion graphics — and
because failed, stopped and superseded renders still consumed credits. **Plan against the
observed ~45 cr/min, not the published 20.**

**One weekly 2-minute episode, rendered entirely by HeyGen:**

| Basis | Per episode / week | Per month |
|---|---|---|
| Published 20 cr/min | 40 | ~174 |
| **Observed ~45 cr/min** | **~90** | **~394** |
| Observed, with one re-render | ~180 | **~787** |

The Creator allowance is ~600 premium credits/month. **A weekly episode eats most of it, and
the house v1→v2 re-render pattern blows straight through it.** That is why the balance is at
zero — `moat` and `pdt` were each rendered twice.

### Higgsfield — B-roll plates only

Priced with `get_cost` (preflight, no spend). **Model choice is a 3.5× swing:**

| Model | 5s vertical clip | Per second |
|---|---|---|
| `seedance_2_5` (the general-video default) | **35 cr** | 7.0 |
| `kling3_0` | **10 cr** | 2.0 |

A 120s episode cutting every 1.2–1.8s is ~70–100 shots, but a punch-in is a camera move
inside a plate, not a new plate, and the bookend reuses one. Estimate **15–25 distinct
plates**, each generated at 5s and cut several ways.

| Model | 15 plates | 25 plates | Monthly (25 plates, +40% retries) |
|---|---|---|---|
| `kling3_0` | 150 cr/wk | 250 cr/wk | **~1,520** |
| `seedance_2_5` | 525 cr/wk | 875 cr/wk | ~5,320 |

The retry margin is not padding: "no faces, no real logos" (`STYLE-GUIDE.md`) is exactly what
a generative model violates, and a plate with a face in it is regenerated, not fixed.

Balance is **0** on the starter plan; top-ups come in 500 / 1,000 / 2,000 / 4,000 packs. So
weekly B-roll is roughly a 1,000-credit pack per month on `kling3_0`, or a 4,000 pack on
`seedance_2_5`. **Use `kling3_0`** unless a specific plate needs the better model.

### Under the adopted plan

| Component | Weekly credits |
|---|---|
| Charts, type, captions, cards — **HyperFrames, local** | **0** |
| B-roll plates — Higgsfield `kling3_0`, *if used* | 150–250 |
| B-roll plates — stock/archive instead | 0 |
| Voice — HeyGen | the only unavoidable cost |

Moving the picture to HyperFrames removes the ~90–180 cr/week HeyGen render **entirely**.
What remains is the voice, and the cheapest route to it is still the open question in the
section above. Sourcing plates from stock rather than generating them takes the weekly
credit cost to **zero**.

---

## The least-credit path (2026-09-20)

**Answer up front: don't upgrade either plan yet.** The optimal pipeline costs **16–36
credits a week**, against a HeyGen Creator allowance of 600/month and a Higgsfield top-up
floor of 500. Upgrading now buys capacity the architecture below removes.

### The finding that sets the shape: the locked voice cannot be TTS'd

`heygen voice speech create` — the free OAuth TTS path — **requires a starfish-engine voice.**
Alex Wright – Informative (`0db3abd8…`) is **not one.** Checked against
`list_voices engine=starfish` across both sort bands: it should sort between `0cbcaee1…`
and `0e2ff5b9…` (band 1) and between `068f3956…` and `13f70a5d…` (band 2), and is absent
from both. Starfish voices also carry `support_locale` and a null preview URL; this voice
has a real preview URL and no `support_locale`.

**So there is no TTS route to this voice at any price.** It exists only inside a rendered
video. The cheapest legitimate way to obtain it is to **render the smallest possible video
that carries the narration and strip the audio** — the picture is discarded, so the avatar
engine only needs to be cheap.

| Voice carrier | Per episode (2 min) | Per month |
|---|---|---|
| HeyGen CLI avatar video on the **OAuth free-usage allowance** | **0** | 0 |
| **Avatar III studio (3 cr/min)** | **6** | ~26 |
| Avatar IV (20 cr/min) | 40 | ~174 |
| Video agent (observed ~45 cr/min) — *what we do today* | 90 | ~391 |

Rendering a throwaway avatar video purely as a VO carrier sounds wasteful and is in fact the
cheapest correct answer: **the voice is TTS and is independent of the avatar engine**, so the
engine that draws the discarded face should be the cheapest one available. It also returns a
**free SRT sidecar** (`subtitle_url`), which gives caption timings for HyperFrames.

### The other lever: stills, not generated video

`heygen asset search` (image catalog) is on the same **free OAuth path**. `STYLE-GUIDE.md`
requires a cinematic photographic BASE layer with camera motion applied to the imagery —
and HyperFrames applies push, parallax and 3D layer separation to a **still** deterministically.

**So most B-roll is a free catalog still plus HyperFrames motion: 0 credits.** Reserve
generated video for the one or two shots per episode where real motion is the point
(the hero macro), at `kling3_0`'s 10 cr per 5s.

### Weekly budget

| Component | Route | Credits |
|---|---|---|
| Charts, type, captions, cards, all motion | HyperFrames, local | **0** |
| B-roll stills | HeyGen catalog, OAuth free | **0** |
| Music / SFX | HeyGen catalog, OAuth free | **0** |
| Hero motion clips ×1–3 | Higgsfield `kling3_0` | 10–30 |
| Voice carrier | Avatar III render, audio stripped | 6 |
| Thumbnail | HyperFrames frame export | **0** |
| **Total** | | **16–36 / week** |

**≈70–156 credits/month**, split ~26 HeyGen and ~44–130 Higgsfield. Against today's path
(90–180 HeyGen + 150–875 Higgsfield per week) that is roughly a **10–20× reduction**, and the
output is *better*, because the charts become exact instead of generated.

### So what to buy

| | Verdict |
|---|---|
| **HeyGen** | **Don't upgrade.** Creator's 600/mo is ~23× the ~26 needed. The balance resets 2026-10-06. |
| **Higgsfield** | **One 500-credit top-up, not a subscription** — ~3.8 months of hero clips. |

Upgrade later only if the shape changes: HeyGen if you run several series a week, need `api`
credits, or go back to full video-agent renders; Higgsfield if you decide every beat wants
generated motion rather than stills.

### Verify before committing (all blocked here by the 0 balance)

1. `heygen auth login --oauth`, then `node <media-use>/scripts/resolve.mjs --doctor` — confirm
   the free-usage path is live and see whether avatar video and catalog search really cost 0.
2. Render one ~10s Avatar III test with `voiceId` = `0db3abd8…` and confirm the voice is
   preserved and the credit charge matches 3 cr/min. Check `supported_api_engines` on the
   chosen look — Avatar III needs a `digital_twin` or `studio_avatar` look.
3. Strip audio (`ffmpeg -vn`) and A/B it against `moat-short` to confirm the voice matches.
4. Run the **pronunciation audit** (`VO_PROFILE.md §3`) on that stem — the 30 glossary terms
   have still never been heard. Pass `brandGlossaryId` on the carrier render.

### The alternative worth knowing about, not recommended

Adopting a **starfish** voice makes narration free and unlimited via OAuth TTS, and gains
in-script `<break>` pause support (every starfish voice reports `support_pause: true`),
which this voice does not have (`VO_PROFILE.md §5`). It costs voice continuity with the four
existing videos, and the brief says the voice must match previous episodes exactly — so it
stays on the table only if that requirement is ever relaxed.


---

## Confirmed in production, 2026-09-23

The account moved to **Pro (361 credits)** and the first real HeyGen render of this system
landed: `07ec91817c45421993a4eaa90c802b78`, 110.07s, the locked Alex Wright voice, script
verbatim, glossary applied. **74 credits — 40.3 cr/min**, which matches the 40.3–48.4 range
measured from the account's own history above. The estimate held.

Three things the run settled:
- **Chat mode is not reliable.** It stalled at `thinking/progress:0` with no `video_id` for
  7+ minutes, exactly as in `paradocs-short-1`. It costs **nothing** when it stalls, so the
  cost of trying it is only time. Use `generate`.
- **Generate mode disables captions regardless of the prompt.** An explicit "captions must
  be ENABLED" instruction was ignored. The separate `captioned_video_url` cut is the fix,
  and it needs no re-render.
- **The CDN is still blocked**, so a HeyGen render remains *complete, not verified*: scene
  data proves voice, script, glossary and aspect ratio, but never the palette, because a
  full-frame `motion_graphics` plate is opaque to `get_video_scenes`.

The split in this document still stands — HyperFrames for pixel-exact charts and working
captions at zero credits, HeyGen for the locked voice — but HeyGen alone is now a viable
one-shot path when the voice matters more than chart precision.

---

## The "voice carrier" theory is dead, 2026-09-25

The cheapest-production plan in the section above rested on one untested assumption: that
`create_video_from_avatar` with `engine:{type:"avatar_iii"}` would bill at the published
**Avatar III rate of 3 cr/min**, letting HeyGen supply only the locked voice while
HyperFrames drew the picture free. That would have been ~6 cr/video against the 74 cr the
video-agent path costs — a 92% saving. It was worth one test to find out.

**Test render:** `ad3453273f76ba92a36f39d934c2b600`, avatar `Daphne_public_1` (confirmed
`supported_api_engines: ["avatar_iii"]`), voice `0db3abd83c74452fb2460b0dd113daad`,
glossary `c906414830134497906c72eecf054153`, 720p, 9:16, `caption:{file_format:"srt"}`,
first two paragraphs of the MSTR script. Picture discarded by design — only the audio and
the SRT word timings were ever wanted.

**Result: 20.53s of finished video cost 52 credits.** Balance went 287 → 275 while the job
was still processing, then → 235 on completion. That is **≈152 cr/min — roughly 3.8× more
expensive than the 40.3 cr/min video-agent path**, not 13× cheaper. The shape of the
numbers (a small charge on submit, a large one on completion, on a sub-half-minute render)
points to a per-render floor rather than true per-second billing, so the published 3 cr/min
Avatar III rate does not appear to reach this API surface on this plan.

**Consequences, in order of cost:**

| Path | Credits for a ~110s short | Voice |
|---|---|---|
| HyperFrames + local Kokoro `am_michael` | **0** | Not the locked voice |
| HeyGen video agent, `generate` mode | 74 | Locked Alex Wright |
| HeyGen Avatar III "carrier" | ~280 (extrapolated) | Locked Alex Wright — **do not use** |

So the honest cost floor for a video carrying the locked voice is **74 credits**, and at
235 credits remaining that is **three more voiced shorts this cycle** (resets 2026-10-06).
Nothing about the carrier path is worth retrying; it is recorded here so it is not
re-proposed.

**Where the real savings are, cheapest first:**
1. **Cut runtime, not quality.** Billing is per minute of finished video, so a 60s short
   costs ~40 cr against a 110s short's ~74. Two 60s shorts cost about the same as one
   110s short and give twice the upload cadence.
2. **Voice only the episodes that need a voice.** Chart-led explainers render free on
   HyperFrames with on-screen type carrying the argument; the locked voice is worth its
   74 credits on the flagship weekly, not on every cut.
3. **The OAuth free-usage path** (`heygen auth login --oauth`, see
   `media-use/references/setup-providers.md`) is still untested and is the only remaining
   candidate for zero-credit access to a HeyGen voice. It needs the user to run the login
   on their own machine; it cannot be tested from this environment.
4. **Relaxing the voice-match requirement** to a starfish voice makes narration free and
   unlimited. Still the single largest saving available, still the user's call.
