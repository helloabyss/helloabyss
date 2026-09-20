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
