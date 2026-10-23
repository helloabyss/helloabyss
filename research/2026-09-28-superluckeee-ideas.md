# Idea scan — @SuperLuckeee (X), 2026-09-28

**Access:** X.com, Thread Reader, YouTube and both of the account's websites are blocked from this environment.
The account was read only through the post text that search engines index. This is a partial sample
of their feed, not a full scan.

## Who they are

- Esther Cho and Michael Luu (Aevitas Partners, LLC, founded 2018). The account sells a paid trading
  community: General Access is $145/mo and Premium $195/mo, run through Whop and Discord.
- They teach day and swing trading: options, SPX credit spreads, ICT, VPA and futures.
- Their bio and YouTube headline claim "$350 to $17 million". Other places say "$350 to $1M in 9 months"
  and "$250k to $8M in a year". **None of these is independently verified. Never repeat them as fact.**

## Posts found (topic signals)

| Date | Post (indexed text) | Signal |
|---|---|---|
| 2026-08-17 | "When yields spike fast $SPY can crash 20% in 1 day. 6 things are pushing yields up at once." (~41k views) | Crash fear + yields |
| 2026 (Apr) | Options flow: "Calls: SPXW $574M NVDA $332M… Puts: SPXW $287M PLTR $103M…" "skewed bearish" | Options-flow reading |
| 2026 | "NVDA explosion 💥 If you lost money on NVDA calls DM us for a new trade." | NVDA calls |
| 2026 | "$AVGO everything you need to know for earnings" | Earnings plays |
| 2026 | "Short term target highs for the week on megacaps are at resistance" (AAPL MSFT NVDA AVGO META TSLA AMZN GOOGL) | Megacap levels |
| 2026-06-01 | "BEARS shorting the $SPY" | Shorting |

The audience engages with **crash fear, same-day options, and "smart money" flow**. Those make good
topics for an explainer. Our angle is the one this channel always takes: the evidence, including
where the popular framing is wrong.

## Ideas, ranked

### 1. "Can the stock market really fall 20% in one day?" (Short, ~60s) — best pick
Hook: posts saying SPY "can crash 20% in 1 day" get tens of thousands of views. The rules say something else.
- The S&P 500's worst day ever was −20.47% on 19 Oct 1987 (Black Monday). SPY didn't exist until 1993. **HIGH**
- The worst day in the modern era was −11.98% on 16 Mar 2020. It ranks third ever, after 1987 and 28 Oct 1929 (−12.94%). **HIGH**
- Since 1987, market-wide circuit breakers pause trading at −7% and −13%. **At −20% trading stops for the
  rest of the day.** A regular-session close below −20% is effectively blocked. **HIGH** (SEC/Investor.gov)
- Disconfirming data (include it): the rules don't stop overnight futures moves, gaps at the next open, or a
  slow crash spread over several days. 2020 fell about 34% in five weeks.
- Close (actionable): size positions for a −30% month, not a −20% day. Know where your stop orders would fill on a gap.
- ⚠ **Framing-reuse watch:** the 10-year yield has been used twice already (ARCHIVE.md). Lead with circuit breakers, not yields.

### 2. "0DTE: the options trade retail loves — and the data on who wins" (6-min long-form)
- About 75% of retail S&P 500 options trades were 0DTE. Retail lost an average of ~$358k/day after daily expiries
  began (May 2022). About 60% of the losses came from transaction costs, and market makers captured them.
  Source: Beckmeyer, Branger & Gayda, SSRN 4404704. **HIGH** (peer-circulated working paper; state the sample window)
- Explain the SPX credit spread fairly: it collects time decay on most days and takes a large loss on a tail day.
  Show the payoff shape.
- Disconfirming data: sellers of 0DTE premium, not buyers, were closer to break-even in the study. Say so.
- Close: if you trade them, count fees and spreads first, and cap the risk per trade.

### 3. "What 'options flow' can't tell you" (Short, ~60s)
- Take the post's own numbers ("SPXW $574M calls") as the example.
- Explain what the number can't show:
  - Premium totals don't say whether the trade was a buy or a sell.
  - Big put buying is often a hedge on stock the buyer already owns.
  - The market maker on the other side hedges too, and that hedging can be what actually moves price.
- Status **MEDIUM**: the sources are practitioner explainers. Get an exchange or academic source before scripting.
- Close: flow is a question, not a signal. Check open interest the next day before you read direction into it.

### 4. "Day trading for a living: what 25 years of data show" (6-min long-form)
- Brazil (Chague, De-Losso & Giovannetti, 2019): 97% of those who day-traded 300+ days lost money. 1.1% earned
  more than minimum wage. There was no evidence that traders learned over time. **HIGH**
- Taiwan (Barber, Lee, Liu & Odean): under 1% earned predictable profits after fees, across 15 years of market-wide data. **HIGH**
- Second half: how to judge *any* trading-course claim.
  - An audited or broker-statement track record, not screenshots.
  - Survivorship: you only see the winners' posts.
  - Whether the money comes from subscriptions or from trading.
- Keep it generic. **Do not name or target any individual educator.**

### 5. "How to read an earnings 'implied move' before you bet on one" (Short)
- From the "$AVGO everything you need for earnings" genre.
- Teach the at-the-money straddle ≈ expected move, and how IV crush means you can be right on direction and still lose.
- Each figure needs a live web check before scripting (per CLAUDE.md).

## Rules for using this scan
- Use their posts as **topic signals only**. No screenshots, no handle on screen, no quoting their performance claims.
  Anything else invites copyright or defamation trouble.
- Every figure above must go into the episode's `SCRIPT.md` fact table and be re-verified on the day of scripting.
- Keep all rates and Fed figures `[OPEN]`: the September 2026 Fed decision (hike to 3.75–4.00%) comes from a
  search snippet only, because the CNBC page is blocked. The UMich year-ahead expectation was 4.3% in August
  (prelim), also from a snippet.

## Sources
- Account and business: x.com/SuperLuckeee (search index only); whop.com/superluckeee; whop.com/blog/superluckeee-trading-review
- Black Monday: en.wikipedia.org/wiki/Black_Monday_(1987)
- 16 Mar 2020: insights.tradestation.com/2020/03/18/sp-500-records-worst-one-day-decline-since-1987/
- Circuit breakers: investor.gov (Stock Market Circuit Breakers glossary); schwab.com/learn/story/what-are-stock-market-circuit-breakers
- 0DTE: papers.ssrn.com/sol3/papers.cfm?abstract_id=4404704
- Brazil: papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101
- UMich: tradingeconomics.com/united-states/michigan-inflation-expectations
