# Which text structures correlate with growth?

Data pulled 2026-11-17. Per-video coding is in [`structure-coding.md`](structure-coding.md).

## Bottom line

1. **Compare & contrast (C&C) and cause & effect (C&E) raise the floor, not the ceiling.**
   Across 12 benchmark channels, 0 of 19 C&C or C&E videos flopped (under 0.2× their channel's
   median), against 20 of 65 for the other structures. Fisher exact test p = 0.004.
   They don't produce bigger hits, though: median performance isn't clearly different (Mann-Whitney p = 0.16).
2. **Pure description is the default everywhere, and it predicts nothing.** Just Explained
   used the same "Every X Explained" list structure in all 8 sampled videos and got
   1.97M at the top and 2.5K at the bottom. Topic, timing and packaging decided those
   results, not structure.
3. **Problem & solution (P&S) as the main structure is the weakest.** Median 0.26×, with 3 of 6 flops.
   That matters for TMI, whose whole format is problem → plan step.
4. **Story-told chronology works for money content.** Crayon Capital (317K subscribers) tells
   every video as a 4-act history story. Even its weakest sampled video got 68K views.

## Proposed structure rule (for approval)

- **Spine: compare & contrast** (then vs now, promise vs reality, A vs B).
- **Links: cause & effect.** Every section explains *why* the contrast exists and *so what*
  follows. This also enforces the "because / so / as a result" writing rule.
- **Never use pure description or a topic roundup as the spine.**
- **Never use problem & solution as the spine.** TMI's plan step stays as the *closing beat*,
  earned by the contrast, not as the structure.
- **Review after 3 videos per channel** on CTR, average % viewed and subscribers per video, per the brief's judging rules.

## Sample

| Group | Channels | Videos coded |
|---|---|---:|
| PX benchmarks | Not Unprecedented, JoshSullivanSpace, Just Explained, Territory, DeepSpaceCourier | 35 |
| TMI benchmarks | Crayon Capital, Joyee Yang, JP Finance | 24 |
| LTV benchmarks | BreeZe GTA, MrGTA, GrandGecko, No Fast Travel | 25 |
| Own long-form, 2026 | PX, TMI | 25 |
| Own Shorts (title-coded) | PX, TMI (latest 30 each) | 60 |

Competitor selection: the top 5 and bottom 3 long-form videos by views from the last ~12 months,
with videos under 10 days old excluded from the bottom picks. Videos with no narration
(ambience and walkthroughs) were excluded.

## Results by structure (benchmarks, x = views / channel median)

| Structure | n | Median x | Hits ≥3× | Flops <0.2× |
|---|---:|---:|---:|---:|
| Description / list | 40 | 5.2 | 24 | **13** |
| Chronological / sequence | 19 | 5.1 | 13 | 4 |
| Compare & contrast | 12 | 5.0 | 7 | **0** |
| Cause & effect | 7 | 5.1 | 6 | **0** |
| Problem & solution | 6 | **0.3** | 2 | 3 |

(Hit counts are inflated by the top-5 sampling. Read the flop column.)

The bottom 3 picks per channel are where structure shows up. Of 18 bottom videos, 13 are
description, 3 are problem & solution, 2 are sequence, and **none** are C&C or C&E.

### Own channels (weak evidence: view counts are 3–71, so mostly noise)

- PX + TMI longs, 2026: C&E median 3.1× own median (n = 4), C&C 0.6× (n = 7),
  description 0.9× (n = 6), P&S 0.7× (n = 4). Too small to conclude anything.
- PX Shorts whose titles carry a contrast (e.g. "Under 0.9s, Half the Range"): median **964**
  views (n = 4), against **150** for label titles (n = 26). TMI: 144 (n = 3) against 45 (n = 17).
  This direction matches the benchmarks.

## Confidence: moderate on the floor effect, low on everything else

- **Single coder** (Claude), coding from chapter titles and descriptions. Transcripts weren't
  available because YouTube blocks caption and watch-page requests from this server, and vidIQ
  transcripts cost 5 credits each. A second pass on transcripts could move borderline codes.
- **Confounds:** the GTA C&C videos all landed in launch-hype weeks. Not Unprecedented has
  only 6 videos and no bottom picks. 8 channels supply all the C&C/C&E videos.
- **Subscriber growth per video isn't public.** "Growth" here means views relative to channel
  size. Studio data (subscribers gained per video) would be the real test for your channels.
- The brief's own audit agrees: "Compare and contrast is the only structure that worked."
