# Disclaimer — required on every video

**No video naming a ticker ships without every item in this file.** This is a
publication gate, not guidance.

## On screen

A thin strip along the bottom edge reading **EDUCATIONAL ONLY. NOT FINANCIAL ADVICE.**,
present from frame one to the last frame, never a full-frame card (`STYLE-GUIDE.md`
§5A: the card eats the hook). White type on near-black; on a dark scene it keeps a red
hairline above it so the strip still reads as a separate element.

## In the description, first paragraph, above the fold

> Educational content only. Nothing here is financial, investment, tax or legal advice,
> and nothing here is a recommendation to buy or sell any security. I am not a licensed
> financial adviser. Figures are taken from company filings and primary sources as of the
> date stated on screen and may be out of date by the time you watch. Do your own research
> and speak to a licensed professional before acting. You can lose money.

## Per-figure discipline

| Requirement | Why |
|---|---|
| Every figure carries its **as-of date** on screen or in the line that states it | Filings supersede; a number without a date is a claim about today |
| Analyst estimates and guidance are labelled **estimate** or **guidance**, never price | `CLAUDE.md`: never present an estimate as a market price |
| Derived figures are labelled **CALCULATED** | e.g. Micron net margin ≈63.8% is computed from net income ÷ revenue, not reported as such |
| A chart's bar lengths are **proportional** to the figures they carry | Equal bars for unequal numbers is a lie, whatever the caption says |
| No invented series | If a price path is drawn, every point is an observed print. Decorative "trend lines" are forbidden |

## Positions

State any position in the named tickers in the description, or state plainly that there
is none. **Current status: no positions held in SPCX, BE, MU or NVDA.** Re-confirm this
before each upload — do not copy it forward unchecked.

## The counter-evidence rule

Every ticker that gets a bull case gets its disconfirming number in the same video,
signposted out loud. This is an editorial rule in `CLAUDE.md` and it is also what keeps
the channel from being promotional. A video that fails it does not ship.

## Pre-upload checklist

- [ ] Bottom strip present frame one to last, legible on every scene
- [ ] Description disclaimer, first paragraph
- [ ] Every figure dated; estimates labelled; derived figures marked CALCULATED
- [ ] Charts proportional; no invented data
- [ ] Positions stated and re-confirmed today
- [ ] Each ticker's counterweight present and spoken
- [ ] Fact table in `SCRIPT.md` has a confidence level on every row
- [ ] A human has watched the render end to end (renders cannot be verified from the agent
      environment — the HeyGen CDN is egress-blocked)
