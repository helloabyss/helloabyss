# PACKAGING — PARADOCS10X short 5 ("82% / 25%") — REBUILD

## Hook veto — exercised BEFORE the script was locked

The previous build failed the silent test. Shorts autoplay muted and the first frame was a
sentence. **Veto conditions on the rebuild, all now met by `SHOTLIST.md`:**

1. **`82%` is on screen in frame one.** Not faded in, not typed on, not waiting for the
   voice. The counter runs up *under* an already-legible number.
2. **Both halves of the contrast land inside 5 seconds.** B01 `82%` at ~0.0–1.2s, B04 `25%`
   at ~5.0–6.0s. A muted viewer gets the entire premise — two numbers, same agent — without
   a word of audio. The red first appears on `25%`, so the colour carries the meaning too.
3. **The notice is a strip, not a card — and it is not a disclaimer.**
   `SECONDARY REPORTING · SOURCES IN DESCRIPTION` runs as a thin strip for 0.0–4.0s.
   A full-frame card in the first four seconds would hand the hook window away. This
   video makes no financial claim, so it carries no financial disclaimer; what it owes
   the viewer is the quality of its figures, not a legal line. See **Compliance** below.
4. **No question opener, no "here's why", no second-person address.** The channel's one
   breakout short opens on a thing and a number. So does this.

**Rejected opens:** "AI agents are failing at real work" (claim before evidence, nothing to
look at); "What happens when you give an AI a real job?" (question openers test worst on
this channel); opening on the benchmark's name (nobody knows it — the number is the hook,
the name is beat 6).

---

## Title

**Pick: `Berkeley's AI Exam: 82% On The Benchmark, 25% On Real Work`**

Built to the only shape that has worked here. The one short since September to clear 1,000
views was *"New Tesla Roadster Thrust: 0-60 Under 0.9s, Half the Range"* (27s, 2,960 views,
breakout 23.4) — **a named thing, one hard number, and the cost that number hides.** Map:

| Tesla winner | This title |
|---|---|
| named thing — `Tesla Roadster` | `Berkeley` |
| hard number — `0-60 Under 0.9s` | `82% On The Benchmark` |
| the cost it hides — `Half the Range` | `25% On Real Work` |

`Berkeley` is the recognisable name here, not the benchmark — nobody searches "Agents' Last
Exam" yet. 57 characters, so it survives the mobile feed truncation.

Alternatives, in order:
2. `Agents' Last Exam: The Test Where The Best AI Scores Zero`
3. `Berkeley Gave AI Agents Real Jobs. They Passed 25%.`

**No vendor and no model is named in the title or the video.** Sources conflict on ranking
and the boards use different scoring, so a leaderboard claim is not defensible here.

## Thumbnail

⚠ **`thumbnail.png` on disk was built for the rejected typographic cut and must be rebuilt.**
It is a white-background type card and is now off-identity.

**Concept — 1080x1920, three elements, nothing else:**
- **BASE:** a frame lifted from plate **A** (the night desk, laptop the only light), graded
  to near-black. Photographic, per `STYLE-GUIDE.md` §1 — the thumbnail obeys the same
  layer-stack rule as the video.
- **`82%`** in heavy condensed white, upper third, large.
- **`25%`** in the red accent, lower third, with a thin red rule between them reading
  `SAME AGENT`.

Test at 180px wide before shipping: `82` and `25` must both still read. Lowest ink stays
≥82px clear of the bottom edge (Shorts UI). Three-colour palette only.

Deliberately **not** chasing the vidIQ thumbnail score, which rewards saturation and would
cost the channel's identity — per `CLAUDE.md`.

## Description

```
The same agent configuration scores 82% on Terminal-Bench and 25.2% on Agents' Last Exam
— UC Berkeley RDI and Snorkel AI's benchmark built from real professional work.

1,400+ task instances, drawn from 960 real workflows across 55 professional subfields,
sourced from the completed work of 300+ practitioners. Every task graded by deterministic
scripts against the expert's own deliverable.

On the hardest "Last Exam" tier, the leading configurations score 0.0%. The average across
mainstream configurations on that tier is 2.6%.

The part that is actually interesting: roughly three quarters of the failures are missing
domain knowledge and wrong approach — not broken tool execution. The tools worked. The
agent did not know the job.

The other side, which belongs in the same video: the scores are climbing fast. 24.0% at
the June launch, 38.2% on one later board, 59.3% on another in October 2026. Different
boards use different scoring, so these are directional, not like-for-like.

Where this is weak: the three-quarters failure split comes from a single analysis of the
paper, and it is the claim the video's payoff rests on. Treat it as the least solid number
here.

Figures are corroborated secondary reporting — arxiv.org, metr.org and the benchmark's own
site were unreachable at the time of writing, so nothing here is confirmed against the
primary paper (arXiv:2606.05405). Where sources conflicted, the conflict is noted rather
than resolved in the video's favour.

All statements about named people and companies are drawn from the public record, with
sources linked above.

Figures are corroborated secondary reporting. Every primary source for this topic
(arxiv.org, metr.org, the benchmark's own site) was unreachable at the time of writing, so
nothing here is confirmed against the paper itself (arXiv:2606.05405). Where sources
conflicted, the conflict is noted rather than resolved in the video's favour.

All statements about named organisations are drawn from the public record.
```

Disclaimer block is `DISCLAIMER.md` verbatim. The line above it is the required
**named individual or company** addition from `DISCLAIMER.md` — Berkeley RDI and Snorkel AI
are named in the video.

**Hashtags:** `#ai #aiagents #benchmark #berkeley #agi #technology #shorts`

## Pinned comment

Reserved for the strongest objection to the weakest claim:

> The 2.6% figure gets quoted as "AI agents pass 2.6% of real work." It doesn't mean that.
> 2.6% is the average across mainstream configurations on the hardest tier only; the
> overall pass rate is around 24%. The headline number people share is off by roughly 10x.

## Definition of done

| Artefact | State |
|---|---|
| Video | **not built** — rebuild per `SHOTLIST.md` |
| Title | ✅ above |
| Description | ✅ above |
| Thumbnail | ❌ **must be rebuilt** on a photographic base; the file on disk is the rejected type card |


## Compliance — why there is no financial disclaimer

This video names no ticker, values no company, quotes no share price and implies no
buy / sell / hold. There is nothing to disclaim. Per the per-channel test in `CLAUDE.md`,
PARADOCS10X carries the money channel's legal card **only** when a viewer is given
something to trade on.

It previously carried `Educational only. Not financial advice.` over a video about AI
benchmark pass rates, plus the full investment disclaimer in the description. That was
inherited from the money channel and it was wrong: an investment disclaimer on a
non-investment video is boilerplate, and boilerplate is a credibility cost on a channel
selling accuracy.

**On-frame notice, first 4 seconds:** `SECONDARY REPORTING · SOURCES IN DESCRIPTION` —
a thin strip, not a full card, so it does not eat the hook window.
