---
description: Run the full weekly This Week in Tech workflow — research, score, script, visual plan, assets, packaging
---

# /twit — weekly This Week in Tech build

Produce one finished 50–60s faceless vertical Short covering the last 7 days of tech news.

`$ARGUMENTS` may carry an ISO date to build for (default: today) and/or steering notes
("lean hardware", "skip AI policy"). Honour steering, but never at the cost of the rules.

## Step 0 — Load state (always, before anything else)

1. Read **`VO_PROFILE.md`**. It is the single source of truth for narration.
   **Never change it** unless the channel owner says so explicitly, in those words.
   Take from it: the word-count band, the WPM, the pronunciation lexicon, the failure list.
2. Read **`STYLE.md`** for voice, format, visual system and rules.
3. Read **`ARCHIVE.md`**. Everything in it is ineligible.
4. Set `DATE` = today (or the date in `$ARGUMENTS`). The research window is
   **`DATE − 7 days` → `DATE`**, inclusive. Nothing older. Ever.

## Step 1 — RESEARCH → `research/DATE.md`

Search the web for tech news published inside the window. Cover:
company newsrooms and press releases · research lab publications · funding and launch
announcements · hardware reveals · AI model releases · space · consumer gadgets.

- **Prefer primary sources** — a company newsroom, a paper, a filing, a spec sheet — over
  aggregator blogs. When only an aggregator has it, say so and mark confidence accordingly.
- Gather **12–20 candidates**. Each needs: headline, **exact date**, **link**, source type
  (primary / secondary / aggregator), the specific facts and figures, and the caveat.
- Cross-check every number against at least one independent search. Note single-sourced
  numbers as such.
- Record **what could not be verified** and why. Do not quietly drop it.

> **Environment note.** `WebFetch` and direct `curl` to news and primary-source domains are
> blocked by this container's egress proxy — only `WebSearch` works. Claims are therefore
> corroborated across independent searches, and source URLs are cited *from search results*
> rather than from opening the page. Say this plainly in the research file's header and set
> confidence honestly. Never write "verified against primary source" for a page you could
> not open.

## Step 2 — SCORE

Drop anything in `ARCHIVE.md` first. Then score each survivor 1–10 on:

| Criterion | Weight |
|---|---|
| "Holy shit" factor | ×1 |
| **Visual potential** | **×2** |
| General-audience relevance | ×1 |
| Freshness | ×1 |

`total = holy_shit + (2 × visual) + relevance + freshness` — max 50.

**Visual potential is doubled because a story with no footage is unusable here.** A huge
story with nothing to show loses to a smaller one with a keynote clip. Say so in the file
when it happens, so the decision is auditable.

Pick the **top 3** plus **one weird/fun wildcard** to close on. Publish the full scored
table, including the losers and one line on why each lost.

Prefer a lineup with a **spine** — three stories that share a thesis beat a grab-bag of
three unrelated ones. Say what the spine is.

## Step 3 — WRITE

Word count comes from `VO_PROFILE.md` §3 — **derive it, never guess**, and report both the
count and the estimated runtime at the three observed WPM rates.

- **0:00–0:04** cold-open hook: the wildest fact of the week. No intro, no "hey guys", no
  channel name.
- **3 beats, ~12s each**, one story each: what happened, then why it matters. Date it.
- **Close on the wildcard** with a specific question that earns comments.
- **Timecode every line.**
- Write for this voice: short clauses, no tongue-twisters, nothing on the failure list,
  numbers spelled as spoken. Mark emphasis words in CAPS (an editing note — the voice does
  not read CAPS as stress).

## Step 4 — VISUAL PLAN (the main deliverable)

**For every 2–4 seconds of runtime**, one row:

| Field | Requirement |
|---|---|
| Shot | What is on screen, concretely |
| **Exact source** | Official press kit (which one) · keynote clip **with timestamp** · stock library **search term** · screen recording **of a specific URL** · motion-graphic build |
| Text overlay | **3–6 words.** Assume muted viewing — the overlays alone must tell the story |
| Motion | Push in · parallax · whip pan · number counter · split screen · cursor move |
| Licence | `press-kit/usable` · `stock/needs licence` · `risky/replace` |

- **Never hold a static image longer than 2.5 seconds.**
- **Flag every gap with no usable footage** and propose a motion-graphic substitute. Do not
  paper over it with a stock cliché.
- Apply the `STYLE.md` visual system: amber wipe between beats, lower-third on each beat's
  first frame, source attribution under third-party footage.

## Step 5 — ASSET MANIFEST

A checklist table of every clip and image to download: asset, URL, where used, licence,
status. **Anything unclear gets replaced, not risked** — mark it `risky/replace` and give
the substitute in the same row.

## Step 6 — NARRATION FILE → `scripts/DATE-vo.txt`

Narration only. No timecodes, no stage directions, no visual notes, no beat headers.

- Numbers spelled exactly as spoken.
- **Pronunciation is applied via HeyGen's `brandGlossaryId`, NOT by respelling in this
  file.** The glossary changes the audio while leaving caption spelling intact; respelling
  inline would corrupt the SRT. See `VO_PROFILE.md` §5.
- **Do not write SSML.** HeyGen does not support it and will read it aloud
  (`VO_PROFILE.md` §6.1).
- **Any drift between this file and the timecoded script is a bug.** Diff them
  mechanically before finishing — strip markdown from the script's VO lines and compare
  word-for-word.

## Step 7 — PACKAGE

- **5 titles, each under 50 characters.** Count them and show the counts.
- **Description** with a source link for **every** claim in the script.
- **8–12 hashtags.**
- **First-frame / thumbnail concept** — text-led, readable at thumbnail size.
- **`scripts/DATE.srt`** caption file, plus burned-in caption styling notes per `STYLE.md`.

## Step 8 — VERIFY, then archive

Check the script against `VO_PROFILE.md` and report each result explicitly:

- [ ] Word count inside the band; runtime at slow/nominal/fast WPM all inside **50–60s**
- [ ] No term mispronounced — every proper noun, acronym and unit either in the glossary
      or added to it **and pushed to HeyGen in this run**
- [ ] No sentence over ~20 words; no four-plus item comma list
- [ ] No banned words (`STYLE.md` §1); no SSML; no bare numerals
- [ ] Every claim has a linked source; company claims labelled as claims
- [ ] "Announced" vs "released" correct on every beat, with real availability dates
- [ ] `-vo.txt` matches the timecoded script verbatim
- [ ] No story already in `ARCHIVE.md`
- [ ] Compliance card decision made (`STYLE.md` §0) — needed only if a beat quotes a
      valuation, funding round or market move

Then **update `ARCHIVE.md`** with every story covered: date, headline, episode file.

Report the runtime estimate and anything that could not be verified. If a check fails, fix
it and say so — never report a pass you did not get.
