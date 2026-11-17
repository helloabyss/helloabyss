# helloabyss — production records for three YouTube channels

This repo is the durable record (scripts, outlines, fact tables, packaging, production
notes) for three channels. **The repo is PUBLIC.** The owner's private brief lives outside
it. Never commit personal details: no name, location, time zone, age or era hints, voice
names or account IDs beyond what is already here.

## Hard workflow rules

- **Nothing gets built until the owner says GO.** That covers scripts, voiceovers, renders,
  paid credits and thumbnails. Pitches and outlines are fine.
- **Outline gate:** every script starts with a one-sentence thesis, a named text structure
  (and why it fits), and section beats. The owner approves the outline before scripting.
- **Evidence first:** every number needs a primary source and a date in the fact table.
  Never script from memory. Re-lock prices, percentages and counts on post day. Flag anything
  you can't source; never estimate it in.
- Lock the script before the voiceover is recorded. After the VO exists, change only
  overlays, titles and thumbnails.
- Ask before spending ElevenLabs, Higgsfield or vidIQ credits.
- The owner uploads everything. Never upload.
- When the owner catches a flaw, fix the check that let it through, not just the one video.

## Channels

| | PARADOCS10X (PX) | The Meticulous Investor (TMI) | Late to Vice (LTV) |
|---|---|---|---|
| Lane | AI and tech only, told as a tech story. **Not a money channel.** No investing angles. | Wealth-building plan-builder. Every video ends on one "ADD TO YOUR PLAN" step. | GTA 6, with "Late Spawn," a first-timer learning in real time. |
| Format | Cinematic documentary long-form | Long + 1-minute Shorts | Owner's own gameplay |
| Look | Black and teal, teal X avatar | Host Zul (match the character sheet; never guess his look) | Fresh cover layouts; cut CapCut end cards |
| Music | Driving electronic | Piano and ambient (calm for drops, upbeat otherwise) | — |
| Voice | One energetic HeyGen voice | HeyGen "Alex Wright – Informative" | The owner's own |
| Status | Active | **Undecided. Ask before planning.** | Starts at the GTA 6 launch |

PX and TMI never share a company story, a music track, B-roll or a cover layout.

## Writing rules

- State the thesis in the first 30 seconds. The hook's topic *is* the thesis.
- Link sections with causal reasoning ("because," "so," "as a result"). **Banned:**
  rhetorical-question links and labels ("The catch?", "Twist:", "Here's the thing").
- One question per video. If a title says "why," the script answers why.
- Always include the other side (what could prove the thesis wrong).

## Public-text fail checks

- Never use the word "cap" in titles, thumbnails or on-screen text.
- No hint of the owner's location, and no time zone other than ET.
- LTV: no age or era hints about the persona (the full banned-word list is in the private brief).
- No "AI voice" or "Narrated by" lines in descriptions. The AI-use toggle is set in Studio.
- Titles in title case, never all caps, no hashtags in titles, at most 3 on-topic hashtags.
- No slide-deck look: every scene sits over real footage or imagery, with motion graphics as overlays.

## Delivery package (hold the video if any piece is missing)

1. Video under 100 MB. 2. Cover (A/B welcome), checked against past covers for layout
repeats. 3. Title, description (chapters, sources, credits), tags, pinned comment.
4. Recommended post time (ET). Never post several videos within the same hour.

## Known environment constraints

- The `helloabyss` cloud environment allows youtube.com, so `yt-dlp` (pip) can pull public
  stats, chapters and captions.
- **HeyGen CDN egress is blocked** (`files2.heygen.ai`, `resource2.heygen.ai`). Renders
  can't be downloaded or watched from here. Report a render as *complete, not verified*.
- HeyGen `create_speech` needs separate API credits. Narration is baked into renders.
- Higgsfield: 0 credits (last checked). vidIQ: 26 credits on 2026-11-17, 5 per call.

## Repo layout

- `research/`: growth and structure analyses.
- One directory per video: `SCRIPT.md` (outline, VO, fact table, shot list, packaging)
  and `PRODUCTION.md` (settings, verification checklist, constraints hit).
- `STYLE-GUIDE.md` is the **legacy** style for the earlier faceless finance Shorts
  (red/black/white, no logos). It does **not** apply to PX long-form or TMI-with-Zul.
  Keep it for reference only.
