# Explained with Honey — series bible (The Meticulous Investor)

A cartoon explainer series that runs alongside the channel's editorial Shorts (owner decision, 2026-10-04). It's modelled on the *system*
behind @primateeconomics (one metaphor world, one title formula, Shorts as trailers), not on their characters.
Study: `research/2026-10-04-primate-economics-study.md`.

## The world (keep it consistent; every episode reuses it)
| Real world | Hive world |
|---|---|
| People | Bees |
| Goods / value | Honey (in jars) |
| Money | Wax tokens (white hexagons) |
| Government / central bank | The hive council |
| Savings / accounts | Comb cells |
| Economy / country | The hive (the "human hive" = the real U.S. economy, used for the one real number per episode) |
| Bad shocks | Bad summers, fewer flowers, storms |

## Rules
- **Title:** `[Topic] Explained with Honey`. Shorts use the same title (no hashtag-only titles).
- **One real, sourced number per episode**, said as "In the human hive …" with an on-screen source stamp. Everything else is labelled
  an illustration. CLAUDE.md fact checking applies.
- **Language:** short, plain, rhythmic lines, one cause → effect step each. No baby-talk imitation.
- **Disconfirming beat:** each episode shows the other side (e.g. cost-push next to demand-pull).
- **Close:** a question the viewer can act on, never "follow for more".
- **Compliance:** "Educational only. Not financial advice." in the first 4 s, plus the full card at the end (COMPLIANCE.md §8).
- **Look:** near-black #0B0B0C, honey gold #F2B705, off-white #F5F5F3; red #D42A2A only for price-up/negative beats. Faint honeycomb
  background. Hand-built SVG + GSAP in HyperFrames: **no AI imagery** (an honest "no AI art" claim is possible).
- **Voice:** pilot uses ElevenLabs "Brian" (premade). Owner's house voice is "Sheldon - Voice" (HeyGen); decide per episode.
- **Format loop:** 45–65 s Short first; topics that perform get an 8–12 min long version.

## Reusable kit
`videos/honey-01-inflation-2026-10-04/build/gen.py` holds the art functions: `bee()`, `jar()`, `token()`, `flower()`. Copy the build
folder for each new episode and change the script, beats and scenes.

## Episode backlog (by demand proven on the reference channel)
1. Inflation ✅ (pilot) · 2. Tax · 3. Stocks · 4. Credit cards · 5. Compound interest (strongest hive metaphor: a growing hive) ·
6. Recession (the long winter) · 7. Bubbles (the swarm)
