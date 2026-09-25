# helloabyss — faceless YouTube Shorts (two channels)

Repo holds scripts, shot lists and production records for **two faceless YouTube
channels**. Video is generated with HeyGen; the repo is the durable record.

## Channels — check which one before scripting

| Channel | Type | Videos | Sign-off | "Not financial advice" card |
|---|---|---|---|---|
| **Finance channel** | Finance / money | `moat-short/`, `pdt-short/` | none | **Required**, first 4s |
| **PARADOCS10X** | **Tech** | `paradocs-*/` | "This is Paradocs 10X." | **None** — tech channel, user's call |

PARADOCS10X's recurring thesis: the winner is never a better version of the old thing, it
is the thing that removes it (horse to car, headset to glasses). If a request names
PARADOCS10X, or is about a product or technology rather than a trade or investment, it is
the tech channel.

## Before writing any script

**Verify every factual claim with a web search first.** Both channels publish claims
people may act on. Never script from memory — regulatory dates, ticker figures and
market-share numbers change. Record each claim in a fact table in `SCRIPT.md` with a
confidence level, and mark analyst estimates as estimates, never as market prices.

Include the disconfirming data. An explainer that admits where the thesis is weak is both
more honest and better content than a promo. **Finance channel only:** every video carries
an on-screen "Educational only. Not financial advice." card in the first 4 seconds. Do not
add it to PARADOCS10X videos; use small source footnotes for company figures instead.

## Thumbnail first — free mockups before any video

Before scripting or rendering a video, mock up 3 thumbnail concepts **for free** with
`node tools/thumbnail-mockup/render.mjs <video-dir>` (see `tools/thumbnail-mockup/README.md`).
Send the user `mockups/sheet.png` and get a pick. The thumbnail's hook then shapes the video's
opening. Only the chosen concept becomes a paid image: one generation, after the pick.
**Never spend image credits on exploration.**

## House style — apply to every short

**Read `STYLE-GUIDE.md` and build the brief from its template.** Both channels share this
locked visual identity. Summary of the non-negotiables:

- **Imagery-first, three-layer stack.** Cinematic photographic imagery is the BASE layer,
  motion graphics over it, type and captions on top. Never typography on abstract
  backgrounds — that was tried and rejected.
- **Faceless.** No avatars, no presenters, no identifiable people, ever.
- **No real corporate logos or badges.** Use plain text name-tags.
- **Three-colour editorial palette** — near-black, white, one red accent. Imagery graded
  dark and desaturated. No neon, gradients, sparkles or emoji.
- **Dramatic motion**, but from camera and animation, not decoration.
- **Never use another company's footage or images**, not even mirrored or remixed to get
  past Content ID. Generate generic, unbranded stand-ins.
- **No clickbait.** No subscribe animations, no "what they don't want you to know" CTAs.
  Close on something the viewer can act on.

## Fixed production settings

| Setting | Value |
|---|---|
| HeyGen style | Economist — `e7f9a12679ec426099db7646b70a4639` |
| HeyGen voice | Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad` |
| Mode | `chat` (revisable — send follow-ups into the session) |
| Orientation | `portrait` (9:16) |

Both channels use the same style and voice. Keep them constant so each channel reads as one series.

## Known environment constraints

- **HeyGen CDN egress is blocked** (`files2.heygen.ai`, `resource2.heygen.ai`). Renders
  cannot be downloaded or watched from here. Always report a render as *complete, not
  verified*, and give the user a verification checklist.
- **HeyGen `create_speech` needs separate `api` credits**, which the Creator plan lacks.
  No detached VO stem is available; narration is baked into the render.
- **Higgsfield: ~530 credits** (Sep 2026). It's the only connected text-to-image generator
  (GPT Image 2.5 at 2K is ~1.4 credits per image). **Generate one image at a time and ask the
  user before spending any more.**
- **Adobe connector: no image generation** (generative AI is disabled apart from outpainting).
  Use it at no generation cost to **look at images** (`asset_inline_preview` fetches URLs this
  container can't reach, e.g. Higgsfield's cloudfront), for Photoshop-style edits, for
  Stock search, and for text layout in Express.
- **vidIQ: ~1 credit.** Thumbnail generation costs 22, scoring 5. Needs a top-up.
- vidIQ thumbnail scores penalise low saturation and reward vibrancy. That conflicts with
  this channel's editorial palette. **Do not chase the score** at the cost of the identity.

## Repo layout

One directory per video: `SCRIPT.md` (VO, fact table, shot list, packaging) and
`PRODUCTION.md` (session IDs, settings, verification checklist, constraints hit).
