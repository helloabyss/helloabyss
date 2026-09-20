# YouTube Short — "Follow Amazon's AI Money"

**Runtime target:** 75–82s · **Format:** 1080x1920 (9:16) · **Style:** faceless, imagery-first
**Voice:** Alex Wright – Informative · dry, confident, analytical newsroom

---

## VO SCRIPT (203 words)

**[HOOK]**
> Want to understand the AI stock race? Follow who's getting paid.

**[THE NEWS]**
> September eighth. Qualcomm and Amazon announce a multi-generation deal — custom silicon
> for AWS data centres, built for inference. That's the work of running AI models, not
> training them.

**[MONEY FLOW — OUTBOUND]**
> Amazon's purchases could reach sixty billion dollars, running through twenty thirty-six.

**[MONEY FLOW — THE REVERSAL]**
> But the money moves both ways. Qualcomm handed Amazon a warrant on twenty-five million of
> its own shares, at a hundred sixty-one twenty-six. Roughly four billion dollars. The
> supplier is paying the customer to become a customer.

**[THE MECHANISM]**
> And it vests in stages, as Amazon buys. Three point seven five million shares have vested
> already, on the initial commitments alone.

**[THE OPPORTUNITY]**
> For Qualcomm that's a first Western hyperscaler, and a door out of a smartphone business
> that's losing Apple's modem.

**[THE COMPETITION — mandatory counter-evidence]**
> Now the other side. Amazon already builds its own chips. Trainium, Graviton and Nitro
> passed a twenty-five billion dollar run rate this year, growing triple digits — and
> Trainium three was designed entirely in-house. Qualcomm is selling silicon to a company
> that makes its own. And sixty billion is a ceiling, not a promise. No committed volume, no
> revenue figure, no delivery date was disclosed.

**[CLOSE — actionable, names no winner]**
> So don't pick a winner off the headline. Watch the vesting. Every tranche that vests is
> Qualcomm confirming, in a filing, that Amazon actually bought.

---

## FACT TABLE

| # | Claim in script | Status | Confidence | Source |
|---|---|---|---|---|
| 1 | Deal announced **September 8, 2026** | **Verified** | High | Reuters via Investing.com / The Star; CNBC; Qz — consistent across outlets |
| 2 | Multi-generation collaboration; custom silicon for AWS data centres, **initially for AI inference** | **Verified** | High | Reuters wire; CNBC |
| 3 | Amazon purchases/commercial commitments could total **up to $60 billion**, through **September 2036** | **Verified** | High | CNBC; Reuters wire |
| 4 | Warrant for **25,000,000 Qualcomm shares at $161.26**, ≈ **$4 billion**; expires **Sept 3, 2036** | **Verified** | High | CNBC ("Qualcomm issues Amazon warrants to acquire 25 million shares") |
| 5 | Warrant **vests in stages** on commercial milestones and purchases | **Verified** | High | CNBC |
| 6 | **3.75 million shares have already vested** on initial purchase commitments | **Verified** | Medium-High | CNBC; corroborated by deal-analysis coverage |
| 7 | Optical connectivity work extending to **1.6 terabits per second** (SerDes + optical DSP) | **Verified** — *not in VO, held as backup* | High | Reuters wire; AiCybr |
| 8 | Revenue begins **Qualcomm fiscal Q1 2027 (Dec 2026 quarter)** | **Verified** — *not in VO* | Medium-High | Deal coverage; Qualcomm commentary |
| 9 | Qualcomm diversifying as it faces **loss of the Apple modem business** | **Verified** | High | Reuters wire |
| 10 | AWS custom chips (**Trainium, Graviton, Nitro**) passed a **$25B annual revenue run rate**, triple-digit YoY growth | **Verified** | High | aboutamazon.com (Amazon's own newsroom) |
| 11 | **Trainium 3 designed entirely in-house** at Annapurna Labs, no Broadcom involvement | **Verified** | Medium-High | Tom's Hardware custom-ASIC survey |
| 12 | Announcement carried **no committed volume, no disclosed revenue, no delivery timetable** | **Verified** | High | Analyst commentary across deal coverage |
| 13 | Most Nvidia inference-share erosion accrues to **hyperscalers' own silicon**, not third parties like Qualcomm | **Verified** — *paraphrased into "makes its own"; the projection itself is kept OUT of the VO* | Medium | Analyst estimates in deal coverage |

### Deliberately excluded from the VO
- **The share-price move.** Sources conflict badly — "rises 5%", "surges 9.5%", "jumped nearly
  10%". Intraday versus close, probably. With no way to reconcile it against a primary quote
  from this environment, it stays out. It is also exactly the kind of number that would read as
  a stock call, which the brief rules out.
- **Analyst inference-share projections** (Nvidia ~90% falling to 20–30% by 2028) and the
  **1.5–2% QCT gross-margin dilution** estimate. Both are analyst *estimates*, not company
  figures. `CLAUDE.md` requires estimates be marked as estimates; rather than spend VO time
  hedging them, the argument is made with company-reported figures instead. Kept here as
  context for the pinned comment.
- **No winner is named.** The video states both sides and closes on a thing to watch, not a
  position. No price target, no "buy", no ranking of Qualcomm against Nvidia or Broadcom.

### Egress note affecting verification
`reuters.com`, `cnbc.com`, `theregister.com` and `sec.gov` are all blocked by this
environment's proxy. Every figure above was read from search-index snippets of those pages
rather than the pages themselves, and each was corroborated across at least two independent
queries returning consistent numbers. The figures are unusually consistent across outlets
(they trace to one Reuters wire and one Qualcomm release), which raises confidence — but
**item 6, the 3.75M already-vested figure, is the one to re-read against Qualcomm's own
release or its 8-K before publishing**, since it is the most specific and the least repeated.

---

## SHOT LIST — imagery-first three-layer stack

**BASE** cinematic server-hall and semiconductor imagery, graded near-black and desaturated
**MID** motion graphics — the money-flow diagram, counters, vesting meter, text name-tags
**TOP** hero type + burned-in word-by-word captions, current word highlighted

**HERO SHOT:** macro of a fibre-optic patch panel. One strand lights and a pulse travels
left-to-right. Then a second strand lights and a pulse travels **right-to-left**. Two
directions on one panel — that is the whole thesis, and it is literally the optical
connectivity in the deal.

**BOOKEND:** the server aisle. Video opens pushing down a cold, dark aisle between racks.
Video closes pulling back out of the identical aisle, same camera path reversed.

| # | Beat | BASE imagery | MID graphics | Transition in |
|---|---|---|---|---|
| 1 | "Follow who's getting paid" | Push down a dark server aisle, fans turning, status LEDs | `FOLLOW THE MONEY` scales past frame edges | open on it |
| 2 | "September eighth" | Institutional glass facade at dawn, cold grade | `SEP 8 · 2026` date stamp slams | whip pan |
| 3 | "Qualcomm and Amazon announce" | Two dark monoliths facing each other across a gap | Plain text name-tags: `QUALCOMM` / `AMAZON · AWS` | camera pushes into the gap |
| 4 | "custom silicon … for inference" | Macro — wafer surface, die pattern, raking light | `INFERENCE ≠ TRAINING`; two racks label-split | match-cut, facade→wafer |
| 5 | **"could reach sixty billion dollars"** | Server hall, wide, receding rows | **MONEY FLOW A→Q**: a thick line of light leaves `AMAZON`, crosses to `QUALCOMM`; counter climbs `$0 → $60B`; `UP TO` sits above it in red, small but legible | punch-in |
| 6 | "through twenty thirty-six" | Same hall, long lens compression | `2026 ——— 2036` timeline draws itself | speed ramp |
| 7 | **"the money moves both ways"** | **HERO** — fibre patch panel macro; strand one pulses L→R, strand two pulses R→L | **MONEY FLOW REVERSES**: a second, thinner line leaves `QUALCOMM` back to `AMAZON` | slow push-in, 1-frame white flash on the reversal |
| 8 | "a warrant on twenty-five million shares" | Macro — dark printed contract page, shallow focus, light sweep | `25,000,000 SHARES @ $161.26` counts up; `≈ $4B` | roll transition |
| 9 | "The supplier is paying the customer" | The two monoliths again, now with the return line lit between them | Impact frame: `THE SUPPLIER PAYS THE CUSTOMER` | hard landing + shake |
| 10 | "it vests in stages, as Amazon buys" | Macro — a mechanical ratchet clicking over one tooth at a time | **VESTING METER** fills `3.75M / 25M`, red segment | glitch cut |
| 11 | "a first Western hyperscaler" | Server aisle from a new angle, a door opening at the end | `FIRST WESTERN HYPERSCALER` | type-as-mask wipe |
| 12 | "losing Apple's modem" | Macro — a phone logic board, one component lifted out with tweezers, no branding visible | `MODEM ▼` | whip pan |
| 13 | **"Amazon already builds its own chips"** | Wafer inspection under cold light — the *same* wafer imagery as shot 4, re-lit | Name-tags `TRAINIUM · GRAVITON · NITRO`; counter to `$25B RUN RATE`; `TRIPLE-DIGIT GROWTH ▲` | match-cut back to the wafer |
| 14 | "selling silicon to a company that makes its own" | The two monoliths — but now a third structure stands behind Amazon's | The A→Q flow line **thins** as a second line routes internally | slow reveal |
| 15 | "sixty billion is a ceiling, not a promise" | Server hall, lights dropping out row by row | `$60B` with `UP TO` scaling until it dwarfs the number | speed ramp |
| 16 | "No committed volume, no revenue, no delivery date" | Dark contract page again, three blank fields | Three red strikes land in sequence | punch-in ×3 |
| 17 | "Watch the vesting" | Return to the ratchet macro, one more tooth clicks | Vesting meter ticks up one segment | match-cut |
| 18 | "Amazon actually bought" | **BOOKEND** — pulling back out of the opening server aisle, reversed camera path | `WATCH THE VESTING SCHEDULE` | pull-back |

**Match-cut chain:** facade → wafer → patch panel → ratchet → wafer → server aisle.
**Impact-frame words:** `$60B`, `THE SUPPLIER PAYS THE CUSTOMER`, `UP TO`, `WATCH THE VESTING`.
**Beat rule:** cut or punch in every 1.2–1.8s. No shot past 2s.

### The money-flow animation — the spine of the piece
The brief asked for an animated money flow, and it carries the whole argument, so it is not
decoration. It appears three times and **changes each time**:
1. **Shot 5** — one thick line, Amazon → Qualcomm, $60B. The obvious story.
2. **Shot 7** — a second line lights in the opposite direction. The actual story.
3. **Shot 14** — the outbound line thins as Amazon routes spend to its own silicon. The risk.
Same diagram, three states. A viewer who watches only the graphics still gets the thesis.

### Name-tags, not logos — and why the render can't do otherwise
House style bans real corporate marks, so `QUALCOMM`, `AMAZON · AWS`, `TRAINIUM · GRAVITON ·
NITRO` are plain heavy-condensed text on dark plates. This is also the only option that
actually works: HeyGen generates imagery, and asking a generative model for real trademarks
produces mangled near-miss logos — worse than text on brand accuracy, legal exposure and
house style at once. Real marks would have to be composited as PNG assets in an editor after
the render. See `PRODUCTION.md`.

---

## PACKAGING

**Titles**
1. Follow Amazon's AI Money
2. Qualcomm Is Paying Amazon To Be Its Customer
3. The $60 Billion Number Everyone Misread

**Description**
> On September 8, 2026, Qualcomm and Amazon announced a multi-generation deal for custom AI
> inference silicon in AWS data centres. The headline number is up to $60 billion. The more
> interesting number is the $4 billion warrant travelling in the opposite direction — and
> the vesting schedule attached to it.
>
> We walk the money in both directions, then the competitive problem: Amazon's own chip
> business is already past a $25B run rate. No winner is picked here.
>
> Educational only. Not financial advice.

**Hashtags:** #qualcomm #amazon #aws #aistocks #semiconductors

**Pinned comment**
> Two things deliberately left out of the video: the share-price reaction (sources ranged
> from +5% to +9.5% and I couldn't reconcile them against a primary quote) and analyst
> estimates for inference market share and gross-margin dilution. Company-reported figures
> only in the script. The $60B is a ceiling on purchases, not a committed order.

---

## COMPLIANCE
On-screen card, 0:00–0:04: **"Educational only. Not financial advice."**
No winner named, no price target, no buy/sell framing. Both companies are described through
their own disclosed figures. The close is an instruction to watch a public filing, not to
take a position.
