# Production Record — "Follow Amazon's AI Money"

## Session
- **video_id:** `687c8bf4b72e4420ab0bbc619c34c674`
- **Watch:** https://app.heygen.com/videos/687c8bf4b72e4420ab0bbc619c34c674
- **session_id:** `c2de770cd4eb4db0869681c38f853022`
- **Mode:** `generate`
- **Style:** Economist — `e7f9a12679ec426099db7646b70a4639`
- **Voice:** Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad`
- **Orientation:** portrait 9:16

### Chat mode not attempted — it is now the known-broken path
Chat mode 404'd again on the ETF short built earlier today (session
`baed2cc7ccb547fab464368b4e195246`), which is the **fourth** occurrence across two build
sessions. The endpoint was confirmed healthy at the time (an older session read back fine)
and credits were not the cause. No further chat attempt was made here — it would have cost
a session id and produced nothing.

**`STYLE-GUIDE.md` §7 should be updated:** it currently frames chat as the default and
generate as the fallback. On this account that is backwards. Left unedited because the style
guide is the locked channel document and changing it is your call, not mine.

The six load-bearing constraints were hoisted to the top of the prompt as a numbered block to
compensate for the missing blueprint-approval step, including the explicit
"burned-in captions must be enabled" that the PARADOCS10X render failed.

## The angle
The brief said follow the money, so the money is the structure. The obvious story is
Amazon → Qualcomm, up to $60B. The actual story is the **$4B warrant travelling the other
way**: Qualcomm is paying its customer to become a customer, and the payment is already
partly made — 3.75M of 25M shares vested on initial commitments alone, before the revenue
starts.

That reversal is the video. It is also why the money-flow animation earns its place rather
than being decoration: **one diagram in three states** — thick line out ($60B), second line
back (the warrant), outbound line thinning (Amazon's own silicon taking the work). Someone
watching with sound off still gets the argument.

**HERO shot:** a fibre-optic patch panel, one strand pulsing left-to-right, then a second
pulsing right-to-left. Two directions on one panel — the thesis, and literally the optical
connectivity that is part of the deal.
**BOOKEND:** a server aisle, pushed down at the open and reversed out of at the close.

## No winner is picked — and how that was enforced
The brief required exploring opportunity and competition without predicting a stock winner.
Three things enforce it:
1. **The share-price reaction is excluded entirely.** Sources conflict (+5%, +9.5%, "nearly
   10%") and could not be reconciled against a primary quote from this environment. It is
   also the number most likely to read as a call.
2. **Analyst estimates are excluded from the VO** — inference market-share projections and
   the 1.5–2% gross-margin dilution estimate. `CLAUDE.md` requires estimates be marked as
   estimates; rather than burn VO time hedging, the argument runs on company-reported
   figures only. Both are recorded in `SCRIPT.md` and flagged in the pinned comment.
3. **The prompt states it as a hard constraint** — no price target, no buy/sell framing, no
   ranking, no rising stock chart.

The close is an instruction to watch a public filing. That is genuinely actionable and takes
no position: the warrant vests as Amazon buys, so the vesting disclosures are a public meter
on whether the $60B ceiling is turning into real orders.

## Logos — text name-tags, and why the render could not do otherwise
The brief asked for company logos. Two independent reasons it is name-tags:
1. `CLAUDE.md` and `STYLE-GUIDE.md` §4 ban real corporate marks outright.
2. **The tool cannot deliver them anyway.** HeyGen generates imagery; asking a generative
   model for real trademarks yields mangled near-miss logos — simultaneously worse for brand
   accuracy, legal exposure and house style than clean typography.

**If you want real marks, the path is compositing, not prompting:** render clean, then lay
actual PNG assets over the name-tag plates in an editor. That needs either an editor with
asset support (the Adobe connector discussed in `etf-distributions-short/PRODUCTION.md`) or
Higgsfield credits. Neither is available right now. The name-tag plates are deliberately
placed and timed so they could be replaced by PNGs later without a re-render.

## Fact-checking — read before publishing
Full table in `SCRIPT.md`, 13 claims. The deal is one day old (announced 8 Sep 2026) and the
figures are unusually consistent across outlets because they trace to a single Reuters wire
and a single Qualcomm release.

**`reuters.com`, `cnbc.com`, `theregister.com` and `sec.gov` are all egress-blocked here**, so
every figure came from search-index snippets rather than the source pages, each corroborated
across at least two independent queries.

**The one to re-read before publishing:** the **3.75M already-vested** figure. It is the most
specific claim in the video and the least repeated across coverage. Check Qualcomm's own
release or its 8-K. Everything else ($60B ceiling, 25M shares at $161.26, Sept 2036,
inference focus, $25B AWS run rate) appeared consistently across multiple outlets.

## NOT VERIFIED — needs your eyes
HeyGen CDN egress is blocked; the render will be **complete, not verified**. Check:
1. **No human face anywhere.**
2. **Burned-in captions enabled** — the defect the PARADOCS10X render shipped with.
3. **Imagery-first** — every scene needs a photographic BASE plate. Watch for type on flat
   backgrounds.
4. **No logos anywhere** — especially check the two "monolith" structures and the phone logic
   board for hallucinated brand marks. This is the highest-risk shot list yet for that,
   because the script names four real product lines.
5. **The money-flow diagram actually changes state three times.** If it renders once and
   repeats unchanged, the video loses its spine — that is a re-run.
6. **The counter-evidence section survived** ("Now the other side … no delivery date was
   disclosed"). If trimmed for runtime, re-run; without it this becomes a promo.
7. **No winner implied** — no rising stock chart, no ranking graphic, no green arrows.
8. **Palette** near-black/white/one red. **Compliance card** in first 4s.
9. **Cut rhythm** — no shot past ~2s.

## Constraints hit
- HeyGen CDN egress blocked — complete, not verified.
- `create_speech` needs separate `api` credits (Creator plan lacks them) — no detached VO stem.
- Higgsfield 0 credits — no custom B-roll. Worth buying if topped up: the fibre-panel hero
  and the three-state money-flow diagram, the two shots most likely to be approximated badly.
- vidIQ ~1 credit — use HeyGen's session thumbnail.
- News and filing domains egress-blocked — see fact-checking above.

---

## RENDER COMPLETE — one script defect, one repeat defect

- **Watch:** https://app.heygen.com/videos/687c8bf4b72e4420ab0bbc619c34c674
- **video_id:** `687c8bf4b72e4420ab0bbc619c34c674`
- **Duration:** 95.3s · 9:16 · 1080p · 19 scenes
- **HeyGen auto-title:** "Qualcomm vs Amazon: The AI Silicon Stakes" — **do not use it.** Beyond
  being off-script per `STYLE-GUIDE.md` §7, the "vs" framing works against the whole point of
  this video, which takes no side. Upload under a title from `SCRIPT.md`.

### Verified from scene data (not from watching — CDN egress is blocked)
| Check | Result |
|---|---|
| VO script verbatim | **FAIL — one duplicated line**, see below |
| The counter-evidence section survived | **PASS** — scenes 13–17 carry it complete |
| No-winner close intact | **PASS** — scenes 18–19 verbatim |
| Series voice (`0db3abd8…`) on every scene | **PASS** |
| 9:16 portrait, 1080p | **PASS** |
| **Burned-in captions** | **FAIL — `caption.enabled: false`** (3 for 3 on generate mode) |
| Imagery-first base layer / palette / logos | **UNKNOWN** — needs human eyes |

### DEFECT 1 — "Roughly four billion dollars" is spoken twice
Scene 8 ends `"at a hundred sixty-one twenty-six. Roughly four billion dollars."`
Scene 9 opens `"Roughly four billion dollars. The supplier is paying the customer to become a
customer."`

The agent split the script across scenes and **repeated the sentence at the seam**. In the
finished audio the narrator says the line, then says it again. Everything else in the VO is
verbatim — this is the only duplication in 19 scenes.

**Recommended fix: trim it in an editor, do not re-run.** It is roughly two seconds at a
single scene boundary, the surrounding audio is clean, and the rest of the render is correct.
A fresh generate-mode run costs credits and would re-roll every other constraint — including
the three that currently pass — for one bad seam. If you would rather re-run, the mitigation
is to remove the sentence-level repetition risk by not ending a sentence and beginning the
next scene on the same clause.

### DEFECT 2 — captions disabled again
Third consecutive generate-mode render with `caption.enabled: false`, despite the instruction
being constraint #5 at the top of the prompt in capitals. **This is now established behaviour,
not variance.** Publish the captioned cut instead:
`captioned_video_url` → `caption_687c8bf4b72e4420ab0bbc619c34c674.mp4`, linked from the video
page. An `.srt` is also exposed if you would rather burn captions in an editor with control
over the word-by-word highlight — which, given Defect 1 needs an editor pass anyway, is
probably the efficient route: fix the seam and burn the captions in the same session.

### Pacing — the bigger concern on this one
19 scenes across 95.3s averages **~5.0s per scene**, against a house rule of a cut or punch-in
every 1.2–1.8s and nothing past 2s. The ETF render came in at ~3.3s per scene; this is
noticeably slower. Scenes can contain internal cuts, so this is not proof — but two renders
now trend the same direction, and this one is the worst. **Watch specifically for static
holds.** If the piece drags, that is a re-run with the cut rhythm made the single loudest
instruction in the prompt, above even the imagery rule.

### Still unresolved: the white-background reading
Same as every prior render — every scene reports `background: {color: '#ffffff'}` with one
`motion_graphics` element, which `get_video_scenes` does not describe. Cannot be resolved
without watching. Check first whether the server-hall and wafer plates are actually there.

### Highest-risk thing to check by eye on this video specifically
**Hallucinated logos.** The script names Qualcomm, Amazon, AWS, Apple, Trainium, Graviton and
Nitro. That is seven real brands in 95 seconds — far more brand surface than any previous
video in this repo. The prompt bans marks explicitly and in three separate places, but this is
the render most likely to have produced a mangled near-miss logo anyway. Check the two
"monolith" structures and the phone logic board first.

## Thumbnail
`thumbnail-amazon-qualcomm.png` — 720x1280, built from `thumbnail-kit/amazon-qualcomm.html`.
Hero reads **$60B OUT. / $4B BACK.** over the two-way flow: a thick white arrow running Amazon
to Qualcomm, a shorter red one running back. It is the same reversal the video is built on,
compressed to one frame.
Company names are **plain text**, consistent with the videos — no marks, so the thumbnail
carries no trademark risk on a video that scrutinises both companies.
Built locally with Chromium; see `thumbnail-kit/README.md`.
