# Numbers file: PX "0.24 Wh. Or 0.10." (locked 2026-10-27)

Format follows `reference/build-playbook/*/numbers.md`. Every figure that
appears on screen or is spoken, with its source.

| On screen / spoken | Value | Source | Grade |
|---|---|---|---|
| 0.24 Wh | Median Gemini Apps text prompt, full fleet-wide accounting | Google technical report, May 2025 data, via corroborated secondary reporting | SECONDARY |
| 0.10 Wh | Same prompt, active TPU and GPU only | Same report, narrower boundary | SECONDARY |
| 0.17 Wh | Plus host machine, idle capacity, data-centre overhead | Same report, middle boundary | SECONDARY |
| 2.4x | 0.24 / 0.10 | arithmetic | DERIVED |
| "median" | The figure is a median, not a mean or a typical cost | Same report | SECONDARY |
| "text prompts only" | Excludes voice and image prompts | Same report | SECONDARY |
| "never publishes how many prompts it serves" | No public prompt-volume figure | Absence of a published figure | SECONDARY |

THUMB_OK: 0.10, 0.24, 2.4x

## Source grade, stated plainly
**Nothing here is CONFIRMED.** Per `CLAUDE.md`, primary sources are DNS-blocked
from this container — `WebFetch` returns `getaddrinfo ENOTFOUND` — so the paper
and Google's own post were never opened. Every figure is corroborated secondary
reporting. That is why the on-frame strip reads `GOOGLE FIGURES · MAY 2025 DATA
· SOURCES IN DESCRIPTION` and why no line is set as a verbatim quotation.

## Not used
- Any total energy figure for Gemini. Prompt volume is unpublished, so a
  per-prompt number cannot be multiplied into a credible total. The video says
  this out loud rather than inventing one.
- Comparisons to a kettle, a car mile or a household. Every one needs an
  assumption the sources do not supply.
- "Google hid the number." They published every line; the video says so.
