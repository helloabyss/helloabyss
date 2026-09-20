---
description: Run the full weekly "This Week in the Market" workflow — research, script, visual plan, metadata
argument-hint: "[YYYY-MM-DD] [--research-only] [--no-render] [--render]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, TodoWrite
---

# /twim — weekly production run

Produce one episode of **This Week in the Market**: a faceless US-stock-market recap.
Voiceover over charts, data visualization, B-roll and kinetic text. **No presenter.**

`$ARGUMENTS` — optional episode date (defaults to today), plus flags:
- `--research-only` — stop after Phase 1
- `--no-render` *(default)* — produce all files, do not call HeyGen
- `--render` — also submit the render (checks credits first, Phase 8)

Let **`DATE`** = the episode date, `YYYY-MM-DD`.

---

## Phase 0 — Read the locked files first

**Do this before writing anything.** In order:

1. `VO_PROFILE.md` — how it sounds. **Locked.** Never edit it to make a script fit.
   Take from it: the word budget, the pace table, the number-spelling rule, the ticker
   rule, the clause-length target, the em-dash budget, `voice_id`, `brand_glossary_id`.
2. `COMPLIANCE.md` — what may be said. **Non-negotiable.**
3. `STYLE.md` — series bible: scope test, episode architecture, chart grammar, palette.
4. `STYLE-GUIDE.md` — the channel's locked visual identity (inherited).
5. `ARCHIVE.md` — **what has already been covered and how it was framed.** Do not repeat a
   framing from the last 4 episodes. If this week's story is last week's story, the angle
   must be what *changed*.
6. `EARNINGS_CALENDAR.md` — what was flagged for this week.

If `VO_PROFILE.md` does not exist, **stop and ask** for provider, voice ID and settings.
Never invent them.

## Phase 1 — RESEARCH

Search the web, **last 7 days only** (`DATE − 7` → `DATE`). Anything older is context, not
news, and is labelled as such.

**Sourcing rule (`COMPLIANCE.md §6`): a news article is a pointer, not a source.** Follow
every figure to its primary document — filing, central bank release, official print,
company IR. Record the primary URL. **A figure that cannot be traced is cut**, not softened.

Every figure recorded as: **value · source · as-of timestamp.**

### Track 1 — Fed and rates
FOMC decisions · dot plot / SEP changes · statement language shifts (quote the changed
words) · Powell press conference and speeches · governor commentary · minutes · Treasury
yields across the curve (2s, 10s, 30s, and 2s10s) · where fed funds futures now price the
next cut or hike.
→ **Record what changed versus what the market expected.** The surprise is the story.

### Track 2 — Macro data
CPI · PPI · PCE · jobs report (headline, unemployment rate, wage growth) · JOLTS · retail
sales · ISM / PMI · GDP · consumer confidence · housing.
→ For each: **actual print · consensus estimate · surprise direction and size · the equity
reaction.** A print with no consensus attached is incomplete.

### Track 3 — Earnings
For every major report in the window: **actual EPS vs. consensus · actual revenue vs.
consensus · beat/miss on each and by how much · forward guidance raised / lowered /
maintained · the stock's reaction · the single line from the call that explains the move.**

Prioritize, in order:
1. Mega caps and index-weight movers
2. Highest-surprise beats and misses
3. Anything that repriced a whole sector
4. **Guidance that contradicts the print** — beat but guided down, or missed but guided up.
   These are the most interesting beats in the format; flag them explicitly.

### Track 4 — Geopolitics and China
Per `STYLE.md §1`, filtered through the China channel table: PBOC and policy · export
controls and tariffs **in both directions** · rare earths and supply chain · Chinese demand
data hitting US revenue lines · semis and chip restrictions · Chinese listings and delisting
risk · yuan moves repricing US multinationals.
→ `COMPLIANCE.md §5` applies from the first note: **describe events, policy and market
reaction. Do not editorialize about governments or take sides.** Flag disputed official data
as disputed at the research stage, not later.

### Track 5 — The tape
Index levels and weekly moves (S&P 500, Nasdaq, Dow, Russell 2000) · sector leadership and
laggards · breadth · volatility · notable single-name moves not covered by earnings ·
commodities and the dollar **only where they transmit to US equities**.
→ Every level: **close or intraday, with its date.**

### Output — `research/DATE.md`

```markdown
# Research — DATE
Window: DATE-7 → DATE · Compiled: <timestamp>

## Track 1 — Fed and rates
### <finding>
- **Figure:** <value>
- **Source:** <primary doc + URL>
- **As-of:** <timestamp / reference period>
- **vs. expected:** <consensus, and the surprise>
- **Equity transmission:** <ticker/sector/index + mechanism>
- **Confidence:** High / Medium / Low
- **Disputed?** <only if applicable>
...

## CUT — traceable-source failures
| Claim | Why cut |
|---|---|
| <claim> | No primary document located (COMPLIANCE §6) |
```

Every finding carries an **Equity transmission** line. A finding that cannot get one has
already failed the scope test and is marked `NO TRANSMISSION — not for script`.

If `--research-only`, stop here and report.

## Phase 2 — SELECT

Build the run of show against `STYLE.md §2`.

1. **Apply the one-sentence scope test to every candidate** (`STYLE.md §1`). Ticker/sector/
   index **and** mechanism, in one sentence. Fails → cut. No exceptions for a good story.
2. **Pick the cold-open number** — the single figure that defined the week.
3. **Identify the counter-beat** (`STYLE.md §2`). Mandatory. The data point that
   contradicts the week's narrative. If nothing contradicts, go back to the research —
   something was missed.
4. **Check `ARCHIVE.md`** — no repeated framing from the last 4 episodes.
5. **Drop empty segments entirely.** A quiet Fed week means a short Fed beat or none, with
   the words redistributed. Never fill.

## Phase 3 — SCRIPT

Write to `scripts/DATE.md`. Obey `VO_PROFILE.md §4` **exactly**:

- **275–325 words** for the 110–130s target. Count the words; state the count.
- Numbers **spelled out** in the VO ("twenty-five basis points"); years stay numerals.
- **Company names spoken, tickers on screen only.**
- 8–10 words per sentence. One idea each. **Number at the end of the sentence.**
- **Two em-dashes maximum** across the whole script — they cost ~20 wpm.
- Paragraph break between segments, giving the render a seam.
- Attribute every forecast by name (`COMPLIANCE.md §2`).
- No greeting, no sign-off branding, no subscribe ask.

Each beat is headed with its scope test made visible:

```markdown
**[0:20–0:42] FED AND RATES** · NVDA, semis · mechanism: discount rate on long-duration growth
> Powell said the committee is not on a preset course. ...
```

## Phase 4 — VISUAL PLAN

**This is the hardest part of the job, not an afterthought** — give it the most time.
Per `STYLE.md §3`, every chart sits **over a photographic plate**. A slideshow of charts on
flat backgrounds is a failed episode.

Three artifacts, all in `scripts/DATE.md`:

### 4a. Shot list
One row per beat. Cut or punch in every 1.2–1.8s, no shot past 2s.

| # | Time | BASE plate | MID graphic | TOP type | Transition |
|---|---|---|---|---|---|

Mark the **hero shot** and the **bookend** (`STYLE.md §3`).

### 4b. Chart specs
One block per chart. Fully specified — a chart without a spec gets improvised, and
improvised charts break the palette.

```
CHART-03
type:      line
series:    US 2Y yield (muted) · US 10Y yield (paper)
range:     2026-09-14 → 2026-09-18
source:    US Treasury daily par yield curve
as-of:     2026-09-18 close
annotate:  FOMC decision 2026-09-16 — vertical rule, accent red
motion:    draws L→R over 1.2s; marker snaps at the annotation; camera pushes past the axis
palette:   paper primary, muted secondary, ONE accent element only
axis:      y starts at 3.50%, labelled — never an unlabelled crop
```

Every chart carries its **as-of stamp and source**, bottom-left (`COMPLIANCE.md §7`).

### 4c. Asset manifest
Everything the render needs, so nothing is invented at generation time.

| ID | Type | Description | Source | Constraint |
|---|---|---|---|---|
| PLATE-01 | B-roll | Trading-floor ceiling geometry, slow push | stock/generated | no faces, no logos |
| CHART-03 | chart | see spec | research/DATE.md §T1 | as-of stamp visible |
| CARD-01 | card | "Educational only. Not financial advice." | COMPLIANCE §8 | first 4s |
| CARD-99 | card | full disclaimer | COMPLIANCE §8 verbatim | final frame, held |

`CARD-01` and `CARD-99` are **mandatory rows in every episode.**

## Phase 5 — METADATA

In `scripts/DATE.md`, per `STYLE.md §5`: 3 title options (date-anchored, no clickbait) ·
description (summary → **source list with as-of dates** → verbatim `COMPLIANCE.md §8`
disclaimer) · pinned comment (the likeliest top-comment caveat) · hashtags · thumbnail
concept honouring the palette.

## Phase 6 — COMPLIANCE PASS

Run `COMPLIANCE.md §9` against the finished draft — **every line ticked.** Then add a
`## COMPLIANCE FLAGS` section (`COMPLIANCE.md §10`) listing anything that brushed a line,
marked `[RESOLVED]` / `[ACCEPTED]` / `[OPEN]`.

Grep the draft for the banned constructions in `COMPLIANCE.md §1` before declaring it clean.

> **An `[OPEN]` flag blocks the ship.** Resolve it or cut the beat. Do not "note it and move
> on."

## Phase 7 — VO TEXT

Write `scripts/DATE-vo.txt`: **narration only, generator-ready.**

- No headers, no timecodes, no stage directions, no markdown, no beat labels.
- Plain UTF-8. Paragraph break between segments.
- Exactly the words that will be spoken, as they should be spoken (numbers already
  spelled out).
- **No pause/break tags** — they do not work on this public-library voice
  (`VO_PROFILE.md §5`). Pacing is punctuation.
- **Verify:** `wc -w scripts/DATE-vo.txt` is inside the budget, and the text matches the
  blockquoted VO in `scripts/DATE.md` word for word.

## Phase 8 — RENDER *(only with `--render`)*

1. **Check credits first:** `mcp__heygen__get_current_user`. Premium credits were **0** on
   2026-09-20, resetting **2026-10-06**. If zero, **stop and report** — do not burn the run.
2. Build the brief from the `STYLE-GUIDE.md §6` template, with the VO text **verbatim** and
   the per-beat imagery from Phase 4a.
3. Call `create_video_agent` with the exact payload in `VO_PROFILE.md §2` —
   `styleId`, `voiceId`, `brandGlossaryId`, `orientation: portrait`, `mode: chat`.
   **Never set `avatarId`.**
4. In `chat` mode the agent pauses for blueprint approval: **restate the grade, the bookend,
   the hero shot and the no-faces/no-logos constraints at approval.** That restatement is
   what makes them survive generation (`STYLE-GUIDE.md §7`).
5. If `chat` 404s, confirm an older session still reads, then fall back to `mode: generate`
   and note the reduced constraint adherence (`VO_PROFILE.md §5`).
6. After render: `get_video_scenes` → **confirm `caption.enabled` is true.** If false, use
   the separate `captioned_video_url` cut.
7. Write `PRODUCTION.md` notes into `scripts/DATE.md`: session ID, video ID, duration,
   settings, constraints hit.
8. **Report the render as _complete, not verified_** — CDN egress is blocked, nothing can be
   watched here. Ship a verification checklist, and include the **pronunciation audit**
   (`VO_PROFILE.md §3`) as the first item, since the lexicon has never been heard.

## Phase 9 — UPDATE THE ROLLING FILES

1. **`EARNINGS_CALENDAR.md`** — remove what reported, add newly confirmed dates for the
   next 4–6 weeks, mark each **Confirmed** (company IR) or **Estimated**. Sanity-check every
   date's **weekday** — recycled prior-year calendars are a known trap and have already been
   caught once in this repo.
2. **`ARCHIVE.md`** — append the episode: stories covered, framing used, tickers named,
   counter-beat, so next week does not repeat it.
3. **`VO_PROFILE.md §4` pace table** — *after a render only*, append words / runtime / WPM
   and recompute the aggregate. **This is the only edit a run may make to that file**, and
   it is maintenance, not a settings change.

## Phase 10 — COMMIT

Commit to the working branch with a descriptive message. Files touched:
`research/DATE.md`, `scripts/DATE.md`, `scripts/DATE-vo.txt`, `EARNINGS_CALENDAR.md`,
`ARCHIVE.md`, and `VO_PROFILE.md` only if Phase 9.3 applied.

---

## Run report

Close with:
- Word count vs. budget, and the runtime it implies at 150 wpm
- The scope test result for every beat (pass, or cut and why)
- The counter-beat, named
- Compliance flags, with any `[OPEN]` called out loudly
- Anything cut for being untraceable to a primary document
- Render status, or why no render (credits / flag)
