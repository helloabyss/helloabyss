# YouTube Short — "The Market Closes at Four. Your App Doesn't."

**Runtime target:** ~72–78s (over the 150–170-word guide; every beat carries a fact, so length won over trimming) · **Format:** 1080x1920 · **Style:** house style (`STYLE-GUIDE.md`)
**Style/voice:** Economist + Alex Wright, same as every other short
**Source brief:** Webull help-centre FAQ "All About Overnight Trading", supplied by the user,
cross-checked against the web searches listed in the fact table.

---

## VO SCRIPT (197 words)

**[0:00–0:04] HOOK**
> The stock market closes at four. Your app doesn't.

**[0:04–0:16] DEFINE**
> On Webull, an overnight session runs eight p.m. to four a.m. Eastern, Sunday through
> Thursday. Chain it to pre-market and after-hours, and select stocks and ETFs trade
> twenty-four hours a day, five days a week.

**[0:16–0:31] HOW IT WORKS**
> Your order isn't going to an exchange. It routes to an alternative trading system
> called Blue Ocean. And the rules tighten. Limit orders only. Whole shares only.
> No margin, no shorting, no options. Anything unfilled cancels at four a.m.

**[0:31–0:48] THE HONEST PART**
> Here's the weak spot. Overnight is still under one percent of U.S. share volume.
> Thin books mean wide spreads, and prices that jump on small orders. In August 2024,
> a volume spike hit Blue Ocean. It cancelled over an hour of trades and shut the
> session down.

**[0:48–0:58] THE CATCH**
> One more. Buy between eight and midnight, and your trade is dated the next business
> day. Do that the night before an ex-dividend date, and you miss the dividend.

**[0:58–1:07] WHAT'S NEXT**
> On December sixth, Nasdaq and NYSE Arca are scheduled to open their own overnight
> sessions, with consolidated overnight quotes for the first time.

**[1:07–1:14] CLOSE**
> Until then, check the spread before you click, and set a limit you'd actually accept.

---

## FACT BASE

| Claim | Detail | Source | Confidence |
|---|---|---|---|
| Session hours | Overnight 8:00 PM–4:00 AM ET, Sun–Thu. Pre-market 4:00–9:30 AM, regular 9:30 AM–4:00 PM, after-hours 4:00–8:00 PM | Webull FAQ (user-supplied); confirmed by Webull blog + search | High |
| "24 hours, 5 days" | For **select** securities only — Webull's own qualifier. Script keeps "select" | Webull FAQ | High |
| Launch | Webull launched overnight trading, powered by Blue Ocean ATS, in Nov 2024 | PR Newswire release | High (not in VO) |
| Venue | Executions/quotes come from an overnight ATS; Webull names Blue Ocean's internal risk controls as deciding eligibility | Webull FAQ; Blue Ocean FAQ | High |
| Order rules | Limit only; whole shares only; day orders only, cancelled 4:00 AM if unfilled; no margin; no shorting; no options or bonds; no market/stop/stop-limit/trailing | Webull FAQ | High |
| Short position → $0 BP | Any short position, incl. covered options, sets overnight buying power to $0 | Webull FAQ | High (not in VO — too granular for 60s; in pinned comment) |
| Volume share | Overnight ≈ **0.9%** of NMS share volume in Aug 2026; ADV 144.6M shares, +359% YoY | Secondary summary of SEC staff roundtable memo (File 4-913, Sept 2026). Could not open the primary PDF — egress blocked | Medium. VO says "under one percent" to stay inside the figure |
| Aug 2024 outage | Aug 5, 2024: volume spike after BoJ hike / weak US jobs data. Blue Ocean cancelled trades from ~1:45–3:06 AM ET and halted; Robinhood and ~19 other brokers affected | Bloomberg, CNBC, Markets Media | High. "over an hour" = 81 min |
| Wide spreads / volatility | Extended-hours liquidity thinner, spreads wider, prices more sensitive to small orders | SEC Investor.gov extended-hours bulletin; Webull disclosure | High |
| Trade-date rule | Orders placed 8:00–11:59:59 PM ET get trade date T+1; 12:00–3:59:59 AM get trade date T | Webull FAQ | High |
| Ex-dividend catch | Webull: overnight purchase on the ex-date is not entitled to the dividend. **Derived:** a buy at e.g. 9 PM the evening before the ex-date is dated the ex-date itself, so it also misses the dividend | Webull FAQ + T+1 rule | High for Webull's rule; the "night before" framing is our inference from it — flag if Webull's disclosure contradicts |
| Dec 6, 2026 | Nasdaq and NYSE Arca overnight sessions 9:00 PM–4:00 AM ET; 23h/5d schedule. SIP hours extend to Sun 9 PM–Fri 8 PM from the same date | Nasdaq Equity Trader Alert 2026-46 (title), NYSE extended-hours FAQ v4.0, Euronews, Sidley roundtable note | Medium-high. Some coverage still says "pending SEC approval and SIP readiness" — VO says "scheduled to", not "will" |
| No consolidated overnight quote today | Overnight 8 PM–4 AM sits outside SIP coverage; no NBBO | SAPINOVER / SEC roundtable coverage | Medium-high |

### Deliberately left out of the VO

- **Webull's day-trade counting examples.** Those exist to count day trades under the old
  Pattern Day Trader rule. FINRA scrapped PDT effective **June 4, 2026**, and Webull
  announced it was dropping the $25K minimum and trade counting (see `pdt-short/`).
  Scripting the counting examples would teach viewers a rule that no longer binds at Webull.
  The *trade-date* part of that section still matters, which is why it survives as the
  ex-dividend catch.
- **Step-by-step order entry and the $4.99/month Level 2 subscription.** Tutorial and upsell
  material; it turns an explainer into an ad for one broker.
- **Cash vs. margin buying-power detail.** Accurate but too dense for 60 seconds. Pinned
  comment carries the headline version.

---

## IMAGERY LAYER (house style)

**Hero shot:** extreme macro of a mechanical clock's minute hand sweeping past midnight while
a date wheel flips forward one day, slow-mo. It carries the whole video: the market never
closing, and the trade-date flip that costs you the dividend.
**Bookend:** a financial-district tower at dusk, floors going dark one by one at 4:00. The
video ends on the same tower at 4 AM, nearly all dark, one floor still lit.

| Beat | Shot |
|---|---|
| "closes at four" | Tower at dusk, office floors switching off in sequence, camera pushing up the facade |
| "Your app doesn't." | Push through one still-lit window into darkness; screen glow on a desk, no person |
| "eight p.m. to four a.m." | Time-lapse of a city grid at night, streetlights; timeline graphic draws the four sessions |
| "twenty-four hours, five days" | Clock face ring segments filling in red, 4 AM → 4 AM |
| "alternative trading system … Blue Ocean" | Fibre-optic cables and a dark server aisle, long lens. Plain text name-tag `BLUE OCEAN ATS` — no logo |
| "Limit only. Whole shares. No margin, no shorting, no options." | Steel gates shutting one by one down a corridor; each gets a red strike-through label |
| "cancels at four a.m." | Split-flap board clearing to blank |
| "under one percent" | A single lit window in a dark tower; bar counts up to 0.9% against a full-height 100% bar |
| "wide spreads" | Two cranes / bridge spans pulling apart, gap widening; BID / ASK tags drift apart |
| "August 2024 … cancelled … shut down" | Chart draws, then cracks and drops; red `TRADES CANCELLED 1:45–3:06 AM` stamp |
| **"dated the next business day"** | **HERO** — clock hand sweeps past midnight, date wheel flips |
| "miss the dividend" | Envelope / cheque slot snapping shut before it arrives |
| "December sixth, Nasdaq and NYSE Arca" | Exchange-style stone facade at night lights floor by floor. Plain text name-tags only |
| "consolidated overnight quotes" | Scattered price tickers merge into one line |
| Close | Return to the tower at 4 AM — one floor lit. Type: `CHECK THE SPREAD. SET YOUR LIMIT.` |

Match-cut chain: lit window → server aisle → clock face → date wheel.
Impact-frame words: "DOESN'T", "BLUE OCEAN", "CANCELLED", "MISS THE DIVIDEND".

---

## HEYGEN BRIEF (from STYLE-GUIDE.md template)

> Create a ~75-second vertical (9:16) YouTube Short for a FACELESS finance channel.
>
> **CRITICAL:** NO avatar, NO presenter, NO human face anywhere. Voiceover only.
> Use this narration script VERBATIM — do not rewrite, shorten, or add to it:
> "[paste VO SCRIPT above, quotes only]"
>
> **LAYER STACK — imagery-first, three layers:**
> 1. BASE — cinematic photographic imagery filling the frame, the foundation of every scene.
> 2. MID — motion graphics over that imagery.
> 3. TOP — hero typography and burned-in word-by-word captions, current word highlighted.
>
> **IMAGERY BY BEAT:** [paste IMAGERY LAYER table]. HERO SHOT: macro of a clock hand sweeping
> past midnight as a date wheel flips forward, slow-mo, on "dated the next business day".
> BOOKEND: open on a financial tower going dark floor by floor at 4 PM; close on the same
> tower at 4 AM with one floor still lit.
>
> **MOTION:** Treat scenes as 3D space — push the camera THROUGH elements, hard parallax
> between layers, foreground streaking past the lens. Hero words scale past frame edges;
> letters arrive individually with overshoot; 1–2 frame white flash and screen shake on the
> biggest landings. No plain cuts — match-cut morphs, type-as-mask reveals, whip transitions
> with motion blur. Numbers count up physically; charts draw themselves then crack and drop
> on negative beats. Continuous motion in every frame; speed ramps into key words. Cut or
> punch in every 1.2–1.8s, no shot past 2s.
>
> **LOOK:** Strict three-colour editorial palette — near-black, white, one red accent.
> Grade imagery dark and desaturated; reserve red for graphics and type. Captions legible at
> all times — dark scrim behind text over busy plates.
>
> **HARD CONSTRAINTS:** No human faces or identifiable people. No real corporate logos —
> plain text name-tags only (WEBULL, BLUE OCEAN ATS, NASDAQ, NYSE ARCA as text). No neon,
> gradients, sparkles, emoji, subscribe animations or clickbait arrows. Show "Educational
> only. Not financial advice." in the first 4 seconds.
>
> **TONE:** Dry, confident, analytical newsroom. Cinematic, not a commercial. A neutral
> explainer that includes the negative data, not a promo for any broker.

Settings: `mode: chat`, `orientation: portrait`,
style `e7f9a12679ec426099db7646b70a4639`, voice `0db3abd83c74452fb2460b0dd113daad`.

---

## PACKAGING

**Titles**
1. The Market Closes at 4. Your App Doesn't.
2. 24-Hour Stock Trading: The Rules Nobody Reads
3. Overnight Trading Can Cost You a Dividend

**Description**
> Some brokers now let you trade select U.S. stocks and ETFs overnight, 8 PM to 4 AM ET,
> through an alternative trading system rather than an exchange. Here's how the overnight
> session works on Webull, the restrictions (limit orders only, no margin, no shorting),
> the August 2024 outage, the trade-date rule that can cost you a dividend, and what
> changes when Nasdaq and NYSE Arca are scheduled to open overnight sessions on
> December 6, 2026.
>
> Sources: Webull "All About Overnight Trading" FAQ; Bloomberg / CNBC coverage of
> Aug 5, 2024; SEC Investor.gov extended-hours bulletin; Nasdaq and NYSE extended-hours
> notices. Not sponsored. Educational only. Not financial advice.

**Hashtags:** #investing #stockmarket #overnighttrading #24hourtrading #webull

**Pinned comment**
> Two rules worth knowing before you try it: overnight buying power uses cash only (no
> margin), and on Webull, holding any short position, even a covered option, drops your
> overnight buying power to $0. Read your broker's Extended Hours Trading Disclosure first.

---

## COMPLIANCE
On-screen 0:00–0:04: **"Educational only. Not financial advice."**
Not sponsored by Webull. If that changes, it must be disclosed on screen and in the description.
