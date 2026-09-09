# Long-Form 2 — Source Capture

**Status: BLOCKED — awaiting source access.** Nothing has been written about this video's
content, because nothing about its content is known. This file is the capture shell.

---

## THE SOURCE

| | |
|---|---|
| **Supplied link** | `https://www.youtube.com/live/39BalPDuTo0?is=xOPy9N0PFhS8oXZk` |
| **Video ID** | `39BalPDuTo0` |
| **Type** | `/live/` — a livestream or a stream archive |
| **Title** | ❓ unknown |
| **Channel** | ❓ unknown |
| **Duration** | ❓ unknown — **matters a lot**, see below |
| **Date** | ❓ unknown |

> Note: the query parameter is `?is=` — YouTube share links normally use `?si=`. Harmless
> either way; the video ID is what resolves. Flagging only in case the link was mistyped and
> points somewhere unintended.

### ⚠️ Not identified — do not assume
A web search for the video ID returned **no page containing it**. A search summary claimed it
was an Apple September 2026 event livestream, but **none of the returned results actually
referenced this ID** — that identification is unsupported and was discarded. Today's date
makes the timing superficially plausible, which is exactly why it should not be trusted.

**The topic of this video is unknown. Do not script from a guess.**

---

## WHY IT COULD NOT BE READ

Every available route was tried. All failed:

| Route | Result |
|---|---|
| `WebFetch` → youtube.com | ❌ `EGRESS_BLOCKED` — blocked by the network egress proxy |
| `curl` → youtube.com/oembed | ❌ `CONNECT tunnel failed, response 403` |
| `curl` → googleapis.com YouTube Data API | ❌ `403` at the proxy |
| **vidIQ** `vidiq_video_transcript` | ❌ Costs **5 credits**, balance is **1** |
| **vidIQ** `vidiq_video_watch` (scene-by-scene) | ❌ Costs **25 credits**, balance is **1** |
| **Higgsfield** `video_analysis_create` (accepts a YouTube URL server-side) | ❌ **0 credits**, plan `starter` |
| Web search for the video ID | ❌ No result containing the ID |

The proxy confirms the denial:
`{"kind":"connect_rejected","detail":"gateway answered 403 to CONNECT","host":"www.youtube.com:443"}`

**Downloading clips, photos or video from the source is not possible from this environment by
any route.** Even if the transcript were readable, media files could not be pulled — the same
proxy blocks `static.heygen.ai`, `resource2.heygen.ai` and `files2.heygen.ai` as well.

---

## HOW TO UNBLOCK — cheapest first

**1. Top up vidIQ to ≥5 credits** *(recommended)*
Balance resets to 150 on **2026-10-03** anyway. Then `vidiq_video_transcript` returns the full
spoken transcript — enough to build the entire script and fact table from. At ≥25 credits,
`vidiq_video_watch` also returns a scene-by-scene visual walkthrough.

**2. Paste the transcript in directly**
Open the video, copy the transcript from YouTube's transcript panel (⋯ → Show transcript), and
paste it into this file under **CAPTURE** below. Costs nothing and unblocks everything.
The title, channel, date and duration are just as useful.

**3. Top up Higgsfield**
`video_analysis_create` takes a YouTube URL and analyses it server-side, returning a
scene-by-scene breakdown. Note its own warning: **the longer the video, the less accurate the
analysis** — for a full livestream this may be weak.

**4. Allowlist `youtube.com` on the environment**
A network-policy change on the remote environment. Fixes it permanently for future sessions.

### If it's a full livestream, read this first
A `/live/` URL is often 1–3 hours. That changes the job:
- A transcript of a 2-hour stream is ~20,000 words. The long-form script needs ~1,850.
- **Roughly 90% of the source gets cut.** The valuable work is selection, not transcription.
- `vidiq_video_watch` degrades on long videos by its own documentation.
- **Better approach for a long stream:** give me the 5–10 timestamp ranges that actually
  matter, rather than the whole thing. A list like *"14:20–19:40 the pricing section,
  1:02:00–1:11:30 the Q&A on margins"* is worth more than the full transcript and costs
  nothing to produce.

---

## CAPTURE — fill this in

Paste raw source material here. Don't polish it; the script gets built from it afterwards.

### Metadata
- Title:
- Channel:
- Published / streamed:
- Duration:
- Why this video matters to PARADOCS10X:

### Transcript / notes

*(paste here)*

### Timestamps worth using
| Timestamp | What happens | Use for |
|---|---|---|
| | | |

### Quotes worth keeping verbatim
| Quote | Speaker | Timestamp |
|---|---|---|
| | | |

### Numbers to fact-check
Every one of these needs a web-search verification pass and a confidence level before it
enters a script — CLAUDE.md, non-negotiable. Company and analyst figures get marked as
estimates, never as prices.

| Claim | Stated in source | Verified? | Confidence |
|---|---|---|---|
| | | | |

### Visual references
Shots, diagrams or moments from the source worth rebuilding as house-style imagery.
**Do not reuse the source's footage** — it will carry logos, faces and a foreign grade, all
banned. Rebuild the *idea* of the shot instead.

| Moment | Shot to rebuild |
|---|---|

---

## READY TO GO ON ARRIVAL

Everything that does not depend on the source is already done:

- ✅ **Format spec** — `LONGFORM-GUIDE.md`: 16-beat spine, 16:9, ~166 wpm, ~66 words/scene,
  the long-form brief template
- ✅ **Precedent recorded** — `paradocs-longform-1/`: full 11m07s transcript, structure
  breakdown, 28-asset manifest, and 5 ranked defects not to repeat
- ✅ **Capacity confirmed** — HeyGen **129 premium credits** (resets 2026-10-06); an 11-minute
  render is proven affordable on this plan
- ✅ **Settings locked** — style `e7f9a12679ec426099db7646b70a4639`, voice
  `0db3abd83c74452fb2460b0dd113daad`, `mode: chat`, **`orientation: landscape`**

**On arrival of the source:** fact-check pass → fact table → script to the 16-beat spine →
imagery map → HeyGen brief → render in chat mode, restating constraints at blueprint approval
→ publish the `captioned_video_url` cut, not the bare one.

---

## OPEN QUESTION — which video is next?

Long-form 1 ends with an on-camera promise to the audience:

> *"the next video breaks down what Tesla's unboxed manufacturing process actually is and why
> it might matter more than the car"*

If this source video is about something else, that promise is left dangling. Worth deciding
deliberately: make the unboxed-process video next, or drop the promise when long-form 1's CTA
is re-cut. See `paradocs-longform-1/PRODUCTION.md`, defect 5.
