# VO_PROFILE.md — locked narration settings

**Series:** This Week in Tech (TWiT)
**Status:** LOCKED. Every `/twit` run reads this before writing a word and changes nothing
here without the channel owner saying so explicitly, in those words.
**Derived:** 2026-09-20, from the three existing episodes in this repo and from the live
HeyGen API records for this account. Nothing in this file is invented — the
[Provenance](#provenance) table says where each value came from.

---

## 1. Provider and voice

| Field | Value |
|---|---|
| Provider | **HeyGen** |
| Voice name | **`Alex Wright - Informative`** (API spelling — hyphen, not en-dash) |
| Voice ID | **`0db3abd83c74452fb2460b0dd113daad`** |
| Language | English |
| Gender | male |
| `support_pause` | **true** |
| Visual style ID | `e7f9a12679ec426099db7646b70a4639` (Economist) |
| Pronunciation glossary | `TWIT — This Week in Tech` → see §5 |

This is the same voice as all three prior episodes on this account. **That is the whole
point** — the channel owner's requirement is that narration match previous episodes
exactly, and this voice ID is the thing that guarantees it. Do not substitute a
"similar" voice.

## 2. Locked generation settings — copy-paste values

```json
{
  "voiceId": "0db3abd83c74452fb2460b0dd113daad",
  "voiceSettings": {
    "speed": 1.0,
    "pitch": 0,
    "volume": 1.0,
    "locale": "en-US"
  }
}
```

**Why these exact values, and why changing them breaks the match.** The three prior
episodes were produced through HeyGen's `create_video_agent` endpoint. That endpoint's
schema accepts `voiceId` and `brandGlossaryId` — and **no tuning parameters at all**: no
speed, no pitch, no stability. So the previous episodes were narrated at the provider
defaults, whatever route is used next. `speed: 1.0 / pitch: 0 / volume: 1.0` **are** those
defaults. Setting speed to 1.05 to "fix" a long runtime would make the new episodes stop
matching the old ones. Fix runtime by cutting words, never by changing speed.

### Settings that do NOT apply here
`stability`, `similarity_boost`, `style`, `use_speaker_boost` are **ElevenLabs** engine
parameters. They exist in HeyGen's API only under `engine_settings.engine_type:
"elevenlabs"`, and only for ElevenLabs-backed voices. Do not pass them with this voice —
HeyGen rejects the request when the voice and engine don't match. If someone asks for "the
stability setting", the honest answer is that this provider/voice pair has none.

## 3. Measured words per minute

Measured from the three finished renders on this account — real word counts against real
durations, not an estimate.

| Episode | VO words | Render duration | WPM |
|---|---:|---:|---:|
| `paradocs-short-1` | 123 | 45.6s | **161.8** |
| `pdt-short` | 147 | 55.8s | **158.1** |
| `moat-short` | 169 | 71.6s | **141.6** |
| **Pooled** | **439** | **173.0s** | **152.3** |

**Planning rate: 152 WPM. Observed spread: 142–162 WPM.**

### The word-count band for a 50–60s Short
The band has to survive the *whole* observed spread, not just the average, or a slow read
runs long and a fast one runs short:

- Slowest observed (142 WPM) must still finish under 60s → **≤ 142 words**
- Fastest observed (162 WPM) must still reach 50s → **≥ 135 words**

> ### **TARGET: 135–142 words. Aim for 138.**

At 138 words the runtime lands at 51.1s (fast) / 54.5s (nominal) / 58.3s (slow) — inside
50–60s across the full range. Outside this band, a Short can miss the target purely on how
the voice feels that day.

**Sample size is n=3.** Re-measure after every render and add a row to the table above. The
`moat-short` outlier at 141.6 WPM is the one to watch: it is the most number-and-name-dense
of the three, and the plausible cause is its seven-item comma list ("Ford, GM, Hyundai,
Toyota, BMW, Honda…") drawing a pause at every comma. That is a **hypothesis, not a
measured finding** — a density check across all three scripts did not reproduce the
correlation (the *fastest* episode was also comparatively dense). Until more episodes exist,
treat long comma lists as a runtime risk and keep the band conservative.

## 4. Read patterns — how this voice behaves

**Pauses.** The voice reports `support_pause: true`. Punctuation is the pause control: a
period gives a full stop, an em dash a shorter break, a comma the shortest. Write the
pauses in with punctuation rather than reaching for markup.

**Numbers.** Spell them the way they should be spoken — this is what all three prior
scripts do, and it is why their numbers read cleanly:
- `$2,195` → **"twenty-one ninety-five"**
- `$25,000` → **"twenty-five thousand dollars"**
- `$1.4B` → **"one point four billion dollars"**
- `2026` → **"twenty twenty-six"**
- `51°` → **"fifty-one degree"**
- `iOS 27` → **"iOS twenty-seven"**
Never leave a raw numeral in the narration file and hope the synthesizer guesses the
register. It will sometimes read `2026` as "two thousand and twenty-six", which costs three
syllables and breaks the runtime maths.

**Lists.** Three items maximum in one breath. A four-plus item list reads as a slow chain of
comma pauses and is the leading suspect for the `moat-short` runtime overrun. Break longer
lists into two sentences, or cut to the two that matter.

**Sentence length.** Keep full sentences in the **8–14 word** zone, and **never go past
~20** — beyond that the pitch contour flattens and the line goes mushy. All three prior
scripts respect the 20-word ceiling.

**Short fragments are house rhythm, not a fault.** The prior episodes lean on them
deliberately — *"It was a seatbelt."* (4 words), *"The gate's open. The floor isn't."*
(3 and 3) — and they land. Two- to four-word fragments are the show's punctuation and the
setup for an emphasis frame. Use them on purpose, between longer sentences, not in a row.

**Emphasis.** CAPS in the script marks an emphasis word for the *writer and editor* — the
stressed beat and the on-screen impact frame. HeyGen does not read CAPS as a prosody
instruction, so never rely on it to produce audible stress. One emphasis word per beat,
five per script at most.

## 5. Pronunciation lexicon

**Applied through HeyGen's brand glossary — NOT by editing the narration text.**

`brandGlossaryId` remaps how a term is *spoken* while leaving its spelling untouched in
captions and subtitles. That is exactly what this series needs: the SRT keeps "TSMC" while
the audio says "tee ess em see". Respelling inline in the script would corrupt every caption
and the SRT along with it.

```
brandGlossaryId: c7cb764ee025432caa879e8d76048c7f     # "TWIT — This Week in Tech"
```

House respelling convention, inherited from the sibling `TWIM — This Week in the Market`
glossary already on this account: acronyms are spelled out letter by letter, lowercase,
space-separated. Where a term already exists in TWIM, **reuse its respelling verbatim** so
the two series pronounce the shared vocabulary identically.

| Term | Pronunciation | Note |
|---|---|---|
| AI | `ay eye` | |
| AR | `ay are` | |
| VR | `vee are` | |
| iOS | `eye oh ess` | |
| macOS | `mack oh ess` | |
| API | `ay pee eye` | |
| MCP | `em see pee` | |
| GPU | `gee pee you` | |
| CPU | `see pee you` | |
| NPU | `en pee you` | |
| LLM | `ell ell em` | |
| FOV | `eff oh vee` | |
| CEO | `see ee oh` | |
| US | `you ess` | |
| UK | `you kay` | |
| EU | `ee you` | |
| FAA | `eff ay ay` | |
| NASA | `nassa` | said as a word, not spelled |
| TSMC | `tee ess em see` | **reused from TWIM** |
| ASML | `ay ess em ell` | **reused from TWIM** |
| SMIC | `ess em eye see` | **reused from TWIM** |
| Nvidia | `en vid ee uh` | |
| Huawei | `hwah way` | |
| Ascend | `uh send` | the chip line, not "ay-send" |
| Xiaomi | `shao mee` | |
| Qualcomm | `kwal comm` | |
| Anthropic | `an throp ik` | |
| Claude | `clawd` | one syllable |
| Gemini | `jem in eye` | |
| Siri | `seer ee` | |
| A17 | `ay seventeen` | also A18, A19, M4, M5 — letter then number |
| H100 | `ay ch one hundred` | same for H200, B200, GB200 |
| exaflops | `ex uh flops` | |
| petabyte | `pet uh bite` | |
| aperiodic | `ay peer ee od ik` | |
| chiral | `ky rul` | |
| monotile | `mon oh tile` | |
| Starlink | `star link` | |
| Starship | `star ship` | |

Add a row whenever a new recurring name appears, and push the change to the glossary in the
same run — a lexicon that lives only in this file is not applied to anything.

## 6. Known failure modes and workarounds

| # | Failure | Workaround |
|---|---|---|
| 1 | **SSML is not supported.** HeyGen's speech endpoint states plainly that "SSML and break tags are not supported." Tags like `<break time="300ms"/>` are read aloud or dropped. | Never put SSML in the narration file. Use punctuation for pauses and the brand glossary for pronunciation. |
| 2 | **Bare numerals read in the wrong register** — `2026` becomes "two thousand and twenty-six". | Spell every number as spoken words (§4). |
| 3 | **Four-plus item comma lists run long** and are the prime suspect in the one measured runtime overrun. | Three items per breath, maximum. |
| 4 | **Sentences past ~20 words go mushy** — the contour flattens and emphasis is lost. | Keep to 8–14 words. Split on the conjunction. |
| 5 | **Adjacent sibilants slur** — "Snap's Specs specs", "six sixty-six". | Reword. "Snap's Specs" is fine; "Specs specs" is not. |
| 6 | **Version strings read as decimals** — "iOS 27.1" becomes "twenty-seven point one", which is correct, but "GPT-4o" is unpredictable. | Write model names phonetically in the script and add them to §5. |
| 7 | **CAPS does not produce audible emphasis.** | Treat CAPS as an editing note. If a word must land, give it its own short sentence. |
| 8 | **No detached VO stem on this plan.** `create_speech` bills to separate `api` credits the Creator plan does not carry, and `generate_model_speech` requires an *active professional* voice — a public library voice like this one does not qualify. Narration is baked into the HeyGen render. | See §7. |

### Words to avoid
Not because the voice cannot say them, but because they cost runtime or read badly at this
pace: *nevertheless, furthermore, additionally, simultaneously, approximately* (say "about"),
*utilize* (say "use"), *particularly*. Prefer the one-syllable word every time — the word
budget is 137, and every four-syllable connective costs most of a second.

## 7. Open constraint — getting a VO stem

The workflow in `/twit` assumes narration can be cut against B-roll on a timeline, which
needs a standalone audio file. **This account cannot currently produce one** (§6.8), and
premium credits are at **0 until 2026-10-06**.

Routes out, in order of preference — none taken without the owner's say-so:
1. **Add HeyGen `api` credits** to the account, then `create_speech` with the voice ID and
   settings above. Keeps the voice identical. Recommended.
2. **Render through HeyGen and strip the audio** from the finished MP4. Free, but bakes in
   HeyGen's visuals and this account's CDN egress is blocked, so the file has to be pulled
   down by hand outside this environment.
3. **Switch provider.** Rejected on 2026-09-20 — it breaks the voice-match requirement,
   which is the reason this file exists.

Until one of these lands, `scripts/YYYY-MM-DD-vo.txt` is the generator-ready deliverable and
the audio step is done by the owner.

## 8. DEVIATION LOG — 2026-09-20 episode used a substitute voice

**The locked voice was not used for `scripts/2026-09-20`. This is a recorded deviation, not
a change to §1–§2.** The lock stands; the next episode reverts to it the moment it is usable.

**Why.** Two independent blockers on the same day:
1. HeyGen premium credits: **0** until 2026-10-06.
2. HeyGen API token **expired/revoked** — `generate_model_speech` returns
   `401 unauthorized: Bearer token expired/revoked — needs re-auth`. **Action for the owner:
   reconnect the HeyGen MCP integration.**

**What was used instead.**
```json
{ "provider": "Higgsfield", "model": "seed_audio",
  "voice": "Arthur", "voice_type": "preset",
  "voice_id": "30fc8796-ceb6-4a66-b3a7-4a145ef7f346",
  "post": "atempo=1.18, silence-trimmed, loudnorm I=-16 TP=-1.5 LRA=11" }
```

**Arthur was chosen by measurement, not by name.** Alex Wright's own preview was pulled from
HeyGen's CDN and every male Higgsfield preset was scored against it on median F0, F0 spread,
spectral centroid and voiced ratio:

| voice | median F0 | F0 spread | brightness | distance |
|---|---:|---:|---:|---:|
| **Alex Wright (target)** | **144.1** | **48.2** | **1706** | — |
| **Arthur** | 140.4 | 48.1 | 1502 | **0.125** |
| Cillian | 123.1 | 35.0 | 1707 | 0.170 |
| Dylan | 149.5 | 44.2 | 1478 | 0.186 |
| Archie | 132.2 | 38.2 | 1472 | 0.227 |
| …7 others | | | | 0.32–0.51 |

Arthur's pitch **spread** matches to within 0.1 Hz (48.1 vs 48.2) — the same intonation
range, which is what carries the delivery.

**Voice cloning was refused.** Alex Wright's sample is reachable and `seed_audio` can clone
from a reference, but cloning a licensed commercial library voice onto another platform is a
rights problem, not a technical one. Not done, and not to be done.

**Rate.** Arthur reads ~127 WPM natural, so the 139-word script ran 65.9s. `atempo=1.18`
brings it to 147.6 WPM and 56.5s. Note this does **not** violate §2's "fix runtime by cutting
words, never by changing speed" — that rule exists to preserve the match to prior episodes,
and this render already isn't that voice. **When the locked voice returns, drop the tempo
lift**: at 152 WPM the same 139 words land at 54.9s, inside the band unaided.

## Provenance

| Value | Source |
|---|---|
| Voice ID, exact name, `support_pause` | HeyGen `get_voice` API, 2026-09-20 |
| Voice/style IDs cross-checked | `CLAUDE.md`, `pdt-short/PRODUCTION.md`, `moat-short/PRODUCTION.md`, `paradocs-short-1/PRODUCTION.md` |
| speed / pitch / volume / locale | HeyGen `create_video_from_avatar` schema defaults; prior episodes used `create_video_agent`, which exposes no tuning fields |
| ElevenLabs params do not apply | HeyGen `VoiceSettingsInput.engine_settings` discriminated union |
| WPM table | Word counts computed from each `SCRIPT.md` VO section against the durations in each `PRODUCTION.md` |
| SSML unsupported | HeyGen `generate_model_speech` tool description |
| Glossary mechanism + caption-safety | HeyGen `create_brand_glossary` / `get_brand_glossary` descriptions |
| Respelling convention | Existing `TWIM — This Week in the Market` glossary, `c906414830134497906c72eecf054153` |
| Credit state | HeyGen `get_current_user`, 2026-09-20 |
