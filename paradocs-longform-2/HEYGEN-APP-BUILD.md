# Build Sheet — Long-Form 2 in the HeyGen app

**Everything is ready. This is a keyboard task, ~15 minutes.** The API path failed and burned
~45 credits producing nothing; the app is the route actually proven to make long-form on this
account. No further API renders have been fired — **54 credits are intact.**

## Files you need

| File | What it is |
|---|---|
| **`app-prompt.txt`** | ⬅ **Paste this whole file into the Video Agent.** Brief + verbatim script + full imagery map |
| `VO-FINAL.txt` | The narration alone (1,348 words), if you'd rather paste the script separately |
| `thumb-longform-A.png` | Thumbnail — **recommended** |
| `thumb-longform-B.png` | Thumbnail — alternative |
| `SCRIPT.md` | Fact table, packaging, title/description/chapters |

`app-prompt.txt` is 13,773 characters — deliberately longer and richer than what the API
allowed. The app has no 10,000-character cap, so it carries the full scene-by-scene imagery map.

---

## Settings — must match the series exactly

| Setting | Value |
|---|---|
| **Style** | Economist — `e7f9a12679ec426099db7646b70a4639` |
| **Voice** | Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad` |
| **Orientation** | **Landscape 16:9** ← different from the Shorts |
| **Mode** | Chat (the app's normal flow) |
| **Captions** | **ON** ← see below |

## Steps

1. Open the HeyGen app → **Video Agent** → new session.
2. Set **landscape 16:9**, the Economist style and the Alex Wright voice **before** generating.
3. Paste the entire contents of `app-prompt.txt`.
4. **Wait for the blueprint. Do not skip it.** ← this is the whole reason the app beats the API
5. **Turn captions ON** in the video settings.
6. Approve, generate, and publish the captioned cut.

### Step 4 is the one that matters
The API's `generate` mode is fire-and-forget: constraints get one shot and cannot be repeated.
`STYLE-GUIDE.md` §7 says restating them at blueprint approval is *what makes them survive
generation* — and that step has been unreachable through the API all day.

When the blueprint appears, **reply with this before approving**:

> Before you generate, hold to these exactly:
> — Every scene's base layer is cinematic photographic imagery filling the frame. Never
>   typography on flat colour or a white background.
> — Grade all imagery dark and desaturated. Near-black, white, one red accent only.
> — Every number counts up physically: $30,000, $25,000–27,000, $725 million, $1,199, $1,299, +$100.
> — Hero shot is the silicon wafer, camera pushing into the die grid.
> — Bookend on the same empty lit stage, identical camera position at open and close.
> — No faces, no people, no Apple or TSMC logo, no recognisable phone.
> — "Educational only. Not financial advice." on screen in the first 4 seconds.
> — Narration verbatim. Do not alter a single figure.

Then check the blueprint's own scene list against that before you hit approve. **Anything wrong
at blueprint stage is free to fix. After generation it costs another render.**

### Step 5 — captions
`caption.enabled: false` has come back on **all five** renders this account has produced,
including both Shorts today. In the app it is a toggle. **Turn it on**, and you fix in one
click a defect that has silently shipped on every video so far.

If it still generates without them, HeyGen produces a separate captioned cut — publish that
one, not the bare render.

---

## ⚠️ The app is not free
App renders draw on the **same 54 premium credits**. The advantage isn't cost, it's that the
blueprint step lets you approve *before* it spends — which is exactly what the API couldn't do.
Credits reset **2026-10-06**.

---

## VERIFICATION — watch it before publishing
You can actually watch this one; I can't (CDN egress is blocked here).

| # | Check | Why it's on this list |
|---|---|---|
| 1 | Captions burned in and legible | Failed on all 5 previous renders |
| 2 | "Educational only. Not financial advice." in first 4s | Non-negotiable — names a listed company on launch day. `longform-1` appears to lack it |
| 3 | Wafer-price footnote on screen | The spoken caveat is in the script; the on-screen one needs eyes |
| 4 | **No Apple or TSMC logo, no recognisable iPhone** | Highest drift risk — the script names both companies repeatedly |
| 5 | No faces — no Moore portrait, no executives, no audience | A keynote-topic brief invites all three |
| 6 | Real imagery, not type on flat colour | The `longform-1` failure mode |
| 7 | Numbers count up | `longform-1` visualised none |
| 8 | Narration verbatim vs `VO-FINAL.txt` — **especially every figure** | Fact integrity |
| 9 | Bookend matches at open and close | |
| 10 | ~8 min, 16:9 | |

---

## Publishing

**Title:** The iPhone Didn't Get More Expensive. The Transistor Did.
*(HeyGen will auto-title it something else — ignore that, it has done so on every render.)*

**Thumbnail:** `thumb-longform-A.png`. It carries the thesis and still shows $30,000 as a
secondary callout. B will likely out-click it but front-loads the least-audited number in the
video.

**Description, chapters, hashtags and the pinned comment** are all written in `SCRIPT.md` under
PACKAGING. The description already carries the wafer-price caveat and the compliance line —
don't drop either.

**Order:** long-form first, then Shorts 3 and 4 as feeders pointing at it
(`LONGFORM-GUIDE.md` §5). Both Shorts are rendered and waiting.

---

## If you want it longer
The app has no character cap, so the 8-minute trim was an API constraint that no longer
applies. The full 16-beat structure supports ~11 minutes — the length `longform-1` ran. Say the
word and I'll expand `VO-FINAL.txt` back out, re-verifying every added claim first.
