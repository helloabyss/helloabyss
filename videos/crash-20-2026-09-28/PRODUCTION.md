# Production — Can the Market Crash 20% in One Day? (Short, 2026-09-28)

**Status: SCRIPTED — NOT RENDERED.** The render is held on credits (below). Nothing has been submitted to HeyGen.

## Credits — why it is held

| | |
|---|---|
| HeyGen premium balance (checked 2026-09-28) | **41**, resets **2026-10-06** |
| Path | Video agent, generate mode, Alex Wright + B-roll (channel default) |
| Measured rate | **~60 cr/min** (`RENDERING.md`, render `69222606…`: 69 cr for 69.3s) |
| This script | 159 words ≈ 64s VO, plus HeyGen's ~3s closing break ≈ **67–70s** |
| **Estimate** | **~65–72 credits** — **does not fit in 41** |

Even the plain motion-graphics path (~40 cr/min, ~46 cr) does not fit. Do not submit until the balance
covers it, because a render that runs out of credits mid-job is a waste. Standing rule: ask Sheldon before spending.

## Settings (locked)

```jsonc
// mcp__heygen__create_video_agent
{
  "mode": "generate",                                   // chat stalls, RENDERING.md 2026-09-23
  "orientation": "portrait",
  "styleId": "e7f9a12679ec426099db7646b70a4639",        // Economist
  "voiceId": "0db3abd83c74452fb2460b0dd113daad",        // Alex Wright - Informative
  "brandGlossaryId": "c906414830134497906c72eecf054153",
  "prompt": "<brief below>"
}
```

## Brief — ready to submit verbatim

> Create a ~65-second vertical (9:16) YouTube Short for a FACELESS finance channel, The Meticulous Investor.
>
> CRITICAL: NO avatar, NO presenter, NO human face anywhere. Voiceover only.
> Use this narration script VERBATIM. Do not rewrite, shorten, or add to it:
> "You may have seen the claim. When yields spike, the market can crash twenty percent in one day. It has happened once. October 19th, 1987. The S&P 500 fell twenty point four seven percent. Circuit breakers came after that. Today there are three. Down seven percent, trading stops for fifteen minutes. Down thirteen, it stops again. Down twenty, it halts for the rest of the day. Under today's rules, that last level has never been hit. In March 2020, the worst day was down twelve percent. The first breaker tripped four times in eight sessions. The rules have gaps. Futures trade overnight and can fall seven percent before pausing. Stocks can open lower after a halt. And a crash can take weeks. In 2020, the S&P fell thirty-four percent in about five weeks. No breaker stops that. The real risk is not one day. Know what a thirty percent drop would do to your portfolio, before you see one."
>
> LAYER STACK, imagery-first: 1) BASE: cinematic photographic B-roll filling the frame in every scene.
> 2) MID: motion graphics over that imagery. 3) TOP: hero typography and burned-in word-by-word captions,
> current word highlighted.
>
> B-ROLL BY BEAT: (hook) rain on a window over a blurred city at night, with "−20% IN ONE DAY?" in red;
> (1987) grainy 1980s ticker board with no company names, a line chart that drops off a cliff, "−20.47%"
> tagged "S&P 500 · close 1987-10-19";
> (circuit breakers) HERO SHOT: macro of a heavy industrial breaker switch snapping open;
> (three levels) server-room corridor with a three-step staircase graphic "7% → 15 MIN · 13% → 15 MIN ·
> 20% → CLOSED FOR THE DAY", the 20% step in red, footnote "Levels 1–2 halt only before 3:25 pm ET";
> (never hit) a lever locked in place with a red stamp "NEVER TRIGGERED · current rules since 2013";
> (March 2020) a deserted city street with no people, a calendar strip 9–18 March with four red marks,
> "−11.98%" tagged "S&P 500 · close 2020-03-16";
> (overnight) a night skyline and a clock passing midnight, "FUTURES · OVERNIGHT LIMIT ±7%";
> (slow crash) a tide going out under a pier, a chart sliding from 19 Feb to 23 Mar 2020 to "−33.9%",
> with "NO BREAKER STOPS THIS";
> (close) BOOKEND: the empty trading floor from the opening, one screen lighting up, a gauge labelled
> "YOUR PORTFOLIO · −30%", with "PLAN FOR THE MONTH, NOT THE DAY."
>
> MOTION: 3D camera pushes through the imagery, hard parallax, letters arrive individually with overshoot,
> numbers count up, charts draw themselves then drop on negative beats. Cut or punch in every 1.2–1.8s.
>
> LOOK: strict three-colour palette of near-black, off-white and one red accent (#D42A2A). All imagery
> graded dark and desaturated; red only on graphics and type. Captions legible over a dark scrim.
>
> HARD CONSTRAINTS: no faces or identifiable people, no exchange, bank or corporate logos, seals or signage,
> no neon, gradients, sparkles, emoji or subscribe animations. Show "Educational only. Not financial advice."
> within the first 4 seconds. End on a held card: "Educational only. Not financial advice. Market commentary,
> not a recommendation to buy or sell any security. Figures as of the dates shown. Sources in the description."
>
> TONE: dry, confident, analytical newsroom. A neutral explainer, not a promo.

## After render — verification checklist (CDN blocked, so the render will be *complete, not verified*)
- [ ] `get_video_scenes`: Alex Wright on every scene, script verbatim, zero avatar elements, 9:16
- [ ] Watch in HeyGen: no faces, logos or signage in any B-roll plate; the grade is dark and desaturated
- [ ] "−20.47%", "−11.98%", "−33.9%", "±7%" and the 7/13/20 staircase are on screen with their stamps
- [ ] Opening card by 4s; closing card held on the final frame
- [ ] Publish the `captioned_video_url` cut (generate mode disables inline captions)
- [ ] Resolve the two `[OPEN]` flags in `SCRIPT.md` before upload
