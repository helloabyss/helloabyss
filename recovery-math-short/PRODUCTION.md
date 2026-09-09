# Production Record — "Lose 50%. Need 100%."

## Session
- **video_id:** `6ec2edbe28814f31958210898e4c61f9`
- **Watch:** https://app.heygen.com/videos/6ec2edbe28814f31958210898e4c61f9
- **session_id:** `35d0808af1ff47ffbb95cc9f6de7a946`
- **Mode:** `generate` (chat mode has 404'd four times across two sessions; not attempted)
- **Style:** Economist — `e7f9a12679ec426099db7646b70a4639`
- **Voice:** Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad`
- **Orientation:** portrait 9:16

## Two decisions taken from direct answers, not inferred

### Voice: unchanged newsroom register
The brief asked for a "Wall Street guru / trapper / Einstein of Wall Street" persona, which
collides head-on with `STYLE-GUIDE.md` §4 ("dry, confident, analytical newsroom — never a hype
guru"). Asked, and the answer was **same newsroom voice as before**. So the persona is dropped
entirely and the style guide stands unamended. The prompt asks for "a teacher who is certain",
which is as far toward the Einstein reading as the locked tone allows.

### Channel: The Meticulous Investor
Two channels exist — Paradocs10X and The Meticulous Investor. This is a finance explainer in
the same series as the ETF and Amazon shorts, and Paradocs10X is the separate parable/futurism
series that already has its own sign-off ("This is Paradocs 10X"). So this signs off as **The
Meticulous Investor**. If that is backwards it is one line of VO and one end card — but it
does require a re-render, because narration is baked in and the Creator plan has no detached
VO stem.

**Worth adding both channel names to `CLAUDE.md`.** Nothing in the repo recorded them, which is
why this needed asking at all. Not edited here because `CLAUDE.md` is a locked channel document.

## The CTA, and why it is not a subscribe animation
The brief asked for a CTA naming the channel. `CLAUDE.md` bans subscribe animations and
clickbait CTAs but requires closing on something actionable. The existing precedent resolves
it — `paradocs-short-1` closes "Full breakdown on the channel. This is Paradocs 10X."

So the close is an instruction plus a series mark: *"Run the number on your worst position
before you average down. This is The Meticulous Investor."* No subscribe button, no bell, no
follow-bait — and the prompt bans all three explicitly.

## Why this one is animation-dense
The brief asked for more animation each time out, and this topic allows it: the arithmetic is
trivial, so none of the runtime is spent teaching a concept. One physical object carries
everything — a stack of 100 steel blocks that only ever loses blocks, gains blocks, or is
measured against a ghost outline of its original height.

The hero moment is literal: on "that fifty has to double", 50 blocks are set onto a pile of 50
in one continuous move and the stack **doubles** to meet the outline. The audience sees why
+50% is not enough before the narrator finishes saying it.

That frugality is what buys the density in the back half — the four stepping recovery bars, the
carved-wall drawdowns, the split-flap calendar spinning 2000 to 2015.

## Fact-checking
Full table in `SCRIPT.md`, 12 claims. Items 1–7 are arithmetic and need no source; the video
shows its own working. Items 8–12 are long-settled market history.

**Two traps this script deliberately avoids, both flagged in the fact table:**
1. **Breakeven percentage.** Exact closes give **+131.4%** for the 2007–09 S&P decline; several
   secondary sources round to "+133%". The script says *roughly a hundred and thirty*, correct
   under either. **Do not "tighten" this to 133%.**
2. **Peak-to-recovery vs trough-to-recovery.** The script says "five and a half years **from the
   peak**" (Oct 2007 → Mar 2013). From the March 2009 trough it is about four years. Commentary
   mixes these constantly; stating which one is the difference between accurate and sloppy.

Market-data domains are egress-blocked here, so items 8–12 came from search-index snippets.
Confidence is High anyway because these are decades-old figures consistent across many
independent outlets — unlike the Amazon short, where the deal was one day old.

## Thumbnail
`thumbnail-recovery-math.png` — 720x1280, from `thumbnail-kit/recovery-math.html`.
Hero reads **LOSE 50%. / NEED 100%.** over two paired bars where the red recovery bar is
visibly exactly twice the white loss bar. The asymmetry is the image; no reading required.

## NOT VERIFIED — needs your eyes
HeyGen CDN egress is blocked; the render will be **complete, not verified**. Check:
1. **No human face, person or hand anywhere** — hands were banned explicitly since blocks are
   being stacked and that is a natural place for the model to add one.
2. **Burned-in captions.** Disabled on the last three generate-mode renders. Expect to publish
   the separate captioned cut.
3. **The doubling actually reads.** If the stack just "gets taller" rather than visibly
   doubling against the ghost outline, the video loses its one job. This is the re-run trigger.
4. **The counter-evidence beat survived** ("what the math does not say: sell to avoid it").
5. **The end card says exactly THE METICULOUS INVESTOR**, and there is no subscribe/bell/follow
   animation anywhere near the close.
6. **Imagery-first, palette, compliance card in first 4s, cut rhythm** — the standing checks.

## Constraints hit
- HeyGen CDN egress blocked — complete, not verified.
- Higgsfield 0 credits, vidIQ 1 credit — no generative B-roll, no generated thumbnail.
- No detached VO stem on the Creator plan, so any wording change means a full re-render.
