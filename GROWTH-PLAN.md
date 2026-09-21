# Growth Plan — faceless finance shorts

Written 2026-09-21. Owner: Sheldon. This is the project-management view: what is actually
true today, what the constraint is, and what connects to what.

---

## 1. Two channels, two lanes — RESOLVED 2026-09-21

There are two channels and they do not share a strategy, an audience or a publishing path.

| | **The Meticulous Investor** | **PARADOCS10X** |
|---|---|---|
| Lane | **Faceless finance — this repo** | AI / tech |
| Subscribers | **6** | 57 |
| Channel ID | *needed — see below* | `UCX2_NXOHIgXUQFsBOub65HQ` |
| vidIQ visibility | Not indexed (too small) | Indexed, connected |
| OpusClip / AgentOpus publishing | **Not connected** | Connected (`6797cd6d213f56bd20026a41`) |
| Status | **Active focus** | Parked |

**Decision:** all work in this repo targets **The Meticulous Investor**. The existing
OpusClip and AgentOpus scheduling connection stays **reserved for PARADOCS10X** — it is not
to be repointed at the finance channel. The tech channel keeps its own scheduling lane for
whenever it's picked back up.

### What a 6-subscriber channel actually means

This is the good case, not the bad one. A near-empty channel has **no mis-trained
recommendation surface**. PARADOCS10X's problem is that YouTube has three years of evidence
that its audience wants Cybertruck and AI content — which is why finance shorts posted there
drew 15–138 views. The Meticulous Investor has no such baggage. Every video is a clean signal.

Treat it as a cold start and optimise for **topical consistency above all else**. Do not post
anything off-lane for the first 90 days. One off-topic video on a 6-sub channel is a
meaningful fraction of the classification evidence.

### Blocked on you — two inputs needed

1. **The channel handle or URL** for The Meticulous Investor. vidIQ can't find it by search
   (channels this small aren't indexed), so I can't pull its stats, competitors or baselines
   without the ID.
2. **Authorise the tooling against it.** `vidiq_authorize_with_youtube` currently points at
   `paradocs10x@gmail.com`. Publishing automation stays unwired until the finance channel has
   its own connection — I will not repoint the tech channel's.

## 2. What the constraint actually is

It is not production quality. The three shorts already in this repo are well-built and on-style.

**The constraint is cadence and news-latency.** The repo has 3 finished shorts. The channel
published 5 videos in 30 days and gained 0 subscribers. Meanwhile:

- Humphrey Yang published an **82-second** Fed short on 2026-09-16 → **286,270 views**, outlier score 4.16.
- Graham Stephan published a 14:54 version the same day → 818,059 views.
- CNBC Television's **35-second** Tom Lee clip → 45,787 views.

The Fed hiked on September 16. Every one of those went up within hours. A perfect short
published on September 23 gets a fraction of a good short published on September 16.

**So the plan optimises for turnaround, not polish.** The house style is already locked and
written down precisely so it costs no decision time.

---

## 3. What is working in this niche — the format to copy

From `vidiq_youtube_search` on the actual Fed story, ranked by pull:

| Pattern | Evidence |
|---|---|
| **Flat declarative news title.** No question marks, no curiosity gap. | Humphrey Yang — "The Federal Reserve Just Raised Interest Rates For The First Time Since 2023", 286k |
| **60–90 seconds.** Long enough to carry a real fact, short enough to complete. | Yang 1:22; CNBC 0:35 and 0:28 both outliers |
| **Publish inside the news window.** | Every outlier above is dated 2026-09-15 or -16 |
| **A named counter-voice raises watch time.** | CNBC's two Tom Lee clips both outlier ≥2.6 — the *disagreement* is the hook |
| **Breakout channels are new and narrow.** | Lock Stock Finance: founded Feb 2025, 201k subs, +4,912% subs/yr, 86 videos, one niche |

That last row matters most. The channels breaking out in finance right now are two years old
and topically disciplined. Not big, not old — **narrow and frequent.**

The channel's existing differentiator — the mandatory counter-evidence beat — is not a
handicap. CNBC's best-performing clips this week were *disagreement* clips. Lean into it.

---

## 4. The stack — what to keep, what to drop

You are paying for twelve things. Several are duplicates, and two that you own are doing
nothing.

### Keep — these are load-bearing

| Tool | Job | Status |
|---|---|---|
| **Claude (here)** | Research, fact-checking, scripting, repo, orchestration | Working |
| **HeyGen** | Render — the only tool producing finished house-style video | **Pro, 372 credits** |
| **vidIQ** | Demand research, competitor data, title validation | 41 credits — research is free, generation isn't |
| **OpusClip** | **Scheduled publishing to YouTube + X** | Connected, unused — see §5 |
| **DaVinci Resolve** | The one editor you need for fixes and grade | Free tier is enough |

### Underused — you own these and they're idle

| Tool | What it can do that you aren't doing |
|---|---|
| **Higgsfield** (564 credits) | `CLAUDE.md` said 0 credits, so B-roll was written off. You can buy specific hero shots — the pendulum, the mooring rope — instead of hoping HeyGen finds them. |
| **AgentOpus** (PRO, 385 credits) | Second render path. Also motion graphics ≤10s — ideal for the compliance card and repeated lower-thirds so they're identical across videos. |
| **Adobe** | Thumbnail production in the locked palette, at no vidIQ credit cost. |

### Consolidate — you're paying twice

- **CapCut + DaVinci + Final Cut.** Three editors for a pipeline whose output arrives finished
  from HeyGen. Pick **one**. Resolve, unless you're already fast in Final Cut. Drop CapCut.
- **OpenAI + Grok + Meta AI + Claude.** Four general models. This pipeline's bottleneck is
  *verified* facts, and the verification lives here with the repo, the style guide and the
  agents. Keep **one** second model for adversarial review — Grok, for its live-feed access on
  breaking stories — and cancel the rest, or drop them to free tiers.

**Estimated saving: 3–4 subscriptions, with no capability lost.** That money is better spent on
vidIQ's renewable pool (currently 0/150) than on a fourth chat model.

---

## 5. Interconnection — what should be wired, and what already is

This is the part you asked about, and it's where the biggest unclaimed win is.

### The pipeline today

```
research → script (repo) → HeyGen render → [MANUAL DOWNLOAD] → [MANUAL UPLOAD] → YouTube
                                                  ↑
                                     everything stops here
```

The repo's own record says it: *"HeyGen CDN egress is blocked… renders cannot be downloaded."*
Every video so far has required you to leave the pipeline, fetch the file by hand, and upload it.

### What's already connected that nobody used

`opusclip_list_social_accounts` returns:

| Platform | Account | ID |
|---|---|---|
| YouTube | PARADOCS10X | `6797cd6d213f56bd20026a41` |
| X / Twitter | TROY 🇯🇲 (@troybillion) | `67c7dc59bbc8c480458731cc` |

**OpusClip can schedule posts to both.** So can AgentOpus (`agentopus_schedule_publish`), and
vidIQ has `vidiq_video_upload` and `vidiq_instagram_publish_reel`. The distribution leg was
never the missing piece — it was sitting unused.

⚠️ **OpusClip is at 87% of its monthly API cap (52/60 hours), resetting 2026-10-01.** Do not
run bulk clipping through it this month. Publishing costs far less than analysis — use it for
scheduling only until the reset.

### The pipeline to build

```
        ┌─ scout ──────────── WebSearch + vidIQ research      (free)
        ├─ fact-checker ───── WebSearch, 2 sources per claim   (free)
 repo ──┼─ scriptwriter ───── verbatim VO from fact table      (free)
        ├─ art-director ───── shot list → HeyGen brief         (free)
        │                        └→ Higgsfield hero shot       (opt, ~credits)
        ├─ HeyGen render ──── chat mode, revisable             (1 credit)
        ├─ packager ───────── titles vs live outliers          (free)
        └─ OpusClip schedule → YouTube + X, same asset         (minimal)
                 └→ you verify the render once, on your phone
```

**Three links to build, in priority order:**

1. **Render → publish.** Register the finished HeyGen asset with OpusClip and schedule it.
   This removes the manual step that currently gates every upload. **Blocked: The Meticulous
   Investor is not connected to OpusClip.** The only YouTube account there is PARADOCS10X, and
   that connection is reserved for the tech channel (§1) — it must not be repointed.
2. **One asset → two platforms.** Every short should post to YouTube and X from the same
   render. The X account (@troybillion) is already connected and has never been used — and
   unlike the YouTube slot it is channel-agnostic, so **this one is usable today.** Free reach
   for finance shorts with no new auth required.
3. **Calendar + repo.** Google Calendar is connected. Put the FOMC dates, CPI release dates and
   earnings dates in it, and have the weekly cycle read from it — so the scout starts the week
   already knowing what's scheduled to happen.

### Left deliberately unwired
- **Gmail / Drive.** No role in this pipeline. Don't connect them to it.
- **Auto-publishing without your review.** The render cannot be watched from here — CDN egress
  is blocked. **A human must watch every video before it goes out.** Schedule, don't auto-post.

---

## 6. The weekly cycle

Full operating detail in `WEEKLY-RUNBOOK.md`. Summary:

| Day | Step | Cost |
|---|---|---|
| **Mon** | `scout` returns 5 ranked angles with decay estimates | free |
| **Mon** | You pick 2–3. 15 minutes. | — |
| **Tue** | `fact-checker` builds the fact tables | free |
| **Tue** | `scriptwriter` → `art-director` | free |
| **Wed** | HeyGen renders. `packager` writes titles. | ~3 credits |
| **Thu** | **You watch all three.** Non-negotiable. | 10 min |
| **Thu** | `OpusClip` schedules to YouTube + X | minimal |
| **Fri** | Breaking-news slot held open — if something moves, ship same-day | ~1 credit |

**3 shorts/week, plus a reactive slot.** At 372 HeyGen credits that runs for months.

The Friday slot is the important one. Everything else is a cadence machine; the Friday slot is
where the outliers come from.

---

## 7. What to measure — recalibrated for a 6-subscriber cold start

The earlier version of this plan targeted 1,000 subscribers in 90 days. **From 6 subscribers
that is not a real target**, and chasing it would push the channel toward exactly the clickbait
the style guide bans. Here is the honest version.

### The monetisation clock — the one deadline that matters

Verified 2026-09-21:

| Threshold | Requirement | Confidence |
|---|---|---|
| YPP Tier 1 (fan funding) | 500 subs **+ 3M Shorts views / 90 days** | High |
| YPP full (ad revenue) | 1,000 subs **+ 10M Shorts views / 90 days**, or 4,000 watch hours / 12 months | High |
| **From 2027-02-01, new applicants** | **8,000 watch hours or 20M Shorts views** | High — announced 2026-08-10 |

Shorts views and long-form watch hours **never mix**.

**So there is a real deadline: 2026-02-01 is ~4.5 months away, and after it the Shorts bar
doubles to 20M.** Qualifying before then is worth a great deal. I am not going to promise you
10M Shorts views in 4.5 months from a standing start — that would be dishonest. But it is the
right thing to aim at, and **Tier 1 at 500 subs + 3M views is genuinely reachable** if the
cadence holds and one or two videos break out.

### Milestones, in order

| Horizon | Target | Why this one |
|---|---|---|
| **Weeks 1–4** | 12 shorts published, zero off-lane | Classification. Nothing else matters yet. |
| **Weeks 1–4** | Median views/short > 150 | Proves the format escapes the 6-sub floor |
| **Weeks 5–8** | One video with vidIQ `outlierScore` > 2.0 | You now have a format to repeat |
| **Weeks 5–8** | Median views/short > 500 | The algorithm is testing you on real surfaces |
| **Weeks 9–12** | 500 subs / 3M Shorts views | YPP Tier 1 |
| **By 2027-02-01** | 1,000 subs / 10M Shorts views | Full YPP before the bar doubles |

### The leading indicators

**Median views per short — never the best short.** One lucky video tells you nothing; a rising
median means the format works. Track it weekly.

**Hours from news break to published.** Under 24 for anything reactive. This is the single
metric most within your control, and §2 shows it is where the views are.

**Do not track subscribers weekly for the first 60 days.** 6 → 40 is noise, it will read as
failure on a week where everything went right, and reacting to it is how channels abandon a
working format three weeks early.

## 8. Honest risks

- **The channel is at 6 subscribers with no tooling connected to it.** Nothing publishes
  automatically until you supply the handle and authorise against it (§1). Until then every
  upload is manual.
- **The monetisation bar doubles on 2027-02-01** (§7). Missing that window means needing 20M
  Shorts views instead of 10M.
- **Breaking-news content decays in hours.** Three of this repo's assets are news-reactive. If
  the weekly cycle slips a week, they're worthless. The 10-year short is the durable one.
- **No render can be verified from this environment.** CDN egress is blocked. Every video ships
  on your eyes, and that's a hard dependency on you.
- **vidIQ's renewable pool is 0/150.** The 41 add-on credits are all there is until 2026-10-03.
- **OpusClip at 87% of cap until 2026-10-01.** Scheduling only this month.
- **The style guide's low-saturation palette will score badly** on vidIQ's thumbnail scorer.
  That is a known, accepted trade. Don't let a score talk you out of the identity.
