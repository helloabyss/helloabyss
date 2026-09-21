# Growth Plan — faceless finance shorts

Written 2026-09-21. Owner: Sheldon. This is the project-management view: what is actually
true today, what the constraint is, and what connects to what.

---

## 1. The thing that has to be decided first

**The channel this repo publishes to is `PARADOCS10X` — an AI/tech channel, not an investing
channel.**

| | |
|---|---|
| Channel | PARADOCS10X — `UCX2_NXOHIgXUQFsBOub65HQ` |
| vidIQ / YouTube auth | `paradocs10x@gmail.com` |
| Subscribers | **57** |
| Lifetime views | 28,829 across 38 videos |
| Subscribers gained, last 30d | **0** |
| Views gained, last 30d | 266 |
| Top videos | 2023–24 AI shorts — reusable rockets (6,050), China AI (3,843), Face++ (2,697) |
| Recent finance shorts | "The Moore's Law Myth" 138 · "2NM Chips" 66 · "Cybercab" 15 |

There is no channel called "The Meticulous Investor" connected to any tool in this stack.
So one of these is true, and they lead to different plans:

- **(a) It's a rebrand of PARADOCS10X.** You keep 28.8k lifetime views and 57 subs, but you
  inherit an audience YouTube has classified as AI/tech. The finance shorts will be shown to
  people who subscribed for Cybertruck content. That's the 15-view problem above.
- **(b) It's a new channel, not yet created or not yet connected.** Cleaner signal, zero
  history, and every tool in the stack needs re-authorising against it.

**My recommendation: (b), a clean channel.** 57 subscribers is not an asset worth protecting,
and the 28.8k views are three years old and topically wrong. A fresh channel gets a clean
classification from the algorithm on day one. The cost of choosing (b) is one afternoon of
re-auth; the cost of choosing (a) is fighting a mis-trained recommendation surface for months.

**Everything below assumes a single dedicated finance channel. Tell me which and I'll wire it.**

---

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

1. **Render → publish.** Register the finished HeyGen asset with OpusClip and schedule it to
   both accounts. This removes the manual step that currently gates every upload. *Blocked on
   the §1 channel decision — I don't want to wire publishing to the wrong channel.*
2. **One asset → two platforms.** Every short should post to YouTube and X from the same
   render. You already have the X account connected and have never used it. This is free reach.
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

## 7. What to measure

Do not measure subscribers for the first 60 days — 57 → 200 is noise and will read as failure
on a week where you did everything right.

| Horizon | Metric | Target |
|---|---|---|
| Weekly | Shorts published | 3 + reactive |
| Weekly | Hours from news break → published | **< 24** for reactive |
| Per video | Views at 48h vs channel median | rising median |
| Per video | vidIQ `outlierScore` | any video > 2.0 = repeat that format |
| 30 days | Median views/short | > 500 |
| 90 days | Subscribers | 1,000 (monetisation floor) |

**The one leading indicator that matters: median views per short, not the best short.** One
lucky video tells you nothing. A rising median means the format works.

---

## 8. Honest risks

- **The channel-identity problem (§1) is unresolved and it gates everything.** Publishing
  finance shorts to an AI/tech channel's audience is why the last three got 15–138 views.
- **Breaking-news content decays in hours.** Three of this repo's assets are news-reactive. If
  the weekly cycle slips a week, they're worthless. The 10-year short is the durable one.
- **No render can be verified from this environment.** CDN egress is blocked. Every video ships
  on your eyes, and that's a hard dependency on you.
- **vidIQ's renewable pool is 0/150.** The 41 add-on credits are all there is until 2026-10-03.
- **OpusClip at 87% of cap until 2026-10-01.** Scheduling only this month.
- **The style guide's low-saturation palette will score badly** on vidIQ's thumbnail scorer.
  That is a known, accepted trade. Don't let a score talk you out of the identity.
