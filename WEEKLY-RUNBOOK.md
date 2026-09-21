# Weekly Runbook — the brainstorming team

Five agents in `.claude/agents/`. They hand off in a fixed order. Each one is deliberately
narrow so it can't drift into the next one's job.

```
scout → fact-checker → scriptwriter → art-director → [HeyGen] → packager → [OpusClip]
 find      verify         write          design        render      title      schedule
```

Run them with the Agent tool by name (`subagent_type: "scout"`), or say "run the weekly cycle"
and I'll drive the whole chain.

---

## Monday — Scout (15 min of your time)

```
Agent(subagent_type="scout",
      prompt="Weekly sweep. Return 5 ranked angles for this week's shorts.")
```

Returns 5 candidates, each with: the differentiated angle, what the big channels missed, the
counter-evidence that exists, a decay estimate, and a comparable video's real numbers.

**Your only job: pick 2–3.** Prefer one evergreen + one news-reactive. If a candidate has no
credible counter-evidence, it's a promo — skip it, whatever the demand data says.

## Tuesday — Fact-check, then write

```
Agent(subagent_type="fact-checker", prompt="Verify all claims for <angle>. Write the fact table into <dir>/SCRIPT.md.")
Agent(subagent_type="scriptwriter", prompt="Write the VO for <dir> from its fact table.")
Agent(subagent_type="art-director",  prompt="Shot list + HeyGen brief for <dir>.")
```

`fact-checker` runs **before** `scriptwriter`, always. The writer is forbidden from using a
number that isn't in the table — that ordering is the whole safety mechanism.

If fact-checker says a thesis has no honest counter-argument, **kill the video.** That call is
the channel's editorial standard, not an obstacle.

## Wednesday — Render

Send the brief to HeyGen: `mode: chat`, `orientation: portrait`, style
`e7f9a12679ec426099db7646b70a4639`, voice `0db3abd83c74452fb2460b0dd113daad`.

**At blueprint approval, restate the grade, the bookend and the hero shot.** Per
`STYLE-GUIDE.md` §7 that restatement is what survives generation. If chat mode 404s, fall back
to `mode: generate` — but the constraints then get one shot only.

```
Agent(subagent_type="packager", prompt="Titles, description, tags, thumbnail direction for <dir>.")
```

## Thursday — YOU WATCH THEM. Then schedule.

Non-negotiable. HeyGen CDN egress is blocked from this environment, so **no agent has ever
seen any render.** Every short ships on your eyes.

Run the checklist in each `PRODUCTION.md`: no faces · three layers live · no shot past 2s ·
compliance card in first 4s · palette clean · bookend intact · numbers verbatim.

Anything wrong → reply into the HeyGen chat session. It revises without a full rebuild.

Then schedule via OpusClip to **both** YouTube and X. Schedule — never auto-post.

## Friday — the reactive slot

Hold it open. If something breaks, compress Mon–Thu into one afternoon and ship inside 24
hours. This slot is where outliers come from; the rest of the week is a cadence machine.

---

## Standing rules

**Credits.** Research is free — `channel_stats`, `channel_videos`, `channel_search`,
`youtube_search`, `keyword_research`, `video_stats`. Generation is not: vidIQ thumbnail 22,
score 5, against a 41-credit pool. No agent spends a generation credit without you saying yes
in that turn. Check balances at session start; `CLAUDE.md` has been stale before.

**`vidiq_outliers` is broken** — it ignores its query argument. Use `channel_search` /
`youtube_search`.

**Never script from memory.** Every figure gets a live search, every analyst number is marked
an estimate, every dataset is scoped on screen.

**Never chase the thumbnail score.** The palette is the identity; the scorer rewards
saturation. Known trade, already decided.

---

## Making it recur

Two options, both available:

1. **A scheduled Routine** — fires Monday morning, runs the scout sweep, leaves 5 angles
   waiting for you. Say the word and I'll create it.
2. **`/loop`** — for driving a single cycle to completion within a session.

Option 1 is the one you want for a weekly rhythm. I haven't created it yet because it should
point at the right channel, and that decision is still open (`GROWTH-PLAN.md` §1).
