# VO_PROFILE — locked narration settings

**Single source of truth for how This Week in the Market sounds.**

Every run reads this file before writing a word of script. **Nothing here changes unless
Sheldon says so explicitly.** If a run finds a reason the profile is wrong, it reports the
finding and leaves the file alone.

Derived on 2026-09-20 from the three episodes actually in this repo (`pdt-short`,
`moat-short`, `paradocs-short-1`) and from the live HeyGen API. Nothing in this file is
assumed — the provenance of each number is stated.

---

## 1. Provider and voice — locked

| Field | Value | Source |
|---|---|---|
| Provider | **HeyGen** (narration baked into the render) | `CLAUDE.md`; all 3 production records |
| Voice name | **Alex Wright - Informative** | `get_voice` |
| **voice_id** | **`0db3abd83c74452fb2460b0dd113daad`** | `get_voice` |
| Voice type | **Public library voice** (not a clone) | `list_voices type=public` |
| Language / gender | English / male | `get_voice` |
| `support_pause` | `true` *(but see §5 — does not apply to this voice in practice)* | `get_voice` |
| Voice created | 2025-10-03 | `get_voice` (`created_at` 1759512992) |

This voice is used by **all four** videos in the account, including the original
PARADOCS10X Short 1 that predates the style guide. It is the channel's identity. Do not
change it, and do not let a HeyGen "suggested voice" override it.

### There is no separate TTS step
`create_speech` bills to a separate `api` credit pool the Creator plan does not have.
There is **no detached VO stem** — narration exists only inside the rendered MP4.
`scripts/YYYY-MM-DD-vo.txt` is therefore the generator input, not a transcript of a stem.

## 2. Generation settings — the honest version

The channel renders through **`create_video_agent`**. That endpoint accepts **only**
`voiceId` (plus `brandGlossaryId`). It exposes **no** speed, pitch, stability, similarity,
style or volume parameter.

> Those knobs exist in the HeyGen API — but only on `create_video_from_avatar`, via
> `voiceSettings` (`speed` 0.5–1.5, `pitch` ±50, `volume` 0–1) and `engine_settings`
> (ElevenLabs `stability`/`similarity_boost`/`style`, Fish `stability`/`similarity`).
> **That endpoint requires an `avatarId` — a presenter on camera — so this faceless
> channel cannot use it.** Checked against the live tool schema on 2026-09-20.

**So: the only lever on this pipeline is the text itself.** Pacing is controlled by word
choice and punctuation (§4), pronunciation by the brand glossary (§3). Any future note
claiming a "locked speed of 1.0" is inventing a setting that does not exist here.

### Copy-pasteable call

```jsonc
// mcp__heygen__create_video_agent
{
  "prompt": "<brief from STYLE-GUIDE.md §6 template + STYLE.md §3 visuals; VO script verbatim>",
  "mode": "chat",                                            // see §6 fallback
  "orientation": "portrait",                                 // 9:16
  "styleId": "e7f9a12679ec426099db7646b70a4639",             // Economist
  "voiceId": "0db3abd83c74452fb2460b0dd113daad",             // Alex Wright - Informative
  "brandGlossaryId": "c906414830134497906c72eecf054153"      // TWIM lexicon, §3
}
```

`avatarId` is **never** set. Setting it puts a presenter on camera and breaks the format.

## 3. Pronunciation lexicon — a HeyGen brand glossary, not respelled script text

**Created 2026-09-20. `brand_glossary_id` = `c906414830134497906c72eecf054153`**
(name: `TWIM — This Week in the Market`). Inspect with `get_brand_glossary`, amend with
`update_brand_glossary`.

### Why a glossary and not phonetic spelling in the script

The glossary remaps **audio only — captions and subtitles keep the original spelling.**
This matters because house style burns in word-by-word captions. Typing `en-VID-ee-uh`
into the script would put that string on screen. The glossary says it correctly and shows
`Nvidia`.

**Scope rule — this is what keeps captions and audio in sync:** a term belongs in the
glossary only when **the written form is already what should appear on screen and only the
audio needs help.** Anything where the *written* form should change is a writing rule (§4),
not a glossary entry. That is why `bps`, `YoY` and `Q1` are **not** in the glossary — they
are spelled out in the script instead.

### Entries (30)

| Category | Terms | Read as |
|---|---|---|
| Letter-read acronyms | FOMC, CPI, PPI, PCE, GDP, ISM, PMI, EPS, SEC, BLS, BEA, ETF, ETFs, IPO, ADR, ADRs | individual letters ("eff oh em see") |
| China / Asia | PBOC, TSMC, ASML, SMIC, Shenzhen, Nikkei, Xi Jinping, Caixin | see glossary |
| Currency | yuan → "yoo ahn", renminbi → "ren min bee" | — |
| Ampersand | S&P → "ess and pee", S&P 500 → "ess and pee five hundred" | — |
| Word-read acronym | JOLTS → "jolts" (not spelled out) | — |

⚠️ **UNVERIFIED BY EAR.** These respellings are reasoned, not confirmed: HeyGen CDN egress
is blocked here and premium credits are at 0, so nothing has been listened back. **The
first render is a pronunciation audit** — check every entry in §3 against the audio and
correct this file. Until then, treat the lexicon as a best-effort draft.

### The ticker rule — decided once, held

> **Narration says the company name. The ticker appears on screen only.**

"Nvidia beat on the data-center line" — never "NVDA beat". The ticker lives in the chart
layer, the lower third and the on-screen tag, where it is read, not heard. This keeps the
spoken line natural and avoids caption/audio drift.

**Exceptions — spoken as letters because that is how they are said aloud in finance:**
`S&P 500`, `ETF`, `IPO`, `EPS`, and the index/agency acronyms above. Indices keep their
spoken names: "the S&P", "the Nasdaq", "the Dow", "the Russell two thousand".

## 4. Read patterns — derived from the three existing scripts

### Numbers: spelled out as words; years stay numerals

Consistent across all three episodes, and it is the single strongest pattern in the corpus:

| In the VO text | Not |
|---|---|
| "twenty-five thousand dollars" | "$25,000" |
| "forty-four percent" | "44%" |
| "twenty-eight thousand Superchargers" | "28,000 Superchargers" |
| "a hundred billion dollars" | "$100B" |
| "two point four billion dollars" | "$2.408B" |
| "twenty-five basis points" | "25bps" |
| "year over year" | "YoY" |
| "the first quarter" | "Q1" |
| **"June 4th, 2026"**, **"October 2027"**, **"in 2019"** | *(years and dates stay numerals — they read correctly)* |

The one deliberate exception: a year spelled out when it **is** the hook —
`paradocs-short-1` opens "Eighteen ninety-four." Spell a year only when it is being
performed, not merely cited.

Decimals: round in the VO, keep precision on screen. Say "two point four billion",
show `$2.408B` in the chart with its as-of stamp. Compliance §7 is satisfied by the
on-screen figure, not by a mouthful of digits.

### Measured pace

| Episode | Words | Runtime | WPM |
|---|---|---|---|
| `pdt-short` (v2) | 147 | 55.8s | **158.1** |
| `moat-short` (v2) | 169 | 71.6s | **141.6** |
| `paradocs-short-1` | 123 | 45.6s | **161.8** |
| **Aggregate** | **439** | **173.0s** | **152.3** |

*(Word counts measured from the blockquoted VO lines. The counts written in those files'
headers — 147 / 166 / 135 — are approximations; two of the three are wrong. Trust the
measurement, not the header.)*

### What drives the spread — and what doesn't

The obvious hypothesis is wrong, so don't re-derive it: **number density does not slow this
voice down.** `pdt-short` is the most number-dense script in the corpus (10.9 number tokens
per 100 words) and is also one of the fastest.

What tracks the spread cleanly is **em-dash parentheticals**:

| Episode | Em-dashes | WPM |
|---|---|---|
| `paradocs-short-1` | 0 | 161.8 |
| `pdt-short` | 2 | 158.1 |
| `moat-short` | 4 | **141.6** |

This matches HeyGen's own guidance that punctuation is the pacing mechanism — commas give
short breaks, periods longer ones with a downward inflection. The interrupted clause in
`moat-short` ("Then Ford, GM, Hyundai, Toyota, BMW, Honda — nearly every automaker —
adopted…") stacks a six-item comma list inside a dash pair and costs roughly **20 wpm
across the whole script.**

⚠️ n = 3. Treat this as a working rule, not a law, and re-measure after every episode (§7).

### Word budget

**Plan at 150 wpm (2.5 words/second).** Then adjust for punctuation:

| Target runtime | Clean prose (160 wpm) | **Plan (150)** | Dash/list-heavy (142 wpm) |
|---|---|---|---|
| 60s | 160 | **150** | 142 |
| 90s | 240 | **225** | 213 |
| **120s (house target)** | 320 | **300** | 284 |
| 150s | 400 | **375** | 355 |

**House target for TWIM: 110–130 seconds, 275–325 words.** Five tracks plus a close does
not fit in 60 seconds, and Shorts allow up to 3 minutes — `STYLE-GUIDE.md` is explicit that
facts are not cut to hit an arbitrary runtime. Stay under 170s for safety margin.

HeyGen's own runtime estimate is unreliable: it quoted 66s for the `pdt-short` script that
rendered at 55.8s — **18% long**. Use the table, not the estimate.

### Clause shape that comes out clean

Measured: **8.2 / 9.4 / 8.8 words per sentence**, 14–18 sentences per script. This voice is
clean on short declaratives and mushy on long subordinate chains.

- **Target 8–10 words per sentence**, hard ceiling ~20.
- **One idea per sentence.** Split on the conjunction rather than riding a comma.
- Number-dense sentences: put the number at the **end**, where the period gives it a beat.
  ✅ "Core PCE came in at two point six percent." ❌ "Two point six percent was where core
  PCE came in, against expectations of two point eight."
- Land each beat on a full stop before the next number arrives. Two figures in one sentence
  is the reliable way to make this voice mush.

### Natural pause points

There is no pause tag available (§5), so pauses are punctuation:
- **Period** — the main tool. Between beats, use a period and a short sentence, not a comma.
- **Paragraph break in the VO text** — between the five tracks, giving the render a seam to
  cut on.
- **Comma** — short break inside a sentence. Three or more in one sentence starts to drag.
- **Em-dash** — the most expensive punctuation in the corpus. **Budget two per script.**
  Never nest a comma list inside a dash pair.

## 5. Known failure modes and workarounds

| # | Failure | Workaround |
|---|---|---|
| 1 | **`support_pause: true` is misleading.** HeyGen's guidance is that in-script pauses (`<break>` / the editor's Add Pause) work for **custom voices only** — not public-library voices. Alex Wright is a public voice. | Do not put break tags in the VO text. Pace with punctuation (§4). If a pause tag is ever tried, treat it as an experiment and verify by ear. |
| 2 | **Captions silently disabled.** `paradocs-short-1` rendered with `caption.enabled: false` — house style requires burned-in captions. | Check `get_video_scenes` after every render. HeyGen also emits a separate `captioned_video_url`; publish that cut if the main one lacks captions. |
| 3 | **`mode: chat` has 404'd** — sessions accepted, listed, then dead with no video. | Verify an older session still reads before blaming the request; fall back to `mode: generate`. Cost: no blueprint approval, so constraints get one shot and hold less tightly. Prefer `chat` whenever it is healthy. |
| 4 | **HeyGen auto-titles off-script.** | Ignore the returned `title`; use the title from `scripts/YYYY-MM-DD.md`. |
| 5 | **Cannot listen back.** `files2.heygen.ai` and `resource2.heygen.ai` egress is blocked. The voice preview URL is on a blocked host. | Every render is **complete, not verified**. Ship a verification checklist; the pronunciation audit (§3) is a human step. |
| 6 | **Premium credits: 0**, reset **2026-10-06** (checked 2026-09-20, Creator plan). | No renders until the reset or a top-up. Research, scripts and VO text can all still be produced — only the render is blocked. |
| 6b | **The locked voice cannot be synthesized at all.** HeyGen TTS requires a *starfish-engine* voice; Alex Wright is not one (checked against `list_voices engine=starfish`, absent from both sort bands). So there is no TTS route to it — free OAuth path included. It exists only inside a rendered video. | Obtain it by rendering the cheapest possible carrier and stripping the audio (`RENDERING.md`). For drafts, a **local Kokoro-82M** stem stands in: `npx hyperframes tts`, or the model directly at `/root/.cache/hyperframes/tts/`. Measured 2026-09-21 at **146.6 wpm** including pauses (voice `am_michael`), close to the 150 planning rate. **Placeholder only — not the channel voice, and never published as such without Sheldon's say-so.** |
| 7 | Brand **kits** are session-internal and do not persist. | Restate the full visual brief every time. The brand **glossary** (§3) *does* persist — it is a real workspace object with an ID. |

## 6. Change control

This file is **locked**. A run may not edit it to make a script fit.

**Only Sheldon changes:** voice, voice_id, provider, the ticker rule, the number-spelling
rule, the house runtime target.

**A run must update, as maintenance:**
- §4 measured-pace table — append every new episode's words/runtime/WPM after each render
  and recompute the aggregate. This is the mechanism that keeps word count matched to real
  runtime as n grows.
- §3 lexicon — add terms the week's script needs (write them into the glossary via
  `update_brand_glossary`, then record them here), and correct any entry the pronunciation
  audit proves wrong.
- §5 — add newly observed failure modes.

Record what changed and why at the bottom of the run's `scripts/YYYY-MM-DD.md`.

---

### Provenance log
- **2026-09-20** — Profile created. Voice/glossary/settings read live from the HeyGen API;
  pace measured from the three repo episodes. Glossary `c906414830134497906c72eecf054153`
  created with 30 terms. Pronunciation **not yet verified by ear** (credits 0, CDN blocked).
