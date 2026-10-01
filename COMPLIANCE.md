# COMPLIANCE — This Week in the Market

**Non-negotiable. Read before writing, enforce before publishing.**

This channel publishes **market commentary and news**. It does not publish investment
advice. Every rule below is a hard gate: a script that breaks one does not ship until it
is fixed. When a rule and a good line conflict, the rule wins.

---

## 1. The bright line: commentary, not advice

| Never say | Say instead |
|---|---|
| "Buy NVDA here" / "This is a buy" | "The stock rose four percent on the print." |
| "This stock will hit $300" | "Goldman's analysts raised their target to three hundred dollars." |
| "You should be positioned for a cut" | "Fed funds futures now price a cut in December." |
| "This is a great entry" | *(cut entirely — there is no compliant version)* |
| "It's going higher from here" | "It closed at a record. Whether that holds is a separate question." |

**Banned constructions — search for these before shipping:**
- `buy`, `sell`, `hold`, `accumulate`, `load up`, `take profits` as a recommendation to the viewer
- `will` attached to a price or direction ("will rally", "will fall to")
- `should` directed at the viewer ("you should", "investors should")
- price targets stated as fact or expectation rather than as somebody's published estimate
- `undervalued` / `overvalued` / `cheap` / `expensive` in the channel's own voice — only ever attributed

> `undervalued` is not banned as a word. It is banned **unattributed**. "Morgan Stanley's
> analysts call it undervalued" is reporting. "It's undervalued" is advice.

## 2. Attribution is mandatory for every forward-looking statement

Every forecast, target, estimate or opinion is attributed **in the narration itself**, not
only on screen. The viewer hears whose view it is.

- ✅ "Goldman's analysts expect two cuts next year."
- ✅ "The median FOMC participant now sees one more cut in 2026."
- ✅ "Consensus was for two hundred thousand jobs."
- ❌ "Two cuts are expected next year."
- ❌ "We're looking at two cuts."

**Analyst estimates are never presented as market prices.** If a number is an estimate, the
word "estimate", "forecast", "target" or "expects" appears in the same sentence, and an
on-screen footnote carries the source. (House precedent: the `$100B` Morgan Stanley
Supercharger figure in `moat-short` carries a "Morgan Stanley est." footnote.)

## 3. Past performance is history, never a prediction

- ✅ "The index has closed higher in nine of the last eleven sessions."
- ❌ "The index has closed higher in nine of eleven — momentum is on its side."

Never attach a forward implication to a historical run. State the record and stop. Seasonality,
"this pattern usually resolves", and "historically this leads to" are all forward implications
wearing a historical costume.

## 4. No implied urgency

Banned outright: "before it's too late", "get in before", "last chance", "don't miss",
"acting now", "while you still can", countdown framing on an investment decision.

The viewer is never given a reason to hurry. A weekly market recap has no deadline.

## 5. Geopolitics and China — describe, don't editorialize

The viewer wants the market read, not a politics take. This is the rule most likely to be
broken by accident, because the source material is itself partisan.

**Do:**
- Describe the event, the policy, and the market reaction, in that order.
- Name the transmission mechanism: "the export controls hit Nvidia's China revenue line."
- Attribute characterizations to whoever made them.

**Don't:**
- Characterize governments, leaders, or systems as good, bad, aggressive, or hostile in the
  channel's own voice.
- Take a side on a dispute, territorial claim, or election.
- Use loaded framing: "regime", "crackdown", "bullying", "capitulation", "provocation".
  Use "policy", "restriction", "measure", "response".
- Speculate about intent. "Beijing is trying to punish…" is editorializing.
  "The measure restricts X" is reporting.

**Disputed official data gets flagged, never presented flatly.** Where official Chinese
figures (GDP, youth unemployment, PMI) are contested or where the series has been
suspended or redefined, say so in the narration:
> "Official GDP came in at five percent — a figure a number of outside economists
> dispute."
Where an independent read exists (e.g. Caixin PMI alongside the official PMI), cite both.

## 6. Sourcing — primary documents or it gets cut

Every factual claim traces to one of:
- an SEC filing (10-Q, 10-K, 8-K) or a company IR press release / earnings call transcript
- a central bank release (FOMC statement, SEP/dot plot, minutes, PBOC release)
- an official statistical print (BLS, BEA, Census, ISM, S&P Global)
- an exchange or official market data source for prices and levels

**A news article is a pointer to a primary document, not a source.** Follow it to the
document. If the primary document cannot be located, the claim is **cut** — not softened,
not hedged, cut.

Analyst estimates are a permitted exception **only** when attributed by name (rule 2).

## 7. Every number carries an as-of timestamp

No bare numbers. Each figure in `research/` records the value, the source, and the
timestamp. In the script and on screen, the as-of is visible wherever the number could
move:
- Prices, levels, yields: date **and** whether it is a close or intraday, e.g.
  `S&P 500 · close 2026-09-18`
- Prints: the reference period, e.g. `CPI · August 2026`
- Estimates: the publication date, e.g. `Morgan Stanley · 2026-09-15`

Market levels quoted in narration state their reference point out loud: "as of Friday's
close."

## 8. The disclaimers — exact wording, written once, reused verbatim

**On-screen, first 4 seconds** (house-wide, matches the existing channel):
```
Educational only. Not financial advice.
```

**On-screen, final frame** (full card, held to the end of the video):
```
Educational only. Not financial advice.
Market commentary, not a recommendation to buy or sell any security.
Figures as of the dates shown. Sources in the description.
```

**Video description — pasted verbatim, every episode, at the end of the description:**
```
Educational and informational content only. This is market commentary and news, not
financial, investment, tax or legal advice, and not a recommendation to buy or sell any
security. Figures are accurate as of the dates stated on screen and may have changed.
Forecasts and price targets are the views of the analysts or institutions named, not of
this channel. Past performance does not indicate future results. Do your own research and
consider speaking with a licensed financial professional before making any investment
decision.
```

Both on-screen cards are part of the shot list, not an afterthought. A cut without the
opening card in the first 4s and the closing card on the final frame does not ship.

## 9. Pre-ship checklist — run this on every draft

Copy into the script file and tick every line. **Any unticked line blocks publication.**

- [ ] No buy/sell/hold recommendation, explicit or implied
- [ ] No price target or forecast stated in the channel's own voice — every one attributed by name
- [ ] No `will` + direction/price; no `should` directed at the viewer
- [ ] No unattributed valuation judgement (cheap/expensive/undervalued/overvalued)
- [ ] No historical run given a forward implication
- [ ] No urgency language of any kind
- [ ] Geopolitics/China: events and reactions described, no characterization of governments, no intent-reading
- [ ] Disputed official data explicitly flagged as disputed
- [ ] Every claim traced to a primary document, linked in `research/`
- [ ] Every number carries an as-of date; market levels state close vs intraday
- [ ] Opening card "Educational only. Not financial advice." in first 4s
- [ ] Closing disclaimer card on final frame, verbatim from §8
- [ ] Description disclaimer pasted verbatim from §8
- [ ] Every beat lands on a named US ticker, sector or index with the mechanism stated

## 10. Flagging

Anything in a draft that brushes one of these lines is surfaced **before** the script is
called finished, in a `## COMPLIANCE FLAGS` section in the script file:

```
## COMPLIANCE FLAGS
- [RESOLVED] Beat 4 read "chips are the trade here" — advice-adjacent. Rewritten to
  "the reaction was concentrated in semis."
- [ACCEPTED] Beat 6 attributes a target to Goldman by name. Permitted under §2.
- [OPEN] Beat 7 cites a Reuters figure I could not trace to the PBOC release. Per §6 this
  is cut unless the primary document is found.
```

An `[OPEN]` flag blocks the ship. Resolve it or cut the beat.
