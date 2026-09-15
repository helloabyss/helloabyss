# Long-Form Guide — PARADOCS10X

`STYLE-GUIDE.md` is written for 45–70 second Shorts. **Its motion rules do not survive
contact with an 11-minute video.** This file is the long-form extension: what carries over
unchanged, what has to change, and the brief template to build from.

Derived from `paradocs-longform-1` — the 11m07s Cybercab video, the only long-form the
channel has made and the proof the format works on the current plan.

---

## 1. What carries over UNCHANGED

Every one of these is a hard channel rule and applies at any runtime:

- **Faceless.** No avatars, no presenters, no identifiable people, ever.
- **No real corporate logos or badges.** Plain text name-tags only.
- **Three-colour editorial palette** — near-black, white, one red accent. Imagery graded dark
  and desaturated. No neon, gradients, sparkles, emoji.
- **Imagery-first.** Cinematic photographic imagery is the BASE layer. Never typography on
  abstract backgrounds.
- **Compliance card** — "Educational only. Not financial advice." on screen in the first 4
  seconds. *Long-form 1 appears to be missing this. Do not repeat that.*
- **The counter-evidence beat is mandatory.** At long-form length it becomes two beats — see §4.
- **Fact-check before scripting.** Every claim into a fact table with a confidence level.
  Analyst and company numbers marked as estimates, never as prices.
- **No clickbait, no follow-bait.** Close on something the viewer can act on.
- **Tone:** dry, confident, analytical newsroom.
- **Voice:** Alex Wright – Informative `0db3abd83c74452fb2460b0dd113daad`. Never changes.
- **Sign-off:** *"This is Paradocs 10X. Think ten times further."*

---

## 2. What CHANGES for long-form

| | Shorts | Long-form |
|---|---|---|
| **Orientation** | `portrait` 9:16 | **`landscape` 16:9** |
| **Runtime** | 45–70s | 8–15 min |
| **Script length** | 135–170 words | **~1,300–2,500 words** |
| **Scene length** | under 2s | **20–30s** (long-form 1 averaged 23.8s) |
| **Scene count** | 8–12 | **~2.5 per minute** (long-form 1: 28 scenes / 11 min) |
| **Structure** | hook → define → case → counter → close | **16-beat spine, §4** |
| **Chapters** | n/a | **Required** — YouTube timestamps in the description |

### The pacing rule, restated for long-form
The Shorts guide says *"cut or punch in every 1.2–1.8s, no shot past 2s."* Taken literally at
11 minutes that is ~400 scene changes — unrenderable, and exhausting to watch.

**Reinterpret it as motion within the scene, not scene changes.** A long-form scene holds one
background for 20–30 seconds, and inside that window the camera never rests: slow push,
parallax drift, a graphic building, a number counting up, type arriving. The *frame* keeps
moving at Shorts energy; the *shot* doesn't change.

**Nothing in long-form 1 moved at all** — 28 still images with voiceover. That is the gap to
close, and the single biggest available quality win.

### Word-count maths
Long-form 1 ran **~166 words per minute** with the house voice. Use it to size a script:

| Target | Words | Scenes |
|---|---|---|
| 8 min | ~1,330 | ~20 |
| 10 min | ~1,665 | ~25 |
| **11 min** *(proven)* | **~1,850** | **28** |
| 12 min | ~2,000 | ~30 |
| 15 min | ~2,500 | ~38 |

Roughly **66 words per scene**. Write scenes as paragraphs, not sentences.

### ⚠️ The 10,000-character prompt cap
`create_video_agent` accepts a prompt of **1–10,000 characters**, and the brief has to fit in
there alongside the script. A verbatim 1,850-word script is ~10,500 characters on its own.

**Practical ceiling for a single-call verbatim long-form: ~1,350–1,400 words, about 8 minutes**
(a ~1,350-word script plus a tight brief lands near 9,950). `paradocs-longform-2` was trimmed
to 1,348 words for exactly this reason.

**Never solve it by sending a shorter prompt and letting the agent expand it.** Anything it
writes is unverified, and this channel publishes finance content — an invented figure is a
fact-check failure, not a style one.

For genuinely longer pieces (`paradocs-longform-1` ran 11 minutes) the single-call route will
not work. Options: build it in the HeyGen app rather than the API, or render in two parts and
join them. Neither has been tested from here — **test before promising a runtime over 8 minutes.**

---

## 3. The three-layer stack at long-form length

Same stack, different workload — 11 minutes of a static BASE layer reads as a slideshow.

| Layer | Long-form job |
|---|---|
| **BASE** | One cinematic image or plate per scene, **always in motion** — slow push, drift, parallax. Never locked off. |
| **MID** | **This is where long-form is won.** Every number in the script gets a graphic: counters counting, charts drawing, comparison bars, timelines advancing, maps lighting up. |
| **TOP** | Hero typography on the 6–10 biggest lines only, plus burned-in captions throughout. Restraint — 11 minutes of kinetic type is unwatchable. |

**Rule of thumb:** if a scene contains a number, the MID layer must show it. Long-form 1's
script has *15 million Model Ts*, *$825 → $260*, *12 hours → 93 minutes*, *20¢ vs 80¢ vs
$2–3 per mile*, *95% parked*, *6,000 miles of railway*. None were visualised. All should have
been.

**Bookend rule holds:** open and close on the same location or object. Long-form 1 does this
correctly (scenes 0 and 25 share a background).

---

## 4. The 16-beat spine

This is the structure that produced long-form 1. It is a strong default, not a straitjacket —
but the beats in **bold** are not optional.

| # | Beat | Share |
|---|---|---|
| 1 | **Cold open** — a specific scene, a date, a concrete image. Never a definition | 4% |
| 2 | **The mistake almost everyone is making** — name the wrong frame | 4% |
| 3 | **Thesis + roadmap** — "in this video we're going to…" | 5% |
| 4 | Stakes + transition into the history | 3% |
| 5 | **Historical case A** — full arc: origin → the cost breakthrough → the skeptics → what actually happened | 20% |
| 6 | **Historical case B** — a second, closer parallel with the same arc | 16% |
| 7 | **The hinge** — "Do you see the pattern yet?" Name the pattern explicitly. Sits at the midpoint | 4% |
| 8 | **The subject, precisely** — just the facts of the thing, no interpretation | 5% |
| 9 | **The economics** — the number, next to what the viewer pays today | 7% |
| 10 | The mechanism — *why* the number is possible | 5% |
| 11 | Second-order effects — household, street, city | 7% |
| 12 | **The honest counter** — who gets hurt. Stated without flinching | 5% |
| 13 | The counter to the counter — what history says comes back | 5% |
| 14 | **The serious skeptics** — real objections, explicitly distinguished from silly ones | 6% |
| 15 | **Signals to watch** — 3 falsifiable future observables, each mapped to a historical turning point | 5% |
| 16 | **What it means for you** + recap + sign-off | 6% |

### Why this works
- **Two historical cases before the subject.** The viewer has accepted a pattern twice before
  the thesis is applied to anything current. The argument is won before it's made.
- **The counter-evidence is doubled** (beats 12 and 14) — the human cost, then the technical
  and regulatory objections. This is what makes it an explainer rather than a promo.
- **Beat 15 is the payload.** Three named, checkable signals, each tied back to a historical
  moment ("that's the Watt condenser", "that's the station town"). It converts an essay into
  a tool. **Reuse this device every time.**
- **Beat 16 satisfies the actionable-close rule** on its own. It needs no like/subscribe
  appended — and per house rules, must not have one.

---

## 5. Packaging

- **Chapters.** Map beats to YouTube timestamps in the description. Roughly one chapter per
  major beat — 8–12 chapters for a 10–12 minute video.
- **Title.** Same no-clickbait rule. Long-form 1's *"The Cybercab Isn't a Car. It's the Next
  Steam Engine."* is the model: a claim, stated flatly, that a viewer can disagree with.
- **Description.** Thesis paragraph → chapter list → **corrections and caveats** → "Educational
  only. Not financial advice."
- **Pinned comment.** Pre-empt the strongest objection to the video's weakest claim, exactly
  as `paradocs-short-1` does.
- **Shorts as feeders.** Beats 1, 7 and 15 each cut down to a standalone Short. The channel
  already works this way — the "Nine Feet of Manure" short is beat 6 of long-form 1.
  **Script the long-form first, harvest the Shorts from it.**

---

## 6. HeyGen brief template — long-form

> Create a ~[N]-minute **landscape (16:9)** explainer video for a FACELESS finance channel.
>
> **CRITICAL:** NO avatar, NO presenter, NO human face anywhere. Voiceover only.
> Use this narration script VERBATIM — do not rewrite, shorten, or add to it:
> "[SCRIPT]"
>
> **PACING:** Roughly [N×2.5] scenes, each holding 20–30 seconds of narration. Do NOT cut
> every 2 seconds — this is long-form. Instead keep continuous motion WITHIN each scene.
>
> **LAYER STACK — imagery-first, three layers:**
> 1. BASE — cinematic photographic imagery filling the frame, **always moving**: slow camera
>    push, parallax drift, never a locked-off still.
> 2. MID — motion graphics over that imagery. **Every number in the script must be
>    visualised**: counters count up, charts draw themselves, comparison bars build,
>    timelines advance.
> 3. TOP — hero typography on the biggest lines only, plus burned-in word-by-word captions
>    throughout, current word highlighted.
>
> **IMAGERY BY BEAT:** [map each scene to a concrete shot; mark the hero shot; bookend the
> video on the same location]
>
> **LOOK:** Strict three-colour editorial palette — near-black, white, one red accent. Grade
> imagery dark and desaturated; reserve red for graphics and type. Dark scrim behind captions
> over busy plates.
>
> **HARD CONSTRAINTS:** No human faces or identifiable people. No real corporate logos —
> plain text name-tags only. No neon, gradients, sparkles, emoji, subscribe animations or
> clickbait arrows. Show "Educational only. Not financial advice." in the first 4 seconds.
>
> **TONE:** Dry, confident, analytical newsroom. Cinematic, not a commercial. A neutral
> explainer that includes the negative data, not a promo.

Settings: `mode: chat`, `orientation: landscape`,
style `e7f9a12679ec426099db7646b70a4639`, voice `0db3abd83c74452fb2460b0dd113daad`.

---

## 7. Production notes

- **Captions have failed on every render so far** — all three shorts and long-form 1 came back
  `caption.enabled: false`. Assume it will happen again. HeyGen produces a **separate captioned
  cut** at `captioned_video_url`; publish that one, and check its styling against house style.
- **Restate the constraints at blueprint approval.** In `chat` mode the agent pauses for
  approval; repeating the grade, bookend, motion and MID-layer rules at that point is what
  makes them survive generation. This matters more at 11 minutes than at 45 seconds.
- **Budget the credits.** The 11-minute render was affordable within a 129-credit balance, but
  check `get_current_user` before starting and don't assume a re-render is free.
- **Verify the fact table before writing, not after.** A wrong claim in an 11-minute video is
  buried where nobody will find it until a commenter does. Long-form 1 shipped with a claim
  the channel's own short had already corrected.
- **Long-form 1 has no session record** — it predates session logging. Record the session ID
  in `PRODUCTION.md` at creation time, not afterwards.
